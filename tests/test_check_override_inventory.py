import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools/check_override_inventory.py"
SPEC = importlib.util.spec_from_file_location("check_override_inventory", MODULE_PATH)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def object_digest(text, key, directive=None):
    return hashlib.sha256(CHECKER.find_object(text, key, directive=directive).encode()).hexdigest()


class OverrideInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        base = Path(self.temp.name)
        self.mod = base / "mod"
        self.game = base / "game"
        (self.mod / "common/laws").mkdir(parents=True)
        (self.game / "common/laws").mkdir(parents=True)
        (self.game / "common/on_actions").mkdir(parents=True)
        (self.game / "map_data").mkdir()
        (self.mod / ".metadata").mkdir()
        (self.mod / "descriptor.mod").write_text('supported_version="1.13.11"\n')
        (self.mod / ".metadata/metadata.json").write_text(json.dumps({
            "supported_game_version": "1.13.11",
            "relationships": [{
                "id": "com.github.Victoria-3-Modding-Co-op.Community-Mod-Framework",
                "version": "1.63.*",
            }],
        }))
        (self.mod / "common/test.txt").write_text("mod copy\n")
        (self.game / "common/test.txt").write_text("upstream copy\n")
        self.mod_object = 'REPLACE:foo = { value = 2 # } ignored\n text = "{quoted}"\n }\n'
        self.up_object = 'foo = { value = 1 }\n'
        (self.mod / "common/laws/mod.txt").write_text(self.mod_object)
        (self.game / "common/laws/base.txt").write_text(self.up_object)
        (self.game / "common/on_actions/00_code_on_actions.txt").write_text(
            "on_treaty_ports_inherited = { effect = { trigger_event = { "
            "id = treaty_port_inheritance_events.1 popup = yes } } }\n"
            "on_company_disbanded = { effect = { "
            "re_add_disbanded_company_prestige_good_jes = yes } }\n"
        )
        meta = {
            "scope": "test",
            "intent": "test fixture",
            "load_order": "test",
            "owner": "tests",
            "rebase_date": "2026-08-06",
        }
        self.inventory = {
            "target_game_version": "1.13.11",
            "target_steam_build": "24799966",
            "generated_for_commit_baseline": "1" * 40,
            "dependencies": [{
                "name": "Community Mod Framework",
                "version": "1.63.0",
                "commit": "bd92022",
            }],
            "approved_replace_paths": [],
            "state_region_blocks": [],
            "same_path_files": [{
                "path": "common/test.txt",
                "upstream_version": "1.13.11",
                "upstream_sha256": digest(self.game / "common/test.txt"),
                "mod_sha256": digest(self.mod / "common/test.txt"),
                "comparison": "text-hash-pair",
                **meta,
            }],
            "keyed_overrides": [{
                "mod_path": "common/laws/mod.txt",
                "directive": "REPLACE",
                "key": "foo",
                "mod_object_sha256": object_digest(self.mod_object, "foo", "REPLACE"),
                "upstream": {
                    "path": "common/laws/base.txt",
                    "key": "foo",
                    "file_sha256": digest(self.game / "common/laws/base.txt"),
                    "object_sha256": object_digest(self.up_object, "foo"),
                },
                **meta,
            }],
        }

    def tearDown(self):
        self.temp.cleanup()

    def validate(self, inventory=None):
        return CHECKER.validate(self.mod, self.game, inventory or self.inventory)

    def test_clean_fixture_passes_and_parser_ignores_comment_and_quote_braces(self):
        self.assertEqual([], self.validate())
        block = CHECKER.find_object(self.mod_object, "foo", directive="REPLACE")
        self.assertIn('"{quoted}"', block)
        self.assertIn("# } ignored", block)

    def test_unmanifested_and_stale_same_path_files_fail(self):
        (self.mod / "common/extra.txt").write_text("mod")
        (self.game / "common/extra.txt").write_text("game")
        self.assertTrue(any("unmanifested same-path" in error for error in self.validate()))
        inventory = copy.deepcopy(self.inventory)
        inventory["same_path_files"].append({"path": "common/missing.txt"})
        self.assertTrue(any("stale same-path" in error for error in self.validate(inventory)))

    def test_upstream_and_mod_hash_drift_fail(self):
        (self.mod / "common/test.txt").write_text("changed")
        self.assertTrue(any("mod hash drift" in error for error in self.validate()))
        (self.mod / "common/test.txt").write_text("mod copy\n")
        (self.game / "common/test.txt").write_text("changed upstream")
        self.assertTrue(any("upstream hash drift" in error for error in self.validate()))

    def test_keyed_override_set_and_object_hash_are_locked(self):
        with (self.mod / "common/laws/mod.txt").open("a") as handle:
            handle.write("REPLACE:bar = { value = 1 }\n")
        errors = self.validate()
        self.assertTrue(any("unmanifested keyed override" in error for error in errors))
        (self.mod / "common/laws/mod.txt").write_text('REPLACE:foo = { value = 3 }\n')
        self.assertTrue(any("mod object hash drift" in error for error in self.validate()))

    def test_descriptor_replace_path_and_version_are_locked(self):
        (self.mod / "descriptor.mod").write_text('supported_version="1.13.8"\n  replace_path = "common/history"\n')
        errors = self.validate()
        self.assertTrue(any("supported_version" in error for error in errors))
        self.assertTrue(any("replace_path drift" in error for error in errors))

    def test_release_metadata_and_dependency_are_locked(self):
        inventory = copy.deepcopy(self.inventory)
        inventory["target_steam_build"] = "old"
        inventory["generated_for_commit_baseline"] = "short"
        inventory["dependencies"][0]["version"] = "1.60.3"
        errors = self.validate(inventory)
        self.assertTrue(any("target_steam_build" in error for error in errors))
        self.assertTrue(any("generated_for_commit_baseline" in error for error in errors))
        self.assertTrue(any("CMF version" in error for error in errors))

        metadata = json.loads((self.mod / ".metadata/metadata.json").read_text())
        metadata["supported_game_version"] = "1.13.9"
        metadata["relationships"][0]["version"] = "1.62.0"
        (self.mod / ".metadata/metadata.json").write_text(json.dumps(metadata))
        errors = self.validate()
        self.assertTrue(any("supported_game_version" in error for error in errors))
        self.assertTrue(any("version 1.63.*" in error for error in errors))

    def test_missing_upstream_state_region_block_fails(self):
        (self.mod / "map_data/state_regions").mkdir(parents=True)
        (self.game / "map_data/state_regions").mkdir(parents=True)
        (self.mod / "map_data/state_regions/04_subsaharan_africa.txt").write_text(
            "STATE_PRESENT = { id = 1 }\n"
        )
        (self.game / "map_data/state_regions/04_subsaharan_africa.txt").write_text(
            "STATE_PRESENT = { id = 1 }\nSTATE_NEW = { id = 2 }\n"
        )
        self.inventory["same_path_files"].append({
            "path": "map_data/state_regions/04_subsaharan_africa.txt",
            "upstream_version": "1.13.11",
            "upstream_sha256": digest(self.game / "map_data/state_regions/04_subsaharan_africa.txt"),
            "mod_sha256": digest(self.mod / "map_data/state_regions/04_subsaharan_africa.txt"),
            "comparison": "text-hash-pair",
            "scope": "test",
            "intent": "test fixture",
            "load_order": "test",
            "owner": "tests",
            "rebase_date": "2026-08-12",
        })
        self.inventory["state_region_blocks"] = ["STATE_PRESENT"]
        self.assertTrue(
            any("omits upstream block: STATE_NEW" in error for error in self.validate())
        )

    def test_vanilla_hotfix_api_surface_is_locked(self):
        on_actions = self.game / "common/on_actions/00_code_on_actions.txt"
        on_actions.write_text(
            "on_treaty_ports_inherited = { effect = { } }\n"
            "on_company_disbanded = { effect = { } }\n"
        )
        errors = self.validate()
        self.assertTrue(any("treaty_port_inheritance_events.1" in error for error in errors))
        self.assertTrue(any("re_add_disbanded_company" in error for error in errors))

    def test_cmf_1_63_api_surface_is_locked(self):
        cmf = Path(self.temp.name) / "cmf"
        (cmf / ".metadata").mkdir(parents=True)
        (cmf / "common/scripted_effects").mkdir(parents=True)
        (cmf / "common/console_command_macros").mkdir(parents=True)
        (cmf / "gui/com_journal_injects").mkdir(parents=True)
        (cmf / ".metadata/metadata.json").write_text(json.dumps({"version": "1.63.0"}))
        (cmf / "common/scripted_effects/com_international_situation_effects.txt").write_text(
            "com_set_situation_left_title = { set_variable = { } }\n"
            "com_set_situation_right_title = { set_variable = { } }\n"
        )
        (cmf / "common/console_command_macros/com_macros.txt").write_text(
            "com_container = { args = 0 }\n"
        )
        (cmf / "gui/com_journal_injects/situation_widgets.gui").write_text(
            "com_situation_left_title_var com_situation_right_title_var\n"
        )
        self.assertEqual([], CHECKER.validate(self.mod, self.game, self.inventory, cmf))

        (cmf / "common/console_command_macros/com_macros.txt").write_text("")
        errors = CHECKER.validate(self.mod, self.game, self.inventory, cmf)
        self.assertTrue(any("CMF 1.63.0 API com_container" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
