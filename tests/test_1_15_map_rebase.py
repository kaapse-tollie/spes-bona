"""Current map invariants, distinct from historical 1.14 reproduction fixtures."""
from pathlib import Path
import hashlib
import json
import re
import unittest

from tools import repair_launch_spline as repair
from tools import spline_structured_merge as spline
from tools import validate

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "Docs/compatibility/evidence/1_15_0_map"
SPLINE = "gfx/map/spline_network/spline_network.splnet"
STATES = "map_data/state_regions/04_subsaharan_africa.txt"


def scalar(block, name):
    match = re.search(rf"(?m)^\s*{name}\s*=\s*([\d.]+)", block)
    return float(match.group(1)) if match else None


class CurrentMapRebaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = validate.find_game_root(None)
        if cls.game is None:
            raise AssertionError("1.15 map acceptance requires the pinned native game")
        cls.native_states = validate.parse_state_blocks(cls.game / STATES)
        cls.states = validate.parse_state_blocks(ROOT / STATES)
        cls.world = json.loads((EVIDENCE / "world_rebase.json").read_text())

    def test_native_spline_records_outside_authored_delta_remain_exact(self):
        evidence = json.loads((EVIDENCE / "spline_merge.json").read_text())
        current_bytes = (ROOT / SPLINE).read_bytes()
        native_bytes = (self.game / SPLINE).read_bytes()
        launch = json.loads((ROOT / "Docs/compatibility/evidence/1_15_0_launch_2026_11_05/map_repair.json").read_text())
        self.assertEqual(launch["result_spline_sha256"], hashlib.sha256(current_bytes).hexdigest())
        self.assertEqual(evidence["result_sha256"], launch["input_spline_sha256"])
        self.assertEqual(evidence["native_1_15_sha256"], hashlib.sha256(native_bytes).hexdigest())
        current, native = spline.parse(current_bytes), spline.parse(native_bytes)
        self.assertEqual(current_bytes, spline.serialize(current))
        spline.validate_references(current)
        repair.validate_link_endpoints(current)
        # Reverse only the recorded launch repair to reproduce the exact initial
        # 1.15 merge. Historical evidence stays immutable, including point order.
        points = [repair.point(p.key, *launch['moved_points'][str(p.key)]['before'])
                  if str(p.key) in launch['moved_points'] else p for p in current.points
                  if str(p.key) not in launch['added_points']]
        merged = spline.Model(current.version, (len(points), len(current.strips), len(current.links)),
                              tuple(points), current.strips, current.links)
        self.assertEqual(evidence['result_sha256'], hashlib.sha256(spline.serialize(merged)).hexdigest())
        current_points = spline.record_map(current.points)
        self.assertEqual((4834.0, 855.0), current_points[25703].payload)
        self.assertEqual(current_points[26203].payload, current_points[8414808].payload)
        for section in ("points", "strips", "links"):
            delta = evidence["sb_delta"][section]
            changed = set(delta["added"] + delta["modified"] + delta["removed"])
            restored = set()
            if section == 'points':
                restored = {int(key) for key in launch['added_points']}
                changed |= restored | {int(key) for key in launch['moved_points']}
            final = spline.record_map(getattr(current, section))
            original = spline.record_map(getattr(native, section))
            self.assertEqual({key: value for key, value in original.items() if key not in changed},
                             {key: value for key, value in final.items() if key not in changed})
            self.assertFalse((set(delta["removed"]) - restored) & final.keys())
            self.assertTrue(set(delta["added"] + delta["modified"]) <= final.keys())

    def test_native_land_state_naval_anchors_have_matching_land_port_anchors(self):
        # Sea-region anchors are outside the land-state set. Do not require a
        # naval anchor for river ports where native does not supply one.
        points = spline.record_map(spline.parse((self.game / SPLINE).read_bytes()).points)
        checked = 0
        for path in (self.game / 'map_data/state_regions').glob('*.txt'):
            for name, block in validate.parse_state_blocks(path).items():
                if 'port' not in dict(validate.HUB_RE.findall(block)):
                    continue
                match = validate.STATE_ID_RE.search(block)
                if match is None:
                    continue
                identifier = int(match.group(1))
                if (1 << 23) + identifier * 100 in points:
                    self.assertTrue(identifier * 100 + 3 in points, name)
                    checked += 1
        self.assertGreater(checked, 100)

    def test_native_state_regions_and_copper_are_restored(self):
        authored = set(self.world[STATES]["preserved_SB_blocks"])
        self.assertEqual(set(self.native_states) | authored, set(self.states))
        for name, native in self.native_states.items():
            if name not in authored:
                self.assertEqual(native, self.states[name], name)
        for name, amount in {"STATE_NAMAQUALAND": 9, "STATE_ZAMBIA": 21, "STATE_KATANGA": 35}.items():
            self.assertEqual(amount, scalar(self.states[name], "building_copper_mine"))
            self.assertEqual(scalar(self.native_states[name], "building_copper_mine"), amount)
        self.assertIsNone(scalar(self.states["STATE_NORTHERN_CAPE"], "building_lead_mine"))
        self.assertEqual(10, scalar(self.states["STATE_HEREROLAND"], "building_lead_mine"))
        self.assertEqual(2, scalar(self.states["STATE_NAMAQUALAND"], "building_lead_mine"))
        # Copper's three native parents are each counted once despite SB partitions.
        self.assertEqual(65, sum(scalar(block, "building_copper_mine") or 0
                                 for block in self.states.values()))

    def test_cold_bounds_follow_parent_intensities_without_summing_children(self):
        for name, values in self.world[STATES]["cold"].items():
            parent = self.native_states[values["parent"]]
            for bound in ("min_cold_effect", "max_cold_effect"):
                self.assertEqual(scalar(parent, bound), scalar(self.states[name], bound), name)

    def test_locators_and_terrain_retain_every_unauthored_native_record(self):
        evidence = json.loads((EVIDENCE / "text_map_merge.json").read_text())
        for path, detail in evidence.items():
            if "changed_ids" not in detail:
                continue
            final, duplicates = validate.parse_locator_instances(ROOT / path)
            native, _ = validate.parse_locator_instances(self.game / path)
            self.assertEqual([], duplicates)
            changes = set(detail["changed_ids"] + detail["added_SB_ids"])
            self.assertEqual({key: value for key, value in native.items() if key not in changes},
                             {key: value for key, value in final.items() if key not in changes}, path)
        terrain = "map_data/province_terrains.txt"
        pattern = r'(?m)^\s*(x[0-9A-Fa-f]{6})\s*=\s*"?(\w+)'
        native = dict(re.findall(pattern, (self.game / terrain).read_text(encoding="utf-8-sig")))
        final = dict(re.findall(pattern, (ROOT / terrain).read_text(encoding="utf-8-sig")))
        delta = evidence[terrain]["authored_desert_provinces"]
        self.assertEqual(native | delta, final)

    def test_native_world_has_no_retired_state_references(self):
        text = (ROOT / "common/history/states/00_states.txt").read_text(encoding="utf-8-sig")
        for name in ("KOSTROMA", "LITHUANIA", "SARATOV", "TULA", "VOLOGDA"):
            self.assertRegex(text, rf"s:STATE_{name}\s*=")
        for directory in ("common/history", "common/country_formation"):
            for path in (ROOT / directory).rglob("*.txt"):
                self.assertNotRegex(path.read_text(encoding="utf-8-sig"),
                                    r"\bSTATE_(?:KAUNAS|GALICH|TARTARIA|CHUKOTKA)\b", str(path))


if __name__ == "__main__":
    unittest.main()
