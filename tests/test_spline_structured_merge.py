from __future__ import annotations

from pathlib import Path
import hashlib
import json
import os
import subprocess
import unittest

from tools import spline_structured_merge as spline


ROOT = Path(__file__).resolve().parents[1]
SPLINE_PATH = ROOT / "gfx/map/spline_network/spline_network.splnet"
REPORT_PATH = (
    ROOT / "Docs/compatibility/1_13_11_to_1_14_0_ob1_spline_merge.json"
)
BASELINE_COMMIT = "51c98bf32fc9f9049c99f858f5a558bdfde0dffe"
BASELINE_SPLINE_PATH = "gfx/map/spline_network/spline_network.splnet"
TOOL_SHA256 = "07ef97cdafd0feb12b219bbed7d3df033e26abc9be98d377cde90f7cc8c7b96c"
NORMALIZED_INPUT_PATHS = {
    "old": "vanilla-1.13.11-build-24799966/gfx/map/spline_network/spline_network.splnet",
    "new": "vanilla-1.14.0-ob1-build-25081502/gfx/map/spline_network/spline_network.splnet",
    "sb": (
        "spes-bona-51c98bf32fc9f9049c99f858f5a558bdfde0dffe/"
        "gfx/map/spline_network/spline_network.splnet"
    ),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def external_input_paths() -> dict[str, Path] | None:
    old = Path(
        os.environ.get(
            "SB_SPLINE_1_13_11",
            str(
                Path.home()
                / "Documents/Paradox Interactive/Victoria 3/mod/References/"
                "spline_network_backups/spline_network_1_13_8_vanilla.splnet"
            ),
        )
    ).expanduser()
    game_root = Path(
        os.environ.get(
            "VIC3_GAME_ROOT",
            str(
                Path.home()
                / "Library/Application Support/Steam/steamapps/common/"
                "Victoria 3/game"
            ),
        )
    ).expanduser()
    new = game_root / "gfx/map/spline_network/spline_network.splnet"
    if not old.is_file() or not new.is_file():
        return None
    return {"old": old, "new": new}


class SplineStructuredMergeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = SPLINE_PATH.read_bytes()
        cls.model = spline.parse(cls.data)
        cls.report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))

    def test_promoted_decoder_is_the_hash_verified_strict_tool(self):
        tool = ROOT / "tools/spline_structured_merge.py"
        self.assertEqual(TOOL_SHA256, sha256(tool.read_bytes()))
        self.assertEqual(4, self.model.version)

    def test_merged_binary_has_exact_identity_counts_and_closed_graph(self):
        self.assertEqual(spline.KNOWN_SIZE["merged"], len(self.data))
        self.assertEqual(spline.KNOWN_SHA256["merged"], sha256(self.data))
        self.assertEqual(spline.KNOWN_COUNTS["merged"], self.model.counts)
        self.assertEqual(self.data, spline.serialize(self.model))
        spline.validate_references(self.model)

        for section in (self.model.points, self.model.strips, self.model.links):
            keys = [record.key for record in section]
            self.assertEqual(len(keys), len(set(keys)))

    def test_report_is_normalized_and_locks_input_output_evidence(self):
        self.assertEqual(set(NORMALIZED_INPUT_PATHS), set(self.report["inputs"]))
        for label, expected_path in NORMALIZED_INPUT_PATHS.items():
            evidence = self.report["inputs"][label]
            self.assertEqual(expected_path, evidence["path"])
            self.assertFalse(Path(evidence["path"]).is_absolute())
            self.assertEqual(spline.KNOWN_SIZE[label], evidence["bytes"])
            self.assertEqual(spline.KNOWN_SHA256[label], evidence["sha256"])
            self.assertEqual(list(spline.KNOWN_COUNTS[label]), evidence["counts"])
            self.assertTrue(evidence["round_trip_exact"])

        merge = self.report["merge"]
        self.assertEqual([], merge["conflicts"])
        self.assertTrue(merge["reverse_direction_byte_identical"])
        self.assertTrue(merge["references_valid"])
        self.assertEqual(spline.KNOWN_SIZE["merged"], merge["bytes"])
        self.assertEqual(spline.KNOWN_SHA256["merged"], merge["sha256"])
        self.assertEqual(list(spline.KNOWN_COUNTS["merged"]), merge["counts"])

    def test_ob1_european_records_and_sb_southern_african_records_survive(self):
        # These are the audited OB1 Scania and French Low Countries/Picardy changes.
        points = spline.section_lookup(self.model, "points")
        strips = spline.section_lookup(self.model, "strips")
        expected_points = {
            8388908: (4389.43798828125, 2924.208740234375),
            8391908: (4149.6474609375, 2788.444580078125),
            8392008: (4136.5185546875, 2764.40869140625),
            277150838: (4377.90234375, 2949.68798828125),
        }
        expected_strips = {
            1658883: (8391908, 277150349, 277150350, 277150352, 8699108),
            1661187: (8392008, 277150355, 277150356, 277150357, 8691408),
            1661955: (8388908, 277150838, 8690508),
        }
        for key, payload in expected_points.items():
            self.assertEqual(payload, points[key].payload)
        for key, payload in expected_strips.items():
            self.assertEqual(payload, strips[key].payload)
        for key in (277145160, 277150307, 277150308, 277150309):
            self.assertNotIn(key, points)
        for key in (299267, 443907, 448003):
            self.assertNotIn(key, strips)

        # SB's Natal reindex and Southern African strips remain exact.
        self.assertEqual((4797.912109375, 804.8287963867188), points[121303].payload)
        self.assertEqual((4785.4609375, 816.4765625), points[121304].payload)
        for key in (25703, 25704):
            self.assertNotIn(key, points)
        expected_natal = {
            (121303, 26003, 16),
            (121304, 25804, 12),
            (121303, 121304, 4),
            (25700, 121304, 9),
        }
        actual_natal = {
            (int(record.payload[0]), int(record.payload[-1]), len(record.payload))
            for record in self.model.strips
            if record.payload
            and (
                record.payload[0] in (121303, 121304)
                or record.payload[-1] in (121303, 121304)
            )
        }
        self.assertEqual(expected_natal, actual_natal)
        spline.validate_known_merge(self.model, self.data)

    def test_same_key_divergence_fails_closed(self):
        base = (spline.Record(1, b"base", ()),)
        variant = (spline.Record(1, b"variant", ()),)
        target = (spline.Record(1, b"target", ()),)
        with self.assertRaises(spline.MergeConflict):
            spline.apply_delta(base, variant, target, "synthetic")

    def test_exact_forward_and_reverse_merge_reproduce_committed_artifacts(self):
        paths = external_input_paths()
        if paths is None:
            self.skipTest("exact external Vanilla 1.13.11/1.14 OB1 spline inputs unavailable")

        try:
            sb_baseline = subprocess.run(
                ["git", "show", f"{BASELINE_COMMIT}:{BASELINE_SPLINE_PATH}"],
                cwd=ROOT,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ).stdout
        except (FileNotFoundError, subprocess.CalledProcessError) as error:
            self.skipTest(f"approved SB baseline spline unavailable from git: {error}")

        blobs = {
            "old": paths["old"].read_bytes(),
            "new": paths["new"].read_bytes(),
            "sb": sb_baseline,
        }
        models = {label: spline.parse(data) for label, data in blobs.items()}
        spline.validate_known_inputs(blobs, models)

        forward = spline.merge(models["old"], models["sb"], models["new"], "SB onto 1.14")
        reverse = spline.merge(models["old"], models["new"], models["sb"], "1.14 onto SB")
        forward_data = spline.serialize(forward)
        reverse_data = spline.serialize(reverse)
        self.assertEqual(forward_data, reverse_data)
        self.assertEqual(self.data, forward_data)

        regenerated_report = spline.build_report(
            {label: Path(path) for label, path in NORMALIZED_INPUT_PATHS.items()},
            blobs,
            models,
            forward,
            forward_data,
        )
        self.assertEqual(self.report, regenerated_report)


if __name__ == "__main__":
    unittest.main()
