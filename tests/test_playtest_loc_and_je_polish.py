import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8-sig")


def object_block(rel: str, name: str) -> str:
    txt = read_text(rel)
    m = re.search(rf"^{re.escape(name)}\s*=\s*\{{", txt, re.M)
    assert m, f"Missing {name} in {rel}"
    depth = 0
    for i in range(m.start(), len(txt)):
        if txt[i] == "{":
            depth += 1
        elif txt[i] == "}":
            depth -= 1
            if depth == 0:
                return txt[m.start() : i + 1]
    raise AssertionError(f"Unclosed block {name} in {rel}")


class PlaytestLocAndJePolishTests(unittest.TestCase):
    def test_griqualand_west_overlord_scope_and_tooltips(self):
        helper = object_block(
            "common/scripted_effects/sb_griqualand_west_effects.txt",
            "sb_griqualand_west_save_country_loc_scopes",
        )
        self.assertIn("overlord = { save_scope_as = sb_gbr_scope }", helper)
        self.assertIn("c:GBR = { save_scope_as = sb_gbr_scope }", helper)

        loc = read_text("localization/english/sb_griqualand_west_l_english.yml")
        for key in (
            "sb_griqualand_west_242_war_tt",
            "sb_griqualand_west_252_boer_aggressor_tt",
            "sb_griqualand_west_253_boer_aggressor_tt",
            "sb_griqualand_west_254_cap_aggressor_tt",
            "sb_griqualand_west_254_boer_aggressor_tt",
        ):
            m = re.search(rf'^\s*{re.escape(key)}:0\s*"([^"]+)"', loc, re.M)
            self.assertIsNotNone(m, f"Missing {key}")
            val = m.group(1)
            self.assertIn("[SCOPE.sCountry('sb_gbr_scope').GetName]", val)
            self.assertNotIn("Britain", val)

    def test_imperial_confederation_terminal_cleanup_is_hidden(self):
        je = object_block(
            "common/journal_entries/1-09_sb_eastern_sphere.txt",
            "je_sb_imperial_confederation_scheme",
        )
        hidden_cleanups = re.findall(
            r"hidden_effect\s*=\s*\{\s*set_global_variable\s*=\s*sb_imperial_confederation_terminal_je_settled_var\s+sb_imperial_confederation_clear_runtime\s*=\s*yes\s*\}",
            je,
        )
        self.assertEqual(2, len(hidden_cleanups))

    def test_delagoa_je_hides_internal_variable_guards(self):
        je = object_block(
            "common/journal_entries/1-09_sb_eastern_sphere.txt",
            "je_sb_delagoa_route_to_sea",
        )
        self.assertIn("is_shown_when_inactive = {", je)
        m_possible = re.search(r"possible\s*=\s*\{(.*?)\n\t\}", je, re.S)
        self.assertIsNotNone(m_possible)
        possible = m_possible.group(1)
        self.assertIn("hidden_trigger = {", possible)
        # Strip brace-balanced hidden_trigger blocks and ensure no raw variable triggers remain in possible
        stripped = possible
        while True:
            m_ht = re.search(r"hidden_trigger\s*=\s*\{", stripped)
            if not m_ht:
                break
            depth = 0
            end = m_ht.start()
            for idx in range(m_ht.start(), len(stripped)):
                if stripped[idx] == "{":
                    depth += 1
                elif stripped[idx] == "}":
                    depth -= 1
                    if depth == 0:
                        end = idx + 1
                        break
            stripped = stripped[: m_ht.start()] + stripped[end:]
        self.assertNotIn("has_variable", stripped)
        self.assertNotIn("has_global_variable", stripped)

    def test_nrp_reduction_tooltips_do_not_spoil_transvaal_petition(self):
        loc = read_text("localization/english/sb_zululand_settlement_l_english.yml")
        for key in (
            "sb_zululand_settlement.210.a.tt",
            "sb_zululand_settlement.230.a.tt",
        ):
            m = re.search(rf'^\s*{re.escape(key)}:0\s*"([^"]+)"', loc, re.M)
            self.assertIsNotNone(m, f"Missing {key}")
            val = m.group(1)
            self.assertNotIn("Transvaal", val)
            self.assertNotIn("petition", val.lower())

    def test_sb_cape_030_uses_valid_overlord_scope_and_no_getcountry_in_loc(self):
        ev = object_block("events/sb_cape_events.txt", "sb_cape.030")
        self.assertIn("immediate = {", ev)
        self.assertIn("overlord = { save_scope_as = sb_gbr_scope }", ev)

        cape_loc = read_text("localization/english/sb_cape_l_english.yml")
        m = re.search(r'^\s*sb_cape\.030\.d:0\s*"([^"]+)"', cape_loc, re.M)
        self.assertIsNotNone(m)
        self.assertIn("[SCOPE.sCountry('sb_gbr_scope').GetName]", m.group(1))
        self.assertNotIn("GetCountry(", m.group(1))

        for path in sorted((ROOT / "localization/english").rglob("*.yml")):
            self.assertNotIn("GetCountry(", path.read_text(encoding="utf-8-sig"), f"Invalid GetCountry( in {path.name}")

    def test_namibia_mission_pulse_events_all_have_option_tooltips(self):
        je = object_block("common/journal_entries/1-08_sb_namibia.txt", "je_sb_map_namibian_coast")
        for status_key in (
            "je_sb_map_namibian_coast_status_active",
            "je_sb_map_namibian_coast_status_coves",
            "je_sb_map_namibian_coast_status_dunes",
            "je_sb_map_namibian_coast_status_corridor",
            "je_sb_map_namibian_coast_status_dangerous",
        ):
            self.assertIn(status_key, je)

        events_text = read_text("events/sb_namibia_events.txt")
        for retired in ("sb_nam.036", "sb_nam.037", "sb_nam.038"):
            self.assertNotIn(f"{retired} = {{", events_text)
            self.assertNotIn(retired, je)

        pulse_block = re.search(r"on_monthly_pulse\s*=\s*\{(.*?)\n\t\}", je, re.S)
        self.assertIsNotNone(pulse_block)
        dispatched = set(re.findall(r"=\s*(sb_nam\.\d+)", pulse_block.group(1)))
        self.assertEqual(dispatched, {f"sb_nam.{n:03d}" for n in range(30, 36)})

        loc = read_text("localization/english/sb_namibia_l_english.yml")
        loc_map = {
            m.group(1): m.group(2)
            for m in re.finditer(r'^\s*([A-Za-z0-9_.\-]+):\d*\s*"([^"]+)"', loc, re.M)
        }
        expected_flags = {
            30: ("sb_nam_act1_done_var", None),
            31: ("sb_nam_act2_done_var", "sb_nam_act1_done_var"),
            32: ("sb_nam_act3_done_var", "sb_nam_act2_done_var"),
            33: ("sb_nam_act4_done_var", "sb_nam_act3_done_var"),
            34: ("sb_nam_optional_event_done_var", "sb_nam_act1_done_var"),
            35: ("sb_nam_optional_event_done_var", "sb_nam_act2_done_var"),
        }
        for num, (done_flag, prev_flag) in expected_flags.items():
            eid = f"sb_nam.{num:03d}"
            ev = object_block("events/sb_namibia_events.txt", eid)
            # Default video window uses minor_left_icon (not left_icon)
            self.assertIn("minor_left_icon = scope:sb_nam_expedition_leader", ev)
            self.assertNotIn("\n\tleft_icon =", ev)
            self.assertIn("NOT = { exists = scope:sb_nam_expedition_leader }", ev)
            self.assertIn("NOT = { has_variable = sb_nam_survey_event_open_var }", ev)
            self.assertIn("set_variable = sb_nam_survey_event_open_var", ev)
            self.assertIn("remove_variable = sb_nam_survey_event_open_var", ev)
            self.assertIn("after = {", ev)
            self.assertIn(f"NOT = {{ has_variable = {done_flag} }}", ev)
            self.assertIn(f"set_variable = {done_flag}", ev)
            if prev_flag:
                self.assertIn(f"has_variable = {prev_flag}", ev)
            self.assertIn("sb_nam_pulse_cooldown_var", ev)

            opts = re.findall(r"\n\toption\s*=\s*\{(.*?)\n\t\}", ev, re.S)
            self.assertEqual(len(opts), 3, f"Expected 3 tradeoff options in {eid}")
            has_unconditional_default = any(
                "default_option = yes" in opt and "\n\t\ttrigger = {" not in opt
                for opt in opts
            )
            self.assertTrue(has_unconditional_default, f"{eid} needs an unconditional default_option")

            # Every option must declare at least one custom_tooltip
            for idx, opt in enumerate(opts):
                self.assertIn("custom_tooltip =", opt, f"{eid} option #{idx+1} missing custom_tooltip")

            # Bidirectional check: every hidden_effect in options must be immediately preceded by a matching custom_tooltip
            hidden_count = len(re.findall(r"\bhidden_effect\s*=\s*\{", ev))
            pairs = list(
                re.finditer(
                    r"custom_tooltip\s*=\s*([A-Za-z0-9_.\-]+)\s*hidden_effect\s*=\s*\{(.*?)\n\t+\}",
                    ev,
                    re.S,
                )
            )
            self.assertEqual(len(pairs), hidden_count, f"{eid}: unmatched custom_tooltip/hidden_effect pairs")
            for m_pair in pairs:
                tt_key, body = m_pair.group(1), m_pair.group(2)
                self.assertIn(tt_key, loc_map, f"Missing loc key {tt_key} for {eid}")
                tt_text = loc_map[tt_key]
                prog = re.search(
                    r"add_progress\s*=\s*\{\s*name\s*=\s*sb_namibian_coast_survey_progress_bar\s+value\s*=\s*(-?\d+)\s*\}",
                    body,
                )
                peril = re.search(
                    r"add_progress\s*=\s*\{\s*name\s*=\s*sb_namibian_coast_expedition_peril_bar\s+value\s*=\s*(-?\d+)\s*\}",
                    body,
                )
                if prog:
                    val = int(prog.group(1))
                    verb = "increases" if val > 0 else "decreases"
                    tag = "#p" if val > 0 else "#n"
                    self.assertIn(
                        f"#b Mission Progress#! {verb} by {tag} {abs(val)}#!",
                        tt_text,
                        f"{eid} {tt_key} progress mismatch: {tt_text}",
                    )
                else:
                    self.assertNotIn("Mission Progress", tt_text, f"{eid} {tt_key} promises Mission Progress without effect")
                if peril:
                    val = int(peril.group(1))
                    verb = "increases" if val > 0 else "decreases"
                    tag = "#n" if val > 0 else "#p"
                    self.assertIn(
                        f"#b Expedition Peril#! {verb} by {tag} {abs(val)}#!",
                        tt_text,
                        f"{eid} {tt_key} peril mismatch: {tt_text}",
                    )
                else:
                    self.assertNotIn("Expedition Peril", tt_text, f"{eid} {tt_key} promises Expedition Peril without effect")

        # Surveyor trait must be checked across the arc and only granted to generals; .031.c uses Prestige, not cash
        ev31 = object_block("events/sb_namibia_events.txt", "sb_nam.031")
        self.assertIn("has_role_of_type = general", ev31)
        self.assertIn("add_trait = surveyor", ev31)
        self.assertNotIn("add_treasury =", ev31)
        self.assertIn("sb_nam_survey_guano_prestige", ev31)
        self.assertIn("has_trait = surveyor", object_block("events/sb_namibia_events.txt", "sb_nam.030"))
        self.assertIn("has_trait = surveyor", object_block("events/sb_namibia_events.txt", "sb_nam.032"))
        self.assertIn("has_trait = surveyor", object_block("events/sb_namibia_events.txt", "sb_nam.033"))
        self.assertIn("has_trait = surveyor", object_block("events/sb_namibia_events.txt", "sb_nam.035"))

    def test_sb_nam_011_has_readable_trigger_and_bar_tooltips(self):
        ev = object_block("events/sb_namibia_events.txt", "sb_nam.011")
        self.assertIn("text = sb_nam_011_can_pay_tt", ev)
        loc = read_text("localization/english/sb_namibia_l_english.yml")
        loc_map = {
            m.group(1): m.group(2)
            for m in re.finditer(r'^\s*([A-Za-z0-9_.\-]+):\d*\s*"([^"]+)"', loc, re.M)
        }
        self.assertIn("£100,000", loc_map["sb_nam_011_can_pay_tt"])
        self.assertIn("[concept_gold_reserves]", loc_map["sb_nam_011_can_pay_tt"])
        self.assertIn("£100,000", loc_map["sb_nam_011_a_tt"])
        self.assertIn("#b Mission Progress#! increases by #p 10#!", loc_map["sb_nam_011_a_tt"])
        self.assertIn("#b Expedition Peril#! decreases by #p 2#!", loc_map["sb_nam_011_a_tt"])
        self.assertIn("No change", loc_map["sb_nam_011_b_tt"])

    def test_sb_nam_017_branches_immediate_vs_deferred_swa_tooltips(self):
        ev = object_block("events/sb_namibia_events.txt", "sb_nam.017")
        # Verify two-port predicate maps to immediate tooltip and else maps to deferred tooltip on all 4 options
        swa_branches = re.findall(
            r"if\s*=\s*\{\s*limit\s*=\s*\{\s*sb_nam_controls_both_consolidation_ports\s*=\s*yes\s*\}\s*custom_tooltip\s*=\s*sb_nam_017_swa_immediate_tt\s*\}\s*else\s*=\s*\{\s*custom_tooltip\s*=\s*sb_nam_017_swa_tt\s*\}",
            ev,
            re.S,
        )
        self.assertEqual(len(swa_branches), 4)
        self.assertRegex(
            ev,
            re.compile(
                r"if\s*=\s*\{\s*limit\s*=\s*\{\s*sb_nam_controls_both_consolidation_ports\s*=\s*yes\s*\}\s*custom_tooltip\s*=\s*sb_nam_017_company_immediate_tt\s*\}\s*else\s*=\s*\{\s*custom_tooltip\s*=\s*sb_nam_017_company_tt\s*\}",
                re.S,
            ),
        )
        self.assertRegex(
            ev,
            re.compile(
                r"if\s*=\s*\{\s*limit\s*=\s*\{\s*sb_nam_can_found_policy_colony\s*=\s*yes\s+sb_nam_controls_both_consolidation_ports\s*=\s*yes\s*\}\s*custom_tooltip\s*=\s*sb_nam_017_ruthless_immediate_tt\s*\}\s*else_if\s*=\s*\{\s*limit\s*=\s*\{\s*sb_nam_can_found_policy_colony\s*=\s*yes\s*\}\s*custom_tooltip\s*=\s*sb_nam_017_ruthless_tt\s*\}\s*else\s*=\s*\{\s*custom_tooltip\s*=\s*sb_nam_017_ruthless_direct_tt\s*\}",
                re.S,
            ),
        )
        loc = read_text("localization/english/sb_namibia_l_english.yml")
        loc_map = {
            m.group(1): m.group(2)
            for m in re.finditer(r'^\s*([A-Za-z0-9_.\-]+):\d*\s*"([^"]+)"', loc, re.M)
        }
        self.assertIn("Found #v South West Africa#! now", loc_map["sb_nam_017_swa_immediate_tt"])
        self.assertIn("immediately as a chartered subject and a company", loc_map["sb_nam_017_company_immediate_tt"])
        self.assertIn("as a chartered subject and a company", loc_map["sb_nam_017_company_tt"])
        self.assertNotIn("South West Africa", loc_map["sb_nam_017_ruthless_direct_tt"])
        self.assertNotIn("Standard of Living", loc_map["sb_nam_017_ruthless_direct_tt"])
        for key in (
            "sb_nam_017_swa_immediate_tt",
            "sb_nam_017_company_immediate_tt",
            "sb_nam_017_ruthless_immediate_tt",
        ):
            self.assertNotIn("Once we hold", loc_map[key])
            self.assertNotIn("Once South West Africa is founded", loc_map[key])


if __name__ == "__main__":
    unittest.main()
