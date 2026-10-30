"""Names-only culture override: preserve Vanilla gameplay and authored identities."""
from pathlib import Path
import re
import unittest

from tools.check_override_inventory import extract_braced_object, find_object
from tools.validate import find_game_root

ROOT = Path(__file__).resolve().parents[1]
GAME = find_game_root(None)
POOLS = (
    "male_common_first_names", "female_common_first_names",
    "noble_last_names", "common_last_names",
)


def read(path):
    return path.read_text(encoding="utf-8-sig")


def pool(block, key):
    match = re.search(r"\b" + key + r"\s*=\s*\{", block)
    return extract_braced_object(block, match.start())


def names(block, key):
    return pool(block, key).split("{", 1)[1].rsplit("}", 1)[0].split()


class ZuluNamesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = find_object(read(ROOT / "common/cultures/sb_zulu_names.txt"), "zulu", directive="REPLACE")

    def test_non_name_fields_match_installed_vanilla(self):
        # A names replacement must not silently change culture gameplay or graphics.
        self.assertIsNotNone(GAME, "current-target Vanilla inputs are mandatory")
        vanilla = find_object(read(GAME / "common/cultures/00_cultures.txt"), "zulu")

        def gameplay(block):
            for key in POOLS:
                block = block.replace(pool(block, key), "")
            block = re.sub(r"#[^\n]*", "", block).removeprefix("REPLACE:")
            return re.sub(r"\s+", "", block)

        self.assertEqual(gameplay(self.mod), gameplay(vanilla))
        self.assertGreater(len(names(self.mod, POOLS[0])), len(names(vanilla, POOLS[0])))
        self.assertGreater(len(names(self.mod, POOLS[1])), len(names(vanilla, POOLS[1])))

    def test_generated_clans_do_not_assign_a_specific_father(self):
        for key in POOLS:
            values = names(self.mod, key)
            self.assertEqual(len(values), len(set(values)), key)
        for key in POOLS[2:]:
            values = names(self.mod, key)
            self.assertFalse(any(re.match(r"(?i)(ka|wa)[A-Z]", value) for value in values))
            self.assertNotIn("Buthelezei", values)
            self.assertIn("Buthelezi", values)
        # Clan membership alone does not decide whether a generated person is noble.
        self.assertEqual(names(self.mod, POOLS[2]), names(self.mod, POOLS[3]))

    def test_pool_and_new_royal_name_keys_have_localisation(self):
        self.assertIsNotNone(GAME)
        keys = set()
        for base in (ROOT / "localization/english", GAME / "localization/english"):
            for path in base.rglob("*.yml"):
                keys.update(re.findall(r"^\s*([^\s:#]+):\d*\s", read(path), re.M))
        wanted = {name for key in POOLS for name in names(self.mod, key)}
        wanted.update(("kaSenzangakhona", "kaMpande", "kaCetshwayo", "kaDinuzulu"))
        self.assertFalse(wanted - keys, wanted - keys)

    def test_royal_patronymics_preserve_template_identities(self):
        dynasty = read(ROOT / "common/character_templates/sb_zulu_dynasty_characters.txt")
        overrides = read(ROOT / "common/character_templates/sb_southern_africa_character_template_overrides.txt")
        expected = (
            (overrides, "ZUL_dingane", "REPLACE", "kaSenzangakhona"),
            (dynasty, "ZUL_mpande_zulu", "REPLACE", "kaSenzangakhona"),
            (dynasty, "ZUL_cetshwayo_heir", None, "kaMpande"),
            (dynasty, "ZUL_mbuyazi_heir", None, "kaMpande"),
            (dynasty, "ZUL_dinuzulu_heir", None, "kaCetshwayo"),
            (dynasty, "ZUL_solomon_heir", None, "kaDinuzulu"),
        )
        for text, key, directive, patronymic in expected:
            block = find_object(text, key, directive=directive)
            self.assertIn(f'last_name = "{patronymic}"', block, key)
            self.assertIn("historical = yes", block, key)
        # The two names describe one prince, not two birth identities.
        hamu = find_object(read(ROOT / "common/character_templates/sb_court_characters.txt"), "SB_ZUL_hamu")
        self.assertIn('last_name = "kaNzibe"', hamu)


if __name__ == "__main__":
    unittest.main()
