from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def object_block(path: str, name: str) -> str:
    source = text(path)
    match = re.search(rf"^{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} in {path}")
    return validate.extract_braced(source, match.start())


class CapeFranchiseWeakeningTests(unittest.TestCase):
    def test_restricted_franchise_replaces_the_full_acceptance_bonus(self):
        full = object_block(
            "common/amendments/sb_amendments.txt",
            "amendment_sb_cape_qualified_franchise",
        )
        restricted = object_block(
            "common/amendments/sb_amendments.txt",
            "amendment_sb_restricted_cape_qualified_franchise",
        )
        self.assertIn("country_acceptance_no_shared_heritage_trait_add = 10", full)
        self.assertIn("NOT = { has_variable = sb_cape_franchise_weakened_var }", full)
        self.assertIn("country_acceptance_no_shared_heritage_trait_add = 5", restricted)
        self.assertIn("has_variable = sb_cape_franchise_weakened_var", restricted)

        compatibility_trigger = object_block(
            "common/scripted_triggers/sb_cape_triggers.txt",
            "sb_has_cape_qualified_franchise_amendment",
        )
        self.assertIn("amendment_sb_cape_qualified_franchise", compatibility_trigger)
        self.assertIn("amendment_sb_restricted_cape_qualified_franchise", compatibility_trigger)

    def test_bigoted_post_story_ruler_schedules_the_event_once(self):
        handler = object_block(
            "common/on_actions/sb_cape_on_action_handlers.txt",
            "sb_on_cape_monthly_pulse_country",
        )
        for token in (
            "country_definition = cd:CAP",
            "NOT = { has_journal_entry = je_sb_cape_politics }",
            "sb_cape_settler_victory_var",
            "sb_cape_compromise_victory_var",
            "has_amendment = amendment_type:amendment_sb_cape_qualified_franchise",
            "ruler = { has_trait = bigoted }",
            "sb_cape_franchise_weakening_pending_var",
            "id = sb_cape.210",
        ):
            self.assertIn(token, handler)

    def test_event_swaps_amendments_and_records_the_outcome(self):
        event = object_block("events/sb_cape_events.txt", "sb_cape.210")
        for token in (
            "NOT = { has_journal_entry = je_sb_cape_politics }",
            "ruler = { has_trait = bigoted }",
            "set_variable = sb_cape_franchise_weakened_var",
            "type = amendment_type:amendment_sb_cape_qualified_franchise",
            "remove_amendment = yes",
            "type = amendment_sb_restricted_cape_qualified_franchise",
            "remove_variable = sb_cape_franchise_weakening_pending_var",
        ):
            self.assertIn(token, event)

        cape_events = text("events/sb_cape_events.txt")
        self.assertEqual(2, cape_events.count("set_variable = sb_cape_settler_victory_var"))
        self.assertEqual(1, cape_events.count("set_variable = sb_cape_compromise_victory_var"))

        loc = text("localization/english/sb_cape_l_english.yml")
        self.assertIn("# ### TO REVIEW ###\n sb_cape.210.t:0", loc)
        self.assertIn("sb_cape_210_franchise_weakened_tt:0", loc)


if __name__ == "__main__":
    unittest.main()
