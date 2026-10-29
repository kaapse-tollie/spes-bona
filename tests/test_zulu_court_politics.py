"""Execute court arithmetic/selection from source; native coup/war delivery remains DP's check."""
from pathlib import Path
import hashlib
import json
import math
import re
import unittest
from tests.test_zulu_institutions_laws import statements, child as script_child
from tools.check_override_inventory import extract_top_level_blocks

ROOT = Path(__file__).resolve().parents[1]
GAME = Path.home() / 'Library/Application Support/Steam/steamapps/common/Victoria 3/game'


def definitions(path):
    return {k: statements(v) for k, v in extract_top_level_blocks((ROOT/path).read_text(encoding='utf-8-sig')).items()}


VALUES = definitions('common/script_values/sb_court_politics_values.txt')
VALUES.update(definitions('common/script_values/sb_court_dynastic_values.txt'))
EFFECTS = definitions('common/scripted_effects/sb_court_politics_effects.txt')
ACTIONS = definitions('common/scripted_effects/sb_court_actions_effects.txt')
for _file in ('coalitions', 'succession', 'rivals', 'episodes', 'cast', 'allegiance', 'concession', 'frontier', 'dynastic', 'force_split'):
    EFFECTS.update(definitions(f'common/scripted_effects/sb_court_{_file}_effects.txt'))
TRIGGERS = definitions('common/scripted_triggers/sb_court_politics_triggers.txt')
TRIGGERS.update(definitions('common/scripted_triggers/sb_court_episode_triggers.txt'))
TRIGGERS.update(definitions('common/scripted_triggers/sb_court_dynastic_triggers.txt'))
TRIGGERS['sb_institutions_profile_country'] = definitions('common/scripted_triggers/sb_institutions_triggers.txt')['sb_institutions_profile_country']
TRIGGERS['sb_is_zulu_dynasty_country'] = definitions('common/scripted_triggers/sb_firearms_triggers.txt')['sb_is_zulu_dynasty_country']
COURT_MODIFIERS = definitions('common/static_modifiers/sb_court_modifiers.txt')
TRAITS = extract_top_level_blocks((ROOT/'common/character_traits/sb_court_allegiance_traits.txt').read_text(encoding='utf-8-sig'))
TRAIT_MODIFIERS = {name:statements(script_child(body,'character_modifier')) for name,body in TRAITS.items() if 'character_modifier' in body}


def character(identity, following, prominence, endorsement=0, alignment=0, age=35, alive=True, agitator=False):
    return {'id': identity, 'prominence': prominence, 'popularity': 0, 'age': age, 'alive': alive, 'agitator': agitator,
            'vars': {'sb_court_registered_var': 1, 'sb_court_following_var': following,
                     'sb_court_endorsement_var': endorsement, 'sb_court_alignment_var': alignment}}


