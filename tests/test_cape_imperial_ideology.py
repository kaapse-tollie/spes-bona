from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def object_block(path: str, name: str) -> str:
    source = text(path)
    match = re.search(rf"^{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} in {path}")
    return validate.extract_braced(source, match.start())


class CapeImperialIdeologyTests(unittest.TestCase):
    def test_cap_and_british_natal_receive_the_imperial_law_package(self):
        cape = text("common/history/countries/cap - cape colony.txt")
        for token in (
            "activate_law = law_type:law_subjecthood",
            "type = amendment_racialized_subjecthood",
            "sponsor = PREV.ig:ig_armed_forces",
            "activate_law = law_type:law_sb_imperial_administration",
        ):
            self.assertIn(token, cape)

        natal = object_block(
            "common/scripted_effects/sb_natalia_colony_effects.txt",
            "sb_apply_british_natal_colony_setup",
        )
        for token in (
            "activate_law = law_type:law_subjecthood",
            "type = amendment_racialized_subjecthood",
            "activate_law = law_type:law_extraction_economy",
            "activate_law = law_type:law_sb_imperial_administration",
            "sb_apply_british_natal_interest_group_identity = yes",
        ):
            self.assertIn(token, natal)
        self.assertNotIn(
            "law_sb_imperial_administration",
            text("common/scripted_effects/sb_natalia_effects.txt"),
        )

    def test_imperial_administration_has_the_requested_effects_and_gate(self):
        law = object_block(
            "common/laws/04_sb_imperial_administration.txt",
            "law_sb_imperial_administration",
        )
        for token in (
            "parent = law_hereditary_bureaucrats",
            'icon = "gfx/interface/icons/law_icons/crownland_diets.dds"',
            "state_bureaucracy_population_base_cost_factor_mult = -0.25",
            "country_aristocrats_pol_str_mult = 0.10",
            "country_sb_aristocrats_armed_forces_attraction_add = 50",
            "country_definition = cd:CAP",
            "country_definition = cd:NAL",
            "sb_natalia_british_colony_resolved_var",
            "sb_is_outside_british_imperial_network = yes",
        ):
            self.assertIn(token, law)

        armed_forces = text("common/interest_groups/zz_sb_armed_forces_override.txt")
        self.assertIn("REPLACE:ig_armed_forces", armed_forces)
        self.assertIn(
            "add = owner.modifier:country_sb_aristocrats_armed_forces_attraction_add",
            armed_forces,
        )
        modifier_type = text(
            "common/modifier_type_definitions/sb_interest_group_modifier_types.txt"
        )
        self.assertIn(
            "country_sb_aristocrats_armed_forces_attraction_add = {",
            modifier_type,
        )
        self.assertIn("script_only = yes", modifier_type)
        self.assertIn(
            'country_sb_aristocrats_armed_forces_attraction_add:0 "$aristocrats$ Attraction to the $ig_armed_forces$"',
            text("localization/english/sb_l_english.yml"),
        )
        self.assertIn(
            "country_sb_aristocrats_armed_forces_attraction_add_desc:0",
            text("localization/english/sb_l_english.yml"),
        )
        self.assertIn(
            "a9bf6cdad3a02a13a0e3edacb9c23cf87cb8695065b6a97a859ba0a730f3ce47",
            armed_forces,
        )

    def test_cap_and_natal_replace_only_jingoist(self):
        identities = text("common/scripted_effects/sb_interest_group_identity_effects.txt")
        for name in (
            "sb_apply_cap_interest_group_identity",
            "sb_apply_british_natal_interest_group_identity",
        ):
            effect = object_block(
                "common/scripted_effects/sb_interest_group_identity_effects.txt",
                name,
            )
            self.assertIn("remove_ideology = ideology_jingoist", effect)
            self.assertIn("add_ideology = ideology_sb_imperialist", effect)
            self.assertIn("add_ideology = ideology_patriotic", effect)
            self.assertIn("add_ideology = ideology_loyalist", effect)
        self.assertIn("set_interest_group_name = ig_sb_imperial_establishment", identities)
        self.assertIn("set_interest_group_name = ig_sb_colonial_garrison", identities)

    def test_imperialist_stances_are_bounded_to_five_law_groups(self):
        for name in ("ideology_sb_imperialist", "ideology_sb_imperialist_leader"):
            ideology = object_block("common/ideologies/sb_ideologies.txt", name)
            self.assertEqual(5, ideology.count("lawgroup_"))
            for token in (
                'icon = "gfx/interface/icons/ideology_icons/royalist.dds"'
                if name == "ideology_sb_imperialist"
                else 'icon = "gfx/interface/icons/ideology_icons/ideology_leader/ideology_leader_royalist.dds"',
                "law_colonial_administration = strongly_approve",
                "law_subjecthood = strongly_approve",
                "law_hereditary_bureaucrats = strongly_approve",
                "law_colonial_exploitation = strongly_approve",
                "law_professional_army = strongly_approve",
                "law_elected_bureaucrats = strongly_disapprove",
                "law_multicultural = strongly_disapprove",
                "law_sb_non_racialism = strongly_disapprove",
            ):
                self.assertIn(token, ideology)
            self.assertNotIn("law_sb_imperial_administration =", ideology)

        leader = object_block(
            "common/ideologies/sb_ideologies.txt", "ideology_sb_imperialist_leader"
        )
        self.assertIn("interest_group_leader_weight = { value = 0 }", leader)
        self.assertIn("non_interest_group_leader_weight = { value = 0 }", leader)

    def test_citizenship_drift_uses_the_new_exclusive_values(self):
        bar = object_block(
            "common/scripted_progress_bars/sb_progress_bars.txt",
            "sb_cape_balance_bar",
        )
        expected = {
            "sb_cape_full_cqf_law": "0.20",
            "sb_cape_restricted_cqf_law": "0.15",
            "sb_cape_cultural_exclusion_law": "0.10",
            "sb_cape_multicultural_law": "0.50",
            "sb_cape_ethnostate_law": "0.50",
            "sb_cape_national_supremacy_law": "0.20",
            "sb_cape_racial_segregation_law": "0.10",
            "sb_cape_cultural_exclusion_enacting": "0.05",
            "sb_cape_multicultural_enacting": "0.25",
            "sb_cape_ethnostate_enacting": "0.25",
            "sb_cape_national_supremacy_enacting": "0.10",
            "sb_cape_racial_segregation_enacting": "0.05",
        }
        for desc, value in expected.items():
            self.assertRegex(
                bar,
                rf'desc = "{re.escape(desc)}"\s+value = {re.escape(value)}',
            )
            self.assertEqual(1, bar.count(f'desc = "{desc}"'))

    def test_rhodes_changes_ideology_only_after_bsac_appointment(self):
        rhodes = object_block(
            "common/character_templates/sb_southern_africa_character_template_overrides.txt",
            "REPLACE:SAF_cecil_rhodes",
        )
        self.assertIn("ideology = ideology_sb_imperialist_leader", rhodes)

        appointment = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_rhodesian_venture_set_rhodes_colonialist_if_installed",
        )
        self.assertIn("executive = scope:sb_rhodes_appointment_scope", appointment)
        self.assertIn("set_ideology = ideology:ideology_sb_colonialist_leader", appointment)

        installer = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_rhodesian_venture_install_bsac_executive",
        )
        self.assertEqual(
            2,
            installer.count(
                "sb_rhodesian_venture_set_rhodes_colonialist_if_installed = yes"
            ),
        )


if __name__ == "__main__":
    unittest.main()
