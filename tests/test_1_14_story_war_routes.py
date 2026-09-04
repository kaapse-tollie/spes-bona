from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]

PHASE_A_PLAY_TYPES = {
    "dp_sb_griqualand_cap_revoke_claim_locked",
    "dp_sb_griqualand_cap_revoke_oranje_proxy_locked",
    "dp_sb_griqualand_oranje_revoke_cap_claim_locked",
}
PHASE_B_PLAY_TYPES = {
    "dp_sb_griqualand_cap_return_wbl_locked",
    "dp_sb_griqualand_oranje_return_wbl_locked",
    "dp_sb_griqualand_oranje_independent_return_wbl_proxy_locked",
}
ALIGNED_PROXY_PLAY_TYPE = "dp_sb_griqualand_oranje_return_wbl_proxy_locked"


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def uncommented(source: str) -> str:
    return re.sub(r"(?m)#.*$", "", source)


def object_block_from_source(source: str, name: str, context: str = "source") -> str:
    match = re.search(
        rf"^\s*(?:REPLACE:)?{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE
    )
    if match is None:
        raise AssertionError(f"missing {name} in {context}")
    return validate.extract_braced(source, match.start())


def object_block(path: str, name: str) -> str:
    return object_block_from_source(text(path), name, path)


def nested_blocks(source: str, name: str) -> list[str]:
    return [
        validate.extract_braced(source, match.start())
        for match in re.finditer(
            rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE
        )
    ]


def shortest_block_containing(source: str, name: str, *tokens: str) -> str:
    matches = [
        block
        for block in nested_blocks(source, name)
        if all(token in block for token in tokens)
    ]
    if not matches:
        raise AssertionError(f"missing {name} block containing {tokens!r}")
    return min(matches, key=len)


def primary_war_goal(play: str) -> str:
    match = re.search(r"(?m)^\s*war_goal\s*=\s*([A-Za-z0-9_]+)\s*$", play)
    if match is None:
        raise AssertionError("play has no primary war_goal")
    return match.group(1)


