import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from tools import cmf_patch, sync_cmf, validate, check_override_inventory as inventory
from tools import build_1_14_2_depot_delta as delta
from test_sync_cmf import VERSION, release_archive, fake_opener


ROOT = Path(__file__).resolve().parents[1]
GAME = validate.find_game_root(None)


class PatchedCmfTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.archive = release_archive()
        pristine = self.base / "pristine"
        pristine.mkdir()
        sync_cmf.extract_release(self.archive, pristine, VERSION)
        tree = pristine / "payload"
        payload = self.base / "files/common/example.txt"
        payload.parent.mkdir(parents=True)
        payload.write_bytes(b"patched")
        self.manifest = self.base / "manifest.json"
        self.patch = {
            "schema_version": 1, "revision": cmf_patch.REVISION, "base_tag": VERSION,
            "base_asset_sha256": cmf_patch.digest(self.archive),
            "base_tree_sha256": cmf_patch.tree_digest(tree),
            "files": [{"path": "common/example.txt", "payload": "files/common/example.txt",
                       "original_sha256": cmf_patch.digest(b"example"), "sha256": cmf_patch.digest(b"patched")}],
        }
        (tree / "common/example.txt").write_bytes(b"patched")
        self.patch["tree_sha256"] = cmf_patch.tree_digest(tree)
        self.manifest.write_text(json.dumps(self.patch))
        self.target = self.base / "installed"
        self.opener, self.calls = fake_opener(archive=self.archive)

    def sync(self, **kwargs):
        return sync_cmf.synchronize(self.target, tag=VERSION,
            expected_sha256=self.patch["base_asset_sha256"], opener=self.opener,
            patch_manifest=self.manifest, **kwargs)

    def test_install_is_patched_repeatable_and_preserves_other_files(self):
        self.assertEqual(("updated", VERSION), self.sync())
        self.assertEqual(b"patched", (self.target / "common/example.txt").read_bytes())
        self.assertEqual(b"example", (self.target / "gui/example.gui").read_bytes())
        self.assertEqual(("current", VERSION), self.sync(check_only=True))
        self.assertEqual(("updated", VERSION), self.sync(force=True))
        cmf_patch.verify_install(self.target, self.manifest)

    def test_check_rejects_unpatched_partial_and_extra_files_without_writing(self):
        self.sync()
        for relative, data in (("common/example.txt", b"example"), ("gui/example.gui", b"altered"), ("common/extra.txt", b"extra")):
            with self.subTest(relative=relative):
                self.sync(force=True)
                path = self.target / relative
                path.write_bytes(data)
                before = cmf_patch.tree_digest(self.target)
                with self.assertRaises(sync_cmf.SyncError):
                    self.sync(check_only=True)
                self.assertEqual(before, cmf_patch.tree_digest(self.target))

    def test_bad_payload_or_original_hash_preserves_install(self):
        self.sync()
        before = cmf_patch.tree_digest(self.target)
        for key in ("sha256", "original_sha256"):
            with self.subTest(key=key):
                patch = json.loads(json.dumps(self.patch))
                patch["files"][0][key] = "0" * 64
                self.manifest.write_text(json.dumps(patch))
                with self.assertRaises(sync_cmf.SyncError):
                    self.sync(force=True)
                self.assertEqual(before, cmf_patch.tree_digest(self.target))

    def test_failed_rename_restores_previous_install(self):
        self.sync()
        before = cmf_patch.tree_digest(self.target)
        original = Path.rename
        def rename(path, target):
            if path.name == "payload":
                raise OSError("test install failure")
            return original(path, target)
        with mock.patch.object(Path, "rename", rename):
            with self.assertRaisesRegex(sync_cmf.SyncError, "restored"):
                self.sync(force=True)
        self.assertEqual(before, cmf_patch.tree_digest(self.target))

    def test_latest_and_unsafe_patch_paths_rejected(self):
        with self.assertRaisesRegex(sync_cmf.SyncError, "--latest"):
            sync_cmf.synchronize(self.target, latest=True, patch_manifest=self.manifest)
        self.patch["files"][0]["payload"] = "../outside"
        self.manifest.write_text(json.dumps(self.patch))
        with self.assertRaisesRegex(ValueError, "unsafe"):
            cmf_patch.load_patch(self.manifest)

    def test_gui_patch_exception_is_exact_and_payload_checked(self):
        entry = self.patch["files"][0]
        entry["path"] = "gui/com_gui_progressbars.gui"
        entry["payload"] = "files/" + entry["path"]
        payload = self.base / entry["payload"]
        payload.parent.mkdir(parents=True)
        payload.write_bytes(b"patched")
        self.manifest.write_text(json.dumps(self.patch))
        cmf_patch.load_patch(self.manifest)
        payload.write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError, "payload hash mismatch"):
            cmf_patch.load_patch(self.manifest)
        entry["path"] = "gui/unrelated.gui"
        entry["payload"] = "files/" + entry["path"]
        self.manifest.write_text(json.dumps(self.patch))
        with self.assertRaisesRegex(ValueError, "unexpected CMF patch target"):
            cmf_patch.load_patch(self.manifest)


