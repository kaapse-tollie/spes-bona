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
    matches = [
        block
        for block in nested_blocks(state_block, "set_owner_of_provinces")
        if re.search(rf"\bcountry\s*=\s*c:{re.escape(country)}\b", block)
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
        self.assertIn("activate_law = law_type:law_frontier_colonization", setup)
        self.assertIn("name = sb_trek_frontier_drive", setup)

    def test_peaceful_highveld_option_delegates_to_the_canonical_founder(self):
        path = "events/iberia_events/struggle_for_the_highveld_events.txt"
        event = object_block(path, "struggle_for_the_highveld.4")
        peaceful = named_option(event, "struggle_for_the_highveld.4.c")

        self.assertEqual(1, peaceful.count("sb_found_natalia_peacefully = yes"))
        self.assertIn("s:STATE_NATAL", peaceful)
        self.assertIn("remove_claim = c:ZUL", peaceful)
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

    def test_core_ultimatum_is_delayed_but_port_natal_starts_it_immediately(self):
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
        self.assertIn("NOT = { has_variable = sb_british_natal_ultimatum_var }", delayed)
        self.assertIn(
            "NOT = { has_variable = sb_british_natal_ultimatum_pending_var }",
            delayed,
        )
        self.assertIn("NOT = { has_variable = sb_natalia_british_colony_resolved_var }", delayed)

        decision = object_block(
            "common/decisions/sb_zulu_decisions.txt", "natalia_raid_port_natal"
        )
        shown = object_block_from_source(decision, "is_shown", "natalia_raid_port_natal")
        taken = object_block_from_source(decision, "when_taken", "natalia_raid_port_natal")
        self.assertIn("NOT = { has_variable = sb_natalia_port_natal_raid_taken_var }", shown)
        self.assertIn("NOT = { has_variable = sb_natalia_british_colony_resolved_var }", shown)
        self.assertIn("set_variable = sb_british_natal_ultimatum_var", taken)
        self.assertIn("remove_variable = sb_british_natal_ultimatum_pending_var", taken)
        self.assertIn("set_variable = sb_natalia_port_natal_raid_taken_var", taken)
        natal = object_block_from_source(taken, "s:STATE_NATAL", "natalia_raid_port_natal")
        self.assertEqual({"x279045"}, validate.object_values(natal, "provinces"))

        ultimatum = object_block("events/sb_natal_crisis_events.txt", "sb_natal_crisis.100")
        trigger = object_block_from_source(ultimatum, "trigger", "sb_natal_crisis.100")
        immediate = object_block_from_source(ultimatum, "immediate", "sb_natal_crisis.100")
        self.assertIn("NOT = { has_variable = sb_british_natal_ultimatum_var }", trigger)
        self.assertIn("remove_variable = sb_british_natal_ultimatum_pending_var", immediate)

    def test_klip_river_county_and_reduced_natalia_keep_explicit_boundaries(self):
        effects_path = "common/scripted_effects/sb_klip_river_county_effects.txt"
        create_county = object_block(effects_path, "sb_klip_river_create_county")
        natal = object_block_from_source(create_county, "s:STATE_NATAL", effects_path)
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
        self.assertIn("s:STATE_NATAL", recognition)
        self.assertIn("remove_claim = c:ZUL", recognition)
        self.assertNotIn("STATE_ZULULAND", recognition)

        guns_acceptance = named_option(
            object_block("events/sb_natal_crisis_events.txt", "sb_natal_crisis.025"),
            "sb_natal_crisis.025.a",
        )
        self.assertIn("s:STATE_NATAL", guns_acceptance)
        self.assertIn("remove_claim = c:ZUL", guns_acceptance)
        self.assertNotIn("STATE_ZULULAND", guns_acceptance)

        reduced = object_block(effects_path, "sb_klip_river_finalize_reduced_natalia")
        reduced_natal = object_block_from_source(reduced, "s:STATE_NATAL", effects_path)
        reduced_zululand = object_block_from_source(
            reduced, "s:STATE_ZULULAND", effects_path
        )
        self.assertEqual(KLR_NATAL_PROVINCES, owner_provinces(reduced_natal, "KLR"))
        self.assertIn("xE1E455", owner_provinces(reduced_zululand, "ZUL"))
        self.assertNotIn("country = c:KLR", reduced_zululand)

    def test_great_trek_adds_the_nal_boer_homeland_to_natal_only(self):
        finalize = object_block(
            "common/scripted_effects/sb_trek_migration.txt",
            "sb_great_trek_finalize_republic",
        )
        natalia = shortest_named_block_containing(
            finalize, "if", "country_definition = cd:NAL"
        )
        self.assertIn("s:STATE_NATAL = { add_homeland = cu:boer }", natalia)
        self.assertNotIn("STATE_ZULULAND", natalia)

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

        postwar = named_option(
            object_block("events/sb_anglo_zulu_events.txt", "sb_anglo_zulu.040"),
            "sb_anglo_zulu.040.a",
        )
        self.assertIn("state_region = s:STATE_NATAL", postwar)
        self.assertIn("state_region = s:STATE_ZULULAND", postwar)
        self.assertIn("set_state_owner = c:NAL", postwar)
        self.assertNotIn("add_homeland = cu:anglo_african", postwar)
        postwar_loc = text("localization/english/sb_eastern_sphere_l_english.yml")
        tooltip = next(
            line for line in postwar_loc.splitlines()
            if "sb_anglo_zulu_040_handoff_tt" in line
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

    def test_representative_southern_and_northern_content_uses_the_right_state(self):
        natal_blocks = (
            object_block(
                "common/scripted_effects/sb_natal_interwar_effects.txt",
                "sb_natal_select_indenture_origin_and_create_migration",
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
            object_block("events/sb_anglo_zulu_events.txt", "sb_anglo_zulu.010"),
            object_block(
                "common/scripted_effects/sb_natal_interwar_effects.txt",
                "sb_natal_restore_zululand_as_puppet",
            ),
            object_block(
                "common/scripted_effects/sb_natal_interwar_effects.txt",
                "sb_natal_create_trn_zulu_arms_treaty",
            ),
        )
        for block in zululand_blocks:
            clean = without_comments(block)
            self.assertIn("STATE_ZULULAND", clean)
            self.assertNotIn("STATE_NATAL", clean)


if __name__ == "__main__":
    unittest.main()
