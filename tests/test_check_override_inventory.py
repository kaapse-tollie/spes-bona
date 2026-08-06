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
        (self.game / "map_data").mkdir()
        (self.mod / "descriptor.mod").write_text('supported_version="1.13.9"\n')
        (self.mod / "common/test.txt").write_text("mod copy\n")
        (self.game / "common/test.txt").write_text("upstream copy\n")
        self.mod_object = 'REPLACE:foo = { value = 2 # } ignored\n text = "{quoted}"\n }\n'
        self.up_object = 'foo = { value = 1 }\n'
        (self.mod / "common/laws/mod.txt").write_text(self.mod_object)
        (self.game / "common/laws/base.txt").write_text(self.up_object)
        meta = {
            "scope": "test",
            "intent": "test fixture",
            "load_order": "test",
            "owner": "tests",
            "rebase_date": "2026-08-06",
        }
        self.inventory = {
            "target_game_version": "1.13.9",
            "approved_replace_paths": [],
            "state_region_blocks": [],
            "same_path_files": [{
                "path": "common/test.txt",
                "upstream_version": "1.13.9",
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


if __name__ == "__main__":
    unittest.main()
