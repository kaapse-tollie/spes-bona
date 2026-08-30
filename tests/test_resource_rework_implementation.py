from collections import defaultdict
from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "map_data/state_regions/04_subsaharan_africa.txt"
GATE_PATH = ROOT / "common/scripted_effects/sb_resource_technology_gates_effects.txt"
ON_ACTION_PATH = ROOT / "common/on_actions/sb_mineral_discoveries_on_actions.txt"
KIMBERLEY_PATH = ROOT / "common/scripted_effects/sb_griqualand_west_effects.txt"
MESSAGE_PATH = ROOT / "common/messages/sb_resource_gate_messages.txt"
GUIDE_PATH = ROOT / "Docs/resource_update_guide.md"
DESIGN_PATH = ROOT / "Docs/resource_gameplay_overrides.md"
SUMMARY_PATH = ROOT / "Docs/resource_balance_summary.md"

ARABLE = "arable_land"
WOOD = "building_logging_camp"
COAL = "building_coal_mine"
FISH = "building_fishing_wharf"
IRON = "building_iron_mine"
LEAD = "building_lead_mine"
SULFUR = "building_sulfur_mine"
WHALE = "building_whaling_station"
GOLD = "building_gold_field"
DIAMOND = "building_diamond_mine"
RUBBER = "building_rubber_plantation"
OIL = "building_oil_rig"

RESOURCE_ORDER = (
    ARABLE, WOOD, COAL, FISH, IRON, LEAD, SULFUR, WHALE,
    GOLD, DIAMOND, RUBBER, OIL,
)

EXPECTED_CONFIGURED = {
    "STATE_CAPE_COLONY": {ARABLE: 33, WOOD: 4, FISH: 12, WHALE: 4},
    "STATE_NORTHERN_CAPE": {ARABLE: 6, WOOD: 1, FISH: 2, LEAD: 8, DIAMOND: 4},
    "STATE_GRIQUALAND_WEST": {ARABLE: 4, IRON: 20, DIAMOND: 20},
    "STATE_BECHUANALAND": {ARABLE: 4, GOLD: 2},
    "STATE_EASTERN_CAPE": {ARABLE: 28, WOOD: 6, COAL: 2, FISH: 2, WHALE: 2},
    "STATE_TRANSVAAL": {ARABLE: 26, WOOD: 1, COAL: 5, IRON: 2, GOLD: 75, DIAMOND: 20},
    "STATE_EAST_TRANSVAAL": {ARABLE: 35, WOOD: 6, COAL: 104, IRON: 6, GOLD: 4},
    "STATE_NORTHERN_TRANSVAAL": {ARABLE: 24, WOOD: 2, COAL: 9, IRON: 6, GOLD: 1, DIAMOND: 6},
    "STATE_VRYSTAAT": {ARABLE: 56, WOOD: 8, COAL: 5, IRON: 1, GOLD: 4, DIAMOND: 5},
    "STATE_NATAL": {ARABLE: 24, WOOD: 4, COAL: 2, FISH: 1, IRON: 2, WHALE: 4},
    "STATE_ZULULAND": {ARABLE: 12, WOOD: 4, COAL: 4, FISH: 1},
    "STATE_DRAKENSBERG": {ARABLE: 8, WOOD: 1, COAL: 1, DIAMOND: 6},
    "STATE_BOTSWANA": {ARABLE: 8, WOOD: 5, COAL: 10, GOLD: 1, DIAMOND: 30},
    "STATE_LOURENCO_MARQUES": {ARABLE: 32, WOOD: 10, FISH: 2, WHALE: 4, RUBBER: 16, OIL: 6},
    "STATE_ZAMBEZI": {ARABLE: 60, WOOD: 11, COAL: 7, IRON: 9, SULFUR: 1, GOLD: 5, DIAMOND: 10, RUBBER: 16},
    "STATE_HEREROLAND": {ARABLE: 18, WOOD: 2, FISH: 6, LEAD: 10},
    "STATE_NAMAQUALAND": {ARABLE: 5, FISH: 7, LEAD: 2, WHALE: 3, DIAMOND: 14},
}

