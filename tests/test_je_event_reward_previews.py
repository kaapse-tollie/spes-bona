from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]

COMPLETION_PREVIEWS = {
    "je_sb_cape_politics": (
        "event_effects_sb_cape.100_tt",
        "event_effects_sb_cape.101_tt",
        "event_effects_sb_cape.102_tt",
        "event_effects_sb_cape.104_tt",
        "event_effects_sb_cape.125_tt",
    ),
    "je_sb_zulu_kingdom": (
        "event_effects_sb_zulu_dynasty.093_dingane_tt",
        "event_effects_sb_zulu_dynasty.093_mpande_tt",
        "event_effects_sb_zulu_dynasty.093_other_tt",
    ),
    "je_sb_adopt_firearms": ("event_effects_sb_firearms.001_tt",),
    "je_sb_transvaal_unity": ("event_effects_sb_transvaal_unity_tt",),
    "je_sb_bst_ora_frontier": ("sb_bst_frontier_300_boer_settlers_tt",),
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
                outcome = field_block(self.journals[journal_name], "event_outcome_completed_desc")
                self.assertTrue(outcome, f"{journal_name} has no completion outcome preview")
                for key in expected_keys:
                    self.assertIn(f"desc = {key}", outcome)

    def test_meaningful_failure_events_have_previews(self):
        for journal_name, expected_keys in FAILURE_PREVIEWS.items():
            with self.subTest(journal=journal_name):
                outcome = field_block(self.journals[journal_name], "event_outcome_failed_desc")
                self.assertTrue(outcome, f"{journal_name} has no failure outcome preview")
                for key in expected_keys:
                    self.assertIn(f"desc = {key}", outcome)

    def test_direct_completion_event_dispatches_cannot_hide_rewards(self):
        missing = []
        for journal_name, journal in self.journals.items():
            on_complete = field_block(journal, "on_complete")
            if "trigger_event" not in on_complete:
                continue
            if not field_block(journal, "event_outcome_completed_desc"):
                missing.append(journal_name)
        self.assertEqual([], missing)

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
            outcomes = [field_block(journal, "event_outcome_completed_desc")]
            if journal_name in FAILURE_PREVIEWS:
                outcomes.append(field_block(journal, "event_outcome_failed_desc"))
            for outcome in outcomes:
                for match in re.finditer(r"^\s*triggered_desc\s*=\s*\{", outcome, re.MULTILINE):
                    description = validate.extract_braced(outcome, match.start())
                    if not re.search(r"^\s*trigger\s*=\s*\{", description, re.MULTILINE):
                        problems.append(journal_name)
        self.assertEqual([], problems)


if __name__ == "__main__":
    unittest.main()
