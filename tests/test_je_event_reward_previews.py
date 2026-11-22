from pathlib import Path
import re
import unittest

from tests.je_outcomes import direct_fields, outcome_field, outcome_nodes

from tools import validate


ROOT = Path(__file__).resolve().parents[1]

COMPLETION_PREVIEWS = {
    "je_sb_transvaal_unity": ("event_effects_sb_transvaal_unity_tt",),
    "je_sb_consolidation_of_south_west_africa": (
        "event_effects_sb_nam.140_direct_tt",
        "sb_nam_140_exterminatory_tt",
        "sb_nam_140_extractive_tt",
        "sb_nam_140_charter_tt",
        "sb_nam_140_mission_tt",
    ),
    "je_sb_map_namibian_coast": ("sb_nam_014_a_tt",),
    "je_sb_consolidating_gaza": ("event_effects_sb_gaza.090_tt",),
    "je_sb_delagoa_route_to_sea": ("event_effects_sb_delagoa.020_tt",),
    "je_sb_bechuanaland_corridor": (
        "event_effects_sb_bechuanaland_corridor.040_tt",
    ),
    "je_sb_rhodesian_venture": ("sb_rhodesian_venture_success_tt",),
    "je_sb_natal_indenture_program_v2": ("sb_natal_indian_ethnogenesis_tt",),
}

NATIVE_COMPLETION_PREVIEWS = {
    "je_sb_adopt_firearms": "sb_apply_firearms_completion_rewards",
    "je_sb_bst_ora_frontier": "custom_tooltip = sb_bst_frontier_300_boer_settlers_tt",
}

FAILURE_PREVIEWS = {
    "je_sb_map_namibian_coast": ("sb_nam_015_a_tt",),
    "je_sb_consolidating_gaza": ("event_effects_sb_gaza.095_tt",),
    "je_sb_bechuanaland_corridor": (
        "event_effects_sb_bechuanaland_corridor.041_boer_tt",
        "event_effects_sb_bechuanaland_corridor.041_swa_tt",
        "event_effects_sb_bechuanaland_corridor.041_tied_tt",
    ),
    "je_sb_rhodesian_venture": ("event_effects_sb_rhodesian_venture.011_tt",),
}


def journal_blocks() -> dict[str, str]:
    blocks = {}
    for path in sorted((ROOT / "common/journal_entries").glob("*.txt")):
        source = validate.mask_script_comments(path.read_text(encoding="utf-8-sig"))
        for match in re.finditer(r"^\s*(je_sb_[A-Za-z0-9_]+)\s*=\s*\{", source, re.MULTILINE):
            blocks[match.group(1)] = validate.extract_braced(source, match.start())
    return blocks


def field_block(journal: str, field: str) -> str:
    match = re.search(rf"^\s*{field}\s*=\s*\{{", journal, re.MULTILINE)
    if match is None:
        return ""
    return validate.extract_braced(journal, match.start())


def localization_keys() -> set[str]:
    keys = set()
    for path in sorted((ROOT / "localization/english").glob("*.yml")):
        source = path.read_text(encoding="utf-8-sig")
        keys.update(re.findall(r"^\s*([A-Za-z0-9_.]+):\d*\s", source, re.MULTILINE))
    return keys


