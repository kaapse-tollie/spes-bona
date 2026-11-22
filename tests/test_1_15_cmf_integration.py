"""Full effective movement-body parity after the 1.15 CMF rebase."""

from pathlib import Path
import re
import unittest

from tools.check_override_inventory import find_object
from tests.test_1_14_3_compatibility import tokens
from tests.test_performance_pass import canonical_trigger
from tests.test_zulu_institutions_laws import child, statements


ROOT = Path(__file__).resolve().parents[1]
CMF = ROOT.parent / "Community Mod Framework"


class MovementParityTests(unittest.TestCase):
    def test_cape_political_movements_retain_only_authored_country_gate(self):
        sb = (ROOT / "common/political_movements/zzz_sb_cape_political_movement_overrides.txt").read_text(encoding="utf-8-sig")
        guard = re.compile(r"NOT\s*=\s*\{\s*AND\s*=\s*\{\s*country_definition\s*=\s*cd:CAP\s+has_journal_entry\s*=\s*je_sb_cape_politics\s*\}\s*\}")
        for key in ("movement_utilitarian", "movement_liberal", "movement_radical"):
            with self.subTest(key=key):
                filename = "ycom_04_country_specific_ideological_movements.txt" if key == "movement_utilitarian" else "ycom_00_ideological_movements.txt"
                cmf = (CMF / "common/political_movements" / filename).read_text(encoding="utf-8-sig")
                actual = find_object(sb, key, directive="REPLACE")
                expected = find_object(cmf, key, directive="REPLACE")
                actual, n = guard.subn("", actual)
                self.assertEqual(1, n)
                if key == "movement_utilitarian":
                    self.assertEqual(1, actual.count("country_has_primary_culture = cu:anglo_african"))
                    actual = actual.replace("country_has_primary_culture = cu:anglo_african", "")
                self.assertEqual(tokens(expected), tokens(actual.replace("sb_chiefs_other_uprising_allowed = yes", "")))

    def test_minority_rights_retains_only_cape_exclusion(self):
        source = (ROOT / "common/political_movements/zz_sb_minority_rights_movement_override.txt").read_text(encoding="utf-8-sig")
        actual = find_object(source, "movement_minority_rights", directive="REPLACE")
        cmf = (CMF / "common/political_movements/ycom_02_cultural_movement.txt").read_text(encoding="utf-8-sig")
        expected = find_object(cmf, "movement_minority_rights", directive="REPLACE")
        creation = child(actual, "creation_trigger")
        self.assertEqual(tokens("creation_trigger = { NOT = { country_definition = cd:CAP } }"), tokens(creation))
        actual = actual.replace(creation, "creation_trigger = {}", 1)
        disband = child(actual, "disband_trigger")
        self.assertEqual(tokens("disband_trigger = { owner = { country_definition = cd:CAP } }"), tokens(disband))
        actual = actual.replace(disband, "", 1)
        self.assertEqual(tokens(expected), tokens(actual.replace("sb_chiefs_other_uprising_allowed = yes", "")))

    def test_cultural_minority_keeps_native_secession_and_natal_handoff(self):
        source = (ROOT / "common/political_movements/zz_sb_cultural_minority_movement_override.txt").read_text(encoding="utf-8-sig")
        actual = find_object(source, "movement_cultural_minority", directive="REPLACE")
        cmf = (CMF / "common/political_movements/ycom_02_cultural_movement.txt").read_text(encoding="utf-8-sig")
        expected = find_object(cmf, "movement_cultural_minority", directive="REPLACE")
        guard = re.compile(r"AND\s*=\s*\{\s*has_variable\s*=\s*sb_natal_zulu_movement_replace_var\s+culture\s*=\s*cu:zulu\s+owner\s*\?=\s*\{\s*country_definition\s*=\s*cd:NAL\s*\}\s*\}")
        actual, n = guard.subn("", actual)
        self.assertEqual(1, n)
        handoff = child(actual, "on_disbanded")
        self.assertIn("sb_natal_snapshot_zulu_movement_modifiers = yes", handoff)
        self.assertIn("trigger_event = { id = sb_natal_interwar.031 days = 1 }", handoff)
        self.assertIn("owner ?= { country_definition = cd:NAL }", handoff)
        actual = actual.replace(handoff, "", 1)
        # The retained performance change only reorders this pure filter.
        a = child(child(expected, "additional_radicalism_factors"), "any_political_movement")
        b = child(child(actual, "additional_radicalism_factors"), "any_political_movement")
        self.assertEqual(canonical_trigger(statements(a)), canonical_trigger(statements(b)))
        actual = actual.replace(b, a, 1)
        self.assertEqual(tokens(expected), tokens(actual))


if __name__ == "__main__":
    unittest.main()
