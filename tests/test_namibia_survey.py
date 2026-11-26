"""Execute the Namibia survey scripts against representative campaign and legacy-save states."""
from copy import deepcopy
from math import ceil
import unittest
from unittest.mock import patch

from tests.test_klip_river_refugees import RefugeeRuntime
from tests.test_warren_swa_policy import NAMIBIA_EVENTS, NAMIBIA_POLICIES, NAMIBIA_TRIGGERS, object_block
from tests.test_zulu_court_politics import EFFECTS, TRIGGERS, VALUES, definitions
from tests.test_zulu_institutions_laws import statements

SURVEY = "je_sb_map_namibian_coast"
OFFER = "sb_nam_maps_offer_var"
LEGACY_OFFER = "sb_nam_german_missionary_support_offered_var"
RESOLVED = "sb_nam_colonial_prestige_resolved_var"
BACKED = "sb_nam_colonial_programme_backed_var"
POLICY = "sb_nam_selected_policy_var"
EXPIRY = "sb_nam_policy_expiry_var"
CAPACITY = "sb_nam_administrative_capacity"
FOUNDER = "sb_nam_policy_founder_var"
PAYMENTS = "sb_nam_company_payments_left_var"
PULSE = definitions("common/on_actions/sb_namibia_on_actions.txt")["sb_on_namibia_monthly_pulse_country"]
EVENTS = {name: statements(object_block(NAMIBIA_EVENTS, name)) for name in ("sb_nam.011", "sb_nam.017", "sb_nam.018")}
POLICIES = definitions(NAMIBIA_POLICIES)
SURVEY_TRIGGERS = definitions(NAMIBIA_TRIGGERS)
SURVEY_VALUES = definitions("common/script_values/sb_namibia_policy_values.txt")
RULES = definitions("common/scripted_triggers/sb_game_rule_triggers.txt")
AI_MACRO = object_block("common/scripted_modifiers/sb_namibia_policy_ai.txt", "sb_nam_survey_policy_weight")


def fields(nodes):
    return {key: value for key, _, value in nodes}


def options(event):
    return [fields(value) for key, _, value in EVENTS[event] if key == "option"]


def branch_containing(nodes, token):
    return next(n for n in nodes if n[0] == "if" and token in str(n[2]))


DISPATCH = branch_containing(fields(PULSE)["effect"], "sb_nam.011")
SWA_MONTHLY = branch_containing(fields(PULSE)["effect"], "sb_nam_apply_administrative_capacity")
REPAIR = branch_containing(SWA_MONTHLY[2], "sb_nam_apply_administrative_capacity")


