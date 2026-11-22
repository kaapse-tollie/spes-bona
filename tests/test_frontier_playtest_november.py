"""Contracts for the November frontier playtest. Native AI and country creation need DP replay."""
import re
import unittest
from pathlib import Path

from tests.test_zulu_institutions_laws import GAME, statements
from tests.test_not_grouping import atoms_in, evaluate
from tools.check_override_inventory import find_object

ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def body(path, key):
    return statements(find_object(source(path), key))


def fields(nodes, key):
    return [value for name, _, value in nodes if name == key]


class FrontierPlaytestTests(unittest.TestCase):
    def test_natal_names_beat_generic_colonial_label_even_after_independence(self):
        names = statements(find_object(source("common/dynamic_country_names/sb_dynamic_names.txt"),
                                       "NAL", directive="REPLACE"))
        entries = {fields(row, "name")[0]: row for row in fields(names, "dynamic_country_name")}
        natalia, colony = (entries[k] for k in ("dyn_c_sb_natalia", "dyn_c_sb_natal_colony"))
        self.assertEqual(fields(natalia, "trigger"), [[("always", "=", "yes")]])
        self.assertGreater(int(fields(natalia, "priority")[0]), 100)
        self.assertGreater(int(fields(colony, "priority")[0]), int(fields(natalia, "priority")[0]))
        self.assertIn(("is_subject_of", "=", "c:GBR"), fields(fields(colony, "trigger")[0], "scope:actor")[0])

    def test_refusal_closes_the_griqua_petition_without_executing_the_transfer(self):
        event = body("events/sb_griqualand_east_events.txt", "sb_griqualand_east.220")
        accept, decline = fields(event, "option")
        self.assertEqual(2, len(fields(accept, "custom_tooltip")))
        self.assertNotIn("sb_griqualand_east_create_march_state", [k for k, _, _ in accept])
        self.assertIn(("sb_griqualand_east_create_march_state", "=", "yes"), fields(accept, "hidden_effect")[0])
        refusal = fields(decline, "hidden_effect")[0]
        flags = {"sb_griqualand_east_pending_var"}
        for effect, _, flag in refusal:
            {"set_variable": flags.add, "remove_variable": flags.remove}[effect](flag)
        self.assertEqual({"sb_griqualand_east_resolved_var"}, flags)
        admission = find_object(source("common/scripted_triggers/sb_mineral_discoveries_triggers.txt"), "sb_cap_can_form_gle")
        self.assertRegex(admission, r"NOT\s*=\s*\{\s*has_variable = sb_griqualand_east_resolved_var")

    def test_griqua_foundation_and_transfers_include_cape_land_only_in_the_authored_footprint(self):
        effect = body("common/scripted_effects/sb_griqualand_west_effects.txt",
                      "sb_griqualand_east_create_march_state")
        creation = fields(effect, "if")[0]
        founders = [v for k, _, v in creation if k in ("if", "else_if")]
        gle = fields(effect, "c:GLE")[0]
        transfers = [v for v in fields(gle, "if") if fields(v, "s:STATE_EASTERN_CAPE")]
        footprint = {"x708ADB", "xC57FEF", "xCA8474", "x678D6E", "x7524D4"}

        def eligible(branch, owners):
            conditions = fields(branch, "limit")[0]
            atoms = {}
            for node in atoms_in(conditions):
                province = node[0].removeprefix("p:").removesuffix(".state.owner")
                self.assertIn(province, footprint)
                self.assertEqual((node[0], node[1]), (f"p:{province}.state.owner", "="))
                atoms[repr(node)] = owners[province] == node[2]
            return evaluate(conditions, atoms)

        seeds = [fields(fields(b, "create_country")[0], "province")[0] for b in founders]
        self.assertEqual(seeds, ["p:x708ADB", "p:xCA8474", "p:x678D6E", "p:x7524D4"])
        targets = []
        for branch in transfers:
            transfer = fields(fields(branch, "s:STATE_EASTERN_CAPE")[0], "set_owner_of_provinces")[0]
            self.assertEqual(fields(transfer, "country"), ["c:GLE"])
            provinces = fields(transfer, "provinces")[0]
            self.assertEqual(len(provinces), 1)
            targets.append(provinces[0][0])
        self.assertEqual(set(targets), footprint)
        self.assertEqual(len(targets), len(footprint))

        for owner in ("c:CAP", "c:XHO", "c:GBR", "c:ZUL", "c:GLE"):
            owners = dict.fromkeys(footprint, owner)
            for index, branch in enumerate(founders + transfers):
                with self.subTest(owner=owner, gate=index):
                    self.assertEqual(eligible(branch, owners), owner in ("c:CAP", "c:XHO"))

        # Select the first eligible seed, then apply the actual transfer guards.
        # Native state splitting, country setup and population movement need DP replay.
        owners = {"x708ADB": "c:GBR", "xC57FEF": "c:CAP", "xCA8474": "c:CAP",
                  "x678D6E": "c:XHO", "x7524D4": "c:ZUL", "outside": "c:CAP"}
        seed = next(fields(fields(b, "create_country")[0], "province")[0]
                    for b in founders if eligible(b, owners))
        self.assertEqual(seed, "p:xCA8474")
        owners[seed.removeprefix("p:")] = "c:GLE"
        for branch, target in zip(transfers, targets):
            if eligible(branch, owners):
                owners[target] = "c:GLE"
        self.assertEqual(owners, {"x708ADB": "c:GBR", "xC57FEF": "c:GLE", "xCA8474": "c:GLE",
                                  "x678D6E": "c:GLE", "x7524D4": "c:ZUL", "outside": "c:CAP"})

    def test_transfer_notice_goes_to_actual_recipient_after_transfer(self):
        decision = body("common/decisions/sb_bst_decisions.txt", "decision_sb_transfer_basutoland_to_cape")
        action = fields(decision, "when_taken")[0]
        self.assertEqual([key for key, _, _ in action], ["c:CAP", "c:BST"])
        self.assertEqual(fields(action[0][2], "transfer_subject"), ["c:BST"])
        notification = fields(action[1][2], "if")[-1]
        self.assertEqual(fields(notification, "limit")[0], [("is_direct_subject_of", "=", "c:CAP")])
        dispatch = fields(fields(notification, "c:CAP")[0], "trigger_event")[0]
        self.assertEqual(fields(dispatch, "id"), ["sb_bst_frontier.210"])
        event = body("events/sb_bst_frontier_events.txt", "sb_bst_frontier.210")
        self.assertEqual({k for k, _, _ in fields(event, "option")[0]}, {"name", "default_option"})

    def test_xhosa_resistance_is_installed_before_the_three_authored_plays(self):
        events = source("events/sb_frontier_ai_wars_events.txt")
        strategy = "ai_strategy_sb_xhosa_frontier_defence"
        for war in (7, 8, 9):
            self.assertRegex(events, r"set_variable = sb_xhosa_story_launch_lease_var\s+"
                             rf"if = \{{ limit = \{{ is_ai = yes \}} set_strategy = {strategy} \}}\s+"
                             rf"create_diplomatic_play = \{{ type = dp_sb_xhosa_war_{war}\b")
        bonus = fields(body("common/ai_strategies/sb_ai_strategies.txt", strategy), "diplomatic_play_boldness")[0]
        self.assertEqual(fields(bonus, "value"), ["0"])
        branch = fields(bonus, "if")[0]
        play = fields(fields(branch, "limit")[0], "scope:diplomatic_play")[0]
        self.assertEqual(fields(play, "initiator"), ["c:XHO"])
        self.assertEqual(set(fields(fields(play, "OR")[0], "is_diplomatic_play_type")),
                         {f"dp_sb_xhosa_war_{war}" for war in (7, 8, 9)})
        self.assertEqual(fields(branch, "add"), ["1000"])

    def test_settlement_effects_are_localised_as_native_sibling_bullets(self):
        files = ("events/sb_natal_interwar_events.txt", "localization/english/sb_natal_interwar_l_english.yml")
        event = body(files[0], "sb_natal_interwar.030")
        loc = source(files[1])
        for choice in fields(event, "option"):
            keys = fields(choice, "custom_tooltip")
            self.assertGreaterEqual(len(keys), 3)
            for key in keys:
                self.assertRegex(loc, rf'(?m)^\s*{re.escape(key)}:0 "[^•\n]+"$')
        self.assertNotIn("#indent_newline", "\n".join(line for line in loc.splitlines() if ".030." in line))

    def test_first_chief_is_named_before_the_laws_change_and_only_at_late_partition(self):
        path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        zul = fields(body(path, "sb_zululand_mark_and_exile_royal_house"), "c:ZUL")[0]
        appointment = next(node for node in zul if node[0] == "if" and fields(node[2], "random_scope_character"))
        first_law = next(node for node in zul if node[0] == "activate_law")
        self.assertLess(zul.index(appointment), zul.index(first_law))
        self.assertEqual(fields(appointment[2], "limit")[0], [("game_date", ">=", "1877.1.1")])
        actor = fields(appointment[2], "random_scope_character")[0]
        elig = fields(actor, "limit")[0]
        self.assertEqual(fields(elig, "has_template"), ["ZUL_zibhebhu_kamaphitha"])
        self.assertEqual(fields(elig, "sb_court_present_member"), ["yes"])
        selection = fields(fields(actor, "scope:sb_court_country")[0], "set_variable")[0]
        self.assertEqual(dict((k, v) for k, _, v in selection),
                         {"name": "sb_court_chiefly_head_scope", "value": "prev"})

    def test_mandlakazi_shelter_follows_the_actual_person_across_annexation(self):
        path = "common/scripted_effects/sb_zululand_settlement_effects.txt"
        shelter = fields(body(path, "sb_zululand_shelter_mandlakazi_chief"), "if")[0]
        actor = fields(shelter, "random_scope_character")[0]
        self.assertIn(("has_template", "=", "ZUL_zibhebhu_kamaphitha"), fields(actor, "limit")[0])
        ref = fields(actor, "set_global_variable")[0]
        self.assertEqual(fields(ref, "value"), ["this"])
        self.assertLess(next(i for i,n in enumerate(actor) if n[0] == "set_global_variable"),
                        next(i for i,n in enumerate(actor) if n[0] == "transfer_character"))
        ret = fields(body(path, "sb_zululand_return_mandlakazi_chief"), "if")[0]
        exact = fields(ret, "global_var:" + fields(ref, "name")[0])[0]
        restore = fields(exact, "if")[0]
        self.assertIn(("is_character_alive", "=", "yes"), fields(restore, "limit")[0])
        self.assertIn(("owner", "?=", "c:GBR"), fields(restore, "limit")[0])
        self.assertIn(("transfer_character", "=", "scope:sb_zululand_chief_home"), restore)
        self.assertEqual(ret[-1][0], "sb_zululand_clear_mandlakazi_shelter")
        frontend = find_object(source(path), "sb_zululand_restore_protectorate_for_natal")
        self.assertLess(frontend.index("create_country ="), frontend.index("sb_zululand_return_mandlakazi_chief"))
        rollback = find_object(source("common/scripted_effects/sb_natal_interwar_effects.txt"),
                               "sb_british_zulu_finalize_bound_annex")
        self.assertRegex(rollback, r"is_country_alive = yes \} \}\s+c:ZUL = \{ sb_zululand_return_mandlakazi_chief")

    def test_shelter_is_an_enforcement_hook_and_every_other_annex_property_matches_native(self):
        self.assertIsNotNone(GAME)
        self.assertFalse((ROOT.parent / "Community Mod Framework/common/war_goal_types/00_annex_country.txt").exists())
        native = find_object((GAME / "common/war_goal_types/00_annex_country.txt")
                             .read_text(encoding="utf-8-sig"), "annex_country")
        override = find_object(source("common/war_goal_types/zz_sb_zululand_annex_handoff.txt"),
                               "annex_country", directive="REPLACE")
        upstream, local = statements(native), statements(override)
        self.assertEqual([node for node in upstream if node[0] != "on_enforced"],
                         [node for node in local if node[0] != "on_enforced"])
        self.assertEqual(fields(upstream, "on_enforced"), [[]])
        condition = fields(fields(fields(local, "on_enforced")[0], "if")[0], "limit")[0]
        self.assertEqual(fields(condition, "country_definition"), ["cd:GBR"])
        self.assertIn(("var:sb_british_zulu_annex_play_scope", "?=", "scope:diplomatic_play"), condition)
        self.assertEqual(fields(condition, "scope:target_country")[0], [("country_definition", "=", "cd:ZUL")])
        self.assertNotIn("sb_zululand_shelter_mandlakazi_chief",
                         source("common/on_actions/sb_diplomatic_play_on_action_handlers.txt"))
