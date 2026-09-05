from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]
NATALIA_CORE = {
    "x5B124F",
    "xFF0EF1",
    "x552449",
    "xE0EB02",
    "x85695F",
    "xDE0EDE",
    "x7ACC38",
    "xB1F868",
    "x3CED3D",
    "x11A090",
    "xCD31DB",
}
KLR_NATAL_PROVINCES = {"xBBCA32", "xDE0EDE", "x552449"}


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def object_block(path: str, name: str) -> str:
    return object_block_from_source(text(path), name, path)


def object_block_from_source(source: str, name: str, context: str = "source") -> str:
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} in {context}")
    return validate.extract_braced(source, match.start())


def nested_blocks(source: str, name: str) -> list[str]:
    return [
        validate.extract_braced(source, match.start())
        for match in re.finditer(
            rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE
        )
    ]


def named_option(event: str, name: str) -> str:
    for option in nested_blocks(event, "option"):
        if re.search(rf"\bname\s*=\s*{re.escape(name)}\b", option):
            return option
    raise AssertionError(f"missing option {name}")


def shortest_named_block_containing(source: str, name: str, token: str) -> str:
    matches = [block for block in nested_blocks(source, name) if token in block]
    if not matches:
        raise AssertionError(f"missing {name} block containing {token}")
    return min(matches, key=len)


def province_set(source: str) -> set[str]:
    return {
        province.upper().replace("X", "x", 1)
        for province in validate.PROVINCE_RE.findall(source)
    }


def owner_provinces(state_block: str, country: str) -> set[str]:
    # Current helpers may keep a compact state transfer on one line. Match the
    # object itself rather than requiring the directive to start a line.
    matches = [
        validate.extract_braced(state_block, match.start())
        for match in re.finditer(r"set_owner_of_provinces\s*=\s*\{", state_block)
        if re.search(
            rf"\bcountry\s*=\s*c:{re.escape(country)}\b",
            validate.extract_braced(state_block, match.start()),
        )
    ]
    if len(matches) != 1:
        raise AssertionError(
            f"expected one {country} ownership transfer, found {len(matches)}"
        )
    return validate.object_values(matches[0], "provinces")


def without_comments(source: str) -> str:
    return re.sub(r"(?m)#.*$", "", source)