class BetaRebaseTests(unittest.TestCase):
    def test_historical_depot_evidence_schema(self):
        data = json.loads(delta.OUTPUT.read_text())
        self.assertEqual({"added": 1, "changed": 69, "removed": 0, "total": 70}, data["counts"])
        paths = {e["path"] for e in data["entries"]}
        self.assertIn("game/common/scripted_guis/diplomacy_sguis.txt", paths)
        for filename in ("00_annex_country.txt", "03_conquer_state.txt", "21_return_state.txt"):
            self.assertNotIn("game/common/war_goal_types/" + filename, paths)
        self.assertFalse(any("spline_network" in p or p.startswith("game/map_data/") for p in paths))

    def test_historical_depot_evidence_rebuilds_when_manifests_retained(self):
        if not all(delta.depot.default_manifest_path(identity).is_file()
                   for identity in (delta.OLD, delta.NEW)):
            self.skipTest("exact historical 1.14.0/1.14.2 manifests are not retained")
        self.assertEqual(json.loads(delta.OUTPUT.read_text()), delta.build_delta())

    def test_historical_installed_payload_only_on_exact_1_14_2_build(self):
        if GAME is None:
            self.skipTest("historical 1.14.2 game root unavailable")
        settings = json.loads((GAME.parent / "launcher/launcher-settings.json").read_text())
        app_path = inventory.find_steam_app_manifest(GAME)
        if settings["rawVersion"] != "1.14.2" or app_path is None:
            self.skipTest("historical 1.14.2 payload is not installed")
        app = inventory.parse_vdf(app_path.read_text())["AppState"]
        if (app.get("buildid") != delta.NEW.steam_build
                or app.get("InstalledDepots", {}).get("529341", {}).get("manifest") != str(delta.NEW.manifest_id)):
            self.skipTest("exact historical 1.14.2 Steam build is not installed")
        delta.depot.verify_current_payload(json.loads(delta.OUTPUT.read_text()), GAME)

    def test_exact_dp_marker_preserves_namespace_boundaries(self):
        source = '# ### (DP) REVIEWED ###\nsb_test.001.t:0 "Title"\nsb_test.002.t:0 "Other"\n'
        self.assertEqual([("event", "sb_test.001", "REVIEWED", 1)], validate.localization_review_classifications(source, []))
        self.assertEqual([], validate.localization_review_classifications(source.replace("sb_test.001.t", "unrelated_key"), []))

    @unittest.skipIf(GAME is None, "Vanilla game root unavailable")
    def test_cmf_categories_equal_current_vanilla_plus_only_cmf_extensions(self):
        patch = cmf_patch.load_patch()
        entry = next(e for e in patch["files"]
                     if e["path"] == "common/scripted_triggers/ycom_ideology_trigger_overrides.txt")
        payload = cmf_patch.DEFAULT_MANIFEST.parent / entry["payload"]
        patched = payload.read_text(encoding="utf-8-sig")
        vanilla = (GAME / "common/scripted_triggers/00_scripted_triggers.txt").read_text(encoding="utf-8-sig")
        matches = inventory.top_level_matches(inventory.HARD_REPLACE_RE, patched)
        self.assertEqual(7, len(matches))
        for match in matches:
            key = match.group(2)
            body = inventory.find_object(patched, key, directive="REPLACE")
            without_extensions = "\n".join(line for line in body.splitlines() if "#usfp" not in line and "#anzfp" not in line)
            self.assertEqual(inventory.find_object(vanilla, key), without_extensions.removeprefix("REPLACE:"))
        self.assertNotIn("ideology_nihilist", inventory.find_object(patched, "has_progressive_ideology", directive="REPLACE"))
        self.assertIn("ideology_nihilist", inventory.find_object(patched, "has_socialist_ideology", directive="REPLACE"))

    @unittest.skipIf(GAME is None, "Vanilla game root unavailable")
    def test_revoke_claim_inherits_assent_only_vanilla(self):
        relative = "common/war_goal_types/23_revoke_claim.txt"
        self.assertFalse((ROOT / relative).exists())
        self.assertFalse((ROOT.parent / "Community Mod Framework" / relative).exists())
        self.assertIn("assent_required", (GAME / relative).read_text())


if __name__ == "__main__":
    unittest.main()
