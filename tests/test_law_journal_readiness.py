"""Law JE call sites and deferred delivery; native scheduling remains a DP check."""
from copy import deepcopy
from pathlib import Path
import unittest

from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import find_object
from tools.validate import find_game_root

ROOT = Path(__file__).resolve().parents[1]
GAME = find_game_root(None)
CMF = ROOT.parent / 'Community Mod Framework'
LAW_PATCH = 'common/laws/zz_sb_law_journal_readiness.txt'
EFFECT_PATCH = 'common/scripted_effects/zz_sb_law_journal_readiness_effects.txt'
HELPERS = {'sb_add_'+name+'_journal_when_ready': 'je_'+name for name in (
    'technocracy', 'king_in_parliament', 'divided_monarchists',
    'spain_provisional_government', 'abolish_monarchy')}
LAW_SOURCES = {
    **{k: 'common/laws/00_distribution_of_power.txt' for k in (
        'law_technocracy', 'law_landed_voting', 'law_wealth_voting',
        'law_census_voting', 'law_universal_suffrage', 'law_single_party_state')},
    'law_monarchy': 'common/laws/00_governance_principles.txt',
    'law_social_monarchy': 'common/laws/00_governance_principles.txt',
}
EFFECT_SOURCES = {
    'transition_off_of_monarchy_effects': 'common/scripted_effects/00_victoria_ep2_scripted_effects.txt',
    'country_launch_abolish_monarchy_effect': 'common/scripted_effects/00_victoria_on_actions_effects.txt',
}


def read(path): return path.read_text(encoding='utf-8-sig')


def objects():
    for key, rel in {**LAW_SOURCES, **EFFECT_SOURCES}.items():
        patch = ROOT / (LAW_PATCH if key in LAW_SOURCES else EFFECT_PATCH)
        if patch.exists(): yield key, find_object(read(patch), key, directive='REPLACE')
        elif key == 'law_monarchy':
            yield key, find_object(read(CMF/'common/laws/com_governance_principles.txt'), key, directive='REPLACE_OR_CREATE')
        else: yield key, find_object(read(GAME/rel), key)
    yield 'sb_ensure_inboekstelsel_journal_entry', find_object(read(ROOT/'common/scripted_effects/sb_inboekstelsel_effects.txt'), 'sb_ensure_inboekstelsel_journal_entry')


def journal_calls(nodes):
    for key, op, value in nodes:
        if key == 'add_journal_entry' or key in HELPERS: yield (key, op, value)
        elif isinstance(value, list): yield from journal_calls(value)


def journal_for(call):
    if call[0] == 'sb_ensure_inboekstelsel_journal_entry': return 'je_sb_inboekstelsel_system'
    if call[0] in HELPERS: return HELPERS[call[0]]
    fields = dict((k, v) for k, _, v in call[2])
    return fields.get('JOURNAL', fields.get('type'))


def country(journal):
    tag = {'je_divided_monarchists': 'FRA', 'je_spain_provisional_government': 'SPA',
           'je_sb_inboekstelsel_system': 'TRN'}.get(journal, 'TEST')
    laws = {'je_technocracy': {'law_technocracy'},
            'je_king_in_parliament': {'law_monarchy', 'law_landed_voting'},
            'je_abolish_monarchy': {'law_presidential_republic'},
            'je_sb_inboekstelsel_system': {'law_discrete_inboekstelsel'}}.get(journal, {'law_monarchy'})
    return dict(tag=tag, laws=laws, journals=set(), alive=True, ai_ready=True,
                variables={'king_in_parliament_possible', 'sb_inboekstelsel_reopen_required_var'},
                enacting=None, is_revolutionary=False, is_secessionist=False,
                ideologies=set(), culture='boer')


