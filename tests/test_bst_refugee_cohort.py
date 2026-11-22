"""Execute the shipped refugee transaction; native economic recovery remains DP's check.

Population primitive contracts are pinned by the 1.14.5 native evidence:
filtered removal has a remainder pass, creation accepts an initial worker share,
and culture restoration may merge into residents. This fixture does not model
native qualifications, political support, mortality statistics or employment.
"""
from pathlib import Path
import math
import unittest

from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import extract_top_level_blocks, find_object
from tools.validate import find_game_root

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "common/scripted_effects/sb_bst_refugee_effects.txt").read_text(encoding="utf-8-sig")
EFFECTS = {key: statements(body) for key, body in extract_top_level_blocks(SOURCE).items()}
RECEIPT = "sb_bst_mountain_refugees_transferred_var"


def fields(nodes):
    return {key: value for key, _, value in nodes}


def people(pop):
    return pop["workers"] + pop["dependants"]


class RefugeRuntime:
    def __init__(self, size=9000, profession="laborers", religion="animist"):
        self.bst = {"tag": "BST", "vars": {}, "mountains_only": True, "slavery": False}
        self.ora = {"tag": "ORA", "vars": {}, "frontier_actor": True}
        self.foreign_root = {"tag": "GBR", "vars": {}}
        self.source = {"region": "s:STATE_VRYSTAAT", "owner": self.ora, "pops": []}
        self.destination = {"region": "s:STATE_DRAKENSBERG", "owner": self.bst, "pops": []}
        self.scopes = {"root": self.foreign_root}
        self.donor = self.pop(self.source, size, profession, religion, ratio=.25)
        self.donor.update(wealth=6, literacy_rate=.17)
        self.arrivals, self.operations, self.setters = [], [], []
        self.on_receipt = None

    @staticmethod
    def pop(state, size, profession="laborers", religion="animist", culture="sotho", ratio=.25):
        worker_count = math.floor(size * ratio)
        pop = dict(state=state, workers=worker_count, dependants=size-worker_count,
                   profession=profession, religion=religion, culture=culture,
                   wealth=3, literacy_rate=.05)
        state["pops"].append(pop)
        return pop

    def ref(self, key, scope):
        if key == "c:BST": return self.bst
        if key == "s:STATE_DRAKENSBERG.region_state:BST":
            return self.destination if self.destination["owner"] is self.bst else None
        if key.startswith("scope:"): return self.scopes.get(key[6:])
        if key == "total_size": return people(scope)
        if key in scope: return scope[key]
        try: return float(key)
        except ValueError: raise AssertionError(("unsupported reference", key))

    def condition(self, nodes, scope):
        for key, op, value in nodes:
            if key == "NOT": result = not any(self.condition([n], scope) for n in value)
            elif key == "exists": result = self.ref(value, scope) is not None
            elif key == "has_variable": result = value in scope["vars"]
            elif key == "has_slavery": result = scope["slavery"] == (value == "yes")
            elif key == "any_scope_pop":
                result = any(self.condition(value, p) for p in scope["pops"])
            elif key == "culture": result = scope["culture"] == value.removeprefix("cu:")
            elif key == "religion": result = scope["religion"] == value.removeprefix("rel:")
            elif key == "is_pop_type": result = scope["profession"] == value
            elif key == "state_region": result = scope["region"] == value
            elif key == "sb_bst_oranje_frontier_actor":
                result = scope.get("frontier_actor", False) == (value == "yes")
            elif key == "sb_bst_controls_only_drakensberg":
                result = scope.get("mountains_only", False) == (value == "yes")
            elif isinstance(value, list):
                target = self.ref(key, scope)
                result = target is not None and self.condition(value, target)
            else:
                left, right = self.ref(key, scope), self.ref(value, scope)
                result = left >= right if op == ">=" else left is right
            if not result: return False
        return True

    def effect(self, nodes, scope):
        matched = False
        for key, op, value in nodes:
            if key in ("if", "else_if", "else"):
                if key == "if": matched = False
                if not matched and self.condition(fields(value).get("limit", []), scope):
                    matched = True
                    self.effect([n for n in value if n[0] != "limit"], scope)
            elif key in EFFECTS:
                body = EFFECTS[key]
                if isinstance(value, list):
                    params = fields(value)
                    def expand(x):
                        if isinstance(x, list):
                            return [(expand(k), operator, expand(v)) for k, operator, v in x]
                        for name, item in params.items(): x = x.replace("$"+name+"$", item)
                        return x
                    body = expand(body)
                self.effect(body, scope)
            elif key == "switch":
                trigger = fields(value)["trigger"]
                for case, _, branch in value:
                    if case != "trigger" and self.condition([(trigger, "=", case)], scope):
                        self.effect(branch, scope)
                        break
            elif key == "save_temporary_scope_as": self.scopes[value] = scope
            elif key == "save_scope_value_as":
                f = fields(value)
                self.scopes[f["name"]] = self.ref(f["value"], scope)
            elif key == "set_variable":
                scope["vars"][value] = True
                if self.on_receipt:
                    callback, self.on_receipt = self.on_receipt, None
                    callback()
            elif key == "every_scope_pop":
                for pop in list(scope["pops"]):
                    if self.condition(fields(value).get("limit", []), pop):
                        self.effect([n for n in value if n[0] != "limit"], pop)
            elif key == "kill_population_in_state":
                f = fields(value)
                assert set(f) == {"value", "culture", "religion", "pop_type"}
                selected = [p for p in scope["pops"]
                            if p["culture"] == f["culture"].removeprefix("cu:")
                            and p["religion"] == f["religion"].removeprefix("rel:")
                            and p["profession"] == f["pop_type"]]
                size, total = int(f["value"]), sum(map(people, selected))
                assert size <= total
                portions = [size * people(p) // total for p in selected]
                left = size - sum(portions)
                for index, pop in enumerate(selected):
                    extra = min(left, people(pop) - portions[index])
                    portions[index] += extra
                    left -= extra
                for pop, count in zip(selected, portions):
                    workers = count * pop["workers"] // people(pop)
                    pop["workers"] -= workers
                    pop["dependants"] -= count-workers
                    if not people(pop): scope["pops"].remove(pop)
                self.operations.append(("debit", size))
            elif key == "create_pop":
                f = fields(value)
                assert set(f) == {"culture", "religion", "pop_type", "size", "working_adult_ratio"}
                self.pop(scope, int(f["size"]), f["pop_type"], f["religion"], f["culture"],
                         float(f["working_adult_ratio"]))
                self.operations.append(("create", int(f["size"])))
            elif key in ("set_pop_wealth", "set_pop_literacy"):
                f = fields(value)
                if key == "set_pop_wealth":
                    assert f["update_loyalties"] == "no"
                distribution = f["wealth_distribution" if key == "set_pop_wealth" else "literacy_rate"]
                amount = self.ref(fields(distribution)["value"], scope)
                self.setters.append((scope, key, scope["culture"]))
                scope["wealth" if key == "set_pop_wealth" else "literacy_rate"] = amount
            elif key == "change_pop_culture":
                f = fields(value)
                assert float(f["value"]) == 1
                target = f["target"].removeprefix("cu:")
                self.arrivals.append({k: v for k, v in scope.items() if k != "state"})
                state = scope["state"]
                resident = next((p for p in state["pops"] if p is not scope
                                 and p["culture"] == target
                                 and p["religion"] == scope["religion"]
                                 and p["profession"] == scope["profession"]), None)
                scope["culture"] = target
                if resident:
                    # Simulate immediate merge for setter-isolation/headcount tests.
                    # Attribute weighting is deliberately not asserted as engine parity.
                    resident["workers"] += scope["workers"]
                    resident["dependants"] += scope["dependants"]
                    state["pops"].remove(scope)
                self.operations.append(("restore_culture", target))
            else:
                target = self.ref(key, scope)
                assert target is not None, key
                self.effect(value, target)

    def run(self):
        self.effect(EFFECTS["sb_bst_transfer_mountain_refugees"], self.donor)

    def total(self):
        return sum(people(p) for s in (self.source, self.destination) for p in s["pops"])


class MountainRefugeTransferTests(unittest.TestCase):
    def test_balanced_arrivals_preserve_selected_donor_metadata(self):
        for original_size in (5000, 5001, 9000, 100003):
            rt = RefugeRuntime(original_size)
            before = rt.total()
            rt.run()
            self.assertEqual(before, rt.total())
            self.assertEqual([("debit",5000),("create",5000),("restore_culture","sotho")], rt.operations)
            self.assertEqual((2500,2500), (rt.arrivals[0]["workers"],rt.arrivals[0]["dependants"]))
            self.assertEqual((6,.17), (rt.arrivals[0]["wealth"],rt.arrivals[0]["literacy_rate"]))
            self.assertEqual({}, rt.foreign_root["vars"])
            self.assertIn(RECEIPT, rt.bst["vars"])

    def test_matching_source_group_rounding_and_unrelated_pops(self):
        rt = RefugeRuntime(5001, religion="protestant")
        second = rt.pop(rt.source, 3127, religion="protestant")
        unrelated = [rt.pop(rt.source, 777, religion="animist"),
                     rt.pop(rt.source, 888, profession="farmers", religion="protestant"),
                     rt.pop(rt.source, 999, culture="zulu", religion="protestant")]
        before, pool = rt.total(), people(rt.donor)+people(second)
        rt.run()
        self.assertEqual(before,rt.total())
        self.assertEqual(pool-5000,people(rt.donor)+people(second))
        self.assertEqual([777,888,999], list(map(people,unrelated)))
        self.assertEqual("protestant", rt.arrivals[0]["religion"])

    def test_existing_residents_never_receive_the_cohort_setters(self):
        rt = RefugeRuntime()
        resident = rt.pop(rt.destination,10000)
        resident.update(wealth=12,literacy_rate=.8)
        rt.run()
        self.assertEqual((5000,10000),(resident["workers"],resident["dependants"]))
        self.assertTrue(all(pop is not resident for pop, _, _ in rt.setters))
        self.assertTrue(all(culture != "sotho" for _, _, culture in rt.setters))
        self.assertFalse(any(p["culture"] != "sotho" for p in rt.destination["pops"]))
        # The merged 15k Pop is one-third workers, while the new 5k cohort was half.
        self.assertAlmostEqual(1/3,resident["workers"]/people(resident))

    def test_staging_fallback_and_collision_failure_do_not_touch_residents(self):
        for occupied, expected in (([], "promethean"),(["promethean"],"ainu"),
                                   (["promethean","ainu"],"maori"),
                                   (["promethean","ainu","maori"],None)):
            rt=RefugeRuntime()
            residents=[rt.pop(rt.destination,101,culture=c) for c in occupied]
            before=rt.total()
            rt.run()
            self.assertEqual(before,rt.total())
            self.assertEqual([101]*len(residents),list(map(people,residents)))
            if expected:
                self.assertEqual(expected,rt.arrivals[0]["culture"])
            else:
                self.assertEqual([],rt.operations)
                self.assertNotIn(RECEIPT,rt.bst["vars"])

    def test_repeated_or_reentrant_delivery_cannot_duplicate_refugees(self):
        rt=RefugeRuntime(20000)
        before=rt.total()
        rt.on_receipt=rt.run
        rt.run(); rt.run()
        self.assertEqual(before,rt.total())
        self.assertEqual(1,len(rt.arrivals))
        self.assertEqual(15000,people(rt.donor))

    def test_invalid_or_changed_participants_are_inert(self):
        for failure in ("too_small","wrong_culture","wrong_region","wrong_actor",
                        "destination_lost","retreat_invalid","bst_missing"):
            rt=RefugeRuntime(4999 if failure=="too_small" else 9000)
            if failure=="wrong_culture": rt.donor["culture"]="zulu"
            if failure=="wrong_region": rt.source["region"]="s:STATE_NATAL"
            if failure=="wrong_actor": rt.ora["frontier_actor"]=False
            if failure=="destination_lost": rt.destination["owner"]=rt.ora
            if failure=="retreat_invalid": rt.bst["mountains_only"]=False
            if failure=="bst_missing": rt.bst=None
            before=rt.total()
            rt.run()
            self.assertEqual(before,rt.total(),failure)
            self.assertEqual([],rt.operations,failure)

    def test_dispatch_covers_installed_professions_and_religions(self):
        game=find_game_root(None)
        self.assertIsNotNone(game)
        names={}
        for folder in ("pop_types","religions"):
            keys=set()
            for path in (game/"common"/folder).glob("*.txt"):
                keys.update(extract_top_level_blocks(path.read_text(encoding="utf-8-sig")))
            names[folder]=keys
        for profession in names["pop_types"]:
            for religion in names["religions"]:
                with self.subTest(profession=profession,religion=religion):
                    rt=RefugeRuntime(profession=profession,religion=religion)
                    rt.run()
                    self.assertEqual(1,len(rt.arrivals))
                    expected = "laborers" if profession in ("peasants", "slaves") else profession
                    self.assertEqual((expected,religion),
                                     (rt.arrivals[0]["profession"],rt.arrivals[0]["religion"]))

    def test_profession_conversion_matches_native_move(self):
        for profession in ("peasants", "slaves", "soldiers", "farmers"):
            for slavery in (False, True):
                rt=RefugeRuntime(profession=profession)
                rt.bst["slavery"]=slavery
                unrelated=rt.pop(rt.source,7000,profession="laborers")
                rt.run()
                expected=("laborers" if profession=="peasants" or
                          (profession=="slaves" and not slavery) else profession)
                self.assertEqual(expected,rt.arrivals[0]["profession"])
                self.assertEqual(4000,people(rt.donor))
                self.assertEqual(7000,people(unrelated))
                self.assertEqual((2500,2500),(rt.arrivals[0]["workers"],rt.arrivals[0]["dependants"]))

    def test_retreat_calls_replacement_inside_hidden_effect(self):
        source=(ROOT/"events/sb_bst_frontier_events.txt").read_text(encoding="utf-8-sig")
        event=statements(find_object(source,"sb_bst_frontier.020"))
        option=next(v for k,_,v in event if k=="option")
        actor=next(v for k,_,v in option if k=="scope:sb_bst_current_oranje_actor")
        hidden=fields(actor)["hidden_effect"]
        state=fields(hidden)["random_scope_state"]
        chosen=fields(state)["ordered_scope_pop"]
        self.assertIn(("sb_bst_transfer_mountain_refugees","=","yes"),chosen)
        self.assertFalse(any(k=="move_partial_pop" for k,_,_ in chosen))


if __name__ == "__main__":
    unittest.main()

