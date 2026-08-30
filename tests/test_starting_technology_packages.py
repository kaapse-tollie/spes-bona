from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
COUNTRY_HISTORY = ROOT / "common/history/countries"


def history(tag: str) -> str:
    path = next(COUNTRY_HISTORY.glob(f"{tag.lower()} -*.txt"))
    return path.read_text(encoding="utf-8-sig")


def technology_package(tag: str) -> tuple[int, set[str]]:
    source = history(tag)
    tier_match = re.search(
        r"^\s*effect_starting_technology_tier_(\d+)_tech\s*=\s*yes\s*$",
        source,
        re.MULTILINE,
    )
    if tier_match is None:
        raise AssertionError(f"{tag} has no starting technology tier")
    additions = re.findall(
        r"^\s*add_technology_researched\s*=\s*([a-z0-9_]+)\s*$",
        source,
        re.MULTILINE,
    )
    if len(additions) != len(set(additions)):
        raise AssertionError(f"{tag} repeats a starting technology")
    return int(tier_match.group(1)), set(additions)


class StartingTechnologyPackageTests(unittest.TestCase):
    def test_eight_tag_approved_package_is_implemented_exactly(self):
        expected = {
            "CAP": (2, set()),
            "ORA": (
                6,
                {
                    "mandatory_service",
                    "military_drill",
                    "line_infantry",
                    "rationalism",
                    "tech_bureaucracy",
                    "democracy",
                    "romanticism",
                    "international_trade",
                    "navigation",
                    "international_relations",
                    "colonization",
                    "urban_planning",
                },
            ),
            "ZUL": (6, {"international_trade"}),
            "GZA": (6, {"international_trade"}),
            "SWZ": (6, {"international_trade"}),
            "BST": (6, {"international_trade", "rationalism"}),
            "PHL": (
                6,
                {"international_trade", "rationalism", "tech_bureaucracy"},
            ),
            "WBL": (
                6,
                {"international_trade", "rationalism", "tech_bureaucracy"},
            ),
        }
        self.assertEqual(expected, {tag: technology_package(tag) for tag in expected})

        preset_counts = {2: 44, 6: 3}
        total = sum(
            preset_counts[tier] + len(additions)
            for tier, additions in expected.values()
        )
        self.assertEqual(88, total)

    def test_swz_uses_the_traditional_mercantilist_baseline_not_isolationism(self):
        swz = history("SWZ")
        self.assertIn("effect_starting_politics_traditional = yes", swz)
        self.assertNotIn("activate_law = law_type:law_isolationism", swz)


if __name__ == "__main__":
    unittest.main()
