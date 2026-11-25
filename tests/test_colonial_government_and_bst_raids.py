"""Execute the colony gates and the raid option, including immediate pop merging."""
from pathlib import Path
import unittest

from tests.test_zulu_court_politics import CourtRuntime, definitions
from tests.test_zulu_frontier_followup import field
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import find_object
from tools.validate import find_game_root

ROOT = Path(__file__).resolve().parents[1]
GAME = find_game_root(None)
GATE = 'sb_is_ordinary_colonial_subject'
COLONIAL = definitions('common/scripted_triggers/sb_colonial_administration.txt')[GATE]
RAID = definitions('common/scripted_effects/sb_bst_effects.txt')
DONOR = definitions('common/scripted_triggers/sb_bst_triggers.txt')['sb_bst_eligible_raid_donor']
EVENT = statements(find_object((ROOT/'events/sb_bst_frontier_events.txt').read_text(encoding='utf-8-sig'), 'sb_bst_frontier.010'))


def block(root, path, key, directive=None):
    return statements(find_object((root / path).read_text(encoding='utf-8-sig'), key, directive=directive))


class PatchRuntime(CourtRuntime):
    def ref(self, key, scope, prev=None):
        if key == 'c:BST.capital':
            return self.destination
        if key.startswith(('cu:', 's:', 'law_type:')):
            return key
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        for node in nodes:
            key, _, value = node
            if key == GATE:
                result = self.condition(COLONIAL, scope) == (value == 'yes')
            elif key == 'is_subject':
                result = bool(scope.get('overlord')) == (value == 'yes')
            elif key in ('is_country_type', 'is_subject_type', 'has_government_type', 'is_pop_type'):
                result = scope.get(key) == value
            elif key == 'has_law':
                result = scope.get('law') == value
            elif key == 'sb_bst_eligible_raid_donor':
                result = self.condition(DONOR, scope)
            elif key == 'any_scope_pop':
                result = any(self.condition(value, p, scope) for p in scope['pops'])
            elif key == 'has_slavery':
                result = scope['slavery'] == (value == 'yes')
            else:
                result = super().condition([node], scope, prev)
            if not result:
                return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, _, value = node
            if key == 'sb_bst_take_raid_captives':
                self.effect(RAID[key], scope)
            elif key.startswith('cu:') or key in ('state', 'culture', 'overlord', 'c:BST.capital'):
                self.effect(value, self.ref(key, scope, prev), scope)
            elif key == 'save_temporary_scope_as':
                self.scopes[value] = scope
            elif key in ('random_scope_state', 'ordered_scope_pop', 'every_scope_pop', 'random_scope_pop'):
                pool = scope['states' if key == 'random_scope_state' else 'pops']
                selected = [p for p in pool if self.condition(field(value, 'limit'), p, scope)]
                if key == 'ordered_scope_pop':
                    selected.sort(key=lambda p: p[field(value, 'order_by')], reverse=True)
                    selected = selected[int(field(value, 'position')):][:1]
                elif key.startswith('random'):
                    selected = selected[:1]
                for p in selected:
                    self.effect([n for n in value if n[0] not in ('limit','order_by','position')], p, scope)
            elif key == 'move_partial_pop':
                dest = self.ref(field(value, 'state'), scope)
                size = int(field(value, 'population'))
                assert 0 < size <= scope['total_size']
                self.add_pop(dest, size, scope['culture'], scope['is_pop_type'])
                scope['total_size'] -= size
                if scope['total_size'] == 0:
                    scope['state']['pops'].remove(scope)
            elif key == 'change_pop_culture':
                assert float(field(value, 'value')) == 1
                # Replace the object, as a native culture change may merge or retire its ID.
                state = scope['state']
                state['pops'].remove(scope)
                self.add_pop(state, scope['total_size'], self.ref(field(value,'target'),scope), scope['is_pop_type'])
            elif key == 'change_poptype':
                scope['is_pop_type'] = value.removeprefix('pop_type:')
            elif key == 'trigger_event':
                self.queued = (field(value,'on_action'), int(field(value,'days')))
            elif key == 'activate_law':
                scope['law'] = value
            else:
                super().effect([node], scope, prev)

    @staticmethod
    def add_pop(state, size, culture, job):
        for p in state['pops']:
            if (p['culture'], p['is_pop_type']) == (culture, job):
                p['total_size'] += size
                return
        state['pops'].append(dict(culture=culture,is_pop_type=job,total_size=size,
                                  state=state,owner=state['owner'],vars={}))


