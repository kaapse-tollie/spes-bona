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


class PinkMapBechuanalandIntegrationTests(unittest.TestCase):
    def test_decision_keeps_vanilla_gate_and_accepts_colonial_network(self):
        decision = object_block("common/decisions/zz_sb_pink_map_override.txt", "pink_map")
        colonization = object_block(
            "common/scripted_triggers/sb_pink_map_triggers.txt",
            "sb_pink_map_has_qualifying_colonization",
        )
        for token in (
            "has_dlc_feature = ip4_content",
            "c:POR ?= this",
            "c:IBE ?= this",
            "is_subject = no",
            "has_variable = portuguese_colonialism_je_completed",
        ):
            self.assertIn(token, decision)
        self.assertIn("any_subject_or_below", colonization)
        self.assertIn("country_is_colonial_or_company = yes", colonization)
        for state in ("STATE_KAZEMBE", "STATE_ZAMBIA", "STATE_ZAMBEZI"):
            self.assertEqual(2, colonization.count(f"state_region = s:{state}"))

    def test_decision_is_visible_but_blocked_during_corridor(self):
        decision = object_block("common/decisions/zz_sb_pink_map_override.txt", "pink_map")
        shown, possible = decision.split("possible = {", 1)
        self.assertNotIn("sb_bechuanaland_corridor_open_global_var", shown)
        self.assertIn(
            "NOT = { has_global_variable = sb_bechuanaland_corridor_open_global_var }",
            possible,
        )
        self.assertIn("sb_pink_map_bechuanaland_resolved_tt", possible)

    def test_decision_routes_every_terminal_outcome(self):
        decision = object_block("common/decisions/zz_sb_pink_map_override.txt", "pink_map")
        self.assertIn("set_variable = sb_pink_map_precedes_bechuanaland_var", decision)
        self.assertIn("sb_pink_map_begin_full_claim_route = yes", decision)
        self.assertIn("sb_bechuanaland_terminal_outcome_boer_global_var", decision)
        self.assertIn("sb_pink_map_begin_boer_claim_route = yes", decision)
        self.assertIn("sb_bechuanaland_terminal_outcome_british_global_var", decision)
        self.assertIn("sb_bechuanaland_terminal_outcome_swa_global_var", decision)
        self.assertIn("sb_pink_map_dispatch_to_recorded_arbiter = yes", decision)
        self.assertGreaterEqual(decision.count("sb_pink_map_begin_full_claim_route = yes"), 2)

    def test_claim_packages_keep_all_pink_map_claims_on_portugal(self):
        path = "common/scripted_effects/sb_pink_map_effects.txt"
        full = object_block(path, "sb_pink_map_add_full_claim_package")
        boer = object_block(path, "sb_pink_map_add_boer_settlement_claim_package")
        for state in ("STATE_KAZEMBE", "STATE_ZAMBIA", "STATE_ZAMBEZI"):
            self.assertIn(f"s:{state} = {{ add_claim = ROOT }}", full)
        self.assertIn("STATE_KAZEMBE", boer)
        self.assertIn("STATE_ZAMBIA", boer)
        self.assertNotIn("STATE_ZAMBEZI", boer)

        redirect = object_block(
            "common/scripted_effects/sb_eastern_sphere_effects.txt",
            "sb_portugal_redirect_southern_africa_claims_to_mzq",
        )
        for state in ("STATE_KAZEMBE", "STATE_ZAMBIA", "STATE_ZAMBEZI"):
            self.assertNotIn(state, redirect)
        self.assertNotIn(
            "sb_mozambique_move_zambezi_claim_to_mzq",
            text("common/scripted_effects/sb_eastern_sphere_effects.txt"),
        )

    def test_corridor_records_durable_terminal_outcome_and_exact_zero_is_boer(self):
        path = "common/scripted_effects/sb_bechuanaland_corridor_effects.txt"
        british = object_block(path, "sb_bechuanaland_record_british_terminal_outcome")
        combined = object_block(path, "sb_bechuanaland_record_boer_swa_terminal_outcome")
        invalid = object_block(path, "sb_bechuanaland_record_invalid_terminal_outcome")
        self.assertIn("sb_bechuanaland_terminal_outcome_invalid_global_var", invalid)
        self.assertIn("sb_bechuanaland_terminal_outcome_british_global_var", british)
        self.assertIn("sb_bechuanaland_pink_map_arbiter_var", british)
        self.assertIn("sb_bechuanaland_pink_map_claimant_var", british)
        self.assertIn("sb_bechuanaland_influence_score_var < 0", combined)
        self.assertIn("sb_bechuanaland_terminal_outcome_swa_global_var", combined)
        self.assertIn("# Exact zero belongs to the Boer settlement.", combined)
        self.assertIn("sb_bechuanaland_terminal_outcome_boer_global_var", combined)

    def test_pre_corridor_pink_map_suppresses_only_basin_rewards(self):
        settlement = object_block(
            "common/scripted_effects/sb_bechuanaland_corridor_effects.txt",
            "sb_bechuanaland_apply_boer_swa_settlement",
        )
        self.assertGreaterEqual(settlement.count("sb_pink_map_precedes_bechuanaland = yes"), 3)
        self.assertIn("s:STATE_BOTSWANA = { add_claim", settlement)
        british_source = text("common/scripted_effects/sb_bechuanaland_corridor_effects.txt")
        self.assertRegex(
            british_source,
            r"NOT = \{ sb_pink_map_precedes_bechuanaland = yes \}\s*"
            r"\}\s*s:STATE_ZAMBIA = \{ add_claim = c:GBR \}",
        )

    def test_arbitration_uses_saved_arbiter_and_three_vanilla_choices(self):
        event = object_block("events/sb_pink_map_events.txt", "sb_pink_map.010")
        self.assertEqual(3, len(re.findall(r"^\toption = \{", event, re.MULTILINE)))
        self.assertIn("var:sb_pink_map_petitioner_scope", event)
        self.assertIn("save_scope_as = gbr_scope", event)
        self.assertIn("default_option = yes", event)
        self.assertNotIn("c:GBR", event)
        for follow_up in ("sb_pink_map.020", "sb_pink_map.030", "sb_pink_map.040"):
            self.assertIn(follow_up, event)

    def test_acceptance_score_bands_and_weights_match_specification(self):
        events = text("events/sb_pink_map_events.txt")
        for base in ("base = 5", "base = 15", "base = 380"):
            self.assertIn(base, events)
        for trigger in (
            "sb_pink_map_ai_relations_cordial",
            "sb_pink_map_ai_relations_amicable",
            "sb_pink_map_ai_relations_friendly",
            "sb_pink_map_ai_relations_poor",
            "sb_pink_map_ai_relations_cold",
            "sb_pink_map_ai_relations_hostile",
            "sb_pink_map_ai_rivals_petitioner",
            "sb_pink_map_ai_petitioner_is_great_power",
            "sb_pink_map_ai_same_power_bloc",
            "sb_pink_map_ai_has_defensive_pact",
            "sb_pink_map_ai_has_alliance",
            "sb_pink_map_ai_petitioner_navy_at_least_three_quarters",
            "sb_pink_map_ai_petitioner_navy_at_least_equal",
            "sb_pink_map_ai_petitioner_gdp_at_least_three_quarters",
            "sb_pink_map_ai_petitioner_gdp_at_least_equal",
        ):
            self.assertEqual(3, events.count(f"trigger = {{ {trigger} = yes }}"), trigger)

        triggers = text("common/scripted_triggers/sb_pink_map_triggers.txt")
        self.assertIn("multiply = 0.75", triggers)
        self.assertIn("naval_power_projection < ROOT.naval_power_projection", triggers)
        self.assertIn("gdp < ROOT.gdp", triggers)

    def test_acceptance_clears_competing_claims_and_defiance_preserves_them(self):
        path = "common/scripted_effects/sb_pink_map_effects.txt"
        accepted = object_block(path, "sb_pink_map_accept_arbitration")
        defiance = object_block(path, "sb_pink_map_apply_defiance")
        self.assertIn("sb_pink_map_remove_competing_corridor_claims = yes", accepted)
        self.assertNotIn("sb_pink_map_remove_competing_corridor_claims", defiance)
        self.assertIn("change_relations = { country = ROOT value = -50 }", defiance)
        self.assertIn("sb_pink_map_defiance_arbiter_var", defiance)
        self.assertIn("sb_pink_map_add_full_claim_package = yes", defiance)

    def test_missing_arbiter_falls_back_to_direct_claims(self):
        repair = object_block(
            "common/scripted_effects/sb_pink_map_effects.txt",
            "sb_pink_map_repair_missing_arbiter",
        )
        self.assertIn("has_variable = pink_map_seeking", repair)
        self.assertIn("is_country_alive = no", repair)
        self.assertIn("sb_pink_map_begin_full_claim_route = yes", repair)
        monthly = text("common/scripted_effects/sb_eastern_sphere_effects.txt")
        self.assertIn("sb_pink_map_repair_missing_arbiter = yes", monthly)

    def test_portuguese_ai_support_is_bounded_and_defiance_is_temporary(self):
        path = "common/ai_strategies/sb_ai_strategies.txt"
        planning = object_block(path, "ai_strategy_sb_portuguese_african_planning")
        hostility = object_block(path, "ai_strategy_sb_pink_map_defiance_hostility")
        for token in (
            "wanted_navy_size = { value = 6 }",
            "wanted_num_supply_ships = { value = 120 }",
            "bg_navy = 1.5",
            "add = 1.0",
            "score = { value = 500 }",
            "country_definition = cd:POR",
            "country_definition = cd:IBE",
        ):
            self.assertIn(token, planning)
        self.assertIn("country_definition = cd:KON", text("common/scripted_triggers/sb_pink_map_triggers.txt"))
        self.assertIn("STATE_NORTH_ANGOLA", text("common/scripted_triggers/sb_pink_map_triggers.txt"))
        self.assertIn("add = 25", hostility)
        self.assertIn("has_journal_entry = je_the_pink_map", hostility)
        monthly = object_block(
            "common/scripted_effects/sb_eastern_sphere_effects.txt",
            "sb_eastern_sphere_monthly_housekeeping",
        )
        self.assertLess(
            monthly.index("sb_pink_map_cleanup_defiance_hostility = yes"),
            monthly.index("country_definition = cd:POR"),
        )

    def test_portugal_starts_with_a_conquer_goal_against_kongo(self):
        history = text("common/history/ai/zz_sb_portuguese_kongo_secret_goal.txt")
        match = re.search(r"^\s*c:POR\s*\?=\s*\{", history, re.MULTILINE)
        self.assertIsNotNone(match)
        portugal = validate.extract_braced(history, match.start())
        self.assertIn("set_secret_goal = {", portugal)
        self.assertIn("country = c:KON", portugal)
        self.assertIn("secret_goal = conquer", portugal)
        self.assertNotIn("country = c:KON", text("common/history/diplomacy/sb_relations.txt"))


if __name__ == "__main__":
    unittest.main()
