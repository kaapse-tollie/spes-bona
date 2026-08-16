from pathlib import Path
import hashlib
import json
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


class RhodesianVentureTests(unittest.TestCase):
    def test_de_beers_bonuses_and_rhodes_home_region(self):
        company = object_block("common/company_types/zz_sb_de_beers_override.txt", "company_de_beers")
        prosperity = validate.extract_braced(company, company.index("prosperity_modifier = {"))
        self.assertIn("country_company_throughput_bonus_add = 0.05", prosperity)
        self.assertIn("building_group_bg_mining_throughput_add = 0.10", prosperity)
        self.assertNotIn("country_prestige_mult", prosperity)
        rhodes = object_block(
            "common/character_templates/sb_southern_africa_character_template_overrides.txt",
            "SAF_cecil_rhodes",
        )
        self.assertIn("home_region = STATE_CAPE_COLONY", rhodes)
        self.assertIn("culture = cu:anglo_african", rhodes)
        self.assertNotIn("ig_leader = yes", rhodes)
        self.assertNotIn("noble = yes", rhodes)
        self.assertIn("earliest_usage_date = 1870.1.1", rhodes)
        traits = validate.extract_braced(rhodes, rhodes.index("traits = {"))
        for trait in (
            "ambitious",
            "bigoted",
            "ruthless",
            "experienced_entrepreneur",
            "basic_political_operator",
        ):
            self.assertIn(trait, traits)
        self.assertNotIn("literary", traits)
        self.assertNotIn("experienced_colonial_administrator", traits)

    def test_decision_is_visible_and_independent_of_de_beers_and_rhodes(self):
        decision = object_block(
            "common/decisions/sb_rhodesian_venture_decisions.txt",
            "decision_sb_back_rhodesian_venture",
        )
        trigger = object_block(
            "common/scripted_triggers/sb_rhodesian_venture_triggers.txt",
            "sb_can_back_rhodesian_venture",
        )
        self.assertIn("is_shown = { country_definition = cd:GBR }", decision)
        for token in ("company_de_beers", "SAF_cecil_rhodes", "game_date"):
            self.assertNotIn(token, decision)
            self.assertNotIn(token, trigger)
        for token in (
            "sb_bechuanaland_terminal_outcome_british_global_var",
            "is_country_type = recognized",
            "is_subject = no",
            "has_technology_researched = malaria_prevention",
            "in_default = no",
            "is_at_war = no",
            "is_diplomatic_play_committed_participant = no",
            "sb_rhodesian_venture_has_colonial_law = yes",
            "sb_rhodesian_venture_has_available_commander = yes",
            "sb_rhodesian_venture_has_eligible_seed = yes",
            "sb_rhodesian_venture_retry_cooldown_var",
        ):
            self.assertIn(token, trigger)

    def test_progress_peril_and_incident_rate_match_specification(self):
        bars = text("common/scripted_progress_bars/sb_rhodesian_venture_progress_bars.txt")
        progress = object_block(
            "common/scripted_progress_bars/sb_rhodesian_venture_progress_bars.txt",
            "sb_rhodesian_venture_progress_bar",
        )
        peril = object_block(
            "common/scripted_progress_bars/sb_rhodesian_venture_progress_bars.txt",
            "sb_rhodesian_venture_peril_bar",
        )
        journal = object_block(
            "common/journal_entries/1-12_sb_rhodesian_venture.txt",
            "je_sb_rhodesian_venture",
        )
        self.assertIn("value = 1", progress)
        self.assertIn("max_value = 18", progress)
        self.assertIn("max_value = 5", peril)
        self.assertIn("chance_to_happen = 20", journal)
        self.assertEqual(6, len(re.findall(r"10 = sb_rhodesian_venture\.02[0-5]", journal)))
        self.assertIn('"scripted_bar_progress(sb_rhodesian_venture_progress_bar)" >= 18', journal)
        self.assertIn('"scripted_bar_progress(sb_rhodesian_venture_peril_bar)" >= 5', journal)
        self.assertIn("days = 1095", text("events/sb_rhodesian_venture_events.txt"))
        self.assertNotIn("max_value = 30", bars)

    def test_failure_conditions_do_not_depend_on_rhodes(self):
        journal = object_block(
            "common/journal_entries/1-12_sb_rhodesian_venture.txt",
            "je_sb_rhodesian_venture",
        )
        invalid = validate.extract_braced(journal, journal.index("invalid = {"))
        for token in (
            "in_default = yes",
            "is_subject = yes",
            "sb_rhodesian_venture_has_colonial_law",
            "sb_rhodesian_venture_has_eligible_seed",
        ):
            self.assertIn(token, invalid)
        self.assertNotIn("SAF_cecil_rhodes", invalid)

    def test_rhodes_lifecycle_prevents_duplicates_and_resurrection(self):
        effects = text("common/scripted_effects/sb_rhodesian_venture_effects.txt")
        scheduler = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_de_beers_schedule_or_assign_cecil_rhodes",
        )
        appointment = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_de_beers_complete_cecil_rhodes_appointment",
        )
        assignment = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_de_beers_assign_cecil_rhodes_to_saved_company",
        )
        executive_setup = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_de_beers_make_cecil_rhodes_executive",
        )
        monthly_repair = object_block(
            "common/on_actions/sb_rhodesian_venture_on_action_handlers.txt",
            "sb_on_de_beers_rhodes_monthly_pulse_country",
        )
        self.assertIn("sb_cecil_rhodes_ever_created_global_var", effects)
        self.assertIn("is_template_used = SAF_cecil_rhodes", effects)
        self.assertIn("sb_de_beers_rhodes_appointment_pending_var", effects)
        self.assertNotIn("set_character_as_executive", scheduler)
        self.assertIn("company:company_de_beers", appointment)
        self.assertIn("add_character_role = character_role_executive", executive_setup)
        self.assertIn("set_is_noble = no", executive_setup)
        self.assertIn("remove_character_role = character_role_ig_leader", executive_setup)
        self.assertIn("remove_character_role = character_role_politician", executive_setup)
        self.assertIn("role = character_role_executive", assignment)
        self.assertIn("sb_de_beers_new_rhodes_executive_var", assignment)
        self.assertIn("save_scope_as = sb_de_beers_rhodes_scope", assignment)
        self.assertIn("sb_de_beers_make_cecil_rhodes_executive = yes", assignment)
        self.assertNotIn("on_created = { save_scope_as = sb_de_beers_rhodes_scope }", assignment)
        self.assertIn("executive = scope:sb_de_beers_rhodes_scope", assignment)
        self.assertEqual(
            3,
            assignment.count("remove_variable = sb_de_beers_rhodes_appointment_pending_var"),
        )
        self.assertIn("game_date >= 1870.1.1", monthly_repair)
        self.assertIn("has_company = company_type:company_de_beers", monthly_repair)
        self.assertIn("any_scope_character = {", monthly_repair)
        self.assertIn("company:company_sb_british_south_africa_company ?=", monthly_repair)
        self.assertIn("set_character_as_executive = scope:sb_de_beers_company_scope", effects)
        self.assertIn("set_character_as_executive = scope:sb_bsac_company_scope", effects)
        self.assertIn("role = character_role_executive", effects)
        self.assertIn("sb_rhodes_de_beers_company_scope", effects)
        self.assertIn("sb_existing_rhodes_de_beers_owner_scope", effects)
        self.assertIn("sb_rhodesian_venture_protected_rhodes_var", effects)

    def test_prosperous_de_beers_moves_rhodes_into_politics_once(self):
        handler = object_block(
            "common/on_actions/sb_rhodesian_venture_on_action_handlers.txt",
            "sb_on_de_beers_prosperous_under_rhodes_monthly_pulse_country",
        )
        event = object_block(
            "events/sb_rhodesian_venture_events.txt",
            "sb_rhodesian_venture.030",
        )
        transition = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_de_beers_transition_cecil_rhodes_to_politics",
        )
        modifier = object_block(
            "common/static_modifiers/sb_rhodesian_venture_modifiers.txt",
            "sb_rhodes_diamond_magnate",
        )
        self.assertIn("company_is_prosperous = yes", handler)
        self.assertIn("executive = {", handler)
        self.assertIn("has_template = SAF_cecil_rhodes", handler)
        self.assertIn("sb_de_beers_rhodes_political_transition_pending_var", handler)
        self.assertIn("id = sb_rhodesian_venture.030", handler)
        self.assertIn("save_scope_as = sb_de_beers_company_scope", event)
        self.assertIn("save_scope_as = sb_de_beers_rhodes_scope", event)
        self.assertIn("sb_de_beers_transition_cecil_rhodes_to_politics = yes", event)
        self.assertIn("sb_de_beers_political_replacement_executive_var", transition)
        self.assertIn("set_character_as_executive = scope:sb_de_beers_company_scope", transition)
        self.assertIn("remove_character_role = character_role_executive", transition)
        self.assertIn("add_character_role = character_role_politician", transition)
        self.assertIn("add_trait = experienced_political_operator", transition)
        self.assertIn("remove_trait = basic_political_operator", transition)
        self.assertIn("add_trait = expert_entrepreneur", transition)
        self.assertIn("remove_trait = experienced_entrepreneur", transition)
        self.assertIn("set_as_interest_group_leader = yes", transition)
        self.assertIn("name = sb_rhodes_diamond_magnate", transition)
        self.assertIn("months = 120", transition)
        self.assertIn("sb_cecil_rhodes_entered_politics_global_var", transition)
        self.assertIn("character_popularity_add = 25", modifier)

    def test_bsac_company_and_charter_package(self):
        company = object_block(
            "common/company_types/sb_british_south_africa_company.txt",
            "company_sb_british_south_africa_company",
        )
        country = object_block("common/country_definitions/sb_countries.txt", "BSA")
        self.assertIn("cultures = { anglo_african }", country)
        self.assertNotIn("cultures = { british }", country)
        for token in (
            "category = bureaucrat_owned",
            "STATE_HOME_COUNTIES",
            'icon = "gfx/icons/company_icons/historical_company_icons/sb_CoA_BSAC.dds"',
            "building_railway_throughput_add = 0.10",
            "state_colony_growth_speed_mult = 0.10",
            "potential = { always = no }",
        ):
            self.assertIn(token, company)
        core = validate.extract_braced(company, company.index("building_types = {"))
        extensions = validate.extract_braced(
            company, company.index("extension_building_types = {")
        )
        self.assertEqual(
            {"building_railway", "building_gold_mine", "building_logging_camp"},
            set(re.findall(r"^\s+(building_[a-z_]+)\s*$", core, re.MULTILINE)),
        )
        self.assertEqual(
            {
                "building_rubber_plantation",
                "building_banana_plantation",
            },
            set(re.findall(r"^\s+(building_[a-z_]+)\s*$", extensions, re.MULTILINE)),
        )

        finalizer = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_rhodesian_venture_finalize_success",
        )
        package = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_rhodesian_venture_apply_chartered_company_package",
        )
        charter_finalizer = object_block(
            "events/sb_rhodesian_venture_events.txt",
            "sb_rhodesian_venture.012",
        )
        company_setup = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_rhodesian_venture_finalize_bsac_company_setup",
        )
        executive_install = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_rhodesian_venture_install_bsac_executive",
        )
        for token in (
            "province = p:x2A4E0D",
            "on_created = {",
            "building = building_government_administration",
            "building = building_barrack",
        ):
            self.assertIn(token, finalizer)
        self.assertRegex(
            finalizer,
            r"building\s*=\s*building_government_administration\s+level\s*=\s*2",
        )
        self.assertIn("id = sb_rhodesian_venture.012 days = 1", finalizer)
        self.assertIn(
            "sb_rhodesian_venture_move_pioneer_column_settlers = yes",
            charter_finalizer,
        )
        self.assertIn(
            "add_company = company_type:company_sb_british_south_africa_company",
            charter_finalizer,
        )
        self.assertIn(
            "sb_rhodesian_venture_finalize_bsac_company_setup = yes",
            charter_finalizer,
        )
        self.assertIn("type = chartered_company", charter_finalizer)
        self.assertNotIn("company:company_sb_british_south_africa_company", finalizer)
        self.assertIn("company:company_sb_british_south_africa_company", company_setup)
        self.assertIn("set_company_state_region = s:STATE_HOME_COUNTIES", company_setup)
        self.assertIn("add_owned_country = c:BSA", company_setup)
        self.assertIn("sb_bsac_starting_asset_created_var", company_setup)
        self.assertIn("building = building_logging_camp", company_setup)
        self.assertIn("type = company_sb_british_south_africa_company", company_setup)
        self.assertIn("country = c:GBR", company_setup)
        self.assertIn("levels = 1", company_setup)
        self.assertIn("sb_rhodesian_venture_install_bsac_executive = yes", company_setup)
        rhodes_preparation = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_rhodesian_venture_prepare_rhodes_for_bsac",
        )
        self.assertIn("remove_character_role = character_role_ig_leader", rhodes_preparation)
        self.assertIn("remove_character_role = character_role_politician", rhodes_preparation)
        self.assertIn("remove_character_role = character_role_ruler", rhodes_preparation)
        self.assertIn("on_remove_ruler_effects = yes", rhodes_preparation)
        self.assertIn("add_character_role = character_role_executive", rhodes_preparation)
        self.assertIn("set_is_noble = no", rhodes_preparation)
        self.assertIn("add_trait = expert_colonial_administrator", rhodes_preparation)

        settler_move = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_rhodesian_venture_move_pioneer_column_settlers",
        )
        for token in (
            "sb_bsac_pioneer_column_settlers_moved_var",
            "s:STATE_CAPE_COLONY",
            "region_state:CAP",
            "culture = cu:anglo_african",
            "total_size >= 380",
            "state = s:STATE_ZAMBEZI.region_state:BSA",
            "add = 80",
            "change_poptype = pop_type:bureaucrats",
            "add = 60",
            "change_poptype = pop_type:clerks",
            "add = 240",
        ):
            self.assertIn(token, settler_move)
        replacement_assignment = executive_install.find(
            "set_character_as_executive = scope:sb_rhodes_de_beers_company_scope"
        )
        detach = executive_install.find(
            "remove_character_role = character_role_executive", replacement_assignment
        )
        transfer = executive_install.find("transfer_character = c:GBR", detach)
        prepare = executive_install.find(
            "sb_rhodesian_venture_prepare_rhodes_for_bsac = yes", transfer
        )
        bsac_assignment = executive_install.find(
            "set_character_as_executive = scope:sb_bsac_company_scope", prepare
        )
        clear_nobility = executive_install.find("set_is_noble = no", bsac_assignment)
        self.assertTrue(
            replacement_assignment < detach < transfer < prepare < bsac_assignment < clear_nobility
        )

        bsa_coa = object_block("common/coat_of_arms/coat_of_arms/sb_countries.txt", "BSA")
        bsa_flag = object_block("common/flag_definitions/sb_flag_definitions.txt", "BSA")
        self.assertIn(
            'texture = "te_bsa_british_south_africa_company_flag.tga"', bsa_coa
        )
        self.assertNotIn("allow_overlord_canton", bsa_flag)
        self.assertNotIn("subject_canton", bsa_flag)
        self.assertIn("priority = 1100", bsa_flag)
        self.assertTrue(
            (ROOT / "gfx/icons/company_icons/historical_company_icons/sb_CoA_BSAC.dds").is_file()
        )
        self.assertTrue(
            (
                ROOT
                / "gfx/coat_of_arms/textured_emblems/te_bsa_british_south_africa_company_flag.tga"
            ).is_file()
        )
        for token in (
            "set_country_type = company",
            "ai_strategy_colonial_extraction",
            "amendment_racialized_subjecthood",
            "resource_extraction_charter_modifier",
            "ideology_colonialist",
        ):
            self.assertIn(token, package)

    def test_footprint_manifest_matches_script_and_is_connected(self):
        manifest_path = ROOT / "tools/rhodesian_venture_footprint.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        provinces = {
            province
            for state_provinces in manifest["states"].values()
            for province in state_provinces
        }
        self.assertEqual(15, len(provinces))
        self.assertEqual({"STATE_ZAMBEZI"}, set(manifest["states"]))
        self.assertEqual("x2A4E0D", manifest["seed"])
        self.assertNotIn("x8F0060", provinces)
        self.assertEqual(provinces, set(manifest["adjacency"]))
        self.assertEqual(1, len(validate.connected_components(provinces, manifest["adjacency"])))

        state_blocks = validate.parse_state_blocks(
            ROOT / "map_data/state_regions/04_subsaharan_africa.txt"
        )
        for state, expected in manifest["states"].items():
            actual = validate.object_values(state_blocks[state], "provinces")
            self.assertTrue(set(expected) <= actual)

        transfer = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_rhodesian_venture_transfer_eligible_footprint",
        )
        scripted = set(re.findall(r"provinces\s*=\s*\{\s*(x[0-9A-F]{6})\s*\}", transfer))
        self.assertEqual(provinces, scripted)
        self.assertEqual(15, transfer.count("sb_rhodesian_venture_seed_owner_is_eligible = yes"))

        province_map = ROOT / "map_data/provinces.png"
        digest = hashlib.sha256(province_map.read_bytes()).hexdigest()
        self.assertEqual(manifest["province_map_sha256"], digest)

    def test_ownership_filter_and_claim_transfer_are_narrow(self):
        trigger = object_block(
            "common/scripted_triggers/sb_rhodesian_venture_triggers.txt",
            "sb_rhodesian_venture_seed_owner_is_eligible",
        )
        for token in (
            "this = root",
            "top_overlord = root",
            "is_country_type = decentralized",
            "is_subject = no",
            "is_country_type = unrecognized",
            "heritage_group_african",
        ):
            self.assertIn(token, trigger)
        claims = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_rhodesian_venture_move_british_claims_to_bsa",
        )
        self.assertIn("has_claim = s:STATE_ZAMBEZI", claims)
        self.assertIn("s:STATE_ZAMBEZI =", claims)
        self.assertNotIn("STATE_ZAMBIA", claims)
        self.assertNotIn("STATE_KAZEMBE", claims)
        self.assertEqual(1, claims.count("remove_claim = root"))
        self.assertEqual(1, claims.count("add_claim = c:BSA"))

    def test_slot_and_disband_cleanup_are_registered(self):
        router = text("common/on_actions/sb_on_actions.txt")
        handlers = text("common/on_actions/sb_rhodesian_venture_on_action_handlers.txt")
        effects = text("common/scripted_effects/sb_rhodesian_venture_effects.txt")
        self.assertIn("on_company_established =", router)
        self.assertIn("sb_on_de_beers_company_established", router)
        self.assertNotIn("sb_on_british_south_africa_company_established", router)
        self.assertIn("sb_on_de_beers_rhodes_monthly_pulse_country", router)
        self.assertIn("sb_on_de_beers_prosperous_under_rhodes_monthly_pulse_country", router)
        self.assertIn("sb_on_british_south_africa_company_disbanded", router)
        self.assertIn("sb_on_rhodesian_venture_monthly_pulse_country", router)
        self.assertIn("company_de_beers", handlers)
        self.assertIn("company_sb_british_south_africa_company", handlers)
        monthly_repair = object_block(
            "common/on_actions/sb_rhodesian_venture_on_action_handlers.txt",
            "sb_on_rhodesian_venture_monthly_pulse_country",
        )
        self.assertIn("sb_bsac_starting_asset_created_var", monthly_repair)
        self.assertIn("sb_rhodesian_venture_finalize_bsac_company_setup = yes", monthly_repair)
        self.assertIn("remove_owned_country = c:BSA", effects)
        self.assertIn("type = colony", effects)
        self.assertIn("sb_british_south_africa_company_charter_slot", effects)


if __name__ == "__main__":
    unittest.main()
