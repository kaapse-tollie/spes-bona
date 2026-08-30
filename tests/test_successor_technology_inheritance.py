from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def object_block(path: str, name: str) -> str:
    source = text(path)
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} in {path}")
    return validate.extract_braced(source, match.start())


def creation_blocks(source: str, tag: str) -> list[str]:
    blocks = [
        validate.extract_braced(source, match.start())
        for match in re.finditer(r"^\s*create_country\s*=\s*\{", source, re.MULTILINE)
    ]
    return [block for block in blocks if f"tag = {tag}" in block]


def assert_no_technology_grants(test: unittest.TestCase, source: str) -> None:
    test.assertNotRegex(source, r"effect_starting_technology_tier_\d+_tech\s*=\s*yes")
    test.assertNotRegex(source, r"add_technology_researched\s*=")


class SuccessorTechnologyInheritanceTests(unittest.TestCase):
    def test_natalia_transvaal_zoutpansberg_and_klip_river_inherit_oranje(self):
        natalia_path = "common/scripted_effects/sb_natalia_effects.txt"
        for effect_name in (
            "sb_create_natalia_republic_if_missing",
            "sb_create_natalia_frontier_republic_if_missing",
        ):
            blocks = creation_blocks(object_block(natalia_path, effect_name), "NAL")
            self.assertEqual(1, len(blocks))
            self.assertIn("origin = c:ORA", blocks[0])

        trek_path = "common/scripted_effects/sb_trek_migration.txt"
        transvaal = object_block(trek_path, "sb_spawn_transvaal_republic_v2")
        trn_blocks = creation_blocks(transvaal, "TRN")
        self.assertEqual(6, len(trn_blocks))
        self.assertTrue(all("origin = c:ORA" in block for block in trn_blocks))

        zoutpansberg = creation_blocks(
            object_block(trek_path, "sb_found_zoutpansberg_republic"), "ZPB"
        )
        self.assertEqual(1, len(zoutpansberg))
        self.assertIn("origin = c:ORA", zoutpansberg[0])

        klip_river = object_block(
            "common/scripted_effects/sb_klip_river_county_effects.txt",
            "sb_klip_river_create_county",
        )
        klr_blocks = creation_blocks(klip_river, "KLR")
        self.assertEqual(1, len(klr_blocks))
        self.assertIn("origin = c:ORA", klr_blocks[0])

        for source in (
            object_block(natalia_path, "sb_apply_natalia_boer_republic_setup"),
            transvaal,
            klip_river,
            text("common/history/countries/zpb - zoutpansberg.txt"),
        ):
            assert_no_technology_grants(self, source)

    def test_lydenburg_inherits_transvaal_without_a_technology_floor(self):
        lydenburg = object_block(
            "common/scripted_effects/sb_trek_migration.txt",
            "sb_found_lydenburg_republic",
        )
        blocks = creation_blocks(lydenburg, "LYD")
        self.assertEqual(1, len(blocks))
        self.assertIn("origin = c:TRN", blocks[0])
        assert_no_technology_grants(
            self, text("common/history/countries/lyd - lydenburg.txt")
        )

    def test_stellaland_goshen_inherits_each_actual_creator(self):
        saved_creator = object_block(
            "common/scripted_effects/sb_griqualand_west_effects.txt",
            "sb_stellaland_goshen_create_from_boer_colony",
        )
        saved_blocks = creation_blocks(saved_creator, "SGO")
        self.assertEqual(1, len(saved_blocks))
        self.assertIn("origin = scope:sb_stellaland_goshen_creator", saved_blocks[0])

        active_creator = object_block(
            "common/scripted_effects/sb_bechuanaland_corridor_effects.txt",
            "sb_bechuanaland_create_sgo_beachhead_for_root",
        )
        active_blocks = creation_blocks(active_creator, "SGO")
        self.assertEqual(4, len(active_blocks))
        self.assertTrue(all("origin = root" in block for block in active_blocks))

        assert_no_technology_grants(
            self,
            object_block(
                "common/scripted_effects/sb_bechuanaland_corridor_effects.txt",
                "sb_bechuanaland_setup_sgo_frontier_republic",
            ),
        )

    def test_direct_british_natal_inherits_cape_without_a_technology_floor(self):
        natalia_path = "common/scripted_effects/sb_natalia_effects.txt"
        creation = object_block(
            natalia_path, "sb_create_british_natal_colony_if_missing"
        )
        blocks = creation_blocks(creation, "NAL")
        self.assertEqual(1, len(blocks))
        self.assertIn("origin = c:CAP", blocks[0])
        assert_no_technology_grants(
            self, object_block(natalia_path, "sb_seed_british_natal_colony_shell")
        )
        assert_no_technology_grants(
            self,
            object_block(
                "common/scripted_effects/sb_natalia_colony_effects.txt",
                "sb_apply_british_natal_colony_setup",
            ),
        )


if __name__ == "__main__":
    unittest.main()