EXPECTED_TOTALS = {
    ARABLE: 383,
    WOOD: 65,
    COAL: 149,
    FISH: 33,
    IRON: 46,
    LEAD: 20,
    SULFUR: 1,
    WHALE: 17,
    GOLD: 92,
    DIAMOND: 115,
    RUBBER: 32,
    OIL: 6,
}

DOCUMENTED_RESOURCE_NAMES = {
    ARABLE: "Arable",
    WOOD: "Wood",
    COAL: "Coal",
    FISH: "Fishing",
    IRON: "Iron",
    LEAD: "Lead",
    SULFUR: "Sulfur",
    WHALE: "Whaling",
    GOLD: "Gold potential",
    DIAMOND: "Diamonds",
    RUBBER: "Rubber",
    OIL: "Oil potential",
}


def nested_blocks(source: str, name: str) -> list[str]:
    return [
        validate.extract_braced(source, match.start())
        for match in re.finditer(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    ]


def object_block(source: str, name: str) -> str:
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name}")
    return validate.extract_braced(source, match.start())


def static_resources(state_block: str) -> dict[str, int]:
    result = {ARABLE: int(re.search(r"^\s*arable_land\s*=\s*(\d+)", state_block, re.MULTILINE).group(1))}
    capped_match = re.search(r"^\s*capped_resources\s*=\s*\{", state_block, re.MULTILINE)
    if capped_match:
        capped = validate.extract_braced(state_block, capped_match.start())
        for resource, value in re.findall(
            r"^\s*(building_[A-Za-z0-9_]+)\s*=\s*(\d+)", capped, re.MULTILINE
        ):
            result[resource] = int(value)
    for block in nested_blocks(state_block, "resource"):
        resource = re.search(r"\btype\s*=\s*\"?(building_[A-Za-z0-9_]+)\"?", block).group(1)
        amounts = re.findall(r"\b(?:undiscovered_amount|discovered_amount)\s*=\s*(\d+)", block)
        result[resource] = result.get(resource, 0) + sum(map(int, amounts))
    return result


class ResourceReworkImplementationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.states = validate.parse_state_blocks(STATE_PATH)
        cls.gates = GATE_PATH.read_text(encoding="utf-8-sig")
        cls.on_actions = ON_ACTION_PATH.read_text(encoding="utf-8-sig")
        cls.messages = MESSAGE_PATH.read_text(encoding="utf-8-sig")

    def configured_resources(self) -> dict[str, dict[str, int]]:
        configured = {
            state: defaultdict(int, static_resources(self.states[state]))
            for state in EXPECTED_CONFIGURED
        }
        effect = object_block(self.gates, "sb_apply_resource_technology_gates")
        stages = nested_blocks(effect, "if")
        self.assertEqual(23, len(stages))
        for stage in stages:
            state = re.search(r"s:(STATE_[A-Z0-9_]+)", stage).group(1)
            resource = re.search(r"\btype\s*=\s*(building_[A-Za-z0-9_]+)", stage).group(1)
            amount = int(re.search(r"\bamount\s*=\s*(\d+)", stage).group(1))
            if re.search(rf"\badd_resource_potential\s*=\s*{re.escape(resource)}\b", stage):
                amount += 1
            configured[state][resource] += amount

        # The established Kimberley event creates one mine and adds 19 remaining levels.
        kimberley = KIMBERLEY_PATH.read_text(encoding="utf-8-sig")
        self.assertIn("level = 1", object_block(kimberley, "sb_kimberley_create_initial_diamond_mine"))
        remaining = object_block(kimberley, "sb_kimberley_seed_remaining_potential")
        self.assertIn("amount = 18", remaining)
        self.assertIn("amount = 19", remaining)
        configured["STATE_GRIQUALAND_WEST"][DIAMOND] += 20
        return configured

    def test_state_caps_match_the_approved_gameplay_design(self):
        configured = self.configured_resources()
        for state, expected_nonzero in EXPECTED_CONFIGURED.items():
            expected = {resource: expected_nonzero.get(resource, 0) for resource in RESOURCE_ORDER}
            actual = {resource: configured[state].get(resource, 0) for resource in RESOURCE_ORDER}
            self.assertEqual(expected, actual, state)

    def test_configured_totals_match_the_approved_scenario(self):
        configured = self.configured_resources()
        actual = {
            resource: sum(state.get(resource, 0) for state in configured.values())
            for resource in RESOURCE_ORDER
        }
        self.assertEqual(EXPECTED_TOTALS, actual)

    def test_gate_lifecycle_and_notification_contract(self):
        for hook in (
            "sb_on_mineral_discoveries_game_started",
            "sb_on_mineral_discoveries_acquired_technology",
            "sb_on_mineral_discoveries_state_owner_change",
        ):
            self.assertIn("sb_apply_resource_technology_gates = yes", object_block(self.on_actions, hook))

        effect = object_block(self.gates, "sb_apply_resource_technology_gates")
        stages = nested_blocks(effect, "if")
        self.assertEqual(23, len(re.findall(r"\bset_global_variable\s*=", effect)))
        self.assertEqual(23, len(set(re.findall(r"\bset_global_variable\s*=\s*([A-Za-z0-9_]+)", effect))))
        self.assertNotIn("force_resource_discovery", effect)

        discoverable = []
        direct = []
        for stage in stages:
            resource = re.search(r"\btype\s*=\s*(building_[A-Za-z0-9_]+)", stage).group(1)
            (discoverable if resource in {GOLD, OIL} else direct).append(stage)
        self.assertEqual(8, len(discoverable))
        self.assertEqual(15, len(direct))
        self.assertTrue(all("post_notification" not in stage for stage in discoverable))
        self.assertTrue(all("post_notification" in stage for stage in direct))

        posted = set(re.findall(r"\bpost_notification\s*=\s*(sb_resource_[A-Za-z0-9_]+)", effect))
        registered = set(re.findall(r"^(sb_resource_[A-Za-z0-9_]+)\s*=\s*\{", self.messages, re.MULTILINE))
        self.assertEqual(posted, registered)
        for message in registered:
            block = object_block(self.messages, message)
            self.assertRegex(block, r"\btype\s*=\s*country\b")
            self.assertRegex(block, r'\bgroup\s*=\s*"resource_discovery_notification_group"')
            self.assertRegex(block, r"\bnotification_type\s*=\s*toast\b")
            self.assertRegex(block, r"\bcolor\s*=\s*good\b")
            self.assertRegex(block, r'\btexture\s*=\s*"gfx/interface/icons/notification_icons/resource\.dds"')

    def test_crop_slot_design_changes_only_the_two_approved_grains(self):
        griqualand = self.states["STATE_GRIQUALAND_WEST"]
        bechuanaland = self.states["STATE_BECHUANALAND"]
        self.assertIn('"building_maize_farm"', griqualand)
        self.assertNotIn('"building_wheat_farm"', griqualand)
        self.assertIn('"building_maize_farm"', bechuanaland)
        self.assertNotIn('"building_millet_farm"', bechuanaland)
        for state, retained in (
            ("STATE_NATAL", "building_coffee_plantation"),
            ("STATE_ZULULAND", "building_cotton_plantation"),
            ("STATE_LOURENCO_MARQUES", "building_cotton_plantation"),
        ):
            self.assertIn(f'"{retained}"', self.states[state])

    def test_live_documentation_matches_the_executable_totals(self):
        guide = GUIDE_PATH.read_text(encoding="utf-8-sig").lower()
        summary = SUMMARY_PATH.read_text(encoding="utf-8-sig").lower()
        design = DESIGN_PATH.read_text(encoding="utf-8-sig")
        for resource, value in EXPECTED_TOTALS.items():
            label = DOCUMENTED_RESOURCE_NAMES[resource]
            label_pattern = r"\s+".join(map(re.escape, label.lower().split()))
            prose_pattern = rf"\b{value}\s+{label_pattern}\b"
            self.assertRegex(guide, prose_pattern)
            self.assertRegex(summary, prose_pattern)
            self.assertRegex(
                design,
                rf"(?m)^\| {re.escape(label)} \|.*\| \*\*{value}\*\* \|",
            )
        self.assertIn("## Active playtesting checks", design)
        self.assertIn("Drakensberg `8`", design)
        self.assertIn("Namaqualand `5`", design)


if __name__ == "__main__":
    unittest.main()
