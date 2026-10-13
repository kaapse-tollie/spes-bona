"""Current-beta contracts: Vanilla parity, preserved CMF additions, and exact evidence."""

import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest

from tools import build_1_14_3_depot_delta as delta
from tools import cmf_patch, check_override_inventory as inventory, validate


ROOT = Path(__file__).resolve().parents[1]
GAME = validate.find_game_root(None)
MOVEMENT = "common/political_movements/ycom_02_cultural_movement.txt"
SB_MOVEMENT = "common/political_movements/zz_sb_cultural_majority_movement_override.txt"


def tokens(source):
    source = re.sub(r"#[^\n]*", "", source)
    return re.findall(r'"(?:\\.|[^"\\])*"|[{}=]|[^\s{}=]+', source)


class CurrentBetaTests(unittest.TestCase):
    def test_exact_current_build_and_depot_report(self):
        self.assertIsNotNone(GAME, "1.14.3 release validation requires the installed game")
        app_path = inventory.find_steam_app_manifest(GAME)
        self.assertIsNotNone(app_path, "current Steam build identity is required")
        app = inventory.parse_vdf(app_path.read_text())["AppState"]
        self.assertEqual("25347710", app["buildid"])
        self.assertEqual("5228357714133991559", app["InstalledDepots"]["529341"]["manifest"])
        self.assertEqual("1.14-openbeta", app["UserConfig"]["BetaKey"])
        settings = json.loads((GAME.parent / "launcher/launcher-settings.json").read_text())
        self.assertEqual("1.14.3", settings["rawVersion"])
        data = delta.build_delta()
        self.assertEqual(delta.depot.normalized_json(data), delta.OUTPUT.read_text())
        self.assertEqual({"added": 3, "changed": 92, "removed": 0, "total": 95}, data["counts"])
        delta.depot.verify_current_payload(data, GAME)
        paths = {e["path"] for e in data["entries"]}
        self.assertIn("game/common/script_values/00_infamy_values.txt", paths)
        self.assertIn("game/common/political_movements/02_cultural_movement.txt", paths)
        locked = json.loads((ROOT / "Docs/compatibility/override_inventory.json").read_text())
        self.assertFalse(paths & {"game/" + e["path"] for e in locked["same_path_files"]})
        self.assertFalse(any(p.startswith("game/map_data/") or "spline_network" in p for p in paths))

    def test_current_manifest_tampering_is_rejected(self):
        path = delta.depot.default_manifest_path(delta.NEW)
        data = bytearray(path.read_bytes())
        data[-1] ^= 1
        with tempfile.TemporaryDirectory() as temporary:
            altered = Path(temporary) / path.name
            altered.write_bytes(data)
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                delta.depot.decode_manifest(altered, delta.NEW)

    def test_territorial_goals_equal_vanilla_except_cmf_hook(self):
        self.assertIsNotNone(GAME)
        for filename in ("00_annex_country.txt", "03_conquer_state.txt", "21_return_state.txt"):
            relative = "common/war_goal_types/" + filename
            with self.subTest(goal=filename):
                self.assertFalse((ROOT / relative).exists())
                patched = (cmf_patch.DEFAULT_MANIFEST.parent / "files" / relative).read_text(encoding="utf-8-sig")
                vanilla = (GAME / relative).read_text(encoding="utf-8-sig")
                hook = "tlim_land_grab_war_goal_possible_trigger = yes"
                self.assertEqual(1, patched.count(hook))
                self.assertEqual(tokens(vanilla), tokens(patched.replace(hook, "")))
                self.assertIn("method = territorial", patched)
                self.assertNotIn("assent_required", patched)
                self.assertIn("country_infamy_value" if filename.startswith("00_") else "state_infamy_value", patched)

    def test_cultural_api_matches_vanilla_and_preserves_cmf_extensions(self):
        self.assertIsNotNone(GAME)
        patch = cmf_patch.load_patch()
        entry = next(e for e in patch["files"] if e["path"] == MOVEMENT)
        source = (cmf_patch.DEFAULT_MANIFEST.parent / entry["payload"]).read_text(encoding="utf-8-sig")
        sb = (ROOT / SB_MOVEMENT).read_text(encoding="utf-8-sig")
        vanilla = (GAME / "common/political_movements/02_cultural_movement.txt").read_text(encoding="utf-8-sig")
        comparisons = re.compile(r"primary_cultures_percent_state\s*=\s*\{\s*target_country\s*=\s*owner\s+value\s*>=\s*([\d.]+)\s*\}")
        expected = comparisons.findall(inventory.find_object(vanilla, "movement_cultural_majority"))
        self.assertEqual(["0.05", "0.75", "0.5", "0.25", "0.1", "0.05"], expected)
        for text in (source, sb):
            self.assertEqual(expected, comparisons.findall(text))
            self.assertEqual(1, text.count('add = "this.primary_cultures_percent_state(owner)"'))
            self.assertNotRegex(text, r"primary_cultures_percent_state\s*(?:>=|<=|>|<)")
        # Undo only the API migration: all upstream CMF extensions and sibling
        # movement definitions must reproduce the immutable release file.
        old = re.sub(
            r"(?m)^(\s*)primary_cultures_percent_state = \{\n\s*target_country = owner\n\s*value >= ([\d.]+)\n\s*\}",
            lambda m: m[1] + "primary_cultures_percent_state >= " + m[2], source,
        ).replace("primary_cultures_percent_state(owner)", "primary_cultures_percent_state")
        self.assertEqual(entry["original_sha256"], hashlib.sha256(old.encode("utf-8-sig")).hexdigest())
        cmf_body = inventory.find_object(source, "movement_cultural_majority", directive="REPLACE")
        sb_body = inventory.find_object(sb, "movement_cultural_majority", directive="REPLACE")
        self.assertEqual(1, sb_body.count("NOT = { country_definition = cd:CAP }"))
        self.assertEqual(1, sb_body.count("owner = { country_definition = cd:CAP }"))
        without_cap = sb_body.replace("NOT = { country_definition = cd:CAP }", "")
        without_cap = re.sub(r"disband_trigger\s*=\s*\{\s*owner\s*=\s*\{\s*country_definition\s*=\s*cd:CAP\s*\}\s*\}", "", without_cap)
        self.assertEqual(tokens(cmf_body), tokens(without_cap))

    def test_current_patch_identity_and_upstream_contracts(self):
        self.assertEqual("sb-1.14.3-r1", cmf_patch.REVISION)
        patch = cmf_patch.load_patch()
        self.assertEqual("1.66.0", patch["base_tag"])
        self.assertEqual(5, len(patch["files"]))
        self.assertIsNotNone(GAME)
        cmf_patch.verify_upstream(GAME)
        cmf_patch.verify_install(ROOT.parent / "Community Mod Framework")


if __name__ == "__main__":
    unittest.main()
