from pathlib import Path
import hashlib
import json
import re
import struct
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]
NATAL_PROVINCES = {
    "x5B124F",
    "xFF0EF1",
    "x552449",
    "xE0EB02",
    "x85695F",
    "xDE0EDE",
    "x7ACC38",
    "xB1F868",
    "x3CED3D",
    "x11A090",
    "xCD31DB",
    "x279045",
    "xBBCA32",
}
NATAL_QWA_PROVINCES = NATAL_PROVINCES - {"x279045", "xBBCA32"}
ZULULAND_PROVINCES = {
    "xBE6FEE",
    "x1A084B",
    "xBFA16B",
    "x9E9742",
    "x88FAD4",
    "x904EBE",
    "x41C070",
    "xE882CE",
    "xE1E455",
}
EXPECTED_HUBS = {
    "STATE_NATAL": {
        "city": "x5B124F",
        "port": "x279045",
        "farm": "xE0EB02",
        "mine": "x552449",
        "wood": "x7ACC38",
    },
    "STATE_ZULULAND": {
        "city": "x41C070",
        "port": "x9E9742",
        "farm": "x88FAD4",
        "mine": "xE1E455",
        "wood": "xBE6FEE",
    },
}
SPLINE_PRE_SPLIT_SHA256 = "b96c927167595c0430c21ad471508d79585fa6a84a440c6230e8896193099715"
SPLINE_NATAL_REINDEX_SHA256 = "74cebc60ca7155f598f03924b725de0b3f0e060ca37af8dc356a4b120cb36274"
SPLINE_ANCHOR_ID_PATCHES = (
    (0x0097DE, 25703, 121303),
    (0x009800, 25704, 121304),
    (0x128E30, 25703, 121303),
    (0x1660F6, 25704, 121304),
    (0x167928, 25703, 121303),
    (0x16793A, 25704, 121304),
    (0x168146, 25704, 121304),
)


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def scoped_block(path: str, name: str) -> str:
    source = text(path)
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} in {path}")
    return validate.extract_braced(source, match.start())