class NatalZululandGameplayContractTests(unittest.TestCase):
    def test_natalia_core_is_the_exact_eleven_province_interior(self):
        core = object_block(
            "common/scripted_triggers/sb_great_trek_triggers.txt",
            "sb_controls_natalia_core",
        )
        actual = {
            province.upper().replace("X", "x", 1)
            for province in re.findall(
                r"\bp:(x[0-9A-Fa-f]{6})\.state\.owner\s*=\s*this\b", core
            )
        }

        self.assertEqual(NATALIA_CORE, actual)
        self.assertNotIn("x279045", core)
        self.assertNotIn("xBBCA32", core)
        self.assertNotIn("owns_entire_state_region", core)

    def test_natalia_stages_founders_then_receives_the_former_ngi_interior(self):
        path = "common/scripted_effects/sb_natalia_effects.txt"
        creation = object_block(path, "sb_create_natalia_republic_if_missing")
        assignment = object_block(path, "sb_assign_natalia_republic_territory")
        frontier_creation = object_block(
            path, "sb_create_natalia_frontier_republic_if_missing"
        )
        frontier_assignment = object_block(
            path, "sb_assign_natalia_frontier_territory"
        )
        peaceful = object_block(path, "sb_found_natalia_peacefully")
        setup = object_block(path, "sb_apply_natalia_boer_republic_setup")

        self.assertIn("p:x5B124F.state", creation)
        self.assertIn("culture = cu:boer", creation)
        self.assertIn("population_ratio = 0.05", creation)
        self.assertLess(creation.index("move_partial_pop"), creation.index("create_country"))
        country = object_block_from_source(creation, "create_country", path)
        self.assertIn("tag = NAL", country)
        self.assertIn("province = p:x5B124F", country)

        natal = object_block_from_source(assignment, "s:STATE_NATAL", path)
        self.assertEqual(NATALIA_CORE, validate.object_values(natal, "provinces"))
        self.assertIn("add_claim = c:NAL", natal)
        self.assertNotIn("STATE_ZULULAND", assignment)
        self.assertIn("province = p:x552449", frontier_creation)
        frontier_natal = object_block_from_source(
            frontier_assignment, "s:STATE_NATAL", path
        )
        self.assertEqual(
            {"x552449", "xDE0EDE"}, owner_provinces(frontier_natal, "NAL")
        )
        self.assertEqual(
            NATALIA_CORE - {"x552449", "xDE0EDE"},
            owner_provinces(frontier_natal, "NGI"),
        )
        housekeeping = object_block_from_source(
            frontier_natal, "hidden_effect", path
        )
        self.assertEqual(
            NATALIA_CORE - {"x552449", "xDE0EDE"},
            owner_provinces(housekeeping, "NGI"),
        )
        self.assertNotIn("country = c:NAL", housekeeping)
        self.assertIn(
            "sb_create_natalia_frontier_republic_if_missing = yes", peaceful
        )
        self.assertIn("sb_assign_natalia_frontier_territory = yes", peaceful)
        self.assertNotIn("sb_assign_natalia_republic_territory = yes", peaceful)
        self.assertIn("activate_law = law_type:law_frontier_colonization", setup)
        self.assertIn("name = sb_trek_frontier_drive", setup)
        frontier_drive = object_block(
            "common/static_modifiers/sb_modifiers.txt", "sb_trek_frontier_drive"
        )
        self.assertIn("state_non_homeland_colony_growth_speed_mult = 0.75", frontier_drive)
        packet_match = re.search(
            r"^\s*s:STATE_NATAL\.region_state:NAL\s*\?=\s*\{",
            setup,
            re.MULTILINE,
        )
        self.assertIsNotNone(packet_match)
        packet = validate.extract_braced(setup, packet_match.start())
        packet_buildings = nested_blocks(packet, "create_building")
        self.assertEqual(
            1,
            sum("building = building_maize_farm" in building for building in packet_buildings),
        )
        self.assertEqual(
            1,
            sum(
                "building = building_livestock_ranch" in building
                for building in packet_buildings
            ),
        )
        for building in packet_buildings:
            self.assertIn("add_ownership", building)
            self.assertNotRegex(building, r"(?m)^\s*level\s*=")
        self.assertIn('"pm_simple_farming"', packet)
        self.assertIn('"pm_no_secondary"', packet)
        self.assertIn('"pm_tools_disabled"', packet)
        self.assertIn('"pm_open_air_stockyards"', packet)
        self.assertIn('"pm_simple_ranch"', packet)
        self.assertIn('"pm_standard_fences"', packet)
        self.assertIn('"pm_unrefrigerated"', packet)

        retief = object_block(
            "common/character_templates/sb_southern_africa_character_template_overrides.txt",
            "REPLACE:ORA_piet_retief",
        )
        self.assertIn("expert_colonial_administrator", retief)
        self.assertNotIn("basic_colonial_administrator", retief)
        self.assertNotIn("experienced_colonial_administrator", retief)

    def test_peaceful_highveld_option_delegates_to_the_canonical_founder(self):
        path = "events/iberia_events/struggle_for_the_highveld_events.txt"
        event = object_block(path, "struggle_for_the_highveld.4")
        peaceful = named_option(event, "struggle_for_the_highveld.4.c")

        self.assertEqual(1, peaceful.count("sb_found_natalia_peacefully = yes"))
        self.assertNotIn("remove_claim = c:ZUL", peaceful)
        self.assertNotIn("STATE_ZULULAND", peaceful)
        for direct_mutation in (
            "create_country =",
            "set_owner_of_provinces =",
            "set_state_owner =",
            "every_scope_state =",
        ):
            self.assertNotIn(direct_mutation, peaceful)
        self.assertEqual(set(), province_set(peaceful))

        for event_id in ("struggle_for_the_highveld.6", "struggle_for_the_highveld.7"):
            highveld_outcome = object_block(path, event_id)
            self.assertIn("STATE_NATAL", highveld_outcome)
            self.assertNotIn("STATE_ZULULAND", highveld_outcome)

    def test_ultimatum_requires_a_natalia_harbour_and_raid_starts_it_immediately(self):
        monthly = object_block(
            "common/on_actions/sb_boer_story_on_action_handlers.txt",
            "sb_on_trek_monthly_pulse_country",
        )
        delayed = shortest_named_block_containing(
            monthly, "if", "sb_controls_natalia_core = yes"
        )
        delays = {
            int(days)
            for days in re.findall(
                r"id\s*=\s*sb_natal_crisis\.100\s+days\s*=\s*(\d+)", delayed
            )
        }
        self.assertEqual(set(range(90, 721, 90)), delays)
        self.assertIn("country_definition = cd:GBR", delayed)
        self.assertIn("sb_controls_natalia_core = yes", delayed)
        self.assertIn("sb_natalia_has_harbour = yes", delayed)
        self.assertNotIn("p:x279045.state.owner = c:NAL", delayed)
        self.assertIn("NOT = { has_variable = sb_british_natal_ultimatum_var }", delayed)
        self.assertIn(
            "NOT = { has_variable = sb_british_natal_ultimatum_pending_var }",
            delayed,
        )
        self.assertIn(
            "NOT = { has_variable = sb_british_natal_nonintervention_var }",
            delayed,
        )
        self.assertIn("NOT = { has_variable = sb_natalia_british_colony_resolved_var }", delayed)

        harbour = object_block(
            "common/scripted_triggers/sb_great_trek_triggers.txt",
            "sb_natalia_has_harbour",
        )
        self.assertIn("state_region = s:STATE_NATAL", harbour)
        self.assertIn("has_building = building_port", harbour)

        decision = object_block(
            "common/decisions/sb_zulu_decisions.txt", "natalia_raid_port_natal"
        )
        shown = object_block_from_source(decision, "is_shown", "natalia_raid_port_natal")
        taken = object_block_from_source(decision, "when_taken", "natalia_raid_port_natal")
        self.assertIn("NOT = { has_variable = sb_natalia_port_natal_raid_taken_var }", shown)
        self.assertIn("NOT = { has_variable = sb_natalia_british_colony_resolved_var }", shown)
        self.assertIn("set_variable = sb_british_natal_ultimatum_var", taken)
        self.assertIn("remove_variable = sb_british_natal_ultimatum_pending_var", taken)
        self.assertIn("remove_variable = sb_british_natal_nonintervention_var", taken)
        self.assertIn("set_variable = sb_natalia_port_natal_raid_taken_var", taken)
        natal = object_block_from_source(taken, "s:STATE_NATAL", "natalia_raid_port_natal")
        self.assertEqual({"x279045"}, validate.object_values(natal, "provinces"))

        ultimatum = object_block("events/sb_natal_crisis_events.txt", "sb_natal_crisis.100")
        trigger = object_block_from_source(ultimatum, "trigger", "sb_natal_crisis.100")
        immediate = object_block_from_source(ultimatum, "immediate", "sb_natal_crisis.100")
        send = named_option(ultimatum, "sb_natal_crisis.100.a")
        wait = named_option(ultimatum, "sb_natal_crisis.100.b")
        self.assertIn("NOT = { has_variable = sb_british_natal_ultimatum_var }", trigger)
        self.assertIn(
            "NOT = { has_variable = sb_british_natal_nonintervention_var }",
            trigger,
        )
        self.assertIn("sb_natalia_has_harbour = yes", trigger)
        self.assertNotIn("p:x279045.state.owner = c:NAL", trigger)
        self.assertIn("remove_variable = sb_british_natal_ultimatum_pending_var", immediate)
        self.assertNotIn("set_variable = sb_british_natal_ultimatum_var", immediate)
        self.assertIn("set_variable = sb_british_natal_ultimatum_var", send)
        self.assertNotIn("sb_british_natal_ultimatum_var", wait)
        self.assertIn("set_variable = sb_british_natal_nonintervention_var", wait)

        events_path = "events/sb_natal_crisis_events.txt"
        relay = object_block(events_path, "sb_natal_crisis.108")
        message = object_block(events_path, "sb_natal_crisis.109")
        final = object_block(events_path, "sb_natal_crisis.110")
        self.assertIn("sb_natalia_has_harbour = yes", relay)
        self.assertGreaterEqual(message.count("sb_natalia_has_harbour = yes"), 2)
        self.assertIn("sb_natalia_has_harbour = yes", final)
        defy = named_option(final, "sb_natal_crisis.110.b")
        self.assertNotIn("set_owner_of_provinces", defy)
        self.assertNotIn("x279045", defy)
        loc = text("localization/english/sb_natal_crisis_l_english.yml")
        self.assertIn(
            'sb_natal_crisis.110.b:0 "Reject the terms and call for aid."', loc
        )
        self.assertNotIn("seize Port Natal and call upon", loc)

    def test_british_ultimatum_ai_weights_reward_imperial_alignment_symmetrically(self):
        event = object_block("events/sb_natal_crisis_events.txt", "sb_natal_crisis.100")
        send = object_block_from_source(
            named_option(event, "sb_natal_crisis.100.a"),
            "ai_chance",
            "send ultimatum",
        )
        leave = object_block_from_source(
            named_option(event, "sb_natal_crisis.100.b"),
            "ai_chance",
            "leave Natalia",
        )

        for weights in (send, leave):
            self.assertEqual(
                7,
                weights.count(
                    "sb_frontier_ai_behavior_strict_historical = no"
                ),
            )
            for threshold in ("cordial", "amicable", "friendly"):
                self.assertIn(f"relations_threshold:{threshold}", weights)
            self.assertIn("is_in_same_power_bloc = root", weights)
            for article in (
                "trade_privilege",
                "foreign_investment_rights",
                "host_power_bloc_embassy",
            ):
                self.assertIn(f"has_type = {article}", weights)
            self.assertEqual(3, weights.count("source_country = scope:natalia"))
            self.assertEqual(3, weights.count("target_country = root"))

        self.assertEqual(5, send.count("add = -10"))
        self.assertEqual(1, send.count("add = -25"))
        self.assertEqual(1, send.count("add = -5"))
        self.assertEqual(5, leave.count("add = 10"))
        self.assertEqual(1, leave.count("add = 25"))
        self.assertEqual(1, leave.count("add = 5"))

    def test_ultimatum_play_returns_natal_and_only_oranje_adds_cape_liberation(self):
        launch = named_option(
            object_block("events/sb_natal_crisis_events.txt", "sb_natal_crisis.114"),
            "sb_natal_crisis.114.a",
        )
        effects_path = "common/scripted_effects/sb_natalia_colony_effects.txt"
        secondary = object_block(
            effects_path, "sb_add_natalia_liberate_cape_goal_if_oranje_supports"
        )

        self.assertIn("type = dp_make_protectorate", launch)
        self.assertIn("holder = scope:natalia", launch)
        self.assertIn("type = return_state", launch)
        self.assertIn("target_country = c:CAP", launch)
        self.assertIn("target_state = s:STATE_NATAL.region_state:CAP", launch)
        self.assertIn("primary_demand = yes", launch)
        self.assertNotIn("type = humiliation", launch)
        self.assertNotIn("type = liberate_subject", launch)
        self.assertEqual(
            1,
            launch.count(
                "sb_add_natalia_liberate_cape_goal_if_oranje_supports = yes"
            ),
        )

        self.assertIn("c:ORA ?= THIS", secondary)
        self.assertIn("is_diplomatic_play_committed_participant = yes", secondary)
        self.assertIn("is_diplomatic_play_enemy_of = c:GBR", secondary)
        self.assertIn("holder = c:NAL", secondary)
        self.assertIn("target_country = c:CAP", secondary)
        self.assertIn("type = liberate_subject", secondary)
        self.assertNotIn("primary_demand = yes", secondary)

    def test_klip_river_county_and_reduced_natalia_keep_explicit_boundaries(self):
        effects_path = "common/scripted_effects/sb_klip_river_county_effects.txt"
        flight = object_block(
            effects_path, "sb_klip_river_prepare_standard_boer_flight"
        )
        create_county = object_block(effects_path, "sb_klip_river_create_county")
        natal = object_block_from_source(create_county, "s:STATE_NATAL", effects_path)
        self.assertIn(
            "trigger_event = { id = sb_klip_river_county.075 days = 7 popup = yes }",
            flight,
        )
        self.assertNotIn("days = 3", flight)
        self.assertEqual(KLR_NATAL_PROVINCES, owner_provinces(natal, "KLR"))
        self.assertIn("s:STATE_NATAL = { add_claim = c:KLR }", create_county)
        self.assertNotIn("STATE_ZULULAND", create_county)

        natalia_assignment = object_block(
            "common/scripted_effects/sb_natalia_effects.txt",
            "sb_assign_natalia_republic_territory",
        )
        self.assertIn("s:STATE_NATAL", natalia_assignment)
        self.assertIn("add_claim = c:NAL", natalia_assignment)
        self.assertNotIn("STATE_ZULULAND", natalia_assignment)

        cession = object_block("events/sb_natal_crisis_events.txt", "sb_natal_crisis.020")
        recognition = named_option(cession, "sb_natal_crisis.020.a")
        self.assertNotIn("remove_claim = c:ZUL", recognition)
        self.assertNotIn("STATE_ZULULAND", recognition)

        guns_acceptance = named_option(
            object_block("events/sb_natal_crisis_events.txt", "sb_natal_crisis.025"),
            "sb_natal_crisis.025.a",
        )
        self.assertNotIn("remove_claim = c:ZUL", guns_acceptance)
        self.assertNotIn("STATE_ZULULAND", guns_acceptance)

        reduced = object_block(effects_path, "sb_klip_river_finalize_reduced_natalia")
        reduced_natal = object_block_from_source(reduced, "s:STATE_NATAL", effects_path)
        reduced_zululand = object_block_from_source(
            reduced, "s:STATE_ZULULAND", effects_path
        )
        self.assertEqual(KLR_NATAL_PROVINCES, owner_provinces(reduced_natal, "KLR"))
        self.assertIn("xE1E455", owner_provinces(reduced_zululand, "ZUL"))
        self.assertNotIn("country = c:KLR", reduced_zululand)
        self.assertNotIn("change_tag = NAL", reduced)
        self.assertNotIn("sb_british_natal_ultimatum_var", reduced)
        self.assertIn("sb_apply_natalia_boer_republic_setup = yes", reduced)
        self.assertIn("country = c:KLR", reduced)
        self.assertNotIn("country = c:NAL", reduced)

        loc = text("localization/english/sb_natal_crisis_l_english.yml")
        self.assertIn('KLR:0 "Klip River Republic"', loc)
        self.assertNotIn('KLR:0 "Klip River County"', loc)

    def test_peaceful_guns_settlement_allows_an_oranje_player_to_lead_natalia(self):
        event = object_block(
            "events/sb_natal_crisis_events.txt", "sb_natal_crisis.025"
        )
        remain = named_option(event, "sb_natal_crisis.025.a")
        switch = named_option(event, "sb_natal_crisis.025.c")

        for effect in (
            "sb_found_natalia_peacefully = yes",
            "sb_create_ora_zul_firearms_treaty = yes",
            "sb_zulu_mark_swazi_question_after_guns_south = yes",
            "sb_zulu_maybe_open_swazi_question = yes",
        ):
            self.assertIn(effect, remain)
            self.assertIn(effect, switch)

        trigger = object_block_from_source(switch, "trigger")
        ai_chance = object_block_from_source(switch, "ai_chance")
        self.assertIn("is_player = yes", trigger)
        self.assertIn("play_as = c:NAL", switch)
        self.assertIn("base = 0", ai_chance)
        self.assertIn(
            'sb_natal_crisis.025.c:0 "Pay the price—and follow the wagons."',
            text("localization/english/sb_natal_crisis_l_english.yml"),
        )

    def test_guns_rejection_uses_full_ngi_annexation_not_a_single_province_transfer(self):
        events_path = "events/sb_natal_crisis_events.txt"
        source = text(events_path)
        offer = object_block(events_path, "sb_natal_crisis.025")
        rejection = named_option(offer, "sb_natal_crisis.025.b")
        response = object_block(events_path, "sb_natal_crisis.026")
        fight = named_option(response, "sb_natal_crisis.026.a")
        cede = named_option(response, "sb_natal_crisis.026.b")

        self.assertIn("sb_natal_story_begin_guns_bargain_generation = yes", rejection)
        authority = object_block(
            "common/scripted_triggers/sb_natal_interwar_triggers.txt",
            "sb_natal_story_bound_guns_bargain_event_authority",
        )
        self.assertIn("sb_natal_guns_bargain_generation_scope", authority)
        self.assertIn("var:sb_natal_guns_bargain_generation_scope = scope:sb_natal_guns_bargain_receipt_scope", authority)
        self.assertIn("sb_natal_story_bound_guns_bargain_event_authority = yes", response)
        self.assertIn("sb_natal_story_begin_exact_launch = yes", fight)
        self.assertNotIn("set_owner_of_provinces", response)
        self.assertNotIn("x5B124F", response)
        self.assertNotIn("sb_natal_crisis.051", source)

        self.assertIn("sb_natal_story_begin_exact_launch = yes", fight)
        self.assertNotIn("annex = c:NGI", fight)
        started = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_diplomatic_play_started",
        )
        self.assertIn("is_diplomatic_play_type = dp_sb_natal_crisis", started)
        self.assertIn("has_variable = sb_natal_story_launch_lease_var", started)
        self.assertIn("set_variable = sb_natal_war_active_var", started)
        self.assertIn("sb_natal_story_absorption_commit_var", started)
        self.assertIn("annex = c:NGI", started)
        self.assertIn("sb_zulu_add_dynastic_stability_10 = yes", started)
        self.assertIn("has_template = ZUL_dingane", started)
        self.assertIn("NOT = { has_trait = brave }", started)
        self.assertIn("add_trait = brave", started)

        stability_bar = object_block(
            "common/scripted_progress_bars/sb_progress_bars.txt",
            "sb_zulu_dynastic_stability_bar",
        )
        brave_drift = shortest_named_block_containing(
            stability_bar, "if", "ruler = { has_trait = brave }"
        )
        self.assertIn('desc = "sb_zulu_drift_brave"', brave_drift)
        self.assertIn("value = 1", brave_drift)

        self.assertIn("c:ORA ?=", cede)
        self.assertIn("sb_found_natalia_peacefully = yes", cede)
        self.assertNotIn("annex = c:NGI", cede)
        self.assertNotIn("sb_create_ora_zul_firearms_treaty", cede)
        self.assertIn("custom_tooltip = sb_zulu_dynasty_lose_stability_5", cede)
        self.assertIn("sb_zulu_remove_dynastic_stability_5 = yes", cede)
        self.assertIn("has_template = ZUL_dingane", cede)
        self.assertIn("NOT = { has_trait = compliant }", cede)
        self.assertIn("add_trait = compliant", cede)
        self.assertGreaterEqual(
            cede.count("remove_variable = sb_natal_guns_bargain_war_var"), 2
        )

        peaceful = object_block(
            "common/scripted_effects/sb_natalia_effects.txt",
            "sb_found_natalia_peacefully",
        )
        self.assertIn("country = scope:sb_natalia_peaceful_founder_scope", peaceful)
        self.assertNotIn("country = root", peaceful)

        guns_victory = object_block(
            "common/scripted_effects/sb_natalia_effects.txt",
            "sb_found_natalia_after_guns_bargain_rejection",
        )
        self.assertLess(
            guns_victory.index("sb_found_natalia_peacefully = yes"),
            guns_victory.index("sb_assign_natalia_republic_territory = yes"),
        )

        loc = text("localization/english/sb_natal_crisis_l_english.yml")
        self.assertIn("sb_natal_crisis.026.b:0", loc)
        self.assertNotIn("sb_natal_crisis.051.", loc)
        self.assertIn(
            "sb_zulu_drift_brave:0", text("localization/english/sb_l_english.yml")
        )

    def test_klr_becomes_natalia_only_after_completing_natal_great_trek(self):
        journal = object_block(
            "common/journal_entries/1-02_sb_great_trek.txt", "je_sb_great_trek"
        )
        self.assertIn("country_definition = cd:KLR", journal)
        natal_stage = shortest_named_block_containing(
            journal, "else_if", "owns_entire_state_region = STATE_NATAL"
        )
        self.assertIn("country_definition = cd:NAL", natal_stage)
        self.assertIn("country_definition = cd:KLR", natal_stage)

        finalize = object_block(
            "common/scripted_effects/sb_trek_migration.txt",
            "sb_great_trek_finalize_republic",
        )
        natalia = shortest_named_block_containing(
            finalize, "if", "country_definition = cd:NAL"
        )
        self.assertIn("s:STATE_NATAL = { add_homeland = cu:boer }", natalia)
        self.assertIn("country_definition = cd:KLR", natalia)
        self.assertNotIn("STATE_ZULULAND", natalia)
        klr_conversion = shortest_named_block_containing(
            finalize, "if", "change_tag = NAL"
        )
        self.assertIn("country_definition = cd:KLR", klr_conversion)
        self.assertEqual(1, finalize.count("change_tag = NAL"))

    def test_british_handoff_can_span_both_states_but_homeland_cannot(self):
        colony_path = "common/scripted_effects/sb_natalia_colony_effects.txt"
        handoff = object_block(colony_path, "sb_assign_british_natal_colony_territory")
        natal = object_block_from_source(handoff, "s:STATE_NATAL", colony_path)
        zululand = object_block_from_source(handoff, "s:STATE_ZULULAND", colony_path)
        for state in (natal, zululand):
            self.assertIn("every_scope_state", state)
            self.assertIn("limit = { owner = ROOT }", state)
            self.assertIn("set_state_owner = c:NAL", state)
        self.assertIn("add_claim = c:NAL", natal)
        self.assertNotIn("add_claim = c:NAL", zululand)
        self.assertNotIn("add_homeland = cu:anglo_african", handoff)

        postwar = object_block(
            "common/decisions/sb_anglo_zulu_decisions.txt",
            "decision_sb_transfer_zululand_to_natal_colony",
        )
        handoff_effect = object_block_from_source(
            postwar, "when_taken", "decision_sb_transfer_zululand_to_natal_colony"
        )
        self.assertIn("sb_zululand_queue_british_handoff = yes", handoff_effect)
        self.assertIn("id = sb_zululand_settlement.001 days = 1 popup = yes", handoff_effect)
        self.assertIn("hidden_effect", handoff_effect)
        self.assertNotIn("add_homeland = cu:anglo_african", postwar)
        self.assertIn("value = 100", object_block_from_source(postwar, "ai_chance"))

        postwar_trigger = object_block(
            "common/scripted_triggers/sb_zululand_settlement_triggers.txt",
            "sb_zululand_under_british_postwar_control",
        )
        owner_trigger = object_block(
            "common/scripted_triggers/sb_zululand_settlement_triggers.txt",
            "sb_zululand_british_postwar_owner",
        )
        self.assertIn("c:NAL ?=", postwar_trigger)
        self.assertIn("is_subject_of = c:GBR", postwar_trigger)
        self.assertEqual(2, postwar_trigger.count("sb_zululand_british_postwar_owner = yes"))
        self.assertEqual(2, postwar_trigger.count("owns_entire_state_region = STATE_ZULULAND"))
        self.assertIn("is_ai = yes", owner_trigger)
        self.assertIn("is_subject_of = c:GBR", owner_trigger)
        handlers = text("common/on_actions/sb_diplomatic_play_on_action_handlers.txt")
        self.assertNotIn("id = sb_anglo_zulu.040", handlers)
        postwar_loc = text("localization/english/sb_eastern_sphere_l_english.yml")
        tooltip = next(
            line for line in postwar_loc.splitlines()
            if "decision_sb_transfer_zululand_to_natal_colony_tt" in line
        )
        self.assertNotIn("homeland", tooltip.casefold())

        responsible = object_block(
            "common/scripted_effects/sb_subject_autonomy_effects.txt",
            "sb_apply_responsible_colony_subject_type_from_overlord",
        )
        homeland = shortest_named_block_containing(
            responsible, "if", "sb_natal_responsible_government_homeland_granted_var"
        )
        self.assertIn("country_definition = cd:NAL", homeland)
        self.assertIn("is_subject_of = c:GBR", homeland)
        self.assertIn("s:STATE_NATAL", homeland)
        self.assertEqual(1, homeland.count("add_homeland = cu:anglo_african"))
        self.assertNotIn("STATE_ZULULAND", homeland)

    def test_anglo_zulu_ai_scheduler_has_two_player_agnostic_truce_safe_routes(self):
        monthly = object_block(
            "common/scripted_effects/sb_eastern_sphere_effects.txt",
            "sb_eastern_sphere_monthly_housekeeping",
        )
        scheduler = shortest_named_block_containing(
            monthly, "if", "target_country = c:ZUL"
        )
        scheduler_limit = object_block_from_source(
            scheduler, "limit", "Anglo-Zulu scheduler"
        )
        nal_match = re.search(r"c:NAL\s*\?=\s*\{", scheduler_limit)
        self.assertIsNotNone(nal_match)
        nal = validate.extract_braced(scheduler_limit, nal_match.start())
        zul_match = re.search(r"c:ZUL\s*\?=\s*\{", scheduler_limit)
        self.assertIsNotNone(zul_match)
        zul = validate.extract_braced(scheduler_limit, zul_match.start())
        british_gate = scheduler_limit[: nal_match.start()]
        play = object_block_from_source(
            scheduler, "create_diplomatic_play", "Anglo-Zulu scheduler"
        )
        transit_article = shortest_named_block_containing(
            scheduler_limit, "any_scope_article", "has_type = transit_rights"
        )

        self.assertIn("country_definition = cd:GBR", scheduler_limit)
        self.assertIn("is_ai = yes", scheduler_limit)
        self.assertNotIn("is_ai = yes", nal)
        self.assertIn("is_subject_of = c:GBR", nal)
        self.assertIn("sb_natalia_british_colony_resolved_var", nal)
        # The scheduler is a preflight. Britain and the Natal subject must be
        # idle before the exact annexation root is created.
        self.assertIn("is_at_war = no", british_gate)
        self.assertIn("is_active_in_diplomatic_play = no", british_gate)
        self.assertNotIn("is_at_war = no", nal)
        self.assertNotIn("is_active_in_diplomatic_play = no", nal)
        self.assertIn("is_at_war = no", zul)
        self.assertIn("is_active_in_diplomatic_play = no", zul)
        self.assertIn("NOT = { has_truce_with = c:ZUL }", scheduler_limit)
        self.assertIn("sb_imperial_confederation_scheme_is_active = yes", scheduler_limit)
        self.assertIn("country_has_primary_culture = cu:boer", scheduler_limit)
        self.assertIn("has_type = transit_rights", scheduler_limit)
        self.assertIn(
            "save_temporary_scope_as = sb_anglo_zulu_transit_receiver_scope",
            scheduler_limit,
        )
        self.assertIn("source_country = c:ZUL", transit_article)
        self.assertIn(
            "target_country = scope:sb_anglo_zulu_transit_receiver_scope",
            transit_article,
        )
        self.assertIn("game_date >= 1879.1.1", scheduler_limit)
        self.assertIn(
            "has_global_variable = sb_imperial_confederation_scheme_unlocked_var",
            scheduler_limit,
        )
        self.assertIn(
            "has_global_variable = sb_imperial_confederation_scheme_resolved_var",
            scheduler_limit,
        )
        self.assertNotIn("game_date >= 1870.1.1", scheduler)
        self.assertEqual(0, scheduler.count("set_variable = sb_anglo_zulu_pressure_active_var"))
        started = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_diplomatic_play_started",
        )
        self.assertEqual(3, started.count("set_variable = sb_anglo_zulu_pressure_active_var"))
        self.assertIn("type = dp_annex_war", play)
        self.assertIn("target_country = c:ZUL", play)
        self.assertNotIn("trigger_event", scheduler)

    def test_anglo_zulu_route_uses_vanilla_annex_and_keeps_zulu_victory_reward(self):
        plays = text("common/diplomatic_plays/sb_diplomatic_plays.txt")
        events = text("events/sb_anglo_zulu_events.txt")
        handlers = text("common/on_actions/sb_diplomatic_play_on_action_handlers.txt")
        victory = object_block("events/sb_anglo_zulu_events.txt", "sb_anglo_zulu.020")
        backdown = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_diplo_play_back_down",
        )
        war_end = object_block(
            "common/on_actions/sb_diplomatic_play_on_action_handlers.txt",
            "sb_on_spes_bona_war_end",
        )

        self.assertNotIn("dp_sb_anglo_zulu_return_state_locked", plays)
        self.assertNotIn("sb_anglo_zulu.010", events)
        self.assertNotIn("sb_anglo_zulu.030", events)
        self.assertNotIn("sb_anglo_zulu.040", events)
        self.assertIn("is_diplomatic_play_type = dp_annex_war", handlers)
        self.assertIn("has_variable = sb_anglo_zulu_pressure_active_var", handlers)
        self.assertIn("sb_boost_firearms_progress_50 = yes", victory)
        self.assertIn("c:GBR ?=", victory)
        self.assertIn("set_variable = sb_anglo_zulu_pressure_resolved_var", victory)
        self.assertIn(
            "root = { is_diplomatic_play_type = dp_annex_war initiator = c:GBR target = c:ZUL }",
            backdown,
        )
        self.assertIn("sb_british_zulu_annex_play_scope", backdown)
        self.assertIn("var:sb_british_zulu_annex_play_scope = root", backdown)
        self.assertIn("scope:actor = c:GBR", backdown)
        self.assertIn("scope:actor = c:ZUL", backdown)
        self.assertIn("set_variable = sb_british_zulu_backdown_finalizer_pending_var", backdown)
        self.assertIn("id = sb_anglo_zulu.099 days = 1", backdown)
        self.assertIn("is_diplomatic_play_type = dp_annex_war", war_end)
        self.assertIn("c:NAL ?=", war_end)
        self.assertGreaterEqual(
            war_end.count("remove_variable = sb_anglo_zulu_pressure_active_var"),
            3,
        )

    def test_klip_river_default_cession_truces_natal_and_britain_for_300_months(self):
        cession = object_block(
            "common/scripted_effects/sb_klip_river_county_effects.txt",
            "sb_klip_river_accept_zulu_cession",
        )

        self.assertEqual(2, cession.count("create_bidirectional_truce"))
        self.assertEqual(2, cession.count("months = 300"))
        self.assertIn("country = c:ZUL", cession)
        self.assertIn("c:ZUL ?=", cession)
        self.assertIn("country = c:GBR", cession)

    def test_british_natal_setup_adopts_freedom_of_conscience_and_refreshes_name(self):
        setup = object_block(
            "common/scripted_effects/sb_natalia_colony_effects.txt",
            "sb_apply_british_natal_colony_setup",
        )
        self.assertIn(
            "activate_law = law_type:law_freedom_of_conscience",
            setup,
        )
        self.assertIn(
            "evaluate_and_assign_state_hub_dynamic_names = yes",
            setup,
        )
        self.assertLess(
            setup.index("remove_primary_culture = cu:boer"),
            setup.index("evaluate_and_assign_state_hub_dynamic_names = yes"),
        )

    def test_shepstone_has_a_twenty_five_year_repeal_lock_independent_of_indenture(self):
        amendment = object_block(
            "common/amendments/sb_amendments.txt",
            "amendment_sb_shepstone_system",
        )
        can_repeal = object_block_from_source(
            amendment, "can_repeal", "amendment_sb_shepstone_system"
        )
        self.assertIn("text = sb_natal_shepstone_repeal_lock_tt", can_repeal)
        self.assertIn(
            "NOT = { has_variable = sb_natal_shepstone_repeal_locked_var }",
            can_repeal,
        )
        self.assertNotIn(
            "has_journal_entry = je_sb_natal_indenture_program_v2",
            can_repeal,
        )

        path = "common/scripted_effects/sb_natal_interwar_effects.txt"
        for effect_name in (
            "sb_natal_apply_shepstone_system",
            "sb_natal_restore_shepstone_system",
        ):
            effect = object_block(path, effect_name)
            self.assertRegex(
                effect,
                r"set_variable\s*=\s*\{\s*"
                r"name\s*=\s*sb_natal_shepstone_repeal_locked_var\s*"
                r"months\s*=\s*300\s*\}",
            )

        localization = text("localization/english/sb_natal_interwar_l_english.yml")
        self.assertIn(
            'sb_natal_shepstone_repeal_lock_tt:0 "The Shepstone System has been in force for at least #v 25 years#!."',
            localization,
        )
        self.assertIn("je_sb_natal_indenture_program_v2_goal:0", localization)

    def test_representative_southern_and_northern_content_uses_the_right_state(self):
        natal_blocks = (
            object_block(
                "common/scripted_effects/sb_natal_interwar_effects.txt",
                "sb_natal_transfer_indenture_cohort",
            ),
            object_block(
                "common/scripted_effects/sb_boer_ai_economy_effects.txt",
                "sb_boer_ai_economy_nal_sugar_plantation",
            ),
            object_block(
                "events/iberia_events/struggle_for_the_highveld_events.txt",
                "struggle_for_the_highveld.3",
            ),
            object_block(
                "events/iberia_events/struggle_for_the_highveld_events.txt",
                "struggle_for_the_highveld.5",
            ),
        )
        for block in natal_blocks:
            clean = without_comments(block)
            self.assertIn("STATE_NATAL", clean)
            self.assertNotIn("STATE_ZULULAND", clean)

        zululand_blocks = (
            object_block(
                "common/scripted_effects/sb_zululand_settlement_effects.txt",
                "sb_zululand_begin_natal_incorporation",
            ),
            object_block(
                "common/scripted_effects/sb_natal_interwar_effects.txt",
                "sb_natal_accept_trn_zulu_aid",
            ),
        )
        for block in zululand_blocks:
            clean = without_comments(block)
            self.assertIn("STATE_ZULULAND", clean)
            self.assertNotIn("STATE_NATAL", clean)


if __name__ == "__main__":
    unittest.main()
