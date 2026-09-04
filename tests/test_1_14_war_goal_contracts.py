from __future__ import annotations

from pathlib import Path
import hashlib
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = validate.find_game_root(None)
SUBJECT_PATH = "common/subject_types/sb_subject_types.txt"
GOAL_PATH = "common/war_goal_types/sb_subject_restoration_war_goals.txt"
LOCALIZATION_PATH = "localization/english/sb_war_goal_contracts_l_english.yml"
RESTORATION_MAP = {
    "subject_type_sb_responsible_colony": "sb_reestablish_responsible_colony",
    "subject_type_sb_responsible_colony_monarchy": "sb_reestablish_responsible_colony_monarchy",
    "subject_type_sb_dominion": "sb_reestablish_dominion",
    "subject_type_sb_boer_presidential_union": "sb_reestablish_boer_presidential_union",
    "subject_type_sb_boer_confederal_partner": "sb_reestablish_boer_confederal_partner",
    "subject_type_sb_cape_confederal_dependency": "sb_reestablish_cape_confederal_dependency",
    "subject_type_sb_zulu_chiefdoms": "sb_reestablish_zulu_chiefdoms",
}
DOMINION_TEMPLATE_GOALS = {
    "sb_reestablish_responsible_colony",
    "sb_reestablish_responsible_colony_monarchy",
    "sb_reestablish_dominion",
    "sb_reestablish_cape_confederal_dependency",
}
PERSONAL_UNION_TEMPLATE_GOALS = {"sb_reestablish_boer_presidential_union"}
PROTECTORATE_TEMPLATE_GOALS = {
    "sb_reestablish_boer_confederal_partner",
    "sb_reestablish_zulu_chiefdoms",
}
FORCED_REVOLUTION_TYPES = {
    "subject_type_sb_boer_presidential_union",
    "subject_type_sb_boer_confederal_partner",
    "subject_type_sb_zulu_chiefdoms",
}
BASE_SETTINGS = {
    "require_target_be_part_of_war",
    "turns_into_subject",
    "conflicts_with_make_subject",
    "validate_subject_relation",
    "validate_conflicts_make_subject",
}
EXTRA_INTEREST_SETTINGS = {"can_add_for_other_country", "requires_interest"}


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def object_block(source: str, key: str, directive: str | None = None) -> str:
    prefix = f"{directive}:" if directive else ""
    match = re.search(
        rf"^\s*(?P<key>{re.escape(prefix + key)})\s*=\s*\{{",
        source,
        re.MULTILINE,
    )
    if match is None:
        raise AssertionError(f"missing {prefix}{key}")
    return validate.extract_braced(source, match.start("key"))


def compact_script(source: str) -> str:
    without_comments = re.sub(r"#.*", "", source)
    return re.sub(r"\s+", "", without_comments)


def bare_setting_names(settings: str) -> set[str]:
    return {
        match.group(1)
        for match in re.finditer(r"^\s*([a-z][a-z0-9_]*)\s*(?:#.*)?$", settings, re.MULTILINE)
    }


def scalar(block: str, field: str) -> str:
    matches = re.findall(rf"^\s*{re.escape(field)}\s*=\s*([^#\s]+)", block, re.MULTILINE)
    if len(matches) != 1:
        raise AssertionError(f"expected one {field}, found {len(matches)}")
    return matches[0]