class ColonialGovernment(unittest.TestCase):
    def setUp(self):
        self.rt = PatchRuntime([])
        self.crown = {'id':'GBR','vars':{}}

    def colony(self, tag, kind='subject_type_colony', country_type='colonial', gov='governor'):
        return dict(id=tag,vars={},overlord=self.crown,is_subject_type=kind,
                    is_country_type=country_type,has_government_type=gov,law='law_type:law_theocracy')

    def test_colony_scope_and_restore_only_after_loss_in_same_relationship(self):
        guard = field(block(ROOT,'common/laws/sb_colonial_administration_guard.txt','law_colonial_administration','INJECT'),'on_deactivate')
        action = definitions('common/on_actions/sb_colonial_administration.txt')['sb_check_colonial_administration']
        for tag, kind, expected in [('CAP','subject_type_colony',True),('NAL','subject_type_colony',True),
                                    ('QUE','subject_type_colony',True),('EIC','subject_type_chartered_company',False),
                                    ('CAP','subject_type_sb_responsible_colony',False)]:
            with self.subTest(tag=tag,kind=kind):
                colony = self.colony(tag,kind)
                if tag == 'QUE':
                    colony['overlord'] = {'id':'FRA','vars':{}}
                self.assertEqual(self.rt.condition(COLONIAL,colony),expected)
                self.rt.queued = None
                self.assertEqual(colony['law'],'law_type:law_theocracy')  # Loading fires no callback.
                self.rt.effect(guard,colony)
                if expected:
                    self.assertEqual(self.rt.queued,('sb_check_colonial_administration',1))
                    self.rt.effect(field(action,'effect'),colony)
                    self.assertEqual(colony['law'],'law_type:law_colonial_administration')
                else:
                    self.assertIsNone(self.rt.queued)
        for transition in ('responsible','independent','different overlord'):
            colony = self.colony('CAP')
            self.rt.effect(guard,colony)
            if transition == 'responsible':
                colony['is_subject_type'] = 'subject_type_sb_responsible_colony'
            elif transition == 'independent':
                colony['overlord'] = None
            else:
                colony['overlord'] = {'id':'FRA','vars':{}}
            self.rt.effect(field(action,'effect'),colony)
            self.assertEqual(colony['law'],'law_type:law_theocracy')

    @unittest.skipUnless(GAME,'Vanilla source required')
    def test_all_gates_preserve_each_native_condition_and_payload(self):
        for folder, native, key, altered in (
            ('diplomatic_actions','38_subjects_increase_autonomy','da_increase_autonomy_of_subject',('potential','possible','accept_effect')),
            ('diplomatic_actions','38_subjects_increase_autonomy','da_increase_autonomy_of_self',('potential','possible','accept_effect')),
            ('diplomatic_plays','00_diplomatic_plays','dp_increase_autonomy',('possible',)),
            ('diplomatic_plays','00_diplomatic_plays','dp_independence',('possible',)),
            ('war_goal_types','09_increase_autonomy','increase_autonomy',('possible','valid'))):
            with self.subTest(key=key):
                mod = block(ROOT,f'common/{folder}/zz_sb_colonial_autonomy.txt',key,'REPLACE')
                original = block(GAME,f'common/{folder}/{native}.txt',key)
                def strip_gate(nodes):
                    kept = []
                    for k, op, v in nodes:
                        if k == GATE:
                            continue
                        kept.append((k,op,strip_gate(v) if isinstance(v,list) else v))
                    return kept
                for k, _, v in mod:
                    if k not in altered:
                        self.assertEqual(v,field(original,k))
                        continue
                    if k == 'accept_effect':
                        wrapped = field(v,'if')
                        v = field(wrapped,'limit')
                        self.assertEqual([n for n in wrapped if n[0]!='limit'],field(original,k))
                    else:
                        self.assertEqual(strip_gate(v),field(original,k))
                    if key.endswith('_of_subject'):
                        v = field(v,'scope:target_country')
                    if key == 'dp_independence':
                        v = field(v,'OR')
                    self.assertIn((GATE,'=','yes' if key=='dp_independence' else 'no'),v)
        law = block(GAME,'common/laws/00_governance_principles.txt','law_colonial_administration')
        self.assertNotIn('on_deactivate',[k for k,_,_ in law])
        group = block(GAME,'common/law_groups/00_laws.txt','lawgroup_governance_principles')
        self.assertIn('subject_type_colony',str(field(group,'change_allowed_trigger')))
        handoff = definitions('common/diplomatic_actions/sb_subject_autonomy_actions.txt')
        for key, event in handoff.items():
            target = field(event,'possible')
            if key.startswith('sb_grant'):
                target = field(target,'scope:target_country')
            self.assertIn((GATE,'=','yes'),target)
            order = str(field(event,'accept_effect'))
            self.assertLess(order.index('sb_apply_responsible_colony_subject_type_from_overlord'),
                            order.index('sb_apply_responsible_colony_governance_from_overlord'))


