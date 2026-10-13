from pathlib import Path
import re
import subprocess
import tempfile
import unittest

from tools import repair_launch_spline as repair
from tools import spline_structured_merge as spline
from tools import validate

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '9f77cac7696d3ba8f2d899e8928301a6f52ddd8c'
SPLINE = 'gfx/map/spline_network/spline_network.splnet'


class LaunchErrorTests(unittest.TestCase):
    def test_create_building_requires_a_direct_level_or_ownership(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            effects = root / 'common/scripted_effects'
            effects.mkdir(parents=True)
            path = effects / 'fixture.txt'
            for body in ('building = building_maize_farm reserves = 1',
                         'building = building_maize_farm bogus = { level = 1 }'):
                path.write_text('fixture = { create_building = { ' + body + ' } }')
                self.assertTrue(any('requires level or add_ownership' in e
                                    for e in validate.runtime_script_hazards(root)))
            for body in ('building = building_maize_farm level = 1',
                         'building = building_maize_farm add_ownership = { country = { country = c:ORA levels = 1 } }'):
                path.write_text('fixture = { create_building = { ' + body + ' } }')
                self.assertEqual([], validate.runtime_script_hazards(root))

    def test_frontier_start_does_not_require_unresearched_arms_technology(self):
        history = (ROOT / 'common/history/countries/ora - oranje.txt').read_text(encoding='utf-8-sig')
        buildings = (ROOT / 'common/history/buildings/04_subsaharan_africa.txt').read_text(encoding='utf-8-sig')
        state = validate.extract_braced(buildings, buildings.index('s:STATE_VRYSTAAT='))
        ora = validate.extract_braced(state, state.index('region_state:ORA='))
        self.assertNotIn('building_arms_industry', ora)
        self.assertNotIn('add_technology_researched = gunsmithing', history)
        self.assertIn('law_right_of_assembly', history)

    def test_sigananda_has_a_localized_template_name(self):
        template = (ROOT / 'common/character_templates/sb_zulu_dynasty_characters.txt').read_text(encoding='utf-8-sig')
        self.assertIn('first_name = "Sigananda"', template)
        names = ''.join(p.read_text(encoding='utf-8-sig') for p in (ROOT / 'localization/english').rglob('*.yml'))
        self.assertRegex(names, r'(?m)^Sigananda:0 "Sigananda"$')

    def test_link_key_round_trip_preserves_style_and_full_anchor_ids(self):
        for a, b, style in [(121303, 26003, 1), (8414308, 8699208, 3)]:
            key = repair.link_key(a, b, style)
            self.assertEqual({a, b}, set(repair.link_endpoints(key)))
            self.assertEqual(style, key & 63)

    def test_launch_repair_reproduces_deployed_asset_and_rejects_old_links(self):
        original = subprocess.check_output(['git', 'show', BASELINE + ':' + SPLINE], cwd=ROOT)
        with self.assertRaisesRegex(ValueError, 'encodes'):
            repair.validate_link_endpoints(spline.parse(original))
        current = (ROOT / SPLINE).read_bytes()
        self.assertEqual(current, repair.repair(original))
        model = spline.parse(current)
        repair.validate_link_endpoints(model)
        points = spline.record_map(model.points)
        self.assertEqual((4798.4833984375, 804.4346313476562), points[8509908].payload)
        for anchor in (8414108, 8414308, 8414808, 8509908):
            self.assertTrue(any(anchor in repair.link_endpoints(link.key)
                                and link.key & 63 == 3 for link in model.links))
        # Every logged non-adjacent route now resolves through its actual state.
        endpoints = {frozenset(repair.link_endpoints(link.key)) for link in model.links}
        for a, b in [(121304, 25804), (121303, 26003), (25503, 26203), (122104, 26300)]:
            self.assertIn(frozenset((a, b)), endpoints)
        # The OB1 European changes remain byte-for-byte intact.
        original_points = spline.record_map(spline.parse(original).points)
        for anchor in (8388908, 8391908, 8392008, 277150838):
            self.assertEqual(original_points[anchor], points[anchor])

    def test_repair_texture_alias_matches_shipped_ob1_asset(self):
        game = validate.find_game_root(None)
        if game is None:
            self.skipTest('installed OB1 game unavailable')
        self.assertEqual((game / 'gfx/interface/icons/generic_icons/repairing.dds').read_bytes(),
                         (ROOT / 'gfx/interface/icons/alert_icons/repairing.dds').read_bytes())


if __name__ == '__main__':
    unittest.main()
