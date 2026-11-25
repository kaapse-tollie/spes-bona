"""Source-level checks for the Warren handoffs and the coastal administration."""

import re
import unittest

from tests.test_1_14_story_war_routes import nested_blocks, text
from tests.test_klip_river_colonial_delivery import expression
from tools.validate import extract_braced


CORRIDOR_EVENTS = "events/sb_bechuanaland_corridor_events.txt"
CORRIDOR_TRIGGERS = "common/scripted_triggers/sb_bechuanaland_corridor_triggers.txt"
CORRIDOR_EFFECTS = "common/scripted_effects/sb_bechuanaland_corridor_effects.txt"
WARREN = "common/scripted_effects/sb_warren_negotiation_effects.txt"
KIMBERLEY = "common/scripted_effects/sb_warren_kimberley_effects.txt"
NAMIBIA_TRIGGERS = "common/scripted_triggers/sb_namibia_triggers.txt"
NAMIBIA_POLICIES = "common/scripted_effects/sb_namibia_policy_effects.txt"
NAMIBIA_EVENTS = "events/sb_namibia_events.txt"


def object_block(path, name):
    source = text(path)
    declaration = re.search(r"^" + re.escape(name) + r" = \{", source, re.MULTILINE)
    if declaration is None:
        raise AssertionError(f"{name} is not defined in {path}")
    return extract_braced(source, declaration.start())


