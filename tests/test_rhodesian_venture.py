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
        self.assertIn("sb_cecil_rhodes_ever_created_global_var", effects)
        self.assertIn("is_template_used = SAF_cecil_rhodes", effects)
        self.assertIn("set_character_as_executive = scope:sb_de_beers_company_scope", effects)
        self.assertIn("set_character_as_executive = scope:sb_bsac_company_scope", effects)
        self.assertIn("role = character_role_executive", effects)
        self.assertIn("sb_rhodes_de_beers_company_scope", effects)
        self.assertIn("sb_existing_rhodes_de_beers_owner_scope", effects)
        self.assertIn("sb_rhodesian_venture_protected_rhodes_var", effects)

    def test_bsac_company_and_charter_package(self):
        company = object_block(
            "common/company_types/sb_british_south_africa_company.txt",
            "company_sb_british_south_africa_company",
        )
        for token in (
            "category = bureaucrat_owned",
            "STATE_HOME_COUNTIES",
            "building_railway",
            "building_gold_mine",
            "building_maize_farm",
            "building_livestock_ranch",
            "building_logging_camp",
            "building_railway_throughput_add = 0.10",
            "state_colony_growth_speed_mult = 0.10",
            "potential = { always = no }",
        ):
            self.assertIn(token, company)

        finalizer = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_rhodesian_venture_finalize_success",
        )
        package = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_rhodesian_venture_apply_chartered_company_package",
        )
        for token in (
            "province = p:x2A4E0D",
            "set_company_state_region = s:STATE_HOME_COUNTIES",
            "add_owned_country = c:BSA",
            "type = chartered_company",
            "building = building_government_administration",
            "building = building_barracks",
        ):
            self.assertIn(token, finalizer)
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
        self.assertEqual(27, len(provinces))
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
        self.assertEqual(27, transfer.count("sb_rhodesian_venture_seed_owner_is_eligible = yes"))

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
        for state in ("STATE_ZAMBEZI", "STATE_ZAMBIA", "STATE_KAZEMBE"):
            self.assertIn(f"has_claim = s:{state}", claims)
            self.assertIn(f"s:{state} =", claims)
        self.assertEqual(3, claims.count("remove_claim = root"))
        self.assertEqual(3, claims.count("add_claim = c:BSA"))

    def test_slot_and_disband_cleanup_are_registered(self):
        router = text("common/on_actions/sb_on_actions.txt")
        handlers = text("common/on_actions/sb_rhodesian_venture_on_action_handlers.txt")
        effects = text("common/scripted_effects/sb_rhodesian_venture_effects.txt")
        self.assertIn("on_company_established =", router)
        self.assertIn("sb_on_de_beers_company_established", router)
        self.assertIn("sb_on_british_south_africa_company_disbanded", router)
        self.assertIn("sb_on_rhodesian_venture_monthly_pulse_country", router)
        self.assertIn("company_de_beers", handlers)
        self.assertIn("company_sb_british_south_africa_company", handlers)
        self.assertIn("remove_owned_country = c:BSA", effects)
        self.assertIn("type = colony", effects)
        self.assertIn("sb_british_south_africa_company_charter_slot", effects)


if __name__ == "__main__":
    unittest.main()
