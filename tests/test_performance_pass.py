"""Behaviour parity and avoided work for the small 29 October performance pass.

Operation counts describe source traversal, not measured engine milliseconds.
Current installed Vanilla/CMF inputs are mandatory, as in the compatibility suite.
"""
from itertools import product
import unittest

from tests.test_zulu_court_politics import CourtRuntime
from tests.test_zulu_institutions_laws import ROOT, GAME, CMF, child, read, statements, tokens
from tools.check_override_inventory import find_object


def body(base, path, key, field, directive=None):
    return child(find_object(read(base, path), key, directive=directive), field)


def canonical_trigger(nodes):
    """Compare pure gates across reordering and one merged existential scan."""
    def combine(kind, items):
        flat = []
        for item in items:
            flat.extend(item[1:] if item[0] == kind else [item])
        return flat[0] if len(flat) == 1 else (kind, *sorted(flat, key=repr))
    def negate(item):
        if item[0] == 'NOT': return item[1]
        if item[0] in ('AND', 'OR'):
            return combine('OR' if item[0] == 'AND' else 'AND', [negate(v) for v in item[1:]])
        return ('NOT', item)
    terms = []
    for key, op, value in nodes:
        if key in ('OR', 'NOR'):
            item = combine('OR', [canonical_trigger([n]) for n in value])
            terms.append(negate(item) if key == 'NOR' else item)
        elif key in ('AND', 'NOT'):
            item = canonical_trigger(value)
            terms.append(negate(item) if key == 'NOT' else item)
        elif isinstance(value, list):
            item = canonical_trigger(value)
            if key == 'any_political_movement' and item[0] == 'OR':
                terms.append(combine('OR', [(key, op, term) for term in item[1:]]))
            else: terms.append((key, op, item))
        else: terms.append((key, op, value))
    return combine('AND', terms)


class Runtime(CourtRuntime):
    def __init__(self):
        super().__init__([])
        self.visits = 0
        self.checks = {}
        self.breakdown = []

    def ref(self, key, scope, prev=None):
        if key == 'acceptance_status_4': return 60
        return super().ref(key.strip('"'), scope, prev)

    def condition(self, nodes, scope, prev=None):
        # Short-circuit like the runtime; the shared court interpreter collects
        # every result and therefore cannot demonstrate avoided traversal.
        for key, op, value in nodes:
            self.checks[key] = self.checks.get(key, 0) + 1
            if key == 'AND': result = self.condition(value, scope, prev)
            elif key == 'OR': result = any(self.condition([n], scope, prev) for n in value)
            elif key in ('any_political_movement', 'any_scope_state'):
                items = scope['movements' if key == 'any_political_movement' else 'states']
                result = False
                for item in items:
                    self.visits += 1
                    if self.condition(value, item, scope):
                        result = True
                        break
            elif key.startswith('c:'): result = scope['id'] == key[2:]
            elif key == 'sb_uses_authored_zulu_movements': result = scope.get('authored', False) == (value == 'yes')
            elif key in ('country_has_voting_franchise', 'is_insurrectionary', 'is_in_government'):
                result = scope.get(key, False) == (value == 'yes')
            elif key == 'is_primary_culture_of':
                result = scope['id'] in self.ref(value, scope, prev)['primary_cultures']
            elif key == 'has_state_in_state_region': result = value in scope['regions']
            elif key == 'has_state_trait': result = value in scope.get('traits', set())
            elif key in ('is_pop_type', 'has_social_hierarchy', 'military_wage_level', 'strata', 'pop_employment_building_group', 'religion', 'culture', 'state_region', 'has_government_type') and not isinstance(value, list):
                result = scope.get(key) == value
            else: result = super().condition([(key, op, value)], scope, prev)
            if not result: return False
        return True

    def calc(self, nodes, scope, prev=None):
        result = 0
        for key, op, value in self.branches(nodes, scope, prev):
            if key == 'desc': continue
            if key in ('owner', 'leader', 'scope:interest_group'):
                target = self.ref(key, scope, prev)
                if target is not None: result += self.calc(value, target, scope)
                continue
            amount = self.calc(value, scope, prev) if isinstance(value, list) else self.ref(value, scope, prev)
            if key == 'value': result = amount
            elif key == 'add': result += amount
            elif key == 'subtract': result -= amount
            elif key == 'multiply': result *= amount
            elif key == 'divide': result /= amount
            elif key == 'min': result = max(result, amount)
            elif key == 'max': result = min(result, amount)
            else: raise AssertionError(key)
        for key, _, value in nodes:
            if key == 'desc': self.breakdown.append((value, result))
        return result


