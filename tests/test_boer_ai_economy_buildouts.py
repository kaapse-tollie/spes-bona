from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]
EFFECTS_PATH = "common/scripted_effects/sb_boer_ai_economy_effects.txt"


def effects_text() -> str:
    return (ROOT / EFFECTS_PATH).read_text(encoding="utf-8-sig")


def effect_block(name: str) -> str:
    source = effects_text()
    match = re.search(rf"^{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing scripted effect {name}")
    return validate.extract_braced(source, match.start())


def year_segment(block: str, year: int) -> str:
    marker = re.search(rf"game_date\s*>=\s*{year}\.1\.1", block)
    if marker is None:
        raise AssertionError(f"missing {year} milestone")
    branches = tuple(
        re.finditer(r"^\s*(?:if|else_if)\s*=\s*\{", block, re.MULTILINE)
    )
    branch = next(candidate for candidate in reversed(branches) if candidate.start() < marker.start())
    return validate.extract_braced(block, branch.start())


def called_effects(segment: str) -> tuple[str, ...]:
    calls = re.findall(r"\b(sb_boer_ai_economy_[a-z0-9_]+)\s*=\s*yes", segment)
    return tuple(call for call in calls if call != "sb_boer_ai_economy_trn_has_priority_state")


class BoerAIEconomyBuildoutTests(unittest.TestCase):
    def test_managed_ai_countries_cannot_build_construction_sectors_before_1850(self):
        guard = (ROOT / "common/buildings/sb_construction_sector_guard.txt").read_text(
            encoding="utf-8-sig"
        )
        injection = re.search(
            r"^INJECT:building_construction_sector\s*=\s*\{",
            guard,
            re.MULTILINE,
        )
        self.assertIsNotNone(injection)
        block = validate.extract_braced(guard, injection.start())
        self.assertIn("possible = {", block)
        self.assertIn("owner ?= {", block)
        self.assertIn("is_ai = no", block)
        self.assertIn("game_date >= 1850.1.1", block)
        self.assertEqual(
            {
                "CAP",
                "ORA",
                "TRN",
                "ZPB",
                "LYD",
                "NAL",
                "PHL",
                "WBL",
                "BST",
                "ZUL",
            },
            set(re.findall(r"country_definition\s*=\s*cd:([A-Z0-9_]+)", block)),
        )

    def test_oranje_schedule(self):
        block = effect_block("sb_boer_ai_economy_ora_yearly_pulse")
        expected = {
            1838: ("sb_boer_ai_economy_ora_tobacco_plantation",),
            1840: (
                "sb_boer_ai_economy_ora_maize_farm",
                "sb_boer_ai_economy_ora_livestock_ranch",
            ),
            1845: (
                "sb_boer_ai_economy_ora_food_industry",
                "sb_boer_ai_economy_ora_maize_farm",
            ),
            1850: (
                "sb_boer_ai_economy_ora_livestock_ranch",
                "sb_boer_ai_economy_ora_logging_camp",
            ),
            1855: ("sb_boer_ai_economy_ora_tooling_workshop",),
            1860: ("sb_boer_ai_economy_ora_iron_mine",),
            1865: ("sb_boer_ai_economy_ora_coal_mine",),
        }
        for year, effects in expected.items():
            with self.subTest(year=year):
                self.assertEqual(effects, called_effects(year_segment(block, year)))
        self.assertNotIn("game_date >= 1870.1.1", block)

    def test_transvaal_early_schedule(self):
        block = effect_block("sb_boer_ai_economy_trn_yearly_pulse")
        expected = {
            1840: ("sb_boer_ai_economy_trn_maize_farm",),
            1845: ("sb_boer_ai_economy_trn_food_industry",),
            1850: (
                "sb_boer_ai_economy_trn_arms_industry",
                "sb_boer_ai_economy_trn_logging_camp",
            ),
            1855: (
                "sb_boer_ai_economy_trn_iron_mine",
                "sb_boer_ai_economy_trn_tobacco_plantation",
            ),
            1860: (
                "sb_boer_ai_economy_trn_tooling_workshop",
                "sb_boer_ai_economy_trn_coal_mine",
            ),
            1865: ("sb_boer_ai_economy_trn_steel_mill",),
        }
        for year, effects in expected.items():
            with self.subTest(year=year):
                self.assertEqual(effects, called_effects(year_segment(block, year)))
        self.assertNotIn("game_date >= 1880.1.1", block)

    def test_transvaal_late_schedule_and_three_state_gate(self):
        block = effect_block("sb_boer_ai_economy_trn_yearly_pulse")
        expected = {
            1870: {
                "STATE_TRANSVAAL": "sb_boer_ai_economy_create_textile_mill",
                "STATE_EAST_TRANSVAAL": "sb_boer_ai_economy_create_logging_camp",
                "STATE_NORTHERN_TRANSVAAL": "sb_boer_ai_economy_create_iron_mine",
            },
            1875: {
                "STATE_TRANSVAAL": "sb_boer_ai_economy_create_motor_industry",
                "STATE_EAST_TRANSVAAL": "sb_boer_ai_economy_create_logging_camp",
                "STATE_NORTHERN_TRANSVAAL": "sb_boer_ai_economy_create_iron_mine",
            },
            1885: {
                "STATE_TRANSVAAL": "sb_boer_ai_economy_create_munition_plant",
                "STATE_EAST_TRANSVAAL": "sb_boer_ai_economy_create_logging_camp",
                "STATE_NORTHERN_TRANSVAAL": "sb_boer_ai_economy_create_iron_mine",
            },
            1890: {
                "STATE_TRANSVAAL": "sb_boer_ai_economy_create_fertilizer_plant",
                "STATE_EAST_TRANSVAAL": "sb_boer_ai_economy_create_logging_camp",
                "STATE_NORTHERN_TRANSVAAL": "sb_boer_ai_economy_create_coal_mine",
            },
        }
        for year, placements in expected.items():
            segment = year_segment(block, year)
            with self.subTest(year=year):
                self.assertEqual(3, segment.count("any_scope_state = { state_region = s:"))
                self.assertEqual(set(placements.values()), set(called_effects(segment)))
                for state, effect in placements.items():
                    self.assertRegex(
                        segment,
                        rf"limit\s*=\s*\{{\s*state_region\s*=\s*s:{state}\s*\}}\s*{effect}\s*=\s*yes",
                    )

    def test_new_industries_and_obsolete_helpers(self):
        source = effects_text()
        arms = effect_block("sb_boer_ai_economy_create_arms_industry")
        textiles = effect_block("sb_boer_ai_economy_create_textile_mill")
        self.assertIn("building = building_arms_industry", arms)
        self.assertIn('"pm_muskets"', arms)
        self.assertIn("building = building_textile_mill", textiles)
        self.assertIn('"pm_handsewn_clothes"', textiles)
        for obsolete in (
            "sb_boer_ai_economy_ora_trade_center",
            "sb_boer_ai_economy_ora_construction_sector",
            "sb_boer_ai_economy_trn_trade_center",
            "sb_boer_ai_economy_trn_construction_sector",
            "sb_boer_ai_economy_create_construction_sector",
        ):
            self.assertNotIn(obsolete, source)


if __name__ == "__main__":
    unittest.main()
