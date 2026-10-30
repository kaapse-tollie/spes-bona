"""Court predicate-order parity; source operation counts are not engine timings."""
from copy import deepcopy
from random import Random
from unittest import TestCase
from unittest.mock import patch

from tests.test_zulu_court_politics import CourtRuntime, EFFECTS, character
from tests.test_zulu_institutions_laws import statements


HOUSE_FILTER = [
    ('var:sb_court_following_var', '=', 'scope:sb_court_candidate.var:sb_court_following_var'),
    ('sb_court_representative_eligible', '=', 'yes'),
]
REPRESENTATIVE_FILTER = [
    ('has_variable', '=', 'sb_court_representative_var'),
    ('has_variable', '=', 'sb_court_represented_weight_var'),
    ('sb_court_member_of_country', '=', 'yes'),
]
PREVIOUS_SHARED_HOUSE = statements('''previous_shared_house = {
    scope:sb_court_country = {
        ordered_in_list = {
            variable = sb_court_members
            limit = { sb_court_representative_eligible = yes var:sb_court_following_var = scope:sb_court_candidate.var:sb_court_following_var }
            order_by = sb_court_house_leadership_score
            position = 0
            set_variable = sb_court_representative_var
            set_variable = sb_court_house_leader_var
            save_scope_as = sb_court_house_head
        }
    }
    set_variable = { name = sb_court_house_leader_scope value = scope:sb_court_house_head }
}''')


def previous_filters(nodes):
    """Restore the pre-pass house selection and gates; leave other source intact."""
    result = []
    for key, op, value in nodes:
        if key == 'else' and isinstance(value, list) and any(n[0] == 'var:sb_court_house_leader_scope' for n in value):
            value = deepcopy(PREVIOUS_SHARED_HOUSE)
        elif key == 'limit' and value == HOUSE_FILTER:
            value = [value[1], value[0]]
        elif key == 'limit' and value == REPRESENTATIVE_FILTER:
            value = [value[2], *value[:2]]
        elif isinstance(value, list):
            value = previous_filters(value)
        result.append((key, op, value))
    return result


class CountingRuntime(CourtRuntime):
    def __init__(self, members):
        super().__init__(members)
        self.checks = {}
        self.sorts = 0

    def ref(self, key, scope, prev=None):
        result = super().ref(key, scope, prev)
        if key == 'prominence' and result is not None:
            return min(result, 100)
        return result

    def condition(self, nodes, scope, prev=None):
        # The existing arithmetic interpreter evaluates complete conjunctions.
        # Short-circuit here to count checks avoided by the shipped gate order.
        for node in nodes:
            self.checks[node[0]] = self.checks.get(node[0], 0) + 1
            if not super().condition([node], scope, prev):
                return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            if node[0] == 'ordered_in_list':
                self.sorts += 1
            super().effect([node], scope, prev)


def fixture(seed):
    rng = Random(seed)
    members = [character('king', 1, 50, 1, 1)]
    for name, template in [('mpande', 'ZUL_mpande_zulu'), ('gqugqu', 'ZUL_gqugqu_claimant')]:
        actor = character(name, 0, rng.randrange(10, 80), -1, 1)
        actor['template'] = template
        actor['vars']['sb_court_claimant_scope'] = actor
        members.append(actor)
    for index in range(36):
        actor = character(f'member-{index}', 2 + index // 3, rng.randrange(-10, 80),
                          rng.choice([-1, 0, 1]), rng.randrange(3),
                          age=rng.choice([15, 16, 40]), alive=index != 35,
                          agitator=index % 7 == 0)
        if actor['vars']['sb_court_endorsement_var'] == -1:
            actor['vars']['sb_court_claimant_scope'] = rng.choice(members[:3])
        if index % 2:
            actor['vars']['sb_court_successor_pledge_scope'] = rng.choice(members[1:3])
        if index % 4 == 0:
            actor['modifiers'] = {'sb_court_junior_status': 1}
        members.append(actor)
    rt = CountingRuntime(members)
    rt.country['ruler']['popularity'] = rng.randrange(-100, 101)
    for kind in ('royal', 'chiefly'):
        rt.country['movements'].append({'id': kind, 'type': f'movement_sb_zulu_{kind}',
                                       'owner': rt.country, 'modifiers': {}})
    foreign = {'id': 'REV', 'vars': {}, 'ruler': None}
    members[-1]['vars']['sb_court_home_scope'] = foreign
    members[-2]['owner'] = {'id': 'CAP', 'ruler': None}
    members[-3]['vars']['sb_court_retired_var'] = 1
    return rt


