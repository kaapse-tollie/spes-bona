"""Preserve authored event bodies independently of native occurrence tracking.

These source checks cannot establish native queue, cancellation or save semantics.
Those scenarios remain in the DP runtime matrix.
"""
import hashlib
import json
from pathlib import Path
import re
import unittest

from tools.check_override_inventory import find_object

ROOT = Path(__file__).resolve().parents[1]


class OnceOnlyContracts(unittest.TestCase):
    def test_migrated_events_preserve_every_other_trigger_and_effect(self):
        contracts = json.loads((ROOT / "tests/fixtures/1_15_once_only_contracts.json").read_text())
        for item in contracts:
            with self.subTest(event=item["event"]):
                body = find_object((ROOT / item["path"]).read_text(encoding="utf-8-sig"), item["event"])
                self.assertEqual(body.count("fire_only_once = yes"), 1)
                self.assertNotIn("fire_only_once_globally", body)
                self.assertNotIn(item["removed_flag"], body)
                preserved = re.sub(r"^[ \t]*fire_only_once = yes\n", "", body, flags=re.M)
                self.assertEqual(hashlib.sha256(preserved.encode()).hexdigest(), item["preserved_body_sha256"])

    def test_repeatable_gaza_episodes_and_shared_diamond_state_survive(self):
        gaza = (ROOT / "common/scripted_effects/sb_eastern_sphere_effects.txt").read_text(encoding="utf-8-sig")
        events = (ROOT / "events/sb_gaza_events.txt").read_text(encoding="utf-8-sig")
        for number in ("010", "020", "030", "040"):
            flag = f"sb_gaza_{number}_fired_var"
            self.assertIn(f"remove_variable = {flag}", gaza)
            self.assertIn(flag, find_object(events, f"sb_gaza.{number}"))
            self.assertNotIn("fire_only_once", find_object(events, f"sb_gaza.{number}"))
        kimberley = (ROOT / "events/sb_griqualand_west_events.txt").read_text(encoding="utf-8-sig")
        for number in ("021", "027"):
            body = find_object(kimberley, f"sb_griqualand_west.{number}")
            self.assertIn("sb_kimberley_discovery_pending_var", body)
            self.assertNotIn("fire_only_once", body)


if __name__ == "__main__":
    unittest.main()
