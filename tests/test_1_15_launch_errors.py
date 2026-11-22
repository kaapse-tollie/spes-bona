"""Negative map controls for launch defects; no claim of engine dock generation."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import repair_launch_spline as repair
from tools import spline_structured_merge as spline
from tools import validate


class LaunchMapValidationTests(unittest.TestCase):
    def check_fixture(self, *, missing_land_anchor=False, port_on_sea=False,
                      state_bom=True, terrain_bom=False):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            files = {
                'map_data/states.txt': '\ufeff' * state_bom +
                    'STATE_TEST = {\n id = 257\n provinces = { "x9E9742" }\n port = "x9E9742"\n}\n',
                'map_data/terrain.txt': '\ufeff' * terrain_bom + 'x9E9742="plains"\n',
                'map_data/provinces.png': 'decoder fixture',
                'map_data/port.txt': 'game_object_locator = {\n instances = {\n {\n id=257\n'
                    f' position={{ {20 if port_on_sea else 10}.000000 0.000000 10.000000 }}\n'
                    ' }\n }\n}\n',
            }
            for relative, value in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(value, encoding='utf-8')
            points = [repair.point(8414308, 10., 10.)]
            if not missing_land_anchor:
                points.append(repair.point(25703, 10., 10.))
            path = root / 'gfx/map/spline_network/spline_network.splnet'
            path.parent.mkdir(parents=True)
            path.write_bytes(spline.serialize(spline.Model(4, (len(points), 0, 0), tuple(points), (), ())))
            manifest = {
                'state_region_file': 'map_data/states.txt', 'terrain_file': 'map_data/terrain.txt',
                'province_map': 'map_data/provinces.png', 'province_map_height': 100,
                'province_map_sha256': hashlib.sha256((root / 'map_data/provinces.png').read_bytes()).hexdigest(),
                'locator_files': {'port': 'map_data/port.txt'},
                'locator_samples': [{'state': 'STATE_TEST', 'kind': 'port'}],
                'spline_samples': [{'state': 'STATE_TEST', 'kind': 'port', 'anchor': 8414308}],
            }
            (root / 'tools').mkdir()
            (root / 'tools/map_connectivity_manifest.json').write_text(json.dumps(manifest))
            raster = (100, 100, {'x9E9742', 'x78FCFC'}, {(10, 89): 'x9E9742', (20, 89): 'x78FCFC'})
            with patch.object(validate, 'ROOT', root), patch.object(validate, 'decode_rgb_png', return_value=raster):
                return validate.check_map_data()

    def test_valid_pair_and_declared_port_province_pass(self):
        result = self.check_fixture()
        self.assertEqual('PASS', result.status, result.detail)

    def test_missing_land_port_anchor_is_rejected_even_with_a_valid_naval_point(self):
        result = self.check_fixture(missing_land_anchor=True)
        self.assertEqual('FAIL', result.status)
        self.assertIn('naval anchor 8414308 has no land-port anchor 25703', result.detail)

    def test_locator_on_other_province_is_rejected(self):
        result = self.check_fixture(port_on_sea=True)
        self.assertEqual('FAIL', result.status)
        self.assertIn('samples x78FCFC, expected x9E9742', result.detail)

    def test_script_and_generated_table_encoding_are_checked_separately(self):
        for kwargs, message in (({'state_bom': False}, 'state-region script requires'),
                                ({'terrain_bom': True}, 'BOM-free encoding')):
            with self.subTest(kwargs=kwargs):
                result = self.check_fixture(**kwargs)
                self.assertEqual('FAIL', result.status)
                self.assertIn(message, result.detail)


if __name__ == '__main__':
    unittest.main()
