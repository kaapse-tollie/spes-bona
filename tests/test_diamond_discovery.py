"""Owner-gated diamond surveys. Native scheduling and notifications require DP replay."""
from decimal import Decimal, ROUND_HALF_UP
from operator import add, mul, sub
import re
import unittest

from tests.test_resource_rework_implementation import DIAMOND, ROOT, SURVEY_PATH, object_block
from tests.test_zulu_institutions_laws import statements

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


SURVEYS = SURVEY_PATH.read_text(encoding="utf-8-sig")
HOOKS = text("common/on_actions/sb_mineral_discoveries_on_actions.txt")
VALUES = text("common/script_values/sb_diamond_surveys.txt")
TRIGGER = text("common/scripted_triggers/sb_diamond_surveys.txt")


def evaluate(nodes, inputs, pick=max):
    """Run the arithmetic subset used by both survey values, including native min/max bounds."""
    current = Decimal(0)
    for key, _, arg in nodes:
        if key == "save_temporary_value_as":
            inputs["scope:" + arg] = current
        elif key == "round":
            current = current.to_integral_value(rounding=ROUND_HALF_UP)
        elif key == "integer_range":
            bounds = [evaluate(v, inputs, pick) if isinstance(v, list) else Decimal(v) for _, _, v in arg]
            current = pick(bounds)
        else:
            value = evaluate(arg, inputs, pick) if isinstance(arg, list) else Decimal(inputs.get(arg, arg))
            if key == "value":
                current = value
            else:
                current = {"add": add, "subtract": sub, "multiply": mul, "min": max, "max": min}[key](current, value)
    return current