class SurveyRuntime(RefugeeRuntime):
    """Reuse the SB arithmetic and headcount fixture. Supply the native survey-specific fields."""
    def __init__(self):
        super().__init__(set())
        self.de = {"id": "GER", "vars": {}, "alive": True, "is_ai": True, "is_subject": False,
                   "is_country_type": "recognized", "country_rank": "rank_value:great_power",
                   "laws": {"law_type:law_colonial_resettlement"},
                   "journal_entries": {SURVEY: {"vars": {}}}, "gold_reserves": 0,
                   "credit": 1000000, "principal": 0, "primary": {"north_german", "south_german"},
                   "capital": {"pops": [], "region": "sr:region_north_germany"}, "igs": [], "ruler": None}
        self.swa = {"id": "SWA", "vars": {FOUNDER: self.de}, "alive": True, "modifiers": {},
                    "is_subject": False, "institution:institution_colonial_affairs": {"investment_max": 4}}
        self.countries.update(GER=self.de, SWA=self.swa)
        self.states = {name: {"id": name, "vars": {}} for name in ("HEREROLAND", "NAMAQUALAND")}
        self.ports = {"p:xB04050.state.owner": self.swa, "p:xDEAA3C.state.owner": self.de}
        self.scopes["sb_nam_policy_founder"] = self.de
        self.day = 0
        self.rule = "dynamic_historical"

    def ref(self, key, scope, prev=None):
        if key in ("THIS", "PREV"):
            return super().ref(key.lower(), scope, prev)
        if key in self.ports:
            return self.ports[key]
        if key == "game_date":
            return self.day
        if key == "long_modifier_time":
            return 3650
        if key.startswith("s:STATE_") and key.endswith(".region_state:SWA"):
            return self.states[key[8:].split(".")[0]]
        if key.startswith("je:"):
            return scope["journal_entries"].get(key[3:])
        if key.startswith("cd:"):
            return key[3:]
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        for key, op, value in nodes:
            if key in ("is_ai", "is_in_government", "is_subject"):
                passed = scope[key] == (value == "yes")
            elif key == "has_game_rule":
                passed = value == "sb_frontier_ai_behavior_" + self.rule
            elif key in ("is_country_type", "country_rank", "region"):
                passed = scope[key] == value
            elif key == "is_pop_type":
                passed = scope["type"] == value
            elif key == "is_primary_culture_of":
                passed = scope in self.ref(value, scope, prev)["primary"]
            elif key == "country_definition":
                passed = scope["id"] == self.ref(value, scope, prev)
            elif op == "<=" and isinstance(value, list):
                passed = self.ref(key, scope, prev) <= self.calc(value, scope, prev)
            else:
                passed = super().condition([(key, op, value)], scope, prev)
            if not passed:
                return False
        return True

    def calc(self, nodes, scope, prev=None):
        expanded = []
        for key, op, value in self.branches(nodes, scope, prev):
            if key == "every_interest_group":
                limit = fields(value)["limit"]
                body = [n for n in value if n[0] != "limit"]
                amount = sum(self.calc(body, ig, scope) for ig in scope["igs"] if self.condition(limit, ig, scope))
                expanded.append(("add", "=", str(amount)))
            elif key == "ceiling":
                expanded = [("value", "=", str(ceil(super().calc(expanded, scope, prev))))]
            else:
                expanded.append((key, op, value))
        return super().calc(expanded, scope, prev)

    def effect(self, nodes, scope, prev=None):
        for key, op, value in self.branches(nodes, scope, prev):
            if key.startswith(("s:STATE_", "je:")):
                self.effect(value, self.ref(key, scope, prev), scope)
            elif key == "change_variable" and "subtract" in fields(value):
                f = fields(value)
                scope["vars"][f["name"]] -= self.ref(f["subtract"], scope, prev)
            elif key == "add_progress":
                f = fields(value)
                scope[f["name"]] = scope.get(f["name"], 0) + int(f["value"])
            elif key == "add_modifier":
                f = fields(value)
                scope["modifiers"][f["name"]] = self.day + self.ref(f["days"], scope, prev) if "days" in f else None
            elif key == "set_institution_investment_level":
                f = fields(value)
                scope["institution:" + f["institution"]]["investment"] = int(f["level"])
            else:
                super().effect([(key, op, value)], scope, prev)

    def policy_odds(self):
        weights = []
        for option in options("sb_nam.017"):
            weight = 0
            if self.condition(option.get("trigger", []), self.de):
                chance = fields(option["ai_chance"])
                weight = int(chance["base"])
                macro = AI_MACRO
                for key, value in fields(chance["sb_nam_survey_policy_weight"]).items():
                    macro = macro.replace("$" + key + "$", value)
                for key, _, block in statements(macro):
                    assert key == "modifier"
                    f = fields(block)
                    if self.condition(f["trigger"], self.de):
                        weight += self.calc(f["add"], self.de) if isinstance(f["add"], list) else int(f["add"])
            weights.append(int(weight))
        return tuple(round(100 * weight / sum(weights), 1) for weight in weights)


