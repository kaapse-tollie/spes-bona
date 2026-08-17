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


class NatalInterwarTests(unittest.TestCase):
    def test_natal_sugar_trait_is_permanent_and_owner_neutral(self):
        trait = object_block(
            "common/state_traits/sb_state_traits.txt",
            "state_trait_sb_natal_sugar_country",
        )
        history = text("common/history/global/sb_state_traits.txt")
        self.assertIn("building_sugar_plantation_throughput_add = 0.10", trait)
        self.assertIn("s:STATE_ZULULAND", history)
        self.assertIn("add_state_trait = state_trait_sb_natal_sugar_country", history)

    def test_responsible_government_normalizes_only_dependency_laws(self):
        effect = object_block(
            "common/scripted_effects/sb_subject_autonomy_effects.txt",
            "sb_apply_responsible_colony_subject_type_from_overlord",
        )
        self.assertIn("subject_type_sb_responsible_colony", effect)
        self.assertIn("subject_type_sb_responsible_colony_monarchy", effect)
        self.assertIn("has_law = law_type:law_subjecthood", effect)
        self.assertIn("activate_law = law_type:law_racial_segregation", effect)
        self.assertIn("has_law = law_type:law_extraction_economy", effect)
        self.assertIn("activate_law = law_type:law_agrarianism", effect)
        for law in (
            "law_national_supremacy",
            "law_cultural_exclusion",
            "law_multicultural",
            "law_interventionism",
            "law_laissez_faire",
        ):
            self.assertNotIn(f"activate_law = law_type:{law}", effect)

    def test_indenture_is_one_shot_and_uses_weighted_available_origins(self):
        monthly = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_interwar_monthly_housekeeping",
        )
        migration = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_select_indenture_origin_and_create_migration",
        )
        event = object_block("events/sb_natal_interwar_events.txt", "sb_natal_interwar.001")
        indian_country = object_block(
            "common/scripted_triggers/sb_natal_interwar_triggers.txt",
            "sb_natal_country_is_indian",
        )
        self.assertIn("has_variable = sb_klip_river_county_resolved_var", monthly)
        self.assertIn("1 = {", monthly)
        self.assertIn("99 = { }", monthly)
        self.assertIn("sb_natal_indenture_completed_var", monthly)
        for weight, culture in (
            (35, "tamil"),
            (25, "telegu"),
            (20, "hindustani"),
            (15, "bihari"),
            (5, "gujarati"),
        ):
            self.assertIn(f"{weight} = {{", migration)
            self.assertIn(f"cu:{culture}", migration)
        self.assertIn("create_mass_migration", migration)
        self.assertIn("state_is_homeland_of_indian_cultures = yes", indian_country)
        self.assertLess(
            migration.index("create_mass_migration"),
            migration.index("set_variable = sb_natal_indenture_completed_var"),
        )
        self.assertIn("cancellation_trigger", event)
        self.assertEqual(
            1, event.count("sb_natal_select_indenture_origin_and_create_migration = yes")
        )
        self.assertLess(
            event.index("sb_natal_select_indenture_origin_and_create_migration = yes"),
            event.index("option = {")
        )

    def test_colonial_industrialists_oppose_responsible_government_economics(self):
        identities = "common/scripted_effects/sb_interest_group_identity_effects.txt"
        apply_identity = object_block(identities, "sb_apply_colonial_industrialist_identity")
        remove_identity = object_block(identities, "sb_remove_colonial_industrialist_identity")
        cap_identity = object_block(identities, "sb_apply_cap_interest_group_identity")
        british_colony = object_block(
            identities, "sb_apply_generic_british_colony_interest_group_identity"
        )
        responsible = object_block(
            "common/scripted_effects/sb_subject_autonomy_effects.txt",
            "sb_apply_responsible_colony_subject_type_from_overlord",
        )
        self.assertIn("remove_ideology = ideology_laissez_faire", apply_identity)
        self.assertIn("add_ideology = ideology_colonialist", apply_identity)
        self.assertIn("remove_ideology = ideology_colonialist", remove_identity)
        self.assertIn("add_ideology = ideology_laissez_faire", remove_identity)
        self.assertIn("is_subject_type = subject_type_colony", cap_identity)
        self.assertIn("sb_apply_colonial_industrialist_identity = yes", british_colony)
        self.assertIn("sb_remove_colonial_industrialist_identity = yes", responsible)

    def test_natalia_political_cast_follows_intended_primary_culture(self):
        path = "common/scripted_effects/sb_natalia_effects.txt"
        boer_setup = object_block(path, "sb_apply_natalia_boer_republic_setup")
        british_shell = object_block(path, "sb_seed_british_natal_colony_shell")
        self.assertLess(
            boer_setup.index("add_primary_culture = cu:boer"),
            boer_setup.index("effect_starting_politics_conservative = yes"),
        )
        self.assertLess(
            british_shell.index("add_primary_culture = cu:anglo_african"),
            british_shell.index("effect_starting_politics_conservative = yes"),
        )

    def test_british_natal_replaces_anti_british_lobby(self):
        effect = object_block(
            "common/scripted_effects/sb_natalia_colony_effects.txt",
            "sb_ensure_british_natal_loyalist_lobby",
        )
        self.assertIn("lobby_anti_country", effect)
        self.assertIn("lobby_anti_overlord", effect)
        self.assertIn("disband_political_lobby = yes", effect)
        self.assertIn("type = lobby_pro_overlord", effect)
        for ig in ("ig_armed_forces", "ig_landowners", "ig_industrialists"):
            self.assertIn(f"add_interest_group = ig:{ig}", effect)

    def test_natalia_resistance_waits_for_all_boer_appeals(self):
        events = "events/sb_natal_crisis_events.txt"
        decision = object_block(
            "common/decisions/sb_zulu_decisions.txt", "natalia_raid_port_natal"
        )
        ultimatum = object_block(events, "sb_natal_crisis.110")
        defeat = object_block(events, "sb_natal_crisis.115")
        for block in (ultimatum, decision):
            for delay in (99, 96, 91):
                self.assertIn(f"days = {delay}", block)
            self.assertIn("sb_natalia_player_boer_support_pledged_var", block)
        self.assertIn("add = 1000", object_block(events, "sb_natal_crisis.111"))
        self.assertIn("add = -1000", object_block(events, "sb_natal_crisis.111"))
        self.assertIn("sb_natal_crisis_british_colony_finalization_tt", ultimatum)
        self.assertIn("sb_natal_crisis_british_colony_finalization_tt", defeat)

    def test_civil_rights_petition_and_gandhi_handoff_are_bounded(self):
        effects = text("common/scripted_effects/sb_natal_interwar_effects.txt")
        movement = object_block(
            "common/political_movements/sb_natal_interwar_movements.txt",
            "movement_sb_natal_civil_rights",
        )
        event = object_block("events/sb_natal_interwar_events.txt", "sb_natal_interwar.010")
        amendment = object_block(
            "common/amendments/sb_amendments.txt",
            "amendment_sb_natal_indian_civic_rights",
        )
        self.assertIn("game_date >= 1893.1.1", effects)
        self.assertIn("has_global_variable = gandhi_spawn", effects)
        self.assertIn("sb_natal_country_is_indian = yes", effects)
        self.assertIn("BIC_mohandas_karamchand_gandhi", movement)
        self.assertIn("political_movement_radicalism >= 0.75", effects)
        self.assertIn("days = 90", effects)
        self.assertIn("sb_natal_civil_rights_petition_spent_var", effects)
        self.assertIn("base = 20", event)
        self.assertIn("base = 80", event)
        self.assertIn("sb_natal_make_indian_pops_loyalist_10 = yes", event)
        self.assertIn("sb_natal_make_indian_pops_radical_20 = yes", event)
        self.assertEqual(29, amendment.count("cultural_acceptance_add = 35"))

    def test_anglo_zulu_ai_decision_has_no_player_deferral(self):
        decision = object_block(
            "common/decisions/sb_anglo_zulu_decisions.txt",
            "decision_sb_anglo_zulu_ultimatum",
        )
        event = object_block("events/sb_anglo_zulu_events.txt", "sb_anglo_zulu.010")
        self.assertIn("is_ai = yes", decision)
        self.assertIn("is_ai = yes", event)
        self.assertNotIn("cooldown", decision)
        self.assertNotIn("sb_anglo_zulu.010.b", event)

    def test_zululand_settlement_has_all_three_terminal_choices(self):
        event = object_block("events/sb_natal_interwar_events.txt", "sb_natal_interwar.030")
        trigger = object_block(
            "common/scripted_triggers/sb_natal_interwar_triggers.txt",
            "sb_natal_owns_complete_northern_zulu_core",
        )
        self.assertEqual(9, len(re.findall(r"p:x[0-9A-F]+\.state\.owner = ROOT", trigger)))
        self.assertIn("add_homeland = cu:anglo_african", event)
        self.assertIn("add_radicals = { value = 0.25 culture = cu:zulu }", event)
        self.assertIn("add_radicals = { value = -0.05 culture = cu:zulu }", event)
        self.assertIn("sb_natal_apply_zulu_chiefdom_settlement = yes", event)
        self.assertIn("sb_natal_gradual_zulu_restoration_var", event)
        self.assertIn("sb_natal_restore_zululand_as_puppet = yes", event)
        self.assertEqual(2, event.count("add = -1000"))
        self.assertEqual(1, event.count("add = 1000"))

    def test_chiefdom_amendment_and_decision_lock_bureaucracy(self):
        amendment = object_block(
            "common/amendments/sb_amendments.txt",
            "amendment_sb_zulu_chiefdom_settlement",
        )
        modifier = object_block(
            "common/static_modifiers/sb_natal_interwar_modifiers.txt",
            "sb_zulu_chiefdom_administration",
        )
        decision = object_block(
            "common/decisions/sb_natal_interwar_decisions.txt",
            "decision_sb_dismantle_zulu_chiefdom_settlement",
        )
        law_hook = object_block(
            "common/on_actions/sb_cape_law_on_actions.txt",
            "sb_on_natal_law_enactment_started",
        )
        self.assertIn("parent = law_sb_imperial_administration", amendment)
        self.assertIn("days = 1825", amendment)
        self.assertIn("can_repeal = { always = no }", amendment)
        self.assertIn("state_pop_qualifications_mult = -0.25", modifier)
        self.assertIn("state_food_security_add = 0.10", modifier)
        self.assertIn("sb_natal_zulu_chiefdom_dismantle_cooldown_var", decision)
        self.assertIn("add_radicals = { value = 0.10 culture = cu:zulu }", decision)
        self.assertIn("cancel_enactment = yes", law_hook)

    def test_restored_zululand_population_play_and_results_match_contract(self):
        effects_path = "common/scripted_effects/sb_natal_interwar_effects.txt"
        restore = object_block(effects_path, "sb_natal_restore_zululand_as_puppet")
        population = object_block(
            effects_path, "sb_natal_normalize_restored_zululand_population"
        )
        launch = object_block(effects_path, "sb_natal_launch_zulu_restoration_play")
        hooks = text("common/on_actions/sb_diplomatic_play_on_action_handlers.txt")
        self.assertIn("type = puppet", restore)
        self.assertIn("add_liberty_desire = 75", restore)
        self.assertIn("population_ratio = 0.30", population)
        self.assertIn("NOT = { culture = cu:zulu }", population)
        self.assertIn("population_ratio = 1", population)
        self.assertIn("type = dp_sb_zulu_restoration_secession", launch)
        self.assertIn("type = annex_country", launch)
        self.assertIn("ai_strategy_sb_zulu_restoration_resistance", launch)
        for handler in (
            "sb_natal_handle_zulu_restoration_backdown",
            "sb_natal_handle_zulu_restoration_war_end",
            "sb_natal_handle_zulu_restoration_wargoal_enforced",
        ):
            self.assertIn(f"{handler} = yes", hooks)

    def test_transvaal_appeal_creates_exact_treaty_and_territorial_payment(self):
        effects = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_create_trn_zulu_arms_treaty",
        )
        event = object_block("events/sb_natal_interwar_events.txt", "sb_natal_interwar.040")
        for province in ("xE1E455", "xE882CE", "x1A084B", "xBFA16B", "x41C070"):
            self.assertIn(province, effects)
        self.assertIn("add_infamy = 2.5", effects)
        self.assertIn("country = c:NAL value = -15", effects)
        self.assertIn("country = c:GBR value = -5", effects)
        self.assertIn("article = military_assistance", effects)
        self.assertIn("article = goods_transfer", effects)
        self.assertIn("goods = g:small_arms", effects)
        self.assertIn("quantity = 10", effects)
        self.assertIn("years = 5", effects)
        self.assertIn("base = 60", event)
        for value in ("add = 20", "add = 15", "add = -30", "add = -20"):
            self.assertIn(value, event)


if __name__ == "__main__":
    unittest.main()