class RaidCaptives(unittest.TestCase):
    def test_actual_option_with_merging_existing_residents_and_ineligible_victims(self):
        for size,culture,slavery,eligible in [(740,'swazi',True,True),(100,'griqua',True,True),
                                              (145,'sotho',False,True),(99,'sotho',True,False),
                                              (350,'boer',True,False)]:
            with self.subTest(size=size,culture=culture,slavery=slavery):
                rt=PatchRuntime([])
                victim={'vars':{},'gold_reserves':1500}
                bst={'vars':{},'slavery':slavery}
                source=dict(state_region='s:STATE_VRYSTAAT',owner=victim,pops=[])
                other=dict(state_region='s:STATE_NATAL',owner=victim,pops=[])
                rt.destination=dict(owner=bst,pops=[])
                victim['states']=[other,source]
                rt.add_pop(source,8000,'cu:boer','peasants')
                rt.add_pop(source,2000,'cu:boer' if culture=='boer' else 'cu:swazi','slaves')
                rt.add_pop(source,size,'cu:'+culture,'farmers')
                if eligible and size>100:
                    rt.add_pop(source,100,'cu:griqua','peasants')
                rt.add_pop(other,10000,'cu:boer' if culture=='boer' else 'cu:sotho','peasants')
                rt.add_pop(rt.destination,777,'cu:'+culture,'farmers')
                rt.add_pop(rt.destination,25,'cu:'+culture,'slaves')
                # Collisions at either end must preserve the existing marker-culture residents.
                if size == 100:
                    rt.add_pop(source,35,'cu:promethean','farmers')
                elif size == 145:
                    rt.add_pop(rt.destination,45,'cu:promethean','peasants')
                def count(state, **match):
                    return sum(p['total_size'] for p in state['pops'] if all(p[k]==v for k,v in match.items()))
                before=[count(st) for st in (source,rt.destination,other)]
                rt.effect(field(field(EVENT,'option'),'hidden_effect'),victim)
                delta=100 if eligible else 0
                self.assertEqual([count(st) for st in (source,rt.destination,other)],
                                 [before[0]-delta,before[1]+delta,before[2]])
                self.assertEqual(count(source,culture='cu:'+culture,is_pop_type='farmers'),size-delta)
                self.assertEqual(count(rt.destination,culture='cu:'+culture,is_pop_type='farmers'),777)
                self.assertEqual(count(rt.destination,is_pop_type='slaves'),25+(delta if slavery else 0))
                self.assertEqual(count(rt.destination,is_pop_type='laborers'),delta if not slavery else 0)
                self.assertFalse(any(count(st,culture='cu:sb_raid_transfer') for st in (source,rt.destination)))
                self.assertEqual(count(source,culture='cu:promethean'),35 if size==100 else 0)
                self.assertEqual(count(rt.destination,culture='cu:promethean'),45 if size==145 else 0)
                self.assertEqual(victim['gold_reserves'],500)
        button=str(RAID['sb_bst_execute_oranje_raid'])
        for token in ('sb_bst_oranje_raid_cooldown_var','365','sb_boost_firearms_progress_raid','1000'):
            self.assertIn(token,button)
