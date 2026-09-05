from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]
ZULULAND_PROVINCES = {
    "xBE6FEE",
    "x1A084B",
    "xBFA16B",
    "x9E9742",
    "x88FAD4",
    "x904EBE",
    "x41C070",
    "xE882CE",
    "xE1E455",
}
GREATER_NRP_PROVINCES = {
    "xE1E455",
    "xE882CE",
    "xBE6FEE",
    "x904EBE",
    "x9E9742",
}
REDUCED_NRP_PROVINCES = {"xBE6FEE", "xE882CE"}


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def object_block(path: str, name: str) -> str:
    source = text(path)
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} in {path}")
    return validate.extract_braced(source, match.start())


def nested_blocks(source: str, name: str) -> list[str]:
    return [
        validate.extract_braced(source, match.start())
        for match in re.finditer(
            rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE
        )
    ]


def option(event: str, name: str) -> str:
    for block in nested_blocks(event, "option"):
        if re.search(rf"\bname\s*=\s*{re.escape(name)}\b", block):
            return block
    raise AssertionError(f"missing option {name}")


def province_values(source: str) -> set[str]:
    match = re.search(r"\bprovinces\s*=\s*\{([^}]*)\}", source, re.DOTALL)
    if match is None:
        raise AssertionError("missing provinces list")
    return set(re.findall(r"x[0-9A-F]{6}", match.group(1)))


