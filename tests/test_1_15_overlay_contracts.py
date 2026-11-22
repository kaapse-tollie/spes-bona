"""Full native-body parity around the narrow SB compatibility additions."""
from pathlib import Path
import re
import unittest

from tools.check_override_inventory import extract_braced_object, find_object
from tools.validate import find_game_root
from tests.test_usuthu_movement_contest import parse

ROOT = Path(__file__).resolve().parents[1]
GAME = find_game_root(None)


@unittest.skipIf(GAME is None, "installed Vanilla sources unavailable")
class OverlayContracts(unittest.TestCase):
    def test_shared_outliner_row_only_restores_native_bar_spacing(self):
        source = (ROOT / 'gui/zzz_sb_international_situation_outliner.gui').read_text(encoding='utf-8-sig')
        cmf = (ROOT.parent / 'Community Mod Framework/gui/00_com_outliner_ongoing_types.gui').read_text(encoding='utf-8-sig')
        header = 'type com_outliner_entry = journal_entry'
        self.assertEqual([header], re.findall(r'\btype\s+\w+\s*=\s*\w+', source))
        actual = extract_braced_object(source, source.index(header))
        expected = extract_braced_object(cmf, cmf.index(header))
        spacing = 'blockoverride "progressbars_spacing" { spacing = 6 }'
        self.assertEqual(1, actual.count(spacing))
        self.assertEqual(expected, actual.replace(spacing, 'blockoverride "progressbars_spacing" {}'))
        organization = "ComJournalEntryGroupSGui('com_international_organization_journal_entry_group_sgui')"
        situation = "ComJournalEntryGroupSGui('com_international_situation_journal_entry_group_sgui')"
        placements = {
            'outliner_journal_entries': (f'Not({organization})', f'Not({situation})'),
            'com_outliner_international_situations_container': (f'Not({organization})', situation),
            'com_outliner_international_organization_entries_container': (organization, f'Not({situation})'),
        }
        for container, (org_filter, situation_filter) in placements.items():
            with self.subTest(container=container):
                body = extract_braced_object(cmf, cmf.index(f'type {container} ='))
                call = 'com_outliner_entry = {'
                self.assertEqual(1, body.count(call))
                row = extract_braced_object(body, body.index(call))
                visibility = f'And4(JournalEntry.IsValid,JournalEntry.IsPinnedInOutliner,{org_filter},{situation_filter})'
                self.assertIn(f'visible="[{visibility}]"', ''.join(row.split()))
                self.assertNotIn('progressbars_spacing', row)
        native = (GAME / 'gui/outliner_ongoing_types.gui').read_text(encoding='utf-8-sig')
        native = extract_braced_object(native, native.index('type outliner_journal_entry ='))
        self.assertRegex(native, r'blockoverride "progressbars_spacing"\s*\{\s*spacing = 6\s*\}')

    def test_frontier_colonisation_preserves_both_native_enactment_hooks(self):
        native = find_object((GAME / "common/laws/01_colonial_affairs.txt").read_text(encoding="utf-8-sig"), "law_frontier_colonization")
        body = find_object((ROOT / "common/laws/00_sb_governance_principles.txt").read_text(encoding="utf-8-sig"), "law_frontier_colonization", directive="REPLACE")
        branch = re.search(r"AND\s*=\s*\{\s*country_has_primary_culture\s*=\s*cu:boer", body)
        self.assertIsNotNone(branch)
        delta = extract_braced_object(body, branch.start())
        for tag in ("TRN", "ZPB", "LYD", "NAL"):
            self.assertIn(f"cd:{tag}", delta)
        body = body.replace(delta, "", 1).replace("REPLACE:", "", 1)
        self.assertEqual(parse(native), parse(body))

    def test_social_mobility_preserves_native_country_gate_and_ai(self):
        native = find_object((GAME / "common/decrees/00_decree.txt").read_text(encoding="utf-8-sig"), "decree_promote_social_mobility")
        body = find_object((ROOT / "common/decrees/zz_sb_institutions_social_mobility.txt").read_text(encoding="utf-8-sig"), "decree_promote_social_mobility", directive="REPLACE")
        branch = re.search(r"custom_tooltip\s*=\s*\{\s*text\s*=\s*sb_institutions_social_mobility_available_tt", body)
        delta = extract_braced_object(body, branch.start())
        self.assertIn("owner ?= { NOT = { has_variable = sb_institutions_active_var } }", delta)
        self.assertEqual(parse(native), parse(body.replace(delta, "", 1).replace("REPLACE:", "", 1)))


if __name__ == "__main__":
    unittest.main()
