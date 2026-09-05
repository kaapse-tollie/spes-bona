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
        recorder = object_block(
            "common/scripted_effects/sb_story_war_effects.txt",
            "sb_story_humiliation_record_enforcement",
        )

        self.assertIn("scope:initiator ?=", started)
        self.assertEqual(
            3, recorder.count("NOT = { exists = scope:enforced_by_timer }")
        )
        self.assertNotIn("sb_story_humiliation_timer_seen_global_var", recorder)
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

    def test_martinus_launcher_uses_preflight_lease_and_exact_on_start_root(self):
        effect_launcher = object_block(
            "common/scripted_effects/sb_martinus_confederation_effects.txt",
            "sb_martinus_force_pretorius_standoff",
        )
        event_launcher = object_block(
            "events/sb_martinus_confederation_events.txt",
            "sb_martinus_confederation.050",
        )
        started = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_diplomatic_play_started",
        )
        story_effects = text("common/scripted_effects/sb_story_war_effects.txt")

        self.assertNotIn("random_diplomatic_play", effect_launcher)
        self.assertIn("sb_martinus_story_generation_scope", effect_launcher)
        self.assertIn(
            "set_variable = { name = sb_martinus_story_generation_scope value = scope:sb_martinus_coercive_receipt_scope }",
            effect_launcher,
        )
        self.assertIn("sb_martinus_story_launch_lease_var", effect_launcher)
        self.assertIn("any_diplomatic_play", effect_launcher)
        self.assertIn("initiator = root target = c:ORA", effect_launcher)
        self.assertIn(
            "is_diplomatic_play_type = dp_sb_martinus_humiliation", effect_launcher
        )
        self.assertIn("create_diplomatic_play =", effect_launcher)
        self.assertNotIn("random_diplomatic_play", event_launcher)
        self.assertEqual(1, event_launcher.count("sb_martinus_force_pretorius_standoff = yes"))
        self.assertNotIn("sb_martinus_story_launch_lease_var", event_launcher)

        config = shortest_block_containing(
            started,
            "if",
            "dp_sb_martinus_humiliation",
            "sb_martinus_story_launch_lease_var",
            "name = sb_martinus_story_play_scope value = root",
        )
        self.assertIn("scope:initiator ?=", config)
        self.assertIn("scope:target ?=", config)
        self.assertIn("add_war_goal", config)
        self.assertIn("holder = scope:target", config)
        self.assertIn("target_country = scope:initiator", config)
        self.assertIn("add_target_backers = { c:LYD }", config)
        self.assertIn("add_target_backers = { c:ZPB }", config)
        self.assertIn("add_target_backers = { c:NAL }", config)
        self.assertIn("remove_variable = sb_martinus_story_launch_lease_var", config)
        self.assertIn("remove_variable = sb_martinus_story_generation_scope", effect_launcher)

        self.assertGreaterEqual(
            story_effects.count("var:sb_martinus_story_play_scope = root"), 2
        )
        self.assertIn(
            "var:sb_martinus_story_play_scope = scope:diplomatic_play",
            story_effects,
        )
        clear = object_block_from_source(
            story_effects,
            "sb_story_humiliation_clear_martinus_state",
            "story effects",
        )
        self.assertIn("remove_variable = sb_martinus_story_play_scope", clear)

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

        live_routes = (
            text("events/sb_griqualand_west_events.txt")
            + text("common/on_actions/sb_diplomatic_play_on_action_handlers.txt")
            + text("common/scripted_effects/sb_story_war_effects.txt")
        )
        for obsolete_trace in (
            "sb_frontier_timer_enforcement_seen_global_var",
            "sb_griqualand_aligned_proxy_creation_failed_global_var",
            "sb_griqualand_aligned_proxy_launch_refused_global_var",
        ):
            with self.subTest(obsolete_trace=obsolete_trace):
                self.assertNotIn(obsolete_trace, live_routes)

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
        self.assertIn("sb_griqualand_phase_b_authority_is_valid = yes", phase_b)
        self.assertIn("sb_griqualand_phase_b_authority_is_launchable = yes", phase_b)
        self.assertEqual(3, phase_b.count("NOT = { any_diplomatic_play = {"))
        self.assertIn("sb_griqualand_phase_b_creation_failed_global_var", retry)
        self.assertIn(
            "remove_global_variable = sb_griqualand_phase_b_event_pending_global_var",
            retry,
        )
        self.assertIn("sb_griqualand_clear_launch_leases = yes", retry)
        self.assertNotIn("trigger_event", retry)
        self.assertNotIn("sb_griqualand_sequence_terminal_fallback = yes", retry)

    def test_griqualand_records_and_closes_only_the_bound_phase_generation(self):
        effects_path = "common/scripted_effects/sb_griqualand_west_effects.txt"
        recorder = object_block(effects_path, "sb_griqualand_record_claim_revocation")
        apply_records = object_block(
            effects_path, "sb_griqualand_apply_recorded_claim_revocations"
        )
        configure = object_block(
            effects_path, "sb_griqualand_configure_started_sequence_play"
        )
        queue_b = object_block(effects_path, "sb_griqualand_sequence_queue_phase_b")
        close = object_block(effects_path, "sb_griqualand_west_close_routed_play")
        handlers_path = "common/on_actions/sb_diplomatic_play_on_action_handlers.txt"
        back_down = object_block(handlers_path, "sb_on_spes_bona_diplo_play_back_down")
        war_end = object_block(handlers_path, "sb_on_spes_bona_war_end")

        self.assertIn("NOT = { exists = scope:enforced_by_timer }", recorder)
        self.assertIn(
            "var:sb_griqualand_sequence_play_scope = scope:diplomatic_play",
            recorder,
        )
        self.assertIn("sb_griqualand_sequence_play_generation_var = 1", recorder)
        self.assertIn("sb_griqualand_sequence_play_generation_var = 2", recorder)

        # Claim removals are individually idempotent. A one-shot global guard
        # would suppress a new WBL counter-demand recorded during Phase B.
        self.assertNotIn("sb_griqualand_claim_revocations_applied_global_var", apply_records)
        self.assertGreaterEqual(apply_records.count("has_claim = s:STATE_GRIQUALAND_WEST"), 4)
        self.assertGreaterEqual(apply_records.count("remove_claim ="), 4)

        self.assertEqual(8, configure.count("name = sb_griqualand_sequence_play_scope"))
        self.assertEqual(3, configure.count("name = sb_griqualand_sequence_play_generation_var value = 1"))
        self.assertEqual(1, configure.count("name = sb_griqualand_sequence_play_generation_var value = 2"))
        self.assertIn(
            "name = sb_griqualand_sequence_generation_global_var value = 2", queue_b
        )
        self.assertIn("destroy_container = yes", queue_b)
        self.assertIn(
            "remove_global_variable = sb_griqualand_sequence_play_scope_global_var", queue_b
        )

        for source in (close, back_down, war_end):
            with self.subTest(source=source[:50]):
                self.assertIn("var:sb_griqualand_sequence_play_scope = root", source)
                self.assertIn("var:sb_griqualand_sequence_play_generation_var = 1", source)
                self.assertIn("var:sb_griqualand_sequence_play_generation_var = 2", source)

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
        self.assertNotIn("any_diplomatic_play", watchdog)
        self.assertNotIn("any_scope_war", watchdog)
        self.assertEqual(
            2, watchdog.count("has_variable = sb_griqualand_sequence_play_scope")
        )
        self.assertEqual(
            2, watchdog.count("has_variable = sb_griqualand_sequence_play_generation_var")
        )
        self.assertIn("sb_griqualand_phase_b_authority_is_valid = yes", watchdog)
        self.assertIn("sb_griqualand_phase_b_authority_is_launchable = yes", watchdog)
        self.assertIn("var:sb_griqualand_sequence_play_generation_var = 1", watchdog)
        self.assertIn("var:sb_griqualand_sequence_play_generation_var = 2", watchdog)
        self.assertIn("sb_griqualand_sequence_close_phase_a = yes", watchdog)
        self.assertIn("sb_griqualand_sequence_close_phase_b = yes", watchdog)
        self.assertIn("id = sb_griqualand_west.261 days = 1", watchdog)
        self.assertIn(
            "NOT = { has_global_variable = sb_griqualand_phase_b_event_pending_global_var }",
            watchdog,
        )

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

    def test_retired_249_event_keeps_only_documented_reviewed_archive_prose(self):
        events = text("events/sb_griqualand_west_events.txt")
        localization = text("localization/english/sb_griqualand_west_l_english.yml")
        evidence = text("Docs/compatibility/1_14_0_open_beta_1_rebase.md")

        self.assertNotRegex(events, r"(?m)^\s*sb_griqualand_west\.249\s*=\s*\{")
        for suffix in ("t", "d", "f", "a"):
            self.assertIn(f"sb_griqualand_west.249.{suffix}:0", localization)
        marker_index = localization.rfind(
            "# ### REVIEWED ###", 0, localization.index("sb_griqualand_west.249.t:0")
        )
        self.assertGreaterEqual(marker_index, 0)
        self.assertIn("byte-for-byte", evidence)
        self.assertIn("sb_griqualand_west.249", evidence)
        self.assertIn("sb_story_war_effects.txt", evidence)

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
            event, "trigger", "sb_griqualand_ingress_political_authority"
        )
        annex = shortest_block_containing(
            event,
            "if",
            "has_variable = sb_griqualand_west_oranje_annexation_demand_var",
            "annex = root",
        )

        self.assertIn("sb_griqualand_ingress_political_authority = yes", trigger)
        self.assertIn("has_global_variable = sb_griqualand_ingress_delivery_pending_global_var", trigger)
        self.assertIn("has_variable = sb_griqualand_ingress_delivery_queued_var", trigger)
        self.assertNotIn("any_scope_state", trigger)
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
        self.assertEqual(2, resolver.count("sb_natal_story_begin_terminal_zulu_neutral = yes"))

    def test_blood_river_terminal_outcomes_use_bound_receipts_and_recover_delivery(self):
        effects_path = "common/scripted_effects/sb_story_war_effects.txt"
        events_path = "events/sb_natal_crisis_events.txt"
        triggers_path = "common/scripted_triggers/sb_natal_interwar_triggers.txt"
        effects = text(effects_path)
        resolver = object_block(effects_path, "sb_story_humiliation_resolve")
        watchdog = object_block(events_path, "sb_natal_crisis.098")

        for begin, result, event_id in (
            ("sb_natal_story_begin_terminal_ora_victory", "sb_natal_terminal_outcome_ora_victory_var", ".070"),
            ("sb_natal_story_begin_terminal_zulu_victory", "sb_natal_terminal_outcome_zulu_victory_var", ".080"),
            ("sb_natal_story_begin_terminal_zulu_neutral", "sb_natal_terminal_outcome_zulu_neutral_var", ".081"),
        ):
            with self.subTest(result=result):
                receipt = object_block(effects_path, begin)
                self.assertIn("create_container", receipt)
                self.assertIn("sb_natal_terminal_outcome_state", receipt)
                self.assertIn(result, receipt)
                self.assertIn("sb_natal_terminal_recipient_scope", receipt)
                self.assertIn("sb_natal_terminal_counterparty_scope", receipt)
                self.assertIn("sb_natal_story_requeue_terminal_outcome = yes", receipt)
                self.assertIn(f"sb_natal_crisis{event_id}", text(events_path))

        queue = object_block(effects_path, "sb_natal_story_requeue_terminal_outcome")
        recover = object_block(effects_path, "sb_natal_story_recover_terminal_outcome")
        consume = object_block(effects_path, "sb_natal_story_consume_terminal_outcome")
        clear = object_block(effects_path, "sb_natal_story_clear_terminal_outcome")
        self.assertIn("days = 20", queue)
        self.assertIn("id = sb_natal_crisis.070", queue)
        self.assertIn("id = sb_natal_crisis.080", queue)
        self.assertIn("id = sb_natal_crisis.081", queue)
        self.assertIn("sb_natal_terminal_outcome_popup_receipt_var", recover)
        self.assertIn("is_country_alive = yes", recover)
        self.assertIn("sb_natal_terminal_outcome_received_var", consume)
        self.assertIn("sb_natal_terminal_recipient_scope", consume)
        self.assertIn("sb_natal_terminal_counterparty_scope", consume)
        self.assertGreaterEqual(2, consume.count("remove_variable = sb_natal_terminal_outcome_scope"))
        self.assertIn("destroy_container = yes", consume)
        self.assertIn("sb_natal_terminal_recipient_scope", clear)
        self.assertIn("sb_natal_terminal_counterparty_scope", clear)
        self.assertIn("sb_natal_story_recover_terminal_outcome = yes", watchdog)
        self.assertIn("sb_natal_terminal_outcome_scope", watchdog)

        for event_id, authority in (
            (".070", "sb_natal_story_terminal_ora_victory_event_authority"),
            (".080", "sb_natal_story_terminal_zulu_victory_event_authority"),
            (".081", "sb_natal_story_terminal_zulu_neutral_event_authority"),
        ):
            with self.subTest(event=event_id):
                event = object_block(events_path, f"sb_natal_crisis{event_id}")
                self.assertIn("sb_natal_terminal_outcome_delivery_queued_var", event)
                self.assertIn("sb_natal_terminal_outcome_popup_receipt_var months = 4", event)
                self.assertIn(authority, event)
                self.assertIn("sb_natal_story_consume_terminal_outcome = yes", event)
                self.assertNotIn("country_definition = cd:", event)

        for authority, result in (
            ("sb_natal_story_terminal_ora_victory_event_authority", "sb_natal_terminal_outcome_ora_victory_var"),
            ("sb_natal_story_terminal_zulu_victory_event_authority", "sb_natal_terminal_outcome_zulu_victory_var"),
            ("sb_natal_story_terminal_zulu_neutral_event_authority", "sb_natal_terminal_outcome_zulu_neutral_var"),
        ):
            with self.subTest(authority=authority):
                trigger = object_block(triggers_path, authority)
                self.assertIn(result, trigger)
                self.assertIn("sb_natal_terminal_recipient_scope = root", trigger)
                self.assertIn("sb_natal_terminal_outcome_popup_receipt_var", trigger)

        self.assertNotIn("scope:initiator", resolver)
        self.assertNotIn("scope:target", resolver)
        self.assertNotIn("id = sb_natal_crisis.070", resolver)
        self.assertNotIn("id = sb_natal_crisis.080", resolver)
        self.assertNotIn("id = sb_natal_crisis.081", resolver)
        self.assertEqual(2, resolver.count("sb_natal_story_begin_terminal_zulu_neutral = yes"))
        self.assertIn("sb_natal_story_begin_terminal_ora_victory = yes", resolver)
        self.assertIn("sb_natal_story_begin_terminal_zulu_victory = yes", resolver)


    def test_blood_river_generation_cleanup_uses_saved_actors_after_retag(self):
        effects_path = "common/scripted_effects/sb_story_war_effects.txt"
        triggers_path = "common/scripted_triggers/sb_natal_interwar_triggers.txt"
        events_path = "events/sb_natal_crisis_events.txt"

        guns_begin = object_block(effects_path, "sb_natal_story_begin_guns_bargain_generation")
        guns_clear = object_block(effects_path, "sb_natal_story_clear_guns_bargain_receipt")
        refusal_begin = object_block(effects_path, "sb_natal_story_begin_refusal_generation")
        refusal_clear = object_block(effects_path, "sb_natal_story_clear_refusal_generation")
        launch_clear = object_block(effects_path, "sb_natal_story_clear_launch_reservation")
        recover = object_block(effects_path, "sb_natal_story_recover_generation")
        failed_create = object_block(effects_path, "sb_natal_story_begin_exact_launch")

        for begin, clear, actor, counterparty, generation, queued in (
            (
                guns_begin,
                guns_clear,
                "sb_natal_guns_bargain_generation_actor_scope",
                "sb_natal_guns_bargain_generation_counterparty_scope",
                "sb_natal_guns_bargain_generation_scope",
                "sb_natal_guns_bargain_delivery_queued_var",
            ),
            (
                refusal_begin,
                refusal_clear,
                "sb_natal_refusal_generation_actor_scope",
                "sb_natal_refusal_generation_counterparty_scope",
                "sb_natal_refusal_generation_scope",
                "sb_natal_refusal_delivery_queued_var",
            ),
        ):
            with self.subTest(generation=generation):
                self.assertIn(actor, begin)
                self.assertIn(counterparty, begin)
                self.assertIn(actor, clear)
                self.assertIn(counterparty, clear)
                self.assertIn(f"remove_variable = {generation}", clear)
                self.assertIn(f"remove_variable = {queued}", clear)
                self.assertNotIn("c:ZUL", uncommented(clear))
                self.assertNotIn("c:ORA", uncommented(clear))

        for token in (
            "sb_natal_guns_bargain_generation_actor_scope",
            "sb_natal_guns_bargain_generation_counterparty_scope",
            "sb_natal_refusal_generation_actor_scope",
            "sb_natal_refusal_generation_counterparty_scope",
            "sb_natal_story_launch_pending_var",
            "sb_natal_story_launch_retry_queued_var",
            "sb_natal_story_launch_lease_var",
        ):
            with self.subTest(token=token):
                self.assertIn(token, launch_clear)
        self.assertNotIn("c:ZUL", uncommented(launch_clear))
        self.assertNotIn("c:ORA", uncommented(launch_clear))

        # The original Oranje scope owns route-open state in both cancellations;
        # the guns marker remains exact to the saved generation actors.
        guns_ora = guns_clear[
            guns_clear.index("var:sb_natal_guns_bargain_generation_counterparty_scope"):
        ]
        refusal_ora = refusal_clear[
            refusal_clear.index("var:sb_natal_refusal_generation_actor_scope"):
        ]
        for scope in (guns_ora, refusal_ora):
            self.assertIn("remove_variable = sb_natal_diplomacy_started_var", scope)
        self.assertIn("remove_variable = sb_natal_guns_bargain_war_var", guns_ora)

        watchdog = object_block(events_path, "sb_natal_crisis.098")
        guns_fallback = shortest_block_containing(
            watchdog,
            "if",
            "NOT = { container_exists = sb_natal_guns_bargain_generation_state }",
            "sb_natal_guns_bargain_war_var",
            "sb_natal_diplomacy_started_var",
        )
        refusal_fallback = shortest_block_containing(
            watchdog,
            "if",
            "NOT = { container_exists = sb_natal_refusal_generation_state }",
            "sb_natal_guns_bargain_war_var",
            "sb_natal_diplomacy_started_var",
        )
        for fallback, generation in (
            (guns_fallback, "sb_natal_guns_bargain_generation_scope"),
            (refusal_fallback, "sb_natal_refusal_generation_scope"),
        ):
            with self.subTest(fallback=generation):
                self.assertIn(f"limit = {{ has_variable = {generation} }}", fallback)
                self.assertLess(
                    fallback.index(f"limit = {{ has_variable = {generation} }}"),
                    fallback.index("remove_variable = sb_natal_diplomacy_started_var"),
                )
                self.assertNotIn("c:ZUL", uncommented(fallback))
                self.assertNotIn("c:ORA", uncommented(fallback))

        # Both watchdog invalidation and failed creation reach the saved-scope
        # cleanup functions, rather than leaving a retagged actor's receipt.
        self.assertIn("sb_natal_story_clear_guns_bargain_generation = yes", recover)
        self.assertIn("sb_natal_story_clear_refusal_generation = yes", recover)
        self.assertIn("sb_natal_story_clear_guns_bargain_generation = yes", failed_create)
        self.assertIn("sb_natal_story_clear_refusal_generation = yes", failed_create)

        # Terminal delivery deliberately does the opposite: its saved recipient
        # identity is tag-agnostic, so a surviving SAF/retag successor can act.
        authority = object_block(
            triggers_path, "sb_natal_story_terminal_ora_victory_event_authority"
        )
        self.assertIn("sb_natal_terminal_recipient_scope = root", authority)
        self.assertNotIn("country_definition", authority)


    def test_klip_routes_use_exact_play_leases_and_route_local_cleanup(self):
        path = "common/scripted_effects/sb_klip_river_county_effects.txt"
        secession = object_block(path, "sb_klip_river_start_secession_play")
        punitive = object_block(path, "sb_klip_river_start_punitive_play")
        configure = object_block(path, "sb_klip_river_configure_started_play")
        enforced = object_block(path, "sb_klip_river_handle_wargoal_enforced")
        back_down = object_block(path, "sb_klip_river_handle_backdown")
        war_end = object_block(path, "sb_klip_river_handle_war_end")
        started = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_diplomatic_play_started",
        )

        for launcher, lease in (
            (secession, "sb_klip_river_secession_launch_lease_var"),
            (punitive, "sb_klip_river_punitive_launch_lease_var"),
        ):
            self.assertNotIn("random_diplomatic_play", launcher)
            self.assertIn("any_diplomatic_play", launcher)
            self.assertLess(launcher.index(lease), launcher.index("create_diplomatic_play"))
            self.assertGreater(launcher.rindex(lease), launcher.index("create_diplomatic_play"))

        self.assertEqual(1, started.count("sb_klip_river_configure_started_play = yes"))
        for token in (
            "scope:initiator ?=",
            "scope:target ?=",
            "sb_klip_river_secession_launch_lease_var",
            "sb_klip_river_punitive_launch_lease_var",
            "name = sb_klip_river_secession_play_scope value = root",
            "name = sb_klip_river_punitive_play_scope value = root",
            "holder = c:ZUL",
            "target_country = c:NAL",
        ):
            self.assertIn(token, configure)

        self.assertIn(
            "var:sb_klip_river_secession_play_scope = scope:diplomatic_play",
            enforced,
        )
        self.assertIn(
            "var:sb_klip_river_punitive_play_scope = scope:diplomatic_play",
            enforced,
        )
        self.assertGreaterEqual(
            back_down.count("var:sb_klip_river_secession_play_scope = root"), 2
        )
        self.assertGreaterEqual(
            back_down.count("var:sb_klip_river_punitive_play_scope = root"), 2
        )
        self.assertIn("scope:actor ?= { country_definition = cd:ZUL }", war_end)
        self.assertIn("scope:actor ?= { country_definition = cd:NAL }", war_end)
        self.assertIn("var:sb_klip_river_secession_play_scope = root", war_end)
        self.assertIn("var:sb_klip_river_punitive_play_scope = root", war_end)
        self.assertIn("sb_klip_river_clear_secession_runtime = yes", war_end)
        self.assertIn("sb_klip_river_clear_punitive_runtime = yes", war_end)
        self.assertIn("else = { c:NAL ?= { sb_klip_river_finalize_secession_white_peace = yes } }", war_end)

    def test_klip_held_deliveries_bind_generation_and_freeze_state_footprints(self):
        effects_path = "common/scripted_effects/sb_klip_river_county_effects.txt"
        events_path = "events/sb_klip_river_county_events.txt"
        triggers_path = "common/scripted_triggers/sb_klip_river_county_triggers.txt"
        secession_queue = object_block(effects_path, "sb_klip_river_queue_secession_delivery")
        punitive_queue = object_block(effects_path, "sb_klip_river_queue_punitive_delivery")
        configure = object_block(effects_path, "sb_klip_river_configure_started_play")
        secession_event = object_block(events_path, "sb_klip_river_county.050")
        punitive_event = object_block(events_path, "sb_klip_river_county.060")
        housekeeping = object_block(effects_path, "sb_klip_river_county_monthly_housekeeping")
        triggers = text(triggers_path)

        for queue, generation, receipt in (
            (secession_queue, "sb_klip_river_secession_generation_scope", "sb_klip_river_secession_receipt_scope"),
            (punitive_queue, "sb_klip_river_punitive_generation_scope", "sb_klip_river_punitive_receipt_scope"),
        ):
            self.assertIn(generation, queue)
            self.assertIn("trigger_event", queue)
            self.assertIn(receipt, triggers)

        for event, bound, permanent in (
            (secession_event, "sb_klip_river_secession_bound_delivery_receipt", "sb_klip_river_secession_delivery_permanently_invalid"),
            (punitive_event, "sb_klip_river_punitive_bound_delivery_receipt", "sb_klip_river_punitive_delivery_permanently_invalid"),
        ):
            self.assertIn(f"trigger = {{ {bound} = yes", event)
            self.assertIn(f"NOT = {{ {permanent} = yes }}", event)
            self.assertIn(f"trigger = {{ {permanent} = yes }}", event)
            self.assertIn(f"NOT = {{ {bound} = yes }}", event)

        self.assertIn("target_state = scope:sb_klip_river_punitive_frozen_state", configure)
        self.assertIn("var:sb_klip_river_secession_frozen_state_scope ?= { owner", text(effects_path))
        self.assertIn("var:sb_klip_river_punitive_frozen_state_scope ?= { owner", text(effects_path))
        self.assertIn("sb_klip_river_secession_delivery_currently_permanently_invalid = yes", housekeeping)
        self.assertIn("sb_klip_river_punitive_delivery_currently_permanently_invalid = yes", housekeeping)

    def test_vanilla_type_story_routes_bind_exact_authored_plays(self):
        started = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_diplomatic_play_started",
        )
        enforced = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_wargoal_enforced",
        )
        back_down = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_diplo_play_back_down",
        )
        war_end = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_war_end",
        )
        gaza = object_block("events/sb_frontier_ai_wars_events.txt", "sb_frontier_ai_wars.040")
        swazi = object_block("events/sb_swazi_frontier_events.txt", "sb_swazi_frontier.094")
        trek = object_block("events/sb_great_trek_events.txt", "sb_great_trek.001")

        self.assertNotIn("random_diplomatic_play", gaza)
        self.assertIn("sb_gaza_zulu_launch_lease_var", gaza)
        self.assertIn("any_diplomatic_play", gaza)
        self.assertNotIn("remove_variable = sb_zulu_gaza_followup_pending_var", gaza)
        self.assertIn(
            "remove_variable = sb_zulu_gaza_followup_pending_var", started
        )
        self.assertIn("sb_zulu_swazi_launch_lease_var", swazi)
        self.assertIn("has_variable = sb_zulu_swazi_launch_lease_var", swazi)
        self.assertNotIn("any_diplomatic_play", shortest_block_containing(
            swazi, "if", "has_variable = sb_zulu_swazi_launch_lease_var",
            "sb_zulu_clear_swazi_campaign_runtime = yes",
        ))
        self.assertIn("sb_great_trek_opening_launch_lease_var", trek)
        self.assertIn("remove_variable = sb_ndebele_opening_play_fired", trek)

        bindings = {
            "sb_gaza_zulu_play_scope": ("dp_annex_war", "cd:ZUL", "cd:GZA"),
            "sb_zulu_swazi_play_scope": ("dp_conquer_state", "cd:ZUL", "cd:SWZ"),
            "sb_great_trek_opening_play_scope": ("dp_native_uprising", "cd:MTB", "cd:ORA"),
        }
        for scope_name, (play_type, initiator, target) in bindings.items():
            with self.subTest(scope=scope_name):
                binding = shortest_block_containing(
                    started, "if", play_type, initiator, target,
                    f"name = {scope_name} value = root",
                )
                self.assertIn("scope:initiator ?=", binding)
                self.assertIn("scope:target ?=", binding)
                self.assertIn(f"var:{scope_name} = scope:diplomatic_play", enforced)
                self.assertIn(f"var:{scope_name} = root", back_down)
                self.assertIn(f"var:{scope_name} = root", war_end)

        self.assertNotIn("scope:initiator", back_down)
        self.assertNotIn("scope:initiator", war_end)

    def test_zulu_terminal_truth_tables_are_unbiased_and_scope_safe(self):
        handler_path = "common/on_actions/sb_diplomatic_play_on_action_handlers.txt"
        war_end = object_block(handler_path, "sb_on_spes_bona_war_end")
        generic = shortest_block_containing(
            war_end,
            "if",
            "sb_zulu_generic_war_play_scope",
            "sb_zulu_apply_generic_war_victory",
            "sb_zulu_apply_generic_war_defeat",
        )
        self.assertIn(
            "has_variable = sb_zulu_generic_goal_accepted_pending_var NOT = { has_variable = sb_zulu_generic_defeat_goal_accepted_pending_var }",
            generic,
        )
        self.assertIn(
            "has_variable = sb_zulu_generic_defeat_goal_accepted_pending_var NOT = { has_variable = sb_zulu_generic_goal_accepted_pending_var }",
            generic,
        )
        self.assertEqual(1, generic.count("sb_zulu_apply_generic_war_victory = yes"))
        self.assertEqual(1, generic.count("sb_zulu_apply_generic_war_defeat = yes"))

        swazi = shortest_block_containing(
            war_end,
            "if",
            "sb_zulu_swazi_play_scope",
            "sb_zulu_apply_swazi_campaign_victory",
            "sb_zulu_apply_swazi_campaign_defeat",
            "sb_zulu_apply_swazi_campaign_stalemate",
        )
        self.assertEqual(2, swazi.count("has_variable = sb_zulu_swazi_target_state_scope"))
        self.assertEqual(
            2, swazi.count("var:sb_zulu_swazi_target_state_scope ?= { owner = c:ZUL }")
        )
        self.assertEqual(
            2, swazi.count("var:sb_zulu_swazi_target_state_scope ?= { owner = c:SWZ }")
        )
        self.assertIn("sb_zulu_clear_swazi_campaign_runtime = yes", swazi)
        victory = object_block(
            "common/scripted_effects/sb_zulu_dynasty_succession_effects.txt",
            "sb_zulu_apply_swazi_campaign_victory",
        )
        self.assertIn("add_claim = c:ZUL", victory)
        self.assertNotIn("add_claim = root", victory)

    def test_bechuanaland_timer_reconciliation_covers_warren_and_total_war(self):
        path = "common/scripted_effects/sb_bechuanaland_corridor_effects.txt"
        tracker = object_block(path, "sb_bechuanaland_track_crisis_wargoal_enforcement")
        resolver = object_block(path, "sb_bechuanaland_resolve_crisis_war_at_end")

        timer = shortest_block_containing(
            tracker, "if", "exists = scope:enforced_by_timer",
            "sb_bechuanaland_british_timer_goal_seen_pending_var",
        )
        self.assertEqual(1, timer.count("sb_bechuanaland_british_timer_goal_seen_pending_var"))
        self.assertEqual(1, timer.count("sb_bechuanaland_boer_swa_timer_goal_seen_pending_var"))
        self.assertIn(
            "scope:actor ?= { sb_bechuanaland_is_british_war_side_member = yes }",
            timer,
        )
        self.assertIn(
            "scope:actor ?= { sb_bechuanaland_is_boer_swa_war_side_member = yes }",
            timer,
        )
        self.assertNotIn("sb_bechuanaland_timer_goal_seen_pending_var", timer)
        self.assertNotIn("sb_bechuanaland_set_british_crisis_victory", timer)
        self.assertNotIn("sb_bechuanaland_set_boer_swa_crisis_victory", timer)
        self.assertGreaterEqual(
            resolver.count("dp_sb_bechuanaland_warren_intervention_locked"), 3
        )
        self.assertGreaterEqual(
            resolver.count("dp_sb_bechuanaland_cap_sgo_return"), 2
        )
        self.assertGreaterEqual(
            resolver.count("sb_bechuanaland_total_war_primary_target_scope"), 2
        )
        self.assertIn("sb_bechuanaland_set_british_crisis_victory = yes", resolver)
        self.assertIn("sb_bechuanaland_set_boer_swa_crisis_victory = yes", resolver)
        self.assertIn("var:sb_bechuanaland_crisis_play_scope = root", resolver)
        self.assertIn("remove_variable = sb_bechuanaland_crisis_play_scope", resolver)
        self.assertIn("sb_bechuanaland_british_terminal_evidence_var", resolver)
        self.assertIn("sb_bechuanaland_boer_swa_terminal_evidence_var", resolver)
        self.assertIn(
            "NOT = { container:sb_bechuanaland_corridor_state = { has_variable = sb_bechuanaland_boer_swa_terminal_evidence_var } }",
            resolver,
        )
        self.assertIn(
            "NOT = { container:sb_bechuanaland_corridor_state = { has_variable = sb_bechuanaland_british_terminal_evidence_var } }",
            resolver,
        )
        self.assertIn(
            "container:sb_bechuanaland_corridor_state.var:sb_bechuanaland_total_war_target_state_scope ?= { owner = c:CAP }",
            resolver,
        )
        self.assertIn(
            "container:sb_bechuanaland_corridor_state.var:sb_bechuanaland_total_war_cap_goal_target_scope ?= { owner = scope:sb_bechuanaland_final_total_war_target }",
            resolver,
        )
        configure = object_block(path, "sb_bechuanaland_configure_started_story_play")
        self.assertEqual(
            5,
            configure.count("name = sb_bechuanaland_crisis_play_scope value = root"),
        )
        self.assertIn(
            "var:sb_bechuanaland_crisis_play_scope = scope:diplomatic_play",
            tracker,
        )

    def test_gaza_claim_finalizer_uses_saved_state_and_exact_play_root(self):
        handler = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_war_end",
        )
        dispatch = shortest_block_containing(
            handler, "if", "sb_gaza_resolve_exact_terminal",
        )
        self.assertIn(
            "root = { is_diplomatic_play_type = dp_annex_war initiator = c:ZUL target = c:GZA }",
            dispatch,
        )
        self.assertIn(
            "initiator = { has_variable = sb_gaza_zulu_play_scope var:sb_gaza_zulu_play_scope = root }",
            dispatch,
        )
        resolver = object_block(
            "common/scripted_effects/sb_zulu_dynasty_succession_effects.txt",
            "sb_gaza_resolve_exact_terminal",
        )
        self.assertIn(
            "initiator ?= { has_variable = sb_gaza_zulu_play_scope var:sb_gaza_zulu_play_scope = root }",
            resolver,
        )
        self.assertIn(
            "var:sb_gaza_east_transvaal_target_state_scope ?= { owner = c:GZA }",
            resolver,
        )
        self.assertIn("s:STATE_EAST_TRANSVAAL = { add_claim = c:GZA }", resolver)
        self.assertNotIn("add_claim = root", resolver)

    def test_bst_backdown_and_timer_guards_do_not_award_an_aggressor_loss(self):
        path = "common/on_actions/sb_bst_on_actions.txt"
        back_down = object_block(path, "sb_on_bst_diplo_play_back_down")
        enforced = object_block(path, "sb_on_bst_wargoal_enforced")
        war_end = object_block(path, "sb_on_bst_war_end")
        monthly = object_block(path, "sb_on_bst_monthly_pulse_country")

        self.assertNotIn("sb_ora_annexed_bst_var", back_down)
        rejected = shortest_block_containing(
            back_down, "if", "sb_bst_annexation_backdown_rejected_var"
        )
        self.assertIn(
            "root = { is_diplomatic_play_type = dp_annex_war initiator = scope:actor target = c:BST }",
            rejected,
        )
        self.assertIn("scope:actor ?=", rejected)
        self.assertIn("sb_bst_oranje_frontier_actor = yes", rejected)
        self.assertNotIn("scope:target", rejected)

        self.assertIn("sb_bst_story_goal_accepted_pending_var", enforced)
        self.assertIn("is_diplomatic_play_type = dp_sb_basotho_gun_war", enforced)
        self.assertIn("var:sb_bst_gun_war_play_scope = scope:diplomatic_play", enforced)
        self.assertNotIn("is_diplomatic_play_type = dp_annex_war", enforced)
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
        self.assertIn("remove_variable = sb_bst_gun_war_launch_lease_var", monthly)
        started = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_diplomatic_play_started",
        )
        self.assertIn("sb_cap_has_bst_subject_for_disarmament = yes", started)


    def test_klip_county_creation_failure_is_attempt_local_and_restores_owners(self):
        path = "common/scripted_effects/sb_klip_river_county_effects.txt"
        create = object_block(path, "sb_klip_river_create_county")
        rollback = object_block(path, "sb_klip_river_rollback_created_county_attempt")
        orphan = object_block(path, "sb_klip_river_cleanup_orphaned_runtime")

        # The creation lease survives country admission and the transfer itself.
        self.assertLess(
            create.index("set_variable = sb_klip_river_county_creation_lease_var"),
            create.index("create_country ="),
        )
        transfer = "country = c:KLR provinces = { xBBCA32 xDE0EDE x552449 }"
        self.assertIn(transfer, create)
        success = shortest_block_containing(
            create,
            "if",
            "p:xBBCA32.state.owner = this",
            "p:xDE0EDE.state.owner = this",
            "p:x552449.state.owner = this",
        )
        self.assertIn(
            "remove_variable = sb_klip_river_county_creation_lease_var", success
        )
        self.assertIn(
            "sb_klip_river_county_created_this_attempt_var", create
        )

        # The rollback stores object identity before/after admission. It restores
        # only provinces still owned by that exact created object, never tags.
        for token in (
            "sb_klip_river_county_original_xbb_owner_scope",
            "sb_klip_river_county_created_country_scope",
            "p:xBBCA32.state.owner = scope:sb_klip_river_attempt_created_country",
            "country = scope:sb_klip_river_attempt_original_xbb_owner",
            "annex = scope:sb_klip_river_attempt_created_country",
            "country = root provinces = { xDE0EDE }",
            "country = root provinces = { x552449 }",
            "sb_klip_river_prepare_standard_boer_flight = yes",
        ):
            self.assertIn(token, rollback)
        self.assertIn(
            "value = scope:sb_klip_river_attempt_original_xbb_owner", create
        )
        self.assertIn(
            "value = scope:sb_klip_river_attempt_created_country", create
        )
        self.assertNotIn("annex = c:KLR", rollback)
        self.assertNotIn("country = c:ZUL", rollback)
        self.assertNotIn("country = c:NAL", rollback)
        self.assertIn("sb_klip_river_rollback_created_county_attempt = yes", create)
        self.assertIn("NOT = { c:KLR ?= { is_country_alive = yes } }", orphan)
        self.assertIn("sb_klip_river_clear_secession_runtime = yes", orphan)


    def test_klip_orphan_handler_uses_saved_actor_not_replacement_tag(self):
        effects = "common/scripted_effects/sb_klip_river_county_effects.txt"
        secession = object_block(
            effects, "sb_klip_river_begin_secession_delivery_generation"
        )
        punitive = object_block(
            effects, "sb_klip_river_begin_punitive_delivery_generation"
        )
        recover = object_block(effects, "sb_klip_river_recover_orphaned_generations")
        values = object_block(effects, "sb_klip_river_clear_country_marker_values")
        public_cleanup = object_block(effects, "sb_klip_river_clear_country_markers")
        regional = text("common/on_actions/sb_regional_on_action_handlers.txt")
        router = object_block("common/on_actions/sb_on_actions.txt", "on_monthly_pulse_country")

        for generation in (secession, punitive):
            self.assertIn("save_temporary_scope_as = sb_klip_river_", generation)
            self.assertIn("generation_actor_scope value = scope:", generation)
        self.assertIn("generation_county_scope", secession)
        self.assertIn("generation_zulu_scope", secession)
        self.assertIn("generation_zulu_scope", punitive)
        self.assertIn("var:sb_klip_river_secession_generation_actor_scope", recover)
        self.assertIn("var:sb_klip_river_punitive_generation_actor_scope", recover)
        # Recovery is inside each container. It clears saved country values first,
        # and has exactly one local destroy per route branch.
        self.assertIn("sb_klip_river_clear_country_marker_values = yes", recover)
        self.assertNotIn("sb_klip_river_clear_country_markers = yes", recover)
        self.assertEqual(2, recover.count("destroy_container = yes"))
        self.assertIn("remove_variable = sb_klip_river_secession_active_var", values)
        self.assertIn("sb_klip_river_clear_country_marker_values = yes", public_cleanup)
        self.assertEqual(2, public_cleanup.count("destroy_container = yes"))
        self.assertIn("every_country = {", recover)
        self.assertIn("NOT = { country_definition = cd:NAL }", recover)
        self.assertIn("sb_on_klip_river_orphan_monthly", regional)
        self.assertIn("sb_klip_river_recover_orphaned_generations = yes", regional)
        self.assertIn("sb_on_klip_river_orphan_monthly", router)



if __name__ == "__main__":
    unittest.main()
