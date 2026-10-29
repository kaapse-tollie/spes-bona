from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def object_block(path: str, name: str) -> str:
    source = text(path)
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} in {path}")
    return validate.extract_braced(source, match.start())


class StartupStoryPatchTests(unittest.TestCase):
    def test_mpande_uses_vanilla_balance_of_power_strategy_on_accession(self):
        router = object_block("common/on_actions/sb_on_actions.txt", "on_new_ruler")
        handler = object_block(
            "common/on_actions/sb_regional_on_action_handlers.txt",
            "sb_on_zulu_mpande_new_ruler",
        )

        self.assertIn("sb_on_zulu_mpande_new_ruler", router)
        self.assertIn("has_template = ZUL_mpande_zulu", handler)
        self.assertIn("country_definition = cd:ZUL", handler)
        self.assertIn("is_ai = yes", handler)
        self.assertIn("is_subject = no", handler)
        self.assertIn("set_strategy = ai_strategy_maintain_power_balance", handler)

    def test_starting_journal_entries_are_history_authored(self):
        expected = {
            "common/history/countries/zul - zulu.txt": (
                "je_sb_adopt_firearms",
                "je_sb_zulu_kingdom",
            ),
            "common/history/countries/bst - basuto.txt": (
                "je_sb_adopt_firearms",
            ),
            "common/history/countries/swz - swaziland.txt": (
                "je_sb_adopt_firearms",
            ),
            "common/history/countries/gza - gaza.txt": (
                "je_sb_adopt_firearms",
            ),
        }
        for path, journals in expected.items():
            history = text(path)
            for journal in journals:
                self.assertIn(f"add_journal_entry = {{ type = {journal} }}", history)

        self.assertNotIn(
            "add_contextless_journal_entry = je_sb_bst_ora_frontier",
            text("common/history/countries/bst - basuto.txt"),
        )
        global_history = object_block(
            "common/history/global/sb_contextless_journal_entries.txt", "GLOBAL"
        )
        self.assertIn(
            "add_contextless_journal_entry = je_sb_bst_ora_frontier",
            global_history,
        )

        nguni_formation = object_block(
            "common/scripted_effects/sb_nguni_effects.txt",
            "sb_nguni_apply_formation_inheritance",
        )
        self.assertIn(
            "add_journal_entry = { type = je_sb_adopt_firearms }",
            nguni_formation,
        )

    def test_day_one_intro_events_are_scheduled_after_lobby(self):
        # PLAN-zul-ngi-playtest-fixes: setup-phase scheduled popups were silently
        # discarded; all four intro events must be scheduled from the after-lobby
        # on_action and no longer from the history files.
        after_lobby = object_block(
            "common/on_actions/sb_startup_on_action_handlers.txt",
            "sb_on_game_started_after_lobby",
        )
        schedules = {
            "c:ZUL": "sb_zulu_dynasty.001",
            "c:ORA": "sb_great_trek.003",
            "c:BST": "sb_bst_frontier.001",
            "c:GZA": "sb_gaza.001",
        }
        for country, event_id in schedules.items():
            pattern = (
                rf"{country} \?=\s*\{{\s*"
                rf"trigger_event = \{{ id = {event_id} days = 1 popup = yes \}}\s*\}}"
            )
            self.assertRegex(after_lobby, pattern)

        for rel, event_id in {
            "common/history/countries/zul - zulu.txt": "sb_zulu_dynasty.001",
            "common/history/countries/ora - oranje.txt": "sb_great_trek.003",
            "common/history/countries/bst - basuto.txt": "sb_bst_frontier.001",
            "common/history/countries/gza - gaza.txt": "sb_gaza.001",
        }.items():
            self.assertNotIn(f"trigger_event = {{ id = {event_id}", text(rel))

        zulu = object_block("events/sb_zulu_dynasty_events.txt", "sb_zulu_dynasty.001")
        self.assertEqual(1, zulu.count("\n\toption = {"))
        self.assertIn("has_template = ZUL_dingane", zulu)
        self.assertIn("any_scope_character = {", zulu)
        self.assertIn("random_scope_character = {", zulu)
        self.assertNotIn("\n\t\truler = {", zulu)
        self.assertIn("has_journal_entry = je_sb_zulu_kingdom", zulu)
        self.assertIn("name = sb_zulu_dynastic_crisis", zulu)
        self.assertIn("months = -1", zulu)

        oranje = object_block("events/sb_great_trek_events.txt", "sb_great_trek.003")
        self.assertEqual(1, oranje.count("\n\toption = {"))
        self.assertIn("has_journal_entry = je_sb_great_trek", oranje)
        self.assertIn("name = sb_trek_frontier_drive", oranje)
        self.assertIn("months = 120", oranje)

        basutoland = object_block(
            "events/sb_bst_frontier_events.txt", "sb_bst_frontier.001"
        )
        self.assertEqual(1, basutoland.count("\n\toption = {"))
        self.assertIn("has_journal_entry = je_sb_bst_ora_frontier", basutoland)
        self.assertIn("has_template = BST_Moshoeshoe", basutoland)
        self.assertIn("any_scope_character = {", basutoland)
        self.assertIn("random_scope_character = {", basutoland)
        self.assertNotIn("\n\t\truler = {", basutoland)
        self.assertIn("add_trait = sb_moshoeshoe_lifeline", basutoland)

        moshoeshoe = object_block(
            "common/character_templates/sb_southern_africa_character_template_overrides.txt",
            "REPLACE:BST_Moshoeshoe",
        )
        self.assertNotIn("sb_moshoeshoe_lifeline", moshoeshoe)

    def test_intro_prose_covers_each_requested_starting_situation(self):
        zulu = text("localization/english/sb_zulu_dynasty_l_english.yml")
        for term in ("Shaka", "Boer", "British"):
            self.assertIn(term, zulu)

        oranje = text("localization/english/sb_great_trek_l_english.yml")
        for term in (
            "Boer families",
            "British",
            "republic",
            "trekkers",
            "Ndebele",
            "Basotho",
            "Zulu",
        ):
            self.assertIn(term, oranje)

        basutoland = text("localization/english/sb_bst_l_english.yml")
        for term in ("Voortrekker", "British", "Sotho-Tswana"):
            self.assertIn(term, basutoland)

    def test_dynastic_stability_bar_displays_its_numeric_value(self):
        progress_bar = object_block(
            "common/scripted_progress_bars/sb_progress_bars.txt",
            "sb_zulu_dynastic_stability_bar",
        )
        self.assertIn('desc = "sb_zulu_dynastic_stability_bar_low"', progress_bar)
        gui = text("gui/sb_prerogative_progress_bars.gui")
        self.assertIn('text = "sb_prerogative_live_readout"', gui)
        localization = text("localization/english/sb_institutions_l_english.yml")
        readout = re.search(r'^\s*sb_prerogative_live_readout:[^\n]+', localization, re.MULTILINE)
        self.assertIsNotNone(readout)
        self.assertIn(
            "[JournalEntry.GetCountry.MakeScope.Var('sb_prerogative_var').GetValue|1]",
            readout.group(),
        )

    def test_history_authored_journals_have_no_inactive_auto_stub(self):
        journal_entries = {
            "common/journal_entries/1-04_sb_firearms_acquisition.txt":
                "je_sb_adopt_firearms",
            "common/journal_entries/1-03_sb_zulu_kingdom.txt":
                "je_sb_zulu_kingdom",
            "common/journal_entries/1-07_sb_bst_frontier.txt":
                "je_sb_bst_ora_frontier",
        }
        for path, journal in journal_entries.items():
            self.assertNotIn("is_shown_when_inactive", object_block(path, journal))

    def test_prerogative_initializes_values_before_recalculation(self):
        effect = object_block("common/scripted_effects/sb_institutions_effects.txt", "sb_institutions_recalculate")
        self.assertLess(effect.index("sb_institutions_initialize = yes"), effect.index("value = sb_prerogative_target"))
        initialize = object_block("common/scripted_effects/sb_institutions_effects.txt", "sb_institutions_initialize")
        self.assertIn("NOT = { has_variable = sb_institutions_initialized_var }", initialize)
        self.assertIn("name = sb_prerogative_cooperation_var value = 0", initialize)
        bar = object_block("common/scripted_progress_bars/sb_progress_bars.txt", "sb_zulu_dynastic_stability_bar")
        self.assertNotIn("monthly_progress", bar)

if __name__ == "__main__":
    unittest.main()
