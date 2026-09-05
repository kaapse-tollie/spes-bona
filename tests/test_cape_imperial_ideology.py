from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def object_block(path: str, name: str) -> str:
    source = text(path)
    return object_block_from_source(source, name, path)


def object_block_from_source(source: str, name: str, context: str = "source") -> str:
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE)
    if match is None:
        raise AssertionError(f"missing {name} in {context}")
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
            "country_liberty_desire_add = -0.10",
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
            "c010ec05625f29a1e2691e49b1b30a2900cfce46553d8a9c2c7f248a1ae3e119",
            armed_forces,
        )

    def test_cap_natal_and_bsa_colonial_forces_receive_colonialist(self):
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
            self.assertIn("add_ideology = ideology_colonialist", effect)
            self.assertIn("add_ideology = ideology_patriotic", effect)
            self.assertIn("add_ideology = ideology_loyalist", effect)
        self.assertIn("set_interest_group_name = ig_sb_imperial_establishment", identities)
        self.assertIn("set_interest_group_name = ig_sb_colonial_garrison", identities)

        bsa = object_block(
            "common/scripted_effects/sb_rhodesian_venture_effects.txt",
            "sb_rhodesian_venture_apply_chartered_company_package",
        )
        self.assertIn("sb_apply_british_natal_interest_group_identity = yes", bsa)

    def test_anglo_imperialist_stances_include_abolitionism(self):
        for name in ("ideology_sb_imperialist", "ideology_sb_imperialist_leader"):
            ideology = object_block("common/ideologies/sb_ideologies.txt", name)
            self.assertEqual(6, ideology.count("lawgroup_"))
            for token in (
                'icon = "gfx/interface/icons/ideology_icons/royalist.dds"'
                if name == "ideology_sb_imperialist"
                else 'icon = "gfx/interface/icons/ideology_icons/ideology_leader/ideology_leader_royalist.dds"',
                "law_monarchy = strongly_approve",
                "law_subjecthood = strongly_approve",
                "law_hereditary_bureaucrats = strongly_approve",
                "law_professional_army = strongly_approve",
                "law_elected_bureaucrats = strongly_disapprove",
                "law_multicultural = strongly_disapprove",
            ):
                self.assertIn(token, ideology)
            self.assertNotIn("law_sb_non_racialism =", ideology)
            self.assertNotIn("law_sb_imperial_administration =", ideology)
            self.assertNotIn("law_colonial_administration =", ideology)
            self.assertNotIn("lawgroup_colonization", ideology)

            distribution = object_block_from_source(
                ideology, "lawgroup_distribution_of_power"
            )
            expected = {
                "law_autocracy": "strongly_approve",
                "law_oligarchy": "approve",
                "law_landed_voting": "neutral",
                "law_technocracy": "neutral",
                "law_wealth_voting": "disapprove",
                "law_census_voting": "disapprove",
                "law_universal_suffrage": "strongly_disapprove",
                "law_anarchy": "strongly_disapprove",
                "law_single_party_state": "strongly_disapprove",
            }
            self.assertEqual(
                expected,
                dict(
                    re.findall(
                        r"^\s*(law_[a-z0-9_]+)\s*=\s*([a-z_]+)",
                        distribution,
                        re.MULTILINE,
                    )
                ),
            )

            slavery = object_block_from_source(ideology, "lawgroup_slavery")
            self.assertEqual(
                {
                    "law_slavery_banned": "strongly_approve",
                    "law_legacy_slavery": "disapprove",
                    "law_colonial_slavery": "disapprove",
                    "law_debt_slavery": "strongly_disapprove",
                    "law_slave_trade": "strongly_disapprove",
                },
                dict(
                    re.findall(
                        r"^\s*(law_[a-z0-9_]+)\s*=\s*([a-z_]+)",
                        slavery,
                        re.MULTILINE,
                    )
                ),
            )

        ideology_sources = "\n".join(
            path.read_text(encoding="utf-8-sig")
            for path in (ROOT / "common/ideologies").glob("*.txt")
        )
        self.assertNotIn("law_colonial_administration =", ideology_sources)

        leader = object_block(
            "common/ideologies/sb_ideologies.txt", "ideology_sb_imperialist_leader"
        )
        self.assertIn("interest_group_leader_weight = { value = 0 }", leader)
        self.assertIn("non_interest_group_leader_weight = { value = 0 }", leader)

        localization = text("localization/english/sb_interest_groups_l_english.yml")
        self.assertIn('ideology_sb_imperialist:0 "Anglo-Imperialism"', localization)

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

    def test_cape_movement_ideologies_cover_bureaucracy_and_internal_security(self):
        ideologies = {
            "ideology_sb_settler_separatist": {
                "lawgroup_bureaucracy": {
                    "law_hereditary_bureaucrats": "approve",
                    "law_appointed_bureaucrats": "neutral",
                    "law_elected_bureaucrats": "disapprove",
                },
                "lawgroup_internal_security": {
                    "law_no_home_affairs": "neutral",
                    "law_secret_police": "strongly_approve",
                    "law_national_guard": "approve",
                    "law_guaranteed_liberties": "disapprove",
                },
            },
            "ideology_sb_cape_liberal": {
                "lawgroup_bureaucracy": {
                    "law_hereditary_bureaucrats": "strongly_disapprove",
                    "law_appointed_bureaucrats": "neutral",
                    "law_elected_bureaucrats": "strongly_approve",
                },
                "lawgroup_internal_security": {
                    "law_no_home_affairs": "disapprove",
                    "law_secret_police": "strongly_disapprove",
                    "law_national_guard": "approve",
                    "law_guaranteed_liberties": "strongly_approve",
                },
            },
        }
        for ideology_name, expected_groups in ideologies.items():
            ideology = object_block("common/ideologies/sb_ideologies.txt", ideology_name)
            for group_name, expected in expected_groups.items():
                group = object_block_from_source(ideology, group_name)
                self.assertEqual(
                    expected,
                    dict(
                        re.findall(
                            r"^\s*(law_[a-z0-9_]+)\s*=\s*([a-z_]+)",
                            group,
                            re.MULTILINE,
                        )
                    ),
                )

    def test_cape_balance_tracks_bureaucracy_and_internal_security_laws(self):
        bar = object_block(
            "common/scripted_progress_bars/sb_progress_bars.txt",
            "sb_cape_balance_bar",
        )
        expected = {
            "sb_cape_imperial_administration_law": "0.1",
            "sb_cape_elected_bureaucrats_law": "0.1",
            "sb_cape_secret_police_law": "0.2",
            "sb_cape_guaranteed_liberties_law": "0.2",
        }
        for desc, value in expected.items():
            self.assertRegex(
                bar,
                rf'desc = "{re.escape(desc)}"\s+value = {re.escape(value)}',
            )
            self.assertEqual(1, bar.count(f'desc = "{desc}"'))
        for neutral_law in (
            "law_appointed_bureaucrats",
            "law_no_home_affairs",
            "law_national_guard",
        ):
            self.assertNotIn(neutral_law, bar)

    def test_xhosa_frontier_no_longer_drives_cape_settler_balance(self):
        bar = object_block(
            "common/scripted_progress_bars/sb_progress_bars.txt",
            "sb_cape_balance_bar",
        )
        localization = text("localization/english/sb_l_english.yml")

        self.assertNotIn("state_trait_sb_xhosa_resistance", bar)
        self.assertNotIn("sb_cape_xhosa_frontier_pressure", bar)
        self.assertNotIn("sb_cape_xhosa_frontier_pressure:0", localization)

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