class Runtime:
    def __init__(self):
        self.lobby_ready = True
        self.queue = []
        self.root = country('unrelated')
        self.triggers = {}
        for rel in ('common/scripted_triggers/sb_law_journal_readiness_triggers.txt',
                    'common/scripted_triggers/sb_boer_conventions_triggers.txt'):
            path = ROOT/rel
            if path.exists():
                from tools.check_override_inventory import extract_top_level_blocks
                self.triggers.update({k: statements(v) for k, v in extract_top_level_blocks(read(path)).items()})

    def gate(self, nodes, owner):
        results = []
        for key, op, value in nodes:
            if key in ('OR', 'AND', 'NOT', 'NOR'):
                values = [self.gate([n], owner) for n in value]
                result = {'OR': any(values), 'AND': all(values), 'NOT': not any(values), 'NOR': not any(values)}[key]
            elif key in self.triggers: result = self.gate(self.triggers[key], owner) == (value == 'yes')
            elif key == 'has_global_variable': result = self.lobby_ready
            elif key == 'has_variable': result = value in owner['variables']
            elif key == 'has_journal_entry': result = value in owner['journals']
            elif key == 'is_country_alive': result = owner['alive'] == (value == 'yes')
            elif key in ('has_law', 'has_law_or_variant'): result = value.removeprefix('law_type:') in owner['laws']
            elif key == 'is_enacting_law': result = value.removeprefix('law_type:') == owner['enacting']
            elif key == 'country_definition': result = value.removeprefix('cd:') == owner['tag']
            elif key == 'country_has_primary_culture': result = value.removeprefix('cu:') == owner['culture']
            elif key.startswith('c:'): result = key[2:] == owner['tag'] and value.lower() == 'this'
            elif key in ('is_revolutionary', 'is_secessionist'): result = owner[key] == (value == 'yes')
            elif key == 'has_dlc_feature': result = True  # SB requires all DLC.
            elif key == 'game_date': result = op == '>'  # These fixtures run in 1856.
            elif key == 'ig:ig_landowners': result = self.gate(value, owner)
            elif key == 'has_ideology': result = value.removeprefix('ideology:') in owner['ideologies']
            else: raise AssertionError(('unmodelled condition', key))
            results.append(result)
        return all(results)

    def effect(self, nodes, owner):
        matched = False
        for key, op, value in nodes:
            if key in ('if', 'else'):
                if key == 'if': matched = False
                fields = dict((k, v) for k, _, v in value)
                if not matched and self.gate(fields.get('limit', []), owner):
                    matched = True
                    self.effect([n for n in value if n[0] != 'limit'], owner)
            elif key in HELPERS:
                body = find_object(read(ROOT/EFFECT_PATCH), key)
                self.effect(statements(body), owner)
            elif key == 'sb_ensure_inboekstelsel_journal_entry':
                self.effect(statements(find_object(read(ROOT/'common/scripted_effects/sb_inboekstelsel_effects.txt'), key)), owner)
            elif key == 'set_variable':
                owner['variables'].add(dict((k, v) for k, _, v in value)['name'])
            elif key == 'add_journal_entry':
                if not owner['ai_ready']: raise AssertionError('JE before country AI creation')
                journal = dict((k, v) for k, _, v in value)['type']
                if journal in owner['journals']: raise AssertionError('duplicate JE')
                owner['journals'].add(journal)
            elif key == 'trigger_event':
                fields = dict((k, v) for k, _, v in value)
                assert fields['days'] == '1'
                event = dict((k, v) for k, _, v in statements(find_object(read(ROOT/'events/sb_law_journal_events.txt'), fields['id'])))
                # Admit the request even if native code checks event eligibility when
                # scheduling. Readiness belongs in the deferred immediate, not its trigger.
                if self.gate(event.get('trigger', []), owner): self.queue.append((fields['id'], owner))
            else: raise AssertionError(('unmodelled effect', key))

    def deliver(self):
        queued, self.queue = self.queue, []
        for event, owner in queued:
            source = find_object(read(ROOT/'events/sb_law_journal_events.txt'), event)
            fields = dict((k, v) for k, _, v in statements(source))
            # Exercise checks at both boundaries without claiming native consumption timing.
            if self.gate(fields.get('trigger', []), owner): self.effect(fields['immediate'], owner)


