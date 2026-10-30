"""Source parity for the 30 October precision pass; visits are not engine timings.

Pre-pass fingerprints preserve complete predicates and native effect arguments.
The pulse interpreter records ordered native calls, not population-engine internals.
"""
from copy import deepcopy
from hashlib import sha256
from itertools import product
import unittest

from tests.test_performance_pass import Runtime
from tests.test_zulu_institutions_laws import ROOT, CMF, read, statements
from tools.check_override_inventory import find_object


CAPE = 'common/on_actions/sb_cape_on_action_handlers.txt'


def field(nodes, key):
    return next(value for name, _, value in nodes if name == key)


def definition(path, key, directive=None):
    return statements(find_object(read(ROOT, path), key, directive=directive))


def digest(value):
    return sha256(repr(value).encode()).hexdigest()


class PulseRuntime(Runtime):
    def __init__(self):
        super().__init__()
        self.operations = []
        self.pop_visits = 0
        protected = ('boer', 'british', 'xhosa', 'nama', 'san', 'tswana', 'cape_malay',
                     'cape_creole', 'griqua', 'oorlam', 'baster', 'german', 'gujarati')
        self.cultures = {
            'cu:'+name: {'id': 'cu:'+name,
                        'groups': {'heritage_group_european'} if name in ('boer', 'british', 'german') else set(),
                        'traits': {'heritage_british'} if name == 'british' else set()}
            for name in protected
        }
        self.religions = {name: {'traits': traits} for name, traits in (
            ('rel:protestant', set()), ('rel:catholic', set()), ('rel:sunni', {'heritage_islamic'}))}

    def ref(self, key, scope, prev=None):
        if key == 'ig:ig_rural_folk': return scope.get('rural_folk')
        if key == 'culture': return self.cultures[scope['culture']]
        if key == 'religion': return self.religions[scope['religion']]
        if key in self.cultures: return self.cultures[key]
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        for key, op, value in nodes:
            if key == 'country_has_primary_culture': result = value in scope['primary_cultures']
            elif key == 'has_ideology': result = value.removeprefix('ideology:') in scope['ideologies']
            elif key == 'has_discrimination_trait_group': result = value in scope['groups']
            elif key == 'has_discrimination_trait': result = value in scope['traits']
            elif key == 'any_scope_pop':
                result = False
                for pop in scope['pops']:
                    self.pop_visits += 1
                    if self.condition(value, pop, scope):
                        result = True
                        break
            else: result = super().condition([(key, op, value)], scope, prev)
            if not result: return False
        return True

    def execute(self, nodes, scope, prev=None):
        for key, op, value in self.branches(nodes, scope, prev):
            if key == 'ig:ig_rural_folk':
                target = self.ref(key, scope, prev)
                if target is not None: self.execute(value, target, scope)
            elif key in ('every_scope_state', 'every_scope_pop'):
                limit = field(value, 'limit')
                body = [node for node in value if node[0] != 'limit']
                for item in scope['states' if key == 'every_scope_state' else 'pops']:
                    if key == 'every_scope_pop': self.pop_visits += 1
                    if self.condition(limit, item, scope): self.execute(body, item, scope)
            elif key in ('add_ideology', 'remove_ideology'):
                self.operations.append((key, value))
                if key == 'add_ideology': scope['ideologies'].add(value)
                else: scope['ideologies'].remove(value)
            elif key == 'change_pop_culture':
                self.operations.append((key, scope['id'], tuple(value)))
            else: raise AssertionError(key)


class MajorityRuntime(Runtime):
    def ref(self, key, scope, prev=None):
        constants = {'suppression_base_value': 5, 'bolstering_base_value': 10, 'acceptance_status_5': 80}
        if key in constants: return constants[key]
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        for key, op, value in nodes:
            if key in ('is_being_suppressed', 'is_being_bolstered', 'culture_has_national_awakening'):
                result = scope.get(key, False) == (value == 'yes')
            elif key == 'has_technology_researched': result = value in scope.get('technologies', set())
            elif key == 'anzfp_is_active': result = self.anz_active == (value == 'yes')
            elif key == 'has_pop_culture': result = scope['culture']['id'] == value
            else: result = super().condition([(key, op, value)], scope, prev)
            if not result: return False
        return True


