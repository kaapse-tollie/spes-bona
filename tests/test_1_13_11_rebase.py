import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CMF_ID = "com.github.Victoria-3-Modding-Co-op.Community-Mod-Framework"
ALLOWED_CORRIDOR_GLOBALS = {
    "sb_bechuanaland_corridor_watch_global_var",
    "sb_bechuanaland_corridor_open_global_var",
    "sb_bechuanaland_corridor_resolved_global_var",
    "sb_bechuanaland_terminal_outcome_invalid_global_var",
    "sb_bechuanaland_terminal_outcome_british_global_var",
    "sb_bechuanaland_terminal_outcome_boer_global_var",
    "sb_bechuanaland_terminal_outcome_swa_global_var",
}


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


class RebaseTests(unittest.TestCase):
    def test_release_metadata_targets_1_13_11_and_cmf_1_63_x(self):
        self.assertIn('supported_version="1.13.11"', text("descriptor.mod"))
        self.assertIn('version="0.19.7"', text("descriptor.mod"))
        metadata = json.loads(text(".metadata/metadata.json"))
        self.assertEqual("1.13.11", metadata["supported_game_version"])
        self.assertEqual("0.19.7", metadata["version"])
        relationships = [item for item in metadata["relationships"] if item["id"] == CMF_ID]
        self.assertEqual(["1.63.*"], [item["version"] for item in relationships])

    def test_1_13_11_hotfix_files_remain_vanilla_owned(self):
        self.assertFalse((ROOT / "common/production_methods/04_plantations.txt").exists())
        self.assertFalse((ROOT / "events/tech_events/military_tech_events.txt").exists())

    def test_corridor_has_one_named_container_and_no_debug_scan(self):
        effects = text("common/scripted_effects/sb_bechuanaland_corridor_effects.txt")
        self.assertEqual(1, effects.count("name = sb_bechuanaland_corridor_state"))
        self.assertIn("tags = { sb_story sb_bechuanaland_corridor }", effects)
        self.assertIn("parent = c:GBR", effects)
        self.assertIn("destroy_container = yes", effects)
        corridor_files = "\n".join(
            path.read_text(encoding="utf-8-sig")
            for path in [*ROOT.glob("common/**/*.txt"), *ROOT.glob("events/*.txt")]
            if "bechuanaland" in path.name
        )
        self.assertNotIn("every_container", corridor_files)
        self.assertNotIn("sb_bechuanaland_container_canary", corridor_files)

    def test_corridor_shared_state_is_container_owned(self):
        paths = [*ROOT.glob("common/**/*.txt"), *ROOT.glob("events/*.txt")]
        pattern = re.compile(
            r"(?:global_var:|(?:has|set|remove|change)_global_variable\s*=\s*"
            r"(?:\{\s*name\s*=\s*)?)(sb_bechuanaland_[A-Za-z0-9_]+)"
        )
        unexpected = []
        for path in paths:
            source = path.read_text(encoding="utf-8-sig")
            for match in pattern.finditer(source):
                if match.group(1) not in ALLOWED_CORRIDOR_GLOBALS:
                    line = source.count("\n", 0, match.start()) + 1
                    unexpected.append(f"{path.relative_to(ROOT)}:{line}:{match.group(1)}")
        self.assertEqual([], unexpected)

    def test_corridor_uses_container_lists_and_singleton_journal_projection(self):
        effects = text("common/scripted_effects/sb_bechuanaland_corridor_effects.txt")
        journal = text("common/journal_entries/1-11_sb_bechuanaland_corridor.txt")
        for variable in (
            "sb_bechuanaland_boer_network",
            "sb_bechuanaland_british_subject_targets",
        ):
            self.assertIn(f"name = {variable}", effects)
            self.assertIn(f"variable = {variable}", effects)
        self.assertNotIn("com_save_journal_to_variable = {", journal)
        self.assertNotIn("sb_bechuanaland_corridor_journal_handle_var", journal)
        self.assertNotIn("sb_bechuanaland_journal_entries", effects)
        self.assertNotIn("com_set_situation_left_title = {", journal)
        self.assertNotIn("com_set_situation_right_title = {", journal)
        self.assertIn("sb_bechuanaland_project_corridor_journal = yes", journal)
        self.assertIn("je:je_sb_bechuanaland_corridor ?= {", effects)
        self.assertIn("sb_bechuanaland_project_corridor_journal = {", effects)
        self.assertNotIn("com_remove_situation_left_title = yes", effects)
        self.assertNotIn("com_remove_situation_right_title = yes", effects)
        self.assertNotIn("com_situation_left_title_var", effects)
        self.assertNotIn("com_situation_right_title_var", effects)
        self.assertIn(
            "container:sb_bechuanaland_corridor_state.var:sb_bechuanaland_influence_score_var < 0",
            journal,
        )

    def test_corridor_progress_bar_reads_cached_container_sources(self):
        bars = text("common/scripted_progress_bars/sb_progress_bars.txt")
        block = bars.split("sb_bechuanaland_boer_swa_influence_bar = {", 1)[1]
        block = block.split("########################## END ZULU", 1)[0]
        self.assertIn("container:sb_bechuanaland_corridor_state = {", block)
        self.assertEqual(
            14,
            block.count("has_variable = sb_bechuanaland_influence_source_"),
        )
        self.assertNotIn("owner = {", block)
        self.assertNotIn("scope:journal_entry = {", block)
        self.assertNotIn("container_exists = sb_bechuanaland_corridor_state", block)

    def test_startup_relations_do_not_target_dormant_transvaal(self):
        relations = text("common/history/diplomacy/00_relations.txt")
        self.assertNotIn(
            "set_relations = { country = c:TRN value = 50 }",
            relations,
        )
        self.assertIn(
            "TRN forms later, so no valid TRN country exists during startup history",
            relations,
        )

    def test_inboekstelsel_reopens_only_after_prior_invalidation(self):
        journal = text("common/journal_entries/1-10_sb_inboekstelsel.txt")
        effects = text("common/scripted_effects/sb_inboekstelsel_effects.txt")
        cape_events = text("events/sb_cape_events.txt")
        self.assertIn("is_shown_when_inactive = {", journal)
        self.assertIn(
            "NOT = { has_variable = sb_inboekstelsel_reopen_required_var }",
            journal,
        )
        self.assertIn("set_variable = sb_inboekstelsel_reopen_required_var", journal)
        self.assertIn("has_variable = sb_inboekstelsel_reopen_required_var", effects)
        self.assertIn("sb_inboekstelsel_reopen_pending_var", effects)
        self.assertNotIn("sb_inboekstelsel_je_add_pending_var", effects)
        self.assertNotIn(
            "add_journal_entry = { type = je_sb_inboekstelsel_system }",
            cape_events,
        )
        self.assertIn("sb_ensure_inboekstelsel_journal_entry = yes", cape_events)

    def test_corridor_illustration_has_no_actor_title_overlays(self):
        journal = text("common/journal_entries/1-11_sb_bechuanaland_corridor.txt")
        localization = text("localization/english/sb_bechuanaland_corridor_l_english.yml")
        for key in (
            "sb_bechuanaland_situation_left_title",
            "sb_bechuanaland_situation_right_title",
        ):
            self.assertNotIn(key, journal)
            self.assertNotIn(key, localization)

    def test_corridor_ui_uses_journal_projection_not_global_display_scopes(self):
        localization = text("localization/english/sb_bechuanaland_corridor_l_english.yml")
        self.assertNotIn("GetGlobalVariable('sb_bechuanaland", localization)
        self.assertIn("JournalEntry.MakeScope.Var('sb_bechuanaland_boer_actor_scope')", localization)
        self.assertIn("JournalEntry.MakeScope.Var('sb_bechuanaland_swa_overlord_scope')", localization)

    def test_mozambique_company_keeps_player_gate_and_ai_asset_floor(self):
        company = text("common/company_types/zz_sb_mozambique_company_override.txt")
        possible = company.split("\tpossible = {", 1)[1].split("\n\tprosperity_modifier", 1)[0]
        self.assertIn("level >= 5", possible)
        self.assertIn("is_ai = yes", possible)
        self.assertIn("country_definition = cd:POR", possible)
        self.assertIn("country_definition = cd:IBE", possible)
        self.assertIn("level >= 2", possible)

    def test_obsolete_corridor_migration_symbols_are_removed(self):
        source = "\n".join(
            path.read_text(encoding="utf-8-sig")
            for path in [*ROOT.glob("common/**/*.txt"), *ROOT.glob("events/*.txt")]
        )
        for symbol in (
            "sb_bechuanaland_caprivi_escalated_var",
            "sb_bechuanaland_boer_influence_positive_var",
            "sb_bechuanaland_swa_influence_positive_var",
        ):
            self.assertNotIn(symbol, source)


if __name__ == "__main__":
    unittest.main()
