"""Completed research across the British handover, including a delayed release."""
import json
import re
import unittest

from tests.test_not_grouping import atoms_in, definition, evaluate, field, walk
from tests.test_zulu_institutions_laws import CMF, GAME, ROOT


RESEARCH = "common/scripted_effects/sb_zululand_research_effects.txt"
SETTLEMENT = "common/scripted_effects/sb_zululand_settlement_effects.txt"
INTERWAR = "common/scripted_effects/sb_natal_interwar_effects.txt"
ARCHIVE = "sb_zululand_refresh_research_archive"
EACH = "sb_zululand_for_each_technology"
BASELINE = "sb_natal_apply_restored_zulu_baseline"
LAW_SOURCE = "sb_zululand_release_law_source"


class ZululandResearchTests(unittest.TestCase):
    def test_catalogue_round_trips_every_supported_technology(self):
        """Exercise the two script passes, including a lost country and a reloaded archive."""
        keys = [field(args, "TECH") for action, _, args in definition(RESEARCH, EACH)
                if action == "$ACTION$"]
        if GAME is None:
            supported = set(keys)
        else:
            supported = set()
            for root in (GAME, CMF, ROOT):
                for path in (root / "common/technology/technologies").glob("*.txt"):
                    supported.update(re.findall(r"^(?:(?:TRY_)?REPLACE:)?([\w-]+)\s*=\s*\{",
                                                path.read_text(encoding="utf-8-sig"), re.M))
        self.assertCountEqual(keys, supported)

        snapshot = field(definition(RESEARCH, ARCHIVE), "if")
        saved = {field(data, "name"): field(data, "value") for key, _, data in snapshot
                 if key == "set_global_variable"}
        self.assertEqual(saved, {"sb_zululand_archived_tech_country": "this",
                                 "sb_zululand_archived_tech_count": "techs_researched"})
        capture = field(definition(RESEARCH, field(field(snapshot, EACH), "ACTION")), "if")
        restore_branch = field(definition(INTERWAR, BASELINE), "if")
        restore = field(definition(RESEARCH, field(field(restore_branch, EACH), "ACTION")), "if")
        required = field(field(capture, "limit"), "has_technology_researched")
        write = field(capture, "add_to_global_variable_list")
        read = field(field(restore, "limit"), "is_target_in_global_variable_list")
        grant = field(restore, "add_technology_researched")
        self.assertEqual(field(field(restore_branch, "limit"), "has_global_variable_list"), field(write, "name"))
        for known in (set(), {"enclosure", "pan-nationalism", "sb_namibian_coastal_access"}, supported):
            with self.subTest(count=len(known)):
                archive = {field(write, "name"): [field(write, "target").replace("$TECH$", key)
                           for key in keys if required.replace("$TECH$", key) in known]}
                reloaded = json.loads(json.dumps(archive))
                rebuilt = {grant.replace("$TECH$", key) for key in keys
                           if field(read, "target").replace("$TECH$", key) in reloaded[field(read, "name")]}
                self.assertEqual(rebuilt, known)
        fallback = field(definition(INTERWAR, BASELINE), "else_if")
        self.assertEqual(field(field(field(fallback, "limit"), "NOT"), "has_global_variable"),
                         "sb_zululand_archived_tech_count")

    def test_snapshot_updates_on_discovery_or_a_different_main_zul(self):
        gate = field(field(definition(RESEARCH, ARCHIVE), "if"), "limit")
        def eligible(*, recorded=True, same_country=True, same_count=True,
                     main=True, alive=True, releasing=False, settled=False):
            values = {"this": main, "is_country_alive": alive, "c:GBR": settled,
                      "global_var:sb_zululand_archived_tech_country": same_country,
                      "techs_researched": same_count}
            flags = {LAW_SOURCE: releasing, "sb_zululand_archived_tech_count": recorded}
            return evaluate(gate, {repr(n): flags[n[2]] if n[0] == "has_global_variable" else values[n[0]]
                                   for n in atoms_in(gate)})
        self.assertTrue(eligible(recorded=False))
        self.assertTrue(eligible(same_count=False))
        self.assertTrue(eligible(same_country=False))
        self.assertFalse(eligible())
        for blocked in ({"main": False}, {"alive": False}, {"releasing": True}, {"settled": True}):
            self.assertFalse(eligible(same_count=False, **blocked))

    def test_capture_callers_supply_zul_even_when_britain_enforces(self):
        monthly = definition(SETTLEMENT, "sb_zululand_postwar_monthly_housekeeping")
        self.assertIn(("c:ZUL", "?=", [(ARCHIVE, "=", "yes")]), list(walk(monthly)))
        annex = definition("common/war_goal_types/zz_sb_zululand_annex_handoff.txt",
                           "annex_country", "REPLACE")
        self.assertIn(("scope:target_country", "=", [(ARCHIVE, "=", "yes")]),
                      list(walk(field(annex, "on_enforced"))))
        acquisition = definition("common/on_actions/sb_startup_on_action_handlers.txt",
                                 "sb_on_spes_bona_acquired_technology")
        self.assertIn((ARCHIVE, "=", "yes"), list(walk(acquisition)))

    def test_both_land_donors_supply_laws_and_neither_supplies_technology(self):
        release = definition(SETTLEMENT, "sb_zululand_restore_protectorate_for_natal")
        donors = [(key, body) for key, _, body in walk(release) if key.endswith(".state.owner")
                  and any(n[0] == "create_country" for n in body)]
        self.assertEqual({key for key, _ in donors}, {"p:xBE6FEE.state.owner",
                         "scope:sb_hamu_release_province.state.owner"})
        for _, body in donors:
            source = field(body, "set_global_variable")
            self.assertEqual((field(source, "name"), field(source, "value")), (LAW_SOURCE, "this"))
            self.assertLess([n[0] for n in body].index("set_global_variable"),
                            [n[0] for n in body].index("create_country"))
            creation = field(body, "create_country")
            self.assertNotIn("origin", [n[0] for n in creation])
            self.assertEqual(field(creation, "tag"), "ZUL")
            self.assertEqual(field(creation, "on_created"), [(BASELINE, "=", "yes")])
        baseline = definition(INTERWAR, BASELINE)
        self.assertEqual(field(baseline, "copy_laws"), "global_var:" + LAW_SOURCE)
        order = [n[0] for n in baseline]
        self.assertLess(order.index("if"), order.index("copy_laws"))
        self.assertLess(order.index("copy_laws"), order.index("effect_starting_politics_traditional"))
        self.assertIn(("remove_global_variable", "=", LAW_SOURCE), list(walk(release)))
        handoff = definition(SETTLEMENT, "sb_zululand_handoff_to_natal")
        alive = ("c:ZUL", "?=", [("is_country_alive", "=", "yes")])
        live = next(body for key, _, body in handoff if key == "if" and alive in field(body, "limit"))
        self.assertEqual(live[1:], [("sb_zululand_normalize_live_subject_for_natal", "=", "yes")])
        self.assertNotIn(BASELINE, [n[0] for n in walk(live)])
