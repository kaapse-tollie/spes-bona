"""Native diamond reserves and technology eligibility; engine rolls need DP's check."""
import re
import unittest

from tests.test_resource_rework_implementation import (
    ROOT, DIAMOND, object_block, nested_blocks,
)


DEPOSITS = {
    "STATE_VRYSTAAT": ("dynamite", 5),
    "STATE_NORTHERN_CAPE": ("pumpjacks", 4),
    "STATE_TRANSVAAL": ("pumpjacks", 20),
    "STATE_NAMAQUALAND": ("pumpjacks", 14),
    "STATE_NORTHERN_TRANSVAAL": ("pneumatic_tools", 6),
    "STATE_DRAKENSBERG": ("pneumatic_tools", 6),
    "STATE_BOTSWANA": ("pneumatic_tools", 30),
    "STATE_ZAMBEZI": ("pneumatic_tools", 10),
}


def text(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


class DiamondDiscoveryTests(unittest.TestCase):
    def test_reserves_start_undiscovered_at_the_unchanged_caps(self):
        states = text("map_data/state_regions/04_subsaharan_africa.txt")
        for state, (technology, amount) in DEPOSITS.items():
            with self.subTest(state=state):
                block = object_block(states, state)
                reserves = [reserve for reserve in nested_blocks(block, "resource")
                            if f'building_sb_diamond_mine_{technology}' in reserve]
                self.assertEqual(1, len(reserves))
                self.assertRegex(reserves[0], rf"undiscovered_amount = {amount}\b")
                self.assertNotIn("discovered_amount =", reserves[0].replace("undiscovered_amount =", ""))
                self.assertNotIn("depleted_type", reserves[0])
        self.assertEqual(95, sum(amount for _, amount in DEPOSITS.values()))

    def test_each_native_building_requires_the_existing_technology(self):
        buildings = text("common/buildings/sb_diamond_mines.txt")
        original = object_block(buildings, DIAMOND)
        for technology in {tech for tech, _ in DEPOSITS.values()}:
            with self.subTest(technology=technology):
                name = f"building_sb_diamond_mine_{technology}"
                block = object_block(buildings, name)
                self.assertIn("building_group = bg_diamond_mining", block)
                self.assertEqual(["prospecting", technology], re.findall(
                    r"\b(?:prospecting|dynamite|pumpjacks|pneumatic_tools)\b",
                    object_block(block, "unlocking_technologies")))
                # A gate must not also change the mine's costs, output or employment.
                restored = block.replace(name, DIAMOND).replace("bg_diamond_mining", "bg_mining")
                restored = restored.replace(f"\n\t\t{technology}\n", "\n")
                self.assertEqual(re.sub(r"\s+", "", original), re.sub(r"\s+", "", restored))
        group = object_block(text("common/building_groups/sb_diamond_mining.txt"), "bg_diamond_mining")
        self.assertIn("parent_group = bg_mining", group)
        self.assertIn("discoverable_resource = yes", group)
        self.assertIn("depletable_resource = no", group)
        self.assertNotIn("auto_place_buildings = yes", group)

    def test_technology_callbacks_do_not_grant_or_force_diamonds(self):
        gates = text("common/scripted_effects/sb_resource_technology_gates_effects.txt")
        self.assertNotIn("building_diamond_mine", gates)
        self.assertNotIn("force_resource_discovery", gates)
        self.assertNotRegex(text("common/messages/sb_resource_gate_messages.txt"), r"sb_resource_\w+_diamonds_")

    def test_kimberley_stays_on_its_original_event_driven_building(self):
        original = object_block(text("common/buildings/sb_diamond_mines.txt"), DIAMOND)
        self.assertIn("building_group = bg_mining", original)
        self.assertIn("prospecting", original)
        effects = text("common/scripted_effects/sb_griqualand_west_effects.txt")
        initial = object_block(effects, "sb_kimberley_create_initial_diamond_mine")
        self.assertIn("building = building_diamond_mine", initial)
        self.assertIn("level = 1", initial)
        remaining = object_block(effects, "sb_kimberley_seed_remaining_potential")
        self.assertIn("add_resource_potential = building_diamond_mine", remaining)
        self.assertIn("amount = 18", remaining)
        self.assertIn("amount = 19", remaining)
        self.assertNotIn("building_sb_diamond_mine_", effects)
        kimberley = object_block(text("map_data/state_regions/04_subsaharan_africa.txt"), "STATE_GRIQUALAND_WEST")
        self.assertNotIn("building_sb_diamond_mine_", kimberley)

    def test_de_beers_can_operate_every_diamond_mine(self):
        company = text("common/company_types/zz_sb_de_beers_override.txt")
        for name in [DIAMOND] + [f"building_sb_diamond_mine_{tech}" for tech in
                                 ("dynamite", "pumpjacks", "pneumatic_tools")]:
            with self.subTest(building=name):
                self.assertIn(name, object_block(company, "building_types"))
                self.assertIn(f"is_building_type = {name}", object_block(company, "possible"))
                self.assertIn(f"has_potential_resource = {name}", object_block(company, "ai_will_do"))
                self.assertIn(f"{name} = {{", object_block(company, "ai_construction_targets"))


if __name__ == "__main__":
    unittest.main()
