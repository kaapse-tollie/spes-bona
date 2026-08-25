from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def object_block(path: str, name: str) -> str:
    source = text(path)
    match = re.search(rf"^(?:REPLACE:)?{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} in {path}")
    return validate.extract_braced(source, match.start())


class InboekstelselAccessTests(unittest.TestCase):
    def test_convention_refusal_play_gives_boers_the_requested_counter_demands(self):
        response = object_block(
            "events/sb_boer_conventions_events.txt", "sb_boer_conventions.142"
        )
        play_match = re.search(r"^\s*random_diplomatic_play\s*=\s*\{", response, re.MULTILINE)
        self.assertIsNotNone(play_match)
        play = validate.extract_braced(response, play_match.start())
        goals = [
            validate.extract_braced(play, match.start())
            for match in re.finditer(r"^\s*add_war_goal\s*=\s*\{", play, re.MULTILINE)
        ]

        humiliation = next(goal for goal in goals if "type = humiliation" in goal)
        self.assertIn("holder = scope:highveld_target", humiliation)
        self.assertIn("target_country = root", humiliation)
        self.assertIn("primary_demand = yes", humiliation)

        cape_liberation = next(
            goal
            for goal in goals
            if "type = liberate_subject" in goal and "target_country = c:CAP" in goal
        )
        natal_liberation = next(
            goal
            for goal in goals
            if "type = liberate_subject" in goal and "target_country = c:NAL" in goal
        )
        for liberation in (cape_liberation, natal_liberation):
            self.assertIn("holder = scope:highveld_target", liberation)
            self.assertNotIn("primary_demand", liberation)

        self.assertEqual(1, play.count("primary_demand = yes"))
        self.assertRegex(
            play,
            r"c:CAP\s*\?=\s*\{[\s\S]*?is_direct_subject_of\s*=\s*root"
            r"[\s\S]*?target_country\s*=\s*c:CAP",
        )
        self.assertRegex(
            play,
            r"sb_boer_convention_nal_is_british_colony\s*=\s*yes"
            r"[\s\S]*?is_direct_subject_of\s*=\s*root"
            r"[\s\S]*?target_country\s*=\s*c:NAL",
        )

    def test_law_does_not_require_an_existing_slavery_law(self):
        law = object_block(
            "common/laws/02_sb_inboekstelsel_slavery.txt",
            "law_discrete_inboekstelsel",
        )
        self.assertIn("parent = law_legacy_slavery", law)
        self.assertNotIn("unlocking_laws", law)
        self.assertIn("sb_is_inboekstelsel_eligible_country = yes", law)

    def test_settler_victory_cap_is_eligible(self):
        trigger = object_block(
            "common/scripted_triggers/sb_boer_conventions_triggers.txt",
            "sb_is_inboekstelsel_eligible_country",
        )
        for token in (
            "sb_is_boer_inboekstelsel_country = yes",
            "country_definition = cd:CAP",
            "has_variable = sb_cape_settler_victory_var",
        ):
            self.assertIn(token, trigger)
        self.assertNotIn("sb_cape_compromise_victory_var", trigger)

    def test_cap_receives_the_same_law_and_journal_contract(self):
        laws = text("common/laws/02_sb_inboekstelsel_slavery.txt")
        journal = text("common/journal_entries/1-10_sb_inboekstelsel.txt")
        effects = text("common/scripted_effects/sb_inboekstelsel_effects.txt")
        self.assertEqual(3, laws.count("sb_is_inboekstelsel_eligible_country = yes"))
        self.assertEqual(4, journal.count("sb_is_inboekstelsel_eligible_country = yes"))
        self.assertIn("sb_is_inboekstelsel_eligible_country = yes", effects)

    def test_expanded_amendment_remains_boer_only(self):
        amendment = object_block(
            "common/amendments/sb_amendments.txt",
            "amendment_sb_expanded_inboekstelsel",
        )
        self.assertIn("sb_is_boer_inboekstelsel_country = yes", amendment)
        self.assertNotIn("sb_is_inboekstelsel_eligible_country", amendment)

    def test_relaxation_returns_freed_slaves_as_peasants(self):
        effect = object_block(
            "common/scripted_effects/sb_inboekstelsel_effects.txt",
            "sb_inboekstelsel_relax",
        )
        localization = text("localization/english/sb_great_trek_l_english.yml")

        self.assertIn("change_poptype = pop_type:peasants", effect)
        self.assertIn("is_pop_type = peasants", effect)
        self.assertNotIn("pop_type:laborers", effect)
        self.assertRegex(
            localization,
            r"sb_inboekstelsel_relax_effect_tt:0 .*GetPopType\('peasants'\)",
        )


if __name__ == "__main__":
    unittest.main()
