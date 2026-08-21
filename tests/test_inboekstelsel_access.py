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
