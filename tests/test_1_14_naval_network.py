from pathlib import Path
import re
import tempfile
import unittest

from tools import check_naval_network as naval


ROOT = Path(__file__).resolve().parents[1]
STATE_REGION_ROOT = ROOT / "map_data/state_regions"
LOURENCO_MARQUES = "STATE_LOURENCO_MARQUES"
EXPECTED_PORT_COUNT = 33


class NavalNetworkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game_root = naval.find_game_root(None)
        cls.state_paths = sorted(STATE_REGION_ROOT.glob("*.txt"))
        cls.ports = naval.parse_state_ports(cls.state_paths)

    def test_main_validator_invokes_the_naval_checker_after_game_root_resolution(self):
        validator = (ROOT / "tools/validate.py").read_text(encoding="utf-8")
        game_root_index = validator.index("game_root = find_game_root(args.game_root)")
        checker_index = validator.index('"tools/check_naval_network.py"')
        self.assertGreater(checker_index, game_root_index)
        self.assertIn('"naval network connectivity"', validator[game_root_index:checker_index])

    def test_mod_network_is_exactly_the_derived_impassable_coast_correction(self):
        native = (self.game_root / naval.NETWORK_PATH).read_text(encoding="utf-8-sig")
        expected = naval.prune_impassable_harbours(native, naval.impassable_provinces(self.state_paths))
        self.assertEqual(expected.encode("utf-8-sig"), (ROOT / naval.NETWORK_PATH).read_bytes())

    def test_lourenco_marques_retains_its_authored_building_port_and_locator(self):
        ports = {port.state: port.province for port in self.ports}
        self.assertEqual(EXPECTED_PORT_COUNT, len(ports))
        self.assertEqual("x54CDC5", ports[LOURENCO_MARQUES])
        self.assertNotIn("x361897", ports.values())

        state_source = (
            ROOT / "map_data/state_regions/04_subsaharan_africa.txt"
        ).read_text(encoding="utf-8-sig")
        state_match = re.search(
            rf"(?m)^{LOURENCO_MARQUES}\s*=\s*\{{", state_source
        )
        self.assertIsNotNone(state_match)
        opening = state_source.find("{", state_match.start(), state_match.end())
        closing = naval.matching_brace(state_source, opening)
        state = state_source[opening : closing + 1]
        self.assertIn('port = "x54CDC5"', state)
        self.assertIn('prime_land = { "x54CDC5" }', state)
        self.assertIn('"x54CDC5"', state)
        self.assertIn('"x361897"', state)  # Still a valid province; only the port moves.
        self.assertIn("id = 264", state)

        locator = (
            ROOT / "gfx/map/map_object_data/generated_map_object_locators_port.txt"
        ).read_text(encoding="utf-8-sig")
        locator_match = re.search(
            r"\{\s*id=264\s+position=\{\s*([-0-9.]+)\s+[-0-9.]+\s+([-0-9.]+)",
            locator,
        )
        self.assertIsNotNone(locator_match)
        self.assertAlmostEqual(4838.494629, float(locator_match.group(1)), places=5)
        self.assertAlmostEqual(907.506287, float(locator_match.group(2)), places=5)

    def test_current_network_against_sb_and_unmodified_native_control(self):
        self.assertIsNotNone(self.game_root, "1.15 validation requires installed game")
        network_path = self.game_root / "common/travel_network/naval_network.txt"
        self.assertEqual(naval.EXPECTED_1_15_SHA256, naval.sha256(network_path))
        network = naval.parse_naval_network(network_path)
        self.assertEqual(naval.EXPECTED_1_15_NODE_COUNT, len(network.nodes))
        self.assertEqual(naval.EXPECTED_1_15_CONNECTION_COUNT, len(network.connections))
        native_ports = naval.parse_state_ports([
            self.game_root / "map_data/state_regions" / path.name
            for path in self.state_paths
        ])
        native = {port.state: port for port in native_ports}
        effective = naval.parse_naval_network(ROOT / naval.NETWORK_PATH)
        errors = naval.validate_state_ports(effective, self.ports)
        native_errors = naval.validate_state_ports(network, native_ports)
        # Hereroland's generic coastal nodes are all impassable in SB. Its
        # actual building port comes from the unchanged native spline instead.
        self.assertEqual(naval.NATIVE_ACCESS_PENDING | {'STATE_HEREROLAND'},
                         {error.split()[0] for error in errors})
        self.assertEqual(tuple(e for e in errors if not e.startswith('STATE_HEREROLAND ')), native_errors)
        self.assertEqual(30, len(self.ports) - len(errors))
        self.assertEqual(29, len(native_ports) - len(native_errors))
        for port in self.ports:
            if port.state in naval.NATIVE_ACCESS_PENDING:
                self.assertEqual(native[port.state].province, port.province)
                self.assertEqual(set(native[port.state].provinces), set(port.provinces))
        lourenco = next(port for port in self.ports if port.state == LOURENCO_MARQUES)
        self.assertIn(lourenco.province, lourenco.provinces)
        self.assertEqual((), naval.validate_state_ports(effective, (lourenco,)))

    def test_validator_rejects_missing_non_harbor_and_disconnected_ports(self):
        network = naval.parse_naval_network_text(
            """
            nodes = {
                { province=x000001 x=10 y=20 type=harbor }
                { province=x000002 x=11 y=21 type=sea }
                { province=x000003 x=12 y=22 type=harbor_from_spline }
            }
            connections = { { from=0 to=1 } }
            """
        )
        ports = (
            naval.StatePort("STATE_CONNECTED", "x000001", Path("fixture.txt")),
            naval.StatePort("STATE_NON_HARBOR", "x000002", Path("fixture.txt")),
            naval.StatePort("STATE_DISCONNECTED", "x000003", Path("fixture.txt")),
            naval.StatePort("STATE_MISSING", "x000004", Path("fixture.txt")),
        )
        self.assertEqual(
            (
                "STATE_NON_HARBOR port x000002 has no harbor node (types: sea)",
                "STATE_DISCONNECTED port x000003 harbor has no route to a sea node",
                "STATE_MISSING port x000004 has no naval node",
            ),
            naval.validate_state_ports(network, ports),
        )

    def test_state_membership_and_isolated_harbor_chain_are_rejected(self):
        network = naval.parse_naval_network_text("""
            nodes = {
                { province=x000001 x=0 y=0 type=harbor }
                { province=x000002 x=1 y=1 type=harbor }
                { province=x000003 x=2 y=2 type=sea }
            }
            connections = { { from=0 to=1 } }
        """)
        ports = (
            naval.StatePort("STATE_INVALID", "x000004", Path("fixture"), ("x000001",)),
            naval.StatePort("STATE_ISOLATED", "x000001", Path("fixture"), ("x000001",)),
        )
        self.assertEqual((
            "STATE_INVALID port x000004 is outside its state region",
            "STATE_ISOLATED port x000001 harbor has no route to a sea node",
        ), naval.validate_state_ports(network, ports))

    def test_state_parser_uses_only_direct_port_assignments(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "states.txt"
            path.write_text(
                """
STATE_FIXTURE = {
    id = 9999
    provinces = { "x000001" }
    port = "x000001"
    resource = {
        port = "x000002"
    }
}
                """,
                encoding="utf-8",
            )
            self.assertEqual(
                (naval.StatePort("STATE_FIXTURE", "x000001", path, ("x000001",), 9999),),
                naval.parse_state_ports([path]),
            )

    def test_parser_rejects_an_out_of_range_connection(self):
        with self.assertRaisesRegex(naval.NavalNetworkError, "endpoint outside"):
            naval.parse_naval_network_text(
                """
                nodes = { { province=x000001 x=10 y=20 type=harbor } }
                connections = { { from=0 to=1 } }
                """
            )


if __name__ == "__main__":
    unittest.main()