class CourtRuntime:
    """Narrow interpreter: field names/arithmetic/order/limits all come from shipped scripts."""
    def __init__(self, members):
        self.country = {'id': 'ZUL', 'vars': {'sb_institutions_active_var': 1}, 'members': members, 'movements': []}
        self.country['ruler'] = members[0] if members else None
        self.scopes = {'root': {'id': 'GBR', 'vars': {}}}
        for m in members:
            m['owner'] = self.country
            m['vars']['sb_court_home_scope'] = self.country

    def ref(self, key, scope, prev=None):
        if scope is None: return None
        if key == 'this': return scope
        if key.startswith('this.'): return self.ref(key[5:], scope, prev)
        if key.startswith('root.'): return self.ref(key[5:], self.scopes['root'])
        if key == 'prev': return prev
        if key == 'owner': return scope.get('owner')
        if key == 'ruler': return scope.get('ruler')
        if key.startswith('prev.'): return self.ref(key[5:], prev)
        if key.startswith('owner.'): return self.ref(key[6:], scope.get('owner'))
        if key.startswith('scope:'):
            name, _, tail = key[6:].partition('.')
            found = self.scopes.get(name)
            return self.ref(tail, found) if tail and found else found
        if key.startswith('modifier:'): return scope.get('modifiers', {}).get(key[9:], 0)
        if key.startswith('var:'):
            name, _, tail = key[4:].partition('.')
            found = scope['vars'].get(name)
            return self.ref(tail, found, scope) if tail and found is not None else found
        if key in VALUES: return self.calc(VALUES[key], scope, prev)
        if key == 'prominence' and key in scope:
            bonus = 0
            for name,multiplier in scope.get('modifiers',{}).items():
                for modifier,_,amount in COURT_MODIFIERS.get(name,[]):
                    if modifier == 'character_prominence_add': bonus += float(amount)*multiplier
            for name in scope.get('traits',set()):
                for modifier,_,amount in TRAIT_MODIFIERS.get(name,[]):
                    if modifier == 'character_prominence_add': bonus += float(amount)
            return scope[key] + bonus
        if scope is not None and key in scope: return scope[key]
        try: return float(key)
        except ValueError:
            if '.' in key:
                head, tail = key.split('.', 1)
                target = self.ref(head, scope, prev)
                return self.ref(tail, target, scope) if target is not None else None
            return None

    def condition(self, nodes, scope, prev=None):
        results = []
        for key, op, value in nodes:
            if key == 'trigger_if':
                fields = {k:v for k,_,v in value}
                r = not self.condition(fields.get('limit', []), scope, prev) or self.condition([n for n in value if n[0] != 'limit'], scope, prev)
            elif key == 'custom_tooltip': r = self.condition([n for n in value if n[0] != 'text'], scope, prev)
            elif key == 'NOT': r = not self.condition(value, scope, prev)
            elif key == 'NOR': r = not any(self.condition([n], scope, prev) for n in value)
            elif key == 'OR': r = any(self.condition([n], scope, prev) for n in value)
            elif key == 'AND': r = self.condition(value, scope, prev)
            elif key in TRIGGERS: r = self.condition(TRIGGERS[key], scope, prev) == (value == 'yes')
            elif key == 'exists': r = self.ref(value, scope, prev) is not None
            elif key == 'any_scope_state': r = any(self.condition(value, state, scope) for state in scope['states'])
            elif key == 'is_incorporated': r = scope['is_incorporated'] == (value == 'yes')
            elif key == 'always': r = value == 'yes'
            elif key == 'is_adult': r = (scope.get('age', 30) >= 16) == (value == 'yes')
            elif key in ('is_in_void', 'is_in_exile_pool'): r = scope.get(key, False) == (value == 'yes')
            elif key in ('has_law', 'has_law_or_variant'): r = value in scope.get('laws', set())
            elif key == 'is_target_in_variable_list':
                f = dict((k,v) for k,_,v in value)
                r = any(m is self.ref(f['target'], scope, prev) for m in scope.get('members' if f['name'] == 'sb_court_members' else f['name'], []))
            elif key == 'any_in_list':
                f = dict((k,v) for k,_,v in value)
                r = any(self.condition([n for n in value if n[0] != 'variable'], m, scope) for m in scope.get('members' if f['variable'] == 'sb_court_members' else f['variable'], []))
            elif key == 'country_definition': r = scope.get('id') == value.removeprefix('cd:')
            elif key == 'has_variable': r = value in scope['vars']
            elif key == 'has_modifier': r = value in scope.get('modifiers', {})
            elif key == 'has_trait': r = value in scope.get('traits', set())
            elif key == 'has_ideology': r = scope.get('ideology') == value.removeprefix('ideology:')
            elif key == 'is_interest_group_type': r = (scope if isinstance(scope, str) else scope.get('type')) == value
            elif key == 'has_journal_entry': r = value in scope.get('journal_entries', set())
            elif key == 'has_template': r = scope.get('template') == value
            elif key == 'is_ruler_of_own_country': r = (scope is scope['owner'].get('ruler')) == (value == 'yes')
            elif key == 'is_character_alive': r = scope['alive'] == (value == 'yes')
            elif key == 'has_role_of_type': r = scope.get(value, False)
            elif key == 'is_political_movement_type': r = scope['type'] == value
            elif isinstance(value, list):
                target = self.ref(key, scope, prev)
                r = target is not None and self.condition(value, target, scope)
            else:
                a = self.ref(key, scope, prev); b = self.ref(value, scope, prev)
                if a is None: r = False
                elif isinstance(a, dict): r = a is b
                else: r = {'=': a == b, '?=': a == b, '>=': a >= b, '<=': a <= b, '<': a < b, '>': a > b}[op]
            results.append(r)
        return all(results)

    def branches(self, nodes, scope, prev=None):
        matched = False
        for key, op, value in nodes:
            if key in ('if', 'else_if', 'else'):
                if key == 'if': matched = False
                if matched: continue
                limit = next((v for k, _, v in value if k == 'limit'), [])
                if self.condition(limit, scope, prev):
                    matched = True
                    yield from self.branches([n for n in value if n[0] != 'limit'], scope, prev)
            else: yield key, op, value

    def calc(self, nodes, scope, prev=None):
        result = 0
        for key, op, value in self.branches(nodes, scope, prev):
            if key == 'desc': continue
            if key == 'round':
                result = math.floor(result + 0.5)
                continue
            if key == 'save_temporary_scope_as':
                self.scopes[value] = scope
                continue
            if key in ('ruler', 'owner') or key.startswith('var:'):
                target = self.ref(key, scope, prev)
                if target is not None: result += self.calc(value, target, scope)
                continue
            if key == 'every_political_movement':
                limit = next(v for k, _, v in value if k == 'limit')
                for m in scope['movements']:
                    if self.condition(limit, m, scope): result += self.calc([n for n in value if n[0] != 'limit'], m, scope)
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
        return result

    def effect(self, nodes, scope, prev=None):
        for key, op, value in self.branches(nodes, scope, prev):
            if key == 'hidden_effect': self.effect(value, scope, prev)
            elif key in ACTIONS or key in EFFECTS:
                body = ACTIONS.get(key, EFFECTS.get(key))
                if isinstance(value, list):
                    params = dict((k, v) for k, _, v in value)
                    def subst(x):
                        if isinstance(x, list): return [(subst(k), op, subst(v)) for k, op, v in x]
                        for param, val in params.items(): x = x.replace('$'+param+'$', val)
                        return x
                    body = subst(body)
                self.effect(body, scope, prev)
            elif key == 'save_scope_as': self.scopes[value] = scope
            elif key == 'set_variable':
                if isinstance(value, str): scope['vars'][value] = 1
                else:
                    fields = {k:v for k, _, v in value}
                    scope['vars'][fields['name']] = self.calc(fields['value'], scope, prev) if isinstance(fields.get('value'), list) else self.ref(fields.get('value', '1'), scope, prev)
            elif key == 'change_variable':
                fields = {k:v for k, _, v in value}
                scope['vars'][fields['name']] += self.ref(fields['add'], scope, prev)
            elif key == 'clear_variable_list': scope['members' if value == 'sb_court_members' else value] = []
            elif key == 'add_to_variable_list':
                fields = dict((k,v) for k,_,v in value)
                items = scope.setdefault('members' if fields['name'] == 'sb_court_members' else fields['name'], [])
                target = self.ref(fields['target'], scope, prev)
                if all(item is not target for item in items): items.append(target)
            elif key == 'remove_variable': scope['vars'].pop(value, None)
            elif key == 'add_trait':
                traits = scope.setdefault('traits', set())
                replaced = re.search(r'replace\s*=\s*\{([^}]+)\}', TRAITS[value]).group(1).split()
                traits.difference_update(replaced)
                traits.add(value)
            elif key == 'remove_trait':scope.setdefault('traits',set()).discard(value)
            elif key == 'every_scope_character':
                limit = next((v for k,_,v in value if k == 'limit'),[])
                for m in list(scope.get('characters',scope.get('members',[]))):
                    if self.condition(limit,m,scope):
                        self.effect([n for n in value if n[0]!='limit'],m,scope)
            elif key in ('every_in_list', 'ordered_in_list'):
                limit = next((v for k, _, v in value if k == 'limit'), [])
                list_name = next(v for k,_,v in value if k == 'variable')
                selected = [m for m in scope.get('members' if list_name == 'sb_court_members' else list_name, []) if self.condition(limit, m, scope)]
                if key == 'ordered_in_list':
                    order = next(v for k, _, v in value if k == 'order_by')
                    fields = {k:v for k, _, v in value}
                    selected = sorted(selected, key=lambda m:self.calc(order, m, scope) if isinstance(order,list) else self.ref(order, m, scope), reverse=True)
                    if 'position' in fields:
                        position = int(fields['position'])
                        if selected and position >= len(selected): raise AssertionError('out-of-range position would cap at the last candidate')
                        selected = selected[position:position+1]
                    elif 'max' in fields:
                        maximum = int(fields['max'])
                        if maximum > len(selected) and fields.get('check_range_bounds') != 'no': raise AssertionError('unbounded ordered list')
                        selected = selected[:maximum]
                for m in selected: self.effect([n for n in value if n[0] not in ('variable','limit','order_by','position','max','check_range_bounds')],m,scope)
            elif key == 'every_political_movement':
                limit = next(v for k, _, v in value if k == 'limit')
                for m in scope['movements']:
                    if self.condition(limit,m,scope): self.effect([n for n in value if n[0]!='limit'],m,scope)
            elif key.startswith(('scope:', 'var:', 'ig:')) or key in ('owner', 'ruler'):
                target = self.ref(key, scope, prev)
                if target is not None: self.effect(value, target, scope)
            elif key == 'add_treasury': scope['gold_reserves'] += self.ref(value, scope, prev)
            elif key == 'set_heir': scope['heir'] = self.ref(value, scope, prev)
            elif key == 'set_ideology': scope['ideology'] = value.removeprefix('ideology:')
            elif key == 'set_character_as_ruler': scope['owner']['ruler'] = scope
            elif key == 'cleanup_ruler_character_roles': pass
            elif key == 'resign_and_retire': scope['retired'] = True
            elif key == 'kill_character': scope['alive'] = False
            elif key == 'activate_law': scope.setdefault('laws', set()).add(value)
            elif key == 'remove_modifier':
                if value not in scope.get('modifiers', {}): raise AssertionError(('absent modifier', value))
                del scope['modifiers'][value]
            elif key == 'trigger_event': scope.setdefault('events', []).append(dict((k, v) for k, _, v in value)['id'])
            elif key == 'add_modifier':
                f={'name': value} if isinstance(value, str) else {k:v for k,_,v in value}
                scope.setdefault('modifiers',{})[f['name']]=self.ref(f.get('multiplier','1'),scope,prev)
            else: raise AssertionError(key)

    def backing(self): self.effect(EFFECTS['sb_court_calculate_backing'],self.country)

    def roster_shown(self, name, actor):
        self.scopes.update(sb_court_country=self.country, sb_court_character=actor)
        gui = extract_top_level_blocks((ROOT/'common/scripted_guis/sb_court_roster.txt').read_text(encoding='utf-8-sig'))[name]
        assert 'scope = country' in gui
        return self.condition(statements(script_child(gui, 'is_shown')), self.country)


