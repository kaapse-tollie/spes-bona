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
        options = [
            validate.extract_braced(event, match.start())
            for match in re.finditer(r"^\s*option\s*=\s*\{", event, re.MULTILINE)
        ]

        self.assertEqual(1, setup.count("sb_natal_schedule_shepstone_system = yes"))
        self.assertLess(
            setup.index("sb_convert_natalia_to_british_crown_colony = yes"),
            setup.index("sb_natal_schedule_shepstone_system = yes"),
        )
        self.assertIn("sb_natal_shepstone_pending_var", schedule)
        self.assertIn("sb_natal_shepstone_resolved_var", schedule)
        self.assertIn("has_variable = sb_natalia_british_colony_resolved_var", schedule)
        self.assertNotIn("sb_natal_is_british_colony = yes", schedule)
        self.assertIn("name = sb_natal_shepstone_pending_var\n\t\t\tdays = 45", schedule)
        self.assertIn("id = sb_natal_interwar.050 days = 30 popup = yes", schedule)
        self.assertIn("sb_natal_is_british_colony = yes", trigger)
        self.assertIn("sb_natal_has_responsible_government = yes", trigger)
        self.assertIn("sb_natal_is_british_colony = yes", cancellation)
        self.assertIn("sb_natal_has_responsible_government = yes", cancellation)
        self.assertNotIn("sb_natal_shepstone_resolved_var", cancellation)
        self.assertIn("remove_variable = sb_natal_shepstone_pending_var", immediate)
        self.assertIn("set_variable = sb_natal_shepstone_resolved_var", immediate)
        self.assertIn("name = sb_natal_shepstone_event_open_var", immediate)
        self.assertIn("days = 120", immediate)
        self.assertEqual(2, len(options))
        for option in options:
            self.assertIn(
                "remove_variable = sb_natal_shepstone_event_open_var", option
            )
        self.assertIn("base = 80", options[0])
        self.assertIn("add = 1000", options[0])
        self.assertIn("base = 20", options[1])
        self.assertIn("add = -1000", options[1])

        monthly = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_interwar_monthly_housekeeping",
        )
        self.assertEqual(1, monthly.count("sb_natal_schedule_shepstone_system = yes"))
        self.assertIn("sb_natal_is_british_colony = yes", monthly)
        self.assertLess(
            monthly.index("sb_natal_recover_interrupted_shepstone_system = yes"),
            monthly.index("sb_natal_schedule_shepstone_system = yes"),
        )

        recovery = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_recover_interrupted_shepstone_system",
        )
        self.assertIn("has_variable = sb_natal_shepstone_resolved_var", recovery)
        self.assertIn("sb_natal_shepstone_accepted_var", recovery)
        self.assertIn("sb_natal_shepstone_declined_var", recovery)
        self.assertIn("sb_natal_shepstone_event_open_var", recovery)
        self.assertIn("remove_variable = sb_natal_shepstone_resolved_var", recovery)
        self.assertIn("name = sb_natal_shepstone_pending_var", recovery)
        self.assertIn("id = sb_natal_interwar.050 days = 1 popup = yes", recovery)

    def test_shepstone_and_klip_river_are_independent_colony_followups(self):
        colony = object_block(
            "common/scripted_effects/sb_natalia_colony_effects.txt",
            "sb_finalize_british_natal_colony",
        )
        event = object_block(
            "events/sb_natal_interwar_events.txt", "sb_natal_interwar.050"
        )
        options = [
            validate.extract_braced(event, match.start())
            for match in re.finditer(r"^\s*option\s*=\s*\{", event, re.MULTILINE)
        ]
        scheduler = object_block(
            "common/scripted_effects/sb_klip_river_county_effects.txt",
            "sb_schedule_klip_river_county_question",
        )
        monthly = object_block(
            "common/scripted_effects/sb_klip_river_county_effects.txt",
            "sb_klip_river_county_monthly_housekeeping",
        )

        self.assertIn("sb_schedule_klip_river_county_question = yes", colony)
        self.assertIn("sb_klip_river_prepare_standard_boer_flight = yes", colony)
        self.assertLess(
            colony.index("sb_apply_british_natal_colony_setup = yes"),
            colony.index("sb_schedule_klip_river_county_question = yes"),
        )
        self.assertEqual(2, len(options))
        for option in options:
            self.assertNotIn("sb_schedule_klip_river_county_question", option)
            self.assertNotIn("sb_klip_river_continue_after_shepstone", option)
        for days in (120, 210, 300, 390):
            self.assertIn(
                f"id = sb_klip_river_county.001 days = {days} popup = no",
                scheduler,
            )
        self.assertEqual(4, scheduler.count("id = sb_klip_river_county.001 days ="))
        self.assertNotIn("sb_natal_shepstone_resolved_var", monthly)
        self.assertNotIn("sb_natal_shepstone_outcome_selected_var", monthly)

    def test_shepstone_package_matches_the_approved_land_and_pop_contract(self):
        amendment = object_block(
            "common/amendments/sb_amendments.txt", "amendment_sb_shepstone_system"
        )
        accept = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_apply_shepstone_system",
        )
        hidden = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_apply_shepstone_hidden_mechanics",
        )
        population_conversion = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_convert_zulu_population_share_to_peasants",
        )
        natal_population_conversion = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_convert_zulu_population_share_to_peasants_in_natal",
        )
        non_zulu_conversion = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_convert_non_zulu_peasant_share_to_laborers",
        )
        staged_non_zulu_conversion = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_convert_non_zulu_peasant_share_with_staging_culture",
        )
        yearly_handler = object_block(
            "common/on_actions/sb_regional_on_action_handlers.txt",
            "sb_on_natal_shepstone_yearly_pulse_country",
        )
        yearly_router = object_block(
            "common/on_actions/sb_on_actions.txt", "on_yearly_pulse_country"
        )
        decline = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_decline_shepstone_system",
        )
        movement_attraction = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_sync_declined_shepstone_zulu_movement_attraction",
        )
        movement_modifier = object_block(
            "common/static_modifiers/sb_natal_interwar_modifiers.txt",
            "sb_shepstone_refusal_zulu_movement_attraction",
        )
        movement_creation = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_create_zulu_national_movement",
        )
        monthly = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_interwar_monthly_housekeeping",
        )
        event = object_block(
            "events/sb_natal_interwar_events.txt", "sb_natal_interwar.050"
        )
        accept_option = next(
            validate.extract_braced(event, match.start())
            for match in re.finditer(r"^\s*option\s*=\s*\{", event, re.MULTILINE)
            if "name = sb_natal_interwar.050.a"
            in validate.extract_braced(event, match.start())
        )

        self.assertIn("parent = law_autocracy", amendment)
        for law in (
            "law_homesteading",
            "law_peasant_proprietorship",
            "law_tenant_farmers",
            "law_commercialized_agriculture",
        ):
            self.assertIn(law, amendment)
        self.assertIn("building_subsistence_output_mult = 0.30", amendment)
        self.assertIn(
            "building_minimum_incorporated_subsistence_employment_add = 0.80",
            amendment,
        )
        self.assertIn(
            "state_minimum_incorporated_subsistence_arable_land_add = 0.15",
            amendment,
        )
        self.assertNotIn("standard_of_living", amendment)
        self.assertIn("sponsor = PREV.ig:ig_armed_forces", accept)
        self.assertIn("set_variable = sb_natal_shepstone_declined_var", decline)
        self.assertNotIn("random_list", accept)
        self.assertNotIn("change_poptype", accept)
        self.assertNotIn("sb_natal_schedule_indenture_program", accept)
        self.assertNotIn("random_list", hidden)
        self.assertIn(
            "sb_natal_convert_zulu_population_share_to_peasants_in_natal = yes",
            hidden,
        )
        for staging_culture in ("promethean", "ainu", "maori"):
            self.assertIn(
                f"STAGING_CULTURE = cu:{staging_culture}",
                natal_population_conversion,
            )
        self.assertIn("culture = cu:zulu", population_conversion)
        self.assertIn(
            "NOT = { is_pop_type = peasants }",
            population_conversion,
        )
        self.assertIn("target = $STAGING_CULTURE$", population_conversion)
        self.assertIn("value = 0.20", population_conversion)
        self.assertIn("change_poptype = pop_type:peasants", population_conversion)
        self.assertIn("culture = $STAGING_CULTURE$", population_conversion)
        self.assertIn("target = cu:zulu", population_conversion)
        self.assertIn("value = 1.00", population_conversion)
        self.assertLess(
            population_conversion.index("target = $STAGING_CULTURE$"),
            population_conversion.index("change_poptype = pop_type:peasants"),
        )
        self.assertLess(
            population_conversion.index("change_poptype = pop_type:peasants"),
            population_conversion.index("target = cu:zulu"),
        )
        self.assertIn(
            "sb_natal_convert_non_zulu_peasant_share_to_laborers = yes",
            hidden,
        )
        self.assertLess(
            hidden.index(
                "sb_natal_convert_zulu_population_share_to_peasants_in_natal = yes"
            ),
            hidden.index(
                "sb_natal_convert_non_zulu_peasant_share_to_laborers = yes"
            ),
        )
        self.assertLess(
            hidden.index(
                "sb_natal_convert_non_zulu_peasant_share_to_laborers = yes"
            ),
            hidden.index("sb_natal_schedule_indenture_program = yes"),
        )
        self.assertIn("country_definition = cd:NAL", non_zulu_conversion)
        self.assertIn("s:STATE_NATAL.region_state:NAL", non_zulu_conversion)
        self.assertIn(
            "has_amendment = amendment_type:amendment_sb_shepstone_system",
            non_zulu_conversion,
        )
        for staging_culture in ("promethean", "ainu", "maori"):
            self.assertIn(
                f"STAGING_CULTURE = cu:{staging_culture}", non_zulu_conversion
            )
        self.assertIn("every_scope_pop", staged_non_zulu_conversion)
        self.assertIn("is_pop_type = peasants", staged_non_zulu_conversion)
        self.assertIn("NOT = { culture = cu:zulu }", staged_non_zulu_conversion)
        self.assertIn("target = $STAGING_CULTURE$", staged_non_zulu_conversion)
        self.assertIn("value = 0.10", staged_non_zulu_conversion)
        self.assertIn(
            "change_poptype = pop_type:laborers", staged_non_zulu_conversion
        )
        self.assertIn(
            "target = scope:sb_natal_non_zulu_original_culture_scope",
            staged_non_zulu_conversion,
        )
        self.assertNotIn("random_list", staged_non_zulu_conversion)
        self.assertIn("country_definition = cd:NAL", yearly_handler)
        self.assertIn(
            "has_amendment = amendment_type:amendment_sb_shepstone_system",
            yearly_handler,
        )
        self.assertIn(
            "sb_natal_convert_non_zulu_peasant_share_to_laborers = yes",
            yearly_handler,
        )
        self.assertIn(
            "sb_on_natal_shepstone_yearly_pulse_country", yearly_router
        )
        self.assertIn("sb_natal_schedule_indenture_program = yes", hidden)
        self.assertIn("add_loyalists = { value = 0.25 culture = cu:zulu }", accept)
        self.assertIn("cu:zulu =", accept)
        self.assertIn("add_fervor = -10", accept)
        self.assertIn("sb_natal_make_fully_accepted_pops_radical_10 = yes", accept)
        self.assertIn(
            "custom_tooltip = sb_natal_shepstone_make_fully_accepted_radical_10_tt",
            accept,
        )
        self.assertEqual(2, accept.count("days = 1825"))
        self.assertIn("custom_tooltip = sb_natal_shepstone_accept_tt", accept_option)
        self.assertIn("sb_natal_apply_shepstone_system = yes", accept_option)
        self.assertIn("hidden_effect =", accept_option)
        self.assertIn(
            "sb_natal_apply_shepstone_hidden_mechanics = yes", accept_option
        )
        self.assertIn("change_relations = { country = c:GBR value = -10 }", decline)
        self.assertIn("add_radicals = { value = 0.50 culture = cu:zulu }", decline)
        self.assertIn("cu:zulu =", decline)
        self.assertIn("add_fervor = 10", decline)
        self.assertIn("sb_natal_make_fully_accepted_pops_loyalist_10 = yes", decline)
        self.assertIn(
            "custom_tooltip = sb_natal_shepstone_make_fully_accepted_loyalist_10_tt",
            decline,
        )
        self.assertIn(
            "custom_tooltip = sb_natal_shepstone_decline_zulu_movement_attraction_tt",
            decline,
        )
        self.assertIn(
            "sb_natal_sync_declined_shepstone_zulu_movement_attraction = yes",
            decline,
        )
        self.assertNotIn("sb_natal_schedule_indenture_program", decline)

        self.assertIn("political_movement_pop_attraction_mult = 1.00", movement_modifier)
        self.assertIn("has_variable = sb_natal_shepstone_declined_var", movement_attraction)
        self.assertIn(
            "sb_natal_shepstone_rejection_attraction_applied_var",
            movement_attraction,
        )
        self.assertIn("is_political_movement_type = movement_cultural_minority", movement_attraction)
        self.assertIn("culture = cu:zulu", movement_attraction)
        self.assertIn(
            "remove_modifier = sb_shepstone_refusal_zulu_movement_attraction",
            movement_attraction,
        )
        self.assertIn(
            "name = sb_shepstone_refusal_zulu_movement_attraction",
            movement_attraction,
        )
        self.assertIn("months = 300", movement_attraction)
        self.assertIn("is_decaying = yes", movement_attraction)
        for caller in (movement_creation, monthly):
            self.assertIn(
                "sb_natal_sync_declined_shepstone_zulu_movement_attraction = yes",
                caller,
            )

        localization = text("localization/english/sb_natal_interwar_l_english.yml")
        loyalist_line = next(
            line
            for line in localization.splitlines()
            if "sb_natal_shepstone_make_fully_accepted_loyalist_10_tt:0" in line
        )
        conversion_line = next(
            line
            for line in localization.splitlines()
            if "sb_natal_shepstone_accept_tt:0" in line
        )
        self.assertIn("#v 80%#! of every", conversion_line)
        self.assertNotIn("chance", conversion_line)
        self.assertIn("[concept_loyalist]", loyalist_line)
        self.assertNotIn("[concept_radical]", loyalist_line)

    def test_repealing_shepstone_applies_half_package_and_allows_reinstatement(self):
        effects_path = "common/scripted_effects/sb_natal_interwar_effects.txt"
        scheduler = object_block(
            effects_path, "sb_natal_schedule_shepstone_repeal_response"
        )
        consequences = object_block(
            effects_path, "sb_natal_apply_repealed_shepstone_consequences"
        )
        attraction = object_block(
            effects_path,
            "sb_natal_sync_repealed_shepstone_zulu_movement_attraction",
        )
        restoration = object_block(
            effects_path, "sb_natal_restore_shepstone_system"
        )
        loyalists = object_block(
            effects_path, "sb_natal_make_fully_accepted_pops_loyalist_5"
        )
        modifiers_path = "common/static_modifiers/sb_natal_interwar_modifiers.txt"
        movement_modifier = object_block(
            modifiers_path, "sb_shepstone_repeal_zulu_movement_attraction"
        )
        garrison_modifier = object_block(
            modifiers_path, "sb_shepstone_repeal_colonial_garrison_opposition"
        )
        industrialists_modifier = object_block(
            modifiers_path, "sb_shepstone_repeal_industrialists_approval"
        )
        monthly = object_block(effects_path, "sb_natal_interwar_monthly_housekeeping")
        movement_creation = object_block(
            effects_path, "sb_natal_create_zulu_national_movement"
        )
        event = object_block(
            "events/sb_natal_interwar_events.txt", "sb_natal_interwar.055"
        )
        trigger = object_block_from_source(event, "trigger")
        immediate = object_block_from_source(event, "immediate")
        options = [
            validate.extract_braced(event, match.start())
            for match in re.finditer(r"^\s*option\s*=\s*\{", event, re.MULTILINE)
        ]
        repeal_option = next(
            option
            for option in options
            if "name = sb_natal_interwar.055.a" in option
        )
        restore_option = next(
            option
            for option in options
            if "name = sb_natal_interwar.055.b" in option
        )

        self.assertIn("political_movement_pop_attraction_mult = 0.50", movement_modifier)
        self.assertIn("has_variable = sb_natal_shepstone_accepted_var", scheduler)
        self.assertIn("amendment_sb_shepstone_system", scheduler)
        self.assertIn("sb_natal_shepstone_repeal_response_pending_var", scheduler)
        self.assertIn("sb_natal_shepstone_repeal_response_resolved_var", scheduler)
        self.assertIn("id = sb_natal_interwar.055 days = 1 popup = yes", scheduler)

        self.assertIn("has_variable = sb_natal_shepstone_repealed_var", attraction)
        self.assertIn("sb_natal_shepstone_repeal_attraction_applied_var", attraction)
        self.assertIn("is_political_movement_type = movement_cultural_minority", attraction)
        self.assertIn("culture = cu:zulu", attraction)
        self.assertIn("name = sb_shepstone_repeal_zulu_movement_attraction", attraction)
        self.assertIn("months = 120", attraction)
        self.assertIn("is_decaying = yes", attraction)
        self.assertNotIn("add_radicals", attraction)
        self.assertNotIn("add_fervor", attraction)
        self.assertNotIn("add_loyalists", attraction)

        self.assertIn("change_relations = { country = c:GBR value = -5 }", consequences)
        self.assertIn("add_radicals = { value = 0.25 culture = cu:zulu }", consequences)
        self.assertIn("add_fervor = 5", consequences)
        self.assertIn(
            "sb_natal_make_fully_accepted_pops_loyalist_5 = yes", consequences
        )
        self.assertIn("set_variable = sb_natal_shepstone_repealed_var", consequences)
        self.assertIn(
            "sb_natal_sync_repealed_shepstone_zulu_movement_attraction = yes",
            consequences,
        )
        self.assertIn("sb_shepstone_repeal_colonial_garrison_opposition", consequences)
        self.assertIn("sb_shepstone_repeal_industrialists_approval", consequences)
        self.assertEqual(2, consequences.count("days = 1825"))
        self.assertIn("value = 0.05", loyalists)
        self.assertNotIn("value = 0.10", loyalists)
        self.assertIn("interest_group_approval_add = -1", garrison_modifier)
        self.assertIn("interest_group_approval_add = 0.5", industrialists_modifier)

        self.assertIn("sb_natal_shepstone_repeal_response_pending_var", trigger)
        self.assertIn(
            "remove_variable = sb_natal_shepstone_repeal_response_pending_var",
            immediate,
        )
        self.assertIn(
            "set_variable = sb_natal_shepstone_repeal_response_resolved_var",
            immediate,
        )
        self.assertEqual(2, len(options))
        self.assertIn("default_option = yes", repeal_option)
        self.assertIn(
            "sb_natal_apply_repealed_shepstone_consequences = yes", repeal_option
        )
        self.assertIn("base = 100", repeal_option)
        self.assertIn("custom_tooltip = sb_natal_shepstone_accept_tt", restore_option)
        self.assertIn("sb_natal_restore_shepstone_system = yes", restore_option)
        self.assertIn("base = 0", restore_option)
        self.assertIn("type = amendment_sb_shepstone_system", restoration)
        self.assertIn("sponsor = PREV.ig:ig_armed_forces", restoration)
        self.assertIn(
            "sb_natal_convert_zulu_population_share_to_peasants_in_natal = yes",
            restoration,
        )
        self.assertNotIn(
            "sb_natal_convert_non_zulu_peasant_share_to_laborers", restoration
        )
        self.assertNotIn("sb_natal_schedule_indenture_program", restoration)
        for caller in (monthly, movement_creation):
            self.assertIn(
                "sb_natal_sync_repealed_shepstone_zulu_movement_attraction = yes",
                caller,
            )
        self.assertIn("sb_natal_schedule_shepstone_repeal_response = yes", monthly)

        localization = text("localization/english/sb_natal_interwar_l_english.yml")
        for key in (
            "sb_natal_interwar.055.t",
            "sb_natal_interwar.055.d",
            "sb_natal_interwar.055.f",
            "sb_natal_interwar.055.a",
            "sb_natal_interwar.055.b",
            "sb_shepstone_repeal_zulu_movement_attraction",
            "sb_shepstone_repeal_zulu_movement_attraction_desc",
            "sb_shepstone_repeal_colonial_garrison_opposition",
            "sb_shepstone_repeal_industrialists_approval",
            "sb_natal_shepstone_make_fully_accepted_loyalist_5_tt",
            "sb_natal_shepstone_repeal_zulu_movement_attraction_tt",
        ):
            self.assertIn(f" {key}:0", localization)

    def test_indenture_uses_automatic_monthly_forced_transfer_cycles(self):
        effects_path = "common/scripted_effects/sb_natal_interwar_effects.txt"
        effects = text(effects_path)
        transfer = object_block(effects_path, "sb_natal_transfer_indenture_cohort")
        staged_transfer = object_block(
            effects_path, "sb_natal_transfer_indenture_cohort_from_state"
        )
        opening = object_block(effects_path, "sb_natal_open_indenture_program")
        cohort = object_block(
            effects_path, "sb_natal_transfer_current_indenture_cohort"
        )
        recruit = object_block(effects_path, "sb_natal_recruit_next_indenture_cohort")
        start_cycle = object_block(effects_path, "sb_natal_start_indenture_cycle")
        process_cycle = object_block(effects_path, "sb_natal_process_indenture_cycle")
        suspend = object_block(effects_path, "sb_natal_suspend_indenture_program")
        resume = object_block(effects_path, "sb_natal_resume_indenture_program")
        migrate_journal = object_block(
            effects_path, "sb_natal_migrate_indenture_program_journal"
        )
        schedule = object_block(effects_path, "sb_natal_schedule_indenture_program")
        next_cohort = object_block(
            "common/scripted_triggers/sb_natal_interwar_triggers.txt",
            "sb_natal_bic_has_next_indenture_cohort",
        )
        event = object_block("events/sb_natal_interwar_events.txt", "sb_natal_interwar.001")
        option = object_block_from_source(event, "option")
        tick_event = object_block(
            "events/sb_natal_interwar_events.txt", "sb_natal_interwar.002"
        )
        journal = object_block(
            "common/journal_entries/1-13_sb_natal_interwar.txt",
            "je_sb_natal_indenture_program_v2",
        )
        legacy_journal = object_block(
            "common/journal_entries/1-13_sb_natal_interwar.txt",
            "je_sb_natal_indenture_program",
        )
        suspend_button = object_block(
            "common/scripted_buttons/sb_natal_interwar_buttons.txt",
            "je_sb_natal_suspend_indenture_program_button",
        )
        resume_button = object_block(
            "common/scripted_buttons/sb_natal_interwar_buttons.txt",
            "je_sb_natal_resume_indenture_program_button",
        )
        intensify_button = object_block(
            "common/scripted_buttons/sb_natal_interwar_buttons.txt",
            "je_sb_natal_intensify_indenture_program_button",
        )
        intensify_visible = object_block_from_source(intensify_button, "visible")
        intensify_possible = object_block_from_source(intensify_button, "possible")
        intensify_selected = object_block_from_source(intensify_button, "selected")
        costs = object_block(
            "common/static_modifiers/sb_natal_interwar_modifiers.txt",
            "sb_natal_indenture_program_costs",
        )
        scaled_costs = object_block(
            "common/static_modifiers/sb_natal_interwar_modifiers.txt",
            "sb_natal_indenture_program_scaled_costs",
        )
        add_costs = object_block(
            effects_path, "sb_natal_add_indenture_program_costs"
        )
        remove_costs = object_block(
            effects_path, "sb_natal_remove_indenture_program_costs"
        )
        intensify = object_block(
            effects_path, "sb_natal_intensify_indenture_program"
        )
        cleanup = object_block(effects_path, "sb_natal_cleanup_indenture_program")
        modifiers = text("common/static_modifiers/sb_natal_interwar_modifiers.txt")
        indenture_status = object_block(
            "common/amendments/sb_amendments.txt",
            "amendment_sb_natal_indian_indenture_status",
        )

        for days in range(3650, 6936, 365):
            self.assertIn(f"days = {days}", schedule)
        self.assertEqual(10, schedule.count("1 = { set_variable"))
        self.assertIn("s:STATE_NATAL.region_state:NAL", transfer)
        self.assertIn("culture = $CULTURE$", transfer)
        self.assertIn("is_pop_type = peasants", transfer)
        self.assertIn("total_size >= $SIZE$", transfer)
        self.assertNotIn("change_poptype", transfer)
        self.assertIn("population = $SIZE$", staged_transfer)
        self.assertIn("target = $STAGING_CULTURE$", staged_transfer)
        self.assertIn("culture = $STAGING_CULTURE$", staged_transfer)
        self.assertIn("change_poptype = $DESTINATION_POP_TYPE$", staged_transfer)
        self.assertIn("target = $CULTURE$", staged_transfer)
        self.assertLess(
            staged_transfer.index("population = $SIZE$"),
            staged_transfer.index("change_poptype = $DESTINATION_POP_TYPE$"),
        )
        for staging_culture in ("promethean", "ainu", "maori"):
            self.assertIn(f"STAGING_CULTURE = cu:{staging_culture}", transfer)
        self.assertNotIn("create_mass_migration", effects)
        self.assertNotIn("add_cultural_community", effects)
        self.assertIn("CULTURE = cu:tamil", opening)
        self.assertIn("SIZE = 342", opening)
        self.assertIn("DESTINATION_POP_TYPE = pop_type:laborers", opening)
        self.assertIn("type = amendment_sb_natal_indian_indenture_status", opening)
        self.assertIn("type = je_sb_natal_indenture_program_v2", opening)
        self.assertEqual(
            ["telegu", "tamil", "bihari", "telegu", "tamil", "hindustani"],
            re.findall(r"CULTURE = cu:(\w+)\s+SIZE = 400", cohort),
        )
        self.assertEqual(2, recruit.count("sb_natal_transfer_current_indenture_cohort = yes"))
        self.assertIn("has_variable = sb_natal_indenture_intensified_var", recruit)
        self.assertEqual(6, next_cohort.count("SIZE = 400"))
        self.assertNotIn("SIZE = 1500", next_cohort)
        self.assertIn("days = 27", start_cycle)
        self.assertIn("id = sb_natal_interwar.002 months = 1", start_cycle)
        self.assertIn(
            "sb_natal_migrate_indenture_program_journal = yes", process_cycle
        )
        self.assertLess(
            process_cycle.index("sb_natal_migrate_indenture_program_journal = yes"),
            process_cycle.index("sb_natal_recruit_next_indenture_cohort = yes"),
        )
        self.assertIn("sb_natal_recruit_next_indenture_cohort = yes", process_cycle)
        self.assertIn("hidden = yes", tick_event)
        self.assertNotIn("timeout =", journal)
        self.assertNotIn("is_goal_complete", journal)
        self.assertIn("text = je_sb_natal_indenture_program_completion_tt", journal)
        self.assertNotIn("text = je_sb_natal_indenture_program_goal", journal)
        self.assertIn("hidden_trigger = {", journal)
        self.assertIn("has_variable = sb_natal_indian_origin_population_var", journal)
        self.assertIn("var:sb_natal_indian_origin_population_var >= 100000", journal)
        self.assertIn("value = 0", journal)
        self.assertIn("add = root.var:sb_natal_indian_origin_population_var", journal)
        self.assertNotIn("divide = 10000", journal)
        self.assertIn("goal_add_value = { value = 100000 }", journal)
        self.assertIn("progressbar = yes", journal)
        self.assertIn(
            "progress_desc = je_sb_natal_indenture_program_progress", journal
        )
        self.assertNotIn("scripted_progress_bar", journal)
        self.assertIn("sb_natal_complete_indenture_program = yes", journal)
        self.assertIn("possible = { always = no }", legacy_journal)
        self.assertIn(
            "has_journal_entry = je_sb_natal_indenture_program_v2", legacy_journal
        )
        self.assertIn("has_journal_entry = je_sb_natal_indenture_program", migrate_journal)
        self.assertIn(
            "add_journal_entry = { type = je_sb_natal_indenture_program_v2 }",
            migrate_journal,
        )
        self.assertIn("name = sb_natal_indenture_cycle_index_var value = 0", migrate_journal)
        self.assertIn("sb_natal_suspend_indenture_program = yes", suspend_button)
        self.assertIn("sb_natal_resume_indenture_program = yes", resume_button)
        self.assertNotIn("sb_natal_recruit_next_indenture_cohort", resume_button)
        self.assertIn(
            "scripted_button = je_sb_natal_intensify_indenture_program_button",
            journal,
        )
        self.assertIn("sb_natal_intensify_indenture_program = yes", intensify_button)
        self.assertNotIn("sb_natal_indenture_suspended_var", intensify_visible)
        self.assertIn("sb_natal_indenture_intensity_requires_active_tt", intensify_possible)
        self.assertIn(
            "NOT = { has_variable = sb_natal_indenture_suspended_var }",
            intensify_possible,
        )
        self.assertIn(
            "has_variable = sb_natal_indenture_intensified_var", intensify_selected
        )
        self.assertNotIn(
            "NOT = { has_variable = sb_natal_indenture_intensified_var }",
            intensify_button,
        )
        self.assertIn("set_variable = sb_natal_indenture_intensified_var", intensify)
        self.assertIn("remove_variable = sb_natal_indenture_intensified_var", intensify)
        self.assertIn(
            "NOT = { has_variable = sb_natal_indenture_suspended_var }", intensify
        )
        self.assertIn("sb_natal_add_indenture_program_costs = yes", intensify)
        self.assertIn("sb_natal_clear_indenture_cycle = yes", intensify)
        self.assertIn("sb_natal_start_indenture_cycle = yes", intensify)
        self.assertNotIn("sb_natal_transfer_current_indenture_cohort", intensify)
        self.assertNotIn("sb_natal_recruit_next_indenture_cohort", intensify)
        self.assertNotIn("sb_natal_indenture_intensified_var", suspend)
        self.assertNotIn("sb_natal_indenture_intensified_var", resume)
        self.assertIn("remove_variable = sb_natal_indenture_intensified_var", cleanup)
        self.assertIn("country_bureaucracy_cost_add = 25", costs)
        self.assertIn("country_expenses_add = 100", costs)
        self.assertIn("country_bureaucracy_cost_add = 75", scaled_costs)
        self.assertIn("country_expenses_add = 950", scaled_costs)
        self.assertEqual(
            2, add_costs.count("value = var:sb_natal_indian_origin_population_var")
        )
        self.assertEqual(2, add_costs.count("divide = 100000"))
        self.assertEqual(2, add_costs.count("max = 1"))
        self.assertEqual(2, add_costs.count("min = 0"))
        self.assertIn("# f(x) = x^2", add_costs)
        self.assertIn(
            "NOT = { has_variable = sb_natal_indian_origin_population_var }",
            add_costs,
        )
        self.assertIn(
            "set_variable = { name = sb_natal_indian_origin_population_var value = 0 }",
            add_costs,
        )
        self.assertGreaterEqual(
            add_costs.count("has_variable = sb_natal_indian_origin_population_var"),
            2,
        )
        self.assertEqual(2, add_costs.count("multiply = 2"))
        self.assertEqual(
            2, add_costs.count("has_variable = sb_natal_indenture_intensified_var")
        )
        self.assertNotIn("add = 1", add_costs)
        self.assertNotIn("divide = 2", add_costs)
        self.assertIn("name = sb_natal_indenture_program_scaled_costs", add_costs)
        self.assertIn(
            "remove_modifier = sb_natal_indenture_program_scaled_costs", add_costs
        )
        self.assertIn(
            "remove_modifier = sb_natal_indenture_program_scaled_costs", remove_costs
        )
        for indenture_scope in (costs, scaled_costs, indenture_status, opening):
            self.assertNotIn("migration_restrictiveness", indenture_scope)
            self.assertNotIn("migration_pull", indenture_scope)
        for obsolete_modifier in (
            "sb_natal_indenture_recruitment",
            "sb_natal_indenture_emigration_recruitment",
        ):
            self.assertNotIn(f"{obsolete_modifier} = {{", modifiers)
            self.assertNotIn(obsolete_modifier, effects)
        self.assertIn("sb_natal_open_indenture_program = yes", option)
        self.assertNotIn("je_sb_natal_recruit_indian_workers_button", journal)
        self.assertNotIn("sb_natal_indenture_recruitment_count_var", effects)
        self.assertNotIn("sb_natal_indenture_recruitment_cooldown_var", effects)
        localization = text("localization/english/sb_natal_interwar_l_english.yml")
        self.assertIn(" je_sb_natal_indenture_program_completion_tt:0", localization)
        self.assertNotIn(" je_sb_natal_indenture_program_goal:0", localization)
        self.assertIn("#v 100,000#!", localization)
        self.assertIn(" je_sb_natal_indenture_program_progress:0", localization)
        self.assertIn(
            ' je_sb_natal_intensify_indenture_program_button:0 "Intensify Recruitment"',
            localization,
        )
        self.assertIn("monthly recruitment and all programme costs are doubled", localization)
        self.assertIn("changing intensity during active recruitment begins a fresh full-month cycle", localization)
        self.assertIn("#v 400#!", localization)
        self.assertIn(
            "desc = je_sb_natal_indenture_program_status_intensified", journal
        )
        self.assertIn(" sb_natal_indenture_intensity_requires_active_tt:0", localization)
        self.assertIn(
            "[ROOT.GetCountry.MakeScope.Var('sb_natal_indian_origin_population_var').GetValue|K]",
            localization,
        )
        self.assertNotIn("JournalEntry.MakeScope.Var", localization)

    def test_indenture_validity_and_ai_safeguards_match_the_design(self):
        trigger_path = "common/scripted_triggers/sb_natal_interwar_triggers.txt"
        effect_path = "common/scripted_effects/sb_natal_interwar_effects.txt"
        origin = object_block(trigger_path, "sb_natal_bic_has_indenture_origin")
        validity = object_block(trigger_path, "sb_natal_indenture_program_is_valid")
        pending = object_block(effect_path, "sb_natal_update_pending_indenture_program")
        cancel = object_block(effect_path, "sb_natal_cancel_pending_indenture_program")
        update = object_block(effect_path, "sb_natal_update_indenture_program")
        cleanup = object_block(effect_path, "sb_natal_cleanup_indenture_program")
        journal = object_block(
            "common/journal_entries/1-13_sb_natal_interwar.txt",
            "je_sb_natal_indenture_program_v2",
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
        self.assertIn("sb_natal_is_british_colony = yes", validity)
        self.assertIn("sb_natal_bic_has_indenture_origin = yes", validity)
        self.assertIn("sb_natal_has_shepstone_system = yes", validity)
        self.assertIn("has_law = law_type:law_closed_borders", validity)
        self.assertIn("has_law = law_type:law_closed_borders", pending)
        self.assertIn("NOT = { sb_natal_bic_has_indenture_origin = yes }", pending)
        self.assertIn("NOT = { sb_natal_has_shepstone_system = yes }", pending)
        self.assertIn("sb_natal_cancel_pending_indenture_program = yes", pending)
        self.assertIn("set_variable = sb_natal_indenture_lapsed_var", cancel)
        self.assertIn("NOT = { sb_natal_indenture_program_is_valid = yes }", journal)
        self.assertIn("sb_natal_cleanup_indenture_program = yes", journal)
        for condition in (
            "scaled_debt >= 0.50",
            "bureaucracy >= 0",
            "net_fixed_income >= 0",
            "scaled_debt < 0.10",
        ):
            self.assertIn(condition, update)
        self.assertNotIn("scaled_debt > 0.20", update)
        self.assertNotIn("set_variable = sb_natal_indenture_intensified_var", update)
        self.assertIn("remove_variable = sb_natal_indenture_intensified_var", update)
        self.assertIn("Baseline calibration: AI Natal recruits at the normal rate", update)
        self.assertIn("sb_natal_remove_indenture_program_costs = yes", cleanup)
        self.assertIn("sb_natal_clear_indenture_cycle = yes", cleanup)
        self.assertIn("law_subjecthood", amendment)
        self.assertIn("law_racial_segregation", amendment)
        self.assertEqual(6, amendment.count("cultural_acceptance_add = 50"))
        self.assertIn("country_natal_indian_cultural_acceptance_add = 50", amendment)
        self.assertIn("sb_natal_cancel_pending_indenture_program = yes", law_hook)

    def test_natal_indian_ethnogenesis_and_consolidation_are_exact_shares(self):
        effects_path = "common/scripted_effects/sb_natal_interwar_effects.txt"
        completion = object_block(
            effects_path, "sb_natal_establish_natal_indian_community"
        )
        consolidation = object_block(
            effects_path, "sb_natal_convert_indian_population_to_natal_indian"
        )
        culture = object_block(
            "common/cultures/sb_southern_african_cultures.txt", "natal_indian"
        )
        heritage = object_block(
            "common/discrimination_traits/sb_heritages.txt", "heritage_natal_indian"
        )
        indian_scope = object_block(
            "common/scripted_triggers/sb_natal_interwar_triggers.txt",
            "sb_natal_pop_is_indian",
        )
        indian_origin_scope = object_block(
            "common/scripted_triggers/sb_natal_interwar_triggers.txt",
            "sb_natal_pop_is_indian_origin",
        )
        handler = object_block(
            "common/on_actions/sb_regional_on_action_handlers.txt",
            "sb_on_natal_indian_consolidation_yearly_pulse_country",
        )
        early = object_block(
            "common/amendments/sb_amendments.txt",
            "amendment_sb_natal_indian_indenture_status",
        )
        civic = object_block(
            "common/amendments/sb_amendments.txt",
            "amendment_sb_natal_indian_civic_rights",
        )
        event = object_block(
            "events/sb_natal_interwar_events.txt", "sb_natal_interwar.005"
        )
        housekeeping = object_block(
            effects_path, "sb_natal_interwar_monthly_housekeeping"
        )
        modifier_types = text(
            "common/modifier_type_definitions/sb_culture_generated_modifier_types.txt"
        )
        static_modifiers = text(
            "common/static_modifiers/sb_culture_generated_modifiers.txt"
        )

        self.assertIn("CULTURE = cu:gujarati", completion)
        self.assertIn("SIZE = 1500", completion)
        self.assertIn("DESTINATION_POP_TYPE = pop_type:shopkeepers", completion)
        self.assertIn("add_homeland = cu:natal_indian", completion)
        self.assertIn("target = cu:natal_indian", completion)
        self.assertIn("value = 0.25", completion)
        self.assertIn("add_primary_culture = cu:natal_indian", completion)
        self.assertIn("remove_primary_culture = cu:natal_indian", completion)
        self.assertLess(
            completion.index("add_primary_culture = cu:natal_indian"),
            completion.index("change_pop_culture ="),
        )
        self.assertLess(
            completion.index("change_pop_culture ="),
            completion.index("add_homeland = cu:natal_indian"),
        )
        self.assertLess(
            completion.index("change_pop_culture ="),
            completion.index(
                "set_variable = sb_natal_indian_ethnogenesis_conversion_applied_var"
            ),
        )
        self.assertLess(
            completion.index(
                "set_variable = sb_natal_indian_ethnogenesis_conversion_applied_var"
            ),
            completion.index("add_homeland = cu:natal_indian"),
        )
        self.assertLess(
            completion.index("add_homeland = cu:natal_indian"),
            completion.index("remove_primary_culture = cu:natal_indian"),
        )
        self.assertIn(
            "NOT = { has_variable = sb_natal_indian_community_established_var }",
            completion,
        )
        self.assertIn("any_scope_pop = { culture = cu:natal_indian }", completion)
        self.assertNotIn("random", completion)
        self.assertIn("set_global_variable = sb_natal_indian_ethnogenesis_completed_global_var", completion)
        self.assertIn("target = cu:natal_indian", consolidation)
        self.assertIn("value = 0.02", consolidation)
        self.assertNotIn("random", consolidation)
        self.assertIn("heritage = heritage_natal_indian", culture)
        self.assertIn("language = language_anglophone", culture)
        self.assertIn("graphics = south_asian", culture)
        self.assertIn("trait_group = heritage_group_south_asian", heritage)
        for modifier_type in (
            "state_natal_indian_standard_of_living_add",
            "country_natal_indian_cultural_acceptance_add",
            "country_fervor_target_natal_indian_add",
        ):
            self.assertIn(f"{modifier_type} = {{", modifier_types)
        for static_modifier in (
            "natal_indian_standard_of_living_modifier_positive",
            "natal_indian_standard_of_living_modifier_negative",
            "natal_indian_cultural_acceptance_modifier_positive",
            "natal_indian_cultural_acceptance_modifier_negative",
            "natal_indian_fervor_target_modifier_positive",
            "natal_indian_fervor_target_modifier_negative",
        ):
            self.assertIn(f"{static_modifier} = {{", static_modifiers)
        self.assertIn("culture = cu:natal_indian", indian_scope)
        self.assertIn("sb_natal_pop_is_indian_origin = yes", indian_scope)
        self.assertIn(
            "has_global_variable = sb_natal_indian_ethnogenesis_completed_global_var",
            indian_scope,
        )
        self.assertNotIn("culture = cu:natal_indian", indian_origin_scope)
        self.assertIn("sb_natal_pop_is_indian_origin = yes", consolidation)
        self.assertIn("has_global_variable = sb_natal_indian_ethnogenesis_completed_global_var", handler)
        self.assertIn("every_scope_state = {", handler)
        self.assertIn("state_region = s:STATE_NATAL", handler)
        self.assertIn("country_natal_indian_cultural_acceptance_add = 50", early)
        self.assertIn("country_natal_indian_cultural_acceptance_add = 60", civic)
        self.assertIn("sb_natal_establish_natal_indian_community = yes", event)
        self.assertIn(
            "has_global_variable = sb_natal_indian_ethnogenesis_completed_global_var",
            housekeeping,
        )
        self.assertIn(
            "NOT = { has_variable = sb_natal_indian_community_established_var }",
            housekeeping,
        )
        self.assertNotIn("is_homeland = cu:natal_indian", housekeeping)
        self.assertIn("sb_natal_establish_natal_indian_community = yes", housekeeping)
        self.assertIn(
            "has_variable = sb_natal_indian_community_established_var", handler
        )

        localization = text("localization/english/sb_natal_interwar_l_english.yml")
        self.assertIn("sb_natal_indian_homeland_tt:0", localization)
        self.assertIn("# ### TO REVIEW ###\n sb_natal_interwar.005.t:0", localization)

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
        frontier_creation = object_block(
            path, "sb_create_natalia_frontier_republic_if_missing"
        )
        self.assertIn("p:x5B124F.state", creation)
        self.assertIn("culture = cu:boer", creation)
        self.assertIn("population_ratio = 0.05", creation)
        self.assertLess(
            creation.index("move_partial_pop ="),
            creation.index("create_country ="),
        )
        self.assertIn("p:x552449.state", frontier_creation)
        self.assertIn("province = p:x552449", frontier_creation)
        self.assertLess(
            frontier_creation.index("move_partial_pop ="),
            frontier_creation.index("create_country ="),
        )
        self.assertNotIn("sb_transfer_ora_boer_founders_to_natalia", source)
        self.assertNotIn("sb_natalia_ora_boer_founders_transferred_var", source)

    def test_split_states_make_founder_relocation_pipeline_obsolete(self):
        path = "common/scripted_effects/sb_natalia_effects.txt"
        source = text(path)
        assignment = object_block(path, "sb_assign_natalia_republic_territory")
        frontier_assignment = object_block(
            path, "sb_assign_natalia_frontier_territory"
        )
        direct = object_block(path, "sb_found_natalia_after_blood_river")
        peaceful = object_block(path, "sb_found_natalia_peacefully")
        guns_bargain = object_block(
            path, "sb_found_natalia_after_guns_bargain_rejection"
        )
        self.assertIn("s:STATE_NATAL", assignment)
        self.assertEqual(NATALIA_CORE, validate.object_values(assignment, "provinces"))
        self.assertNotIn("STATE_ZULULAND", assignment)
        self.assertIn("country = c:NAL", frontier_assignment)
        self.assertIn("provinces = { x552449 xDE0EDE }", frontier_assignment)
        self.assertIn("country = c:NGI", frontier_assignment)
        self.assertNotIn("STATE_ZULULAND", frontier_assignment)
        self.assertNotIn("sb_relocate_inherited_natalia_buildings_to_zul", source)
        self.assertNotIn("sb_natalia_blood_river_building_transfer_pending_var", source)
        self.assertLess(
            direct.index("sb_assign_natalia_republic_territory = yes"),
            direct.index("sb_apply_natalia_boer_republic_setup = yes"),
        )
        self.assertLess(
            peaceful.index("sb_assign_natalia_frontier_territory = yes"),
            peaceful.index("sb_apply_natalia_boer_republic_setup = yes"),
        )
        self.assertNotIn("sb_assign_natalia_republic_territory = yes", peaceful)
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
        self.assertIn("save_scope_as = sb_natalia_commando_scope", military)
        self.assertIn(
            "transfer_to_formation = scope:sb_natalia_commando_scope", military
        )
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
        self.assertEqual(30, amendment.count("cultural_acceptance_add = 60"))
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
        self.assertEqual(2, event.count("sb_natal_create_zulu_national_movement = yes"))
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

    def test_zulu_restoration_uses_engine_secession_and_story_appeal_only(self):
        effects_path = "common/scripted_effects/sb_natal_interwar_effects.txt"
        effects = text(effects_path)
        restore = object_block(effects_path, "sb_natal_restore_zululand_as_puppet")
        finalize = object_block(
            effects_path, "sb_natal_finalize_restored_zululand_as_puppet"
        )
        movement = object_block(effects_path, "sb_natal_create_zulu_national_movement")
        agitator = object_block(
            effects_path, "sb_natal_ensure_zulu_restoration_agitator"
        )
        dinuzulu_cleanup = object_block_from_source(
            agitator, "every_scope_character"
        )
        handlers = text("common/on_actions/sb_natal_interwar_on_action_handlers.txt")
        appeal = object_block(
            "events/sb_natal_interwar_events.txt", "sb_natal_interwar.035"
        )
        plays = text("common/diplomatic_plays/sb_diplomatic_plays.txt")
        movements = text("common/political_movements/sb_natal_interwar_movements.txt")
        hooks = text("common/on_actions/sb_diplomatic_play_on_action_handlers.txt")
        self.assertIn("type = puppet", finalize)
        self.assertIn("add_liberty_desire = 75", finalize)
        self.assertIn("s:STATE_ZULULAND", finalize)
        self.assertIn("province = p:xBE6FEE", restore)
        for province in (
            "xBE6FEE", "x1A084B", "xBFA16B", "x9E9742", "x88FAD4",
            "x904EBE", "x41C070", "xE882CE", "xE1E455",
        ):
            self.assertIn(province, finalize)
        self.assertNotIn("STATE_NATAL", restore + finalize)
        self.assertNotIn("population_ratio", restore + finalize)
        self.assertNotIn("sb_natal_normalize_restored_zululand_population", effects)
        self.assertNotIn("sb_restore_zululand_population_split_after_zulu_defeat", effects)

        self.assertIn("type = movement_cultural_minority", movement)
        self.assertIn("culture = cu:zulu", movement)
        self.assertIn("ZUL_dinuzulu_heir", agitator)
        self.assertIn("ZUL_mbuyazi_heir", agitator)
        self.assertIn("sb_zulu_mbuyazi_succession_global_var", agitator)
        self.assertIn("has_role_of_type = agitator", dinuzulu_cleanup)
        self.assertNotIn("is_agitator = yes", dinuzulu_cleanup)
        self.assertIn("remove_character_role = agitator", agitator)
        self.assertIn("set_ideology = ideology:ideology_sovereignist_leader", agitator)
        self.assertIn("sb_on_natal_zulu_secession_start", handlers)
        self.assertIn("country_definition = cd:NAL", handlers)
        self.assertIn("sb_natal_is_british_colony = yes", handlers)
        self.assertIn("country_definition = cd:ZUL", handlers)
        self.assertIn("is_secessionist = yes", handlers)
        self.assertIn("set_variable = sb_natal_zulu_settlement_resolved_var", handlers)
        self.assertIn("remove_variable = sb_natal_zulu_settlement_pending_var", handlers)
        self.assertIn("id = sb_natal_interwar.035 days = 1 popup = yes", handlers)
        self.assertIn("sb_on_natal_zulu_secession_end", handlers)
        self.assertIn("sb_natal_zulu_restoration_resolved_var", handlers)
        self.assertIn("sb_natal_clear_zulu_restoration_runtime = yes", handlers)
        self.assertIn("id = sb_natal_interwar.040 days = 5 popup = yes", appeal)
        self.assertIn("sb_natal_interwar.035.a", appeal)
        self.assertIn("sb_natal_interwar.035.b", appeal)
        self.assertIn("base = 100", appeal)
        self.assertIn("base = 0", appeal)

        self.assertNotIn("movement_sb_zulu_restoration", movements)
        self.assertNotIn("dp_sb_zulu_restoration_secession", plays)
        self.assertNotIn("create_diplomatic_play", effects)
        for handler in (
            "sb_natal_handle_zulu_restoration_backdown",
            "sb_natal_handle_zulu_restoration_war_end",
            "sb_natal_handle_zulu_restoration_wargoal_enforced",
        ):
            self.assertNotIn(f"{handler} = yes", hooks)

    def test_restored_zululand_defers_country_tag_links_until_the_next_day(self):
        effects_path = "common/scripted_effects/sb_natal_interwar_effects.txt"
        restore = object_block(effects_path, "sb_natal_restore_zululand_as_puppet")
        finalize = object_block(
            effects_path, "sb_natal_finalize_restored_zululand_as_puppet"
        )
        followup = object_block(
            "events/sb_natal_interwar_events.txt", "sb_natal_interwar.031"
        )
        trigger = object_block_from_source(followup, "trigger")
        immediate = object_block_from_source(followup, "immediate")

        self.assertIn("sb_natal_restored_zululand_setup_pending_var", restore)
        self.assertIn("id = sb_natal_interwar.031 days = 1 popup = no", restore)
        self.assertNotIn("c:ZUL =", restore)
        self.assertNotIn("country = c:ZUL", restore)
        self.assertIn(
            "has_variable = sb_natal_restored_zululand_setup_pending_var", trigger
        )
        self.assertNotIn("c:ZUL", trigger)
        self.assertIn(
            "sb_natal_finalize_restored_zululand_as_puppet = yes", immediate
        )
        self.assertIn(
            "remove_variable = sb_natal_restored_zululand_setup_pending_var", finalize
        )
        self.assertIn("c:ZUL ?= { is_country_alive = yes }", finalize)
        self.assertIn("country = c:ZUL", finalize)
        self.assertIn("c:ZUL = { add_liberty_desire = 75 }", finalize)
        self.assertIn(
            "c:ZUL = { sb_natal_restore_archived_zulu_firearms = yes }", finalize
        )

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
        self.assertIn("is_secessionist = yes", trigger)
        self.assertIn("sb_natal_zulu_restoration_active_var", trigger)
        self.assertNotIn("article = goods_transfer", trigger)
        self.assertNotIn("inputs =", trigger)
        self.assertNotIn("is_direct_subject_of = c:NAL", event)
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
            "common/on_actions/sb_natal_interwar_on_action_handlers.txt",
            "common/buildings/sb_construction_sector_guard.txt",
            "events/sb_pink_map_events.txt",
            "common/history/ai/zz_sb_portuguese_kongo_secret_goal.txt",
        ):
            self.assertTrue((ROOT / path).read_bytes().startswith(b"\xef\xbb\xbf"), path)


if __name__ == "__main__":
    unittest.main()