def projected_state(rt):
    def value(item):
        if isinstance(item, dict):
            return item['id']
        if isinstance(item, (list, tuple)):
            return [value(v) for v in item]
        if isinstance(item, set):
            return sorted(item)
        return item

    def record(scope):
        return {key: ({k: value(v) for k, v in item.items()} if key in ('vars', 'modifiers') else value(item))
                for key, item in scope.items() if key not in ('members', 'movements')}

    return (record(rt.country), [record(m) for m in rt.country['members']],
            [record(m) for m in rt.country['movements']],
            {key: value(item) for key, item in rt.scopes.items()})


class CourtPerformanceParity(TestCase):
    def execute_pair(self, old, new):
        overrides = {name: previous_filters(deepcopy(EFFECTS[name]))
                     for name in ('sb_court_calculate_backing', 'sb_court_calculate_coalitions')}
        self.assertNotEqual(overrides['sb_court_calculate_backing'], EFFECTS['sb_court_calculate_backing'])
        self.assertNotEqual(overrides['sb_court_calculate_coalitions'], EFFECTS['sb_court_calculate_coalitions'])
        with patch.dict(EFFECTS, overrides):
            old.backing()
        new.backing()
        self.assertEqual(projected_state(old), projected_state(new))
        self.assertLessEqual(new.sorts, old.sorts)

    def test_recalculation_preserves_every_projection_scope_and_native_choice(self):
        for seed in range(24):
            with self.subTest(seed=seed):
                old, new = fixture(seed), fixture(seed)
                self.execute_pair(old, new)
                # A second pass and live changes preserve leadership, penalties,
                # foreign homes, dead patrons and exit/re-entry behaviour.
                self.execute_pair(old, new)
                for rt in (old, new):
                    rt.country['members'][3]['prominence'] = 100
                    rt.country['members'][4]['age'] = 16
                    rt.country['members'][1]['alive'] = False
                    rt.country['vars'].pop('sb_institutions_active_var')
                self.execute_pair(old, new)
                for rt in (old, new):
                    rt.country['vars']['sb_institutions_active_var'] = 1
                    rt.country['members'][3]['prominence'] = 40
                    rt.country['members'][4]['prominence'] = 40
                self.execute_pair(old, new)

    def test_nested_membership_work_and_repeated_house_sorts_fall(self):
        old, new = fixture(0), fixture(0)
        self.execute_pair(old, new)
        before = old.checks['sb_court_representative_eligible']
        after = new.checks['sb_court_representative_eligible']
        self.assertLess(after, before / 3)
        self.assertLess(new.checks['sb_court_member_of_country'], old.checks['sb_court_member_of_country'])
        self.assertLess(new.sorts, old.sorts)
        self.assertEqual({}, new.scopes['root']['vars'])

    def test_singletons_ties_and_roster_duplicates_preserve_selection_and_order(self):
        for grouped in (False, True):
            for reverse, prominence in ((False, 40), (True, 40), (False, 115), (True, 115)):
                old, new = fixture(0), fixture(0)
                for rt in (old, new):
                    for index, member in enumerate(rt.country['members'][3:]):
                        member['age'] = 40
                        member['prominence'] = prominence
                        member.pop('modifiers', None)
                        member['vars']['sb_court_following_var'] = 2 + (index // 3 if grouped else index)
                    if reverse:
                        rt.country['members'].reverse()
                    rt.country['members'].append(rt.country['members'][5])
                self.execute_pair(old, new)
                self.execute_pair(old, new)