class CourtBackingTests(unittest.TestCase):
    def test_allegiance_traits_follow_each_axis_without_changing_ideology(self):
        actor = character('chief', 2, 10)
        actor.update(ideology='ideology_traditionalist', traits={'brave'})
        runtime = CourtRuntime([character('king',1,20,1,1),actor])
        for alignment, align_name in ((1, 'royal'), (2, 'chiefly'), (0, 'neutral'), (1, 'royal')):
            for endorsement, end_name in ((1, 'incumbent'), (-1, 'claimant'), (0, 'uncommitted')):
                actor['vars'].update(sb_court_alignment_var=alignment, sb_court_endorsement_var=endorsement)
                runtime.backing()
                expected = {'brave', f'sb_court_alignment_{align_name}_trait', f'sb_court_endorsement_{end_name}_trait'}
                self.assertEqual(expected, actor['traits'])
                self.assertEqual('ideology_traditionalist', actor['ideology'])
                runtime.backing()
                self.assertEqual(expected, actor['traits'])
        for helper, name in (('sb_court_align_royal', 'royal'), ('sb_court_align_chiefly', 'chiefly')):
            runtime.effect(EFFECTS[helper], actor)
            self.assertIn(f'sb_court_alignment_{name}_trait', actor['traits'])
            self.assertEqual('ideology_traditionalist', actor['ideology'])

    def test_claimant_card_distinguishes_self_claim_from_support_and_heir_eligibility(self):
        ruler = character('ruler', 1, 10, 1, 1)
        claimant = character('claimant', 2, 10, -1, 1)
        supporter = character('supporter', 3, 10, -1, 1)
        heir = character('eligible_heir', 4, 10, 0, 1)
        heir['template'] = 'ZUL_cetshwayo_heir'
        claimant.update(ideology='ideology_traditionalist', traits={'brave'})
        claimant['vars']['sb_court_claimant_scope'] = claimant
        supporter['vars']['sb_court_claimant_scope'] = claimant
        runtime = CourtRuntime([ruler, claimant, supporter, heir])
        claimant['owner'] = {'id': 'CAP'}
        original_vars = dict(claimant['vars'])
        runtime.backing()
        expected = {'brave', 'sb_court_alignment_royal_trait', 'sb_court_claimant_trait'}
        self.assertEqual(expected, claimant['traits'])
        self.assertEqual(35,runtime.ref('prominence',claimant))
        self.assertIn('sb_court_endorsement_claimant_trait', supporter['traits'])
        self.assertNotIn('sb_court_claimant_trait', supporter['traits'])
        self.assertEqual(supporter['prominence'],runtime.ref('prominence',supporter))
        self.assertTrue(runtime.condition(TRIGGERS['sb_court_royal_candidate'], heir))
        self.assertIn('sb_court_endorsement_uncommitted_trait', heir['traits'])
        self.assertNotIn('sb_court_claimant_trait', heir['traits'])
        self.assertEqual(heir['prominence'],runtime.ref('prominence',heir))
        for name, value in original_vars.items():
            self.assertIs(value, claimant['vars'][name])
        runtime.backing()
        self.assertEqual(expected, claimant['traits'])
        for endorsement, target, name in ((-1, heir, 'claimant'), (1, claimant, 'incumbent'), (0, None, 'uncommitted')):
            with self.subTest(endorsement=endorsement):
                claimant['vars'].update(sb_court_endorsement_var=-1, sb_court_claimant_scope=claimant)
                runtime.backing()
                self.assertIn('sb_court_claimant_trait', claimant['traits'])
                claimant['vars'].update(sb_court_endorsement_var=endorsement, sb_court_claimant_scope=target)
                runtime.backing()
                self.assertEqual({'brave', 'sb_court_alignment_royal_trait', f'sb_court_endorsement_{name}_trait'}, claimant['traits'])
                self.assertEqual('ideology_traditionalist', claimant['ideology'])

    def test_trait_sync_and_roster_use_home_country_including_exiles(self):
        exile, child, dead, foreign = [character(name, i, 10) for i, name in enumerate(('exile', 'child', 'dead', 'foreign'))]
        exile['vars']['sb_court_following_var']=9
        runtime = CourtRuntime([character('king',1,20,1,1), exile, child, dead, foreign])
        exile['owner'] = {'id': 'CAP'}
        child['age'] = 12
        dead['alive'] = False
        foreign['vars']['sb_court_home_scope'] = {'id': 'NGN'}
        runtime.backing()
        self.assertEqual(2, len(exile['traits']))
        for actor in (child, dead, foreign):
            self.assertNotIn('traits', actor)
        self.assertTrue(runtime.roster_shown('sb_court_roster_member', exile))
        for actor in (child, dead, foreign):
            self.assertFalse(runtime.roster_shown('sb_court_roster_member', actor))

    def test_zero_following_attraction_does_not_add_an_empty_modifier(self):
        runtime = CourtRuntime([character('unaligned', 1, 10)])
        for kind in ('royal', 'chiefly'):
            runtime.country['movements'].append({'type': f'movement_sb_zulu_{kind}', 'owner': runtime.country, 'modifiers': {'sb_court_following_recruitment': .2}})
        runtime.backing()
        for movement in runtime.country['movements']:
            self.assertNotIn('sb_court_following_recruitment', movement['modifiers'])

    def test_successor_menu_selects_each_available_candidate_once_without_range_overflow(self):
        slots = ['sb_court_action_actor_scope', 'sb_court_second_candidate_scope', 'sb_court_third_candidate_scope'] + [f'sb_court_candidate_{i}_scope' for i in range(4, 13)]
        for count, minor in ((0,False), (0,True), (1,True), (2,True), (3,True), (12,True), (14,True)):
            with self.subTest(candidates=count, minor=minor):
                king = character('king', 1, 100, 1, 1)
                candidates = [character(f'prince-{i}', i + 2, i + 1, 0, 1) for i in range(count)]
                if minor: candidates.append(character('child', 99, 1000, alignment=1, age=12))
                excluded = [character('dead', 100, 1000, alignment=1, alive=False)]
                for member in [king] + candidates + excluded: member['template'] = 'ZUL_mpande_zulu'
                rt = CourtRuntime([king] + candidates + excluded)
                rt.country['vars'].update(dict.fromkeys(slots, king))  # An earlier menu must not leak selections.
                rt.effect(ACTIONS['sb_court_prepare_succession_choice'], rt.country)
                expected = sorted(candidates, key=lambda c: c['prominence'], reverse=True)[:12]
                actual = [rt.country['vars'][slot] for slot in slots if slot in rt.country['vars']]
                self.assertEqual([c['id'] for c in expected], [c['id'] for c in actual])
                self.assertEqual(['sb_court_politics.001'], rt.country['events'])
                self.assertNotIn('sb_court_candidate_index_var', rt.country['vars'])
                self.assertEqual({}, rt.scopes['root']['vars'])

    def test_foreign_event_root_households_age_and_death(self):
        members=[character('king',1,10,1,1),character('prince',1,9,-1,1),character('chief',2,10,0,2),character('child',3,100,1,1,age=12),character('dead',4,100,1,1,alive=False)]
        members[1]['vars']['sb_court_claimant_scope']=members[1]
        rt=CourtRuntime(members);rt.backing()
        self.assertEqual(44,rt.country['vars']['sb_court_weight_var'])
        self.assertEqual(2,rt.country['vars']['sb_court_representatives_var'])
        self.assertAlmostEqual(-34/36.5*100,rt.country['vars']['sb_prerogative_cooperation_var'])
        self.assertEqual({},rt.scopes['root']['vars'])
        self.assertIn('sb_court_representative_var',members[1]['vars'])

    def test_exiled_following_retains_identity_and_existing_claimant(self):
        king=character('king',1,10,1,1);exile=character('claimant',2,10,-1,1)
        exile['vars']['sb_court_claimant_scope']=exile
        rt=CourtRuntime([king,exile]);exile['owner']={'id':'CAP'};rt.backing()
        self.assertAlmostEqual((10-35)/45*100,rt.country['vars']['sb_prerogative_cooperation_var'])
        self.assertIs(exile,exile['vars']['sb_court_claimant_scope'])
        exile['alive']=False;rt.backing()
        self.assertEqual(100,rt.country['vars']['sb_prerogative_cooperation_var'])

    def test_shared_revolution_registry_counts_only_home_side_including_exiles(self):
        royal=character('royal',1,30,-1,1);chief=character('chief',2,10,1,2)
        royal['vars']['sb_court_claimant_scope']=royal
        rt=CourtRuntime([chief,royal]);rebel={'id':'REV','vars':{},'members':[chief,royal],'ruler':royal,'movements':[]}
        royal['vars']['sb_court_home_scope']=rebel;royal['owner']={'id':'CAP'}
        rt.backing()
        self.assertEqual(10,rt.country['vars']['sb_court_weight_var'])
        self.assertEqual(100,rt.country['vars']['sb_prerogative_cooperation_var'])
        rt.effect(EFFECTS['sb_court_calculate_backing'],rebel)
        self.assertEqual(30,rebel['vars']['sb_court_weight_var'])
        self.assertEqual(-100,rebel['vars']['sb_prerogative_cooperation_var'])
        self.assertIn('sb_court_representative_var',chief['vars'])
        self.assertIn('sb_court_representative_var',royal['vars'])

    def test_popularity_is_applied_once_and_clamped(self):
        rt=CourtRuntime([character('king',1,10,0,1)])
        rt.country['ruler']['popularity']=50;rt.backing()
        self.assertEqual(25,rt.country['vars']['sb_prerogative_cooperation_var'])
        rt.country['ruler']['vars']['sb_court_endorsement_var']=1;rt.backing()
        self.assertEqual(100,rt.country['vars']['sb_prerogative_cooperation_var'])

    def test_agitator_following_not_paid_twice_and_recruitment_disappears_on_exit(self):
        king=character('king',1,10,1,1);agitator=character('agitator',2,10,0,1,agitator=True)
        rt=CourtRuntime([king,agitator]);m={'type':'movement_sb_zulu_royal','vars':{},'owner':rt.country};rt.country['movements']=[m];rt.backing()
        self.assertEqual(.25,m['modifiers']['sb_court_following_recruitment'])
        agitator['owner']={'id':'CAP'};rt.backing()
        self.assertEqual(.5,m['modifiers']['sb_court_following_recruitment'])
        rt.country['vars'].pop('sb_institutions_active_var');rt.backing()
        self.assertNotIn('sb_court_following_recruitment',m['modifiers'])

    def test_alignment_weight_sum_and_representative_only_roll(self):
        rt=CourtRuntime([]);rt.country['movements']=[{'type':'movement_sb_zulu_royal','political_movement_support':.1},{'type':'movement_sb_zulu_chiefly','political_movement_support':.3}]
        self.assertEqual(3,rt.calc(VALUES['sb_court_royal_alignment_chance'],rt.country))
        self.assertEqual(9,rt.calc(VALUES['sb_court_chiefly_alignment_chance'],rt.country))
        self.assertEqual(88,rt.calc(VALUES['sb_court_neutral_alignment_chance'],rt.country))
        annual=(ROOT/'common/scripted_effects/sb_court_politics_effects.txt').read_text(encoding='utf-8-sig').split('sb_court_annual_alignment = {',1)[1].split('\nsb_court_align_neutral_chiefly',1)[0]
        self.assertIn('has_variable = sb_court_representative_var',annual)
        self.assertEqual(1,annual.count('random_list'))
        self.assertNotIn('random =',annual)