class ZululandPostwarSettlementTests(unittest.TestCase):
    def test_british_handoff_restores_the_full_zululand_state_atomically(self):
        path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        normalize = object_block(path, "sb_zululand_normalize_live_subject_for_natal")
        restore = object_block(path, "sb_zululand_restore_protectorate_for_natal")
        direct = object_block(path, "sb_zululand_apply_direct_british_administration")
        event = object_block("events/sb_zululand_settlement_events.txt", "sb_zululand_settlement.001")
        trigger = object_block(
            "common/scripted_triggers/sb_zululand_settlement_triggers.txt",
            "sb_zululand_under_british_postwar_control",
        )
        releasable = object_block("common/country_creation/sb_releasable_countries.txt", "ZUL")

        self.assertEqual(ZULULAND_PROVINCES, province_values(direct))
        self.assertIn("type = protectorate", normalize)
        self.assertIn("sb_natal_schedule_zulu_settlement = yes", normalize)
        self.assertNotIn("set_owner_of_provinces", normalize)

        self.assertIn("save_scope_as = sb_zululand_restoration_state", restore)
        self.assertIn("state = scope:sb_zululand_restoration_state", restore)
        self.assertIn("sb_natal_apply_restored_zulu_baseline = yes", restore)
        self.assertIn("sb_zululand_normalize_live_subject_for_natal = yes", restore)
        self.assertNotIn("province =", restore)
        self.assertNotIn("set_owner_of_provinces", restore)
        self.assertNotIn("subject_shell", restore)

        self.assertEqual(2, trigger.count("owns_entire_state_region = STATE_ZULULAND"))
        self.assertIn("STATE_NATAL", releasable)
        self.assertIn("STATE_ZULULAND", releasable)
        self.assertIn("add_radicals = { value = 0.25 culture = cu:zulu }", direct)
        self.assertIn("sb_natal_create_zulu_national_movement = yes", direct)
        self.assertIn("sb_zululand_handoff_to_natal = yes", option(event, "sb_zululand_settlement.001.a"))
        direct_option = option(event, "sb_zululand_settlement.001.b")
        self.assertIn("is_player = yes", direct_option)
        self.assertIn("sb_zululand_apply_direct_british_administration = yes", direct_option)

        housekeeping = object_block(path, "sb_zululand_postwar_monthly_housekeeping")
        self.assertIn(
            "NOT = { has_variable = sb_zululand_postwar_handoff_event_open_var }",
            housekeeping,
        )
        self.assertIn(
            "name = sb_zululand_postwar_handoff_event_open_var days = 120",
            housekeeping,
        )
        event_preamble = event.split("option =", 1)[0]
        self.assertNotIn(
            "remove_variable = sb_zululand_postwar_handoff_event_open_var",
            event_preamble,
        )
        for effect in (
            "sb_zululand_handoff_to_natal",
            "sb_zululand_apply_direct_british_administration",
        ):
            self.assertIn(
                "remove_variable = sb_zululand_postwar_handoff_event_open_var",
                object_block(path, effect),
            )

        event_source = text("events/sb_zululand_settlement_events.txt")
        effect_source = text(path)
        self.assertNotIn("sb_zululand_settlement.002", event_source)
        self.assertNotIn("sb_zululand_subject_shell_pending_var", effect_source)

    def test_natal_administration_event_routes_to_three_distinct_settlements(self):
        event = object_block("events/sb_natal_interwar_events.txt", "sb_natal_interwar.030")
        direct_option = option(event, "sb_natal_interwar.030.a")
        chiefdom_option = option(event, "sb_natal_interwar.030.b")
        crown_option = option(event, "sb_natal_interwar.030.c")
        effects_path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        direct = object_block(effects_path, "sb_zululand_choose_direct_natal_administration")
        chiefdoms = object_block(effects_path, "sb_zululand_choose_thirteen_chiefdoms")
        crown = object_block(effects_path, "sb_zululand_choose_subordinate_crown")

        self.assertIn("sb_zululand_choose_direct_natal_administration = yes", direct_option)
        self.assertIn("custom_tooltip = sb_natal_interwar.030.a.tt", direct_option)
        self.assertIn("hidden_effect = {", direct_option)
        self.assertIn("sb_zululand_choose_thirteen_chiefdoms = yes", chiefdom_option)
        self.assertIn("sb_zululand_choose_subordinate_crown = yes", crown_option)
        self.assertEqual(2, event.count("add = -1000"))
        self.assertEqual(1, event.count("add = 1000"))

        self.assertIn("annex = c:ZUL", direct)
        self.assertIn("add_radicals = { value = 0.25 culture = cu:zulu }", direct)
        self.assertIn("sb_natal_create_zulu_national_movement = yes", direct)
        self.assertIn("sb_zululand_begin_natal_incorporation = yes", direct)

        scheduler = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_schedule_zulu_settlement",
        )
        self.assertIn(
            "NOT = { has_variable = sb_natal_zulu_settlement_event_open_var }",
            scheduler,
        )
        self.assertIn(
            "name = sb_natal_zulu_settlement_event_open_var days = 120",
            scheduler,
        )
        for branch in (direct, chiefdoms, crown):
            self.assertIn(
                "remove_variable = sb_natal_zulu_settlement_event_open_var",
                branch,
            )

        self.assertIn("change_subject_type = subject_type_sb_zulu_chiefdoms", chiefdoms)
        self.assertEqual(2, chiefdoms.count("add_radicals = { value = 0.05 culture = cu:zulu }"))
        self.assertIn("sb_zululand_mark_and_exile_royal_house = yes", chiefdoms)
        self.assertIn("sb_zululand_open_chiefdoms_situation = yes", chiefdoms)

        self.assertIn("change_subject_type = subject_type_protectorate", crown)
        self.assertIn("sb_zululand_restore_preannexation_royal_house = yes", crown)
        self.assertEqual(2, crown.count("add_loyalists = { value = 0.10 culture = cu:zulu }"))
        self.assertNotIn("incorporation", crown)

    def test_british_annexation_preserves_and_restores_the_actual_zulu_crown(self):
        effects_path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        archive = object_block(
            effects_path, "sb_zululand_archive_preannexation_royal_house"
        )
        restore = object_block(
            effects_path, "sb_zululand_restore_preannexation_royal_house"
        )
        discard = object_block(
            effects_path, "sb_zululand_discard_preannexation_royal_house_archive"
        )
        baseline = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_apply_restored_zulu_baseline",
        )
        hooks_path = "common/on_actions/sb_diplomatic_play_on_action_handlers.txt"
        started = object_block(hooks_path, "sb_on_spes_bona_diplomatic_play_started")
        back_down = object_block(hooks_path, "sb_on_spes_bona_diplo_play_back_down")
        enforced = object_block(hooks_path, "sb_on_spes_bona_wargoal_enforced")
        war_end = object_block(hooks_path, "sb_on_spes_bona_war_end")

        self.assertIn("name = sb_zululand_preannexation_ruler_scope_var", archive)
        self.assertIn("name = sb_zululand_preannexation_heir_scope_var", archive)
        self.assertIn("value = scope:sb_zululand_preannexation_ruler_scope", archive)
        self.assertIn("value = scope:sb_zululand_preannexation_heir_scope", archive)
        self.assertNotIn("exile_character", archive)

        self.assertIn("exists = var:sb_zululand_preannexation_ruler_scope_var", restore)
        self.assertIn("exists = var:sb_zululand_preannexation_heir_scope_var", restore)
        self.assertIn("transfer_character = PREV", restore)
        self.assertIn("sb_zulu_install_summoned_claimant_as_ruler = yes", restore)
        self.assertIn("sb_zulu_assign_new_heir_scope = yes", restore)
        for variable in (
            "sb_zululand_preannexation_ruler_scope_var",
            "sb_zululand_preannexation_heir_scope_var",
            "sb_zululand_preannexation_royal_house_archived_var",
            "sb_zululand_preannexation_mbuyazi_line_var",
            "sb_zululand_preannexation_cetshwayo_line_var",
        ):
            self.assertIn(f"remove_variable = {variable}", discard)
        self.assertNotIn("sb_zulu_install_summoned_claimant_as_ruler", discard)
        self.assertNotIn("sb_zulu_assign_new_heir_scope", discard)
        self.assertIn("sb_zululand_restore_preannexation_royal_house = yes", baseline)

        started_routes = [
            block
            for block in nested_blocks(started, "if")
            if "sb_zululand_archive_preannexation_royal_house = yes" in block
        ]
        self.assertGreaterEqual(len(started_routes), 1)
        started_route = min(started_routes, key=len)
        self.assertIn("is_diplomatic_play_type = dp_annex_war", started_route)
        self.assertIn("scope:initiator ?=", started_route)
        self.assertIn("country_definition = cd:GBR", started_route)
        self.assertIn("scope:target ?= { country_definition = cd:ZUL is_country_alive = yes }", started_route)
        self.assertIn("sb_anglo_zulu_pressure_launch_lease_var", started_route)
        self.assertIn("sb_port_natal_british_annex_launch_lease_var", started_route)
        self.assertIn("sb_british_zulu_snapshot_annex_target_states = yes", started_route)
        self.assertIn("sb_british_zulu_backdown_finalizer_pending_var", back_down)
        self.assertIn("id = sb_anglo_zulu.099 days = 1", back_down)
        self.assertNotIn("sb_zululand_restore_preannexation_royal_house = yes", back_down)

        # OB1 timer enforcement is reversible. The crown snapshot is taken once
        # when the exact play starts, never again from a goal-enforcement callback.
        self.assertNotIn(
            "sb_zululand_archive_preannexation_royal_house = yes", enforced
        )
        self.assertIn("root = { is_diplomatic_play_type = dp_annex_war }", war_end)
        self.assertIn("scope:actor ?= { sb_zululand_british_postwar_owner = yes }", war_end)
        self.assertIn(
            "sb_zululand_discard_preannexation_royal_house_archive = yes",
            war_end,
        )
        self.assertNotIn("sb_zululand_restore_preannexation_royal_house = yes", war_end)

    def test_direct_annexation_archives_and_restores_the_named_dynastic_line(self):
        path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        direct = object_block(path, "sb_zululand_choose_direct_natal_administration")
        archive = object_block(path, "sb_zululand_archive_preannexation_royal_house")
        restore = object_block(path, "sb_zululand_restore_secession_dynasty")

        self.assertLess(
            direct.index("sb_zululand_archive_preannexation_royal_house = yes"),
            direct.index("annex = c:ZUL"),
        )
        self.assertIn("sb_zululand_preannexation_mbuyazi_line_var", archive)
        self.assertIn("sb_zululand_preannexation_cetshwayo_line_var", archive)
        ordinary_restore = object_block(path, "sb_zululand_restore_preannexation_royal_house")
        self.assertIn("remove_variable = sb_zululand_preannexation_mbuyazi_line_var", ordinary_restore)
        self.assertIn("remove_variable = sb_zululand_preannexation_cetshwayo_line_var", ordinary_restore)
        self.assertIn("sb_zululand_preannexation_ruler_scope_var", restore)
        self.assertIn("sb_zululand_preannexation_heir_scope_var", restore)
        self.assertIn("ZUL_mbuyazi_successor", restore)
        self.assertIn("ZUL_dinuzulu_heir", restore)
        self.assertIn("sb_zulu_install_summoned_claimant_as_ruler = yes", restore)
        self.assertNotIn("sb_zululand_restore_preannexation_royal_house = yes", restore)

    def test_chiefdoms_relation_and_situation_are_locked_and_shared(self):
        subject = object_block(
            "common/subject_types/sb_subject_types.txt", "subject_type_sb_zulu_chiefdoms"
        )
        action = object_block(
            "common/diplomatic_actions/sb_subject_relationships.txt", "sb_zulu_chiefdoms"
        )
        journal = object_block(
            "common/journal_entries/1-14_sb_zululand_chiefdoms.txt",
            "je_sb_zululand_chiefdoms",
        )
        involved = object_block(
            "common/scripted_triggers/sb_zululand_settlement_triggers.txt",
            "sb_zululand_chiefdoms_involved_actor",
        )

        self.assertIn("autonomy_level = 1", subject)
        self.assertIn("can_start_own_diplomatic_plays = no", subject)
        self.assertIn("use_for_release_country = no", subject)
        self.assertNotIn("higher_autonomy_subject_type_alternatives", subject)
        self.assertNotIn("lower_autonomy_subject_type_alternatives", subject)
        self.assertIn("actor_can_break = { always = no }", action)
        self.assertIn("target_can_break = { always = no }", action)

        self.assertIn("scripted_progress_bar = sb_zululand_chiefdom_balance_bar", journal)
        self.assertIn("scripted_progress_bar = sb_zululand_boer_commitment_bar", journal)
        self.assertEqual(8, journal.count("scripted_button ="))
        for country in ("NAL", "ZUL", "GBR", "TRN"):
            self.assertIn(f"country_definition = cd:{country}", involved)
        self.assertIn("state_region = s:STATE_EAST_TRANSVAAL", involved)

        runtime = object_block(
            "common/scripted_triggers/sb_zululand_settlement_triggers.txt",
            "sb_zululand_chiefdoms_runtime_valid",
        )
        housekeeping = object_block(
            "common/scripted_effects/sb_zululand_settlement_effects.txt",
            "sb_zululand_chiefdoms_monthly_housekeeping",
        )
        self.assertIn("is_subject_type = subject_type_sb_zulu_chiefdoms", runtime)
        self.assertIn("limit = { sb_zululand_chiefdoms_runtime_valid = yes }", housekeeping)
        self.assertIn("sb_zululand_cleanup_situation = yes", housekeeping)

    def test_situation_math_and_resolution_windows_match_the_design(self):
        path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        create = object_block(path, "sb_zululand_create_chiefdoms_container")
        economic = object_block(path, "sb_zululand_update_economic_dependence_drift")
        bureaucracy = object_block(path, "sb_zululand_update_bureaucracy_drift")
        terminal = object_block(path, "sb_zululand_queue_terminal_outcome")

        self.assertIn("name = sb_zululand_balance_var value = 60", create)
        self.assertIn("name = sb_zululand_boer_commitment_var value = 0", create)
        self.assertIn('value = "c:ZUL.economic_dependence(c:NAL)"', economic)
        self.assertIn("subtract = 1", economic)
        self.assertIn("min = -1 max = 1", economic)
        self.assertIn("multiply = 0.5", economic)

        self.assertIn("value = c:NAL.relative_bureaucracy", bureaucracy)
        self.assertIn("multiply = 2", bureaucracy)
        self.assertIn("subtract = var:sb_zululand_bureaucracy_square_var", bureaucracy)
        self.assertIn("multiply = 0.9", bureaucracy)
        self.assertIn("add = 0.1", bureaucracy)
        self.assertIn("min = 0 max = 1", bureaucracy)

        self.assertEqual(2, terminal.count("sb_zululand_situation_months_var >= 18"))
        for flag in (
            "sb_zululand_skirmish_fired_var",
            "sb_zululand_hut_tax_fired_var",
            "sb_zululand_defection_fired_var",
        ):
            self.assertEqual(2, terminal.count(f"has_variable = {flag}"))
        self.assertIn("sb_zululand_situation_months_var >= 60", terminal)
        self.assertIn("sb_zululand_balance_var > 50", terminal)
        self.assertIn("sb_zululand_begin_zibhebhu_terminal_generation = yes", terminal)
        self.assertIn("sb_zululand_begin_crown_terminal_generation = yes", terminal)
        zibhebhu_generation = object_block(path, "sb_zululand_begin_zibhebhu_terminal_generation")
        crown_generation = object_block(path, "sb_zululand_begin_crown_terminal_generation")
        self.assertIn("id = sb_zululand_settlement.120", zibhebhu_generation)
        self.assertIn("id = sb_zululand_settlement.121", crown_generation)
        for guard in (
            "NOT = { has_variable = sb_zululand_event_spacing_var }",
            "NOT = { has_variable = sb_zululand_incident_pending_var }",
            "NOT = { has_variable = sb_zululand_claimant_fate_pending_var }",
        ):
            self.assertEqual(3, terminal.count(guard))

    def test_player_actions_have_the_agreed_costs_and_monthly_drift(self):
        modifiers = text("common/static_modifiers/sb_modifiers.txt")
        subject_pact = object_block(
            "common/diplomatic_actions/sb_subject_relationships.txt",
            "sb_zulu_chiefdoms",
        )
        full_hut_tax = object_block(
            "common/scripted_effects/sb_zululand_settlement_effects.txt",
            "sb_zululand_apply_full_hut_tax",
        )
        relaxed_hut_tax = object_block(
            "common/scripted_effects/sb_zululand_settlement_effects.txt",
            "sb_zululand_relax_hut_tax",
        )
        relaxed_transfer = object_block(
            "common/static_modifiers/sb_modifiers.txt",
            "sb_zululand_relaxed_hut_tax_transfer",
        )
        drift = object_block(
            "common/scripted_effects/sb_zululand_settlement_effects.txt",
            "sb_zululand_apply_monthly_action_drift",
        )
        unload_trigger = object_block(
            "common/scripted_triggers/sb_zululand_settlement_triggers.txt",
            "sb_zululand_can_unload_refugees",
        )
        unload = object_block(
            "common/scripted_effects/sb_zululand_settlement_effects.txt",
            "sb_zululand_unload_zulu_refugees",
        )
        claimant = object_block(
            "common/scripted_effects/sb_zululand_settlement_effects.txt",
            "sb_zululand_return_exiled_claimant",
        )

        self.assertIn("country_authority_add = -100", modifiers)
        self.assertIn("country_expenses_add = 250", modifiers)
        self.assertIn("state_soldiers_mortality_mult = 0.01", modifiers)
        self.assertIn("income_transfer = 0.3", subject_pact)
        self.assertIn("income_transfer_based_on_second_country = yes", subject_pact)
        self.assertIn("country_subject_income_transfer_mult = -0.50", relaxed_transfer)
        self.assertNotIn("country_tax_income_add", full_hut_tax + relaxed_hut_tax)
        self.assertNotIn("c:NAL", full_hut_tax + relaxed_hut_tax)
        for value in ("add = 0.5", "subtract = 0.5", "subtract = 0.25"):
            self.assertIn(value, drift)
        self.assertIn("name = sb_zululand_boer_commitment_var add = 2", drift)
        self.assertIn("name = sb_zululand_boer_commitment_var add = 3", drift)
        self.assertIn("set_variable = sb_zululand_boer_committed_var", drift)

        self.assertNotIn("has_journal_entry = je_sb_natal_indenture_program_v2", unload_trigger)
        self.assertIn(
            "NOT = { has_variable = sb_natal_shepstone_repeal_locked_var }",
            unload_trigger,
        )
        self.assertIn("population_ratio = 0.05", unload)
        self.assertIn("remove_amendment = yes", unload)
        self.assertIn("sb_natal_apply_repealed_shepstone_consequences = yes", unload)
        self.assertIn("sb_zululand_shift_balance_usuthu_5 = yes", unload)

        self.assertIn("add_loyalists = { value = 0.20 culture = cu:zulu }", claimant)
        self.assertIn("sb_zululand_claimant_returned_var", claimant)
        self.assertIn("sb_zululand_claimant_fate_not_before_var days = 180", claimant)

    def test_incidents_claimant_fate_and_boer_appeal_are_bounded(self):
        events_path = "events/sb_zululand_settlement_events.txt"
        fate = object_block(events_path, "sb_zululand_settlement.113")
        appeal = object_block(events_path, "sb_zululand_settlement.115")
        effects_path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        spacing = object_block(effects_path, "sb_zululand_set_followup_incident_wait")
        death = object_block(effects_path, "sb_zululand_claimant_is_killed")
        aid = object_block(effects_path, "sb_zululand_accept_boer_appeal")
        move = object_block(effects_path, "sb_zululand_move_boer_volunteers_to_zululand")

        self.assertIn("days = 60", spacing)
        for event_id in (".110", ".111", ".112"):
            self.assertIn(f"sb_zululand_settlement{event_id}", text(effects_path))
        self.assertEqual(2, fate.count("80 = { sb_zululand_claimant_is_killed = yes }"))
        self.assertIn("50 = { sb_zululand_claimant_is_killed = yes }", fate)
        self.assertIn("sb_frontier_ai_behavior_strict_historical = yes", fate)
        self.assertIn("change_variable = { name = sb_zululand_balance_var add = 10 }", death)
        self.assertIn("sb_zululand_prepare_crown_successor = yes", death)

        self.assertIn("population = 500", move)
        self.assertIn("name = sb_zululand_boer_commitment_var add = 20", aid)
        self.assertIn("name = sb_zululand_balance_var subtract = 7", aid)
        self.assertIn("sb_frontier_ai_behavior_strict_historical = yes", appeal)
        self.assertIn("sb_frontier_ai_behavior_dynamic_historical = yes", appeal)
        self.assertIn("sb_frontier_ai_behavior_off = yes", appeal)

    def test_terminal_outcomes_and_later_incorporation_are_distinct(self):
        path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        zibhebhu = object_block(path, "sb_zululand_apply_zibhebhu_victory")
        crown = object_block(path, "sb_zululand_apply_crown_victory")
        incorporation = object_block(path, "sb_zululand_apply_post_annex_incorporation")
        modifiers = text("common/static_modifiers/sb_modifiers.txt")

        self.assertIn("change_subject_type = subject_type_puppet", zibhebhu)
        self.assertEqual(2, zibhebhu.count("add_radicals = { value = 0.10 culture = cu:zulu }"))
        self.assertIn("country_liberty_desire_add = -0.10", modifiers)
        self.assertIn("state_incorporation_speed_mult = 1.00", modifiers)

        self.assertIn("change_subject_type = subject_type_puppet", crown)
        self.assertEqual(2, crown.count("add_loyalists = { value = 0.10 culture = cu:zulu }"))
        self.assertIn("country_liberty_desire_add = 0.05", modifiers)
        self.assertIn("state_incorporation_speed_mult = 0.50", modifiers)
        self.assertIn("has_variable = sb_zululand_boer_committed_var", crown)
        self.assertIn("sb_nrp_create_greater_republic = yes", crown)

        self.assertEqual(2, incorporation.count("months = 120"))
        self.assertIn("sb_zululand_begin_natal_incorporation = yes", incorporation)

    def test_natal_incorporation_request_uses_the_normal_ai_interaction(self):
        effects_path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        begin = object_block(effects_path, "sb_zululand_begin_natal_incorporation")
        check = object_block(effects_path, "sb_zululand_check_natal_incorporation")

        self.assertIn(
            "set_variable = sb_zululand_incorporation_requested_var", begin
        )
        self.assertNotIn("start_incorporation", begin + check)
        self.assertIn("incorporation_progress > 0", check)
        self.assertIn("set_variable = sb_zululand_incorporation_started_var", check)
        self.assertIn("owner = root", check)
        self.assertIn("is_incorporated = no", check)
        self.assertIn("is_incorporated = yes", check)
        self.assertIn("id = sb_zululand_settlement.130", check)

    def test_dynastic_fallbacks_are_explicit_and_not_forced_agitators(self):
        templates = text("common/character_templates/sb_zulu_dynasty_characters.txt")
        effects = text("common/scripted_effects/sb_zululand_settlement_effects.txt")
        old_effects = text("common/scripted_effects/sb_natal_interwar_effects.txt")
        successor = object_block(
            "common/scripted_effects/sb_zululand_settlement_effects.txt",
            "sb_zululand_prepare_crown_successor",
        )

        for template in ("ZUL_uthumbu_successor", "ZUL_mbuyazi_successor"):
            block = object_block("common/character_templates/sb_zulu_dynasty_characters.txt", template)
            self.assertIn("historical = no", block)
        for template in (
            "ZUL_uthumbu_successor",
            "ZUL_mbuyazi_successor",
            "ZUL_dinuzulu_heir",
        ):
            self.assertIn(template, successor)
        self.assertNotIn("is_agitator = yes", effects)
        self.assertNotIn("sb_natal_ensure_zulu_restoration_agitator", old_effects)
        self.assertIn("create_political_movement", old_effects)
        self.assertIn("add_movement_enthusiasm_modifier = yes", old_effects)
        self.assertIn("Mandla", templates)

    def test_every_natal_foundation_route_seeds_the_normal_zulu_movement_once(self):
        boer_setup = object_block(
            "common/scripted_effects/sb_natalia_effects.txt",
            "sb_apply_natalia_boer_republic_setup",
        )
        british_setup = object_block(
            "common/scripted_effects/sb_natalia_colony_effects.txt",
            "sb_apply_british_natal_colony_setup",
        )
        for setup in (boer_setup, british_setup):
            self.assertIn("sb_natal_zulu_movement_seeded_var", setup)
            self.assertIn("sb_natal_create_zulu_national_movement = yes", setup)

    def test_nieuwe_republiek_uses_only_the_agreed_zululand_footprints(self):
        path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        create = object_block(path, "sb_nrp_create_greater_republic")
        finalize = object_block(path, "sb_nrp_finalize_greater_republic")
        cutback = object_block(path, "sb_nrp_accept_boundary_cutback")
        setup = object_block(path, "sb_nrp_apply_boer_republic_setup")
        ranch = object_block(path, "sb_nrp_seed_livestock_ranch")
        fallback = object_block(
            "events/sb_zululand_settlement_events.txt",
            "sb_zululand_settlement.201",
        )
        relocate_one = object_block(path, "sb_nrp_return_building_type_to_zul")
        relocate = object_block(path, "sb_nrp_return_inherited_buildings_to_zul")
        reduced = object_block(
            "common/scripted_triggers/sb_zululand_settlement_triggers.txt",
            "sb_nrp_is_reduced_republic",
        )
        trek = object_block("common/journal_entries/1-02_sb_great_trek.txt", "je_sb_great_trek")

        self.assertEqual(GREATER_NRP_PROVINCES, province_values(finalize))
        self.assertNotIn("STATE_NATAL", finalize)
        returned = province_values(cutback)
        self.assertEqual(GREATER_NRP_PROVINCES - REDUCED_NRP_PROVINCES, returned)
        for province in REDUCED_NRP_PROVINCES:
            self.assertIn(f"p:{province}.state.owner = ROOT", reduced)
        for province in GREATER_NRP_PROVINCES - REDUCED_NRP_PROVINCES:
            self.assertIn(
                f"p:{province}.state.owner = {{ NOT = {{ this = ROOT }} }}",
                reduced,
            )
        self.assertIn("origin = c:TRN", create)
        self.assertIn("on_created = {", create)
        self.assertIn("c:NAL = { sb_nrp_finalize_greater_republic = yes }", create)
        self.assertIn(
            "trigger_event = { id = sb_zululand_settlement.201 days = 1 popup = no }",
            create,
        )
        self.assertIn("has_variable = sb_nrp_setup_pending_var", fallback)
        self.assertIn("sb_nrp_finalize_greater_republic = yes", fallback)
        self.assertIn("sb_apply_boer_republic_spawn_setup = yes", setup)
        self.assertIn("add_journal_entry = { type = je_sb_great_trek }", setup)
        self.assertIn("building = building_livestock_ranch", ranch)
        self.assertNotIn("building_maize_farm", ranch + setup)
        self.assertIn("has_building = $BUILDING$", relocate_one)
        self.assertEqual(2, relocate_one.count("is_building_type = $BUILDING$"))
        self.assertEqual(2, relocate_one.count("remove_building = $BUILDING$"))
        self.assertIn("building = $BUILDING$", relocate_one)
        self.assertIn("value = PREV.level", relocate_one)
        self.assertIn(
            "level = ROOT.var:sb_nrp_relocated_building_levels_var",
            relocate_one,
        )
        self.assertNotIn(".type", relocate_one + relocate)
        inherited_types = set(re.findall(r"BUILDING\s*=\s*(building_[a-z0-9_]+)", relocate))
        self.assertTrue(
            {
                "building_tooling_workshop",
                "building_paper_mill",
                "building_chemical_plant",
                "building_shipyard",
                "building_arms_industry",
                "building_artillery_foundry",
                "building_livestock_ranch",
                "building_sugar_plantation",
                "building_banana_plantation",
                "building_barrack",
                "building_logging_camp",
                "building_fishing_wharf",
                "building_port",
                "building_construction_sector",
                "building_diamond_mine",
            }.issubset(inherited_types)
        )
        self.assertIn("sb_nrp_return_inherited_buildings_to_zul = yes", finalize)
        self.assertLess(
            finalize.index("sb_nrp_return_inherited_buildings_to_zul = yes"),
            finalize.index("sb_nrp_apply_boer_republic_setup = yes"),
        )
        self.assertLess(
            finalize.index("sb_nrp_apply_boer_republic_setup = yes"),
            finalize.index("sb_nrp_seed_livestock_ranch = yes"),
        )
        self.assertNotIn("create_building", finalize)
        self.assertNotIn("remove_building", finalize)
        self.assertIn("country_definition = cd:NRP", trek)
        self.assertIn("owns_entire_state_region = STATE_ZULULAND", trek)
        self.assertIn("id = sb_great_trek.046", trek)

    def test_rebellion_nrp_waits_for_the_secession_result_before_boundary_action(self):
        path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        finalize = object_block(path, "sb_nrp_finalize_greater_republic")
        handlers = object_block(
            "common/on_actions/sb_natal_interwar_on_action_handlers.txt",
            "sb_on_natal_zulu_secession_end",
        )

        self.assertIn("sb_nrp_direct_annexation_rebellion_pending_var", finalize)
        self.assertIn("sb_nrp_direct_annexation_rebellion_var", finalize)
        self.assertIn("exists = s:STATE_ZULULAND.region_state:NAL", finalize)
        direct_branch = finalize[finalize.index("sb_nrp_direct_annexation_rebellion_pending_var") :]
        self.assertIn("NOT = { c:ZUL ?= { is_country_alive = yes } }", direct_branch)
        self.assertIn("sb_nrp_boundary_not_before_var days = 30", direct_branch)
        self.assertGreaterEqual(
            finalize.count("remove_variable = sb_nrp_direct_annexation_rebellion_pending_var"),
            2,
        )
        self.assertIn("sb_nrp_zulu_victory_honored_var", handlers)
        self.assertIn("sb_nrp_boundary_pending_var", handlers)
        self.assertIn("sb_nrp_boundary_not_before_var days = 30", handlers)
        self.assertIn("id = sb_zululand_settlement.209 days = 30 popup = no", handlers)

    def test_chiefdoms_delayed_events_revalidate_the_live_subject_relationship(self):
        events_path = "events/sb_zululand_settlement_events.txt"
        for event_id in (110, 111, 112, 113):
            event = object_block(events_path, f"sb_zululand_settlement.{event_id}")
            self.assertIn("sb_zululand_chiefdoms_runtime_valid = yes", event)
        for event_id, authority in (
            (120, "sb_zululand_bound_zibhebhu_terminal_event_authority"),
            (121, "sb_zululand_bound_crown_terminal_event_authority"),
        ):
            event = object_block(events_path, f"sb_zululand_settlement.{event_id}")
            # Delivery is intentionally broad; each option authenticates the
            # exact saved terminal receipt and stale deliveries only clean up.
            self.assertIn("trigger = { country_definition = cd:NAL }", event)
            self.assertIn(f"{authority} = yes", event)
            self.assertIn(f"NOT = {{ {authority} = yes }}", event)

        trn_eligibility = object_block(
            "common/scripted_triggers/sb_zululand_settlement_triggers.txt",
            "sb_zululand_trn_is_eligible_participant",
        )
        self.assertIn("c:NAL ?=", trn_eligibility)
        self.assertIn("sb_zululand_chiefdoms_runtime_valid = yes", trn_eligibility)

    def test_normal_endpoints_wait_for_claimant_fate_and_boer_appeal(self):
        queue = object_block(
            "common/scripted_effects/sb_zululand_settlement_effects.txt",
            "sb_zululand_queue_terminal_outcome",
        )
        hard_timeout = queue.rfind(
            "container:sb_zululand_chiefdoms_state.var:sb_zululand_situation_months_var >= 60"
        )
        self.assertGreater(hard_timeout, 0)
        normal_endpoints = queue[:hard_timeout]
        self.assertEqual(
            2,
            normal_endpoints.count(
                "NOT = { has_variable = sb_zululand_boer_appeal_pending_var }"
            ),
        )
        self.assertEqual(
            2,
            normal_endpoints.count(
                "has_variable = sb_zululand_claimant_fate_resolved_var"
            ),
        )

    def test_boundary_timers_ai_safety_and_return_state_goals_are_fixed(self):
        path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        finalize = object_block(path, "sb_nrp_finalize_greater_republic")
        cutback = object_block(path, "sb_nrp_accept_boundary_cutback")
        strength = object_block(path, "sb_nrp_calculate_boundary_strength")
        roll = object_block(path, "sb_nrp_roll_boundary_response")
        goals = object_block(path, "sb_nrp_add_boundary_war_goals")
        support = object_block(path, "sb_nrp_accept_defence_request")
        decline = object_block(path, "sb_nrp_decline_defence_request")
        housekeeping = object_block(path, "sb_nrp_monthly_housekeeping")
        monthly = object_block(
            "common/on_actions/sb_regional_on_action_handlers.txt",
            "sb_on_eastern_sphere_monthly_pulse_country",
        )

        self.assertIn("sb_nrp_boundary_not_before_var days = 30", finalize)
        self.assertIn("id = sb_zululand_settlement.209 days = 30", finalize)
        self.assertIn("sb_nrp_union_wait_var months = 24", cutback)
        self.assertNotIn("sb_nrp_union_wait_var months = 36", cutback)
        self.assertNotIn("sb_nrp_accelerate_union_after_zululand_annexation", text(path))
        self.assertNotIn("sb_nrp_union_accelerated_var", housekeeping)
        self.assertIn("country_definition = cd:NRP", monthly)

        for threshold, chance in (
            ("0.50", "5"),
            ("0.75", "15"),
            ("1", "35"),
            ("1.50", "60"),
        ):
            self.assertRegex(
                strength,
                rf"sb_nrp_strength_ratio_var < {threshold}[\s\S]*?sb_nrp_refusal_chance_var value = {chance}",
            )
        self.assertIn("sb_nrp_refusal_chance_var value = 80", strength)
        self.assertIn("c:ORA.army_power_projection", strength)
        self.assertIn("c:TRN.army_power_projection", strength)
        self.assertIn("c:GBR.army_power_projection", strength)
        self.assertIn("multiply = 0.10", strength)
        self.assertIn("sb_nrp_subject_hard_safety = yes", roll)
        self.assertIn("sb_nrp_dynamic_hard_safety = yes", roll)
        self.assertIn("random_list = { 50 =", roll)

        self.assertEqual(3, goals.count("type = return_state"))
        self.assertIn("target_country = c:NRP", goals)
        self.assertIn("target_country = c:ZUL", goals)
        self.assertIn("sb_nrp_launch_boundary_confrontation = yes", support)
        deferred_pact = object_block(path, "sb_nrp_commit_deferred_defence_pact")
        self.assertIn("sb_nrp_deferred_defence_pact_pending_var", deferred_pact)
        self.assertIn("type = sb_boer_confederal_partner", deferred_pact)
        self.assertIn("is_at_war = no", deferred_pact)
        self.assertIn("is_active_in_diplomatic_play = no", deferred_pact)
        self.assertIn("sb_nrp_trn_defence_declined_pending_var", decline)
        self.assertIn("sb_nrp_launch_boundary_confrontation = yes", decline)
        started_boundary = object_block(path, "sb_nrp_configure_started_boundary_play")
        self.assertIn("change_relations = { country = c:NRP value = -50 }", started_boundary)
        self.assertIn("has_type = defensive_pact", started_boundary)
        self.assertNotIn("add_initiator_backers = { c:GBR }", goals)

        union_event = object_block(
            "events/sb_zululand_settlement_events.txt",
            "sb_zululand_settlement.221",
        )
        accept = option(union_event, "sb_zululand_settlement.221.a")
        refuse = option(union_event, "sb_zululand_settlement.221.b")
        self.assertIn("default_option = yes", accept)
        self.assertIn("ai_chance = { base = 100 }", accept)
        self.assertIn("is_player = yes", refuse)

    def test_nrp_union_refusal_and_boundary_launch_receipts_are_generation_safe(self):
        effects_path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        union_event = object_block(
            "events/sb_zululand_settlement_events.txt", "sb_zululand_settlement.221"
        )
        player_refusal = option(union_event, "sb_zululand_settlement.221.b")
        stale_defence = next(
            block
            for block in nested_blocks(
                object_block(
                    "events/sb_zululand_settlement_events.txt",
                    "sb_zululand_settlement.211",
                ),
                "option",
            )
            if "NOT = { AND =" in block
        )
        roll = object_block(effects_path, "sb_nrp_roll_boundary_response")
        refusal = object_block(effects_path, "sb_nrp_refuse_boundary_demand")
        cleanup = object_block(effects_path, "sb_nrp_clear_boundary_confrontation_runtime")
        configured = object_block(effects_path, "sb_nrp_configure_started_boundary_play")

        # A Clausewitz object may have only one trigger key. The refusal is
        # available only to a living independent player TRN with a live receipt.
        self.assertEqual(1, player_refusal.count("trigger ="))
        self.assertIn("is_player = yes", player_refusal)
        self.assertIn("sb_nrp_union_petition_response_pending_var", player_refusal)

        # The shared AI receipt is created only after this refusal is delivered,
        # then every stale/cancel route removes it before another request can use it.
        self.assertNotIn("sb_nrp_shared_refusal_commitment_var", roll)
        self.assertIn("sb_nrp_shared_refusal_commitment_var", refusal)
        self.assertIn("if = { limit = { is_ai = yes }", refusal)
        self.assertIn("remove_variable = sb_nrp_shared_refusal_commitment_var", stale_defence)
        self.assertIn("c:TRN ?=", cleanup)
        self.assertIn("remove_variable = sb_nrp_shared_refusal_commitment_var", cleanup)

        transient_start = validate.extract_braced(
            configured,
            configured.index("else_if = {", configured.index("A real leased root")),
        )
        permanent_loss = validate.extract_braced(
            configured,
            configured.index("else_if = {", configured.index("durable route authority")),
        )
        # A leased real root with political authority but wrong target shape is
        # unbound and retryable: only its lease/scaffolding is cleared.
        self.assertIn("sb_nrp_boundary_current_political_authority = yes", transient_start)
        self.assertIn("remove_variable = sb_nrp_boundary_launch_lease_var", transient_start)
        self.assertNotIn("sb_nrp_clear_boundary_confrontation_runtime", transient_start)
        self.assertNotIn("sb_nrp_add_boundary_war_goals", transient_start)
        self.assertNotIn("sb_nrp_trn_defence_accepted_pending_var", transient_start)
        self.assertNotIn("sb_nrp_trn_defence_declined_pending_var", transient_start)
        # Lost political authority takes the central terminal cleanup and leaves
        # the unbound engine play without a route receipt or mutation authority.
        self.assertIn("sb_nrp_clear_boundary_confrontation_runtime = yes", permanent_loss)
        self.assertIn("remove_variable = sb_nrp_boundary_launch_lease_var", permanent_loss)

    def test_unrelated_imperial_wars_do_not_stall_the_nrp_boundary_demand(self):
        trigger = object_block(
            "common/scripted_triggers/sb_zululand_settlement_triggers.txt",
            "sb_nrp_boundary_demand_can_open",
        )
        selector = object_block(
            "common/scripted_effects/sb_zululand_settlement_effects.txt",
            "sb_nrp_select_boundary_initiator",
        )

        # NRP (and Crown-restored ZUL on that route) must be at peace, but a
        # global British or Natal war must not hold this regional demand forever.
        self.assertEqual(2, trigger.count("is_at_war = no"))
        self.assertNotIn("is_at_war = no", selector)
        self.assertIn("is_active_in_diplomatic_play = no", trigger)
        self.assertIn("is_active_in_diplomatic_play = no", selector)

    def test_direct_rebellion_boundary_targets_natal_without_changing_the_crown_route(self):
        path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        cutback = object_block(path, "sb_nrp_accept_boundary_cutback")
        goals = object_block(path, "sb_nrp_add_boundary_war_goals")
        launch = object_block(path, "sb_nrp_launch_boundary_confrontation")
        event = object_block(
            "events/sb_zululand_settlement_events.txt",
            "sb_zululand_settlement.230",
        )
        crown_event = object_block(
            "events/sb_zululand_settlement_events.txt",
            "sb_zululand_settlement.210",
        )
        notice = object_block(
            "events/sb_zululand_settlement_events.txt",
            "sb_zululand_settlement.231",
        )

        self.assertIn("sb_nrp_direct_annexation_rebellion_var", cutback)
        self.assertIn("country = c:NAL", cutback)
        self.assertIn("country = c:ZUL", cutback)
        for province in ("xE1E455", "x904EBE", "x9E9742"):
            self.assertIn(province, cutback)

        self.assertIn("type = annex_country", goals)
        self.assertIn("holder = c:NAL", goals)
        self.assertIn("target_country = c:NRP", goals)
        self.assertIn("holder = c:NRP", goals)
        self.assertIn("target_country = c:NAL", goals)
        self.assertIn("target_state = scope:sb_nrp_boundary_natal_state", goals)
        self.assertIn("sb_nrp_boundary_current_launch_authority = yes", launch)
        self.assertIn("sb_nrp_boundary_initiator_scope", launch)
        self.assertIn("set_variable = sb_nrp_boundary_launch_lease_var", launch)
        self.assertIn("target_country = c:TRN", launch)
        self.assertIn("target_country = c:NRP", launch)
        authority = object_block(
            "common/scripted_triggers/sb_zululand_settlement_triggers.txt",
            "sb_nrp_boundary_current_launch_authority",
        )
        self.assertIn("sb_nrp_direct_annexation_rebellion_var", authority)

        self.assertIn("sb_nrp_direct_annexation_rebellion_var", event)
        self.assertIn("sb_nrp_notify_natal_of_boundary_cutback = yes", event)
        self.assertIn("sb_nrp_notify_natal_of_boundary_cutback = yes", crown_event)
        self.assertIn("sb_nrp_refuse_boundary_demand = yes", event)
        self.assertIn("country_definition = cd:NAL", notice)
        self.assertIn("sb_nrp_boundary_cutback_notification_pending_var", notice)
        self.assertIn("sb_nrp_accept_boundary_cutback = yes", notice)
        self.assertIn("sb_nrp_seed_livestock_ranch = yes", cutback)

    def test_nieuwe_republiek_uses_the_supplied_flag(self):
        coa = object_block("common/coat_of_arms/coat_of_arms/sb_countries.txt", "NRP")
        flag = object_block("common/flag_definitions/sb_flag_definitions.txt", "NRP")
        self.assertIn('texture = "te_nrp_nieuwe_republiek_flag.tga"', coa)
        self.assertIn("coa = NRP", flag)
        self.assertTrue(
            (ROOT / "gfx/flags/source/Flag_of_Nieuwe_Republiek.svg").is_file()
        )
        self.assertTrue(
            (
                ROOT
                / "gfx/coat_of_arms/textured_emblems/te_nrp_nieuwe_republiek_flag.tga"
            ).is_file()
        )

    def test_nieuwe_republiek_has_a_distinct_sky_blue_map_colour(self):
        country = object_block(
            "common/country_definitions/zz_sb_southern_africa_country_definition_overrides.txt",
            "NRP",
        )
        self.assertIn("color = { 87 178 224 }", country)

    def test_shepstone_land_mechanics_follow_natal_government_law(self):
        amendment = object_block(
            "common/amendments/sb_amendments.txt", "amendment_sb_shepstone_system"
        )

        self.assertIn("tax_land_add = 0.03", amendment)
        self.assertNotIn("country_tax_income_add", amendment)
        for modifier in (
            "building_subsistence_output_mult = 0.30",
            "building_minimum_incorporated_subsistence_employment_add = 0.80",
            "state_minimum_incorporated_subsistence_arable_land_add = 0.15",
            "state_migration_pull_mult = -0.35",
        ):
            self.assertIn(modifier, amendment)
        self.assertNotIn(
            "sb_natal_shepstone_reserves",
            text("common/static_modifiers/sb_modifiers.txt"),
        )
        self.assertNotIn(
            "sb_natal_sync_shepstone_state_modifier",
            text("common/scripted_effects/sb_natal_interwar_effects.txt"),
        )


if __name__ == "__main__":
    unittest.main()