@patch.dict(EFFECTS, POLICIES)
@patch.dict(TRIGGERS, {**RULES, **SURVEY_TRIGGERS})
@patch.dict(VALUES, SURVEY_VALUES)
class NamibiaSurveyTests(unittest.TestCase):
    def test_maps_dispatch_once_for_endorsed_and_undecided_surveys(self):
        for marks, allowed in (({}, True), ({RESOLVED: 1, BACKED: 1}, True), ({RESOLVED: 1}, False)):
            world = SurveyRuntime()
            world.de["vars"].update(marks)
            for _ in range(2):
                world.effect([DISPATCH], world.de)
            self.assertEqual(world.events, [("sb_nam.011", "GER", 390)] if allowed else [])
            if allowed:
                self.assertTrue(world.condition(fields(EVENTS["sb_nam.011"])["trigger"], world.de))
                replay = deepcopy(world)
                self.assertTrue(replay.condition(fields(EVENTS["sb_nam.011"])["trigger"], replay.de))

    def test_held_or_queued_maps_cannot_pay_on_refusal_end_or_replacement(self):
        for change in ("refusal", "ended", "new survey"):
            world = SurveyRuntime()
            world.effect([DISPATCH], world.de)
            first = world.de["journal_entries"][SURVEY]
            if change == "refusal":
                world.de["vars"][RESOLVED] = 1
            elif change == "ended":
                world.de["journal_entries"].clear()
            else:
                world.de["journal_entries"][SURVEY] = {"vars": {}}
                world.effect([DISPATCH], world.de)
                self.assertEqual(len(world.events), 2)
                world.scopes["sb_nam_maps_survey"] = first
            event = fields(EVENTS["sb_nam.011"])
            self.assertFalse(world.condition(event["trigger"], world.de))
            self.assertTrue(world.condition(event["cancellation_trigger"], world.de))
            for option in options("sb_nam.011"):
                world.effect(option["hidden_effect"], world.de)
            self.assertEqual(world.de["gold_reserves"], 0)
            self.assertEqual(first["vars"][OFFER], 1)

    def test_legacy_dispatch_and_decline(self):
        world = SurveyRuntime()
        world.de["vars"][LEGACY_OFFER] = 1
        world.effect([DISPATCH], world.de)
        self.assertFalse(world.events)
        self.assertTrue(world.condition(fields(EVENTS["sb_nam.011"])["trigger"], world.de))
        world.effect(options("sb_nam.011")[1]["hidden_effect"], world.de)
        world.effect(options("sb_nam.011")[0]["hidden_effect"], world.de)
        self.assertEqual(world.de["gold_reserves"], 0)
        self.assertEqual(world.de["journal_entries"][SURVEY]["vars"][OFFER], 2)
        self.assertIn("remove_variable = " + LEGACY_OFFER, object_block(
            "common/scripted_effects/sb_namibia_effects.txt", "sb_nam_cleanup_coastal_expedition"))

    def test_cash_and_projected_credit_apply_to_choice_weight_and_payment(self):
        fund, decline = options("sb_nam.011")
        decline_when = fields(fields(decline["ai_chance"])["modifier"])["trigger"]
        for ai, cash, debt, credit, can_pay in (
                (False, 100000, 0, 0, True), (False, 99999, 0, 1000000, False),
                (True, 0, 7596000, 86876000, True), (True, 0, 0, 0, False),
                (True, 50000, 250000, 1000000, True), (True, 50000, 250001, 1000000, False)):
            with self.subTest(ai=ai, cash=cash, debt=debt):
                world = SurveyRuntime()
                world.de.update(is_ai=ai, gold_reserves=cash, principal=debt, credit=credit)
                world.effect([DISPATCH], world.de)
                self.assertEqual(world.condition(fund["trigger"], world.de), can_pay)
                self.assertEqual(world.condition(decline_when, world.de), not can_pay)
                world.effect(fund["hidden_effect"], world.de)
                # Even if borrowing capacity subsequently improves, a held answer is spent.
                world.de["credit"] = 10000000
                world.effect(fund["hidden_effect"], world.de)
                journal = world.de["journal_entries"][SURVEY]
                self.assertEqual(journal["vars"][OFFER], 2)
                self.assertEqual(world.de["gold_reserves"], cash - (100000 if can_pay else 0))
                self.assertEqual(journal.get("sb_namibian_coast_survey_progress_bar", 0), 10 if can_pay else 0)
                self.assertEqual(journal.get("sb_namibian_coast_expedition_peril_bar", 0), -2 if can_pay else 0)

    def test_settlers_conserve_free_primary_residents_across_cohorts(self):
        for sizes, expected in (((1800, 800), (1000, 1000)), ((998, 1001), (1000, 999)),
                                ((0, 1), (1, 0)), ((0, 0), (0, 0))):
            world = SurveyRuntime()
            people = [{"origin": "GER", "total_size": size, "culture": culture, "type": job, "vars": {}}
                      for size, culture, job in ((9000, "north_german", "slaves"), (5000, "czech", "peasants"),
                                                 (sizes[0], "south_german", "peasants"), (sizes[1], "north_german", "laborers"))]
            world.de["capital"]["pops"] = people
            before = sum(p["total_size"] for p in people)
            world.effect(POLICIES["sb_nam_move_founding_settlers"], world.swa)
            received = tuple(sum(n for (_, state, _), n in world.arrivals.items() if state == name) for name in world.states)
            self.assertEqual(received, expected)
            self.assertEqual([p["total_size"] for p in people[:2]], [9000, 5000])
            self.assertEqual(before, sum(p["total_size"] for p in people) + sum(received))
            self.assertTrue(all(s["vars"] == {} for s in world.states.values()))

    def test_founding_order_interrupted_handover_and_native_institution_ceiling(self):
        world = SurveyRuntime()
        world.de["vars"][POLICY] = 2
        gate = fields(EVENTS["sb_nam.018"])["trigger"]
        self.assertTrue(world.condition(gate, world.de))
        reconcile = fields(POLICIES["sb_nam_reconcile_seeded_policy_colony"][0][2])
        self.assertTrue(world.condition(reconcile["limit"], world.de))
        world.ports["p:xDEAA3C.state.owner"] = world.countries["GBR"]
        self.assertFalse(world.condition(reconcile["limit"], world.de))
        world.de["vars"]["sb_nam_policy_colony_founded_var"] = 1
        self.assertFalse(world.condition(gate, world.de))
        finish = object_block(NAMIBIA_POLICIES, "sb_nam_finish_policy_colony")
        order = ["set_variable = sb_nam_policy_colony_founded_var", "set_state_owner = c:SWA",
                 "sb_nam_apply_selected_policy_laws", "sb_nam_maximise_founding_colonial_affairs",
                 "sb_nam_move_founding_settlers", "sb_nam_offer_swa_play_as_to_player_overlord"]
        self.assertEqual(sorted(order, key=finish.index), order)
        self.assertNotIn("sb_nam_move_founding_settlers", str(PULSE))
        institution = world.swa["institution:institution_colonial_affairs"]
        for maximum in range(1, 6):
            institution.update(investment=2, investment_max=maximum)
            world.effect(POLICIES["sb_nam_maximise_founding_colonial_affairs"], world.swa)
            self.assertEqual(institution["investment"], maximum)
        institution["investment"] = 1
        world.effect([REPAIR], world.swa)
        self.assertEqual(institution["investment"], 1)

    def test_every_selection_records_the_same_deadline_and_only_the_first_choice(self):
        for policy in range(1, 5):
            world = SurveyRuntime()
            world.day = 830
            world.de["vars"]["sb_nam_policy_report_pending_var"] = 1
            with patch.dict(EFFECTS, {"sb_nam_try_found_policy_colony": [], "sb_nam_sync_regional_policy": []}):
                for pick in (policy, 4):
                    world.effect([("sb_nam_choose_policy", "=", [("POLICY", "=", str(pick))])], world.de)
                    world.day += 15
            self.assertEqual(world.de["vars"][POLICY], policy)
            self.assertEqual(world.de["vars"][EXPIRY], 4480)
            world.swa["vars"].update(world.de["vars"])
            world.effect(POLICIES["sb_nam_apply_administrative_capacity"], world.swa)
            self.assertEqual(world.swa["modifiers"][CAPACITY], 4480)

    def test_october_save_expiry_and_missing_entitlement(self):
        # Native game dates have 365 days per year. 689019 is the saved SWA policy deadline.
        world = SurveyRuntime()
        world.day = 1877 * 365 + 273  # 1 October
        end = 1887 * 365 + 264  # 22 September
        world.swa["vars"].update({EXPIRY: 689019, POLICY: 3})
        world.swa["modifiers"][CAPACITY] = None
        world.effect([REPAIR], world.swa)
        self.assertEqual(world.swa["modifiers"][CAPACITY], end)
        for day in (world.day + 30, end - 1):
            world.day = day
            world.effect([REPAIR], world.swa)
            self.assertEqual(world.swa["modifiers"][CAPACITY], end)
        del world.swa["modifiers"][CAPACITY]  # native expiry
        for day in (end, end + 30):
            world.day = day
            world.effect([REPAIR], world.swa)
            self.assertNotIn(CAPACITY, world.swa["modifiers"])
        for record in ({EXPIRY: end}, {}):
            world.swa["vars"] = record.copy()
            world.swa["modifiers"][CAPACITY] = None
            world.effect([REPAIR], world.swa)
            self.assertNotIn(CAPACITY, world.swa["modifiers"])

    def test_charter_ends_legacy_grant_on_original_founders_last_payment(self):
        for dated in (False, True):
            world = SurveyRuntime()
            world.de["vars"][PAYMENTS] = 2
            world.swa["vars"][POLICY] = 2
            world.swa["overlord"] = world.countries["GBR"]  # the original link has closed
            world.swa["modifiers"][CAPACITY] = None
            if dated:
                world.swa["vars"][EXPIRY] = 3650
            world.effect([REPAIR], world.swa)
            for remaining in (1, 0):
                world.effect(POLICIES["sb_nam_maintain_swa_company"], world.de)
                self.assertEqual(world.de["vars"].get(PAYMENTS, 0), remaining)
                self.assertEqual(CAPACITY in world.swa["modifiers"], dated or remaining > 0)
            self.assertEqual(world.de["gold_reserves"], -4000)
            if dated:
                self.assertEqual(world.swa["modifiers"][CAPACITY], 3650)

    def test_affinities_cabinets_outside_rulers_and_human_default(self):
        world = SurveyRuntime()
        world.swa["alive"] = False  # The sponsor chooses before formation.

        def cabinet(members, ruler=None):
            groups = {ig: {"type": "ig_" + ig, "ig_clout": clout, "is_in_government": True, "owner": world.de}
                      for ig, clout in members.items()}
            if ruler:
                groups.setdefault(ruler, {"type": "ig_" + ruler, "ig_clout": .15, "is_in_government": False, "owner": world.de})
            world.de["igs"] = list(groups.values())
            world.de["ruler"] = {"interest_group": groups[ruler]} if ruler else None

        for ig, row in (("devout", (75, 5, 15, 5)), ("industrialists", (5, 65, 10, 20)),
                        ("rural_folk", (10, 5, 80, 5)), ("petty_bourgeoisie", (10, 15, 60, 15)),
                        ("landowners", (10, 15, 30, 45)), ("armed_forces", (5, 10, 30, 55)),
                        ("intelligentsia", (40, 15, 45, 0)), ("trade_unions", (50, 5, 45, 0))):
            for members, ruler in (({ig: .2}, ig), ({ig: .2}, None), ({}, ig)):
                cabinet(members, ruler)
                self.assertEqual(world.policy_odds(), row)
        cabinet({}, None)
        self.assertEqual(world.policy_odds(), (25, 25, 25, 25))
        world.de["id"] = "GBR"
        self.assertEqual(world.policy_odds(), (33.3, 0, 33.3, 33.3))
        for rule in ("dynamic_historical", "off", "strict_historical"):
            world.rule = rule
            strict = rule == "strict_historical"
            world.de["id"] = "GER"
            cabinet({"devout": .19215, "landowners": .14986, "petty_bourgeoisie": .14571}, "petty_bourgeoisie")
            self.assertEqual(world.policy_odds(), (0, 0, 0, 100) if strict else (29.2, 12.0, 39.8, 19.0))
            world.de["id"] = "GBR"
            cabinet({"armed_forces": .12784, "devout": .13969}, "industrialists")
            self.assertEqual(world.policy_odds(), (0, 0, 0, 100) if strict else (37.2, 0, 25.1, 37.7))
        survey = options("sb_nam.017")
        self.assertEqual([o["name"] for o in survey if o.get("default_option") == "yes"], ["sb_nam.017.a"])
        self.assertEqual([o.get("trigger") for o in survey],
                         [None, [("sb_nam_can_found_policy_colony", "=", "yes")], None, None])
