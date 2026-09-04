from __future__ import annotations

from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = validate.find_game_root(None)
TRIGGER_PATH = "common/scripted_triggers/zz_sb_ai_incorporation_overrides.txt"
EXPECTED_PRIORITIES = {
    ("NAL", "STATE_ZULULAND"),
    ("CAP", "STATE_BECHUANALAND"),
    ("CAP", "STATE_GRIQUALAND_WEST"),
    ("ORA", "STATE_DRAKENSBERG"),
}
EXPECTED_REPLACEMENTS = {
    "ai_can_incorporate_state": r'''REPLACE:ai_can_incorporate_state = {
	OR = {
		AND = {
			OR = {
				is_homeland_of_country_cultures = root
				"years_to_incorporate(root)" <= define:NAI|INCORPORATE_STATE_MAX_YEARS
			}
		}
		sb_regional_ai_should_incorporate = yes
	}
}''',
    "ai_will_incorporate_state": r'''REPLACE:ai_will_incorporate_state = {
	OR = {
		AND = {
			OR = {
				is_homeland_of_country_cultures = root
				"years_to_incorporate(root)" <= define:NAI|INCORPORATE_STATE_MAX_YEARS
			}
			state_population >= define:NAI|INCORPORATE_STATE_MIN_POPULATION
		}
		sb_regional_ai_should_incorporate = yes
	}
}''',
    "ai_colony_will_incorporate_state": r'''REPLACE:ai_colony_will_incorporate_state = {
	OR = {
		AND = {
			OR = {
				region = root.capital.region
				any_neighbouring_state = {
					owner = root
					is_incorporated = yes
				}
			}
			state_population >= define:NAI|INCORPORATE_STATE_MIN_POPULATION
		}
		sb_regional_ai_should_incorporate = yes
	}
}''',
}


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def object_block(source: str, key: str, directive: str | None = None) -> str:
    prefix = f"{directive}:" if directive else ""
    match = re.search(
        rf"^\s*(?P<key>{re.escape(prefix + key)})\s*=\s*\{{",
        source,
        re.MULTILINE,
    )
    if match is None:
        raise AssertionError(f"missing {prefix}{key}")
    return validate.extract_braced(source, match.start("key"))


def parsed_priorities(helper: str) -> set[tuple[str, str]]:
    pairs = re.findall(
        r"root\s*=\s*\{\s*country_definition\s*=\s*cd:([A-Z0-9_]+)\s*\}"
        r"\s*state_region\s*=\s*s:(STATE_[A-Z0-9_]+)",
        helper,
    )
    return set(pairs)


class RegionalAIIncorporationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = text(TRIGGER_PATH)
        cls.helper = object_block(cls.source, "sb_regional_ai_should_incorporate")
        cls.priorities = parsed_priorities(cls.helper)

    def helper_matches(
        self,
        root_tag: str,
        state_region: str,
        *,
        owner_tag: str,
        is_ai: bool,
    ) -> bool:
        return (
            owner_tag == root_tag
            and is_ai
            and (root_tag, state_region) in self.priorities
        )

    def test_all_three_replacements_wrap_byte_faithful_ob1_gates(self):
        for key, expected in EXPECTED_REPLACEMENTS.items():
            with self.subTest(key=key):
                self.assertEqual(expected, object_block(self.source, key, "REPLACE"))

    def test_helper_is_ai_owned_and_has_exact_four_positive_mappings(self):
        self.assertEqual(EXPECTED_PRIORITIES, self.priorities)
        self.assertEqual(1, len(re.findall(r"^\s*owner\s*=\s*root$", self.helper, re.MULTILINE)))
        self.assertEqual(1, len(re.findall(r"^\s*is_ai\s*=\s*yes$", self.helper, re.MULTILINE)))
        self.assertEqual(4, self.helper.count("AND = {"))
        self.assertNotIn("is_ai = no", self.helper)

    def test_named_priorities_ignore_country_type_population_and_geography(self):
        for root_tag, state_region in EXPECTED_PRIORITIES:
            for country_type in ("recognized", "colonial", "company"):
                for population in (1, 99_999, 100_000, 10_000_000):
                    for adjacent in (False, True):
                        for owns_entire_region in (False, True):
                            with self.subTest(
                                root_tag=root_tag,
                                state_region=state_region,
                                country_type=country_type,
                                population=population,
                                adjacent=adjacent,
                                owns_entire_region=owns_entire_region,
                            ):
                                self.assertTrue(
                                    self.helper_matches(
                                        root_tag,
                                        state_region,
                                        owner_tag=root_tag,
                                        is_ai=True,
                                    )
                                )
        for forbidden_gate in (
            "state_population",
            "any_neighbouring_state",
            "is_homeland",
            "years_to_incorporate",
            "country_is_colonial_or_company",
            "owns_entire_state_region",
            "has_state_in_state_region",
            "sb_zululand_incorporation_requested_var",
            "sb_zululand_incorporation_started_var",
        ):
            self.assertNotIn(forbidden_gate, self.helper)

    def test_human_wrong_owner_tag_and_state_are_negative_controls(self):
        for root_tag, state_region in EXPECTED_PRIORITIES:
            with self.subTest(kind="human", root_tag=root_tag, state_region=state_region):
                self.assertFalse(
                    self.helper_matches(
                        root_tag,
                        state_region,
                        owner_tag=root_tag,
                        is_ai=False,
                    )
                )
            with self.subTest(kind="owner", root_tag=root_tag, state_region=state_region):
                self.assertFalse(
                    self.helper_matches(
                        root_tag,
                        state_region,
                        owner_tag="GBR",
                        is_ai=True,
                    )
                )
        for root_tag, state_region in (
            ("NAL", "STATE_DRAKENSBERG"),
            ("CAP", "STATE_ZULULAND"),
            ("ORA", "STATE_GRIQUALAND_WEST"),
            ("GBR", "STATE_ZULULAND"),
        ):
            with self.subTest(kind="mapping", root_tag=root_tag, state_region=state_region):
                self.assertFalse(
                    self.helper_matches(
                        root_tag,
                        state_region,
                        owner_tag=root_tag,
                        is_ai=True,
                    )
                )

    def test_helper_is_orred_once_into_both_will_paths_and_ai_can(self):
        for key in EXPECTED_REPLACEMENTS:
            block = object_block(self.source, key, "REPLACE")
            self.assertEqual(1, block.count("sb_regional_ai_should_incorporate = yes"), key)
        self.assertNotIn("sb_zululand_ai_should_incorporate", self.source)

    def test_ob1_caller_and_transfer_scoring_surface_remain_vanilla_owned(self):
        self.assertFalse((ROOT / "common/ai_strategies/00_default_strategy.txt").exists())
        self.assertFalse((ROOT / "common/treaty_articles/06_transfer_state.txt").exists())

    @unittest.skipIf(GAME_ROOT is None, "Vanilla game root unavailable")
    def test_unchanged_default_strategy_routes_both_country_type_branches(self):
        source = (GAME_ROOT / "common/ai_strategies/00_default_strategy.txt").read_text(
            encoding="utf-8-sig"
        )
        default = object_block(source, "ai_strategy_default")
        start_gate = object_block(default, "will_incorporate_state")
        colonial = "scope:target_state = { ai_colony_will_incorporate_state = yes }"
        ordinary = "scope:target_state = { ai_will_incorporate_state = yes }"
        self.assertEqual(1, start_gate.count("country_is_colonial_or_company = yes"))
        self.assertEqual(1, start_gate.count(colonial))
        self.assertEqual(1, start_gate.count(ordinary))
        self.assertLess(start_gate.index(colonial), start_gate.index(ordinary))
        self.assertLess(start_gate.index(ordinary), start_gate.index("trigger_else = { # Content"))
        self.assertNotIn("ai_can_incorporate_state", start_gate)

    @unittest.skipIf(GAME_ROOT is None, "Vanilla game root unavailable")
    def test_ai_can_is_scoring_only_in_both_visible_ob1_callers(self):
        strategy = (GAME_ROOT / "common/ai_strategies/00_default_strategy.txt").read_text(
            encoding="utf-8-sig"
        )
        transfer = (GAME_ROOT / "common/treaty_articles/06_transfer_state.txt").read_text(
            encoding="utf-8-sig"
        )
        default = object_block(strategy, "ai_strategy_default")
        self.assertEqual(2, default.count("ai_can_incorporate_state = yes"))
        self.assertIn('desc = "STATE_VALUE_CAN_INCORPORATE"', default)
        self.assertIn('desc = "STATE_VALUE_INCORPORATED_HOMELAND_RELUCTANCE"', default)
        self.assertEqual(1, transfer.count("ai_can_incorporate_state = yes"))
        self.assertIn("DIPLOMATIC_ACCEPTANCE_TRADE_STATE_SOURCE", transfer)
        self.assertNotIn(
            "ai_can_incorporate_state",
            object_block(default, "will_incorporate_state"),
        )


if __name__ == "__main__":
    unittest.main()
