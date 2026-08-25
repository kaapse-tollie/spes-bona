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
    def test_namaqualand_uses_the_settled_three_slot_whaling_cap(self):
        namaqualand = object_block(
            "map_data/state_regions/04_subsaharan_africa.txt", "STATE_NAMAQUALAND"
        )
        hereroland = object_block(
            "map_data/state_regions/04_subsaharan_africa.txt", "STATE_HEREROLAND"
        )
        self.assertIn("building_whaling_station = 3", namaqualand)
        self.assertNotIn("building_whaling_station", hereroland)

    def test_rehoboth_formation_installs_baster_ruler_and_migration(self):
        event = object_block("events/sb_namibia_events.txt", "sb_nam.020")
        ruler_effects = object_block(
            "common/scripted_effects/sb_namibia_effects.txt",
            "sb_nam_install_rehoboth_historical_ruler",
        )
        ruler = object_block(
            "common/character_templates/sb_southern_africa_character_template_overrides.txt",
            "RHB_hermanus_van_wyk",
        )
        modifier = object_block(
            "common/static_modifiers/sb_modifiers.txt",
            "sb_arid_frontier_pastoralism",
        )
        self.assertIn("sb_nam_install_rehoboth_historical_ruler = yes", event)
        self.assertIn("population = 2500", event)
        self.assertIn("historical = yes", ruler)
        self.assertIn("culture = cu:baster", ruler)
        self.assertIn("birth_date = 1835.1.1", ruler)
        self.assertIn("set_character_as_ruler = yes", ruler_effects)
        self.assertIn("state_food_security_add = 0.30", modifier)

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

    def test_namaqualand_port_locator_is_localized_as_walvis_bay(self):
        generic_hubs = text("localization/english/replace/sb_hub_names_l_english.yml")
        dynamic_hubs = text("localization/english/replace/dynamic_state_and_hub_names_l_english.yml")
        self.assertIn('HUB_NAME_STATE_NAMAQUALAND_port:0 "Walvis Bay"', generic_hubs)
        self.assertIn('HUB_NAME_STATE_NAMAQUALAND_port_german:0 "Walvis Bay"', dynamic_hubs)

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

    def test_scramble_growth_adds_the_global_fallback_generation_bonus(self):
        modifier = object_block(
            "common/static_modifiers/sb_modifiers.txt",
            "sb_scramble_for_africa_colonial_growth",
        )
        self.assertIn("state_colony_growth_creation_factor = 0.10", modifier)
        self.assertIn("state_colony_growth_speed_mult = 1.00", modifier)


if __name__ == "__main__":
    unittest.main()
