from __future__ import annotations

from pathlib import Path
import re
import unittest

from tools import validate
from tests.test_usuthu_movement_contest import parse


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = validate.find_game_root(None)
TRIGGER_PATH = "common/scripted_triggers/zz_sb_ai_incorporation_overrides.txt"
EXPECTED_PRIORITIES = {
    ("NAL", "STATE_ZULULAND"),
    ("CAP", "STATE_BECHUANALAND"),
    ("CAP", "STATE_GRIQUALAND_WEST"),
    ("ORA", "STATE_DRAKENSBERG"),
}
REPLACEMENTS = (
    "ai_can_incorporate_state",
    "ai_will_incorporate_state",
    "ai_colony_will_incorporate_state",
)


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


def evaluate(nodes, state, root, triggers, defines):
    """Evaluate only the incorporation trigger vocabulary, rejecting unknown gates."""
    def check(key, op, value):
        if key in ("AND", "OR"):
            results = [evaluate([n], state, root, triggers, defines) for n in value]
            return all(results) if key == "AND" else any(results)
        if key == "root":
            return evaluate(value, root, root, triggers, defines)
        if key in triggers:
            return evaluate(triggers[key], state, root, triggers, defines) == (value == "yes")
        if key == "owner": return state["owner"] == root["tag"]
        if key == "country_definition": return value == "cd:" + state["tag"]
        if key == "state_region": return value == "s:" + state["state_region"]
        if key == "is_ai": return state["is_ai"] == (value == "yes")
        if key == "is_incorporated": return state["incorporated"] == (value == "yes")
        if key == "is_homeland_of_country_cultures": return state["homeland"]
        if key == "region": return state["region"] == root["capital_region"]
        if key == "any_neighbouring_state":
            return any(evaluate(value, n, root, triggers, defines) for n in state["neighbours"])
        if key == "primary_cultures_percent_state":
            assert value[0] == ("target_country", "=", "root"), value
            assert value[1][:2] == ("value", ">="), value
            return state["primary_share"] >= float(value[1][2])
        if key in ('"years_to_incorporate(root)"', "state_population"):
            bound = defines[value]
            if key == "state_population":
                assert op == ">="
                return state["population"] >= bound
            assert op == "<="
            return state["years"] <= bound
        raise AssertionError((key, op, value))
    return all(check(*node) for node in nodes)


class NativeIncorporationBoundariesTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(GAME_ROOT)
        source = text(TRIGGER_PATH)
        self.triggers = {key: parse(object_block(source, key, "REPLACE")) for key in REPLACEMENTS}
        self.triggers["sb_regional_ai_should_incorporate"] = parse(object_block(source, "sb_regional_ai_should_incorporate"))
        defines = (GAME_ROOT / "common/defines/00_ai.txt").read_text(encoding="utf-8-sig")
        self.defines = {
            "define:NAI|" + key: float(re.search(rf"\b{key}\s*=\s*(\d+(?:\.\d+)?)", defines)[1])
            for key in ("INCORPORATE_STATE_MAX_YEARS", "INCORPORATE_STATE_MIN_POPULATION")
        }
        self.minimum = self.defines["define:NAI|INCORPORATE_STATE_MIN_POPULATION"]
        self.maximum = self.defines["define:NAI|INCORPORATE_STATE_MAX_YEARS"]
        self.root = dict(tag="GBR", is_ai=True, capital_region="europe")
        self.state = dict(owner="GBR", state_region="STATE_ZULULAND", primary_share=0,
                          homeland=False, years=self.maximum + 1, population=self.minimum,
                          region="africa", neighbours=[])

    def result(self, key, **changes):
        return evaluate(self.triggers[key], dict(self.state, **changes), self.root, self.triggers, self.defines)

    def test_primary_culture_and_same_owner_incorporated_adjacency_thresholds(self):
        for owner, incorporated, share, expected in (
            ("GBR", True, .2499, False), ("GBR", True, .25, True),
            ("GBR", False, .25, False), ("FRA", True, .25, False),
            ("FRA", False, .4999, False), ("FRA", False, .5, True),
        ):
            with self.subTest(owner=owner, incorporated=incorporated, share=share):
                neighbour = dict(owner=owner, incorporated=incorporated)
                for key in REPLACEMENTS[:2]:
                    self.assertEqual(expected, self.result(key, primary_share=share, neighbours=[neighbour]))
        for key in REPLACEMENTS:
            self.assertFalse(self.result(key, primary_share=.4999))
            self.assertTrue(self.result(key, primary_share=.5))

    def test_homeland_and_incorporation_years_keep_their_native_paths(self):
        for key in REPLACEMENTS:
            self.assertTrue(self.result(key, homeland=True))
            self.assertTrue(self.result(key, years=self.maximum))
            self.assertFalse(self.result(key, years=self.maximum + 1))

    def test_ordinary_and_colonial_population_and_geography_boundaries(self):
        self.assertTrue(self.result("ai_can_incorporate_state", primary_share=.5, population=1))
        for key in REPLACEMENTS[1:]:
            self.assertFalse(self.result(key, primary_share=.5, population=self.minimum - 1))
            self.assertTrue(self.result(key, primary_share=.5, population=self.minimum))
        for region, neighbours, expected in (
            ("europe", [], True), ("africa", [], False),
            ("africa", [dict(owner="GBR", incorporated=True)], True),
            ("africa", [dict(owner="FRA", incorporated=True)], False),
            ("africa", [dict(owner="GBR", incorporated=False)], False),
        ):
            self.assertEqual(expected, self.result("ai_colony_will_incorporate_state", region=region, neighbours=neighbours))
            self.assertFalse(self.result("ai_will_incorporate_state", region=region, neighbours=neighbours))

    def test_four_regional_exceptions_and_negative_controls_through_all_three_paths(self):
        self.state.update(population=1)
        for tag, region in EXPECTED_PRIORITIES:
            for is_ai, owner, actor, expected in (
                (True, tag, tag, True), (False, tag, tag, False),
                (True, "GBR", tag, False), (True, "GBR", "GBR", False),
            ):
                self.root.update(tag=actor, is_ai=is_ai)
                for key in REPLACEMENTS:
                    with self.subTest(key=key, actor=actor, region=region, owner=owner, is_ai=is_ai):
                        self.assertEqual(expected, self.result(key, owner=owner, state_region=region))
            self.root.update(tag=tag, is_ai=True)
            for key in REPLACEMENTS:
                self.assertFalse(self.result(key, owner=tag, state_region="STATE_CAPE_COLONY"))


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

    def test_all_three_replacements_wrap_complete_current_native_gates(self):
        self.assertIsNotNone(GAME_ROOT, "current Vanilla incorporation contracts are mandatory")
        native = (GAME_ROOT / "common/scripted_triggers/00_ai_triggers.txt").read_text(encoding="utf-8-sig")
        for key in REPLACEMENTS:
            with self.subTest(key=key):
                self.assertEqual(
                    [("OR", "=", [("AND", "=", parse(object_block(native, key))),
                                    ("sb_regional_ai_should_incorporate", "=", "yes")])],
                    parse(object_block(self.source, key, "REPLACE")),
                )

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
        for key in REPLACEMENTS:
            block = object_block(self.source, key, "REPLACE")
            self.assertEqual(1, block.count("sb_regional_ai_should_incorporate = yes"), key)
        self.assertNotIn("sb_zululand_ai_should_incorporate", self.source)

    def test_caller_and_transfer_scoring_surface_remain_vanilla_owned(self):
        self.assertFalse((ROOT / "common/ai_strategies/00_default_strategy.txt").exists())
        self.assertFalse((ROOT / "common/treaty_articles/06_transfer_state.txt").exists())

    def test_unchanged_default_strategy_routes_both_country_type_branches(self):
        self.assertIsNotNone(GAME_ROOT)
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

    def test_ai_can_scoring_contexts_remain_in_both_native_callers(self):
        self.assertIsNotNone(GAME_ROOT)
        strategy = (GAME_ROOT / "common/ai_strategies/00_default_strategy.txt").read_text(
            encoding="utf-8-sig"
        )
        transfer = (GAME_ROOT / "common/treaty_articles/06_transfer_state.txt").read_text(
            encoding="utf-8-sig"
        )
        default = object_block(strategy, "ai_strategy_default")
        scoring = object_block(default, "state_value")
        own = object_block(scoring, "if")
        foreign = object_block(scoring[scoring.index("else = { # For other countries states"):], "else")
        self.assertIn("scope:target_state = { owner = root }", own)
        self.assertIn('desc = "STATE_VALUE_CAN_INCORPORATE"', own)
        self.assertIn('desc = "STATE_VALUE_INCORPORATED_HOMELAND_RELUCTANCE"', own)
        self.assertIn("ai_can_incorporate_state = yes", foreign)
        self.assertIn('desc = "STATE_VALUE_CAN_INCORPORATE"', foreign)
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
