from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def object_block(path: str, name: str) -> str:
    source = text(path)
    match = re.search(rf"^{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} in {path}")
    return validate.extract_braced(source, match.start())


class MediumLowRemediationTests(unittest.TestCase):
    def test_sgo_border_contract_matches_creation_priority(self):
        trigger = object_block(
            "common/scripted_triggers/sb_bechuanaland_corridor_triggers.txt",
            "sb_bechuanaland_tsw_holds_actor_border_beachhead",
        )
        effect = object_block(
            "common/scripted_effects/sb_bechuanaland_corridor_effects.txt",
            "sb_bechuanaland_create_sgo_beachhead_for_root",
        )
        expected = ("D76CB9", "20CAA7", "4AFDFD", "A494F8")
        trigger_provinces = tuple(value.upper() for value in re.findall(r"holds_([0-9a-f]+)_actor_border", trigger, re.I))
        self.assertEqual(expected, trigger_provinces)
        self.assertEqual(expected, tuple(re.findall(r"province\s*=\s*p:x([0-9A-F]+)", effect)))
        self.assertIn("NOT = { c:SGO ?= { is_country_alive = yes } }", effect)

    def test_basotho_retreat_reuses_one_actor_scope(self):
        event = object_block("events/sb_bst_frontier_events.txt", "sb_bst_frontier.020")
        self.assertIn("total_size >= 5000", event)
        self.assertGreaterEqual(event.count("scope:sb_bst_current_oranje_actor"), 3)
        self.assertNotIn("sb_bst_second_oranje_actor", event)

    def test_martinus_chain_has_lease_and_central_cleanup(self):
        events = text("events/sb_martinus_confederation_events.txt")
        cleanup = object_block(
            "common/scripted_effects/sb_martinus_confederation_effects.txt",
            "sb_martinus_clear_coercive_chain_state",
        )
        monthly = text("common/on_actions/sb_boer_story_on_action_handlers.txt")
        self.assertRegex(events, r"name\s*=\s*sb_martinus_coercive_chain_active_var\s+days\s*=\s*90")
        self.assertIn("remove_variable = sb_martinus_coercive_chain_active_var", cleanup)
        self.assertIn("sb_martinus_clear_coercive_chain_state = yes", monthly)

    def test_imperial_confederation_terminal_cleanup_is_persistent(self):
        effects_path = "common/scripted_effects/sb_eastern_sphere_effects.txt"
        effects = text(effects_path)
        journal = object_block(
            "common/journal_entries/1-09_sb_eastern_sphere.txt",
            "je_sb_imperial_confederation_scheme",
        )
        success = object_block(effects_path, "sb_imperial_confederation_form_saf")
        failure = object_block(effects_path, "sb_imperial_confederation_fail_scheme")
        recovery = object_block(effects_path, "sb_imperial_confederation_recover_terminal_je")
        self.assertGreaterEqual(effects.count("set_global_variable = sb_imperial_confederation_scheme_resolved_var"), 2)
        self.assertNotIn("sb_imperial_confederation_clear_runtime = yes", success)
        self.assertNotIn("sb_imperial_confederation_clear_runtime = yes", failure)
        self.assertEqual(2, journal.count("sb_imperial_confederation_clear_runtime = yes"))
        self.assertIn("has_global_variable = sb_imperial_confederation_scheme_resolved_var", journal)
        self.assertIn("NOT = { exists = c:SAF }", journal)
        self.assertIn("add_involved_country = c:GBR", recovery)
        self.assertIn("sb_imperial_confederation_recover_terminal_je = yes", effects)

    def test_delagoa_gateway_handles_network_and_market_owner(self):
        gateway = object_block(
            "common/scripted_triggers/sb_eastern_sphere_triggers.txt",
            "sb_delagoa_has_valid_gateway",
        )
        transit = object_block(
            "common/scripted_triggers/sb_eastern_sphere_triggers.txt",
            "sb_delagoa_actor_has_trade_through",
        )
        self.assertIn("sb_is_outside_british_imperial_network = yes", gateway)
        self.assertIn("this = scope:sb_delagoa_actor_scope", transit)

    def test_mozambique_company_matches_charter_package(self):
        effects = text("common/scripted_effects/sb_eastern_sphere_effects.txt")
        for token in (
            "amendment_racialized_subjecthood",
            "resource_extraction_charter_modifier",
            "ideology_colonialist",
            "colonial_enterprise_modifier",
            "ai_strategy_colonial_extraction",
        ):
            self.assertIn(token, effects)

    def test_gui_and_ideology_overrides_are_narrowed(self):
        self.assertFalse((ROOT / "gui/journal.gui").exists())
        self.assertFalse((ROOT / "gui/journal_entry.gui").exists())
        self.assertFalse((ROOT / "common/ideologies/zz_sb_reformer_ideology_override.txt").exists())
        junker = text("common/ideologies/zz_sb_junker_colonialism.txt")
        self.assertIn("law_social_monarchy = approve", junker)

    def test_responsible_government_lens_icons_match_source(self):
        source = (ROOT / "gfx/interface/icons/diplomatic_action_icons/responsible_government.dds").read_bytes()
        for name in (
            "sb_grant_responsible_government.dds",
            "sb_ask_responsible_government.dds",
            "sb_ask_responsible_government_obligation.dds",
        ):
            self.assertEqual(source, (ROOT / "gfx/interface/icons/lens_toolbar_icons" / name).read_bytes())

    def test_subject_cleanup_and_modifier_repairs_are_low_frequency(self):
        subject_actions = text("common/on_actions/sb_cap_subject_cleanup_on_actions.txt")
        self.assertNotIn("on_monthly_pulse_country", subject_actions)
        self.assertIn("on_yearly_pulse_country", subject_actions)
        for path, variable in (
            ("common/scripted_effects/sb_zulu_dynasty_effects.txt", "sb_zulu_dynastic_stability_applied_tier_var"),
            ("common/scripted_effects/sb_namibia_effects.txt", "sb_nam_consolidation_applied_tier_var"),
            ("common/scripted_effects/sb_cape_politics_effects.txt", "sb_cape_balance_applied_band_var"),
        ):
            self.assertIn(variable, text(path))

    def test_crisis_queue_uses_one_initializer_and_one_snapshot_refresh(self):
        path = "common/scripted_effects/sb_bechuanaland_corridor_effects.txt"
        for name in (
            "sb_bechuanaland_queue_warren_direct_crisis",
            "sb_bechuanaland_queue_warren_proxy_crisis",
            "sb_bechuanaland_queue_caprivi_direct_crisis",
            "sb_bechuanaland_queue_caprivi_proxy_crisis",
        ):
            block = object_block(path, name)
            self.assertEqual(1, block.count("sb_bechuanaland_initialize_crisis_queue = yes"))
            self.assertEqual(1, block.count("sb_bechuanaland_refresh_crisis_launch_participants = yes"))

    def test_central_router_preserves_handler_order(self):
        router = text("common/on_actions/sb_on_actions.txt")
        expected = {
            "on_game_started": ("sb_on_game_started",),
            "on_game_started_after_lobby": ("sb_on_game_started_after_lobby",),
            "on_diplomatic_play_started": ("sb_on_spes_bona_diplomatic_play_started",),
            "on_diplo_play_join_side": ("sb_on_spes_bona_diplo_play_join_side",),
            "on_diplo_play_war_start": ("sb_on_spes_bona_diplo_play_war_start",),
            "on_diplo_play_back_down": ("sb_on_spes_bona_diplo_play_back_down",),
            "on_diplo_play_abandon_side": ("sb_on_spes_bona_diplo_play_abandon_side",),
            "on_become_subject": (
                "sb_on_natalia_become_british_subject",
                "sb_on_bechuanaland_subject_status_changed",
            ),
            "on_monthly_pulse_country": (
                "sb_on_cape_monthly_pulse_country",
                "sb_on_trek_monthly_pulse_country",
                "sb_on_zpb_monthly_pulse_country",
                "sb_on_gbr_colonial_offices_monthly_pulse_country",
                "sb_on_de_beers_rhodes_monthly_pulse_country",
                "sb_on_de_beers_prosperous_under_rhodes_monthly_pulse_country",
                "sb_on_rhodesian_venture_monthly_pulse_country",
                "sb_on_namibia_monthly_pulse_country",
                "sb_on_eastern_sphere_monthly_pulse_country",
                "sb_on_natal_colony_monthly_pulse_country",
                "sb_on_frontier_force_monthly_pulse_country",
            ),
            "on_yearly_pulse_country": (
                "sb_on_cape_yearly_pulse_country",
                "sb_on_modifier_cache_yearly_repair",
                "sb_on_boer_restraint_yearly_repair",
            ),
            "on_state_owner_change": ("sb_on_namibia_consolidation_state_owner_change",),
            "on_acquired_technology": ("sb_on_spes_bona_acquired_technology",),
            "on_election_campaign_end": ("sb_on_martinus_union_election_end",),
            "on_colony_created": ("sb_on_spes_bona_colony_created",),
            "on_secession_start": ("sb_on_cape_secession_start",),
            "on_revolution_start": ("sb_on_cape_secession_start",),
            "on_secession_end": ("sb_on_cape_secession_end",),
            "on_revolution_end": ("sb_on_cape_secession_end",),
            "on_wargoal_enforced": ("sb_on_spes_bona_wargoal_enforced",),
            "on_war_end": ("sb_on_spes_bona_war_end",),
            "on_law_activated": ("sb_on_boer_convention_law_activated",),
            "on_company_established": ("sb_on_de_beers_company_established",),
            "on_company_disbanded": (
                "sb_on_mozambique_company_disbanded",
                "sb_on_british_south_africa_company_disbanded",
            ),
        }
        for on_action, handlers in expected.items():
            block = validate.extract_braced(router, router.index(f"{on_action} = {{"))
            registered = tuple(re.findall(r"\bsb_[a-z0-9_]+\b", block))
            self.assertEqual(handlers, registered, on_action)

    def test_boer_restraint_uses_direct_tags_and_annual_watchdog(self):
        effects = text("common/scripted_effects/sb_british_boer_restraint_effects.txt")
        strategies = text("common/ai_strategies/sb_ai_strategies.txt")
        localization = text("localization/english/sb_l_english.yml")
        self.assertNotIn("ai_strategy_sb_british_boer_restraint", strategies)
        self.assertNotIn("ai_strategy_sb_british_boer_restraint", localization)
        self.assertNotIn("every_country", effects)
        self.assertIn("secret_goal = befriend", effects)
        self.assertIn("sb_frontier_ai_scripting_enabled = yes", effects)
        self.assertIn("NOT = { has_war_with = scope:sb_boer_restraint_actor_scope }", effects)
        self.assertIn(
            "NOT = { is_diplomatic_play_enemy_of = scope:sb_boer_restraint_actor_scope }",
            effects,
        )
        self.assertIn("sb_british_boer_restraint_goal_var", effects)
        self.assertIn("sb_cape_boer_restraint_goal_var", effects)
        for tag in ("ORA", "TRN", "ZPB", "LYD", "NAL", "SGO", "ABY", "KLR"):
            self.assertIn(f"c:{tag} ?=", effects)
        handlers = text("common/on_actions/sb_regional_on_action_handlers.txt")
        self.assertIn("sb_on_boer_restraint_yearly_repair", handlers)
        monthly = object_block(
            "common/on_actions/sb_regional_on_action_handlers.txt",
            "sb_on_gbr_colonial_offices_monthly_pulse_country",
        )
        self.assertNotIn("sb_refresh_british_cape_boer_restraint", monthly)

    def test_recurring_feature_ownership_is_singular(self):
        mineral = text("common/on_actions/sb_mineral_discoveries_on_actions.txt")
        self.assertEqual(1, mineral.count("sb_on_mineral_discoveries_acquired_technology = {"))
        self.assertEqual(1, mineral.count("on_actions = { sb_on_mineral_discoveries_acquired_technology }"))

        cape_handlers = text("common/on_actions/sb_cape_on_action_handlers.txt")
        router = text("common/on_actions/sb_on_actions.txt")
        self.assertEqual(1, cape_handlers.count("sb_on_cape_yearly_pulse_country = {"))
        self.assertEqual(1, router.count("sb_on_cape_yearly_pulse_country"))

        boer_actions = text("common/on_actions/sb_boer_ai_economy_on_actions.txt")
        self.assertEqual(1, boer_actions.count("sb_boer_ai_economy_ora_law_yearly_pulse = yes"))
        self.assertEqual(1, boer_actions.count("sb_boer_ai_economy_ora_yearly_pulse = yes"))

        all_on_actions = "\n".join(
            path.read_text(encoding="utf-8-sig")
            for path in (ROOT / "common/on_actions").glob("*.txt")
        )
        self.assertNotRegex(all_on_actions, r"sb_on_namibia_[a-z0-9_]*yearly")


if __name__ == "__main__":
    unittest.main()
