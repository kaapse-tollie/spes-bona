"""Execute the Namibia survey scripts against representative campaign and legacy-save states."""
from copy import deepcopy
from datetime import date
from math import ceil
import unittest
from unittest.mock import patch

from tools.validate import find_game_root

if find_game_root(None) is None:
    raise unittest.SkipTest("installed Vanilla sources required by survey and court fixtures")

from tests.test_klip_river_refugees import RefugeeRuntime
from tests.test_warren_swa_policy import CORRIDOR_EFFECTS, NAMIBIA_EVENTS, NAMIBIA_POLICIES, NAMIBIA_TRIGGERS, object_block
from tests.test_zulu_court_politics import EFFECTS, GAME, TRAITS, TRIGGERS, VALUES, definitions
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import extract_top_level_blocks

SURVEY = "je_sb_map_namibian_coast"
OFFER = "sb_nam_maps_offer_var"
PROGRESS = "sb_namibian_coast_survey_progress_bar"
PERIL = "sb_namibian_coast_expedition_peril_bar"
ADMINISTRATION = "building_government_administration"
LEGACY_OFFER = "sb_nam_german_missionary_support_offered_var"
RESOLVED = "sb_nam_colonial_prestige_resolved_var"
BACKED = "sb_nam_colonial_programme_backed_var"
POLICY = "sb_nam_selected_policy_var"
EXPIRY = "sb_nam_policy_expiry_var"
CAPACITY = "sb_nam_administrative_capacity"
FOUNDER = "sb_nam_policy_founder_var"
HANDOVER = "sb_nam_handover_started_var"
FRONTIER = "law_type:law_frontier_colonization"
COLONIAL_LAW = "active_law:lawgroup_colonization"
CONCESSIONS = "amendment_sb_extractive_concessions"
GENERATION = "sb_nam_frontier_generation"
STRATEGY = "ai_strategy_sb_swa_colonial_affairs"
EXPERT = "expert_colonial_administrator"
NATIVE_EXPERT = extract_top_level_blocks((GAME / "common/character_traits/skill_traits.txt").read_text(encoding="utf-8-sig"))[EXPERT]
PAYMENTS = "sb_nam_company_payments_left_var"
PULSE = definitions("common/on_actions/sb_namibia_on_actions.txt")["sb_on_namibia_monthly_pulse_country"]
EVENTS = {name: statements(object_block(NAMIBIA_EVENTS, name)) for name in ("sb_nam.010", "sb_nam.011", "sb_nam.017", "sb_nam.018")}
BARS = definitions("common/scripted_progress_bars/sb_namibia_progress_bars.txt")
POLICIES = definitions(NAMIBIA_POLICIES)
COAST = definitions("common/scripted_effects/sb_namibia_effects.txt")
OLD_MAPPING = "sb_nam_mapping_permanent_engagement_var"
COASTAL_REGIONS = {"HEREROLAND", "NAMAQUALAND"}
COLONISATION_LAWS = {"law_type:law_" + law for law in
                     ("no_colonial_affairs", "internal_colonization", "frontier_colonization",
                      "colonial_resettlement", "colonial_exploitation")}
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
        if key.startswith("ig:") and isinstance(scope, dict) and key in scope:
            return scope[key]
        if key in ("THIS", "PREV"):
            return super().ref(key.lower(), scope, prev)
        if key.startswith("PREV."):
            return self.ref(key[5:], prev)
        if key.startswith("law_type:"):
            return key
        if key == "region_state:SWA":
            return scope.get("swa_fragment")
        if key.count(".") == 2 and all(part.isdigit() for part in key.split(".")):
            return date(*map(int, key.split("."))).toordinal()
        if key == "root":
            return self.scopes["root"]
        if key in self.ports:
            return self.ports[key]
        if key == "game_date":
            return self.day
        if key == "long_modifier_time":
            return 3650
        if key.startswith("s:STATE_") and key.endswith(".region_state:SWA"):
            return self.states[key[8:].split(".")[0]]
        if key.startswith("s:STATE_"):
            return self.states[key[8:]]
        if key.startswith("je:"):
            return scope["journal_entries"].get(key[3:])
        if key.startswith("cd:"):
            return key[3:]
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        for key, op, value in nodes:
            if key in ("is_ai", "is_in_government", "is_subject", "is_coastal", "is_land_theater"):
                passed = scope[key] == (value == "yes")
            elif key == "is_player":
                passed = (not scope["is_ai"]) == (value == "yes")
            elif key == "is_subject_of":
                passed = scope.get("overlord") is self.ref(value, scope, prev)
            elif key == "has_institution":
                passed = "institution:" + value in scope
            elif key == "has_building":
                passed = scope.get("buildings", {}).get(value, 0) > 0
            elif key == "has_amendment":
                passed = value.removeprefix("amendment_type:") in scope.get("amendments", {})
            elif key == "has_company":
                passed = value in scope.get("companies", [])
            elif key in ("is_subject_type", "is_company_type"):
                passed = scope.get(key) == value
            elif key in ("is_land_adjacent_to_state", "is_adjacent_to_state"):
                passed = self.ref(value, scope, prev)["id"] in scope.get("land_borders", set())
            elif key in ("any_sea_node_adjacent_state", "any_political_movement"):
                items = scope.get("sea_neighbours" if key == "any_sea_node_adjacent_state" else "movements", [])
                passed = any(self.condition(value, item, scope) for item in items)
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
            elif key == "is_direct_subject_of":
                passed = scope.get("overlord") is self.ref(value, scope, prev)
            elif key == "has_claim":
                passed = self.ref(value, scope, prev)["id"] in scope.get("claims", set())
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
            elif key == "overlord":
                self.effect(value, scope["overlord"], scope)
            elif key in ("add_claim", "remove_claim"):
                claims = self.ref(value, scope, prev).setdefault("claims", set())
                if key == "add_claim":
                    claims.add(scope["id"])
                else:
                    claims.discard(scope["id"])
            elif key == "activate_law" and value in COLONISATION_LAWS:
                laws = scope.setdefault("laws", set())
                if scope.get(COLONIAL_LAW, {}).get("type") != value:
                    scope[COLONIAL_LAW] = {"type": value, "amendments": {}}
                laws.difference_update(COLONISATION_LAWS)
                laws.add(value)
            elif key.startswith("active_law:"):
                if key in scope:
                    self.effect(value, scope[key], scope)
            elif key == "add_amendment":
                f = fields(value)
                scope["amendments"][f["type"]] = (prev["id"], self.ref(f["sponsor"], scope, prev))
            elif key == "create_country":
                f = fields(value)
                assert f["tag"] == "SWA" and self.ref(f["origin"], scope, prev) is scope
                assert not self.swa["alive"]
                self.swa["alive"] = True
                for field, _, province in value:
                    if field == "province":
                        assert self.ports[province + ".state.owner"] is scope
                        self.ports[province + ".state.owner"] = self.swa
            elif key == "set_strategy":
                scope["strategy"] = value
            elif key == "create_diplomatic_pact":
                f = fields(value)
                subject = self.ref(f["country"], scope, prev)
                subject.update(is_subject=True, overlord=scope, is_subject_type="subject_type_" + f["type"])
            elif key == "set_country_type":
                scope["is_country_type"] = value
            elif key == "set_state_owner":
                new_owner = self.ref(value, scope, prev)
                scope["owner"]["states"].remove(scope)
                new_owner["states"].append(scope)
                scope["owner"] = new_owner
            elif key == "every_primary_culture":
                for culture in scope["primary"]:
                    self.effect(value, culture, scope)
            elif key == "add_primary_culture":
                scope["primary"].add(self.ref(value, scope, prev))
            elif key == "remove_primary_culture":
                scope["primary"].discard(value)
            elif key == "set_capital":
                scope["capital"] = self.states[value.removeprefix("STATE_")]
            elif key == "set_state_type":
                scope["is_incorporated"] = value == "incorporated"
            elif key == "create_building":
                f = fields(value)
                buildings = scope.setdefault("buildings", {})
                buildings[f["building"]] = buildings.get(f["building"], 0) + int(f["level"])
            elif key == "add_technology_researched":
                scope.setdefault("technologies", set()).add(value)
            elif key == "add_company":
                scope.setdefault("companies", []).append(value)
                scope[value.replace("company_type:", "company:")] = {"is_company_type": value}
            elif key.startswith("company:"):
                self.effect(value, scope[key], scope)
            elif key == "set_company_state_region":
                scope["state_region"] = self.ref(value, scope, prev)
            elif key == "add_owned_country":
                self.ref(value, scope, prev)["owning_company"] = scope
            elif key == "create_character":
                scope.setdefault("characters", []).append({"template": fields(value)["template"], "owner": scope,
                                                          "traits": set(), "alive": True})
            elif key == "set_as_interest_group_leader":
                scope["ig_leader"] = True
            elif key == "change_variable" and "subtract" in fields(value):
                f = fields(value)
                scope["vars"][f["name"]] -= self.ref(f["subtract"], scope, prev)
            elif key == "add_progress":
                f = fields(value)
                bar = fields(BARS[f["name"]])
                result = scope.get(f["name"], int(bar["start_value"])) + int(f["value"])
                scope[f["name"]] = max(int(bar["min_value"]), min(int(bar["max_value"]), result))
            elif key == "add_modifier":
                f = fields(value)
                if f["name"] == GENERATION and GENERATION in scope["modifiers"]:
                    raise AssertionError("Repeated capital generation grant")
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
@patch.dict(TRAITS, {EXPERT: NATIVE_EXPERT})
class NamibiaSurveyTests(unittest.TestCase):
    def test_survey_and_monthly_claims_distinguish_a_swa_founder_from_direct_rule(self):
        survey = COAST["sb_nam_finalize_coastal_expedition_success"]
        grants = [(key, op, [n for n in body if n[0] != "set_owner_of_provinces"])
                  for branch, _, nodes in survey if branch == "if"
                  for key, op, body in nodes if key.startswith("s:STATE_")]
        self.assertEqual(len(grants), 2)
        self.assertNotIn(OLD_MAPPING, str(survey))
        monthly = branch_containing(fields(PULSE)["effect"], "add_claim")
        for stage in ("survey", "seeded", "overlord", "British direct rule"):
            with self.subTest(stage=stage):
                world = SurveyRuntime()
                sponsor = world.de
                world.countries["CAP"] = {"states": [], "vars": {}}
                world.swa["alive"] = stage in ("seeded", "overlord")
                if stage == "seeded":
                    sponsor["vars"][POLICY] = 3
                    world.swa["vars"][HANDOVER] = world.day
                if stage == "overlord":
                    world.swa.update(overlord=sponsor, is_subject=True)
                if stage == "British direct rule":
                    sponsor["id"] = "GBR"
                    world.countries["GBR"] = sponsor
                expected = COASTAL_REGIONS if stage == "British direct rule" else set()
                world.effect(grants, sponsor)
                self.assertEqual(sponsor.get("claims", set()), expected)
                sponsor["claims"] = set()
                world.scopes["root"] = sponsor
                world.effect([monthly], sponsor)
                self.assertEqual(sponsor["claims"], expected & {"NAMAQUALAND"})

    @patch.dict(EFFECTS, COAST)
    def test_handover_and_old_survey_cleanup_release_only_the_sponsors_coastal_claims(self):
        release = "sb_nam_relinquish_swa_coastal_claims"
        for handover in (POLICIES["sb_nam_finish_policy_colony"], COAST["sb_nam_finalize_swa_administration"]):
            world = SurveyRuntime()  # GBR is the foreign event root.
            world.de["claims"] = COASTAL_REGIONS | {"FLANDERS"}
            world.scopes["root"]["claims"] = {"HEREROLAND"}
            world.effect([n for n in handover if n[0] == release or
                          (n[0].startswith("s:STATE_") and "add_claim" in str(n))], world.de)
            self.assertEqual(world.swa["claims"], COASTAL_REGIONS)
            self.assertEqual(world.de["claims"], {"FLANDERS"})
            self.assertEqual(world.scopes["root"]["claims"], {"HEREROLAND"})

        repair = branch_containing(SWA_MONTHLY[2], OLD_MAPPING)
        for registered_founder in (False, True):
            world = SurveyRuntime()
            if registered_founder:
                world.de["vars"]["sb_nam_policy_colony_founded_var"] = 1
                world.swa["overlord"] = world.countries["GBR"]  # The charter has changed hands.
            else:
                world.swa["vars"].pop(FOUNDER)
                world.de["vars"][OLD_MAPPING] = 1
                world.swa["overlord"] = world.de
            world.de["claims"] = COASTAL_REGIONS | {"WALLONIA", "FLANDERS"}
            world.countries["GBR"]["claims"] = {"HEREROLAND"}
            world.swa["claims"] = {"NAMAQUALAND"}  # An earlier peace revoked its other claim.
            world.effect([repair], world.swa)
            self.assertEqual(world.de["claims"], {"WALLONIA", "FLANDERS"})
            self.assertEqual(world.swa["claims"], {"NAMAQUALAND"})
            self.assertEqual(world.countries["GBR"]["claims"], {"HEREROLAND"})
            world.de["claims"].add("HEREROLAND")
            world.effect([repair], world.swa)
            self.assertIn("HEREROLAND", world.de["claims"])

    def test_corridor_awards_only_the_living_colonys_claims_even_with_an_old_saved_sponsor(self):
        settlement = definitions(CORRIDOR_EFFECTS)["sb_bechuanaland_apply_boer_swa_settlement"]
        start = next(i for i, n in enumerate(settlement)
                     if n[0] == "if" and "sb_bechuanaland_transfer_tsw_corridor_to_root" in str(n))
        for alive in (True, False):
            for score in (-1, 0, 1):
                world = SurveyRuntime()
                regions = {"BOTSWANA", "KAZEMBE", "ZAMBIA", "ZAMBEZI"}
                world.states.update({name: {"id": name} for name in regions})
                world.swa["alive"] = alive
                world.scopes["sb_bechuanaland_swa_settlement_claimant_scope"] = world.de
                world.containers["sb_bechuanaland_corridor_state"] = {"vars": {
                    "sb_bechuanaland_influence_score_var": score, "sb_bechuanaland_swa_claimant_scope": world.de}}
                with patch.dict(EFFECTS, {"sb_bechuanaland_grant_swa_settlement_leverage": []}), \
                        patch.dict(TRIGGERS, {"sb_pink_map_precedes_bechuanaland": [("always", "=", "no")]}):
                    world.effect(settlement[start:start + 3], world.de)
                expected = {-1: regions, 0: {"BOTSWANA"}, 1: set()}[score]
                self.assertEqual(world.swa.get("claims", set()), expected if alive else set())
                self.assertFalse(world.de.get("claims"))

    def test_all_swa_policies_replace_the_inherited_overseas_law_only_on_the_colony(self):
        for policy, old_package in enumerate(("mission", "charter", "extractive", "exterminatory"), 1):
            world = SurveyRuntime()
            world.swa["vars"][POLICY] = policy
            world.swa["laws"] = {"law_type:law_colonial_exploitation"}
            with patch.dict(EFFECTS, {"sb_nam_apply_swa_subjecthood_amendment": []}):
                world.effect(POLICIES["sb_nam_apply_selected_policy_laws"], world.swa)
            self.assertEqual(world.swa["laws"] & COLONISATION_LAWS, {"law_type:law_frontier_colonization"})
            expected = {CONCESSIONS: ("SWA", "ig:ig_industrialists")} if policy in (2, 4) else {}
            self.assertEqual(world.swa[COLONIAL_LAW]["amendments"], expected)
            self.assertEqual(world.de["laws"], {"law_type:law_colonial_resettlement"})
            economy = "agrarianism" if policy in (1, 3) else "extraction_economy"
            self.assertIn("law_type:law_" + economy, world.swa["laws"])
            world.swa["laws"] = {"law_type:law_colonial_resettlement"}
            world.swa["vars"][f"sb_nam_administration_{old_package}_var"] = 1
            with patch.dict(EFFECTS, {**COAST, "sb_nam_apply_swa_subjecthood_amendment": []}):
                world.effect(COAST["sb_nam_apply_swa_administration_package"], world.swa)
            self.assertEqual(world.swa["laws"] & COLONISATION_LAWS, {"law_type:law_frontier_colonization"})

    def test_berlin_skips_an_existing_colonial_institution_without_refusing_maps(self):
        dispatch = branch_containing(fields(PULSE)["effect"], "sb_nam.010")
        berlin = fields(EVENTS["sb_nam.010"])
        for law in sorted(COLONISATION_LAWS):
            with self.subTest(law=law):
                world = SurveyRuntime()
                world.day = date(1872, 4, 12).toordinal()
                world.de["ig:ig_landowners"] = {"is_in_government": True}
                world.de["ig:ig_armed_forces"] = {"is_in_government": False}
                world.de["laws"] = {law}
                eligible = law == "law_type:law_no_colonial_affairs"
                if not eligible:
                    world.de["institution:institution_colonial_affairs"] = {"investment": 1}
                world.effect([dispatch], world.de)
                self.assertEqual(bool(world.events), eligible)
                self.assertEqual(world.condition(berlin["trigger"], world.de), eligible)
                world.de["institution:institution_colonial_affairs"] = {"investment": 1}
                self.assertTrue(world.condition(berlin["cancellation_trigger"], world.de))
                for option in options("sb_nam.010"):
                    world.effect(option["hidden_effect"], world.de)
                self.assertFalse(world.de["vars"])
                world.effect([DISPATCH], world.de)
                self.assertIn(("sb_nam.011", "GER", 390), world.events)

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

    def test_an_explicit_berlin_refusal_blocks_the_later_expedition_offer(self):
        world = SurveyRuntime()
        world.day = date(1870, 1, 1).toordinal()
        world.de["laws"] = {"law_type:law_no_colonial_affairs"}
        world.de["ig:ig_landowners"] = {"is_in_government": True, "modifiers": {}}
        world.de["ig:ig_armed_forces"] = {"is_in_government": False}
        world.de["journal_entries"].clear()
        world.effect(options("sb_nam.010")[1]["hidden_effect"], world.de)
        self.assertIn(RESOLVED, world.de["vars"])
        self.assertNotIn(BACKED, world.de["vars"])
        world.de["institution:institution_colonial_affairs"] = {"investment": 4}
        world.de["journal_entries"][SURVEY] = {"vars": {}}
        world.effect([DISPATCH], world.de)
        self.assertFalse(world.events)

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
        self.assertEqual(world.de["journal_entries"][SURVEY]["vars"][OFFER], 3)
        self.assertIn("remove_variable = " + LEGACY_OFFER, object_block(
            "common/scripted_effects/sb_namibia_effects.txt", "sb_nam_cleanup_coastal_expedition"))

    def test_cash_and_projected_credit_apply_to_choice_weight_and_payment(self):
        fund, decline = options("sb_nam.011")
        decline_when = fields(fields(decline["ai_chance"])["modifier"])["trigger"]
        for ai, cash, debt, credit, can_pay in (
                (False, 100000, 0, 0, True), (False, 99999, 0, 1000000, False),
                (True, 0, 7596000, 86876000, True), (True, 0, 0, 0, False),
                (True, 50000, 250000, 1000000, True), (True, 50000, 250001, 1000000, False),
                (False, 0, 87604636, 95728410, False), (True, 0, 87604636, 95728410, False)):
            with self.subTest(ai=ai, cash=cash, debt=debt):
                world = SurveyRuntime()
                world.de.update(is_ai=ai, gold_reserves=cash, principal=debt, credit=credit)
                world.effect([DISPATCH], world.de)
                self.assertTrue(world.condition(fields(EVENTS["sb_nam.011"])["trigger"], world.de))
                self.assertTrue(world.condition(fund["show_as_unavailable"], world.de))
                journal = world.de["journal_entries"][SURVEY]
                journal.update({PROGRESS: 7, PERIL: 4})
                self.assertEqual(world.condition(fund["trigger"], world.de), can_pay)
                self.assertEqual(world.condition(decline_when, world.de), not can_pay)
                world.effect(fund["hidden_effect"], world.de)
                # Even if borrowing capacity subsequently improves, a held answer is spent.
                world.de["credit"] = 10000000
                world.effect(fund["hidden_effect"], world.de)
                self.assertEqual(journal["vars"][OFFER], 2 if can_pay else 3)
                self.assertEqual(world.de["gold_reserves"], cash - (100000 if can_pay else 0))
                self.assertEqual((journal[PROGRESS], journal[PERIL]), (17, 2) if can_pay else (7, 4))

    def test_funded_maps_apply_once_at_the_limits_of_both_displayed_bars(self):
        world = SurveyRuntime()
        world.de.update(is_ai=False, gold_reserves=100000)
        world.de["journal_entries"][SURVEY].update({PROGRESS: 27, PERIL: 1})
        world.effect([DISPATCH], world.de)
        replay = deepcopy(world)
        fund, decline = options("sb_nam.011")
        for option in (fund, fund, decline):
            replay.effect(option["hidden_effect"], replay.de)
        journal = replay.de["journal_entries"][SURVEY]
        self.assertEqual((journal[PROGRESS], journal[PERIL], journal["vars"][OFFER]), (30, 0, 2))
        self.assertEqual(replay.de["gold_reserves"], 0)

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

    def test_founding_order_and_native_institution_ceiling(self):
        world = SurveyRuntime()
        finish = object_block(NAMIBIA_POLICIES, "sb_nam_finish_policy_colony")
        order = ["set_variable = sb_nam_policy_colony_founded_var", "set_state_owner = c:SWA",
                 "sb_nam_apply_selected_policy_laws", "sb_nam_maximise_founding_colonial_affairs",
                 "sb_nam_move_founding_settlers", "sb_nam_establish_swa_company", "sb_nam_assign_german_swa_ruler",
                 "set_strategy = " + STRATEGY, "sb_nam_offer_swa_play_as_to_player_overlord"]
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

    @staticmethod
    def before_founding(policy):
        world = SurveyRuntime()
        world.swa.update(alive=False, is_ai=True, is_country_type="colonial", vars={}, states=[], primary={"cu:british"})
        world.de.update(is_ai=False, modifiers={}, states=[])
        world.de["vars"][POLICY] = policy
        world.de["capital"]["pops"] = [{"origin": "GER", "culture": "north_german", "type": "peasants", "total_size": 5000}]
        world.day = date(1877, 9, 4).toordinal()
        world.ports = dict.fromkeys(world.ports, world.de)
        return world

    @patch.dict(EFFECTS, COAST)
    def test_both_ports_then_one_administration_across_reload_and_monthly_retry(self):
        event = fields(EVENTS["sb_nam.018"])
        for policy in range(1, 5):
            with self.subTest(policy=policy):
                world = self.before_founding(policy)
                inherited_offices = 2 if policy == 2 else 0
                world.states["HEREROLAND"]["buildings"] = {ADMINISTRATION: inherited_offices}
                deadline = world.day + 900
                world.de["vars"][EXPIRY] = deadline
                extra = {"owner": world.de, "state_region": world.states["HEREROLAND"], "id": "extra", "vars": {}, "modifiers": {}}
                world.de["states"].append(extra)
                world.effect(POLICIES["sb_nam_try_found_policy_colony"], world.de)
                self.assertTrue(all(owner is world.swa for owner in world.ports.values()))
                self.assertEqual(world.states["HEREROLAND"]["buildings"][ADMINISTRATION], max(1, inherited_offices))
                self.assertNotIn(ADMINISTRATION, world.states["NAMAQUALAND"].get("buildings", {}))
                self.assertEqual(world.events, [("sb_nam.018", "GER", 1)])
                self.assertIs(world.scopes["sb_nam_new_colony"], world.swa)
                self.assertTrue(world.condition(event["trigger"], world.de))
                retry = branch_containing(fields(PULSE)["effect"], "sb_nam_reconcile_seeded_policy_colony")
                world.effect([retry], world.de)
                self.assertFalse(world.swa["is_subject"])  # The creation-day pulse is too early.
                world = deepcopy(world)
                world.scopes.pop("sb_nam_policy_founder")  # Only saved scopes survive event delivery.
                world.day += 1
                world.effect(event["immediate"] if policy % 2 else [retry], world.de)
                self.assertFalse(world.condition(event["trigger"], world.de))
                world.effect([retry], world.de)
                self.assertIs(world.swa["overlord"], world.de)
                self.assertEqual(world.swa["vars"][EXPIRY], deadline)
                self.assertEqual(world.swa["modifiers"][CAPACITY], deadline)
                self.assertEqual(world.swa["is_subject_type"], "subject_type_chartered_company" if policy == 2 else "subject_type_colony")
                self.assertIn("extra", [state["id"] for state in world.swa["states"]])
                self.assertEqual(world.de["capital"]["pops"][0]["total_size"], 3000)
                self.assertEqual([world.arrivals["GER", region, "north_german"] for region in world.states], [1000, 1000])
                self.assertEqual(len(world.de.get("companies", [])), int(policy == 2))
                self.assertEqual(world.de["vars"].get(PAYMENTS), 120 if policy == 2 else None)
                self.assertEqual(world.events.count(("sb_nam.151", "GER", 1)), 1)
                self.assertEqual(world.swa["strategy"], STRATEGY)
                self.assertIn(EXPERT, world.swa["ruler"]["traits"])
                self.assertEqual(world.states["HEREROLAND"]["buildings"][ADMINISTRATION], max(1, inherited_offices))

    def test_rival_ports_wrong_founder_and_replacement_colony(self):
        event = fields(EVENTS["sb_nam.018"])
        for port in ("p:xDEAA3C.state.owner", "p:xB04050.state.owner"):
            world = self.before_founding(2)
            rival = world.countries["GBR"]
            world.ports[port] = rival
            world.effect(POLICIES["sb_nam_try_found_policy_colony"], world.de)
            self.assertFalse(world.swa["alive"])
            self.assertNotIn(ADMINISTRATION, world.states["HEREROLAND"].get("buildings", {}))
            self.assertEqual(world.events, [])
            world.ports[port] = world.de
            world.effect(POLICIES["sb_nam_try_found_policy_colony"], world.de)
            world.day += 1
            rival["vars"][POLICY] = 2
            self.assertFalse(world.condition(event["trigger"], rival))
            world.countries["SWA"] = dict(world.swa)  # Same tag, founder and date, different country object.
            self.assertFalse(world.condition(event["trigger"], world.de))
            world.countries["SWA"] = world.swa
            world.ports[port] = rival
            ownership = world.ports.copy()
            world.effect(event["immediate"], world.de)
            self.assertTrue(all(world.ports[key] is owner for key, owner in ownership.items()))
            self.assertFalse(world.condition(event["trigger"], world.de))
            self.assertFalse(world.swa["is_subject"])
            self.assertFalse(world.arrivals)
            self.assertNotIn(PAYMENTS, world.de["vars"])

        for participant in ("de", "swa"):
            world = self.before_founding(2)
            world.effect(POLICIES["sb_nam_try_found_policy_colony"], world.de)
            world.day += 1
            subject = getattr(world, participant)
            subject.update(is_subject=True, overlord=world.countries["GBR"])
            world.effect(event["immediate"], world.de)
            self.assertIs(subject["overlord"], world.countries["GBR"])
            self.assertFalse(world.condition(event["trigger"], world.de))
            self.assertFalse(world.arrivals)
            self.assertNotIn(PAYMENTS, world.de["vars"])

    def test_concessions_match_vanilla_and_only_active_ruthless_concessions_unlock_orders(self):
        amendment = fields(definitions("common/amendments/sb_amendments.txt")[CONCESSIONS])
        self.assertEqual(amendment["parent"], "law_colonial_exploitation")
        self.assertEqual(list(fields(amendment["allowed_laws"])), ["law_frontier_colonization"])
        self.assertEqual(amendment["can_repeal"], [("legitimacy", ">=", "legitimacy_to_repeal_amendment")])
        self.assertEqual(fields(amendment["ai_will_revoke"])["always"], "yes")
        vanilla = definitions(GAME / "common/laws/01_colonial_affairs.txt")
        def bonuses(block):
            return {name: float(value) for name, _, value in fields(block)["modifier"]}
        exploitation = bonuses(vanilla["law_colonial_exploitation"])
        frontier = bonuses(vanilla["law_frontier_colonization"])
        concessions = {name: float(value) for name, _, value in amendment["modifier"]}
        self.assertEqual(concessions, exploitation | {"state_migration_pull_unincorporated_mult": -frontier["state_migration_pull_unincorporated_mult"]})
        gate = SURVEY_TRIGGERS["sb_nam_extermination_orders_available"]
        with patch.dict(TRIGGERS, {"sb_nam_controls_administration_territory": [("always", "=", "yes")]}):
            for policy in range(1, 5):
                world = SurveyRuntime()
                world.swa["vars"][POLICY] = policy
                world.swa["movements"] = [{"type": "movement_minority_rights", "political_movement_radicalism": .75}]
                world.swa[COLONIAL_LAW] = {"type": FRONTIER, "amendments": {CONCESSIONS: "Industrialists"}}
                self.assertEqual(world.condition(gate, world.swa), policy == 4)
                world.swa[COLONIAL_LAW]["amendments"].clear()
                self.assertFalse(world.condition(gate, world.swa))
                for law in ("law_colonial_exploitation", "law_national_supremacy", "law_ethnostate"):
                    world.swa["laws"] = {"law_type:" + law}
                    self.assertEqual(world.condition(gate, world.swa), policy in (3, 4))
                world.swa["movements"][0]["political_movement_radicalism"] = .749
                self.assertFalse(world.condition(gate, world.swa))

    @patch.dict(EFFECTS, COAST)
    def test_governor_date_boundaries_reuse_and_natural_succession(self):
        for when, template in (("1890.12.31", "SWA_heinrich_ernst_goring"), ("1891.1.1", "SWA_curt_von_francois"),
                               ("1893.12.31", "SWA_curt_von_francois"), ("1894.1.1", "SWA_theodor_leutwein")):
            for lower in ("basic_colonial_administrator", "experienced_colonial_administrator"):
                world = SurveyRuntime()
                world.day = world.ref(when, world.de)
                appointee = {"template": template, "owner": world.swa, "alive": True, "traits": {lower, "persistent"}}
                successor = {"template": "generic", "owner": world.swa, "alive": True, "traits": set()}
                world.swa["characters"] = [successor, appointee]
                world.effect(COAST["sb_nam_assign_german_swa_ruler"], world.de)
                self.assertIs(world.swa["ruler"], appointee)
                self.assertEqual(appointee["traits"], {EXPERT, "persistent"})
                self.assertEqual(len(world.swa["characters"]), 2)
                world.swa["ruler"] = successor
                self.assertNotIn("sb_nam_assign_german_swa_ruler", str(PULSE))
                world.effect(COAST["sb_nam_assign_german_swa_ruler"], world.countries["GBR"])
                self.assertIs(world.swa["ruler"], successor)
                self.assertFalse(successor["traits"])

    def test_swa_strategy_is_an_ai_institution_preference(self):
        strategy = fields(definitions("common/ai_strategies/sb_ai_strategies.txt")[STRATEGY])
        self.assertEqual(fields(strategy["weight"])["value"], "1000")
        self.assertEqual(fields(fields(strategy["institution_scores"])["institution_colonial_affairs"])["value"], "10000")
        world = SurveyRuntime()
        for subject in ("subject_type_colony", "subject_type_chartered_company"):
            world.swa.update(is_ai=True, is_subject=True, is_subject_type=subject)
            self.assertTrue(world.condition(strategy["possible"], world.swa))
            world.swa["is_ai"] = False
            self.assertFalse(world.condition(strategy["possible"], world.swa))
        world.swa["is_ai"] = True
        world.swa.pop("institution:institution_colonial_affairs")
        self.assertFalse(world.condition(strategy["possible"], world.swa))
        self.assertFalse(world.condition(strategy["possible"], world.de))
        self.assertNotIn("sb_nam_maximise_founding_colonial_affairs", str(PULSE))

    @staticmethod
    def frontier_world():
        world = SurveyRuntime()
        world.swa.update(is_country_type="colonial", states=[], land_borders=set())
        for region in world.states.values():
            station = {"id": region["id"] + " station", "vars": {}, "owner": world.swa, "is_coastal": True,
                       "theater": {"is_land_theater": True}, "is_incorporated": False, "modifiers": {}}
            interior = {"id": region["id"] + " interior", "owner": {"is_country_type": "decentralized"},
                        "is_coastal": False, "sea_neighbours": []}
            region.update(swa_fragment=station, states=[station, interior])
            world.swa["states"].append(station)
            world.swa["land_borders"].add(interior["id"])
        world.swa["capital"] = world.states["HEREROLAND"]["swa_fragment"]
        world.swa["capital"]["is_incorporated"] = True
        return world

    def test_two_fronts_use_local_land_or_capital_connected_coast_during_the_policy_term(self):
        sync = POLICIES["sb_nam_sync_frontier_generation"]
        modifier = fields(definitions("common/static_modifiers/sb_namibia_modifiers.txt")[GENERATION])
        self.assertEqual(float(modifier["state_colony_growth_creation_factor"]), 340)
        for policy in range(1, 5):
            world = self.frontier_world()
            world.swa["vars"].update({POLICY: policy, EXPIRY: 3650})
            world.day = 2400  # SWA forms well after the survey policy was chosen.
            capital = world.swa["capital"]
            nama_port, nama_target = world.states["NAMAQUALAND"]["states"]
            world.swa["land_borders"].remove(nama_target["id"])
            nama_target.update(is_coastal=True, sea_neighbours=[nama_port, capital])
            world.swa["is_ai"] = policy % 2 == 0
            capital["colonization_paused"] = True
            world.effect(sync, world.swa)
            world.effect(sync, world.swa)
            self.assertEqual(capital["modifiers"][GENERATION], 3650)
            self.assertNotIn(GENERATION, nama_port["modifiers"])
            nama_target["sea_neighbours"] = [nama_port]  # A disconnected SWA station.
            world.effect(sync, world.swa)
            self.assertNotIn(GENERATION, capital["modifiers"])
            world.day = 3649
            world.swa["land_borders"].add(nama_target["id"])
            world.effect(sync, world.swa)
            self.assertEqual(capital["modifiers"][GENERATION], 3650)
            for region in world.states.values():
                target = region["states"][1]
                target["owner"]["is_country_type"] = "unrecognized"
                world.effect(sync, world.swa)
                self.assertNotIn(GENERATION, capital["modifiers"])
                target["owner"]["is_country_type"] = "decentralized"
                station = region.pop("swa_fragment")  # A reachable region without an SWA foothold.
                world.effect(sync, world.swa)
                self.assertNotIn(GENERATION, capital["modifiers"])
                region["swa_fragment"] = station
                world.effect(sync, world.swa)
                self.assertEqual(capital["modifiers"][GENERATION], 3650)
            for day in (3650, 3680):
                world.day = day
                world.effect(sync, world.swa)
                self.assertNotIn(GENERATION, capital["modifiers"])

    def test_monthly_update_dates_an_old_permanent_grant_only_for_the_remaining_term(self):
        monthly = branch_containing(SWA_MONTHLY[2], "sb_nam_sync_frontier_generation")
        checkpoint = 1878 * 365 + 181  # 1 July 1878, German Ruthless SWA.
        saved_expiry = 688635  # 3 September 1886, as recorded on Bureaucracy.
        for deadline in (saved_expiry, checkpoint, checkpoint - 1, None):
            with self.subTest(deadline=deadline):
                world = self.frontier_world()
                world.swa["vars"][POLICY] = 4
                if deadline is not None:
                    world.swa["vars"][EXPIRY] = deadline
                world.swa["capital"]["modifiers"][GENERATION] = None  # Saved without a duration.
                for day in (checkpoint, checkpoint + 30, saved_expiry, saved_expiry + 30):
                    world.day = day
                    world.effect([monthly], world.swa)
                    modifiers = world.swa["capital"]["modifiers"]
                    if deadline is not None and day < deadline:
                        self.assertEqual(modifiers[GENERATION], deadline)
                    else:
                        self.assertNotIn(GENERATION, modifiers)
                    world = deepcopy(world)

    def test_generation_moves_with_the_capital_and_is_removed_on_foreign_transfer(self):
        world = self.frontier_world()
        world.swa["vars"].update({POLICY: 2, EXPIRY: 3650})
        monthly = branch_containing(SWA_MONTHLY[2], "sb_nam_sync_frontier_generation")
        action = fields(definitions("common/on_actions/sb_namibia_on_actions.txt")["sb_on_swa_frontier_state_owner_change"])
        original, new = world.swa["states"]
        world.states["NAMAQUALAND"]["states"].append({"owner": {"id": "CAP", "is_country_type": "colonial"},
                                                      "id": "Walvis Bay", "is_coastal": True})
        world.effect([monthly], world.swa)
        self.assertEqual(original["modifiers"][GENERATION], 3650)
        world.day = 3500
        world.swa["capital"] = new
        world.effect([monthly], world.swa)
        self.assertNotIn(GENERATION, original["modifiers"])
        self.assertNotIn(GENERATION, new["modifiers"])  # New capital is still unincorporated.
        new["is_incorporated"] = True
        world.effect([monthly], world.swa)
        self.assertEqual(new["modifiers"][GENERATION], 3650)
        world.swa["states"] = [original]
        world.swa["capital"] = original
        new["owner"] = world.de
        world.states["NAMAQUALAND"].pop("swa_fragment")
        self.assertTrue(world.condition(action["trigger"], new))
        world.effect(action["effect"], new)
        self.assertNotIn(GENERATION, new["modifiers"])
        self.assertNotIn(GENERATION, original["modifiers"])

    def test_every_selection_records_the_same_deadline_and_only_the_first_choice(self):
        for policy in range(1, 5):
            world = self.frontier_world()
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
            world.effect(POLICIES["sb_nam_sync_frontier_generation"], world.swa)
            self.assertEqual(world.swa["modifiers"][CAPACITY], 4480)
            self.assertEqual(world.swa["capital"]["modifiers"][GENERATION], 4480)

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