class StoryWarRouteTests(unittest.TestCase):
    def test_new_story_war_contract_files_have_required_utf8_bom(self):
        for path in (
            "common/war_goal_types/sb_story_war_goals.txt",
            "common/scripted_effects/sb_story_war_effects.txt",
            "localization/english/sb_war_goal_contracts_l_english.yml",
        ):
            with self.subTest(path=path):
                self.assertTrue(
                    (ROOT / path).read_bytes().startswith(b"\xef\xbb\xbf"),
                    f"{path} must keep the Clausewitz UTF-8 BOM",
                )

    def test_story_humiliation_is_hidden_assent_only_and_used_by_story_routes(self):
        goal = object_block(
            "common/war_goal_types/sb_story_war_goals.txt",
            "sb_story_humiliation",
        )
        settings = object_block_from_source(goal, "settings", "sb_story_humiliation")

        self.assertRegex(goal, r"(?m)^\s*kind\s*=\s*humiliation\s*$")
        self.assertRegex(goal, r"(?m)^\s*execution_priority\s*=\s*18\s*$")
        self.assertRegex(goal, r"(?m)^\s*contestion_type\s*=\s*control_any_target_country_state\s*$")
        self.assertRegex(goal, r"(?m)^\s*target_type\s*=\s*country\s*$")
        self.assertIn("require_target_be_part_of_war", settings)
        self.assertIn("assent_required", settings)
        self.assertIn("validate_conflicts_war_goals_all", settings)
        self.assertIn("possible = { always = no }", goal)
        self.assertNotIn("mirrored_wargoal", goal)
        self.assertNotIn("enforcement_progress", goal)

        expected_primaries = {
            "dp_sb_natal_crisis": "sb_story_humiliation",
            "dp_sb_martinus_humiliation": "sb_story_humiliation",
            "dp_sb_bechuanaland_warren_intervention_locked": "sb_story_humiliation",
            "dp_sb_bechuanaland_proxy_intervention_locked": "sb_story_humiliation",
            "dp_sb_nrp_boundary_confrontation": "sb_story_humiliation",
        }
        for play_name, expected in expected_primaries.items():
            with self.subTest(play=play_name):
                play = object_block(
                    "common/diplomatic_plays/sb_diplomatic_plays.txt", play_name
                )
                self.assertEqual(expected, primary_war_goal(play))

        story_sources = (
            "common/diplomatic_plays/sb_diplomatic_plays.txt",
            "events/sb_natal_crisis_events.txt",
            "events/sb_martinus_confederation_events.txt",
            "common/scripted_effects/sb_martinus_confederation_effects.txt",
            "common/scripted_effects/sb_bechuanaland_corridor_effects.txt",
            "common/scripted_effects/sb_zululand_settlement_effects.txt",
        )
        bare_humiliation = re.compile(
            r"\b(?:war_goal|type)\s*=\s*humiliation\b"
        )
        for path in story_sources:
            with self.subTest(path=path):
                self.assertIsNone(bare_humiliation.search(uncommented(text(path))))

    def test_story_humiliation_records_then_uses_one_idempotent_close_resolver(self):
        handlers_path = "common/on_actions/sb_diplomatic_play_on_action_handlers.txt"
        started = object_block(handlers_path, "sb_on_spes_bona_diplomatic_play_started")
        enforced = object_block(handlers_path, "sb_on_spes_bona_wargoal_enforced")
        back_down = object_block(handlers_path, "sb_on_spes_bona_diplo_play_back_down")
        war_end = object_block(handlers_path, "sb_on_spes_bona_war_end")
        resolver = object_block(
            "common/scripted_effects/sb_story_war_effects.txt",
            "sb_story_humiliation_resolve",
        )

        self.assertIn("scope:initiator ?=", started)
        story_goal = object_block(
            "common/war_goal_types/sb_story_war_goals.txt",
            "sb_story_humiliation",
        )
        self.assertIn(
            "on_enforced = { sb_story_humiliation_record_enforcement = yes }",
            story_goal,
        )
        self.assertNotIn("sb_martinus_create_presidential_union_with_ora = yes", enforced)
        self.assertNotIn("id = sb_natal_crisis.070", enforced)
        self.assertNotIn("id = sb_natal_crisis.080", enforced)
        self.assertLess(
            back_down.index("sb_story_humiliation_record_back_down = yes"),
            back_down.index("sb_story_humiliation_resolve = yes"),
        )
        self.assertIn("sb_story_humiliation_resolve = yes", war_end)

        for route in ("natal", "martinus"):
            with self.subTest(route=route):
                self.assertIn(
                    f"sb_{route}_story_initiator_demand_accepted_global_var", resolver
                )
                self.assertIn(
                    f"sb_{route}_story_target_demand_accepted_global_var", resolver
                )
                self.assertIn(f"sb_{route}_story_war_resolved_global_var", resolver)
        self.assertGreaterEqual(resolver.count("# 2:"), 2)
        self.assertGreaterEqual(resolver.count("# 1:"), 4)
        self.assertGreaterEqual(resolver.count("# 0:"), 2)

    def test_griqualand_claim_goals_are_assent_records_before_territorial_transfer(self):
        path = "common/war_goal_types/sb_griqualand_west_war_goals.txt"
        direct = object_block(path, "sb_griqualand_story_revoke_claim")
        proxy = object_block(path, "sb_revoke_oranje_griqualand_claim")
        transfer = object_block(path, "sb_return_oranje_griqualand")

        for name, goal in (
            ("direct", direct),
            ("proxy", proxy),
        ):
            with self.subTest(goal=name):
                settings = object_block_from_source(goal, "settings", name)
                self.assertRegex(goal, r"(?m)^\s*kind\s*=\s*custom\s*$")
                self.assertRegex(goal, r"(?m)^\s*execution_priority\s*=\s*80\s*$")
                self.assertIn("require_target_be_part_of_war", settings)
                self.assertIn("can_add_for_other_country", settings)
                self.assertIn("assent_required", settings)
                self.assertIn("possible = { always = no }", goal)
                self.assertIn(
                    "on_enforced = { sb_griqualand_record_claim_revocation = yes }",
                    goal,
                )
                self.assertNotIn("remove_claim", goal)
                self.assertNotIn("set_state_owner", goal)
                self.assertNotIn("mirrored_wargoal", goal)

        proxy_valid = object_block_from_source(proxy, "valid", "proxy record goal")
        self.assertIn("country_definition = cd:TRN", proxy_valid)
        self.assertIn("is_diplomatic_play_enemy_of = root", proxy_valid)
        self.assertIn("is_direct_subject_of = scope:target_country", proxy_valid)
        self.assertIn("sb_oranje_federated_into_trn_var", proxy_valid)
        self.assertNotIn("targets_enemy_claims", proxy)

        transfer_settings = object_block_from_source(
            transfer, "settings", "ORA proxy transfer goal"
        )
        self.assertRegex(transfer, r"(?m)^\s*execution_priority\s*=\s*70\s*$")
        self.assertIn("assent_required", transfer_settings)
        self.assertNotIn("mirrored_wargoal", transfer)
        self.assertIn("set_state_owner = c:ORA", transfer)
        self.assertLess(
            int(re.search(r"execution_priority\s*=\s*(\d+)", transfer).group(1)),
            int(re.search(r"execution_priority\s*=\s*(\d+)", direct).group(1)),
        )

        expected_primaries = {
            "dp_sb_griqualand_cap_revoke_claim_locked": "sb_griqualand_story_revoke_claim",
            "dp_sb_griqualand_cap_revoke_oranje_proxy_locked": "sb_revoke_oranje_griqualand_claim",
            "dp_sb_griqualand_oranje_revoke_cap_claim_locked": "sb_griqualand_story_revoke_claim",
            "dp_sb_griqualand_oranje_return_wbl_proxy_locked": "sb_return_oranje_griqualand",
            "dp_sb_griqualand_oranje_independent_return_wbl_proxy_locked": "sb_return_oranje_griqualand",
        }
        for play_name, expected in expected_primaries.items():
            with self.subTest(play=play_name):
                self.assertEqual(
                    expected,
                    primary_war_goal(
                        object_block(
                            "common/diplomatic_plays/sb_diplomatic_plays.txt",
                            play_name,
                        )
                    ),
                )

    def test_eight_planned_launchers_have_no_post_create_random_selector(self):
        launchers = (
            (
                "common/scripted_effects/sb_zululand_settlement_effects.txt",
                "sb_nrp_launch_boundary_confrontation",
            ),
            (
                "common/scripted_effects/sb_natal_interwar_effects.txt",
                "sb_natal_add_zulu_secession_war_goal",
            ),
            (
                "common/scripted_effects/sb_bechuanaland_corridor_effects.txt",
                "sb_bechuanaland_launch_direct_crisis",
            ),
            (
                "common/scripted_effects/sb_bechuanaland_corridor_effects.txt",
                "sb_bechuanaland_launch_proxy_crisis",
            ),
            (
                "common/scripted_effects/sb_bechuanaland_corridor_effects.txt",
                "sb_bechuanaland_launch_warren_direct_crisis",
            ),
            (
                "common/scripted_effects/sb_bechuanaland_corridor_effects.txt",
                "sb_bechuanaland_launch_warren_proxy_crisis",
            ),
            (
                "common/scripted_effects/sb_bechuanaland_corridor_effects.txt",
                "sb_bechuanaland_start_cap_sgo_annex_war",
            ),
            ("events/sb_griqualand_west_events.txt", "sb_griqualand_west.252"),
        )
        self.assertEqual(8, len(launchers))
        for path, name in launchers:
            with self.subTest(path=path, launcher=name):
                self.assertNotIn("random_diplomatic_play", object_block(path, name))

    def test_on_start_configuration_is_lease_and_identity_guarded(self):
        handlers = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_diplomatic_play_started",
        )
        dispatchers = {
            "sb_griqualand_configure_started_sequence_play",
            "sb_griqualand_configure_started_aligned_proxy_play",
            "sb_nrp_configure_started_boundary_play",
            "sb_natal_configure_started_zulu_secession_play",
            "sb_bechuanaland_configure_started_story_play",
        }
        for dispatcher in dispatchers:
            with self.subTest(dispatcher=dispatcher):
                self.assertEqual(1, handlers.count(f"{dispatcher} = yes"))

        configurations = (
            (
                "common/scripted_effects/sb_griqualand_west_effects.txt",
                "sb_griqualand_configure_started_sequence_play",
                "sb_griqualand_phase_a_launch_lease_var",
            ),
            (
                "common/scripted_effects/sb_griqualand_west_effects.txt",
                "sb_griqualand_configure_started_aligned_proxy_play",
                "sb_griqualand_aligned_proxy_launch_lease_var",
            ),
            (
                "common/scripted_effects/sb_zululand_settlement_effects.txt",
                "sb_nrp_configure_started_boundary_play",
                "sb_nrp_boundary_launch_lease_var",
            ),
            (
                "common/scripted_effects/sb_natal_interwar_effects.txt",
                "sb_natal_configure_started_zulu_secession_play",
                "sb_natal_zulu_secession_launch_lease_var",
            ),
        )
        for path, name, lease in configurations:
            with self.subTest(configurator=name):
                configuration = object_block(path, name)
                self.assertIn("is_diplomatic_play_type =", configuration)
                self.assertIn("scope:initiator ?=", configuration)
                self.assertIn("scope:target ?=", configuration)
                self.assertIn(lease, configuration)
                self.assertIn(f"remove_variable = {lease}", configuration)

        bechuanaland = object_block(
            "common/scripted_effects/sb_bechuanaland_corridor_effects.txt",
            "sb_bechuanaland_configure_started_story_play",
        )
        bechuanaland_contracts = {
            "sb_bechuanaland_direct_launch_lease_var": "dp_sb_bechuanaland_direct_intervention_locked",
            "sb_bechuanaland_proxy_launch_lease_var": "dp_sb_bechuanaland_proxy_intervention_locked",
            "sb_bechuanaland_warren_direct_launch_lease_var": "dp_sb_bechuanaland_warren_intervention_locked",
            "sb_bechuanaland_warren_proxy_launch_lease_var": "dp_sb_bechuanaland_warren_intervention_locked",
            "sb_bechuanaland_total_launch_lease_var": "dp_sb_bechuanaland_cap_sgo_return",
        }
        for lease, play_type in bechuanaland_contracts.items():
            with self.subTest(lease=lease):
                self.assertIn(lease, bechuanaland)
                self.assertIn(f"remove_variable = {lease}", bechuanaland)
                self.assertIn(f"is_diplomatic_play_type = {play_type}", bechuanaland)
        self.assertIn("scope:initiator ?=", bechuanaland)
        self.assertIn("scope:target ?=", bechuanaland)

        nrp_goals = object_block(
            "common/scripted_effects/sb_zululand_settlement_effects.txt",
            "sb_nrp_add_boundary_war_goals",
        )
        self.assertLess(
            nrp_goals.index("add_war_goal ="),
            nrp_goals.index("remove_war_goal ="),
        )
        self.assertIn("type = sb_story_humiliation", nrp_goals)

    def test_launch_leases_wrap_creation_and_have_explicit_failure_cleanup(self):
        path = "common/scripted_effects/sb_bechuanaland_corridor_effects.txt"
        bechuanaland_launchers = {
            "sb_bechuanaland_launch_direct_crisis": "sb_bechuanaland_direct_launch_lease_var",
            "sb_bechuanaland_launch_proxy_crisis": "sb_bechuanaland_proxy_launch_lease_var",
            "sb_bechuanaland_launch_warren_direct_crisis": "sb_bechuanaland_warren_direct_launch_lease_var",
            "sb_bechuanaland_launch_warren_proxy_crisis": "sb_bechuanaland_warren_proxy_launch_lease_var",
            "sb_bechuanaland_start_cap_sgo_annex_war": "sb_bechuanaland_total_launch_lease_var",
        }
        for launcher, lease in bechuanaland_launchers.items():
            with self.subTest(launcher=launcher):
                block = object_block(path, launcher)
                first_set = block.index(f"set_variable = {lease}")
                first_create = block.index("create_diplomatic_play", first_set)
                failure_clear = block.rindex(f"remove_variable = {lease}")
                self.assertLess(first_set, first_create)
                self.assertLess(first_create, failure_clear)
                self.assertIn("any_diplomatic_play", block)
                self.assertIn("sb_bechuanaland_crisis_creation_failed_var", block)

        nrp = object_block(
            "common/scripted_effects/sb_zululand_settlement_effects.txt",
            "sb_nrp_launch_boundary_confrontation",
        )
        self.assertLess(
            nrp.index("set_variable = sb_nrp_boundary_launch_lease_var"),
            nrp.index("create_diplomatic_play"),
        )
        self.assertIn("sb_nrp_boundary_creation_failed_var", nrp)

        secession_start = object_block(
            "common/on_actions/sb_natal_interwar_on_action_handlers.txt",
            "sb_on_natal_zulu_secession_start",
        )
        secession_finish = object_block(
            "common/scripted_effects/sb_natal_interwar_effects.txt",
            "sb_natal_add_zulu_secession_war_goal",
        )
        self.assertIn(
            "set_variable = sb_natal_zulu_secession_launch_lease_var",
            secession_start,
        )
        self.assertIn(
            "remove_variable = sb_natal_zulu_secession_launch_lease_var",
            secession_finish,
        )
        self.assertIn("sb_natal_zulu_secession_configuration_failed_var", secession_finish)

    def test_independent_wbl_route_runs_claim_phase_then_delayed_owner_phase(self):
        event = object_block(
            "events/sb_griqualand_west_events.txt", "sb_griqualand_west.254"
        )
        effects_path = "common/scripted_effects/sb_griqualand_west_effects.txt"
        begin = object_block(effects_path, "sb_griqualand_sequence_begin")
        phase_a = object_block(effects_path, "sb_griqualand_sequence_launch_phase_a")
        close_a = object_block(effects_path, "sb_griqualand_sequence_close_phase_a")
        queue_b = object_block(effects_path, "sb_griqualand_sequence_queue_phase_b")
        phase_b_event = object_block(
            "events/sb_griqualand_west_events.txt", "sb_griqualand_west.261"
        )
        phase_b = object_block(effects_path, "sb_griqualand_sequence_launch_phase_b")
        retry = object_block(
            effects_path, "sb_griqualand_sequence_phase_b_creation_failure"
        )

        self.assertEqual(1, event.count("sb_griqualand_sequence_begin = yes"))
        self.assertNotIn("create_diplomatic_play", event)
        self.assertIn("sb_griqualand_sequence_launch_phase_a = yes", begin)
        self.assertNotIn("sb_griqualand_sequence_launch_phase_b = yes", begin)

        for play_type in PHASE_A_PLAY_TYPES:
            self.assertIn(f"type = {play_type}", phase_a)
        for play_type in PHASE_B_PLAY_TYPES:
            self.assertNotIn(f"type = {play_type}", phase_a)
        self.assertIn("sb_griqualand_phase_a_launch_lease_var", phase_a)
        self.assertIn("any_diplomatic_play", phase_a)

        self.assertLess(
            close_a.index("sb_griqualand_apply_recorded_claim_revocations = yes"),
            close_a.index("sb_griqualand_sequence_queue_phase_b = yes"),
        )
        self.assertIn("sb_griqualand_advancing_claimant_scope", close_a)
        self.assertIn("is_subject = no", close_a)
        self.assertIn("p:x68B5E8.state.owner = c:WBL", close_a)
        self.assertIn("sb_griqualand_sequence_terminal_fallback = yes", close_a)

        self.assertIn("sb_griqualand_phase_b_pending_global_var", queue_b)
        self.assertIn("id = sb_griqualand_west.261 days = 1", queue_b)
        self.assertIn("sb_griqualand_phase_b_pending_global_var", phase_b_event)
        self.assertIn("sb_griqualand_sequence_launch_phase_b = yes", phase_b_event)
        self.assertNotIn("sb_griqualand_west_grant_oranje_claim", phase_b_event + phase_b)

        for play_type in PHASE_B_PLAY_TYPES:
            self.assertIn(f"type = {play_type}", phase_b)
        for play_type in PHASE_A_PLAY_TYPES:
            self.assertNotIn(f"type = {play_type}", phase_b)
        self.assertIn("sb_griqualand_phase_b_launch_lease_var", phase_b)
        self.assertIn("is_subject = no", phase_b)
        self.assertIn("p:x68B5E8.state.owner = c:WBL", phase_b)
        self.assertIn("id = sb_griqualand_west.261 days = 7", retry)
        self.assertIn("sb_griqualand_phase_b_retry_used_global_var", retry)
        self.assertIn("sb_griqualand_sequence_terminal_fallback = yes", retry)

    def test_griqualand_phase_guards_watchdog_and_close_lists_are_complete(self):
        effects_path = "common/scripted_effects/sb_griqualand_west_effects.txt"
        early_finalize = object_block(
            effects_path, "sb_griqualand_west_try_finalize_refusal_contest"
        )
        watchdog = object_block(effects_path, "sb_griqualand_sequence_watchdog")
        cleanup = object_block(effects_path, "sb_griqualand_sequence_cleanup")
        on_actions = object_block(
            "common/on_actions/sb_on_actions.txt", "on_monthly_pulse_country"
        )
        handlers_path = "common/on_actions/sb_diplomatic_play_on_action_handlers.txt"
        back_down = object_block(handlers_path, "sb_on_spes_bona_diplo_play_back_down")
        war_end = object_block(handlers_path, "sb_on_spes_bona_war_end")

        self.assertIn(
            "NOT = { has_global_variable = sb_griqualand_sequence_active_global_var }",
            early_finalize,
        )
        self.assertIn("sb_on_griqualand_sequence_watchdog_monthly", on_actions)
        self.assertIn("any_diplomatic_play", watchdog)
        self.assertIn("any_scope_war", watchdog)
        self.assertIn("sb_griqualand_sequence_close_phase_a = yes", watchdog)
        self.assertIn("sb_griqualand_sequence_close_phase_b = yes", watchdog)

        routed_types = PHASE_A_PLAY_TYPES | PHASE_B_PLAY_TYPES | {ALIGNED_PROXY_PLAY_TYPE}
        for play_type in routed_types:
            with self.subTest(play_type=play_type):
                self.assertIn(f"is_diplomatic_play_type = {play_type}", back_down)
                self.assertIn(f"is_diplomatic_play_type = {play_type}", war_end)

        for flag in (
            "sb_griqualand_sequence_active_global_var",
            "sb_griqualand_sequence_generation_global_var",
            "sb_griqualand_phase_a_pending_global_var",
            "sb_griqualand_phase_a_active_global_var",
            "sb_griqualand_phase_a_close_handled_global_var",
            "sb_griqualand_phase_b_pending_global_var",
            "sb_griqualand_phase_b_event_pending_global_var",
            "sb_griqualand_phase_b_active_global_var",
            "sb_griqualand_phase_b_retry_used_global_var",
            "sb_griqualand_cap_claim_revocation_accepted_global_var",
            "sb_griqualand_boer_claim_revocation_accepted_global_var",
        ):
            with self.subTest(cleanup_flag=flag):
                self.assertIn(f"remove_global_variable = {flag}", cleanup)
        self.assertIn("destroy_container = yes", cleanup)
        self.assertIn("sb_griqualand_clear_launch_leases = yes", cleanup)

    def test_retired_griqualand_play_has_no_definition_handler_or_localization(self):
        retired = "dp_sb_griqualand_revoke_claim"
        for path in (
            "common/diplomatic_plays/sb_diplomatic_plays.txt",
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "localization/english/sb_griqualand_west_l_english.yml",
        ):
            with self.subTest(path=path):
                self.assertNotIn(retired, text(path))

    def test_griqualand_025_accepts_and_executes_the_oranje_annex_route(self):
        event = object_block(
            "events/sb_griqualand_west_events.txt", "sb_griqualand_west.025"
        )
        trigger = shortest_block_containing(
            event, "trigger", "country_definition = cd:WBL", "any_scope_state"
        )
        annex = shortest_block_containing(
            event,
            "if",
            "has_variable = sb_griqualand_west_oranje_annexation_demand_var",
            "annex = root",
        )

        self.assertIn("sb_griqualand_west_oranje_annexation_demand_var", trigger)
        self.assertIn("c:ORA ?=", annex)
        self.assertLess(
            annex.index("annex = root"),
            annex.index("sb_kimberley_finalize_direct_boer_route = yes"),
        )
        self.assertNotIn("sb_kimberley_finalize_ora_puppet_route = yes", annex)

    def test_zululand_owner_change_guard_clears_only_transient_story_leases(self):
        registrations = object_block(
            "common/on_actions/sb_on_actions.txt", "on_state_owner_change"
        )
        handler = object_block(
            "common/on_actions/sb_regional_on_action_handlers.txt",
            "sb_on_zululand_incorporation_state_owner_change",
        )
        incorporation_handler = object_block(
            "common/on_actions/sb_regional_on_action_handlers.txt",
            "sb_on_zululand_state_incorporation",
        )
        completion = object_block(
            "events/sb_zululand_settlement_events.txt",
            "sb_zululand_settlement.130",
        )

        self.assertIn("sb_on_zululand_incorporation_state_owner_change", registrations)
        self.assertIn("state_region = s:STATE_ZULULAND", handler)
        self.assertIn("NOT = { owner ?= { country_definition = cd:NAL } }", handler)
        for lease in (
            "sb_zululand_incorporation_requested_var",
            "sb_zululand_incorporation_started_var",
            "sb_zululand_post_annex_incorporation_pending_var",
            "sb_zululand_incorporation_complete_pending_var",
        ):
            with self.subTest(transient=lease):
                self.assertIn(f"remove_variable = {lease}", handler)
        self.assertNotIn(
            "remove_variable = sb_zululand_incorporation_complete_var", handler
        )

        for route_marker in (
            "sb_zululand_incorporation_requested_var",
            "sb_zululand_incorporation_started_var",
            "sb_zululand_direct_natal_administration_var",
            "sb_zululand_zibhebhu_victory_var",
            "sb_zululand_crown_restored_victory_var",
        ):
            self.assertIn(route_marker, incorporation_handler)
            self.assertIn(route_marker, completion)
        self.assertGreaterEqual(completion.count("owner = root"), 2)
        self.assertGreaterEqual(completion.count("is_incorporated = yes"), 2)
        self.assertIn("sb_zululand_incorporation_complete_pending_var", completion)

    def test_natal_neutral_outcome_preserves_followup_without_triumph_rewards(self):
        event = object_block(
            "events/sb_natal_crisis_events.txt", "sb_natal_crisis.081"
        )
        resolver = object_block(
            "common/scripted_effects/sb_story_war_effects.txt",
            "sb_story_humiliation_resolve",
        )

        for token in (
            "set_variable = sb_zulu_blood_river_resolved_var",
            "set_variable = sb_zulu_port_natal_raid_available_var",
            "sb_zulu_maybe_open_swazi_question = yes",
        ):
            self.assertIn(token, event)
        for exclusive_reward in (
            "sb_zulu_natal_triumph",
            "sb_dingane_triumphant",
            "add_trait = brave",
            "sb_desc_firearms_gain_10",
            "sb_zulu_dynasty_gain_stability_20",
            "sb_zulu_apply_blood_river_victory",
            "sb_zulu_mark_swazi_question_after_blood_river_win",
        ):
            with self.subTest(exclusive_reward=exclusive_reward):
                self.assertNotIn(exclusive_reward, event)
        self.assertEqual(2, resolver.count("id = sb_natal_crisis.081"))

    def test_bst_backdown_and_timer_guards_do_not_award_an_aggressor_loss(self):
        path = "common/on_actions/sb_bst_on_actions.txt"
        back_down = object_block(path, "sb_on_bst_diplo_play_back_down")
        enforced = object_block(path, "sb_on_bst_wargoal_enforced")
        war_end = object_block(path, "sb_on_bst_war_end")

        self.assertNotIn("sb_ora_annexed_bst_var", back_down)
        rejected = shortest_block_containing(
            back_down, "if", "sb_bst_annexation_backdown_rejected_var"
        )
        self.assertIn("scope:actor ?=", rejected)
        self.assertIn("sb_bst_oranje_frontier_actor = yes", rejected)
        self.assertIn("scope:target ?= { country_definition = cd:BST }", rejected)

        self.assertIn("sb_bst_story_goal_accepted_pending_var", enforced)
        for terminal_mutation in (
            "sb_ora_annexed_bst_var",
            "remove_variable = sb_bst_cap_annexation_crisis_var",
            "sb_bst_restore_gbr_protectorate = yes",
            "sb_bst_return_to_gbr_as_puppet = yes",
        ):
            with self.subTest(terminal_mutation=terminal_mutation):
                self.assertNotIn(terminal_mutation, enforced)

        self.assertIn("NOT = { is_subject_of = c:CAP }", war_end)
        self.assertIn("sb_bst_gun_war_resolution_guard_var", war_end)
        self.assertIn("sb_bst_restore_gbr_protectorate = yes", war_end)



if __name__ == "__main__":
    unittest.main()
