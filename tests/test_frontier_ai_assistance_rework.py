from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]
ZULULAND_PROVINCES = {
    "xBE6FEE", "x1A084B", "xBFA16B", "x9E9742", "x88FAD4",
    "x904EBE", "x41C070", "xE882CE", "xE1E455",
}


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def block_from_source(source: str, name: str, context: str = "source") -> str:
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} in {context}")
    return validate.extract_braced(source, match.start())


def block(path: str, name: str) -> str:
    return block_from_source(text(path), name, path)


def nested_blocks(source: str, name: str) -> list[str]:
    return [
        validate.extract_braced(source, match.start())
        for match in re.finditer(
            rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE
        )
    ]


def modifier_additions(source: str, modifier: str) -> list[str]:
    return [
        candidate
        for candidate in nested_blocks(source, "add_modifier")
        if re.search(rf"\bname\s*=\s*{re.escape(modifier)}\b", candidate)
    ]


class FrontierAiAssistanceReworkTests(unittest.TestCase):
    def test_two_rules_are_independent_and_player_challenge_defaults_off(self):
        rules = text("common/game_rules/sb_game_rules.txt")
        history = block_from_source(rules, "sb_frontier_ai_behavior", "game rules")
        challenge = block_from_source(rules, "sb_frontier_player_challenge", "game rules")
        self.assertIn("default = sb_frontier_ai_behavior_dynamic_historical", history)
        self.assertIn("default = sb_frontier_player_challenge_disabled", challenge)
        self.assertIn("sb_frontier_player_challenge_enabled", challenge)

        play_enemy = block(
            "common/scripted_triggers/sb_game_rule_triggers.txt",
            "sb_frontier_play_has_committed_player_enemy",
        )
        self.assertIn("is_diplomatic_play_committed_participant = yes", play_enemy)
        self.assertIn("is_diplomatic_play_enemy_of = $RECIPIENT$", play_enemy)

        routing = block(
            "common/scripted_triggers/sb_game_rule_triggers.txt",
            "sb_frontier_play_artificial_assistance_enabled",
        )
        for token in (
            "sb_frontier_play_has_committed_player_enemy = {",
            "RECIPIENT = $RECIPIENT$",
            "sb_frontier_player_challenge_enabled = yes",
            "sb_frontier_ai_scripting_enabled = yes",
            "is_diplomatic_play_committed_participant = yes",
        ):
            self.assertIn(token, routing)

        loc = text("localization/english/sb_game_rules_l_english.yml")
        self.assertIn('rule_sb_frontier_ai_behavior:0 "SB Frontier AI History"', loc)
        self.assertIn('rule_sb_frontier_player_challenge:0 "SB Frontier Player Challenge"', loc)
        self.assertIn("Player-facing assistance replaces the AI-History route", loc)

    def test_laager_variants_have_exact_packages_same_loc_and_fifteen_months(self):
        modifiers = text("common/static_modifiers/sb_modifiers.txt")
        laager = block_from_source(modifiers, "sb_laager_defence", "modifiers")
        ai_laager = block_from_source(modifiers, "sb_laager_defence_ai", "modifiers")
        self.assertEqual(1, modifiers.count("sb_laager_defence = {"))
        self.assertEqual(1, modifiers.count("sb_laager_defence_ai = {"))
        for token in (
            "unit_kill_rate_add = 0.50",
            "unit_recovery_rate_add = 0.75",
            "unit_defense_mult = 0.10",
        ):
            self.assertIn(token, laager)
        for forbidden in (
            "building_training_rate",
            "battle_casualties_mult",
            "unit_supply_consumption_mult",
            "military_formation_organization_gain_add",
        ):
            self.assertNotIn(forbidden, laager)

        for token in (
            "building_training_rate_add = 1000",
            "battle_casualties_mult = -1",
            "unit_recovery_rate_add = 0.75",
            "unit_kill_rate_add = 1.25",
            "unit_supply_consumption_mult = -1",
            "military_formation_organization_gain_add = 0.5",
        ):
            self.assertIn(token, ai_laager)
        self.assertNotIn("unit_defense_mult", ai_laager)

        loc = text("localization/english/sb_l_english.yml")
        desc = text("localization/english/sb_mtb_modifiers_l_english.yml")
        self.assertIn('sb_laager_defence:0 "Laager Defensive System"', loc)
        self.assertIn('sb_laager_defence_ai:0 "Laager Defensive System"', loc)
        normal_desc = re.search(r'^\s*sb_laager_defence_desc:0\s+"([^"]+)"', desc, re.MULTILINE)
        ai_desc = re.search(r'^\s*sb_laager_defence_ai_desc:0\s+"([^"]+)"', desc, re.MULTILINE)
        self.assertIsNotNone(normal_desc)
        self.assertIsNotNone(ai_desc)
        self.assertEqual(normal_desc.group(1), ai_desc.group(1))

        additions = {modifier: [] for modifier in ("sb_laager_defence", "sb_laager_defence_ai")}
        for base in (ROOT / "common", ROOT / "events"):
            for path in base.rglob("*.txt"):
                source = text(str(path.relative_to(ROOT)))
                for modifier in additions:
                    additions[modifier].extend(modifier_additions(source, modifier))
        self.assertGreaterEqual(len(additions["sb_laager_defence"]), 2)
        self.assertGreaterEqual(len(additions["sb_laager_defence_ai"]), 9)
        for modifier_adds in additions.values():
            for addition in modifier_adds:
                self.assertRegex(addition, r"\bmonths\s*=\s*15\b")

        ai_events = text("events/sb_frontier_ai_wars_events.txt")
        self.assertIn("name = sb_laager_defence_ai", ai_events)
        self.assertNotRegex(ai_events, r"name\s*=\s*sb_laager_defence\s")

    def test_removed_assistance_symbols_are_gone(self):
        removed = {
            "sb_swazi_frontier_muster_vs_player",
            "sb_bst_gun_war_defensive_muster_vs_player",
            "sb_ora_scripted_frontier_edge",
            "sb_native_conscription_MTB_player",
            "sb_xhosa_native_warbands",
            "sb_frontier_levy_reconstitution",
            "sb_amabutho_levy_reconstitution",
            "sb_trek_ai_mobilization",
            "sb_iron_age_natives",
            "sb_iron_age_weaponry",
            "sb_potgieter_relief",
        }
        source = "\n".join(
            path.read_text(encoding="utf-8-sig")
            for base in (ROOT / "common", ROOT / "events", ROOT / "localization")
            for path in base.rglob("*")
            if path.is_file() and path.suffix in {".txt", ".yml"}
        )
        for symbol in removed:
            self.assertNotIn(symbol, source)
        self.assertFalse((ROOT / "common/static_modifiers/sb_conscription_modifiers.txt").exists())

    def test_force_floors_are_structural_routed_and_mobilized(self):
        values = text("common/script_values/sb_frontier_force_values.txt")
        conscripts = block_from_source(values, "sb_frontier_conscript_force_floor", "force values")
        regulars = block_from_source(values, "sb_frontier_regular_force_floor", "force values")
        self.assertRegex(conscripts, r"country_definition\s*=\s*cd:XHO[\s\S]*?add\s*=\s*12")
        self.assertNotIn("cd:MTB", conscripts)
        self.assertNotIn("cd:XHO", regulars)
        self.assertNotIn("cd:MTB", regulars)

        eligibility = block(
            "common/scripted_triggers/sb_game_rule_triggers.txt",
            "sb_frontier_ai_force_floor_eligible",
        )
        for tag in ("cd:ZUL", "cd:SWZ", "cd:GZA", "cd:BST", "cd:XHO"):
            self.assertIn(tag, eligibility)
        self.assertNotIn("cd:MTB", eligibility)
        self.assertIn("sb_frontier_artificial_assistance_enabled = yes", eligibility)

        effects = text("common/scripted_effects/sb_frontier_force_effects.txt")
        state_selection = block_from_source(
            effects, "sb_save_frontier_recruitment_state", "force effects"
        )
        restore = block_from_source(effects, "sb_restore_ai_frontier_force_floor", "force effects")
        mobilize = block_from_source(
            effects, "sb_mobilize_ai_frontier_historical_formation", "force effects"
        )
        mobilize_for_play = block_from_source(
            effects,
            "sb_mobilize_ai_frontier_historical_formations_for_play",
            "force effects",
        )
        self.assertNotIn("building_training_rate", restore)
        self.assertNotIn("sb_native_conscription_MTB", restore)
        self.assertNotIn("cd:MTB", state_selection)
        self.assertIn("building = building_conscription_center", restore)

        mtb_history = text("common/history/countries/mtb - matabele.txt")
        mtb_setup = block(
            "common/scripted_effects/sb_native_conscription.txt",
            "sb_effect_native_conscription_MTB",
        )
        self.assertIn("sb_effect_native_conscription_MTB = yes", mtb_history)
        self.assertIn("is_country_type = decentralized", mtb_setup)
        self.assertIn("sb_mtb_native_host_assistance_enabled = yes", mtb_setup)
        self.assertIn("name = sb_native_conscription_MTB", mtb_setup)
        self.assertIn("months = -1", mtb_setup)

        mtb_gate = block(
            "common/scripted_triggers/sb_game_rule_triggers.txt",
            "sb_mtb_native_host_assistance_enabled",
        )
        for token in (
            "country_definition = cd:MTB",
            "is_ai = yes",
            "c:ORA ?= { is_country_alive = yes is_player = yes }",
        ):
            self.assertIn(token, mtb_gate)
        for forbidden in (
            "sb_frontier_player_challenge_enabled",
            "sb_frontier_ai_scripting_enabled",
            "c:ORA ?= { is_country_alive = yes is_ai = yes }",
        ):
            self.assertNotIn(forbidden, mtb_gate)

        mtb_levy = block_from_source(
            text("common/static_modifiers/sb_modifiers.txt"),
            "sb_native_conscription_MTB",
            "modifiers",
        )
        self.assertIn("state_conscription_rate_add = 0.50", mtb_levy)
        self.assertIn("building_training_rate_add = 1000", mtb_levy)
        self.assertIn("modifier_rifle_positive.dds", mtb_levy)
        for forbidden in (
            "unit_offense",
            "unit_defense",
            "unit_kill_rate",
            "unit_recovery_rate",
        ):
            self.assertNotIn(forbidden, mtb_levy)

        mtb_loc = text("localization/english/sb_mtb_modifiers_l_english.yml")
        self.assertIn(' sb_native_conscription_MTB:0 "Mzilikazi\'s Host"', mtb_loc)
        self.assertIn(" sb_native_conscription_MTB_desc:0 ", mtb_loc)
        self.assertIn("fully_mobilize_army = yes", mobilize)
        for tag in ("ZUL", "SWZ", "GZA", "BST", "XHO"):
            self.assertIn(f"cd:{tag}", mobilize)
            self.assertIn(
                f"sb_frontier_play_artificial_assistance_enabled = {{ RECIPIENT = c:{tag} }}",
                mobilize_for_play,
            )
        self.assertNotIn("cd:MTB", mobilize)
        self.assertNotIn("c:MTB", mobilize_for_play)

        xho_history = text("common/history/countries/xho - xhosa.txt")
        self.assertIn("effect_native_conscription_6 = yes", xho_history)
        self.assertNotIn("effect_native_conscription_4", xho_history)

        buildings = text("common/history/buildings/04_subsaharan_africa.txt")
        self.assertNotRegex(
            buildings,
            r"(?s)s:STATE_NORTHERN_TRANSVAAL\s*=\s*\{.*?region_state:MTB\s*=\s*\{.*?building_conscription_center",
        )

        formations = text("common/history/military_formations/07_military_formations_subsaharan_africa.txt")
        self.assertRegex(formations, r"c:XHO[\s\S]*?service_type\s*=\s*conscript[\s\S]*?count\s*=\s*6")
        self.assertNotIn("c:MTB ?=", formations)
        self.assertNotIn("mzilikazi_amabutho", formations)

    def test_xhosa_warbands_advance_after_seventh_and_eighth_war_defeats(self):
        effects_path = "common/scripted_effects/sb_native_conscription.txt"
        tier_9 = block(effects_path, "sb_xhosa_set_native_conscription_tier_9")
        tier_12 = block(effects_path, "sb_xhosa_set_native_conscription_tier_12")

        self.assertIn("is_country_type = decentralized", tier_9)
        self.assertIn("remove_modifier = native_conscription_6", tier_9)
        self.assertIn("NOT = { has_modifier = native_conscription_12 }", tier_9)
        self.assertEqual(1, len(modifier_additions(tier_9, "native_conscription_9")))
        self.assertIn("months = -1", modifier_additions(tier_9, "native_conscription_9")[0])

        self.assertIn("is_country_type = decentralized", tier_12)
        self.assertIn("remove_modifier = native_conscription_6", tier_12)
        self.assertIn("remove_modifier = native_conscription_9", tier_12)
        self.assertEqual(1, len(modifier_additions(tier_12, "native_conscription_12")))
        self.assertIn("months = -1", modifier_additions(tier_12, "native_conscription_12")[0])

        enforced = block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_wargoal_enforced",
        )
        war_end = block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_war_end",
        )
        routes = {
            "dp_sb_xhosa_war_7": (
                "sb_xhosa_war_7_goal_accepted_pending_var",
                "sb_xhosa_set_native_conscription_tier_9 = yes",
            ),
            "dp_sb_xhosa_war_8": (
                "sb_xhosa_war_8_goal_accepted_pending_var",
                "sb_xhosa_set_native_conscription_tier_12 = yes",
            ),
        }
        for play, (pending, effect) in routes.items():
            self.assertIn(f"is_diplomatic_play_type = {play}", enforced)
            self.assertIn(pending, enforced)
            self.assertNotIn(effect, enforced)
            self.assertIn(f"is_diplomatic_play_type = {play}", war_end)
            self.assertIn(pending, war_end)
            self.assertIn(effect, war_end)

    def test_mtb_opening_uprising_capacity_is_vrystaat_only(self):
        opening = block("events/sb_great_trek_events.txt", "sb_great_trek.001")
        self.assertIn("type = dp_native_uprising", opening)
        self.assertIn("target_country = c:ORA", opening)

        pops = text("common/history/pops/04_subsaharan_africa.txt")
        vrystaat = block_from_source(pops, "s:STATE_VRYSTAAT", "population history")
        mtb = block_from_source(vrystaat, "region_state:MTB", "Vrystaat history")
        population = sum(
            int(size) for size in re.findall(r"\bsize\s*=\s*(\d+)", mtb)
        )
        self.assertEqual(13_218, population)
        self.assertEqual(1, int(population * 0.25 * 0.54 / 1000))

    def test_dynamic_historical_dice_match_the_agreed_matrix(self):
        path = "events/sb_frontier_ai_wars_events.txt"
        ora_phl = block(path, "sb_frontier_ai_wars.010")
        ora_bst = block(path, "sb_frontier_ai_wars.020")
        bst_trn = block(path, "sb_frontier_ai_wars.025")
        bst_zpb = block(path, "sb_frontier_ai_wars.026")
        annex = block(path, "sb_frontier_ai_wars.030")

        self.assertIn("95 = {", ora_phl)
        self.assertIn("5 = { }", ora_phl)
        self.assertNotIn("sb_ora_scripted_frontier_edge", ora_phl)
        self.assertIn("80 = {", ora_bst)
        self.assertIn("20 = {", ora_bst)
        self.assertIn("sb_ora_bst_surprise_disarray", ora_bst)
        self.assertNotIn("create_pop", ora_bst)
        for event in (bst_trn, bst_zpb):
            self.assertIn("90 = {", event)
            self.assertIn("10 = {", event)
        for weight in ("60 = {", "20 = {"):
            self.assertIn(weight, annex)

    def test_blood_river_routes_without_material_injections_or_double_help(self):
        resolver = block("events/sb_natal_crisis_events.txt", "sb_natal_crisis.019")
        reconcile = block(
            "common/scripted_effects/sb_natalia_effects.txt",
            "sb_reconcile_blood_river_assistance_for_play",
        )
        for token in (
            "sb_frontier_player_challenge_enabled = yes",
            "sb_frontier_ai_behavior_dynamic_historical = yes",
            "sb_frontier_ai_behavior_strict_historical = yes",
            "30 = {",
            "70 = {",
            "name = sb_blood_river_zulu_limited_support",
            "name = sb_zul_blood_river_no_relief_roll_var",
            "months = 15",
        ):
            self.assertIn(token, resolver)
        limited = block_from_source(
            text("common/static_modifiers/sb_modifiers.txt"),
            "sb_blood_river_zulu_limited_support",
            "modifiers",
        )
        self.assertIn("unit_offense_mult = 0.05", limited)
        self.assertIn("unit_defense_mult = 0.05", limited)
        self.assertNotIn("sb_ora_blood_river_player_zul_extra_force_var", resolver)
        self.assertNotIn("remove_modifier = sb_laager_defence", resolver)
        for token in (
            "sb_frontier_play_has_committed_player_enemy = { RECIPIENT = c:ORA }",
            "sb_frontier_play_has_committed_player_enemy = { RECIPIENT = c:ZUL }",
            "sb_apply_ora_blood_river_player_laager = yes",
            "sb_apply_ora_blood_river_ai_laager = yes",
            "sb_ensure_ora_ai_natal_front_commitment = yes",
            "sb_clear_ora_blood_river_laager = yes",
            "remove_modifier = sb_blood_river_zulu_no_relief",
            "remove_modifier = sb_blood_river_zulu_limited_support",
            "remove_modifier = sb_blood_river_zulu_relief_mobilization",
            "sb_apply_zul_blood_river_readiness = yes",
            "has_variable = sb_zul_blood_river_positive_roll_var",
            "has_variable = sb_zul_blood_river_no_relief_roll_var",
        ):
            self.assertIn(token, reconcile)
        player_laager = block(
            "common/scripted_effects/sb_natalia_effects.txt",
            "sb_apply_ora_blood_river_player_laager",
        )
        ai_laager = block(
            "common/scripted_effects/sb_natalia_effects.txt",
            "sb_apply_ora_blood_river_ai_laager",
        )
        clear_laager = block(
            "common/scripted_effects/sb_natalia_effects.txt",
            "sb_clear_ora_blood_river_laager",
        )
        self.assertIn("name = sb_laager_defence", player_laager)
        self.assertIn("name = sb_laager_defence_ai", ai_laager)
        self.assertIn("sb_ora_blood_river_laager_active_var", player_laager)
        self.assertIn("sb_ora_blood_river_laager_active_var", ai_laager)
        self.assertIn("sb_ora_blood_river_laager_active_var", clear_laager)
        self.assertIn("remove_modifier = sb_laager_defence", clear_laager)
        self.assertIn("remove_modifier = sb_laager_defence_ai", clear_laager)

        floor = block(
            "common/scripted_effects/sb_natalia_effects.txt",
            "sb_ensure_ora_ai_natal_front_commitment",
        )
        self.assertEqual(1, floor.count("combat_unit_type_dragoons"))
        self.assertEqual(1, floor.count("combat_unit_type_line_infantry"))
        self.assertEqual(2, floor.count("count = 1"))
        self.assertNotIn("create_pop", floor)
        self.assertNotIn("create_building", floor)
        handlers = text("common/on_actions/sb_diplomatic_play_on_action_handlers.txt")
        self.assertGreaterEqual(
            handlers.count("sb_reconcile_blood_river_assistance_for_play = yes"), 3
        )

    def test_swazi_and_gun_war_use_single_rule_routed_packages(self):
        modifiers = text("common/static_modifiers/sb_modifiers.txt")
        self.assertEqual(1, modifiers.count("sb_swazi_frontier_muster = {"))
        self.assertEqual(1, modifiers.count("sb_bst_gun_war_defensive_muster = {"))
        self.assertNotIn("_vs_player", modifiers)

        swazi = block(
            "common/scripted_effects/sb_swazi_effects.txt",
            "sb_route_swazi_defensive_muster_for_play",
        )
        for token in (
            "scope:target ?= {",
            "country_definition = cd:SWZ",
            "sb_frontier_play_has_committed_player_enemy = { RECIPIENT = c:SWZ }",
            "sb_frontier_player_challenge_enabled = yes",
            "sb_frontier_ai_scripting_enabled = yes",
            "sb_clear_swazi_defensive_muster_for_play = yes",
            "sb_swazi_ai_history_muster_selected_var",
        ):
            self.assertIn(token, swazi)
        self.assertNotIn("any_scope_play_involved = { country_definition = cd:SWZ }", swazi)
        raw_muster = block(
            "common/scripted_effects/sb_swazi_effects.txt",
            "sb_swazi_raise_defensive_muster",
        )
        clear_muster = block(
            "common/scripted_effects/sb_swazi_effects.txt",
            "sb_swazi_clear_defensive_muster",
        )
        self.assertEqual(1, raw_muster.count("add_treasury = 10000"))
        self.assertEqual(1, clear_muster.count("add_treasury = -10000"))
        self.assertEqual(2, raw_muster.count("sb_swazi_defensive_muster_var"))
        self.assertNotIn("sb_swazi_defensive_muster_vs_player_var", raw_muster)

        swazi_event = block("events/sb_swazi_frontier_events.txt", "sb_swazi_frontier.094")
        self.assertEqual(2, swazi_event.count("base = 50"))
        self.assertIn("sb_frontier_ai_behavior_strict_historical = yes", swazi_event)
        self.assertIn("add = 1000", swazi_event)
        self.assertIn("add = -1000", swazi_event)

        gun = block(
            "common/scripted_effects/sb_bst_effects.txt",
            "sb_initialize_bst_gun_war_defence_for_play",
        )
        for token in (
            "scope:target ?= { country_definition = cd:BST",
            "sb_frontier_play_has_committed_player_enemy = { RECIPIENT = c:BST }",
            "sb_frontier_player_challenge_enabled = yes",
            "sb_frontier_ai_behavior_strict_historical = yes",
            "sb_frontier_ai_behavior_dynamic_historical = yes",
            "66 = {",
            "33 = {}",
        ):
            self.assertIn(token, gun)
        gun_event = block("events/sb_bst_frontier_events.txt", "sb_bst_frontier.220")
        self.assertIn("sb_initialize_bst_gun_war_defence_for_play = yes", gun_event)
        self.assertNotIn("sb_bst_apply_gun_war_ai_defence", gun_event)
        self.assertIn("add = 1000", gun_event)
        self.assertIn("add = -1000", gun_event)

        handlers = text("common/on_actions/sb_diplomatic_play_on_action_handlers.txt")
        for token in (
            "sb_on_spes_bona_diplo_play_abandon_side",
            "sb_cleanup_blood_river_assistance_for_play = yes",
            "sb_cleanup_swazi_defensive_muster_for_play = yes",
            "sb_cleanup_bst_gun_war_defence_for_play = yes",
        ):
            self.assertIn(token, handlers)
        abandon = block_from_source(
            handlers,
            "sb_on_spes_bona_diplo_play_abandon_side",
            "diplomatic-play handlers",
        )
        self.assertNotIn("sb_schedule_trn_frontier_deployment_for_play", abandon)

    def test_trn_deployment_uses_only_committed_opponents_in_the_current_play(self):
        schedule = block(
            "common/scripted_effects/sb_frontier_ai_deployment_effects.txt",
            "sb_schedule_trn_frontier_deployment_for_play",
        )
        self.assertIn(
            "sb_frontier_play_artificial_assistance_enabled = { RECIPIENT = c:TRN }",
            schedule,
        )
        self.assertIn("is_diplomatic_play_committed_participant = yes", schedule)
        self.assertIn("is_diplomatic_play_enemy_of = c:TRN", schedule)
        self.assertNotIn("sb_frontier_artificial_assistance_enabled = yes", schedule)

        join = block(
            "common/scripted_effects/sb_natalia_effects.txt",
            "sb_join_trn_to_active_natal_war",
        )
        self.assertIn("is_diplomatic_play_committed_participant = yes", join)

    def test_natalia_player_support_requires_a_committed_player_in_its_exact_play(self):
        path = "common/scripted_effects/sb_natalia_colony_effects.txt"
        routing = block(path, "sb_handle_natalia_player_support_join")
        self.assertIn("initiator = c:GBR", routing)
        self.assertIn("target = c:NAL", routing)
        self.assertIn("is_player = yes", routing)
        self.assertIn("is_diplomatic_play_committed_participant = yes", routing)

        join = block(path, "sb_join_natalia_against_britain")
        goal = block(path, "sb_add_natalia_liberate_cape_goal_if_oranje_supports")
        for candidate in (join, goal):
            self.assertIn("is_diplomatic_play_committed_participant = yes", candidate)

    def test_zoutpansberg_anti_player_support_is_challenge_gated(self):
        crackdown = block(
            "common/scripted_effects/sb_treaty_effects.txt",
            "sb_open_trn_zpb_crackdown_play",
        )
        self.assertIn("is_player = yes", crackdown)
        self.assertIn("sb_frontier_player_challenge_enabled = yes", crackdown)
        self.assertIn("sb_apply_zpb_player_trn_civil_war_support = yes", crackdown)

    def test_klip_river_keeps_story_assets_but_routes_only_artificial_rolls(self):
        setup = block(
            "common/scripted_triggers/sb_klip_river_county_triggers.txt",
            "sb_klip_river_county_setup_valid",
        )
        self.assertIn("p:xBBCA32.state.owner = this", setup)
        self.assertNotIn("xE1E455", setup)

        effects_path = "common/scripted_effects/sb_klip_river_county_effects.txt"
        creation = block(effects_path, "sb_klip_river_create_county")
        for token in (
            "xBBCA32 xDE0EDE x552449",
            "building = building_maize_farm",
            "combat_unit_type_dragoons",
            "combat_unit_type_irregular_infantry",
        ):
            self.assertIn(token, creation)
        self.assertNotIn("sb_frontier_ai_scripting_enabled", creation)
        self.assertNotIn("sb_frontier_player_challenge_enabled", creation)

        coalition = block(effects_path, "sb_klip_river_roll_coalition_boost")
        coalition_laager = block(effects_path, "sb_klip_river_apply_coalition_laager")
        punitive = block(effects_path, "sb_klip_river_roll_punitive_zulu_boost")
        self.assertIn("sb_klip_river_coalition_assistance_enabled = yes", coalition)
        self.assertIn("sb_klip_river_apply_coalition_laager = yes", coalition)
        self.assertIn("70 = {", coalition)
        self.assertIn("30 = {", coalition)
        self.assertIn("sb_klip_river_coalition_player_challenge_enabled = yes", coalition_laager)
        self.assertIn("name = sb_laager_defence months = 15", coalition_laager)
        self.assertIn("sb_klip_river_coalition_ai_history_enabled = yes", coalition_laager)
        self.assertIn("name = sb_laager_defence_ai months = 15", coalition_laager)
        self.assertIn("sb_klip_river_punitive_assistance_enabled = yes", punitive)
        self.assertIn("60 = {", punitive)

        boundary = block("events/sb_klip_river_county_events.txt", "sb_klip_river_county.010")
        strict_weights = [
            candidate
            for candidate in nested_blocks(boundary, "modifier")
            if "sb_frontier_ai_behavior_strict_historical = yes" in candidate
        ]
        self.assertEqual(1, len(strict_weights))
        for token in ("is_ai = yes", "c:ZUL ?=", "c:GBR ?="):
            self.assertIn(token, strict_weights[0])

        reduced = block(effects_path, "sb_klip_river_finalize_reduced_natalia")
        zululand = block_from_source(reduced, "s:STATE_ZULULAND", "reduced Natalia")
        transfers = [
            candidate
            for candidate in nested_blocks(zululand, "set_owner_of_provinces")
            if "country = c:ZUL" in candidate
        ]
        self.assertEqual(1, len(transfers))
        self.assertEqual(ZULULAND_PROVINCES, validate.object_values(transfers[0], "provinces"))
        self.assertNotIn("country = c:KLR", zululand)
        self.assertNotIn("region_state:NAL", reduced)


if __name__ == "__main__":
    unittest.main()
