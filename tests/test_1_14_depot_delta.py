import collections
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/build_steam_depot_delta.py"
ARTIFACT_PATH = ROOT / "Docs/compatibility/1_13_11_to_1_14_0_ob1_depot_delta.json"
GAME_ROOT = (
    Path.home()
    / "Library/Application Support/Steam/steamapps/common/Victoria 3/game"
)

SPEC = importlib.util.spec_from_file_location("build_steam_depot_delta", MODULE_PATH)
DEPOT_DELTA = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = DEPOT_DELTA
SPEC.loader.exec_module(DEPOT_DELTA)

SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class DepotDeltaEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = ARTIFACT_PATH.read_bytes()
        cls.delta = json.loads(cls.raw.decode("utf-8"))
        cls.entries = cls.delta["entries"]

    def test_artifact_is_normalized_utf8_without_bom(self):
        self.assertTrue(self.raw.startswith(b"{\n"))
        self.assertFalse(self.raw.startswith(bytes((0xEF, 0xBB, 0xBF))))
        self.assertTrue(self.raw.endswith(b"\n"))
        self.assertEqual(
            self.raw.decode("utf-8"),
            DEPOT_DELTA.normalized_json(self.delta),
        )

    def test_schema_and_exact_manifest_identities(self):
        self.assertEqual(1, self.delta["schema_version"])
        self.assertEqual("529341", self.delta["depot_id"])
        self.assertEqual("1.14-openbeta", self.delta["target_branch"])
        self.assertEqual("tools/build_steam_depot_delta.py", self.delta["generated_by"])

        old = self.delta["old_manifest"]
        self.assertEqual("1.13.11", old["game_version"])
        self.assertEqual("24799966", old["steam_build"])
        self.assertEqual("4498977168532327663", old["manifest_id"])
        self.assertEqual("2026-08-18T13:02:33Z", old["created_utc"])
        self.assertEqual("529341_4498977168532327663.manifest", old["source_file"])
        self.assertEqual(4_732_224, old["source_size"])
        self.assertEqual(26_642, old["depot_entry_count"])
        self.assertEqual(
            "5ffcff6dab4ad7d8008618c50413bb3dcaeb12608cbe9d3e93872fa287fc4ddc",
            old["source_sha256"],
        )

        new = self.delta["new_manifest"]
        self.assertEqual("1.14.0", new["game_version"])
        self.assertEqual("25081502", new["steam_build"])
        self.assertEqual("3868129321396195520", new["manifest_id"])
        self.assertEqual("2026-09-01T09:43:27Z", new["created_utc"])
        self.assertEqual("529341_3868129321396195520.manifest", new["source_file"])
        self.assertEqual(4_733_748, new["source_size"])
        self.assertEqual(26_653, new["depot_entry_count"])
        self.assertEqual(
            "1c76bc89eebffc465999a90cfc8ded5c1e771c089bbecb05c86b0d4f6bde4977",
            new["source_sha256"],
        )
        self.assertRegex(old["source_sha256"], SHA256_RE)
        self.assertRegex(new["source_sha256"], SHA256_RE)

    def test_counts_paths_and_change_kinds_are_exact(self):
        self.assertEqual(
            {"added": 13, "changed": 182, "removed": 2, "total": 197},
            self.delta["counts"],
        )
        self.assertEqual(197, len(self.entries))
        self.assertEqual(
            {"added": 13, "changed": 182, "removed": 2},
            dict(collections.Counter(entry["change"] for entry in self.entries)),
        )
        paths = [entry["path"] for entry in self.entries]
        self.assertEqual(sorted(paths), paths)
        self.assertEqual(len(paths), len(set(paths)))
        for path in paths:
            self.assertTrue(path.startswith("game/"), path)
            self.assertNotIn("\\", path)
            self.assertNotIn("..", PurePosixPath(path).parts)
            self.assertEqual(PurePosixPath(path).as_posix(), path)

    def test_every_entry_has_complete_evidence_and_review_classification(self):
        classification = self.delta["classification"]
        subsystems = set(classification["subsystems"])
        dispositions = set(classification["dispositions"])
        self.assertTrue(classification["collision_basis"])
        self.assertNotIn("unclassified", subsystems)
        self.assertNotIn("unreviewed", dispositions)

        for entry in self.entries:
            with self.subTest(path=entry["path"]):
                self.assertEqual(
                    {
                        "change",
                        "disposition",
                        "new",
                        "old",
                        "path",
                        "sb_collision",
                        "subsystem",
                    },
                    set(entry),
                )
                self.assertIn(entry["subsystem"], subsystems)
                self.assertIn(entry["disposition"], dispositions)
                self.assertIs(type(entry["sb_collision"]), bool)
                self.assertEqual({"kind", "sha1", "size"}, set(entry["old"]))
                self.assertEqual({"kind", "sha1", "size"}, set(entry["new"]))

                for side in (entry["old"], entry["new"]):
                    if side["size"] is None:
                        self.assertIsNone(side["sha1"])
                        self.assertIsNone(side["kind"])
                    else:
                        self.assertIs(type(side["size"]), int)
                        self.assertGreaterEqual(side["size"], 0)
                        self.assertRegex(side["sha1"], SHA1_RE)
                        self.assertIn(side["kind"], {"directory", "file", "symlink"})

                if entry["change"] == "changed":
                    self.assertIsNotNone(entry["old"]["size"])
                    self.assertIsNotNone(entry["new"]["size"])
                    self.assertNotEqual(entry["old"]["sha1"], entry["new"]["sha1"])
                elif entry["change"] == "added":
                    self.assertEqual(
                        {"kind": None, "sha1": None, "size": None}, entry["old"]
                    )
                    self.assertIsNotNone(entry["new"]["size"])
                elif entry["change"] == "removed":
                    self.assertIsNotNone(entry["old"]["size"])
                    self.assertEqual(
                        {"kind": None, "sha1": None, "size": None}, entry["new"]
                    )
                else:
                    self.fail("unsupported change kind: {}".format(entry["change"]))

    def test_collision_set_and_key_dispositions_match_review(self):
        collision_paths = {
            entry["path"] for entry in self.entries if entry["sb_collision"]
        }
        self.assertEqual(set(DEPOT_DELTA.SB_COLLISION_PATHS), collision_paths)
        by_path = {entry["path"]: entry for entry in self.entries}
        self.assertEqual(
            "removed-unused-by-sb",
            by_path["game/common/script_values/war_exhaustion_values.txt"][
                "disposition"
            ],
        )
        self.assertEqual(
            "adapt-sb-contract-runtime-pending",
            by_path["game/common/script_values/war_support_values.txt"]["disposition"],
        )
        self.assertEqual(
            "merge-required",
            by_path["game/common/dynamic_country_names/00_dynamic_country_names.txt"][
                "disposition"
            ],
        )
        self.assertEqual(
            "merge-required-runtime-pending",
            by_path["game/gfx/map/spline_network/spline_network.splnet"][
                "disposition"
            ],
        )
        self.assertEqual(
            "repin-reviewed-sb-surface",
            by_path["game/common/interest_groups/00_armed_forces.txt"]["disposition"],
        )

    def test_committed_artifact_rebuilds_from_exact_manifests_when_retained(self):
        old_path = DEPOT_DELTA.default_manifest_path(DEPOT_DELTA.OLD_IDENTITY)
        new_path = DEPOT_DELTA.default_manifest_path(DEPOT_DELTA.NEW_IDENTITY)
        if not old_path.is_file() or not new_path.is_file():
            self.skipTest("exact retained Steam manifests are not installed")
        rebuilt = DEPOT_DELTA.build_delta(old_path, new_path)
        self.assertEqual(self.raw.decode("utf-8"), DEPOT_DELTA.normalized_json(rebuilt))

    def test_decoder_rejects_a_same_size_manifest_with_different_hash(self):
        old_path = DEPOT_DELTA.default_manifest_path(DEPOT_DELTA.OLD_IDENTITY)
        if not old_path.is_file():
            self.skipTest("exact retained old Steam manifest is not installed")
        mutated = bytearray(old_path.read_bytes())
        mutated[-1] ^= 0x01
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / old_path.name
            path.write_bytes(mutated)
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                DEPOT_DELTA.decode_manifest(path, DEPOT_DELTA.OLD_IDENTITY)

    def test_installed_new_side_matches_manifest_when_ob1_is_present(self):
        if not GAME_ROOT.is_dir():
            self.skipTest("Victoria 3 game root is not installed")
        for entry in self.entries:
            evidence = entry["new"]
            if evidence["size"] is None:
                continue
            path = GAME_ROOT / entry["path"][len("game/") :]
            with self.subTest(path=entry["path"]):
                if evidence["kind"] == "directory":
                    self.assertTrue(path.is_dir())
                    continue
                self.assertEqual("file", evidence["kind"])
                self.assertTrue(path.is_file())
                self.assertEqual(evidence["size"], path.stat().st_size)
                self.assertEqual(
                    evidence["sha1"], hashlib.sha1(path.read_bytes()).hexdigest()
                )


if __name__ == "__main__":
    unittest.main()
