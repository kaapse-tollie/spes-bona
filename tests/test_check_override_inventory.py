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


def steam_app_manifest(
    *,
    build="25081502",
    branch="1.14-openbeta",
    core_manifest="3868129321396195520",
):
    return f'''"AppState"
{{
    "appid" "529340"
    "buildid" "{build}"
    "InstalledDepots"
    {{
        "529341"
        {{
            "manifest" "{core_manifest}"
        }}
    }}
    "UserConfig"
    {{
        "BetaKey" "{branch}"
    }}
    "MountedConfig"
    {{
        "BetaKey" "{branch}"
    }}
}}
'''


class OverrideInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        base = Path(self.temp.name)
        self.mod = base / "mod"
        self.game = base / "game"
        self.appmanifest = base / "appmanifest_529340.acf"
        self.appmanifest.write_text(steam_app_manifest())
        (self.mod / "common/laws").mkdir(parents=True)
        (self.game / "common/laws").mkdir(parents=True)
        (self.game / "common/on_actions").mkdir(parents=True)
        (self.game / "map_data").mkdir()
        (self.mod / ".metadata").mkdir()
        (self.mod / "descriptor.mod").write_text('supported_version="1.14.0"\n')
        (self.mod / ".metadata/metadata.json").write_text(json.dumps({
            "supported_game_version": "1.14.0",
            "relationships": [{
                "id": "com.github.Victoria-3-Modding-Co-op.Community-Mod-Framework",
                "version": "1.66.*",
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
            "schema_version": 3,
            "target_game_version": "1.14.0",
            "target_steam_build": "25081502",
            "target_steam_branch": "1.14-openbeta",
            "target_core_depot": "529341",
            "target_core_depot_manifest": "3868129321396195520",
            "generated_for_commit_baseline": "1" * 40,
            "dependencies": [{
                "name": "Community Mod Framework",
                "version": "1.66.0",
                "version_range": "1.66.*",
                "commit": "807c32ff42b75714a3a0e090c0db3357b5e46ed7",
                "release_tag": "1.66.0",
                "asset_name": "release-1.66.0.zip",
                "asset_sha256": "79dd0d434e6ffb617147ad1b91b73e6306139adfffcadf6774eeb32db3a09b8b",
            }],
            "approved_replace_paths": [],
            "state_region_blocks": [],
            "same_path_files": [{
                "path": "common/test.txt",
                "upstream_version": "1.14.0",
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
        return CHECKER.validate(
            self.mod,
            self.game,
            inventory or self.inventory,
            steam_app_manifest=self.appmanifest,
        )

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

    def test_unregistered_additive_zz_file_fails(self):
        (self.mod / "common/history/ai").mkdir(parents=True, exist_ok=True)
        (self.mod / "common/history/ai/zz_sb_new_additive.txt").write_text("AI = { }\n")
        errors = self.validate()
        self.assertTrue(any("unregistered zz_ override-style file" in e for e in errors))

    def test_registered_additive_override_hash_drift_fails(self):
        rel = "common/history/ai/zz_sb_portuguese_kongo_secret_goal.txt"
        (self.mod / "common/history/ai").mkdir(parents=True, exist_ok=True)
        (self.mod / rel).write_text("AI = { }\n")
        inv = dict(self.inventory)
        inv["additive_overrides"] = [{
            "path": rel, "intent": "test", "owner": "tests", "rebase_date": "2026-09-04",
            "mod_sha256": "deadbeef",
        }]
        errors = self.validate(inv)
        self.assertTrue(any("additive override mod hash drift" in e for e in errors))
        inv["additive_overrides"][0]["mod_sha256"] = CHECKER.sha256(self.mod / rel)
        self.assertEqual([], self.validate(inv))
        for field in ("owner", "rebase_date"):
            bad_inventory = copy.deepcopy(inv)
            bad_inventory["additive_overrides"][0].pop(field)
            self.assertTrue(
                any(f"additive override missing {field}" in error for error in self.validate(bad_inventory))
            )

    def test_unregistered_localization_replace_file_fails(self):
        replace = self.mod / "localization/english/replace"
        replace.mkdir(parents=True, exist_ok=True)
        (replace / "sb_new_l_english.yml").write_text("l_english:\n")
        errors = self.validate()
        self.assertTrue(any("unregistered localization replace file" in e for e in errors))

    def test_registered_localization_replace_with_upstream_is_checked(self):
        replace = self.mod / "localization/english/replace"
        replace.mkdir(parents=True, exist_ok=True)
        (replace / "sb_new_l_english.yml").write_text("l_english:\n")
        inv = dict(self.inventory)
        inv["localization_replace_files"] = [{
            "path": "localization/english/replace/sb_new_l_english.yml",
            "upstream_file": None, "intent": "test", "owner": "tests",
            "rebase_date": "2026-09-04",
            "mod_sha256": CHECKER.sha256(replace / "sb_new_l_english.yml"),
        }]
        self.assertEqual([], self.validate(inv))
        for field in ("owner", "rebase_date"):
            bad_inventory = copy.deepcopy(inv)
            bad_inventory["localization_replace_files"][0].pop(field)
            self.assertTrue(
                any(
                    f"localization replace entry missing {field}" in error
                    for error in self.validate(bad_inventory)
                )
            )
        inv["localization_replace_files"][0]["mod_sha256"] = "deadbeef"
        errors = self.validate(inv)
        self.assertTrue(any("localization replace mod hash drift" in e for e in errors))

    def test_localization_key_parser_accepts_column_zero_without_crossing_lines(self):
        path = Path(self.temp.name) / "fixture_l_english.yml"
        path.write_text(
            "l_english:\n"
            "column_zero_one:0 \"One\"\n"
            "column_zero_two: \"Two\"\n"
            " indented_key:0 \"Three\"\n"
            "# commented_key:0 \"No\"\n"
        )
        self.assertEqual(
            {"column_zero_one", "column_zero_two", "indented_key"},
            CHECKER.localization_keys(path),
        )

    def test_null_primary_localization_collisions_require_exact_key_source_pins(self):
        replace = self.mod / "localization/english/replace"
        vanilla = self.game / "localization/english"
        replace.mkdir(parents=True, exist_ok=True)
        vanilla.mkdir(parents=True, exist_ok=True)
        mod_file = replace / "sb_names_l_english.yml"
        source = vanilla / "hub_names_l_english.yml"
        mod_file.write_text('l_english:\n key_test:0 "Mod"\n')
        source.write_text('l_english:\n key_test:0 "Vanilla"\n')
        inventory = copy.deepcopy(self.inventory)
        inventory["localization_replace_files"] = [{
            "path": "localization/english/replace/sb_names_l_english.yml",
            "upstream_file": None,
            "intent": "test",
            "owner": "tests",
            "rebase_date": "2026-09-04",
            "mod_sha256": digest(mod_file),
        }]
        errors = self.validate(inventory)
        self.assertTrue(any("unmanifested localization key collision" in error for error in errors))

        inventory["localization_key_collisions"] = [{
            "mod_file": "localization/english/replace/sb_names_l_english.yml",
            "key": "key_test",
            "upstream_version": "1.14.0",
            "upstream_file": "hub_names_l_english.yml",
            "upstream_sha256": digest(source),
            "scope": "exact test key",
            "intent": "test",
            "load_order": "localization replace precedence",
            "owner": "tests",
            "rebase_date": "2026-09-04",
        }]
        self.assertEqual([], self.validate(inventory))
        for version in (None, "0.0.0"):
            with self.subTest(version=version):
                bad_inventory = copy.deepcopy(inventory)
                if version is None:
                    bad_inventory["localization_key_collisions"][0].pop("upstream_version")
                else:
                    bad_inventory["localization_key_collisions"][0]["upstream_version"] = version
                self.assertTrue(
                    any(
                        "localization collision version does not match target" in error
                        for error in self.validate(bad_inventory)
                    )
                )
        source.write_text('l_english:\n key_test:0 "Changed"\n')
        self.assertTrue(
            any("upstream localization source hash drift" in error for error in self.validate(inventory))
        )

    def test_secondary_localization_source_is_pinned_separately(self):
        replace = self.mod / "localization/english/replace"
        vanilla = self.game / "localization/english"
        replace.mkdir(parents=True, exist_ok=True)
        vanilla.mkdir(parents=True, exist_ok=True)
        mod_file = replace / "dynamic_l_english.yml"
        primary = vanilla / "dynamic_l_english.yml"
        secondary = vanilla / "hub_names_l_english.yml"
        for path, value in (
            (mod_file, "Mod"),
            (primary, "Primary"),
            (secondary, "Secondary"),
        ):
            path.write_text(f'l_english:\n key_test:0 "{value}"\n')
        inventory = copy.deepcopy(self.inventory)
        inventory["localization_replace_files"] = [{
            "path": "localization/english/replace/dynamic_l_english.yml",
            "upstream_file": "dynamic_l_english.yml",
            "upstream_sha256": digest(primary),
            "intent": "test",
            "owner": "tests",
            "rebase_date": "2026-09-04",
            "mod_sha256": digest(mod_file),
        }]
        errors = self.validate(inventory)
        self.assertEqual(1, sum("unmanifested localization key collision" in error for error in errors))
        inventory["localization_key_collisions"] = [{
            "mod_file": "localization/english/replace/dynamic_l_english.yml",
            "key": "key_test",
            "upstream_version": "1.14.0",
            "upstream_file": "hub_names_l_english.yml",
            "upstream_sha256": digest(secondary),
            "scope": "exact secondary test key",
            "intent": "test",
            "load_order": "localization replace precedence",
            "owner": "tests",
            "rebase_date": "2026-09-04",
        }]
        self.assertEqual([], self.validate(inventory))

    def test_stale_localization_key_collision_entry_fails(self):
        inventory = copy.deepcopy(self.inventory)
        inventory["localization_key_collisions"] = [{
            "mod_file": "localization/english/replace/missing_l_english.yml",
            "key": "missing_key",
            "upstream_file": "missing_l_english.yml",
            "upstream_sha256": "0" * 64,
            "scope": "exact missing key",
            "intent": "test",
            "load_order": "localization replace precedence",
            "owner": "tests",
            "rebase_date": "2026-09-04",
        }]
        errors = self.validate(inventory)
        self.assertTrue(any("stale localization key collision entry" in error for error in errors))
        self.assertTrue(any("mod_file is not a registered" in error for error in errors))

    def test_descriptor_replace_path_and_version_are_locked(self):
        (self.mod / "descriptor.mod").write_text('supported_version="1.14.8"\n  replace_path = "common/history"\n')
        errors = self.validate()
        self.assertTrue(any("supported_version" in error for error in errors))
        self.assertTrue(any("replace_path drift" in error for error in errors))

    def test_steam_app_manifest_is_inferred_from_game_root_ancestors(self):
        steamapps = Path(self.temp.name) / "steamapps"
        nested_game = steamapps / "common/Victoria 3/game"
        nested_game.mkdir(parents=True)
        manifest = steamapps / "appmanifest_529340.acf"
        manifest.write_text(steam_app_manifest())
        self.assertEqual(manifest, CHECKER.find_steam_app_manifest(nested_game))

    def test_steam_app_manifest_locks_build_branch_and_core_depot_manifest(self):
        cases = (
            ({"build": "25099999"}, "installed Steam build"),
            ({"branch": "1.14-openbeta-next"}, "installed Steam branch"),
            ({"core_manifest": "999"}, "installed core depot 529341 manifest"),
        )
        for values, expected in cases:
            with self.subTest(values=values):
                self.appmanifest.write_text(steam_app_manifest(**values))
                self.assertTrue(any(expected in error for error in self.validate()))
        self.appmanifest.write_text(steam_app_manifest())
        self.assertEqual([], self.validate())

    def test_target_schema_requires_complete_ob1_identity(self):
        for field in (
            "target_steam_build",
            "target_steam_branch",
            "target_core_depot",
            "target_core_depot_manifest",
        ):
            with self.subTest(field=field):
                inventory = copy.deepcopy(self.inventory)
                inventory.pop(field)
                self.assertTrue(any(field in error for error in self.validate(inventory)))
        inventory = copy.deepcopy(self.inventory)
        inventory["schema_version"] = 1
        self.assertTrue(any("schema_version" in error for error in self.validate(inventory)))
        inventory = copy.deepcopy(self.inventory)
        inventory["target_steam_build"] = 25081502
        self.assertTrue(any("target_steam_build" in error for error in self.validate(inventory)))

    def test_release_metadata_and_dependency_are_locked(self):
        inventory = copy.deepcopy(self.inventory)
        inventory["target_steam_build"] = "old"
        inventory["generated_for_commit_baseline"] = "short"
        inventory["dependencies"][0]["version"] = "1.60.3"
        inventory["dependencies"][0]["version_range"] = "1.65.*"
        inventory["dependencies"][0]["commit"] = "807c32f"
        inventory["dependencies"][0]["release_tag"] = "1.67.0"
        inventory["dependencies"][0]["asset_name"] = "release-1.67.0.zip"
        inventory["dependencies"][0]["asset_sha256"] = "0" * 64
        errors = self.validate(inventory)
        self.assertTrue(any("target_steam_build" in error for error in errors))
        self.assertTrue(any("generated_for_commit_baseline" in error for error in errors))
        self.assertTrue(any("CMF version" in error for error in errors))
        self.assertTrue(any("CMF version_range" in error for error in errors))
        self.assertTrue(any("CMF commit" in error for error in errors))
        self.assertTrue(any("CMF release_tag" in error for error in errors))
        self.assertTrue(any("CMF asset_name" in error for error in errors))
        self.assertTrue(any("CMF asset_sha256" in error for error in errors))

        metadata = json.loads((self.mod / ".metadata/metadata.json").read_text())
        metadata["supported_game_version"] = "1.14.9"
        metadata["relationships"][0]["version"] = "1.62.0"
        (self.mod / ".metadata/metadata.json").write_text(json.dumps(metadata))
        errors = self.validate()
        self.assertTrue(any("supported_game_version" in error for error in errors))
        self.assertTrue(any("version 1.66.*" in error for error in errors))

    def test_non_shadowed_upstream_contract_is_hash_and_object_pinned(self):
        inventory = copy.deepcopy(self.inventory)
        inventory["upstream_contracts"] = [{
            "path": "common/laws/base.txt",
            "key": "foo",
            "upstream_version": "1.14.0",
            "file_sha256": digest(self.game / "common/laws/base.txt"),
            "object_sha256": object_digest(self.up_object, "foo"),
            "scope": "test caller",
            "intent": "test",
            "load_order": "Vanilla-owned",
            "owner": "tests",
            "rebase_date": "2026-09-04",
        }]
        self.assertEqual([], self.validate(inventory))
        inventory["upstream_contracts"][0]["object_sha256"] = "0" * 64
        self.assertTrue(
            any("upstream contract object hash drift" in error for error in self.validate(inventory))
        )

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
            "upstream_version": "1.14.0",
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

    def test_vanilla_1_14_api_surface_is_locked(self):
        on_actions = self.game / "common/on_actions/00_code_on_actions.txt"
        on_actions.write_text(
            "on_treaty_ports_inherited = { effect = { } }\n"
            "on_company_disbanded = { effect = { } }\n"
        )
        errors = self.validate()
        self.assertTrue(any("treaty_port_inheritance_events.1" in error for error in errors))
        self.assertTrue(any("re_add_disbanded_company" in error for error in errors))

    def test_cmf_1_66_api_surface_is_locked(self):
        cmf = Path(self.temp.name) / "cmf"
        (cmf / ".metadata").mkdir(parents=True)
        (cmf / "common/scripted_effects").mkdir(parents=True)
        (cmf / "common/console_command_macros").mkdir(parents=True)
        (cmf / "gui/com_journal_injects").mkdir(parents=True)
        (cmf / ".metadata/metadata.json").write_text(json.dumps({"version": "1.66.0"}))
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
        self.assertTrue(any("CMF 1.66.0 API com_container" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
