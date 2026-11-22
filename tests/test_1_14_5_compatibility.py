"""Mandatory current-target evidence and the four narrowly scoped SB ports."""

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from tests.je_outcomes import outcome_field, outcome_nodes
from tests.test_zulu_institutions_laws import statements

from tools import build_1_14_5_depot_delta as historical_delta
from tools import check_1_15_2_target as delta
from tools import check_override_inventory as inventory, validate
from tests.test_usuthu_movement_contest import parse

ROOT = Path(__file__).resolve().parents[1]
GAME = validate.find_game_root(None)
BOER_REGIONS = (
    "CAPE_COLONY", "EASTERN_CAPE", "NORTHERN_CAPE", "GRIQUALAND_WEST",
    "NATAL", "ZULULAND", "TRANSVAAL", "EAST_TRANSVAAL", "NORTHERN_TRANSVAAL",
    "VRYSTAAT", "DRAKENSBERG", "BOTSWANA", "LOURENCO_MARQUES", "ZAMBEZIA",
    "ZAMBEZI", "NAMAQUALAND", "HEREROLAND",
)


def read(root, path):
    return (root / path).read_text(encoding="utf-8-sig")


def child(nodes, key):
    return next(value for name, op, value in nodes if name == key)


class CurrentTargetTests(unittest.TestCase):
    def test_exact_build_and_manifest_identity(self):
        self.assertIsNotNone(GAME, "1.15.2 validation requires the installed game")
        app_path = inventory.find_steam_app_manifest(GAME)
        self.assertIsNotNone(app_path, "current Steam build identity is mandatory")
        app = inventory.parse_vdf(app_path.read_text())["AppState"]
        self.assertEqual("26763837", app["buildid"])
        self.assertEqual("5942745929618312121", app["InstalledDepots"]["529341"]["manifest"])
        self.assertEqual("public", app.get("UserConfig", {}).get("BetaKey", "public"))
        settings = json.loads((GAME.parent / "launcher/launcher-settings.json").read_text())
        self.assertEqual("1.15.2", settings["rawVersion"])

    def test_current_manifest_and_installed_payload_are_mandatory(self):
        self.assertIsNotNone(GAME, "current installed payload is mandatory")
        current = delta.depot.decode_manifest(delta.depot.default_manifest_path(delta.NEW), delta.NEW)
        data = json.loads(delta.OUTPUT.read_text())
        self.assertEqual(delta.depot._manifest_summary(delta.NEW), data["new_manifest"])
        self.assertEqual({"changed": 560, "added": 13}, data["counts"])
        self.assertEqual(573, len(data["entries"]))
        for entry in data["entries"]:
            self.assertEqual(current.records[entry["path"]].evidence(), entry["new"])
        delta.verify_current_target(GAME)

    def test_current_manifest_tampering_and_missing_input_fail(self):
        path = delta.depot.default_manifest_path(delta.NEW)
        data = bytearray(path.read_bytes())  # No historical-input skip here.
        data[-1] ^= 1
        with tempfile.TemporaryDirectory() as temporary:
            altered = Path(temporary) / path.name
            with self.assertRaises(FileNotFoundError):
                delta.verify_current_target(GAME, manifest_path=altered)
            altered.write_bytes(data)
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                delta.verify_current_target(GAME, manifest_path=altered)

    def test_current_payload_missing_or_altered_is_rejected(self):
        data = json.loads(delta.OUTPUT.read_text())
        entry = next(e for e in data["entries"] if e["new"]["kind"] == "file")
        with tempfile.TemporaryDirectory() as temporary:
            game = Path(temporary)
            with self.assertRaisesRegex(ValueError, "not an installed file"):
                delta.depot.verify_current_payload({"entries": [entry]}, game)
            path = game / entry["path"].removeprefix("game/")
            path.parent.mkdir(parents=True)
            path.write_text("altered payload")
            with self.assertRaisesRegex(ValueError, "installed evidence"):
                delta.depot.verify_current_payload({"entries": [entry]}, game)

    def test_retained_historical_pair_reproduces_report(self):
        old_path = historical_delta.depot.default_manifest_path(historical_delta.OLD)
        if not old_path.is_file():
            self.skipTest("historical 1.14.4 manifest unavailable; current 1.15.2 checks remain mandatory")
        self.assertEqual(historical_delta.depot.normalized_json(historical_delta.build_delta()), historical_delta.OUTPUT.read_text())


class PortParityTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(GAME, "current Vanilla parity requires 1.14.5")

    def test_colonial_claim_diff_is_only_the_exact_boer_region_guard(self):
        vanilla = parse(read(GAME, "common/diplomatic_actions/56_stake_colonial_claim.txt"))
        sb = parse(read(ROOT, "common/diplomatic_actions/zz_sb_stake_colonial_claim_override.txt"))
        regions = [("state_region", "=", "s:STATE_" + name) for name in BOER_REGIONS]
        guard = ("NOT", "=", [("AND", "=", [
            ("scope:country", "=", [("country_has_primary_culture", "=", "cu:boer")]),
            ("OR", "=", regions),
        ])])
        selection = child(sb, "second_state_trigger")
        self.assertEqual(1, selection.count(guard))
        selection.remove(guard)
        self.assertEqual(vanilla, sb)

    def test_scramble_is_native_except_growth_and_cleanup(self):
        vanilla = statements(read(GAME, "common/journal_entries/00_scramble_for_africa.txt"))
        sb = statements(read(ROOT, "common/journal_entries/zz_sb_scramble_for_africa_override.txt"))
        name = "sb_scramble_for_africa_colonial_growth"
        add = ("add_modifier", "=", [("name", "=", name), ("months", "=", "-1")])
        remove = ("if", "=", [("limit", "=", [("has_modifier", "=", name)]),
                               ("remove_modifier", "=", name)])
        ensure = ("if", "=", [("limit", "=", [("NOT", "=", [("has_modifier", "=", name)])]), add])
        child(sb, "immediate").remove(add)
        child(outcome_nodes(sb, "complete"), "effect").remove(remove)
        child(outcome_nodes(sb, "fail"), "effect").remove(remove)
        child(outcome_nodes(sb, "timeout"), "effect").remove(remove)
        child(child(sb, "on_weekly_pulse"), "effect").remove(ensure)
        self.assertIn(("is_at_war", "=", "no"), child(outcome_nodes(sb, "fail"), "trigger"))
        self.assertEqual(vanilla, sb)

    def test_all_native_formations_except_preserved_portuguese_armies(self):
        path = "common/history/military_formations/00_military_formations_europe.txt"
        vanilla = parse(read(GAME, path))
        sb = parse(read(ROOT, path))
        native_por, sb_por = child(vanilla, "c:POR"), child(sb, "c:POR")
        armies = [n for n in sb_por if ("type", "=", "army") in n[2]]
        # Pre-rebase Portuguese redistribution and African formations, not Vanilla's armies.
        digest = hashlib.sha256(json.dumps(armies, sort_keys=True).encode()).hexdigest()
        self.assertEqual("95d121af4d367da381ee433673adea06849fcb1ff6eabac8579d09382a880cc4", digest)
        for country in (native_por, sb_por):
            country[:] = [n for n in country if ("type", "=", "army") not in n[2]]
        self.assertEqual(vanilla, sb)
        self.assertEqual(14, read(ROOT, path).count("ship_type:ship_type_early_troop_ship"))


if __name__ == "__main__":
    unittest.main()
