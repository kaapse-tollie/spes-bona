"""Impassable-coast graph correction; native dock generation still needs DP."""
from dataclasses import replace
from pathlib import Path
import unittest

from tools import check_naval_network as naval
from tools import repair_launch_spline as repair
from tools import spline_structured_merge as spline

ROOT = Path(__file__).resolve().parents[1]


class HarbourDockingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = naval.find_game_root(None)
        if cls.game is None:
            raise AssertionError('Pinned native map required')
        cls.native_source = (cls.game / naval.NETWORK_PATH).read_text(encoding='utf-8-sig')
        cls.native = naval.parse_naval_network_text(cls.native_source)
        cls.impassable = naval.impassable_provinces(list((ROOT / 'map_data/state_regions').glob('*.txt')))

    def test_native_control_has_no_harbours_on_impassable_land(self):
        native_impassable = naval.impassable_provinces(list((self.game / 'map_data/state_regions').glob('*.txt')))
        self.assertFalse(any(n.type == 'harbor' and n.province in native_impassable for n in self.native.nodes))
        self.assertEqual(self.native_source, naval.prune_impassable_harbours(self.native_source, native_impassable))

    def test_only_the_fifteen_logged_harbour_leaves_and_their_edges_are_removed(self):
        expected_ids = {8753, 8754, 8755, 8756, 8758, 8759, 8760, 8761,
                        8762, 8763, 8764, 8765, 8835, 8837, 8839}
        removed = {n.index for n in self.native.nodes if n.type == 'harbor' and n.province in self.impassable}
        self.assertEqual(expected_ids, removed)
        for index in removed:
            self.assertEqual(1, self.native.degrees[index])
        current_source = (ROOT / naval.NETWORK_PATH).read_text(encoding='utf-8-sig')
        current = naval.parse_naval_network_text(current_source)
        kept = [n for n in self.native.nodes if n.index not in removed]
        self.assertEqual(10995, len(current.nodes))
        self.assertEqual(11076, len(current.connections))
        self.assertEqual([replace(n, index=i) for i, n in enumerate(kept)], list(current.nodes))
        old_bodies = naval.flat_record_bodies(naval.assignment_block(self.native_source, 'nodes'), 'nodes')
        new_bodies = naval.flat_record_bodies(naval.assignment_block(current_source, 'nodes'), 'nodes')
        self.assertEqual(tuple(body for i, body in enumerate(old_bodies) if i not in removed), new_bodies)
        remap = {n.index: i for i, n in enumerate(kept)}
        self.assertEqual(tuple((remap[a], remap[b]) for a, b in self.native.connections
                               if a not in removed and b not in removed), current.connections)
        self.assertFalse(any(n.type == 'harbor' and n.province in self.impassable for n in current.nodes))

    def test_pruning_reindexes_edges_and_preserves_the_passable_harbour(self):
        source = '''nodes = {
            { province=x000000 x=0 y=0 type=sea }
            { province=x000001 x=1 y=0 type=harbor }
            { province=x000002 x=2 y=0 type=harbor }
            { province=x000003 x=3 y=0 type=sea }
        }
        connections = { { from=0 to=1 } { from=0 to=2 } { from=0 to=3 } }
        '''
        result = naval.parse_naval_network_text(naval.prune_impassable_harbours(source, {'x000001'}))
        self.assertEqual(['x000000', 'x000002', 'x000003'], [n.province for n in result.nodes])
        self.assertEqual(((0, 1), (0, 2)), result.connections)
        self.assertEqual((), naval.validate_state_ports(result, (
            naval.StatePort('STATE_PASSABLE', 'x000002', Path('fixture')),)))

    def test_pruning_rejects_a_harbour_used_as_a_through_route(self):
        source = '''nodes = {
            { province=x000000 x=0 y=0 type=sea }
            { province=x000001 x=1 y=0 type=harbor }
            { province=x000002 x=2 y=0 type=sea }
        }
        connections = { { from=0 to=1 } { from=1 to=2 } }
        '''
        with self.assertRaisesRegex(naval.NavalNetworkError, 'not a leaf connected to sea'):
            naval.prune_impassable_harbours(source, {'x000001'})

    def test_hereroland_actual_port_and_sea_route_are_native_and_mutations_fail(self):
        relative = 'gfx/map/spline_network/spline_network.splnet'
        current = spline.parse((ROOT / relative).read_bytes())
        native = spline.parse((self.game / relative).read_bytes())
        self.assertTrue(naval.unchanged_native_spline_port(256, current, native))
        for anchor in (25603, 8414208):
            with self.subTest(anchor=anchor):
                missing = replace(current, points=tuple(p for p in current.points if p.key != anchor))
                self.assertFalse(naval.unchanged_native_spline_port(256, missing, native))
                moved = replace(current, points=tuple(repair.point(p.key, 0., 0.) if p.key == anchor else p
                                                       for p in current.points))
                self.assertFalse(naval.unchanged_native_spline_port(256, moved, native))
        disconnected = replace(current, links=tuple(link for link in current.links
                              if 8414208 not in repair.link_endpoints(link.key)))
        self.assertFalse(naval.unchanged_native_spline_port(256, disconnected, native))


if __name__ == '__main__':
    unittest.main()
