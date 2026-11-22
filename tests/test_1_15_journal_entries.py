"""Check the 1.15 port against captured pre-port contracts and current native code.

These assertions preserve source behaviour; native outcome evaluation and GUI
rendering remain DP's engine checks.
"""
import hashlib
import json
from pathlib import Path
import re
import unittest

from tests.je_outcomes import outcome_nodes
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import extract_braced_object, top_level_matches
from tools.validate import find_game_root

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = json.loads((ROOT / 'Docs/compatibility/evidence/1_15_0_journal_implementation/contracts.json').read_text())
GAME = find_game_root(None)
CHIEFDOMS_AMENDMENTS = json.loads((ROOT/'Docs/compatibility/chiefdoms_journal_amendments_2026_11_10.json').read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def definition(path, key):
    source = path.read_text(encoding='utf-8-sig')
    pattern = re.compile(r'^(?:(?:TRY_)?REPLACE:)?' + re.escape(key) + r'\s*=\s*\{', re.M)
    matches = top_level_matches(pattern, source)
    assert len(matches) == 1, key
    return statements(extract_braced_object(source, matches[0].start()))


class JournalMigrationTests(unittest.TestCase):
    def test_every_authored_trigger_effect_and_nonterminal_contract_is_preserved(self):
        self.assertEqual(27, len(CONTRACTS['journals']))
        for record in CONTRACTS['journals']:
            if record.get('native_rebase'):
                continue
            with self.subTest(journal=record['key']):
                nodes = definition(ROOT / record['file'], record['key'])
                self.assertEqual([('activation_description', '=', [('always', '=', 'yes')])],
                                 [n for n in nodes if n[0] == 'activation_description'])
                amendment = CHIEFDOMS_AMENDMENTS.get(record['key'])
                if amendment:
                    self.assertEqual(record['retained_fields_sha256'], amendment['prior_retained_fields_sha256'])
                self.assertEqual(amendment['retained_fields_sha256'] if amendment else record['retained_fields_sha256'],
                                 digest([n for n in nodes if n[0] not in ('outcome', 'activation_description')]))
                if record['key'] == 'je_sb_cape_politics':
                    # The authorised playtest correction splits this dispatcher
                    # into five previews. The captured dispatcher remains pinned
                    # here; test_1850_playtest_fixes executes both forms across
                    # overlapping conditions and compares ordered effects.
                    self.assertEqual(6, sum(k == 'outcome' for k, _, _ in nodes))
                    old = statements((ROOT / 'Docs/compatibility/evidence/1_15_0_playtest_1850_fixes_2026_11_07/cape_completion_before.txt').read_text())
                    nodes = [n for n in nodes if n[0] != 'outcome'] + [
                        ('outcome', '=', old), ('outcome', '=', outcome_nodes(nodes, 'invalid'))]
                self.assertEqual(len(record['outcomes']), sum(n[0] == 'outcome' for n in nodes))
                self.assertEqual([outcome_nodes(nodes, e['kind']) for e in record['outcomes']], [v for k, _, v in nodes if k == 'outcome'])
                for expected in record['outcomes']:
                    fields = {k: v for k, _, v in outcome_nodes(nodes, expected['kind'])}
                    for key, value in expected.items():
                        if key.endswith('_sha256'):
                            field = key.removesuffix('_sha256')
                            if record['key'] == 'je_sb_bst_ora_frontier' and expected['kind'] == 'complete':
                                if field == 'event_outcome_desc':
                                    self.assertNotIn(field, fields)  # Single-choice presentation, checked separately.
                                    continue
                                if field == 'effect':
                                    def without_preview(ns):
                                        return [(k, op, without_preview(v) if isinstance(v, list) else v)
                                                for k, op, v in ns if k != 'show_as_tooltip']
                                    self.assertEqual(value, digest(without_preview(fields[field])))
                                    continue
                            self.assertEqual(value, digest(fields[field]), (record['key'], expected['kind'], key))
                        elif key in ('header', 'effect_header'):
                            self.assertEqual(value, fields[key])

    def test_no_legacy_callbacks_and_every_outcome_has_required_shape(self):
        legacy = {'complete', 'fail', 'invalid', 'on_complete', 'on_fail', 'on_invalid', 'on_timeout',
                  'custom_completion_header', 'custom_failure_header', 'custom_on_completion_header', 'custom_on_failure_header',
                  'event_outcome_completed_desc', 'event_outcome_failed_desc'}
        for record in CONTRACTS['journals']:
            nodes = definition(ROOT / record['file'], record['key'])
            self.assertIn('activation_description', [k for k, _, _ in nodes], record['key'])
            self.assertFalse(legacy.intersection(k for k, _, _ in nodes), record['key'])
            for key, _, value in nodes:
                if key != 'outcome':
                    continue
                fields = {k: v for k, _, v in value}
                flags = {k for k, _, _ in fields.get('flags', [])}
                self.assertIn('conclusion_desc', fields)
                self.assertIn('effect', fields)
                if 'timeout' in flags:
                    self.assertNotIn('trigger', fields)
                else:
                    self.assertIn('trigger', fields)
                if 'invalid_outcome' in flags:
                    self.assertIn('hidden', flags)
                if 'hidden' not in flags:
                    self.assertIn('header', fields)
                    self.assertIn('effect_header', fields)

    def test_shared_corridor_settles_once_and_institutions_only_invalidate(self):
        corridor = definition(ROOT / 'common/journal_entries/1-11_sb_bechuanaland_corridor.txt', 'je_sb_bechuanaland_corridor')
        for kind in ('complete', 'fail', 'invalid'):
            self.assertNotIn('effect_all_involved', {k for k, _, _ in outcome_nodes(corridor, kind)})
        zulu = definition(ROOT / 'common/journal_entries/1-03_sb_zulu_kingdom.txt', 'je_sb_zulu_kingdom')
        self.assertEqual(1, sum(k == 'outcome' for k, _, _ in zulu))
        self.assertTrue(outcome_nodes(zulu, 'invalid'))

    def test_bar_arithmetic_and_order_are_unchanged(self):
        styling = {'double_sided_bad', 'progress_texture', 'background_texture', 'glow_texture', 'glow_line_texture', 'marker'}
        self.assertEqual(4, sum(r['custom'] for r in CONTRACTS['bars']))
        for record in CONTRACTS['bars']:
            nodes = definition(ROOT / record['file'], record['key'])
            if record['key'] == 'sb_zululand_chiefdom_balance_bar':
                # 12 November: activism is a single red fill in both the full JE
                # and CMF outliner. Keep the historical arithmetic contract.
                self.assertIn(('default_bad', '=', 'yes'), nodes)
                self.assertFalse(styling.intersection(k for k, _, _ in nodes))
                nodes.remove(('default_bad', '=', 'yes'))
                widget = (ROOT / 'gui/sb_zululand_chiefdoms_progress_bars.gui').read_text()
                self.assertIn('visible = "[ScriptedProgressBar.IsDefaultBad]"', widget)
                self.assertNotIn('ScriptedProgressBar.IsDynamic', widget)
            self.assertEqual(record['retained_fields_sha256'], digest([n for n in nodes if n[0] not in styling]), record['key'])
            fields = {k: v for k, _, v in nodes}
            self.assertNotIn('double_sided_bad', fields)
            if record['custom'] and record['key'] != 'sb_zululand_chiefdom_balance_bar':
                self.assertEqual('yes', fields['marker'])
                if GAME:
                    for key in ('progress_texture', 'background_texture', 'glow_texture', 'glow_line_texture'):
                        self.assertTrue((GAME / fields[key].strip('"')).is_file(), fields[key])

    @unittest.skipUnless(GAME, 'requires installed Vanilla')
    def test_monarchy_is_current_native_except_the_two_boer_guards(self):
        native = definition(GAME / 'common/journal_entries/00_abolish_monarchy.txt', 'je_abolish_monarchy')
        sb = definition(ROOT / 'common/journal_entries/zz_sb_abolish_monarchy_override.txt', 'je_abolish_monarchy')
        sb.remove(('possible', '=', [('NOT', '=', [('country_has_primary_culture', '=', 'cu:boer')])]))
        invalid = outcome_nodes(sb, 'invalid')
        trigger = next(v for k, _, v in invalid if k == 'trigger')
        self.assertEqual('OR', trigger[0][0])
        self.assertEqual(('country_has_primary_culture', '=', 'cu:boer'), trigger[0][2][0])
        trigger[:] = trigger[0][2][1:]
        self.assertEqual(native, sb)

    def test_bechuanaland_dynamic_bar_has_effective_cmf_fallback(self):
        cmf = (ROOT.parent / 'Community Mod Framework/gui/com_gui_progressbars.gui').read_text(encoding='utf-8-sig')
        for name in ('com_journal_entry_progress_bars', 'com_journal_outliner_progress_bars'):
            with self.subTest(renderer=name):
                renderer = extract_braced_object(cmf, cmf.index(f'type {name} ='))
                fallback = re.search(r'container\s*=\s*\{\s*visible\s*=\s*"\[Not\(ComProgressBar.IsSet\)\]"', renderer)
                self.assertIsNotNone(fallback)
                native = extract_braced_object(renderer, fallback.start())
                self.assertEqual(1, native.count('scripted_progressbar_dynamic = {'))
                self.assertIn('visible = "[ScriptedProgressBar.IsDynamic]"', native)
                dynamic = extract_braced_object(native, native.index('scripted_progressbar_dynamic = {'))
                self.assertIn('ScriptedProgressBar.GetPeriodicProgressBreakdown', dynamic)
                styled = extract_braced_object(renderer, renderer.index('com_progressbar_dynamic = {'))
                self.assertIn('And(ScriptedProgressBar.IsDynamic, Not(ComProgressBarBaseColor.IsSet))', styled)
        self.assertNotIn('ScriptedProgressBar.IsDoubleSidedBad', (ROOT / 'gui/sb_zululand_chiefdoms_progress_bars.gui').read_text())


if __name__ == '__main__':
    unittest.main()