@unittest.skipIf(GAME is None or not CMF.is_dir(), 'installed Vanilla and CMF required')
class LawJournalReadinessTests(unittest.TestCase):
    def calls(self):
        calls = [(name, call) for name, source in objects() if name != 'sb_ensure_inboekstelsel_journal_entry'
                 for call in journal_calls(statements(source))]
        calls.append(('sb_ensure_inboekstelsel_journal_entry', ('sb_ensure_inboekstelsel_journal_entry', '=', 'yes')))
        self.assertEqual(13, len(calls))
        return calls

    def test_call_sites_defer_unfinished_countries_and_preserve_ready_activation(self):
        for name, call in self.calls():
            journal = journal_for(call)
            for lobby, alive in ((True, False), (False, True), (False, False), (True, True)):
                with self.subTest(caller=name, journal=journal, lobby=lobby, alive=alive):
                    rt = Runtime(); rt.lobby_ready = lobby; foreign = deepcopy(rt.root)
                    owner = country(journal); owner.update(alive=alive, ai_ready=lobby and alive)
                    rt.effect([call], owner)
                    if lobby and alive:
                        self.assertEqual({journal}, owner['journals']); self.assertFalse(rt.queue)
                    else:
                        self.assertFalse(owner['journals']); self.assertEqual(1, len(rt.queue))
                        # Duplicate inheritance callbacks must not create duplicate entries.
                        rt.effect([call], owner)
                        owner.update(alive=True, ai_ready=True); rt.lobby_ready = True
                        rt.deliver(); self.assertEqual({journal}, owner['journals'])
                    self.assertEqual(foreign, rt.root)

    def test_delivery_rechecks_law_and_existing_journal_and_country_readiness(self):
        for name, call in self.calls():
            journal = journal_for(call)
            for changed in ('law', 'dead', 'existing', 'startup'):
                with self.subTest(caller=name, journal=journal, changed=changed):
                    rt = Runtime(); owner = country(journal); owner.update(alive=False, ai_ready=False)
                    rt.effect([call], owner)
                    owner.update(alive=True, ai_ready=True)
                    if changed == 'law': owner['laws'].clear()
                    elif changed == 'dead': owner.update(alive=False, ai_ready=False)
                    elif changed == 'startup': rt.lobby_ready = False
                    else: owner['journals'].add(journal)
                    rt.deliver()
                    self.assertEqual({journal} if changed == 'existing' else set(), owner['journals'])
                    self.assertFalse(rt.queue)  # No permanent polling or stale retries.

    def test_all_other_native_and_cmf_definition_bytes_are_preserved(self):
        for name, source in objects():
            if name not in LAW_SOURCES and name not in EFFECT_SOURCES: continue
            restored = source.removeprefix('REPLACE:')
            for helper, journal in HELPERS.items():
                restored = restored.replace(helper+' = yes', 'add_journal_entry = { type = '+journal+' }')
            if name == 'law_monarchy':
                native = find_object(read(CMF/'common/laws/com_governance_principles.txt'), name, directive='REPLACE_OR_CREATE').removeprefix('REPLACE_OR_CREATE:')
            else: native = find_object(read(GAME/({**LAW_SOURCES, **EFFECT_SOURCES}[name])), name)
            self.assertEqual(native, restored, name)

    def test_cancelled_inboekstelsel_delivery_leaves_no_reservation_and_can_retry(self):
        rt = Runtime(); owner = country('je_sb_inboekstelsel_system')
        owner.update(alive=False, ai_ready=False)
        call = ('sb_ensure_inboekstelsel_journal_entry', '=', 'yes')
        rt.effect([call], owner)
        self.assertNotIn('sb_inboekstelsel_reopen_pending_var', owner['variables'])
        owner.update(alive=True, ai_ready=True); owner['laws'].clear()
        rt.deliver()
        self.assertFalse(owner['journals'])
        self.assertNotIn('sb_inboekstelsel_reopen_pending_var', owner['variables'])
        owner['laws'].add('law_discrete_inboekstelsel')
        rt.effect([call], owner)
        self.assertEqual({'je_sb_inboekstelsel_system'}, owner['journals'])
        self.assertIn('sb_inboekstelsel_reopen_pending_var', owner['variables'])

    def test_deferred_native_exclusions_and_enactment_cancellation(self):
        calls = {journal_for(call): call for _, call in self.calls()}
        cases = [
            ('je_king_in_parliament', lambda c: c['variables'].discard('king_in_parliament_possible')),
            ('je_divided_monarchists', lambda c: c['variables'].add('one_true_french_dynasty')),
            ('je_divided_monarchists', lambda c: c.update(tag='GBR')),
            ('je_spain_provisional_government', lambda c: c.update(is_revolutionary=True)),
            ('je_spain_provisional_government', lambda c: c.update(is_secessionist=True)),
            ('je_abolish_monarchy', lambda c: c['variables'].add('monarchy_stamped_out_var')),
            ('je_abolish_monarchy', lambda c: c['variables'].add('rcw_russian_faction')),
            ('je_abolish_monarchy', lambda c: c['ideologies'].add('ideology_republican_paternalistic')),
        ]
        for journal, change in cases:
            with self.subTest(journal=journal, change=change):
                rt = Runtime(); owner = country(journal); owner.update(alive=False, ai_ready=False)
                rt.effect([calls[journal]], owner)
                owner.update(alive=True, ai_ready=True); change(owner); rt.deliver()
                self.assertFalse(owner['journals'])
        for cancelled in (False, True):
            rt = Runtime(); owner = country('je_abolish_monarchy')
            owner.update(alive=False, ai_ready=False, laws={'law_monarchy'}, enacting='law_council_republic')
            rt.effect([calls['je_abolish_monarchy']], owner)
            owner.update(alive=True, ai_ready=True)
            if cancelled: owner['enacting'] = None
            rt.deliver()
            self.assertEqual(set() if cancelled else {'je_abolish_monarchy'}, owner['journals'])


if __name__ == '__main__': unittest.main()