def nested_blocks(source: str, name: str) -> list[str]:
    return [
        validate.extract_braced(source, match.start())
        for match in re.finditer(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    ]


def startup_owners(state_block: str) -> dict[str, set[str]]:
    owners = {}
    for block in nested_blocks(state_block, "create_state"):
        country = re.search(r"\bcountry\s*=\s*c:([A-Z0-9_]+)", block)
        if country is None:
            continue
        owners[country.group(1)] = {
            province.upper().replace("X", "x", 1)
            for province in validate.PROVINCE_RE.findall(block)
        }
    return owners


class NatalZululandStateSplitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state_path = ROOT / "map_data/state_regions/04_subsaharan_africa.txt"
        cls.states = validate.parse_state_blocks(cls.state_path)

    def test_state_ids_membership_hubs_traits_and_coastal_exit(self):
        natal = self.states["STATE_NATAL"]
        zululand = self.states["STATE_ZULULAND"]
        self.assertEqual(NATAL_PROVINCES, validate.object_values(natal, "provinces"))
        self.assertEqual(ZULULAND_PROVINCES, validate.object_values(zululand, "provinces"))
        self.assertTrue(NATAL_PROVINCES.isdisjoint(ZULULAND_PROVINCES))
        self.assertEqual(1213, int(validate.STATE_ID_RE.search(natal).group(1)))
        self.assertEqual(257, int(validate.STATE_ID_RE.search(zululand).group(1)))
        self.assertNotIn("state_trait_malaria", natal)
        self.assertIn('traits = { "state_trait_malaria" }', zululand)
        self.assertEqual(1, natal.count("naval_exit_id = 3106"))
        self.assertEqual(1, zululand.count("naval_exit_id = 3106"))

        ids = [
            int(validate.STATE_ID_RE.search(block).group(1))
            for block in self.states.values()
        ]
        self.assertEqual(len(ids), len(set(ids)))
        for state, expected in EXPECTED_HUBS.items():
            actual = {
                kind: province.upper().replace("X", "x", 1)
                for kind, province in validate.HUB_RE.findall(self.states[state])
            }
            self.assertEqual(expected, actual)
            self.assertTrue(set(actual.values()) <= validate.object_values(self.states[state], "provinces"))

    def test_connectivity_and_all_ten_hub_locators_are_contract_locked(self):
        manifest = json.loads(text("tools/map_connectivity_manifest.json"))
        samples = {
            (sample["state"], sample["kind"])
            for sample in manifest["locator_samples"]
        }
        for state, provinces in (
            ("STATE_NATAL", NATAL_PROVINCES),
            ("STATE_ZULULAND", ZULULAND_PROVINCES),
        ):
            contract = manifest["states"][state]
            self.assertEqual(provinces, set(contract["adjacency"]))
            self.assertEqual(
                1,
                len(validate.connected_components(provinces, contract["adjacency"])),
            )
            self.assertEqual([], contract["allowed_isolated_components"])
            for kind in EXPECTED_HUBS[state]:
                self.assertIn((state, kind), samples)

        for kind, path in manifest["locator_files"].items():
            instances, duplicates = validate.parse_locator_instances(ROOT / path)
            self.assertEqual([], duplicates)
            self.assertIn(257, instances, kind)
            self.assertIn(1213, instances, kind)

    def test_spline_anchor_reindex_changes_only_seven_logical_ids(self):
        spline = (
            ROOT / "gfx/map/spline_network/spline_network.splnet"
        ).read_bytes()
        self.assertEqual(SPLINE_NATAL_REINDEX_SHA256, hashlib.sha256(spline).hexdigest())

        reconstructed = bytearray(spline)
        for offset, old_id, new_id in SPLINE_ANCHOR_ID_PATCHES:
            self.assertEqual(struct.pack("<I", new_id), spline[offset : offset + 4])
            reconstructed[offset : offset + 4] = struct.pack("<I", old_id)

        changed_bytes = {
            index
            for index, (current, previous) in enumerate(zip(spline, reconstructed))
            if current != previous
        }
        self.assertEqual(
            {offset + byte for offset, _, _ in SPLINE_ANCHOR_ID_PATCHES for byte in range(3)},
            changed_bytes,
        )
        self.assertEqual(21, len(changed_bytes))
        self.assertEqual(
            SPLINE_PRE_SPLIT_SHA256,
            hashlib.sha256(reconstructed).hexdigest(),
        )

        for old_id in (25703, 25704):
            self.assertEqual(0, spline.count(b"\x14\x00" + struct.pack("<I", old_id)))
        self.assertEqual(3, spline.count(b"\x14\x00" + struct.pack("<I", 121303)))
        self.assertEqual(4, spline.count(b"\x14\x00" + struct.pack("<I", 121304)))

        expected_anchors = {
            121303: (4797.912109, 804.828796),
            121304: (4785.460938, 816.476562),
        }
        for anchor_id, expected_position in expected_anchors.items():
            marker = (
                b"\x14\x00"
                + struct.pack("<I", anchor_id)
                + b"\x4c\x00\x01\x00\x03\x00\x0d\x00"
            )
            start = spline.index(marker) + len(marker)
            position = (
                struct.unpack_from("<f", spline, start)[0],
                struct.unpack_from("<f", spline, start + 6)[0],
            )
            self.assertEqual(b"\x0d\x00", spline[start + 4 : start + 6])
            for actual, expected in zip(position, expected_position):
                self.assertAlmostEqual(expected, actual, places=5)

        strips = []
        strip_pattern = re.compile(
            rb"\xf7\x05\x01\x00\x03\x00((?:\x14\x00.{4})+?)"
            rb"\x04\x00\x04\x00\x03\x00\x0b\x00\x01\x00",
            re.DOTALL,
        )
        for match in strip_pattern.finditer(spline):
            values = match.group(1)
            ids = [
                struct.unpack_from("<I", values, offset + 2)[0]
                for offset in range(0, len(values), 6)
            ]
            if ids[0] in (121303, 121304) or ids[-1] in (121303, 121304):
                strips.append((ids[0], ids[-1], len(ids)))
        self.assertEqual(4282, len(list(strip_pattern.finditer(spline))))
        self.assertCountEqual(
            [
                (121303, 26003, 16),
                (121304, 25804, 12),
                (121303, 121304, 4),
                (25700, 121304, 9),
            ],
            strips,
        )

    def test_fresh_1836_ownership_population_and_building_history(self):
        states_path = "common/history/states/00_states.txt"
        natal = scoped_block(states_path, "s:STATE_NATAL")
        zululand = scoped_block(states_path, "s:STATE_ZULULAND")
        self.assertEqual(
            {
                "NGI": NATAL_QWA_PROVINCES,
                "CAP": {"x279045"},
                "ZUL": {"xBBCA32"},
            },
            startup_owners(natal),
        )
        self.assertEqual({"ZUL": ZULULAND_PROVINCES}, startup_owners(zululand))
        for block in (natal, zululand):
            self.assertIn("add_homeland = cu:zulu", block)
            self.assertIn("add_claim = c:ZUL", block)

        pop_path = "common/history/pops/04_subsaharan_africa.txt"
        natal_pops = scoped_block(pop_path, "s:STATE_NATAL")
        zulu_pops = scoped_block(pop_path, "s:STATE_ZULULAND")
        natal_zul_pops = scoped_block_from_source(natal_pops, "region_state:ZUL")
        self.assertEqual(
            ["2000"], re.findall(r"\bsize\s*=\s*(\d+)", natal_zul_pops)
        )
        self.assertIn("culture = zulu", natal_zul_pops)
        self.assertNotIn("pop_type = slaves", natal_zul_pops)
        self.assertEqual(
            ["84945"],
            re.findall(
                r"\bsize\s*=\s*(\d+)",
                scoped_block_from_source(natal_pops, "region_state:NGI"),
            ),
        )
        self.assertEqual(
            ["55"],
            re.findall(
                r"\bsize\s*=\s*(\d+)",
                scoped_block_from_source(natal_pops, "region_state:CAP"),
            ),
        )
        self.assertEqual(
            ["266000", "2000"], re.findall(r"\bsize\s*=\s*(\d+)", zulu_pops)
        )
        self.assertEqual(
            270000,
            sum(
                int(size)
                for size in re.findall(
                    r"\bsize\s*=\s*(\d+)", natal_zul_pops + zulu_pops
                )
            ),
        )

        buildings_path = "common/history/buildings/04_subsaharan_africa.txt"
        natal_buildings = scoped_block(buildings_path, "s:STATE_NATAL")
        zulu_buildings = scoped_block(buildings_path, "s:STATE_ZULULAND")
        self.assertIn("region_state:NGI", natal_buildings)
        self.assertIn("region_state:CAP", natal_buildings)
        self.assertNotIn("region_state:ZUL", natal_buildings)
        self.assertIn('region="STATE_NATAL"', natal_buildings)
        self.assertIn("region_state:ZUL", zulu_buildings)
        self.assertNotIn("region_state:NGI", zulu_buildings)
        self.assertNotIn("region_state:CAP", zulu_buildings)
        self.assertEqual(1, zulu_buildings.count('building="building_logging_camp"'))
        self.assertEqual(1, zulu_buildings.count('building="building_livestock_ranch"'))

    def test_traits_capitals_regions_formation_and_localization(self):
        traits = text("common/history/global/sb_state_traits.txt")
        sugar = re.search(
            r"s:STATE_NATAL\s*=\s*\{[^}]*state_trait_sb_natal_sugar_country[^}]*\}",
            traits,
            re.DOTALL,
        )
        self.assertIsNotNone(sugar)
        self.assertIsNone(
            re.search(
                r"s:STATE_ZULULAND\s*=\s*\{[^}]*state_trait_sb_natal_sugar_country",
                traits,
                re.DOTALL,
            )
        )

        countries = text("common/country_definitions/sb_countries.txt") + text(
            "common/country_definitions/zz_sb_southern_africa_country_definition_overrides.txt"
        )
        for country in ("NGI", "KLR", "REPLACE:NAL"):
            self.assertIn("capital = STATE_NATAL", scoped_block_from_source(countries, country))
        for country in ("NGN", "REPLACE:ZUL"):
            self.assertIn("capital = STATE_ZULULAND", scoped_block_from_source(countries, country))

        characters = text("common/character_templates/sb_cape_and_colonial_characters.txt")
        for character in ("NAL_martin_west", "KLR_andries_theodorus_spies"):
            self.assertIn(
                "home_region = STATE_NATAL",
                scoped_block_from_source(characters, character),
            )

        for path in (
            "common/strategic_regions/sb_african_strategic_regions.txt",
            "common/geographic_regions/sb_geographic_regions.txt",
            "common/country_formation/sb_formable_countries.txt",
        ):
            source = text(path)
            self.assertIn("STATE_NATAL", source)
            self.assertIn("STATE_ZULULAND", source)

        base_states = text("localization/english/replace/sb_states_l_english.yml")
        base_hubs = text("localization/english/replace/sb_hub_names_l_english.yml")
        dynamic = text("localization/english/replace/dynamic_state_and_hub_names_l_english.yml")
        self.assertIn('STATE_NATAL:0 "Natal"', base_states)
        self.assertIn('STATE_NATAL_boer:0 "Natalia"', dynamic)
        self.assertIn('STATE_NATAL_british:0 "Natal"', dynamic)
        self.assertIn('STATE_ZULULAND_zulu:0 "KwaZulu"', dynamic)
        self.assertIn('STATE_ZULULAND_boer:0 "Zululand"', dynamic)
        self.assertIn('STATE_ZULULAND_british:0 "Zululand"', dynamic)
        for state in EXPECTED_HUBS:
            for kind in EXPECTED_HUBS[state]:
                self.assertIn(f"HUB_NAME_{state}_{kind}", base_hubs + dynamic)

        names_path = "common/scripted_effects/zz_sb_dynamic_state_names_southern_africa.txt"
        dispatch = scoped_block(names_path, "REPLACE:assign_state_name_region_southern_africa")
        natal_names = scoped_block(names_path, "STATE_NATAL_state_name_assign")
        zululand_names = scoped_block(names_path, "REPLACE:STATE_ZULULAND_state_name_assign")
        self.assertIn("STATE_NATAL_state_name_assign = yes", dispatch)
        self.assertIn("STATE_ZULULAND_state_name_assign = yes", dispatch)
        for key in ("STATE_NATAL_zulu", "STATE_NATAL_boer", "STATE_NATAL_british"):
            self.assertIn(key, natal_names)
        for key in (
            "STATE_ZULULAND_zulu",
            "STATE_ZULULAND_boer",
            "STATE_ZULULAND_british",
        ):
            self.assertIn(key, zululand_names)


def scoped_block_from_source(source: str, name: str) -> str:
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name}")
    return validate.extract_braced(source, match.start())


if __name__ == "__main__":
    unittest.main()