class WarrenNegotiationTests(unittest.TestCase):
    def test_only_final_boer_resistance_can_launch_each_offer(self):
        start = object_block(WARREN, "sb_bechuanaland_start_warren_negotiation")
        self.assertIn("sb_bechuanaland_corridor.011", start)
        self.assertIn("sb_bechuanaland_consult_warren_sponsor = yes", start)
        consult = object_block(WARREN, "sb_bechuanaland_consult_warren_sponsor")
        self.assertIn("var:sb_warren_sponsor_scope", consult)
        self.assertIn("sb_bechuanaland_corridor.012", consult)
        answer = object_block(WARREN, "sb_bechuanaland_send_warren_answer")
        self.assertEqual(answer.count("trigger_event"), 1)
        self.assertIn("var:sb_bechuanaland_warren_defender_scope", answer)
        self.assertIn("sb_bechuanaland_corridor.013", answer)

        sponsor = object_block(CORRIDOR_EVENTS, "sb_bechuanaland_corridor.012")
        self.assertIn("default_option = yes", nested_blocks(sponsor, "option")[2])
        for offer, choice in zip((1, 2, 0), nested_blocks(sponsor, "option"), strict=True):
            with self.subTest(offer=offer):
                self.assertIn(f"OFFER = {offer}", choice)
                self.assertNotIn("launch_", choice)
                self.assertNotIn("change_infamy", choice)
        for event in ("011", "013"):
            with self.subTest(event=event):
                scene = object_block(CORRIDOR_EVENTS, "sb_bechuanaland_corridor." + event)
                default = nested_blocks(scene, "option")[0]
                self.assertIn("default_option = yes", default)
                self.assertIn("sb_bechuanaland_accept_warren_terms = yes", default)
                self.assertNotIn("launch_", default)
        resistance = nested_blocks(scene, "option")[1]
        self.assertIn("sb_bechuanaland_warren_answer_is_current = yes", resistance)
        self.assertIn("sb_bechuanaland_stand_firm_over_warren = yes", resistance)

    def test_replacing_a_lapsed_pledge_invalidates_the_previous_popup(self):
        dispatch = object_block(WARREN, "sb_bechuanaland_open_warren_decision")
        guard = object_block(CORRIDOR_TRIGGERS, "sb_bechuanaland_warren_event_is_current")
        repair = object_block(WARREN, "sb_bechuanaland_repair_warren_negotiation")
        self.assertIn("change_variable = { name = sb_warren_sequence_var add = 1 }", dispatch)
        self.assertIn("var:sb_warren_sequence_var = scope:sb_warren_event_sequence", guard)
        self.assertIn("sb_bechuanaland_send_warren_answer = { OFFER = 0 }", repair)
        self.assertIn("sb_bechuanaland_cancel_warren_negotiation = yes", repair)

    def test_kimberley_uses_the_same_actual_states_for_peace_and_war(self):
        play = object_block("common/diplomatic_plays/sb_diplomatic_plays.txt",
                            "dp_sb_bechuanaland_warren_kimberley_locked")
        self.assertIn("sb_bechuanaland_warren_demand_is_current = yes", play)
        self.assertNotIn("c:SGO", play)
        self.assertNotIn("region_state:CAP", play)
        peace = object_block(WARREN, "sb_bechuanaland_accept_warren_terms")
        primary = object_block(KIMBERLEY, "sb_bechuanaland_add_warren_primary_goals")
        for state in ("bechuanaland", "griqualand"):
            self.assertIn(f"var:sb_warren_{state}_state = {{ set_state_owner = c:CAP }}", peace)
            self.assertIn("DEMAND = " + state, primary)
        goal = object_block(KIMBERLEY, "sb_bechuanaland_add_kimberley_region_demands")
        self.assertIn("var:sb_warren_$DEMAND$_owner", goal)
        self.assertIn("holder = c:CAP", goal)
        self.assertIn("primary_demand = yes", goal)
        revoke = object_block(KIMBERLEY, "sb_bechuanaland_add_kimberley_revoke_claim")
        self.assertIn("has_claim = s:$REGION$", revoke)
        self.assertIn("type = revoke_claim", revoke)
        self.assertIn("primary_demand = yes", revoke)
        for route in ("direct", "proxy", "total"):
            config = object_block(CORRIDOR_EFFECTS, "sb_bechuanaland_configure_" +
                                  (f"warren_{route}_crisis_play" if route != "total" else "total_crisis_play"))
            self.assertIn("sb_bechuanaland_add_warren_primary_goals = yes", config)
            self.assertIn("sb_bechuanaland_add_british_boer_subjugation_goals = yes", config)

    def test_only_final_enforcement_on_bound_play_can_stamp_results(self):
        callbacks = "common/on_actions/sb_diplomatic_play_on_action_handlers.txt"
        target = "sb_bechuanaland_track_kimberley_warren_enforcement = yes"
        self.assertIn(target, object_block(callbacks, "sb_on_spes_bona_wargoal_enforced"))
        self.assertNotIn(target, object_block(callbacks, "sb_on_spes_bona_wargoal_enforced_by_timer"))
        tracker = object_block(KIMBERLEY, "sb_bechuanaland_track_kimberley_warren_enforcement")
        self.assertIn("var:sb_bechuanaland_crisis_play_scope ?= scope:diplomatic_play", tracker)
        terminal = object_block(KIMBERLEY, "sb_bechuanaland_reconcile_kimberley_warren")
        territorial = nested_blocks(terminal, "limit")[2]
        self.assertIn("DEMAND = bechuanaland", territorial)
        self.assertIn("DEMAND = griqualand", territorial)
        self.assertNotIn("OR = {", territorial)


