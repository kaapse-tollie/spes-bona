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


class FrontierTweaksTests(unittest.TestCase):
    def test_bst_starts_with_partial_firearms_progress(self):
        seed = object_block(
            "common/scripted_effects/sb_firearms_effects.txt",
            "sb_seed_initial_firearms_progress",
        )
        bst_seed = object_block_from_source(seed, "if")
        self.assertIn("country_definition = cd:BST", bst_seed)
        self.assertIn("name = sb_firearms_treaty_progress_months_var", bst_seed)
        self.assertIn("value = 9.6", bst_seed)
        self.assertNotIn("sb_firearms_industry_progress_months_var", bst_seed)

    def test_bst_starts_with_chiefly_levy_law(self):
        law = object_block(
            "common/laws/04_sb_chiefly_levy.txt", "law_sb_chiefly_levy"
        )
        history = text("common/history/countries/bst - basuto.txt")
        amendments = text("common/amendments/sb_amendments.txt")
        for token in (
            "parent = law_peasant_levies",
            "country_can_only_conscript_peasants_bool = yes",
            "state_conscription_rate_add = 0.60",
            "country_aristocrats_pol_str_mult = 0.10",
            "unit_morale_loss_mult = 0.1",
            "unit_experience_gain_mult = -0.25",
            "state_building_barrack_max_level_add = 5",
            "state_building_conscription_center_max_level_add = 25",
            "country_definition = cd:BST",
            "has_law = law_type:law_sb_chiefly_levy",
        ):
            self.assertIn(token, law)
        self.assertNotIn("building_training_rate", law)
        self.assertNotIn("country_military_goods_cost_mult", law)
        self.assertIn("activate_law = law_type:law_sb_chiefly_levy", history)
        self.assertNotIn("amendment_sb_chiefly_levy", history)
        self.assertNotIn("amendment_sb_chiefly_levy", amendments)

    def test_customary_muster_uses_low_officer_staffing_and_excludes_competitors(self):
        path = "common/production_methods/sb_customary_muster.txt"
        muster = object_block(path, "pm_sb_customary_muster_conscription")
        for token in (
            "soldiers = 99",
            "officers = 1",
            "law_sb_amabutho_system",
            "law_sb_chiefly_levy",
            "building_training_rate_add = 100",
            "building_training_rate_add = 20",
        ):
            self.assertIn(token, muster)

        for method in (
            "pm_no_organization_conscription",
            "pm_general_training_conscription",
            "pm_advanced_tactics_training_conscription",
            "pm_training_streamlining_conscription",
            "pm_nco_incorporation_conscription",
            "pm_mobile_warfare_tactics_conscription",
        ):
            injection = object_block(path, f"INJECT:{method}")
            self.assertIn("law_sb_amabutho_system", injection)
            self.assertIn("law_sb_chiefly_levy", injection)

        group = object_block(
            "common/production_method_groups/sb_customary_muster.txt",
            "INJECT:pmg_training_conscription",
        )
        self.assertIn("pm_sb_customary_muster_conscription", group)

    def test_frontier_floors_do_not_add_reconstitution_training(self):
        effects = object_block(
            "common/scripted_effects/sb_frontier_force_effects.txt",
            "sb_restore_ai_frontier_force_floor",
        )
        eligibility = object_block(
            "common/scripted_triggers/sb_game_rule_triggers.txt",
            "sb_frontier_ai_force_floor_eligible",
        )
        amabutho_law = object_block(
            "common/laws/03_sb_amabutho_system.txt", "law_sb_amabutho_system"
        )
        self.assertFalse(
            (ROOT / "common/static_modifiers/sb_conscription_modifiers.txt").exists()
        )
        self.assertNotIn("building_training_rate", effects)
        self.assertNotIn("sb_native_conscription_MTB", effects)
        self.assertNotIn("building_training_rate_mult", amabutho_law)
        self.assertIn("is_ai = yes", eligibility)
        self.assertIn("sb_frontier_artificial_assistance_enabled = yes", eligibility)
        self.assertIn("cd:XHO", eligibility)
        self.assertNotIn("cd:MTB", eligibility)

    def test_uthumbu_heir_assignment_matches_the_vanilla_lifecycle_order(self):
        path = "common/scripted_effects/sb_zulu_dynasty_succession_effects.txt"
        assign = object_block(path, "sb_zulu_assign_new_heir_scope")
        prepare = object_block(path, "sb_zulu_prepare_uthumbu_heir")
        secured = object_block(path, "sb_resolve_zulu_dynasty_secured")

        self.assertLess(
            assign.index("set_heir = scope:new_heir_scope"),
            assign.index("free_character_from_void = yes"),
        )
        self.assertNotIn("replace_character_roles", assign)
        self.assertIn("template = ZUL_uthumbu_claimed_son", prepare)
        self.assertIn("sb_zulu_assign_new_heir_scope = yes", prepare)
        self.assertIn("sb_zulu_prepare_uthumbu_heir = yes", secured)

    def test_potgieter_has_no_colonial_administrator_trait(self):
        history = text("common/history/characters/ora - oranje.txt")
        characters = [
            validate.extract_braced(history, match.start())
            for match in re.finditer(r"^\s*create_character\s*=\s*\{", history, re.MULTILINE)
        ]
        potgieter = next(
            candidate
            for candidate in characters
            if "template = ORA_hendrik_potgieter" in candidate
        )
        self.assertNotIn("add_trait = basic_colonial_administrator", potgieter)
        self.assertNotIn("add_trait = experienced_colonial_administrator", potgieter)
        self.assertNotIn("add_trait = expert_colonial_administrator", potgieter)

    def test_ndebele_vegkop_frontier_transfers_to_oranje(self):
        vrystaat = object_block(
            "common/history/states/00_states.txt", "s:STATE_VRYSTAAT"
        )
        oranje_start = vrystaat.index("country = c:ORA")
        ndebele_start = vrystaat.index("country = c:MTB")
        philippolis_start = vrystaat.index("country = c:PHL")
        oranje_fragment = vrystaat[oranje_start:ndebele_start]
        ndebele_fragment = vrystaat[ndebele_start:philippolis_start]
        vegkop = object_block("events/sb_great_trek_events.txt", "sb_great_trek.002")

        for province in ("x52B31E", "xF17D3D"):
            self.assertNotIn(province, oranje_fragment)
            self.assertIn(province, ndebele_fragment)
            self.assertIn(province, vegkop)

    def test_bst_starts_with_six_conscripts_and_one_standing_battalion(self):
        buildings = object_block(
            "common/history/buildings/04_subsaharan_africa.txt",
            "s:STATE_DRAKENSBERG",
        )
        bst_buildings = object_block_from_source(buildings, "region_state:BST")
        self.assertRegex(
            bst_buildings,
            r'(?s)building="building_barrack".*?country="c:BST".*?levels=1',
        )
        self.assertRegex(
            bst_buildings,
            r'(?s)building="building_conscription_center".*?country="c:BST".*?levels=6',
        )
        self.assertIn("pm_sb_customary_muster_conscription", bst_buildings)
        self.assertNotIn("pm_no_organization_conscription", bst_buildings)
        self.assertNotIn("levels=14", bst_buildings)

    def test_british_corridor_settlement_incorporates_cape_fragment(self):
        settlement = object_block(
            "common/scripted_effects/sb_bechuanaland_corridor_effects.txt",
            "sb_bechuanaland_apply_british_settlement",
        )
        self.assertIn("s:STATE_BECHUANALAND", settlement)
        self.assertIn("region_state:CAP ?=", settlement)
        self.assertIn("set_state_type = incorporated", settlement)

    def test_landed_tswana_uses_protectorate_status(self):
        path = "common/scripted_effects/sb_bechuanaland_corridor_effects.txt"
        for effect_name, overlord in (
            ("sb_bechuanaland_make_tsw_subject_of_gbr", "GBR"),
            ("sb_bechuanaland_make_tsw_subject_of_cap", "CAP"),
        ):
            effect = object_block(path, effect_name)
            self.assertIn(f"is_direct_subject_of = c:{overlord}", effect)
            self.assertIn("type = protectorate", effect)
            self.assertIn("subject_type_protectorate", effect)
            self.assertNotIn("type = puppet", effect)
            self.assertNotIn("subject_type_puppet", effect)

    def test_grondwet_retains_agrarianism_and_adopts_protectionism(self):
        event = object_block("events/sb_boer_republics_events.txt", "sb_boer_republics.130")
        option = object_block_from_source(event, "option")
        self.assertIn("activate_law = law_type:law_agrarianism", option)
        self.assertIn("activate_law = law_type:law_protectionism", option)
        self.assertNotIn("activate_law = law_type:law_interventionism", option)
        self.assertRegex(
            option,
            r"hidden_effect\s*=\s*\{\s*activate_law\s*=\s*law_type:law_agrarianism",
        )

    def test_grondwet_normalization_is_shared_after_ten_days(self):
        finalizer = object_block(
            "common/scripted_effects/sb_trek_migration.txt",
            "sb_great_trek_finalize_republic",
        )
        self.assertIn(
            "trigger_event = { id = sb_boer_republics.130 days = 10 popup = yes }",
            finalizer,
        )
        for tag in ("TRN", "ORA", "ZPB", "LYD", "NAL", "KLR", "SGO"):
            self.assertIn(f"country_definition = cd:{tag}", finalizer)

        event = object_block("events/sb_boer_republics_events.txt", "sb_boer_republics.130")
        for tag in ("TRN", "ORA", "ZPB", "LYD", "NAL", "SGO"):
            self.assertIn(f"country_definition = cd:{tag}", event)
        self.assertEqual(2, event.count("\n\toption = {"))
        self.assertEqual(2, event.count("set_variable = sb_great_trek_normalized_var"))

        sources = "\n".join(
            text(path)
            for path in (
                "common/scripted_effects/sb_trek_migration.txt",
                "common/on_actions/sb_boer_story_on_action_handlers.txt",
                "events/sb_great_trek_events.txt",
            )
        )
        self.assertNotIn("sb_great_trek.101", sources)

    def test_great_trek_stages_are_sequential_and_natal_is_the_nal_or_klr_target(self):
        journal = object_block(
            "common/journal_entries/1-02_sb_great_trek.txt", "je_sb_great_trek"
        )
        self.assertRegex(
            journal,
            r"STAGE 2:[\s\S]*?else_if\s*=\s*\{[\s\S]*?country_definition\s*=\s*cd:NAL"
            r"[\s\S]*?country_definition\s*=\s*cd:KLR"
            r"[\s\S]*?owns_entire_state_region\s*=\s*STATE_NATAL"
            r"[\s\S]*?id\s*=\s*sb_great_trek\.043",
        )
        self.assertNotIn("sb_controls_natalia_core", journal)
        self.assertIn(
            'sb_great_trek_stage2_completion_nal:0 "Natal"',
            text("localization/english/sb_l_english.yml"),
        )

    def test_natalia_uses_its_specific_stage_one_event_text(self):
        journal = object_block(
            "common/journal_entries/1-02_sb_great_trek.txt", "je_sb_great_trek"
        )
        event = object_block("events/sb_great_trek_events.txt", "sb_great_trek.032")
        localization = text("localization/english/sb_great_trek_l_english.yml")

        self.assertRegex(
            journal,
            r"STAGE 1:[\s\S]*?country_definition\s*=\s*cd:NAL"
            r"[\s\S]*?id\s*=\s*sb_great_trek\.032[\s\S]*?STAGE 2:",
        )
        for token in (
            "title = sb_great_trek.032.t",
            "desc = sb_great_trek.032.d",
            "flavor = sb_great_trek.032.f",
            "name = sb_great_trek.032.a",
            "sb_great_trek_stage_item_boer_slice_reward = yes",
        ):
            self.assertIn(token, event)
        for suffix in ("t", "d", "f", "a"):
            self.assertIn(f"sb_great_trek.032.{suffix}:0", localization)
        self.assertNotIn("sb_great_trek.033.", localization)

    def test_caledon_raid_only_blocks_shared_conflicts_and_truces(self):
        target = object_block(
            "common/scripted_triggers/sb_bst_triggers.txt",
            "sb_bst_oranje_frontier_actor_can_be_raided",
        )
        trigger = object_block(
            "common/scripted_triggers/sb_bst_triggers.txt", "sb_bst_frontier_raid_valid"
        )
        effect = object_block(
            "common/scripted_effects/sb_bst_effects.txt", "sb_bst_execute_oranje_raid"
        )
        event = object_block("events/sb_bst_frontier_events.txt", "sb_bst_frontier.010")
        for block in (target, trigger, effect, event):
            self.assertNotIn("is_at_war = no", block)
            self.assertNotIn("is_active_in_diplomatic_play = no", block)
        self.assertIn("NOT = { has_truce_with = c:BST }", target)
        self.assertIn("NOT = { has_war_with = c:BST }", target)
        self.assertIn("NOT = { is_diplomatic_play_participant_with = c:BST }", target)
        self.assertNotIn("= root", target)
        self.assertIn("country_definition = cd:BST", trigger)
        self.assertIn("sb_bst_oranje_frontier_actor_can_be_raided = yes", trigger)
        self.assertIn("sb_bst_frontier_raid_valid = yes", effect)
        self.assertIn("sb_bst_oranje_frontier_actor_can_be_raided = yes", effect)
        self.assertIn("sb_bst_oranje_frontier_actor_can_be_raided = yes", event)
        self.assertRegex(
            effect,
            r"sb_bst_execute_oranje_raid\s*=\s*\{\s*if\s*=\s*\{\s*limit\s*=\s*\{\s*sb_bst_frontier_raid_valid\s*=\s*yes",
        )

    def test_caledon_frontier_resolves_when_opposing_land_is_gone(self):
        journal = object_block(
            "common/journal_entries/1-07_sb_bst_frontier.txt",
            "je_sb_bst_ora_frontier",
        )
        complete = object_block_from_source(journal, "complete")
        on_complete = object_block_from_source(journal, "on_complete")
        fail = object_block_from_source(journal, "fail")
        on_fail = object_block_from_source(journal, "on_fail")
        triggers = text("common/scripted_triggers/sb_bst_triggers.txt")
        events = text("events/sb_bst_frontier_events.txt")
        oranje_result = object_block_from_source(events, "sb_bst_frontier.300")
        basotho_result = object_block_from_source(events, "sb_bst_frontier.310")

        self.assertIn("sb_bst_any_oranje_frontier_land_holder_exists = yes", complete)
        self.assertIn("c:BST ?=", complete)
        self.assertIn("sb_bst_holds_frontier_land = yes", complete)
        self.assertNotIn("owns_entire_state_region", complete)
        self.assertIn("sb_bst_oranje_frontier_land_holder = yes", on_complete)
        self.assertNotIn("owns_entire_state_region", on_complete)
        self.assertIn(
            "trigger_event = { id = sb_bst_frontier.300 days = 1 popup = yes }",
            on_complete,
        )
        self.assertLess(
            on_complete.index("set_variable = sb_ora_annexed_bst_var"),
            on_complete.index("trigger_event = { id = sb_bst_frontier.300"),
        )

        self.assertIn("sb_bst_holds_frontier_land = yes", fail)
        self.assertIn(
            "NOT = { sb_bst_any_oranje_frontier_land_holder_exists = yes }", fail
        )
        self.assertIn("trigger_event = { id = sb_bst_frontier.310", on_fail)
        self.assertIn("sb_bst_oranje_frontier_land_holder = {", triggers)
        self.assertIn("state_region = s:STATE_VRYSTAAT", triggers)
        self.assertIn("state_region = s:STATE_DRAKENSBERG", triggers)
        oranje_trigger = object_block_from_source(oranje_result, "trigger")
        self.assertNotIn("sb_bst_oranje_frontier_land_holder", oranje_trigger)
        self.assertIn("has_variable = sb_ora_annexed_bst_var", oranje_trigger)
        self.assertNotIn("owns_entire_state_region", basotho_result)

    def test_ovambo_fragment_and_lourenco_region_are_restored(self):
        pops = object_block(
            "common/history/pops/04_subsaharan_africa.txt", "s:STATE_SOUTH_ANGOLA"
        )
        states = object_block(
            "common/history/states/00_states.txt", "s:STATE_SOUTH_ANGOLA"
        )
        southern = object_block(
            "common/strategic_regions/sb_african_strategic_regions.txt",
            "REPLACE:region_southern_africa",
        )
        eastern = object_block(
            "common/strategic_regions/sb_african_strategic_regions.txt",
            "REPLACE:region_east_africa",
        )
        ovb = object_block_from_source(pops, "region_state:OVB")
        self.assertIn("culture = ovambo", ovb)
        self.assertIn("size = 28100", ovb)
        self.assertIn("add_homeland = cu:ovambo", states)
        self.assertNotIn("STATE_LOURENCO_MARQUES", southern)
        self.assertIn("STATE_LOURENCO_MARQUES", eastern)
        formations = text(
            "common/history/military_formations/07_military_formations_subsaharan_africa.txt"
        )
        gaza = object_block_from_source(formations, "c:GZA ?")
        self.assertIn("hq_region = sr:region_east_africa", gaza)
        self.assertNotIn("hq_region = sr:region_southern_africa", gaza)

    def test_zoutpansberg_targets_every_transvaal_state_and_inherits_tag(self):
        path = "common/scripted_effects/sb_treaty_effects.txt"
        launch = object_block(path, "sb_open_trn_zpb_crackdown_play")
        succession = object_block(path, "sb_zpb_assume_transvaal_after_crackdown_victory")
        war_end = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_war_end",
        )
        self.assertIn("c:TRN ?= {\n\t\t\tevery_scope_state", launch)
        self.assertIn("holder = c:ZPB", launch)
        self.assertIn("type = conquer_state", launch)
        self.assertIn("target_state = prev", launch)
        self.assertIn("primary_demand = yes", launch)
        self.assertIn("NOT = { exists = c:TRN }", succession)
        self.assertIn("activate_law = law_type:law_discrete_inboekstelsel", succession)
        self.assertIn("sb_add_expanded_inboekstelsel_amendment = yes", succession)
        self.assertIn("change_tag = TRN", succession)
        self.assertIn("sb_zpb_assume_transvaal_after_crackdown_victory = yes", war_end)
        self.assertIn("set_variable = sb_zpb_crackdown_successor_pending_var", war_end)

        backdown = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_diplo_play_back_down",
        )
        monthly = object_block(
            "common/on_actions/sb_boer_story_on_action_handlers.txt",
            "sb_on_zpb_monthly_pulse_country",
        )
        self.assertIn("sb_zpb_crackdown_successor_pending_var", backdown)
        self.assertIn("country_definition = cd:ZPB", monthly)
        self.assertIn("sb_zpb_assume_transvaal_after_crackdown_victory = yes", monthly)

    def test_walvis_bay_receives_prime_land_and_extra_arable(self):
        namaqualand = object_block(
            "map_data/state_regions/04_subsaharan_africa.txt",
            "STATE_NAMAQUALAND",
        )
        prime_land = re.search(r"prime_land\s*=\s*\{([^}]*)\}", namaqualand)
        self.assertIsNotNone(prime_land)
        self.assertIn('"x8031D0"', prime_land.group(1))
        self.assertIn("arable_land = 4", namaqualand)

    def test_maseko_starts_with_ngoni_not_shangaan_population(self):
        zambezia = object_block(
            "common/history/pops/04_subsaharan_africa.txt",
            "s:STATE_ZAMBEZIA",
        )
        maseko = object_block_from_source(zambezia, "region_state:MSK")
        self.assertIn("culture = nguni", maseko)
        self.assertIn("culture = chewa", maseko)
        self.assertNotIn("culture = shangaan", maseko)

    def test_vanilla_nguni_key_is_presented_as_distinct_ngoni_culture(self):
        ngoni = object_block(
            "common/cultures/sb_culture_overrides.txt", "REPLACE:nguni"
        )
        for token in (
            "heritage = heritage_southern_bantu",
            "language = language_nguni",
            "Mputa",
            "Zwangendaba",
            "Maseko",
            "Jere",
        ):
            self.assertIn(token, ngoni)

        localization = text("localization/english/sb_cultures_l_english.yml")
        self.assertIn('nguni:0 "Ngoni"', localization)
        self.assertNotIn('nguni:0 "Nguni"', localization)

        states = text("common/history/states/00_states.txt")
        zambezia = object_block_from_source(states, "s:STATE_ZAMBEZIA")
        self.assertNotIn("add_homeland = cu:nguni", zambezia)

    def test_commandant_general_law_uses_opt_in_interest_group_commands(self):
        law = object_block(
            "common/laws/00_sb_governance_principles.txt",
            "law_sb_commandant_general_republic",
        )
        interaction = object_block(
            "common/character_interactions/sb_commandant_general_interactions.txt",
            "sb_grant_command_to_interest_group_leader",
        )
        effects = text("common/scripted_effects/sb_boer_commandant_effects.txt")
        on_actions = text("common/on_actions/sb_boer_commandant_on_actions.txt")

        self.assertNotIn("sb_ensure_commandant_general_interest_group_commands", law)
        self.assertNotIn("sb_ensure_commandant_general_interest_group_commands", effects)
        self.assertNotIn("on_new_interest_group_leader", on_actions)
        self.assertIn("is_interest_group_leader = yes", interaction)
        self.assertIn("has_law = law_type:law_sb_commandant_general_republic", interaction)
        self.assertIn("add_character_role = general", interaction)
        self.assertIn("value = 0", interaction)


def object_block_from_source(source: str, name: str) -> str:
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} block")
    return validate.extract_braced(source, match.start())


if __name__ == "__main__":
    unittest.main()
