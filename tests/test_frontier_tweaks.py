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

    def test_caledon_raid_requires_both_sides_to_be_at_peace(self):
        trigger = object_block(
            "common/scripted_triggers/sb_bst_triggers.txt", "sb_bst_frontier_raid_valid"
        )
        effect = object_block(
            "common/scripted_effects/sb_bst_effects.txt", "sb_bst_execute_oranje_raid"
        )
        for block in (trigger, effect):
            self.assertGreaterEqual(block.count("is_at_war = no"), 2)
            self.assertGreaterEqual(block.count("is_active_in_diplomatic_play = no"), 2)
            self.assertIn("NOT = { has_truce_with = root }", block)

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
        self.assertIn("arable_land = 5", namaqualand)


def object_block_from_source(source: str, name: str) -> str:
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} block")
    return validate.extract_braced(source, match.start())


if __name__ == "__main__":
    unittest.main()
