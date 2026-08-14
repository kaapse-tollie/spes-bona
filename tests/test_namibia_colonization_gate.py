from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def object_block(path: str, name: str) -> str:
    source = text(path)
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} in {path}")
    return validate.extract_braced(source, match.start())


class NamibiaColonizationGateTests(unittest.TestCase):
    def test_desert_coastline_blocks_walvis_bay_frontier_expansion(self):
        trait = object_block(
            "common/state_traits/sb_state_traits.txt",
            "state_trait_sb_south_west_africa_administrative_barrier",
        )
        required = re.search(r"required_techs_for_colonization\s*=\s*\{([^}]*)\}", trait)
        self.assertIsNotNone(required)
        self.assertEqual(
            ["sb_namibian_coastal_access"],
            re.findall(r'"([^"]+)"', required.group(1)),
        )
        self.assertIn(
            'disabling_technologies = { "sb_namibian_coastal_access" }',
            trait,
        )
        self.assertIn("state_colony_growth_speed_mult = -100", trait)

        namaqualand = object_block(
            "common/history/states/00_states.txt",
            "s:STATE_NAMAQUALAND",
        )
        self.assertRegex(
            namaqualand,
            r"country\s*=\s*c:CAP[\s\S]*?owned_provinces\s*=\s*\{[\s\S]*?x8031D0",
        )

    def test_scripted_access_still_requires_both_public_technologies(self):
        trigger = object_block(
            "common/scripted_triggers/sb_namibia_triggers.txt",
            "sb_nam_has_coastal_engineering_technologies",
        )
        self.assertIn("has_technology_researched = floating_harbor", trigger)
        self.assertIn("has_technology_researched = civilizing_mission", trigger)

        grant = object_block(
            "common/scripted_effects/sb_namibia_effects.txt",
            "sb_nam_grant_coastal_access_if_eligible",
        )
        self.assertIn("sb_nam_has_coastal_engineering_technologies = yes", grant)
        self.assertIn("sb_nam_has_physical_coastal_access = yes", grant)
        self.assertIn("add_technology_researched = sb_namibian_coastal_access", grant)

        decision = object_block(
            "common/decisions/sb_namibia_decisions.txt",
            "decision_sb_map_namibian_coast",
        )
        self.assertGreaterEqual(
            decision.count("sb_nam_has_coastal_engineering_technologies = yes"),
            2,
        )


if __name__ == "__main__":
    unittest.main()
