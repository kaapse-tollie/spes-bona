from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def object_block(path: str, name: str) -> str:
    source = text(path)
    match = re.search(rf"^(?:REPLACE:)?{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} in {path}")
    return validate.extract_braced(source, match.start())


class FrontierSettlerIdeologyTests(unittest.TestCase):
    def test_cap_and_boer_rural_folk_share_the_fixed_package(self):
        identities = "common/scripted_effects/sb_interest_group_identity_effects.txt"
        for effect_name, display_name in (
            ("sb_apply_cap_interest_group_identity", "ig_frontier_farmers"),
            ("sb_apply_boer_republic_interest_group_identity", "ig_klein_boere"),
        ):
            effect = object_block(identities, effect_name)
            self.assertIn(f"set_interest_group_name = {display_name}", effect)
            self.assertIn("add_ideology = ideology_sb_kleinboer_agrarianism", effect)
            self.assertIn("add_ideology = ideology_sb_settler_colonialist", effect)
            self.assertNotIn("remove_ideology = ideology_particularist", effect)

    def test_smallholder_agrarianism_owns_only_economy_land_and_tax(self):
        ideology = object_block(
            "common/ideologies/sb_ideologies.txt",
            "ideology_sb_kleinboer_agrarianism",
        )
        self.assertEqual(3, ideology.count("lawgroup_"))
        for token in (
            "law_agrarianism = strongly_approve",
            "law_cooperative_ownership = approve",
            "law_peasant_proprietorship = strongly_approve",
            "law_collectivized_agriculture = neutral",
            "law_consumption_based_taxation = approve",
        ):
            self.assertIn(token, ideology)
        self.assertNotIn("lawgroup_distribution_of_power", ideology)
        self.assertNotIn("lawgroup_slavery", ideology)

    def test_settler_colonialist_has_the_selected_hierarchy(self):
        ideology = object_block(
            "common/ideologies/sb_ideologies.txt",
            "ideology_sb_settler_colonialist",
        )
        for token in (
            "law_national_supremacy = strongly_approve",
            "law_ethnostate = approve",
            "law_racial_segregation = approve",
            "law_subjecthood = neutral",
            "law_cultural_exclusion = disapprove",
            "law_multicultural = strongly_disapprove",
            "law_sb_non_racialism = strongly_disapprove",
            "law_census_voting = strongly_approve",
            "law_landed_voting = approve",
            "law_wealth_voting = neutral",
            "law_universal_suffrage = disapprove",
            "law_single_party_state = disapprove",
            "law_oligarchy = strongly_disapprove",
            "law_autocracy = strongly_disapprove",
            "law_technocracy = strongly_disapprove",
            "law_discrete_inboekstelsel = strongly_approve",
            "law_slave_trade = neutral",
        ):
            self.assertIn(token, ideology)
        for token in (
            "law_anarchy",
            "law_legacy_slavery",
            "law_slavery_banned",
        ):
            self.assertNotIn(token, ideology)

    def test_colonial_racialism_accepts_settler_rural_folk_sponsors(self):
        amendment = object_block(
            "common/amendments/zz_sb_racialized_subjecthood_override.txt",
            "amendment_racialized_subjecthood",
        )
        for token in (
            "scope:approval > 0",
            "is_interest_group_type = ig_armed_forces",
            "is_interest_group_type = ig_industrialists",
            "is_interest_group_type = ig_rural_folk",
            "has_ideology = ideology:ideology_sb_settler_colonialist",
        ):
            self.assertIn(token, amendment)
        cape = text("common/history/countries/cap - cape colony.txt")
        self.assertIn("sponsor = PREV.ig:ig_armed_forces", cape)

    def test_display_names_distinguish_ig_and_separatist_movement(self):
        interest_groups = text("localization/english/sb_interest_groups_l_english.yml")
        general = text("localization/english/sb_l_english.yml")
        self.assertIn('ig_frontier_farmers:0 "Frontier Settlers"', interest_groups)
        self.assertIn('ideology_sb_settler_colonialist:0 "Settler Colonialist"', general)
        self.assertIn('ideology_sb_settler_separatist:0 "Settler Separatist"', general)


if __name__ == "__main__":
    unittest.main()