class PrecisionPerformanceTests(unittest.TestCase):
    def test_majority_scores_match_cmf_and_only_the_zero_radical_line_can_disappear(self):
        path = 'common/political_movements/zz_sb_cultural_majority_movement_override.txt'
        current = field(definition(path, 'movement_cultural_majority', 'REPLACE'), 'pop_support_weight')
        before = field(statements(find_object(
            read(CMF, 'common/political_movements/ycom_02_cultural_movement.txt'),
            'movement_cultural_majority', directive='REPLACE')), 'pop_support_weight')
        movement_sets = ([], ['movement_liberal'], ['movement_reactionary'], ['movement_fascist'],
                         ['movement_liberal', 'movement_fascist', 'movement_reactionary'])
        for fraction, movements, status, anz_active, pop_type in product(
                (-0.01, 0, 0.00001, 0.5, 1), movement_sets, (None, 'suppressed', 'bolstered'),
                (False, True), ('peasants', 'shopkeepers', 'officers')):
            country = {'movements': [{'type': name} for name in movements], 'technologies': {'pan-nationalism'}}
            pop = {'owner': country, 'is_pop_type': pop_type,
                   'strata': 'lower' if pop_type == 'peasants' else 'middle',
                   'state': {'is_incorporated': False}, 'pop_radical_fraction': fraction, 'pop_acceptance': 60,
                   'culture': {'id': 'british', 'culture_current_fervor': 55, 'culture_has_national_awakening': True}}
            a, b = MajorityRuntime(), MajorityRuntime()
            for runtime in (a, b):
                runtime.anz_active = anz_active
                if status is not None: runtime.scopes['political_movement'] = {'is_being_'+status: True}
            self.assertEqual(a.calc(before, pop), b.calc(current, pop))
            expected = [entry for entry in a.breakdown
                        if not (fraction == 0 and entry[0] == '"POP_RADICAL_MOVEMENT_LOSSES"')]
            self.assertEqual(expected, b.breakdown)
            if fraction == 0:
                self.assertEqual(0, b.visits)
                if movements: self.assertGreater(a.visits, 0)
            else: self.assertEqual(a.visits, b.visits)

    def test_nguni_keeps_every_requirement_and_avoids_safety_scan_when_ineligible(self):
        nodes = definition('common/decisions/sb_nguni_decisions.txt', 'sb_proclaim_nguni_nation')
        current = field(nodes, 'possible')
        self.assertEqual('914ae4c81e0f5159a83055ee33eb802a4bd16b02975a8141c81c196f8131d924',
                         digest(sorted(current, key=repr)))
        names = [field(v, 'text') if k == 'custom_tooltip' else k for k, _, v in current]
        old_order = ('is_at_war', 'sb_nguni_no_diplomatic_play_tt', 'sb_nguni_settlements_resolved_tt',
                     'has_technology_researched', 'sb_nguni_formation_lands_tt')
        # All possible truth values of the unchanged, pure top-level predicates.
        for outcomes in product((False, True), repeat=5):
            truth = dict(zip(old_order, outcomes))
            visits = []
            def evaluate(order):
                for name in order:
                    visits.append(name)
                    if not truth[name]: return False
                return True
            before = evaluate(old_order)
            visits.clear()
            self.assertEqual(before, evaluate(names))
            if not truth['has_technology_researched'] or not truth['sb_nguni_formation_lands_tt']:
                self.assertNotIn('sb_nguni_settlements_resolved_tt', visits)

    def test_frontier_law_only_reorders_the_three_existing_alternatives(self):
        nodes = definition('common/laws/00_sb_governance_principles.txt', 'law_frontier_colonization', 'REPLACE')
        alternatives = field(field(nodes, 'can_enact'), 'OR')
        self.assertEqual('6eeaa6a9d20b7b9bb322734b255ac8e1b1c13d9398917d09477e1773740c0f17',
                         digest(sorted(alternatives, key=repr)))
        boer = alternatives[0][2]
        for tag, culture in product(('TRN', 'ZPB', 'LYD', 'NAL', 'CAP', 'FRA'), ('boer', 'british')):
            actor = {'id': tag, 'primary_cultures': {'cu:'+culture}}
            self.assertEqual(culture == 'boer' and tag in ('TRN', 'ZPB', 'LYD', 'NAL'),
                             PulseRuntime().condition(boer, actor))

    def monthly(self):
        effects = field(definition(CAPE, 'sb_on_cape_monthly_pulse_country'), 'effect')
        current = next(node for node in effects if 'add_ideology' in repr(node)
                       and 'ideology_sb_settler_colonialist' in repr(node))
        before = deepcopy(current)
        limit = field(before[2], 'limit')
        limit.remove(next(node for node in limit if node[0] == 'ig:ig_rural_folk'))
        self.assertEqual('3377e82295aff9a303c78476e94f4c6477f25b87d44f297565291eb37d8d77cc', digest(before))
        return before, current

    def test_monthly_keeps_ideology_operations_and_skips_completed_repairs(self):
        before, current = self.monthly()
        isolationist, settler = 'ideology_isolationist', 'ideology_sb_settler_colonialist'
        for culture, region, ideologies in product(
                ('british', 'anglo_african', 'boer', 'french'),
                ('s:STATE_NATAL', 's:STATE_EASTERN_CAPE', 's:STATE_TRANSVAAL', 's:STATE_HOME_COUNTIES'),
                (None, set(), {isolationist}, {settler}, {isolationist, settler})):
            actor = {'id': 'CAP', 'primary_cultures': {'cu:'+culture},
                     'states': [{'state_region': region}],
                     'rural_folk': None if ideologies is None else {'ideologies': set(ideologies)}}
            a, b = PulseRuntime(), PulseRuntime()
            # A foreign root's qualifying state must not be borrowed by either body.
            a.scopes['root'] = b.scopes['root'] = {'id': 'GBR', 'states': [{'state_region': 's:STATE_CAPE_COLONY'}]}
            old_actor, new_actor = deepcopy(actor), deepcopy(actor)
            a.execute([before], old_actor)
            b.execute([current], new_actor)
            self.assertEqual(old_actor, new_actor)
            self.assertEqual(a.operations, b.operations)
            if ideologies == {settler}: self.assertEqual(0, b.visits)

    def test_yearly_filters_and_ordered_conversion_calls_are_unchanged(self):
        current = definition(CAPE, 'sb_on_cape_yearly_pulse_country')
        before = deepcopy(current)
        loops = field(before, 'effect')[0][2]
        for key, _, body in loops:
            if key == 'every_scope_state':
                pop_filter = field(field(body, 'every_scope_pop'), 'limit')
                field(body, 'limit').append(('any_scope_pop', '=', deepcopy(pop_filter)))
        self.assertEqual('448308d6d29c773d7849c74d5c33bb100e9e8ef9a949c51a1476e9591f6151da', digest(before))
        sample = PulseRuntime()
        pops = [{'id': str(i), 'culture': culture, 'religion': religion}
                for i, (culture, religion) in enumerate(product(sample.cultures, sample.religions))]
        for tag, population in product(('CAP', 'FRA'), ([], pops, list(reversed(pops)))):
            actor = {'id': tag, 'states': [
                {'state_region': region, 'pops': deepcopy(population)} for region in
                ('s:STATE_CAPE_COLONY', 's:STATE_NATAL', 's:STATE_EASTERN_CAPE', 's:STATE_HEREROLAND')]}
            a, b = PulseRuntime(), PulseRuntime()
            a.execute(field(before, 'effect'), deepcopy(actor))
            b.execute(field(current, 'effect'), deepcopy(actor))
            self.assertEqual(a.operations, b.operations)
            self.assertLessEqual(b.pop_visits, a.pop_visits)
            if tag == 'CAP' and population:
                self.assertTrue(b.operations)
                self.assertLess(b.pop_visits, a.pop_visits)
                self.assertTrue(all(('value', '=', '0.02') in call[2] for call in b.operations))


if __name__ == '__main__':
    unittest.main()