class PerformanceParityTests(unittest.TestCase):
    def absolutist(self, field):
        old = body(CMF, 'common/political_movements/ycom_00_ideological_movements.txt', 'movement_royalist_absolutist', field, 'REPLACE')
        new = body(ROOT, 'common/political_movements/zz_sb_absolutist_override.txt', 'movement_royalist_absolutist', field, 'REPLACE')
        # Restore the pre-pass SB-only exclusion to the unchanged dependency gate.
        if field == 'creation_trigger': old = old.replace('{', '{ sb_uses_authored_zulu_movements = no', 1)
        else: old = old.replace('OR = {', 'OR = { sb_uses_authored_zulu_movements = yes', 1)
        return statements(old), statements(new)

    def test_absolutist_creation_and_disband_truth_tables(self):
        gates = [self.absolutist(field) for field in ('creation_trigger', 'disband_trigger')]
        for tag, monarchy, voting, authored, bakufu, stamped, parliament, restored, mask in product(
                ('ZUL', 'FRA', 'JAP', 'AUS'), (False, True), (False, True), (False, True),
                (False, True), (False, True), (False, True), (False, True), range(8)):
            country = dict(id=tag, laws=set(), vars={}, authored=authored, country_has_voting_franchise=voting,
                           movements=[{'type': name} for i, name in enumerate(('movement_royalist_constitutional', 'movement_carlist', 'movement_miguelist')) if mask & (1 << i)])
            if monarchy: country['laws'].add('law_type:law_monarchy')
            if bakufu: country['laws'].add('law_type:law_bakufu')
            for flag, enabled in [('monarchy_stamped_out_var', stamped), ('king_in_parliament_possible', parliament), ('japan_restoration_complete', restored)]:
                if enabled: country['vars'][flag] = 1
            for old, new in gates:
                self.assertEqual(Runtime().condition(old, country), Runtime().condition(new, country), country)

    def test_absolutist_avoids_duplicate_or_ineligible_scans(self):
        old, new = self.absolutist('creation_trigger')
        country = dict(id='AUS', laws={'law_type:law_monarchy'}, vars={}, movements=[{'type': 'movement_liberal'}] * 12)
        a, b = Runtime(), Runtime()
        self.assertTrue(a.condition(old, country)); self.assertTrue(b.condition(new, country))
        self.assertEqual((24, 12), (a.visits, b.visits))
        country['id'] = 'FRA'
        a, b = Runtime(), Runtime()
        self.assertFalse(a.condition(old, country)); self.assertFalse(b.condition(new, country))
        self.assertEqual((24, 0), (a.visits, b.visits))

    def test_majority_only_reorders_neighbour_filter_and_preserves_scopes(self):
        old = body(CMF, 'common/political_movements/ycom_02_cultural_movement.txt', 'movement_cultural_majority', 'additional_radicalism_factors', 'REPLACE')
        new = body(ROOT, 'common/political_movements/zz_sb_cultural_majority_movement_override.txt', 'movement_cultural_majority', 'additional_radicalism_factors', 'REPLACE')
        old_filter, new_filter = child(old, 'any_political_movement'), child(new, 'any_political_movement')
        self.assertEqual(tokens(old.replace(old_filter, new_filter)), tokens(new))
        for kind, insurgent, same_majority, same_minority in product(('movement_cultural_majority', 'movement_cultural_minority', 'movement_liberal'), (False, True), (False, True), (False, True)):
            neighbour = {'primary_cultures': ['zulu' if same_majority else 'british']}
            neighbour['cultures'] = [{'id': c} for c in neighbour['primary_cultures']]
            movement = {'type': kind, 'is_insurrectionary': insurgent, 'culture': {'id': 'zulu' if same_minority else 'british'}}
            class CultureRuntime(Runtime):
                def condition(self, nodes, scope, prev=None):
                    if len(nodes) == 1 and nodes[0][0] == 'any_primary_culture':
                        self.checks['culture_scan'] = self.checks.get('culture_scan', 0) + 1
                        return any(self.condition(nodes[0][2], c, scope) for c in scope['cultures'])
                    return super().condition(nodes, scope, prev)
            a, b = CultureRuntime(), CultureRuntime()
            for rt in (a, b): rt.scopes['root'] = {'owner': {'primary_cultures': ['zulu']}}
            expected = insurgent and ((kind == 'movement_cultural_majority' and same_majority) or (kind == 'movement_cultural_minority' and same_minority))
            self.assertEqual(expected, a.condition(statements(old_filter), movement, neighbour))
            self.assertEqual(expected, b.condition(statements(new_filter), movement, neighbour))
            if not insurgent: self.assertEqual(0, b.checks.get('culture_scan', 0))

    def test_minority_neighbour_filter_preserves_optional_culture_and_skips_lookup(self):
        old = body(CMF, 'common/political_movements/ycom_02_cultural_movement.txt', 'movement_cultural_minority', 'additional_radicalism_factors', 'REPLACE')
        new = body(ROOT, 'common/political_movements/zz_sb_cultural_minority_movement_override.txt', 'movement_cultural_minority', 'additional_radicalism_factors', 'REPLACE')
        old_filter, new_filter = child(old, 'any_political_movement'), child(new, 'any_political_movement')
        self.assertEqual(tokens(old.replace(old_filter, new_filter)), tokens(new))
        for insurgent, culture in product((False, True), (None, 'zulu', 'british')):
            movement = {'is_insurrectionary': insurgent, 'culture': culture}
            class CultureRuntime(Runtime):
                def condition(self, nodes, scope, prev=None):
                    if len(nodes) == 1 and nodes[0][0] == 'culture':
                        self.checks['culture_lookup'] = self.checks.get('culture_lookup', 0) + 1
                        return scope['culture'] is None or scope['culture'] == self.scopes['root']['culture']
                    return super().condition(nodes, scope, prev)
            a, b = CultureRuntime(), CultureRuntime()
            for rt in (a, b): rt.scopes['root'] = {'culture': 'zulu'}
            self.assertEqual(a.condition(statements(old_filter), movement), b.condition(statements(new_filter), movement))
            if not insurgent: self.assertEqual(0, b.checks.get('culture_lookup', 0))

    def test_dynastic_challenge_preserves_gates_and_skips_ineligible_war_scans(self):
        from tests.test_zulu_contested_crown import court, ClaimantRuntime, TRIGGERS
        new = TRIGGERS['sb_court_dynastic_can_challenge']
        old = [node for node in new if node[0] != 'sb_court_dynastic_conflict_free']
        old.insert(2, ('sb_court_dynastic_conflict_free', '=', 'yes'))
        self.assertEqual(canonical_trigger(old), canonical_trigger(new))
        class CountRuntime(ClaimantRuntime):
            def condition(self, nodes, scope, prev=None):
                for node in nodes:
                    if node[0] == 'any_civil_war': self.war_scans += 1
                    if not super().condition([node], scope, prev): return False
                return True
        flags = (None, 'sb_court_dynastic_crisis_var', 'sb_court_dynastic_victory_cooldown_var',
                 'sb_court_accession_open_var', 'sb_court_action_open_var', 'sb_court_selecting_head_var')
        for prerogative, flag, war in product((-100, -50, -49.99, 0, 100), flags, (False, True)):
            rt, *_ = court()
            rt.__class__ = CountRuntime
            rt.country['vars']['sb_prerogative_var'] = prerogative
            if flag: rt.country['vars'][flag] = 1
            rt.country['wars'] = [{}] if war else []
            rt.war_scans = 0
            before = rt.condition(old, rt.country)
            before_scans = rt.war_scans
            rt.war_scans = 0
            after = rt.condition(new, rt.country)
            self.assertEqual(before, after)
            self.assertLessEqual(rt.war_scans, before_scans)
            if prerogative > -50 or flag: self.assertEqual(0, rt.war_scans)

    def test_armed_forces_scores_and_breakdown_match_native_plus_sb_modifier(self):
        old = body(GAME, 'common/interest_groups/00_armed_forces.txt', 'ig_armed_forces', 'pop_weight')
        # This was SB's only numerical delta before optimisation.
        anchor = '\t\t\t\t\tadd = 50\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\n\t\tadd = {\n\t\t\tdesc = "SAMURAI_TRADITIONS"'
        self.assertEqual(1, old.count(anchor))
        old = old.replace(anchor, anchor.replace('\t\t\t}\n\t\t}', '\t\t\t\tadd = owner.modifier:country_sb_aristocrats_armed_forces_attraction_add\n\t\t\t}\n\t\t}', 1))
        new = body(ROOT, 'common/interest_groups/zz_sb_armed_forces_override.txt', 'ig_armed_forces', 'pop_weight', 'REPLACE')
        old, new = statements(old), statements(new)
        for pop_type, wage, government, accepted, incorporated, army, imperial in product(
                ('soldiers', 'officers', 'aristocrats', 'laborers', 'bureaucrats'),
                ('very_low', 'low', 'medium', 'high', 'very_high'), (None, False, True),
                (False, True), (False, True), ('law_professional_army', 'law_peasant_levies', 'law_warrior_caste'), (0, 50)):
            country = {'id': 'ALK', 'laws': {'law_type:'+army, 'law_type:law_frontier_colonization'}, 'military_wage_level': wage,
                       'modifiers': {'age_of_caudillos_modifier': 1, 'country_sb_aristocrats_armed_forces_attraction_add': imperial}, 'has_government_type': 'gov_chartered_company'}
            pop = {'owner': country, 'is_pop_type': pop_type, 'pop_acceptance': 60 if accepted else 59,
                   'state': {'is_incorporated': incorporated}, 'culture': 'cu:japanese', 'religion': 'rel:sikh',
                   'strata': 'middle', 'pop_employment_building_group': 'bg_military_industry', 'pop_loyalist_fraction': .4, 'pop_radical_fraction': .2}
            a, b = Runtime(), Runtime()
            for rt in (a, b):
                if government is not None: rt.scopes['interest_group'] = {'is_in_government': government, 'leader': {'popularity': -40}, 'modifiers': {'interest_group_in_government_attraction_mult': .15}}
            self.assertAlmostEqual(a.calc(old, pop), b.calc(new, pop))
            self.assertEqual(a.breakdown, b.breakdown)
            self.assertLessEqual(b.checks.get('military_wage_level', 0), a.checks.get('military_wage_level', 0))

    def test_cape_region_guard_keeps_split_ownership_and_avoids_unrelated_states(self):
        source = read(ROOT, 'common/on_actions/sb_cape_on_action_handlers.txt')
        handler = find_object(source, 'sb_on_cape_monthly_pulse_country')
        new = statements(child(child(handler, 'trigger'), 'AND'))
        old = statements(child(child(child(handler, 'trigger'), 'AND'), 'any_scope_state'))
        old = [('any_scope_state', '=', old)]
        self.assertEqual(4, handler.count('has_state_in_state_region = STATE_EASTERN_CAPE'))
        for owns_region, trait in product((False, True), (False, True)):
            actor = {'states': [{'state_region': 's:STATE_TRANSVAAL'} for _ in range(200)], 'regions': set()}
            foreign = {'states': [{'state_region': 's:STATE_EASTERN_CAPE', 'traits': {'state_trait_sb_xhosa_resistance'}}]}
            if owns_region:
                actor['regions'].add('STATE_EASTERN_CAPE')
                actor['states'].append({'state_region': 's:STATE_EASTERN_CAPE', 'traits': {'state_trait_sb_xhosa_resistance'} if trait else set()})
            a, b = Runtime(), Runtime()
            a.scopes['root'] = b.scopes['root'] = foreign
            self.assertEqual(a.condition(old, actor), b.condition(new, actor))
            self.assertEqual(owns_region and trait, b.condition(new, actor))
            if not owns_region:
                self.assertEqual(200, a.visits)
                self.assertEqual(0, b.visits)

    def test_tribute_guard_admits_both_parties_only(self):
        handler = find_object(read(ROOT, 'common/on_actions/sb_ngi_tribute_on_action_handlers.txt'), 'sb_on_ngi_tribute_monthly_pulse_country')
        for tag in ('NGI', 'ZUL', 'NGN', 'CAP', 'FRA'):
            self.assertEqual(tag in ('NGI', 'ZUL'), Runtime().condition(statements(child(handler, 'trigger')), {'id': tag}))


if __name__ == '__main__':
    unittest.main()
