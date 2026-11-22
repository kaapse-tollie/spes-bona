"""Historical 1.14.3 evidence and current CMF/SB compatibility contracts."""

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


class HistoricalEvidenceTests(unittest.TestCase):
    def test_recorded_1_14_3_report_structure(self):
        data = json.loads(delta.OUTPUT.read_text())
        self.assertEqual({"added": 3, "changed": 92, "removed": 0, "total": 95}, data["counts"])
        self.assertEqual(delta.depot._manifest_summary(delta.NEW), data["new_manifest"])
        paths = {e["path"] for e in data["entries"]}
        self.assertEqual(95, len(paths))
        self.assertIn("game/common/script_values/00_infamy_values.txt", paths)
        self.assertIn("game/common/political_movements/02_cultural_movement.txt", paths)
        self.assertFalse(any(p.startswith("game/map_data/") or "spline_network" in p for p in paths))

    def test_historical_report_reproduces_when_both_manifests_are_retained(self):
        if not all(delta.depot.default_manifest_path(i).is_file() for i in (delta.OLD, delta.NEW)):
            self.skipTest("historical 1.14.2/1.14.3 Steam manifests unavailable")
        self.assertEqual(delta.depot.normalized_json(delta.build_delta()), delta.OUTPUT.read_text())

    def test_historical_installed_payload_only_on_its_exact_build(self):
        app_path = inventory.find_steam_app_manifest(GAME) if GAME else None
        if app_path is None:
            self.skipTest("historical 1.14.3 installation unavailable")
        app = inventory.parse_vdf(app_path.read_text())["AppState"]
        if app["buildid"] != "25347710":
            self.skipTest("historical 1.14.3 build is not installed")
        self.assertEqual("5228357714133991559", app["InstalledDepots"]["529341"]["manifest"])
        self.assertEqual("1.14-openbeta", app["UserConfig"]["BetaKey"])
        settings = json.loads((GAME.parent / "launcher/launcher-settings.json").read_text())
        self.assertEqual("1.14.3", settings["rawVersion"])
        delta.depot.verify_current_payload(json.loads(delta.OUTPUT.read_text()), GAME)

    def test_historical_manifest_tampering_is_rejected_when_available(self):
        path = delta.depot.default_manifest_path(delta.NEW)
        if not path.is_file():
            self.skipTest("historical 1.14.3 Steam manifest unavailable")
        data = bytearray(path.read_bytes())
        data[-1] ^= 1
        with tempfile.TemporaryDirectory() as temporary:
            altered = Path(temporary) / path.name
            altered.write_bytes(data)
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                delta.depot.decode_manifest(altered, delta.NEW)