class CourtContractsTests(unittest.TestCase):
    def test_only_claimant_card_has_native_bonus_and_forced_faction_ideologies_are_gone(self):
        localization = self.source('localization/english/sb_court_politics_l_english.yml')
        for name, body in TRAITS.items():
            if name == 'sb_court_claimant_trait':
                self.assertEqual([('character_prominence_add','=', '25')],TRAIT_MODIFIERS[name])
            else:self.assertNotIn('_modifier', body)
            self.assertIn('possible = { always = no }', body)
            self.assertIn('value = 0', body)
            self.assertIn('weight = 0', body)
            self.assertIn(name + ':', localization)
            self.assertIn(name + '_desc:', localization)
            texture = re.search(r'texture = "([^"]+)"', body).group(1)
            self.assertTrue((ROOT/texture).is_file(), texture)
        for path in ('common/scripted_effects/sb_court_politics_effects.txt', 'common/scripted_effects/sb_zululand_settlement_effects.txt', 'common/character_templates/sb_court_characters.txt'):
            self.assertNotRegex(self.source(path), r'ideology_sb_zulu_(royalist|chiefly)_character')

    def test_prerogative_scale_has_neutral_centre_and_cap_marker(self):
        gui = self.source('gui/sb_prerogative_progress_bars.gui')
        self.assertIn('bad_progressbar_horizontal', gui)
        self.assertIn('value = 0.5 min = 0 max = 1', gui)
        self.assertIn('noprogresstexture = "gfx/interface/progressbar/progressbar_green.dds"', gui)
        self.assertIn('value = "[JournalEntry.GetCurrentBarProgress(ScriptedProgressBar.Self)]"', gui)
        native_gui = (GAME/'gui/journal_entry.gui').read_text(encoding='utf-8-sig')
        for asset in re.findall(r'(?:texture|progresstexture|noprogresstexture) = "([^"]+)"', gui):
            self.assertTrue((GAME/asset).is_file(), asset)
        self.assertIn('gfx/interface/progressbar/progressbar_marker.dds', native_gui)

    def test_titles_follow_constitution_and_roster_names_actual_allegiance(self):
        custom = definitions('common/customizable_localization/sb_court_custom_loc.txt')
        title = custom['sb_prerogative_title']
        first = next(v for k, _, v in title if k == 'text')
        self.assertEqual([('has_law', '=', 'law_type:law_sb_federated_chiefdoms')], first[0][2])
        self.assertEqual('sb_prerogative_chiefly_title', first[1][2])
        loc = self.source('localization/english/sb_court_politics_l_english.yml')
        self.assertIn("[Character.MakeScope.Var('sb_court_claimant_scope').GetCharacter.GetFullName]", loc)
        self.assertIn("[Character.MakeScope.Var('sb_court_home_scope').GetCountry.GetRuler.GetFullName]", loc)
        self.assertNotIn('[Character.GetCountry.GetRuler', loc)
        modifiers = self.source('common/static_modifiers/sb_court_modifiers.txt')
        icon = re.search(r'icon = "([^"]+)"', modifiers).group(1)
        self.assertTrue((GAME/icon).is_file())

    def test_named_negotiation_requirements_preserve_each_blocker(self):
        runtime = CourtRuntime([])
        requirements = TRIGGERS['sb_court_can_negotiate']
        self.assertTrue(runtime.condition(requirements, runtime.country))
        for flag in ('sb_court_civil_war_var', 'sb_court_dynastic_crisis_var', 'sb_court_action_open_var'):
            runtime.country['vars'][flag] = 1
            self.assertFalse(runtime.condition(requirements, runtime.country), flag)
            del runtime.country['vars'][flag]
        del runtime.country['vars']['sb_institutions_active_var']
        self.assertFalse(runtime.condition(requirements, runtime.country))

    def test_court_button_requirements_do_not_expose_internal_conditions(self):
        localization = self.source('localization/english/sb_court_politics_l_english.yml')
        buttons = definitions('common/scripted_buttons/sb_court_buttons.txt')

        def check_visible(nodes):
            for key, _, value in nodes:
                if key == 'custom_tooltip':
                    label = next(v for k, _, v in value if k == 'text')
                    self.assertIn(label + ':', localization)
                elif key in TRIGGERS:
                    check_visible(TRIGGERS[key])
                else:
                    self.assertNotIn(key, ('has_variable', 'any_in_list', 'has_template'))
                    self.assertFalse(key.startswith('var:'), key)
                    if isinstance(value, list):
                        check_visible(value)

        for name, body in buttons.items():
            with self.subTest(button=name):
                check_visible(next(v for k, _, v in body if k == 'possible'))

    def test_prerogative_uses_japans_gavel_and_one_button_renderer(self):
        journal = statements(self.source('common/journal_entries/1-03_sb_zulu_kingdom.txt'))
        japan = extract_top_level_blocks((GAME/'common/journal_entries/00_meiji_restoration.txt').read_text(encoding='utf-8-sig'))['je_meiji_main']
        icon = next(v for k, _, v in journal if k == 'icon')
        self.assertEqual(next(v for k, _, v in statements(japan) if k == 'icon'), icon)
        self.assertTrue((GAME/icon.strip('"')).is_file())
        buttons = [v for k, _, v in journal if k == 'scripted_button']
        self.assertEqual({'sb_court_recognize_successor_button', 'sb_court_introduce_heir_button', 'sb_court_accommodation_button'}, set(buttons))
        for key, _, value in journal:
            if key == 'widget':
                self.assertNotIn(('name', '=', '"com_journal_scripted_buttons"'), value)


    def source(self,path): return (ROOT/path).read_text(encoding='utf-8-sig')


    def test_actual_king_and_mbuyazi_are_candidates_and_never_recreated_by_install(self):
        text=self.source('common/scripted_triggers/sb_court_politics_triggers.txt')
        self.assertIn('has_template = ZUL_dingane',text)
        self.assertIn('has_template = ZUL_mbuyazi_heir',text)
        source=extract_top_level_blocks(self.source('common/scripted_effects/sb_court_politics_effects.txt'))['sb_court_install_royal_claimant']
        self.assertNotIn('create_character',source)
        self.assertNotIn('kill_character',source)
        actions=extract_top_level_blocks(self.source('common/scripted_effects/sb_court_actions_effects.txt'))
        recognize=actions['sb_court_recognize_candidate']
        install=actions['sb_court_install_recognized_successor']
        self.assertIn('sb_court_install_recognized_successor = yes',recognize)
        self.assertIn('sb_zulu_assign_new_heir_scope = yes',install)
        helper=extract_top_level_blocks(self.source('common/scripted_effects/sb_zulu_dynasty_succession_effects.txt'))['sb_zulu_assign_new_heir_scope']
        self.assertLess(helper.index('set_heir'),helper.index('free_character_from_void'))
        self.assertIn('set_variable = sb_zulu_mpande_mbuyazi_heir_var',install)
        self.assertNotIn('kill_',recognize + install)
        self.assertNotIn('create_character',recognize + install)
        menu=extract_top_level_blocks(self.source('common/scripted_effects/sb_court_actions_effects.txt'))['sb_court_prepare_succession_choice']
        self.assertIn('max = 12',menu)


    def test_real_war_receipt_precedes_once_dispatch_not_peaceful_gate(self):
        defs=extract_top_level_blocks(self.source('common/scripted_effects/sb_court_constitutional_war_effects.txt'))
        self.assertIn('var:sb_court_civil_war_var ?= scope:target',defs['sb_court_record_war_end'])
        win=defs['sb_court_resolve_won_war']
        self.assertLess(win.index('remove_variable = sb_court_war_ended_var'),win.index('sb_zululand_resolve_royal_contest'))
        self.assertNotIn('sb_prerogative_var',win)
        self.assertNotIn('is_at_war',win)
        self.assertIn('save_scope_as = sb_court_defeated_country',win)
        self.assertEqual(2,win.count('remove_variable = sb_court_war_ended_var'))
        self.assertEqual(2,win.count('remove_variable = sb_court_civil_war_var'))
        self.assertEqual(2,win.count('remove_variable = sb_court_war_alignment_var'))
        start=defs['sb_court_track_revolution']
        self.assertIn('is_civil_war_type = revolution',start)
        self.assertIn('set_variable = sb_institutions_zulu_profile_var',start)
        self.assertIn('transfer_character = scope:sb_court_rebels',start)
        self.assertNotIn('num_states',start)

    def test_claimant_must_accept_accommodation_and_coup_does_not_inherit_endorsements(self):
        defs=extract_top_level_blocks(self.source('common/scripted_effects/sb_court_actions_effects.txt'))
        self.assertIn('var:sb_court_action_actor_scope ?= var:sb_court_restoration_claimant_scope',defs['sb_court_accept_accommodation'])
        self.assertIn('name = sb_court_action_actor_scope value = var:sb_court_restoration_claimant_scope',defs['sb_court_prepare_opposition_offer'])
        hook=self.source('common/on_actions/sb_court_on_actions.txt')
        self.assertIn('scope:previous ?= { is_character_alive = no }',hook)
        self.assertIn('sb_court_capture_accession = yes', hook)
        self.assertIn('name = sb_court_endorsement_var value = 0',hook)
        self.assertIn('id = sb_court_politics.900 days = 1',hook)

    def test_no_future_cast_or_fabricated_genealogical_edges(self):
        text=self.source('common/scripted_effects/sb_court_politics_effects.txt')
        self.assertIn('year >= 1857',text)
        self.assertIn('year >= 1865',text)
        self.assertIn('year >= 1855',text)
        self.assertNotIn('template = ZUL_zibhebhu_kamaphitha',extract_top_level_blocks(text)['sb_court_spawn_dated_cast'])
        self.assertNotIn('ZUL_mbuyazi_successor',self.source('common/character_templates/sb_court_characters.txt'))
        self.assertIn('var:sb_court_following_var = scope:sb_court_candidate.var:sb_court_following_var',text)

    def test_split_carries_seed_receipt_and_closed_popup_cannot_reverse_exit(self):
        defs=extract_top_level_blocks(self.source('common/scripted_effects/sb_court_constitutional_war_effects.txt'))
        start=defs['sb_court_track_revolution']
        self.assertIn('set_variable = sb_institutions_movements_seeded_var',start)
        self.assertIn('name = sb_prerogative_last_change_var value = scope:sb_court_country.var:sb_prerogative_last_change_var',start)
        actions=self.source('common/scripted_effects/sb_court_actions_effects.txt')
        self.assertIn('sb_court_suspend',actions)
        events=self.source('events/sb_court_politics_events.txt')
        self.assertIn('sb_court_confrontation = { PURGE = yes }', events)
        self.assertIn('limit = { has_variable = sb_institutions_active_var var:sb_prerogative_var >= 25',events)



if __name__ == '__main__': unittest.main()
