from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]
NATALIA_CORE = {
    "x5B124F", "xFF0EF1", "x552449", "xE0EB02", "x85695F", "xDE0EDE",
    "x7ACC38", "xB1F868", "x3CED3D", "x11A090", "xCD31DB",
}


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def object_block(path: str, name: str) -> str:
    source = text(path)
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} in {path}")
    return validate.extract_braced(source, match.start())


def object_block_from_source(source: str, name: str) -> str:
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name}")
    return validate.extract_braced(source, match.start())


class NatalInterwarTests(unittest.TestCase):
    def test_british_natal_disables_the_great_trek_before_conversion(self):
        colony_path = "common/scripted_effects/sb_natalia_colony_effects.txt"
        disable = object_block(
            colony_path, "sb_disable_natalia_great_trek_for_british_colony"
        )
        setup = object_block(colony_path, "sb_apply_british_natal_colony_setup")
        journal = object_block(
            "common/journal_entries/1-02_sb_great_trek.txt", "je_sb_great_trek"
        )
        completion = object_block(
            "events/sb_great_trek_events.txt", "sb_great_trek.043"
        )
        stage_one = object_block(
            "events/sb_great_trek_events.txt", "sb_great_trek.030"
        )

        self.assertLess(
            setup.index("sb_disable_natalia_great_trek_for_british_colony = yes"),
            setup.index("sb_convert_natalia_to_british_crown_colony = yes"),
        )
        self.assertIn("set_variable = sb_natalia_great_trek_disabled_var", disable)
        self.assertIn("remove_variable = sb_trek_stage2_pending_var", disable)
        self.assertIn("remove_modifier = sb_trek_migration_pull", disable)

        self.assertGreaterEqual(
            journal.count(
                "NOT = { has_variable = sb_natalia_great_trek_disabled_var }"
            ),
            3,
        )
        invalid = object_block_from_source(journal, "invalid")
        self.assertIn("has_variable = sb_natalia_great_trek_disabled_var", invalid)

        trigger = object_block_from_source(completion, "trigger")
        cancellation = object_block_from_source(completion, "cancellation_trigger")
        option = object_block_from_source(completion, "option")
        self.assertIn("has_journal_entry = je_sb_great_trek", trigger)
        self.assertIn("sb_natalia_great_trek_disabled_var", trigger)
        self.assertIn("has_journal_entry = je_sb_great_trek", cancellation)
        self.assertIn("sb_natalia_great_trek_disabled_var", cancellation)
        self.assertIn("sb_natalia_great_trek_disabled_var", option)
        self.assertIn("has_journal_entry = je_sb_great_trek", stage_one)
        self.assertGreaterEqual(
            stage_one.count("sb_natalia_great_trek_disabled_var"), 3
        )

    def test_british_natal_installs_governor_once_and_exiles_andries_immediately(self):
        colony_path = "common/scripted_effects/sb_natalia_colony_effects.txt"
        colony_source = text(colony_path)
        setup = object_block(colony_path, "sb_apply_british_natal_colony_setup")
        finalize = object_block(colony_path, "sb_finalize_british_natal_colony")
        monthly = object_block(
            "common/on_actions/sb_regional_on_action_handlers.txt",
            "sb_on_natal_colony_monthly_pulse_country",
        )

        self.assertEqual(1, colony_source.count("sb_install_british_natal_governor = yes"))
        self.assertIn("sb_install_british_natal_governor = yes", setup)
        self.assertNotIn("sb_ensure_british_natal_colony_governor", colony_source)
        self.assertNotIn("sb_install_british_natal_governor", monthly)

        self.assertLess(
            finalize.index("sb_mark_natalia_boer_leadership_for_deferred_exile = yes"),
            finalize.index("sb_exile_natalia_boer_leadership = yes"),
        )
        self.assertLess(
            finalize.index("sb_exile_natalia_boer_leadership = yes"),
            finalize.index("sb_apply_british_natal_colony_setup = yes"),
        )
        self.assertNotIn("move_partial_pop", finalize)

    def test_dingane_kills_piet_retief_before_the_blood_river_war(self):
        event = object_block("events/sb_natal_crisis_events.txt", "sb_natal_crisis.020")
        options = [
            validate.extract_braced(event, match.start())
            for match in re.finditer(r"^\s*option\s*=\s*\{", event, re.MULTILINE)
        ]
        rejection = next(
            option for option in options if "name = sb_natal_crisis.020.b" in option
        )
        self.assertIn("has_template = ORA_piet_retief", rejection)
        self.assertIn("is_character_alive = yes", rejection)
        self.assertIn("kill_character = { hidden = yes }", rejection)
        self.assertLess(
            rejection.index("kill_character = { hidden = yes }"),
            rejection.index("trigger_event = { id = sb_natal_crisis.050 days = 21 }"),
        )

    def test_natal_sugar_trait_is_permanent_and_owner_neutral(self):
        trait = object_block(
            "common/state_traits/sb_state_traits.txt",
            "state_trait_sb_natal_sugar_country",
        )
        history = text("common/history/global/sb_state_traits.txt")
        self.assertIn("building_sugar_plantation_throughput_add = 0.20", trait)
        self.assertIn("s:STATE_NATAL", history)
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

    def test_shepstone_event_is_scheduled_once_from_shared_colony_setup(self):
        colony_path = "common/scripted_effects/sb_natalia_colony_effects.txt"
        setup = object_block(colony_path, "sb_apply_british_natal_colony_setup")
        schedule = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_schedule_shepstone_system",
        )
        event = object_block("events/sb_natal_interwar_events.txt", "sb_natal_interwar.050")
        trigger = object_block_from_source(event, "trigger")
        cancellation = object_block_from_source(event, "cancellation_trigger")
        immediate = object_block_from_source(event, "immediate")

        self.assertEqual(1, setup.count("sb_natal_schedule_shepstone_system = yes"))
        self.assertIn("sb_natal_shepstone_pending_var", schedule)
        self.assertIn("sb_natal_shepstone_resolved_var", schedule)
        self.assertIn("id = sb_natal_interwar.050 days = 60 popup = yes", schedule)
        self.assertIn("sb_natal_is_british_colony = yes", trigger)
        self.assertIn("sb_natal_has_responsible_government = yes", trigger)
        self.assertIn("sb_natal_is_british_colony = yes", cancellation)
        self.assertIn("sb_natal_has_responsible_government = yes", cancellation)
        self.assertIn("remove_variable = sb_natal_shepstone_pending_var", immediate)
        self.assertIn("set_variable = sb_natal_shepstone_resolved_var", immediate)
        self.assertIn("base = 100", event)
        self.assertIn("base = 0", event)

    def test_shepstone_package_matches_the_approved_land_and_pop_contract(self):
        amendment = object_block(
            "common/amendments/sb_amendments.txt", "amendment_sb_shepstone_system"
        )
        accept = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_apply_shepstone_system",
        )
        decline = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_decline_shepstone_system",
        )

        self.assertIn("parent = law_autocracy", amendment)
        for law in (
            "law_homesteading",
            "law_peasant_proprietorship",
            "law_tenant_farmers",
            "law_commercialized_agriculture",
        ):
            self.assertIn(law, amendment)
        self.assertIn("building_subsistence_output_mult = 0.25", amendment)
        self.assertIn(
            "state_minimum_incorporated_subsistence_arable_land_add = 0.15",
            amendment,
        )
        self.assertNotIn("standard_of_living", amendment)
        self.assertIn("sponsor = PREV.ig:ig_armed_forces", accept)
        self.assertIn("culture = cu:zulu", accept)
        self.assertIn("NOT = { is_pop_type = peasants }", accept)
        self.assertIn("90 = { change_poptype = pop_type:peasants }", accept)
        self.assertIn("add_loyalists = { value = 0.20 culture = cu:zulu }", accept)
        self.assertIn("sb_natal_make_fully_accepted_pops_radical_10 = yes", accept)
        self.assertEqual(2, accept.count("days = 1825"))
        self.assertIn("sb_natal_schedule_indenture_program = yes", accept)
        self.assertIn("change_relations = { country = c:GBR value = -10 }", decline)
        self.assertIn("add_radicals = { value = 0.35 culture = cu:zulu }", decline)
        self.assertIn("sb_natal_make_fully_accepted_pops_loyalist_10 = yes", decline)
        self.assertNotIn("sb_natal_schedule_indenture_program", decline)

    def test_indenture_uses_a_fixed_je_and_exact_direct_cohort_sequence(self):
        effects_path = "common/scripted_effects/sb_natal_interwar_effects.txt"
        effects = text(effects_path)
        transfer = object_block(effects_path, "sb_natal_transfer_indenture_cohort")
        opening = object_block(effects_path, "sb_natal_open_indenture_program")
        recruit = object_block(effects_path, "sb_natal_recruit_next_indenture_cohort")
        schedule = object_block(effects_path, "sb_natal_schedule_indenture_program")
        event = object_block("events/sb_natal_interwar_events.txt", "sb_natal_interwar.001")
        option = object_block_from_source(event, "option")
        journal = object_block(
            "common/journal_entries/1-13_sb_natal_interwar.txt",
            "je_sb_natal_indenture_program",
        )
        button = object_block(
            "common/scripted_buttons/sb_natal_interwar_buttons.txt",
            "je_sb_natal_recruit_indian_workers_button",
        )
        old_modifiers = text("common/static_modifiers/sb_modifiers.txt")

        for days in range(3650, 6936, 365):
            self.assertIn(f"days = {days}", schedule)
        self.assertEqual(10, schedule.count("1 = { set_variable"))
        self.assertIn("s:STATE_NATAL.region_state:NAL", transfer)
        self.assertIn("culture = $CULTURE$", transfer)
        self.assertIn("is_pop_type = peasants", transfer)
        self.assertIn("total_size >= $SIZE$", transfer)
        self.assertIn("population = $SIZE$", transfer)
        self.assertNotIn("create_mass_migration", effects)
        self.assertNotIn("add_cultural_community", effects)
        self.assertIn(
            "sb_natal_transfer_indenture_cohort = { CULTURE = cu:tamil SIZE = 342 }",
            opening,
        )
        self.assertIn("type = amendment_sb_natal_indian_indenture_status", opening)
        self.assertIn("type = je_sb_natal_indenture_program", opening)
        sequence = (
            "telegu", "tamil", "bihari", "telegu", "tamil",
            "hindustani", "telegu", "tamil", "bihari", "gujarati",
        )
        positions = []
        for index, culture in enumerate(sequence):
            marker = (
                f"sb_natal_transfer_indenture_cohort = {{ CULTURE = cu:{culture} "
                "SIZE = 2000 }"
            )
            position = recruit.find(marker, positions[-1] + 1 if positions else 0)
            self.assertNotEqual(-1, position, (index, culture))
            positions.append(position)
        self.assertEqual(sorted(positions), positions)
        self.assertIn("months = 24", recruit)
        self.assertIn("timeout = 7300", journal)
        self.assertIn("complete = { always = no }", journal)
        self.assertIn("goal_add_value = { add = 10 }", journal)
        self.assertIn("sb_natal_bic_has_next_indenture_cohort = yes", button)
        self.assertIn("sb_natal_recruit_next_indenture_cohort = yes", button)
        self.assertIn("sb_natal_open_indenture_program = yes", option)
        self.assertNotIn("sb_natal_indenture_recruitment = {", old_modifiers)
        self.assertNotIn("sb_natal_indenture_emigration_recruitment = {", old_modifiers)

    def test_closed_borders_contract_distinguishes_natal_from_bic(self):
        trigger_path = "common/scripted_triggers/sb_natal_interwar_triggers.txt"
        effect_path = "common/scripted_effects/sb_natal_interwar_effects.txt"
        origin = object_block(trigger_path, "sb_natal_bic_has_indenture_origin")
        pending = object_block(effect_path, "sb_natal_update_pending_indenture_program")
        cancel = object_block(effect_path, "sb_natal_cancel_pending_indenture_program")
        journal = object_block(
            "common/journal_entries/1-13_sb_natal_interwar.txt",
            "je_sb_natal_indenture_program",
        )
        button = object_block(
            "common/scripted_buttons/sb_natal_interwar_buttons.txt",
            "je_sb_natal_recruit_indian_workers_button",
        )
        amendment = object_block(
            "common/amendments/sb_amendments.txt",
            "amendment_sb_natal_indian_indenture_status",
        )
        law_hook = object_block(
            "common/on_actions/sb_regional_on_action_handlers.txt",
            "sb_on_natal_interwar_law_activated",
        )

        self.assertIn("c:BIC ?=", origin)
        self.assertIn("is_subject_of = c:GBR", origin)
        self.assertNotIn("law_closed_borders", origin)
        self.assertIn("has_law = law_type:law_closed_borders", pending)
        self.assertIn("sb_natal_cancel_pending_indenture_program = yes", pending)
        self.assertIn("set_variable = sb_natal_indenture_lapsed_var", cancel)
        self.assertIn("has_law = law_type:law_closed_borders", journal)
        self.assertIn("NOT = { sb_natal_is_british_colony = yes }", journal)
        self.assertIn("NOT = { has_law = law_type:law_closed_borders }", button)
        self.assertIn("sb_natal_bic_has_indenture_origin = yes", button)
        self.assertIn("law_subjecthood", amendment)
        self.assertIn("law_racial_segregation", amendment)
        self.assertEqual(5, amendment.count("cultural_acceptance_add = 50"))
        self.assertIn("sb_natal_cancel_pending_indenture_program = yes", law_hook)

    def test_port_natal_migration_deterrent_has_a_closed_lifecycle(self):
        effect = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_refresh_port_natal_migration_deterrent",
        )
        modifier = object_block(
            "common/static_modifiers/sb_natal_interwar_modifiers.txt",
            "sb_port_natal_migration_deterrent",
        )
        setup = object_block(
            "common/scripted_effects/sb_natalia_colony_effects.txt",
            "sb_apply_british_natal_colony_setup",
        )
        startup = object_block(
            "common/on_actions/sb_startup_on_action_handlers.txt",
            "sb_on_game_started_after_lobby",
        )
        owner_change = object_block(
            "common/on_actions/sb_regional_on_action_handlers.txt",
            "sb_on_port_natal_state_owner_change",
        )

        self.assertIn("state_migration_pull_mult = -0.80", modifier)
        self.assertIn("owner = c:CAP", effect)
        self.assertIn("p:x279045.state.owner = c:CAP", effect)
        self.assertIn("sb_british_natal_ever_formed_global_var", effect)
        self.assertIn("remove_modifier = sb_port_natal_migration_deterrent", effect)
        self.assertIn("set_global_variable = sb_british_natal_ever_formed_global_var", setup)
        self.assertIn("remove_modifier = sb_port_natal_migration_deterrent", setup)
        self.assertIn("sb_natal_refresh_port_natal_migration_deterrent = yes", startup)
        self.assertIn("state_region = s:STATE_NATAL", owner_change)
        self.assertIn("sb_natal_refresh_port_natal_migration_deterrent = yes", owner_change)

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

    def test_boer_founders_precede_natalia_country_creation(self):
        path = "common/scripted_effects/sb_natalia_effects.txt"
        source = text(path)
        creation = object_block(path, "sb_create_natalia_republic_if_missing")
        self.assertIn("p:x5B124F.state", creation)
        self.assertIn("culture = cu:boer", creation)
        self.assertIn("population_ratio = 0.05", creation)
        self.assertLess(
            creation.index("move_partial_pop ="),
            creation.index("create_country ="),
        )
        self.assertNotIn("sb_transfer_ora_boer_founders_to_natalia", source)
        self.assertNotIn("sb_natalia_ora_boer_founders_transferred_var", source)

    def test_split_states_make_founder_relocation_pipeline_obsolete(self):
        path = "common/scripted_effects/sb_natalia_effects.txt"
        source = text(path)
        assignment = object_block(path, "sb_assign_natalia_republic_territory")
        direct = object_block(path, "sb_found_natalia_after_blood_river")
        peaceful = object_block(path, "sb_found_natalia_peacefully")
        guns_bargain = object_block(
            path, "sb_found_natalia_after_guns_bargain_rejection"
        )
        self.assertIn("s:STATE_NATAL", assignment)
        self.assertEqual(NATALIA_CORE, validate.object_values(assignment, "provinces"))
        self.assertNotIn("STATE_ZULULAND", assignment)
        self.assertNotIn("sb_relocate_inherited_natalia_buildings_to_zul", source)
        self.assertNotIn("sb_natalia_blood_river_building_transfer_pending_var", source)
        for founding in (direct, peaceful):
            self.assertLess(
                founding.index("sb_assign_natalia_republic_territory = yes"),
                founding.index("sb_apply_natalia_boer_republic_setup = yes"),
            )
        self.assertIn(
            "set_variable = sb_natalia_blood_river_military_setup_pending_var",
            guns_bargain,
        )

    def test_blood_river_natalia_uses_standard_boer_commando_without_levies(self):
        path = "common/scripted_effects/sb_natalia_effects.txt"
        military = object_block(
            path, "sb_apply_natalia_blood_river_military_setup"
        )
        direct = object_block(path, "sb_found_natalia_after_blood_river")
        peaceful = object_block(path, "sb_found_natalia_peacefully")

        self.assertLess(
            military.index("remove_building = building_conscription_center"),
            military.index("create_military_formation ="),
        )
        self.assertEqual(2, military.count("combat_unit = {"))
        self.assertEqual(2, military.count("count = 1"))
        self.assertIn("combat_unit_type_irregular_infantry", military)
        self.assertIn("combat_unit_type_dragoons", military)
        self.assertNotIn("service_type = conscript", military)
        self.assertNotIn("combat_unit_type_line_infantry", military)
        self.assertEqual(
            1, direct.count("sb_apply_natalia_blood_river_military_setup = yes")
        )
        self.assertIn("sb_apply_natalia_blood_river_military_setup = yes", peaceful)
        self.assertLess(
            peaceful.index("sb_apply_natalia_blood_river_military_setup = yes"),
            peaceful.index(
                "remove_variable = sb_natalia_blood_river_military_setup_pending_var"
            ),
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
        gandhi = object_block("events/sb_natal_interwar_events.txt", "sb_natal_interwar.060")
        amendment = object_block(
            "common/amendments/sb_amendments.txt",
            "amendment_sb_natal_indian_civic_rights",
        )
        replacement = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_replace_indenture_status_with_civic_rights",
        )
        self.assertIn("game_date >= 1893.1.1", effects)
        self.assertIn("has_global_variable = gandhi_spawn", effects)
        self.assertIn("BIC_mohandas_karamchand_gandhi", movement)
        self.assertIn("multiply = 20", movement)
        self.assertIn("political_movement_radicalism >= 0.75", effects)
        self.assertIn("days = 90", effects)
        self.assertIn("sb_natal_civil_rights_petition_spent_var", effects)
        self.assertNotIn("sb_natal_civil_rights_petition_requires_gandhi_var", effects)
        self.assertNotIn("sb_natal_civil_rights_petition_requires_gandhi_var", event)
        self.assertIn("base = 20", event)
        self.assertIn("base = 80", event)
        self.assertIn("sb_natal_replace_indenture_status_with_civic_rights = yes", event)
        self.assertIn("sb_natal_make_indian_pops_loyalist_10 = yes", event)
        self.assertIn("sb_natal_make_indian_pops_radical_20 = yes", event)
        self.assertEqual(29, amendment.count("cultural_acceptance_add = 60"))
        self.assertIn("amendment_sb_natal_indian_indenture_status", replacement)
        self.assertIn("remove_amendment = yes", replacement)
        self.assertIn("amendment_sb_natal_indian_civic_rights", replacement)
        self.assertIn("has_dlc_feature = ip2_content", gandhi)
        self.assertIn("game_date >= 1893.1.1", gandhi)
        self.assertIn("set_global_variable = gandhi_spawn", gandhi)
        self.assertIn("modifier_natal_indian_congress", gandhi)
        self.assertIn("add_trait = scarred", gandhi)

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
        self.assertNotIn("add_homeland = cu:anglo_african", event)
        responsible = object_block(
            "common/scripted_effects/sb_subject_autonomy_effects.txt",
            "sb_apply_responsible_colony_subject_type_from_overlord",
        )
        self.assertIn("s:STATE_NATAL", responsible)
        self.assertIn("add_homeland = cu:anglo_african", responsible)
        self.assertNotIn("STATE_ZULULAND", responsible)
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
        effects = text(effects_path)
        restore = object_block(effects_path, "sb_natal_restore_zululand_as_puppet")
        launch = object_block(effects_path, "sb_natal_launch_zulu_restoration_play")
        hooks = text("common/on_actions/sb_diplomatic_play_on_action_handlers.txt")
        self.assertIn("type = puppet", restore)
        self.assertIn("add_liberty_desire = 75", restore)
        self.assertIn("s:STATE_ZULULAND", restore)
        self.assertIn("province = p:xBE6FEE", restore)
        for province in (
            "xBE6FEE", "x1A084B", "xBFA16B", "x9E9742", "x88FAD4",
            "x904EBE", "x41C070", "xE882CE", "xE1E455",
        ):
            self.assertIn(province, restore)
        self.assertNotIn("STATE_NATAL", restore)
        self.assertNotIn("population_ratio", restore)
        self.assertNotIn("sb_natal_normalize_restored_zululand_population", effects)
        self.assertNotIn("sb_restore_zululand_population_split_after_zulu_defeat", effects)
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
        trigger = object_block(
            "common/scripted_triggers/sb_natal_interwar_triggers.txt",
            "sb_natal_trn_arms_treaty_possible",
        )
        effects = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_create_trn_zulu_arms_treaty",
        )
        event = object_block("events/sb_natal_interwar_events.txt", "sb_natal_interwar.040")
        for province in ("xE1E455", "xE882CE", "x1A084B", "xBFA16B", "x41C070"):
            self.assertIn(province, effects)
        self.assertIn("change_infamy = 2.5", effects)
        self.assertNotIn("add_infamy", effects)
        self.assertIn("country = c:NAL value = -15", effects)
        self.assertIn("country = c:GBR value = -5", effects)
        self.assertIn("article = military_assistance", effects)
        self.assertIn("article = goods_transfer", effects)
        self.assertIn("goods = g:small_arms", effects)
        self.assertIn("quantity = 10", effects)
        self.assertIn("years = 5", effects)
        self.assertIn("article = military_assistance", trigger)
        self.assertNotIn("article = goods_transfer", trigger)
        self.assertNotIn("inputs =", trigger)
        self.assertIn("base = 60", event)
        for value in ("add = 20", "add = 15", "add = -30", "add = -20"):
            self.assertIn(value, event)

    def test_civil_rights_event_trigger_has_no_gandhi_dependency(self):
        event = object_block("events/sb_natal_interwar_events.txt", "sb_natal_interwar.010")
        trigger = object_block_from_source(event, "trigger")
        self.assertNotIn("if = {", trigger)
        self.assertNotIn("gandhi", trigger.casefold())

    def test_launch_sensitive_new_scripts_use_utf8_bom(self):
        for path in (
            "common/scripted_triggers/sb_natal_interwar_triggers.txt",
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "common/journal_entries/1-13_sb_natal_interwar.txt",
            "common/scripted_buttons/sb_natal_interwar_buttons.txt",
            "common/static_modifiers/sb_natal_interwar_modifiers.txt",
            "common/ideologies/sb_natal_interwar_ideologies.txt",
            "common/political_movements/sb_natal_interwar_movements.txt",
            "events/sb_pink_map_events.txt",
            "common/history/ai/zz_sb_portuguese_kongo_secret_goal.txt",
        ):
            self.assertTrue((ROOT / path).read_bytes().startswith(b"\xef\xbb\xbf"), path)


if __name__ == "__main__":
    unittest.main()