class CurrentCmfPatchTests(unittest.TestCase):
    def test_territorial_goals_are_native_with_only_authored_sb_deltas(self):
        self.assertIsNotNone(GAME)
        for filename in ("00_annex_country.txt", "03_conquer_state.txt", "21_return_state.txt"):
            relative = "common/war_goal_types/" + filename
            with self.subTest(goal=filename):
                self.assertFalse((ROOT / relative).exists())
                self.assertFalse((ROOT.parent / "Community Mod Framework" / relative).exists())
                vanilla = (GAME / relative).read_text(encoding="utf-8-sig")
                if filename == "21_return_state.txt":
                    continue
                key = "annex_country" if filename.startswith("00_") else "conquer_state"
                sbfile = "zz_sb_zululand_annex_handoff.txt" if key == "annex_country" else "zz_sb_swazi_conquest_override.txt"
                body = inventory.find_object((ROOT / "common/war_goal_types" / sbfile).read_text(encoding="utf-8-sig"), key, directive="REPLACE")
                native = inventory.find_object(vanilla, key)
                self.assertNotIn("tlim_land_grab", body)
                if key == "conquer_state":
                    self.assertEqual(2, body.count("sb_swazi_conquest_target_allowed = yes"))
                    body = body.replace("sb_swazi_conquest_target_allowed = yes", "")
                else:
                    # The foreign-target handoff remains exactly the existing SB effect;
                    # all remaining fields must reproduce current native behaviour.
                    start = body.index("\ton_enforced = {")
                    end = body.index("\n\tmirrored_wargoal", start)
                    handoff = body[start:end]
                    self.assertIn("var:sb_british_zulu_annex_play_scope ?= scope:diplomatic_play", handoff)
                    self.assertIn("scope:target_country = { sb_zululand_shelter_mandlakazi_chief = yes }", handoff)
                    self.assertIn("sb_british_shelter_preannex_zulu_royals = yes", handoff)
                    a = native.index("\ton_enforced = {"); b = native.index("\n\tmirrored_wargoal", a)
                    body = body[:start] + native[a:b] + body[end:]
                self.assertEqual(tokens(native), tokens(body.removeprefix("REPLACE:")))

    def test_cultural_api_matches_vanilla_and_preserves_cmf_extensions(self):
        self.assertIsNotNone(GAME)
        # CMF supplies both the cultural API and the minority secession flag.
        source = (ROOT.parent / "Community Mod Framework" / MOVEMENT).read_text(encoding="utf-8-sig")
        sb = (ROOT / SB_MOVEMENT).read_text(encoding="utf-8-sig")
        vanilla = (GAME / "common/political_movements/02_cultural_movement.txt").read_text(encoding="utf-8-sig")
        comparisons = re.compile(r"primary_cultures_percent_state\s*=\s*\{\s*target_country\s*=\s*owner\s+value\s*>=\s*([\d.]+)\s*\}")
        expected = comparisons.findall(inventory.find_object(vanilla, "movement_cultural_majority"))
        self.assertEqual(["0.05", "0.75", "0.5", "0.25", "0.1", "0.05"], expected)
        for text in (source, sb):
            self.assertEqual(expected, comparisons.findall(text))
            self.assertEqual(1, text.count('add = "this.primary_cultures_percent_state(owner)"'))
            self.assertNotRegex(text, r"primary_cultures_percent_state\s*(?:>=|<=|>|<)")
        cmf_body = inventory.find_object(source, "movement_cultural_majority", directive="REPLACE")
        sb_body = inventory.find_object(sb, "movement_cultural_majority", directive="REPLACE")
        self.assertEqual(1, sb_body.count("NOT = { country_definition = cd:CAP }"))
        self.assertEqual(1, sb_body.count("owner = { country_definition = cd:CAP }"))
        without_cap = sb_body.replace("NOT = { country_definition = cd:CAP }", "")
        without_cap = without_cap.replace("owner = { country_definition = cd:CAP }", "")
        from tests.test_performance_pass import canonical_trigger
        from tests.test_zulu_institutions_laws import child, statements
        old_filter = child(child(cmf_body, 'additional_radicalism_factors'), 'any_political_movement')
        new_filter = child(child(without_cap, 'additional_radicalism_factors'), 'any_political_movement')
        self.assertEqual(canonical_trigger(statements(old_filter)), canonical_trigger(statements(new_filter)))
        without_cap = without_cap.replace(new_filter, old_filter, 1)
        # Zero-radical pops skip only the neutral competing-movement multiplier.
        weight = child(without_cap, 'pop_support_weight')
        neutral_guard = 'NOT = { pop_radical_fraction = 0 }'
        self.assertEqual(1, weight.count(neutral_guard))
        without_cap = without_cap.replace(weight, weight.replace(neutral_guard, '', 1), 1)
        self.assertEqual(tokens(cmf_body), tokens(without_cap))

    def test_current_patch_identity_and_upstream_contracts(self):
        self.assertEqual("sb-1.15.2-r1", cmf_patch.REVISION)
        patch = cmf_patch.load_patch()
        self.assertEqual("1.67.9", patch["base_tag"])
        previous = json.loads((ROOT / "patches/cmf/sb-1.15.1-r2/manifest.json").read_text())
        for entry in previous["files"]:
            self.assertIn(entry, patch["files"])
        self.assertEqual(13, len(patch["files"]))
        self.assertEqual(25, len(patch["upstream_contracts"]))
        contracts = {(e["path"], e["key"]): e for e in patch["upstream_contracts"]}
        for old in previous["upstream_contracts"]:
            current = contracts[old["path"], old["key"]]
            self.assertEqual(old["object_sha256"], current["object_sha256"])
        self.assertIsNotNone(GAME)
        cmf_patch.verify_upstream(GAME)
        cmf_patch.verify_install(ROOT.parent / "Community Mod Framework")


if __name__ == "__main__":
    unittest.main()