class FocusedOverrideRebaseTests(unittest.TestCase):
    def test_bic_uses_evaluated_actor_and_keeps_responsible_colony_tier(self):
        source = text("common/dynamic_country_names/sb_dynamic_names.txt")
        bic = object_block(source, "BIC", "REPLACE")
        self.assertEqual(
            "d764da8000ca8e2ca1d771123e5094e63d75c6f34401d06f1d9bc050f3125c42",
            hashlib.sha256(bic.encode("utf-8")).hexdigest(),
        )
        self.assertEqual(1, bic.count("who = scope:actor"))
        self.assertNotIn("who = c:BIC", bic)
        self.assertIn("priority = 60", bic)
        self.assertEqual(
            2,
            len(re.findall(r"subject_type_sb_responsible_colony(?!_monarchy)", bic)),
        )
        self.assertEqual(2, bic.count("subject_type_sb_responsible_colony_monarchy"))

    def test_saf_custom_replacement_is_intentionally_unchanged(self):
        source = text("common/dynamic_country_names/sb_dynamic_names.txt")
        saf = object_block(source, "SAF", "REPLACE")
        self.assertEqual(
            "d83ba0fe0dcf37b83f4d69260a05408d68da70c6edc911fa877144ddbf822e68",
            hashlib.sha256(saf.encode("utf-8")).hexdigest(),
        )
        self.assertIn("dyn_c_sb_confederated_states_of_southern_africa", saf)
        self.assertIn("dyn_c_sb_union_of_south_africa", saf)

    def test_vanilla_dominion_restores_itself_but_keeps_no_auto_join(self):
        source = text("common/subject_types/zz_sb_dominion_override.txt")
        dominion = object_block(source, "subject_type_dominion", "REPLACE")
        self.assertEqual(
            "4245cf6bb01386d3647fe1d786946c63d5aee5872cb1c6e932c5a05a8031d1fb",
            hashlib.sha256(dominion.encode("utf-8")).hexdigest(),
        )
        self.assertEqual("make_dominion", scalar(dominion, "re_establish_war_goal"))
        self.assertEqual("no", scalar(dominion, "join_overlord_wars"))

    def test_armed_forces_keeps_ob1_executable_body_plus_one_sb_consumer(self):
        source = text("common/interest_groups/zz_sb_armed_forces_override.txt")
        armed_forces = object_block(source, "ig_armed_forces", "REPLACE")
        consumer = "add = owner.modifier:country_sb_aristocrats_armed_forces_attraction_add"
        self.assertEqual(1, armed_forces.count(consumer))
        self.assertIn("Vanilla 1.14.0", source.splitlines()[0])
        self.assertIn(
            "c010ec05625f29a1e2691e49b1b30a2900cfce46553d8a9c2c7f248a1ae3e119",
            source.splitlines()[1],
        )
        self.assertEqual(
            "4b961ed71e7b4d12539cc818175366849b0d49435677957d9f3eb269609bb05c",
            hashlib.sha256(armed_forces.encode("utf-8")).hexdigest(),
        )

    @unittest.skipIf(GAME_ROOT is None, "Vanilla game root unavailable")
    def test_armed_forces_token_stream_matches_ob1_after_removing_sb_delta(self):
        mod = object_block(
            text("common/interest_groups/zz_sb_armed_forces_override.txt"),
            "ig_armed_forces",
            "REPLACE",
        ).replace("REPLACE:ig_armed_forces", "ig_armed_forces", 1)
        upstream_source = (GAME_ROOT / "common/interest_groups/00_armed_forces.txt").read_text(
            encoding="utf-8-sig"
        )
        upstream = object_block(upstream_source, "ig_armed_forces")
        consumer = "add = owner.modifier:country_sb_aristocrats_armed_forces_attraction_add"
        self.assertEqual(compact_script(upstream), compact_script(mod.replace(consumer, "", 1)))


class SubjectRestorationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.subject_source = text(SUBJECT_PATH)
        cls.goal_source = text(GOAL_PATH)

    def test_exact_seven_subject_to_goal_mappings(self):
        actual = {}
        for subject_type in RESTORATION_MAP:
            block = object_block(self.subject_source, subject_type)
            actual[subject_type] = scalar(block, "re_establish_war_goal")
        self.assertEqual(RESTORATION_MAP, actual)
        self.assertEqual(7, self.subject_source.count("re_establish_war_goal ="))

    def test_sb_dominion_restoration_keeps_no_auto_join(self):
        block = object_block(self.subject_source, "subject_type_sb_dominion")
        self.assertEqual("sb_reestablish_dominion", scalar(block, "re_establish_war_goal"))
        self.assertEqual("no", scalar(block, "join_overlord_wars"))

    def test_forced_overlord_revolution_set_is_exactly_the_three_locked_types(self):
        actual_forced = set()
        actual_locked = set()
        for subject_type in RESTORATION_MAP:
            block = object_block(self.subject_source, subject_type)
            if "forced_into_overlord_revolution = yes" in block:
                actual_forced.add(subject_type)
            if scalar(block, "can_start_own_diplomatic_plays") == "no":
                actual_locked.add(subject_type)
        self.assertEqual(FORCED_REVOLUTION_TYPES, actual_forced)
        self.assertEqual(FORCED_REVOLUTION_TYPES, actual_locked)
        self.assertEqual(3, self.subject_source.count("forced_into_overlord_revolution = yes"))
        self.assertNotIn("forced_into_overlord_revolution = no", self.subject_source)

    def test_restoration_goal_key_set_is_exact(self):
        actual = set(
            re.findall(r"^(sb_reestablish_[a-z0-9_]+)\s*=\s*\{", self.goal_source, re.MULTILINE)
        )
        self.assertEqual(set(RESTORATION_MAP.values()), actual)
        self.assertEqual(7, len(actual))

    def test_every_goal_has_exact_core_fields_and_zero_costs(self):
        inverse_map = {goal: subject for subject, goal in RESTORATION_MAP.items()}
        for goal, subject_type in inverse_map.items():
            block = object_block(self.goal_source, goal)
            with self.subTest(goal=goal):
                self.assertEqual("make_subject", scalar(block, "kind"))
                self.assertEqual(subject_type, scalar(block, "subject_type"))
                self.assertEqual("country", scalar(block, "target_type"))
                self.assertEqual("on_capitulation", scalar(block, "side_switch"))
                self.assertEqual(
                    "possible={always=no}",
                    compact_script(object_block(block, "possible")),
                )
                self.assertEqual(
                    "maneuvers={value=0}",
                    compact_script(object_block(block, "maneuvers")),
                )
                self.assertEqual(
                    "infamy={value=0}",
                    compact_script(object_block(block, "infamy")),
                )
                self.assertEqual(
                    "mirrored_wargoal={method=subjugate}",
                    compact_script(object_block(block, "mirrored_wargoal")),
                )
                self.assertNotIn("fill_per_week", block)
                self.assertNotIn("deplete_per_week", block)

    def test_template_families_have_exact_settings_icons_and_priorities(self):
        for goal in RESTORATION_MAP.values():
            block = object_block(self.goal_source, goal)
            settings = bare_setting_names(object_block(block, "settings"))
            if goal in DOMINION_TEMPLATE_GOALS:
                expected_icon = '"gfx/interface/icons/war_goals/make_dominion.dds"'
                expected_priority = "14"
                expected_settings = BASE_SETTINGS | EXTRA_INTEREST_SETTINGS
            elif goal in PERSONAL_UNION_TEMPLATE_GOALS:
                expected_icon = '"gfx/interface/icons/war_goals/make_dominion.dds"'
                expected_priority = "12"
                expected_settings = BASE_SETTINGS
            else:
                self.assertIn(goal, PROTECTORATE_TEMPLATE_GOALS)
                expected_icon = '"gfx/interface/icons/war_goals/make_protectorate.dds"'
                expected_priority = "12"
                expected_settings = BASE_SETTINGS | EXTRA_INTEREST_SETTINGS
            with self.subTest(goal=goal):
                self.assertEqual(expected_settings, settings)
                self.assertEqual(expected_icon, scalar(block, "icon"))
                self.assertEqual(expected_priority, scalar(block, "execution_priority"))
                self.assertEqual(
                    "control_half_target_country_states",
                    scalar(block, "contestion_type"),
                )
                self.assertEqual("yes", scalar(object_block(block, "ai"), "is_significant_demand"))

    def test_technical_localization_is_bom_marked_unreviewed_and_complete(self):
        path = ROOT / LOCALIZATION_PATH
        self.assertTrue(path.read_bytes().startswith(b"\xef\xbb\xbf"))
        source = text(LOCALIZATION_PATH)
        self.assertIn("# TO REVIEW (non-event/JE keys)", source)
        self.assertNotIn("### TO REVIEW ###", source)
        self.assertNotIn("### REVIEWED ###", source)
        expected = {
            f"war_goal_{goal}{suffix}"
            for goal in RESTORATION_MAP.values()
            for suffix in ("_type_name", "_type_desc", "", "_desc")
        }
        actual = {
            key
            for key in re.findall(
                r"^\s+(war_goal_[A-Za-z0-9_]+):(?:0\s+)?",
                source,
                re.MULTILINE,
            )
            if key.startswith("war_goal_sb_reestablish_")
        }
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