class DiamondDiscoveryTests(unittest.TestCase):
    def test_new_campaign_seeds_eight_fixed_reserves_without_buildable_levels(self):
        mapping = object_block(SURVEYS, "sb_register_diamond_deposits")
        entries = []
        for region, _, calls in statements(mapping):
            ((effect, _, args),) = calls
            self.assertEqual(effect, "sb_register_diamond_deposit")
            fields = {key: value for key, _, value in args}
            entries.append((region.removeprefix("s:"), fields["TECH"], int(fields["LEVELS"])))
        self.assertCountEqual(entries, [(state, tech, levels) for state, (tech, levels) in DEPOSITS.items()])
        self.assertEqual(95, sum(levels for _, _, levels in entries))
        seed = object_block(SURVEYS, "sb_register_diamond_deposit")
        self.assertIn("NOT = { has_variable = sb_diamond_reserve_size }", seed)
        self.assertIn("name = sb_diamond_remaining value = $LEVELS$", seed)
        self.assertIn("name = sb_diamond_gate value = flag:$TECH$", seed)
        self.assertIn("every_scope_state = { sb_diamond_check_new_owner = yes }", seed)
        self.assertIn("sb_register_diamond_deposits = yes", object_block(HOOKS, "sb_on_mineral_discoveries_game_started"))
        states = text("map_data/state_regions/04_subsaharan_africa.txt")
        self.assertNotIn("diamond_mine", states)
        self.assertEqual(1, SURVEYS.count("change_resource_potential ="))
        self.assertNotIn("force_resource_discovery", SURVEYS)
        self.assertNotIn("create_building", SURVEYS)

    def test_only_the_territorial_owner_can_qualify_or_expand_in_a_survey_region(self):
        gate = statements(object_block(TRIGGER, "sb_diamond_owner_has_survey_technology"))
        for (_, _, branch), tech in zip(gate, ("dynamite", "pumpjacks", "pneumatic_tools")):
            self.assertEqual(branch[0][2][0][2], "flag:" + tech)
            self.assertIn(("owner", "=", [("has_technology_researched", "=", tech)]), branch)
        self.assertEqual(gate[-1], ("trigger_else", "=", [("always", "=", "no")]))
        self.assertNotIn("invest", TRIGGER.split("\n", 1)[1])
        possible = object_block(text("common/buildings/sb_diamond_mines.txt"), "possible")
        self.assertIn("limit = { state_region = { has_variable = sb_diamond_gate } }", possible)
        self.assertIn("sb_diamond_owner_has_survey_technology = yes", possible)
        owner = object_block(SURVEYS, "sb_diamond_check_new_owner")
        self.assertIn("limit = { sb_diamond_owner_has_survey_technology = yes }", owner)
        self.assertIn("state_region = { sb_start_diamond_surveys = yes }", owner)
        research = object_block(SURVEYS, "sb_diamond_check_research")
        self.assertIn("has_variable = sb_diamond_waiting_for_$TECH$ has_technology_researched = $TECH$", research)
        self.assertIn("every_scope_state", research)
        self.assertIn("var:sb_diamond_gate = flag:$TECH$", research)
        on_research = object_block(HOOKS, "sb_on_mineral_discoveries_acquired_technology")
        for tech in {tech for tech, _ in DEPOSITS.values()}:
            self.assertIn(f"sb_diamond_check_research = {{ TECH = {tech} }}", on_research)
        on_transfer = object_block(HOOKS, "sb_on_mineral_discoveries_state_owner_change")
        self.assertIn("sb_diamond_check_new_owner = yes", on_transfer)
        for state in DEPOSITS:
            self.assertIn(f"state_region = s:{state}", on_transfer)

    def test_one_rolling_window_per_region_including_misses_and_ownership_changes(self):
        start = object_block(SURVEYS, "sb_start_diamond_surveys")
        self.assertIn("NOT = { has_variable = sb_diamond_surveys_started }", start)
        self.assertLess(start.index("set_variable = sb_diamond_surveys_started"), start.index("sb_roll_diamond_survey_year = yes"))
        self.assertNotIn("remove_variable = sb_diamond_surveys_started", SURVEYS)
        year = statements(object_block(SURVEYS, "sb_roll_diamond_survey_year"))
        self.assertEqual([key for key, _, _ in year], ["random_scope_state", "trigger_event"])
        state, renewal = year[0][2], year[1][2]
        self.assertEqual(state[0][2], [("sb_diamond_owner_has_survey_technology", "=", "yes")])
        roll = dict((k, v) for k, _, v in state)["random"]
        self.assertEqual(roll[0], ("chance", "=", "owner.sb_diamond_annual_discovery_chance"))
        self.assertEqual(renewal, [("on_action", "=", "sb_next_diamond_survey_year"), ("days", "=", "365")])
        self.assertIn("var:sb_diamond_remaining > 0", object_block(HOOKS, "sb_next_diamond_survey_year"))
        selection = [("save_scope_as", "=", "sb_diamond_survey_state"),
                     ("random_province_in_southern_africa_old", "=", [
                         ("limit", "=", [("state", "=", "scope:sb_diamond_survey_state")]),
                         ("save_scope_as", "=", "sb_diamond_survey_province"),
                     ])]
        self.assertEqual(selection, roll[1:3])
        self.assertNotIn("random_province", [k for k, _, _ in roll])
        pending = dict((k, v) for k, _, v in roll)["state_region"]
        self.assertEqual([k for k, _, _ in pending], ["set_variable", "trigger_event"])
        self.assertIn(("value", "=", "scope:sb_diamond_survey_province"), pending[0][2])
        self.assertIn(("days", "=", [("0", "bare", "0"), ("364", "bare", "364")]), pending[1][2])

    def test_delivery_revalidates_the_same_land_and_consumes_the_receipt_once(self):
        entry = object_block(HOOKS, "sb_deliver_diamond_survey")
        self.assertIn("exists = var:sb_diamond_pending_site", entry)
        find = object_block(SURVEYS, "sb_deliver_diamond_find")
        order = [
            "var:sb_diamond_pending_site = { save_scope_as = sb_diamond_site }",
            "remove_variable = sb_diamond_pending_site",
            "exists = scope:sb_diamond_site.state.owner",
            "scope:sb_diamond_site.state = { sb_diamond_owner_has_survey_technology = yes }",
            "name = sb_diamond_found_levels value = sb_diamond_find_size",
            "count = scope:sb_diamond_found_levels",
            "type = building_diamond_mine amount = 1",
            "name = sb_diamond_remaining subtract = scope:sb_diamond_found_levels",
            "scope:sb_diamond_site.state.owner = { post_notification = sb_diamond_survey_discovery }",
        ]
        positions = [find.index(token) for token in order]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("sb_roll_diamond_survey_year", find)

    def test_annual_chance_approximates_daily_odds_for_the_owner(self):
        # The engine rejected the former six-decimal coefficient on launch.
        self.assertNotRegex(VALUES, r"\d+\.\d{6,}")
        chance = statements(object_block(VALUES, "sb_diamond_annual_discovery_chance"))
        for bonus in (-1, -0.15, 0, 0.1, 0.25, 0.35, 0.5, 0.6, 0.75):
            with self.subTest(bonus=bonus):
                result = evaluate(chance, {
                    "modifier:country_resource_discovery_chance_mult": str(bonus),
                    "define:NEconomy|BASE_RESOURCE_DISCOVER_CHANCE": "0.02",
                })
                expected = 100 * (1 - (1 - 0.0002 * (1 + bonus)) ** 365)
                self.assertAlmostEqual(float(result), expected, delta=0.001)

    def test_province_iterator_region_covers_every_survey_deposit(self):
        region = object_block(text("common/geographic_regions/sb_geographic_regions.txt"),
                              "REPLACE:geographic_region_southern_africa_old")
        self.assertTrue(set(DEPOSITS) <= set(re.findall(r"\bSTATE_\w+", region)))

    def test_find_bounds_and_final_remainder_use_the_original_geology(self):
        size = statements(object_block(VALUES, "sb_diamond_find_size"))
        for _, total in DEPOSITS.values():
            for left in range(1, total + 1):
                limits = {
                    "var:sb_diamond_reserve_size": total, "var:sb_diamond_remaining": left,
                    "define:NEconomy|RESOURCE_DISCOVER_MIN_FRACTION": "0.2",
                    "define:NEconomy|RESOURCE_DISCOVER_MAX_FRACTION": "0.5",
                }
                minimum = max(1, int(total * 0.2 + 0.5))
                bonus = max(1, int(total * 0.5 + 0.5))
                self.assertEqual(evaluate(size, limits, min), min(left, minimum))
                self.assertEqual(evaluate(size, limits, max), min(left, minimum + bonus))

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

    def test_one_mine_for_construction_and_de_beers(self):
        mines = text("common/buildings/sb_diamond_mines.txt")
        self.assertEqual([DIAMOND], re.findall(r"^(building_\w+) = \{", mines, re.M))
        company = text("common/company_types/zz_sb_de_beers_override.txt")
        self.assertNotIn("building_sb_diamond_mine_", company)
        for key, target in (("building_types", DIAMOND), ("possible", "is_building_type = " + DIAMOND),
                            ("ai_will_do", "has_potential_resource = " + DIAMOND),
                            ("ai_construction_targets", DIAMOND + " = {")):
            self.assertIn(target, object_block(company, key))


if __name__ == "__main__":
    unittest.main()