class SouthWestAfricaPolicyTests(unittest.TestCase):
    def test_maturity_reads_the_actual_fragments_on_the_map(self):
        nodes = expression(object_block(NAMIBIA_TRIGGERS, "sb_nam_controls_administration_territory"))

        def complete(hereroland, namaqualand):
            def evaluate(items, fragment=None):
                for key, value in items:
                    if key in ("OR", "NOT", "NOR"):
                        passes = any(evaluate([item], fragment) for item in value)
                        if key != "OR":
                            passes = not passes
                    elif key == "owns_entire_state_region":
                        owned = hereroland if value == "STATE_HEREROLAND" else namaqualand
                        passes = all(holder == "SWA" for holder, _ in owned)
                    elif key == "AND" or key == "s:STATE_NAMAQUALAND":
                        passes = evaluate(value, fragment)
                    elif key == "p:x8031D0.state":
                        passes = evaluate(value, namaqualand[0])
                    elif key == "any_scope_state":
                        passes = any(evaluate(value, part) for part in namaqualand)
                    elif key == "owner":
                        passes = fragment[0] == value.removeprefix("c:").replace("$ADMINISTRATOR$", "SWA")
                    elif key == "num_provinces":
                        passes = fragment[1] == int(value)
                    elif key == "this":
                        passes = fragment is namaqualand[0] and value == "p:x8031D0.state"
                    else:
                        raise AssertionError(key)
                    if not passes:
                        return False
                return True

            return evaluate(nodes)

        cases = (
            ([("SWA", 44)], [("SWA", 22)], True),
            ([("SWA", 44)], [("CAP", 1), ("SWA", 21)], True),
            ([("SWA", 44)], [("CAP", 2), ("SWA", 20)], False),
            ([("SWA", 44)], [("CAP", 1), ("SWA", 20), ("RHB", 1)], False),
            ([("SWA", 43), ("ORL", 1)], [("CAP", 1), ("SWA", 21)], False),
            ([("SWA", 44)], [("PRT", 1), ("SWA", 21)], False),
        )
        for hereroland, namaqualand, expected in cases:
            with self.subTest(hereroland=hereroland, namaqualand=namaqualand):
                self.assertEqual(complete(hereroland, namaqualand), expected)

    def test_foundation_performs_policy_laws_after_land_transfer(self):
        attempt = object_block(NAMIBIA_POLICIES, "sb_nam_try_found_policy_colony")
        self.assertIn("sb_nam_controls_both_consolidation_ports = yes", attempt)
        self.assertIn("sb_nam_can_found_policy_colony = yes", attempt)
        foundation = object_block(NAMIBIA_POLICIES, "sb_nam_finish_policy_colony")
        self.assertLess(foundation.index("set_state_owner = c:SWA"),
                        foundation.index("sb_nam_apply_selected_policy_laws = yes"))
        self.assertIn("sb_nam_apply_administrative_capacity = yes", foundation)
        laws = object_block(NAMIBIA_POLICIES, "sb_nam_apply_selected_policy_laws")
        self.assertIn("var:sb_nam_selected_policy_var = 1 has_technology_researched = medical_degrees", laws)
        self.assertIn("law_type:law_charitable_health_system", laws)
        self.assertIn("law_type:law_slavery_banned", laws)
        capacity = object_block("common/static_modifiers/sb_namibia_modifiers.txt",
                                "sb_nam_administrative_capacity")
        self.assertIn("country_bureaucracy_mult = 0.20", capacity)

    def test_charges_and_slot_follow_different_receipts(self):
        establish = object_block(NAMIBIA_POLICIES, "sb_nam_establish_swa_company")
        monthly = object_block(NAMIBIA_POLICIES, "sb_nam_maintain_swa_company")
        self.assertLess(establish.index("add_owned_country = c:SWA"),
                        establish.index("sb_nam_company_payments_left_var value = 120"))
        branches = nested_blocks(monthly, "if")
        payments, slot = branches[0], branches[-1]
        self.assertIn("add_treasury = -2000", payments)
        self.assertIn("sb_nam_company_payments_left_var subtract = 1", payments)
        self.assertNotIn("sb_nam_company_is_linked", payments)
        self.assertIn("NOT = { sb_nam_company_is_linked = yes }", slot)

    def test_extermination_uses_one_live_gate_and_a_durable_choice(self):
        gate = object_block(NAMIBIA_TRIGGERS, "sb_nam_extermination_orders_available")
        self.assertIn("var:sb_nam_selected_policy_var = 3 var:sb_nam_selected_policy_var = 4", gate)
        self.assertIn("political_movement_radicalism >= 0.75", gate)
        self.assertIn("sb_nam_controls_administration_territory", gate)
        self.assertNotIn("expiry", gate)
        self.assertNotIn("corridor", gate)
        dispatch = object_block(NAMIBIA_POLICIES, "sb_nam_offer_extermination_orders")
        self.assertLess(dispatch.index("set_variable"), dispatch.index("trigger_event"))
        event = object_block(NAMIBIA_EVENTS, "sb_nam.201")
        for choice in nested_blocks(event, "option"):
            self.assertIn("sb_nam_extermination_orders_available = yes", choice)
            self.assertIn("set_variable = sb_nam_extermination_fired_var", choice)