class JournalEventRewardPreviewTests(unittest.TestCase):
    def setUp(self):
        self.journals = journal_blocks()
        self.localization = localization_keys()

    def test_completion_event_rewards_have_vanilla_style_previews(self):
        for journal_name, expected_keys in COMPLETION_PREVIEWS.items():
            with self.subTest(journal=journal_name):
                outcome = outcome_field(self.journals[journal_name], "complete", "event_outcome_desc")
                self.assertTrue(outcome, f"{journal_name} has no completion outcome preview")
                for key in expected_keys:
                    self.assertIn(f"desc = {key}", outcome)

    def test_meaningful_failure_events_have_previews(self):
        for journal_name, expected_keys in FAILURE_PREVIEWS.items():
            with self.subTest(journal=journal_name):
                outcome = outcome_field(self.journals[journal_name], "fail", "event_outcome_desc")
                self.assertTrue(outcome, f"{journal_name} has no failure outcome preview")
                for key in expected_keys:
                    self.assertIn(f"desc = {key}", outcome)

    def test_direct_completion_event_dispatches_cannot_hide_rewards(self):
        missing = []
        for journal_name, journal in self.journals.items():
            if 'color = "gold_positive"' not in journal:
                continue
            if journal_name == "je_sb_cape_politics":
                # Cape now has five independently displayed native outcomes;
                # all routes and shared dispatch are checked below and in the
                # exhaustive pre-change comparison fixture.
                continue
            on_complete = outcome_field(journal, "complete", "effect")
            if "trigger_event" not in on_complete:
                continue
            native_preview = field_block(on_complete, "show_as_tooltip")
            native_reward = NATIVE_COMPLETION_PREVIEWS.get(journal_name)
            if not outcome_field(journal, "complete", "event_outcome_desc") and not (
                native_reward and native_reward in native_preview
            ):
                missing.append(journal_name)
        self.assertEqual([], missing)

    def test_cape_exposes_each_ending_and_caledon_has_no_false_alternatives(self):
        endings = [dict(direct_fields(v)) for k, v in direct_fields(self.journals["je_sb_cape_politics"])
                   if k == "outcome" and 'color = "gold_positive"' in v]
        self.assertEqual(5, len(endings))
        for fields, number in zip(endings, ("125", "100", "101", "102", "104")):
            self.assertEqual(f"sb_cape.{number}.t", fields["header"])
            self.assertEqual("je_standard_on_completion_header", fields["effect_header"])
            self.assertIn(f"EVENT = sb_cape.{number}", fields["effect"])
            self.assertIn(f"desc = event_effects_sb_cape.{number}_tt", fields["event_outcome_desc"])
            self.assertIn(f"event_effects_sb_cape.{number}_tt", self.localization)
        for kind in ("complete", "fail"):
            self.assertFalse(outcome_field(self.journals["je_sb_bst_ora_frontier"], kind, "event_outcome_desc"))

    def test_single_firearms_outcome_uses_native_effects_and_modifier_breakdown(self):
        journal = self.journals["je_sb_adopt_firearms"]
        self.assertFalse(outcome_field(journal, "complete", "event_outcome_desc"))
        on_complete = outcome_field(journal, "complete", "effect")
        helper = NATIVE_COMPLETION_PREVIEWS["je_sb_adopt_firearms"]
        self.assertIn(f"{helper} = yes", field_block(on_complete, "show_as_tooltip"))
        event = (ROOT / "events/sb_firearms_events.txt").read_text(encoding="utf-8-sig")
        self.assertIn(f"{helper} = yes", field_block(event, "option"))
        effects = (ROOT / "common/scripted_effects/sb_firearms_effects.txt").read_text(encoding="utf-8-sig")
        reward = field_block(effects, helper)
        modifier = field_block(reward, "add_modifier")
        self.assertIn("name = sb_new_tactics", modifier)
        self.assertIn("days = 1825", modifier)
        self.assertNotIn("custom_tooltip", reward)
        self.assertNotIn("dynastic_stability", reward + event)
        self.assertNotIn("prerogative", reward + event)

    def test_firearms_completion_exposes_only_its_named_requirement(self):
        complete = outcome_field(self.journals["je_sb_adopt_firearms"], "complete", "trigger")
        requirement = field_block(complete, "custom_tooltip")
        self.assertIn("text = je_sb_adopt_firearms_completion_tt", requirement)
        self.assertIn("has_variable = sb_firearms_modernized_var", requirement)
        self.assertIn("var:sb_firearms_supply_weeks_var >= 260", requirement)
        self.assertNotIn("has_variable", complete.replace(requirement, ""))
        self.assertNotIn("var:", complete.replace(requirement, ""))

    def test_preview_localization_resolves(self):
        expected = {
            key
            for keys in (*COMPLETION_PREVIEWS.values(), *FAILURE_PREVIEWS.values())
            for key in keys
        }
        self.assertEqual([], sorted(expected - self.localization))

    def test_reward_preview_descriptions_have_explicit_trigger_guards(self):
        problems = []
        for journal_name in COMPLETION_PREVIEWS:
            journal = self.journals[journal_name]
            outcomes = [outcome_field(journal, "complete", "event_outcome_desc")]
            if journal_name in FAILURE_PREVIEWS:
                outcomes.append(outcome_field(journal, "fail", "event_outcome_desc"))
            for outcome in outcomes:
                for match in re.finditer(r"^\s*triggered_desc\s*=\s*\{", outcome, re.MULTILINE):
                    description = validate.extract_braced(outcome, match.start())
                    if not re.search(r"^\s*trigger\s*=\s*\{", description, re.MULTILINE):
                        problems.append(journal_name)
        self.assertEqual([], problems)


if __name__ == "__main__":
    unittest.main()
