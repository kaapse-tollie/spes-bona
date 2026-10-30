"""Run shipped claimant scripts with explicit native callback inputs, not a simulated engine war."""
import hashlib
import json
import math
import re
import unittest
from itertools import product
from pathlib import Path
from unittest.mock import patch

from tests.test_zulu_court_politics import character, EFFECTS, VALUES, TRIGGERS, definitions
from tests.test_zulu_court_rework import ReworkRuntime
from tests.test_zulu_institutions_laws import statements, child
from tools.check_override_inventory import extract_top_level_blocks, find_object

ROOT = Path(__file__).resolve().parents[1]
GAME = Path.home()/'Library/Application Support/Steam/steamapps/common/Victoria 3/game'
GOVERNANCE = {'law_type:'+n for n in ('law_monarchy','law_social_monarchy','law_sb_contested_crown','law_sb_contested_social_crown')}
IG_TYPES = ('ig_armed_forces','ig_landowners','ig_devout','ig_industrialists','ig_intelligentsia','ig_petty_bourgeoisie','ig_rural_folk','ig_trade_unions')


class ClaimantRuntime(ReworkRuntime):
    """Native movement/war creation is supplied by tests; no allocation or winner is invented."""
    def calc(self,nodes,scope,prev=None):
        expanded=[]
        for key,op,value in nodes:
            if key in ('every_scope_building','every_scope_pop'):
                limit=next((v for k,_,v in value if k=='limit'),[])
                body=[n for n in value if n[0]!='limit']
                items=scope.get('buildings',[]) if key=='every_scope_building' else scope.get('pops',[p for st in scope.get('states',[]) for p in st.get('pops',[])])
                for building in items:
                    if self.condition(limit,building,scope):
                        expanded.append(('add','=',str(self.calc(body,building,scope))))
            else: expanded.append((key,op,value))
        return super().calc(expanded,scope,prev)

    def ref(self,key,scope,prev=None):
        if key == 'num_states': return len(scope.get('states',[]))
        if key.startswith(('law_type:','movement_type:','s:')): return key
        if key == 'active_law:lawgroup_governance_principles.type':
            return next(iter(scope.get('laws',set()) & GOVERNANCE),None)
        return super().ref(key,scope,prev)

    def condition(self,nodes,scope,prev=None):
        for key,op,value in nodes:
            if key == 'any_civil_war': result=any(self.condition(value,w,scope) for w in scope.get('wars',[]))
            elif key == 'any_political_movement': result=any(self.condition(value,m,scope) for m in scope.get('movements',[]))
            elif key == 'is_civil_war_type': result=scope.get('type') == value
            elif key == 'is_player': result=scope.get('player',False) == (value=='yes')
            elif key == 'is_ai': result=(not scope.get('player',False)) == (value=='yes')
            elif key == 'is_country_alive': result=scope.get('alive',True) == (value=='yes')
            elif key == 'any_scope_building': result=any(self.condition(value,b,scope) for b in scope.get('buildings',[]))
            elif key == 'is_building_type': result=scope.get('type') == value
            elif key == 'is_employed': result=scope.get('employed',True) == (value=='yes')
            elif key == 'is_pop_type': result=scope.get('type') == value
            elif key == 'has_active_production_method': result=value in scope.get('production_methods',set())
            elif key == 'is_enacting_law': result=scope.get('enacting') == value
            elif key == 'has_ideology' and 'ideologies' in scope: result=value.removeprefix('ideology:') in scope['ideologies']
            else: result=super().condition([(key,op,value)],scope,prev)
            if not result: return False
        return True

    def effect(self,nodes,scope,prev=None):
        for node in self.branches(nodes,scope,prev):
            key,op,value=node
            if key in ('sb_institutions_reconcile','sb_institutions_recalculate','sb_court_ensure_roster'):
                # This fixture retains IR>0; real law/IR lifecycle is separately executed below.
                if key == 'sb_institutions_reconcile' and scope.get('laws',set()) & GOVERNANCE:
                    scope['vars']['sb_institutions_active_var']=1
                self.effect(EFFECTS['sb_court_calculate_backing'],scope)
            elif key == 'create_political_movement':
                kind=dict((k,v) for k,_,v in value)['type']
                self.recruitment_at_movement_creation={st['id']:sum(b['level'] for b in st.get('buildings',[])
                    if b['type'] in ('building_barrack','building_conscription_center')) for st in scope.get('states',[])}
                scope.setdefault('movements',[]).append({'id':'movement','type':kind,'owner':scope,'vars':{},'political_movement_support':0})
            elif key in ('random_political_movement','random_civil_war'):
                limit=next((v for k,_,v in value if k=='limit'),[])
                pool=scope.get('movements' if key=='random_political_movement' else 'wars',[])
                chosen=next((x for x in pool if self.condition(limit,x,scope)),None)
                if chosen is not None: self.effect([n for n in value if n[0]!='limit'],chosen,scope)
            elif key == 'set_core_ideology': scope['ideology']=value
            elif key == 'add_ideology': scope.setdefault('ideologies',set()).add(value)
            elif key == 'remove_ideology': scope.setdefault('ideologies',set()).discard(value)
            elif key == 'every_interest_group':
                limit=next((v for k,_,v in value if k=='limit'),[])
                for ig_key,ig in list(scope.items()):
                    if ig_key.startswith('ig:') and self.condition(limit,ig,scope):
                        self.effect([n for n in value if n[0]!='limit'],ig,scope)
            elif key == 'add_civil_war_progress': scope['progress']=scope.get('progress',0)+float(value)
            elif key in ('every_scope_state','ordered_scope_state','every_scope_building'):
                fields=dict((k,v) for k,_,v in value)
                items=list(scope.get('buildings' if key=='every_scope_building' else 'states',[]))
                items=[x for x in items if self.condition(fields.get('limit',[]),x,scope)]
                if key=='ordered_scope_state':
                    items=sorted(items,key=lambda x:self.ref(fields['order_by'],x,scope),reverse=True)
                    pos=int(fields['position']); items=items[pos:pos+1]
                for item in items:
                    self.effect([n for n in value if n[0] not in ('limit','order_by','position','check_range_bounds')],item,scope)
            elif key == 'remove_building':
                scope['buildings']=[b for b in scope['buildings'] if b['type']!=value]
                self.demolitions=getattr(self,'demolitions',[])+[(scope['id'],value)]
                self.force_operations=getattr(self,'force_operations',[])+['demolish']
            elif key == 'every_scope_pop':
                limit=next((v for k,_,v in value if k=='limit'),[])
                pops=scope.get('pops',[]) if 'pops' in scope else [p for s in scope.get('states',[]) for p in s.get('pops',[])]
                for pop in list(pops):
                    if self.condition(limit,pop,scope): self.effect([n for n in value if n[0]!='limit'],pop,scope)
            elif key == 'move_partial_pop':
                # Native movement is a primitive here, not a model of hiring/training or conscription caps.
                fields=dict((k,v) for k,_,v in value)
                destination=self.ref(fields['state'],scope,prev)
                ratio=self.ref(fields['population_ratio'],scope,prev)
                self.assert_valid_pop_move(scope,destination,ratio)
                moved=dict(scope,state=destination,owner=destination['owner'],vars=dict(scope['vars']))
                for count in ('workforce','dependants'):
                    moved[count]=math.floor(scope[count]*ratio)
                    scope[count]-=moved[count]
                destination.setdefault('pops',[]).append(moved)
                self.pop_moves=getattr(self,'pop_moves',[])+[(scope['type'],scope['state']['id'],destination['id'],moved['workforce'],moved['dependants'])]
                self.force_operations=getattr(self,'force_operations',[])+['move']
            elif key == 'create_building':
                fields=dict((k,v) for k,_,v in value)
                level=self.ref(fields['level'],scope,prev)
                existing=next((b for b in scope['buildings'] if b['type']==fields['building']),None)
                if existing is not None: existing['level']=max(existing['level'],level)
                else: scope['buildings'].append({'type':fields['building'],'level':level,'vars':{},'production_methods':set()})
            elif key == 'activate_production_method':
                fields=dict((k,v) for k,_,v in value)
                b=next(b for b in scope['buildings'] if b['type']==fields['building_type'])
                b['production_methods']={fields['production_method']}
            elif key == 'transfer_character':
                target=self.ref(value,scope,prev)
                self.transfers=getattr(self,'transfers',[])+[(scope['id'],scope['owner']['id'],target['id'])]
                scope['owner']=target
            elif key == 'add_character_role': scope[value]=True
            elif key in ('free_from_exile_effect','free_character_from_void'):
                scope['is_in_exile_pool' if key=='free_from_exile_effect' else 'is_in_void']=False
            elif key == 'activate_law':
                law=self.ref(value,scope,prev)
                if law in GOVERNANCE: scope['laws'].difference_update(GOVERNANCE)
                scope.setdefault('laws',set()).add(law)
            elif key == 'play_as':
                target=self.ref(value,scope,prev)
                self.switches=getattr(self,'switches',[])+[target['id']]
                scope['player']=False;target['player']=True
            elif key == 'cancel_enactment': scope.pop('enacting',None)
            elif key == 'set_variable' and isinstance(value,list) and any(k=='months' for k,_,v in value):
                fields=dict((k,v) for k,_,v in value)
                scope.setdefault('timed_writes',[]).append((fields['name'],float(fields['months'])))
                super().effect([node],scope,prev)
            elif key == 'set_global_variable': self.scopes['root']['vars'][value]=1
            elif key == 'remove_global_variable': self.scopes['root']['vars'].pop(value,None)
            else: super().effect([node],scope,prev)

    @staticmethod
    def assert_valid_pop_move(pop,destination,ratio):
        assert pop['state'] is not destination
        assert 0 <= ratio <= 1
    def run(self,name,scope=None): self.effect(EFFECTS[name],scope or self.country)


def court(king_weight=100,prince_weight=100):
    king=character('Dingane',1,king_weight,1,1);king['template']='ZUL_dingane'
    prince=character('Mpande',2,prince_weight-25,-1,1);prince['template']='ZUL_mpande_zulu'
    prince['vars']['sb_court_claimant_scope']=prince
    third=character('Gqugqu',3,30,-1,1);third['template']='ZUL_gqugqu_claimant'
    third['vars']['sb_court_claimant_scope']=third
    neutral=character('uncommitted house',4,100)
    rt=ClaimantRuntime([king,prince,third,neutral])
    rt.country.update(player=True,laws={'law_type:law_monarchy','law_type:law_autocracy'},wars=[],states=[],game_date=18360101)
    rt.country['ig:ig_armed_forces']={'id':'AF','type':'ig_armed_forces','owner':rt.country,'vars':{},
                                    'ideologies':{'ideology_patriotic','ideology_jingoist'},'approval':3,
                                    'leader':{'ideology':'ideology_royalist'},'modifiers':{}}
    for kind in IG_TYPES[1:]:
        rt.country['ig:'+kind]={'id':kind,'type':kind,'owner':rt.country,'vars':{},
                               'ideologies':{'original_'+kind},'approval':3,
                               'leader':{'ideology':'ideology_moderate'},'modifiers':{}}
    rt.country['vars'].update(sb_institutions_zulu_profile_var=1,sb_prerogative_var=-50,
        sb_prerogative_last_change_var=0,sb_prerogative_cooperation_var=0,sb_court_incumbent_scope=king)
    rt.backing()
    return rt,king,prince,third,neutral


def reserve(rt,nominee,rival,reason=1):
    rt.country['vars'].update(sb_court_accession_nominee_scope=nominee,sb_court_accession_rival_scope=rival)
    rt.effect([('sb_court_reserve_dynastic_crisis','=',[('REASON','=',str(reason))])],rt.country)
    rt.scopes.update(sb_court_nominee=nominee,sb_court_rival=rival)


def answer(rt,rebels=False):
    rt.effect([('sb_court_answer_dynastic_crisis','=',[('CLAIMANT','=','yes' if rebels else 'no')])],rt.country)


def organising_war(rt,social=False):
    movement=rt.country['vars']['sb_court_dynastic_movement_scope']
    movement['most_desired_law']='law_type:law_sb_contested_social_crown' if social else 'law_type:law_sb_contested_crown'
    # Native agitator assignment is an explicit input, not fabricated by the script harness.
    rt.country['vars']['sb_court_dynastic_rival_scope']['political_movement']=movement
    war={'id':'native-war','type':'revolution','political_movement':movement,'vars':{},'progress':0}
    rt.country['wars'].append(war)
    return war


def split(rt,native_rebel_characters=(),native_ruler=None,native_heir=None,inherit_sponsor=True,native_rebel_states=()):
    war=organising_war(rt,rt.country['vars']['sb_court_dynastic_original_law_var']==2)
    rt.run('sb_court_progress_dynastic_crisis')
    # Native civil-war lists belong to the origin country, not the uprising country.
    rebels={'id':'REB','vars':{'civil_war_type_var':'movement_type:movement_sb_dynastic_test'},
            'civil_war_origin_country':rt.country,'wars':[],'laws':set(rt.country['laws']),
            'members':[], 'movements':[], 'states':list(native_rebel_states), 'ruler':native_ruler, 'heir':native_heir, 'game_date':18360101}
    # Supply native IG inheritance explicitly, just as the native war object is supplied.
    for kind in IG_TYPES:
        sponsor=rt.country['ig:'+kind]
        rebels['ig:'+kind]={'id':'rebel-'+kind,'type':kind,'owner':rebels,'vars':{},
                           'ideologies':set(sponsor['ideologies']),'modifiers':dict(sponsor['modifiers']) if inherit_sponsor else {}}
    for state in native_rebel_states:
        state['owner']=rebels
        for pop in state.get('pops',[]): pop['owner']=rebels
    for actor in native_rebel_characters: actor['owner']=rebels
    for actor in (native_ruler,native_heir):
        if actor is not None: actor['owner']=rebels
    rt.scopes['target']=rebels
    rt.run('sb_court_track_dynastic_war')
    return war,rebels


class ClaimantBehaviour(unittest.TestCase):
    def recruitment_states(self,rt,counts):
        states=[]
        for i,(regular,conscript) in enumerate(counts):
            buildings=[]
            for kind,levels,pm in (('building_barrack',regular,'pm_general_training'),
                                   ('building_conscription_center',conscript,'pm_sb_customary_muster_conscription')):
                if levels: buildings.append({'type':kind,'level':levels,'vars':{},'production_methods':{pm}})
            buildings.append({'type':'building_logging_camp','level':2,'vars':{}})
            states.append({'id':f'state-{i}','owner':rt.country,'vars':{},'state_population':100000-i,'buildings':buildings})
        rt.country['states']=states
        return states

    def add_staff(self,state,kind,workers,dependants,culture='zulu',religion='animist'):
        state.setdefault('pops',[]).append(dict(type=kind,workforce=workers,dependants=dependants,
            culture=culture,religion=religion,state=state,owner=state['owner'],vars={}))

    def test_coalition_geography_protects_stronger_homeland_for_both_choices(self):
        for weights,back_prince in product(((300,100),(100,300),(200,200)),(False,True)):
            rt,king,prince,*_=court(*weights)
            mainland,natal=self.recruitment_states(rt,[(4,17),(0,0)])
            mainland['state_region']='s:STATE_ZULULAND';natal['state_region']='s:STATE_NATAL'
            reserve(rt,king,prince);answer(rt,back_prince)
            rebels_stronger=(weights[0]>=weights[1]) if back_prince else (weights[1]>weights[0])
            target=mainland if rebels_stronger else natal;protected=natal if rebels_stronger else mainland
            self.assertEqual(1000000,rt.calc(VALUES['sb_court_dynastic_state_weight'],target))
            self.assertEqual(0,rt.calc(VALUES['sb_court_dynastic_state_weight'],protected))
            # Live politics cannot change the frozen regional decision; neither can foreign ROOT.
            king['prominence']=9999;prince['prominence']=1
            self.assertEqual(1000000,rt.calc(VALUES['sb_court_dynastic_state_weight'],target))
            rt.country['states']=[mainland]
            self.assertEqual(1,rt.calc(VALUES['sb_court_dynastic_state_weight'],mainland))
            rt.country['states']=[mainland,natal];rt.country['vars'].pop('sb_court_dynastic_test_pending_var')
            self.assertEqual(1,rt.calc(VALUES['sb_court_dynastic_state_weight'],mainland))
            self.assertEqual(1,rt.calc(VALUES['sb_court_dynastic_state_weight'],natal))

    def test_staff_follows_both_service_jobs_before_workplaces_are_rebuilt(self):
        for weights,back_prince,native_rebels_mainland in product(((300,100),(100,300),(200,200)),(False,True),(False,True)):
            rt,king,prince,*_=court(*weights)
            mainland,natal=self.recruitment_states(rt,[(4,17),(0,0)])
            self.add_staff(mainland,'soldiers',7600,24000)
            self.add_staff(natal,'soldiers',400,1200)
            self.add_staff(mainland,'officers',100,300)
            self.add_staff(natal,'officers',300,900,'swazi')
            self.add_staff(natal,'peasants',9000,27000)
            reserve(rt,king,prince);answer(rt,back_prince)
            rt.force_operations=[]
            original,rebel=(natal,mainland) if native_rebels_mainland else (mainland,natal)
            rt.country['states']=[original]
            _,rebels=split(rt,native_rebel_states=[rebel])
            prince_country=rt.country if back_prince else rebels
            # Four barracks: reserve one for the weaker side, round its quota,
            # then use the exact remainder for the stronger side.
            regular=prince_country['vars']['sb_court_regular_quota_var']
            levy=prince_country['vars']['sb_court_conscript_quota_var']
            # 17,400 available workers / 1,200 per level allows ten levies after four regulars.
            levy_total=10
            soldier_share=(regular*950+levy*990)/(4*950+levy_total*990)
            officer_share=(regular*50+levy*10)/(4*50+levy_total*10)
            for kind,total in (('soldiers',8000),('officers',400)):
                got=sum(p['workforce'] for st in prince_country['states'] for p in st['pops'] if p['type']==kind)
                self.assertAlmostEqual(total*(soldier_share if kind=='soldiers' else officer_share),got,delta=2)
                self.assertEqual(total,sum(p['workforce'] for st in (mainland,natal) for p in st['pops'] if p['type']==kind))
            for kind,dependants in (('soldiers',25200),('officers',1200),('peasants',27000)):
                self.assertEqual(dependants,sum(p['dependants'] for st in (mainland,natal) for p in st['pops'] if p['type']==kind))
            self.assertEqual(9000,sum(p['workforce'] for st in (mainland,natal) for p in st['pops'] if p['type']=='peasants'))
            self.assertEqual(300,sum(p['workforce'] for st in (mainland,natal) for p in st['pops'] if p['culture']=='swazi'))
            self.assertEqual(['animist'],list(set(p['religion'] for st in (mainland,natal) for p in st['pops'])))
            self.assertLess(max(i for i,k in enumerate(rt.force_operations) if k=='move'),rt.force_operations.index('demolish'))
            first=list(rt.pop_moves);rt.run('sb_court_rebuild_dynastic_forces');rt.run('sb_court_track_dynastic_war')
            self.assertEqual(first,rt.pop_moves)
            self.assertFalse(any('staff' in k for k in rt.country['vars']))
            self.assertNotIn('pops',rt.scopes['root'])

    def test_zero_balanced_and_tiny_staff_pools_do_not_create_people(self):
        for workers in (0,1,100):
            rt,king,prince,*_=court()
            mainland,natal=self.recruitment_states(rt,[(2,0),(1,0)])
            self.add_staff(mainland,'officers',workers,workers*3)
            self.add_staff(natal,'officers',workers*2,workers*6)
            reserve(rt,king,prince);answer(rt)
            rt.country['states']=[mainland];split(rt,native_rebel_states=[natal])
            self.assertFalse(hasattr(rt,'pop_moves'))
            self.assertEqual(workers*3,sum(p['workforce'] for st in (mainland,natal) for p in st['pops']))

    def test_empty_state_receives_existing_recruitment_before_movement_creation(self):
        for back_prince in (False,True):
            rt,king,prince,*_=court(177,334)
            states=self.recruitment_states(rt,[(4,17),(0,0)])
            reserve(rt,king,prince);answer(rt,back_prince)
            self.assertEqual({'state-0':20,'state-1':1},rt.recruitment_at_movement_creation)
            self.assertEqual(4,sum(b['level'] for st in states for b in st['buildings'] if b['type']=='building_barrack'))
            self.assertEqual(17,sum(b['level'] for st in states for b in st['buildings'] if b['type']=='building_conscription_center'))
            self.assertEqual({'pm_general_training'},next(b for b in states[1]['buildings'] if b['type']=='building_barrack')['production_methods'])
            self.assertEqual([('state-0','building_barrack')],rt.demolitions)
            first=list(rt.demolitions)
            rt.run('sb_court_prepare_dynastic_forces');rt.run('sb_court_progress_dynastic_crisis');answer(rt,back_prince)
            self.assertEqual(first,rt.demolitions)
            self.assertNotIn('sb_court_dynastic_forces_rebuilt_var',rt.country['vars'])

    def test_preparation_conserves_sparse_services_and_keeps_donors_nonempty(self):
        for counts,expected_occupied in (([(0,4),(0,0)],2), ([(1,1),(0,0)],2),
                                         ([(2,1),(0,0),(0,0)],3), ([(1,0),(0,0)],1),
                                         ([(0,0),(0,0)],0), ([(4,17)],1), ([(2,0),(0,3)],2)):
            rt,king,prince,*_=court();states=self.recruitment_states(rt,counts)
            reserve(rt,king,prince);answer(rt)
            totals=[sum(b['level'] for st in states for b in st['buildings'] if b['type']==kind)
                    for kind in ('building_barrack','building_conscription_center')]
            self.assertEqual([sum(c[n] for c in counts) for n in (0,1)],totals)
            self.assertEqual(expected_occupied,sum(n>0 for n in rt.recruitment_at_movement_creation.values()))
            self.assertEqual(2*len(states),sum(b['level'] for st in states for b in st['buildings'] if b['type']=='building_logging_camp'))
            for st in states:
                for b in st['buildings']:
                    if b['type']=='building_barrack': self.assertEqual({'pm_general_training'},b['production_methods'])
                    if b['type']=='building_conscription_center': self.assertEqual({'pm_sb_customary_muster_conscription'},b['production_methods'])
            if expected_occupied==sum(sum(c)>0 for c in counts): self.assertFalse(hasattr(rt,'demolitions'))

    def test_preparation_then_actual_split_preserves_both_coalition_quotas(self):
        for back_prince,rebels_take_mainland in product((False,True),repeat=2):
            rt,king,prince,*_=court(177,334)
            mainland,natal=self.recruitment_states(rt,[(4,17),(0,0)])
            self.add_staff(mainland,'peasants',50000,150000)
            reserve(rt,king,prince);answer(rt,back_prince)
            self.assertGreater(rt.recruitment_at_movement_creation['state-1'],0)
            original,rebel=(natal,mainland) if rebels_take_mainland else (mainland,natal)
            rt.country['states']=[original]
            _,rebels=split(rt,native_rebel_states=[rebel])
            prince_country=rt.country if back_prince else rebels
            king_country=rebels if back_prince else rt.country
            for country,regular,conscript in ((prince_country,2,11),(king_country,2,6)):
                self.assertEqual(regular,sum(b['level'] for st in country['states'] for b in st['buildings'] if b['type']=='building_barrack'))
                self.assertEqual(conscript,sum(b['level'] for st in country['states'] for b in st['buildings'] if b['type']=='building_sb_court_muster'))
            changes=list(rt.demolitions)
            rt.run('sb_court_prepare_dynastic_forces');rt.run('sb_court_rebuild_dynastic_forces')
            self.assertEqual(changes,rt.demolitions)
            rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win')
            for country in (rt.country,rebels):
                self.assertNotIn('sb_court_dynastic_forces_prepared_var',country['vars'])

    def test_preparation_is_current_country_only_and_cancellation_does_not_rebuild(self):
        rt,king,prince,*_=court();states=self.recruitment_states(rt,[(4,17),(0,0)])
        foreign_state={'id':'foreign','owner':rt.scopes['root'],'vars':{},'state_population':100000,
                       'buildings':[{'type':'building_barrack','level':50,'vars':{}}]}
        rt.scopes['root']['states']=[foreign_state]
        rt.run('sb_court_prepare_dynastic_forces')
        self.assertFalse(hasattr(rt,'demolitions'))
        reserve(rt,king,prince);rt.run('sb_court_prepare_dynastic_forces')
        self.assertFalse(hasattr(rt,'demolitions'))
        answer(rt)
        self.assertEqual(50,foreign_state['buildings'][0]['level'])
        self.assertNotIn('sb_court_dynastic_forces_prepared_var',rt.scopes['root']['vars'])
        changed=list(rt.demolitions)
        rt.run('sb_court_cancel_dynastic_crisis')
        self.assertEqual(changed,rt.demolitions)
        self.assertNotIn('sb_court_dynastic_forces_prepared_var',rt.country['vars'])
        self.assertFalse(any(k.startswith(('sb_court_regular_','sb_court_conscript_')) for k in rt.country['vars']))
        self.assertEqual(21,sum(b['level'] for st in states for b in st['buildings'] if b['type']!='building_logging_camp'))

    def test_preparation_rejects_invalid_participants_disabled_courts_and_existing_wars(self):
        for invalid in ('dead','disabled','unrelated_war','already_split'):
            rt,king,prince,*_=court();states=self.recruitment_states(rt,[(4,17),(0,0)])
            reserve(rt,king,prince);rt.country['vars']['sb_court_dynastic_test_pending_var']=1
            if invalid=='dead': prince['alive']=False
            elif invalid=='disabled':
                rt.country['vars'].pop('sb_institutions_zulu_profile_var');rt.country['id']='FRA'
            elif invalid=='unrelated_war': rt.country['wars']=[{'id':'other','vars':{}}]
            else: rt.country['vars']['sb_court_dynastic_war_scope']={'id':'war','vars':{}}
            rt.run('sb_court_prepare_dynastic_forces')
            self.assertFalse(hasattr(rt,'demolitions'))
            self.assertNotIn('sb_court_dynastic_forces_prepared_var',rt.country['vars'])

    def test_claimant_recruitment_uses_prince_popularity_not_incumbent(self):
        rt,king,prince,*_=court();reserve(rt,king,prince)
        for king_q in (-100,0,100):
            king['popularity']=king_q
            for prince_q,factor in ((-100,.2),(-50,.5),(0,1),(50,1.5),(100,1.8)):
                prince['popularity']=prince_q
                self.assertAlmostEqual(factor,rt.calc(VALUES['sb_court_claimant_popularity_attraction'],rt.country))
        movement=(ROOT/'common/political_movements/sb_court_dynastic_test.txt').read_text(encoding='utf-8-sig')
        self.assertNotIn('owner.ruler',movement)
        self.assertNotIn('movement_support_ruler_popularity',movement)
        self.assertIn('owner.sb_court_claimant_popularity_attraction',movement)

    def test_force_quotas_conserve_separate_service_totals_and_rounding(self):
        rt,*_=court()
        for i,r,total in product((0,1,100,177,300),(1,100,334,900),(0,1,4,17,100)):
            rt.country['vars'].update(sb_court_dynastic_incumbent_weight_var=i,sb_court_dynastic_rival_weight_var=r)
            for service in ('regular','conscript'):
                rt.country['vars']['sb_court_'+service+'_total_var']=total
                allocated=rt.calc(VALUES['sb_court_dynastic_'+service+'_allocation'],rt.country)
                if service=='regular' and total and i!=r:
                    weaker=math.floor(1+(total-1)*min(i,r)/(i+r)+.5)
                    expected=total-weaker if r>i else weaker
                    self.assertGreaterEqual(weaker,1)
                else: expected=math.floor(total*r/(i+r)+.5)
                self.assertEqual(expected,allocated)
                self.assertGreaterEqual(allocated,0);self.assertLessEqual(allocated,total)
        # House Prominence is frozen: later political changes cannot alter the split.
        rt.country['vars'].update(sb_court_dynastic_incumbent_weight_var=177,sb_court_dynastic_rival_weight_var=334)
        rt.country['vars'].update(sb_court_regular_total_var=4,sb_court_conscript_total_var=17)
        self.assertEqual(2,rt.calc(VALUES['sb_court_dynastic_regular_allocation'],rt.country))
        self.assertEqual(11,rt.calc(VALUES['sb_court_dynastic_conscript_allocation'],rt.country))

    def test_actual_split_rebuilds_once_for_both_choices_and_geographies(self):
        def state(identity,pop,regular=0,conscript=0):
            buildings=[]
            for kind,levels,pm in (('building_barrack',regular,'pm_general_training'),
                                   ('building_conscription_center',conscript,'pm_sb_customary_muster_conscription')):
                if levels: buildings.append({'type':kind,'level':levels,'vars':{},'production_methods':{pm}})
            buildings.append({'type':'building_naval_base','level':2,'vars':{}})
            return {'id':identity,'vars':{},'state_population':pop,'buildings':buildings}
        for back_prince,rebels_take_army in product((False,True),repeat=2):
            rt,king,prince,*_=court(177,334)
            mainland=state('mainland',1000000,4,17);natal=state('Natal fragment',100000)
            for st in (mainland,natal): st['owner']=rt.country
            rt.country['states']=[mainland,natal]
            self.add_staff(mainland,'peasants',50000,150000)
            reserve(rt,king,prince);answer(rt,back_prince)
            rt.demolitions=[]
            original_state,rebel_state=(natal,mainland) if rebels_take_army else (mainland,natal)
            original_state['owner']=rt.country;rt.country['states']=[original_state]
            # Nothing is destroyed while the movement has no actual native split.
            rt.run('sb_court_rebuild_dynastic_forces')
            self.assertFalse(rt.demolitions)
            _,rebels=split(rt,native_rebel_states=[rebel_state])
            prince_country=rt.country if back_prince else rebels
            king_country=rebels if back_prince else rt.country
            for country,regular,conscript in ((prince_country,2,11),(king_country,2,6)):
                buildings={b['type']:b for st in country['states'] for b in st['buildings']}
                self.assertEqual(regular,buildings['building_barrack']['level'])
                self.assertEqual(conscript,buildings['building_sb_court_muster']['level'])
                self.assertEqual({'pm_general_training'},buildings['building_barrack']['production_methods'])
                self.assertEqual({'pm_sb_customary_muster_conscription'},buildings['building_sb_court_muster']['production_methods'])
                self.assertEqual(2,buildings['building_naval_base']['level'])
            first=list(rt.demolitions)
            rt.run('sb_court_track_dynastic_war');rt.run('sb_court_rebuild_dynastic_forces')
            self.assertEqual(first,rt.demolitions)
            self.assertFalse(any('total' in k or 'largest' in k or 'training' in k for k in rt.country['vars'] if k.startswith(('sb_court_regular_','sb_court_conscript_'))))
            rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win')
            for side in (rt.country,rebels):
                for key in ('sb_court_dynastic_forces_rebuilt_var','sb_court_regular_quota_var','sb_court_conscript_quota_var'):
                    self.assertNotIn(key,side['vars'])

    def test_no_force_rebuild_outside_the_reserved_split(self):
        rt,*_=court()
        rt.country['states']=[{'id':'unrelated','vars':{},'state_population':100000,
                               'buildings':[{'type':'building_barrack','level':20,'vars':{}}]}]
        rt.run('sb_court_rebuild_dynastic_forces')
        self.assertEqual(20,rt.country['states'][0]['buildings'][0]['level'])
        self.assertFalse(hasattr(rt,'demolitions'))

    def test_rebuild_totals_all_states_and_uses_largest_existing_training_method(self):
        rt,king,prince,*_=court(300,100)
        def state(identity,pop,regular,conscript,pm):
            return {'id':identity,'owner':rt.country,'vars':{},'state_population':pop,'buildings':[
                {'type':'building_barrack','level':regular,'vars':{},'production_methods':{pm}},
                {'type':'building_conscription_center','level':conscript,'vars':{},
                 'production_methods':{'pm_no_organization_conscription'}},
                {'type':'building_logging_camp','level':2,'vars':{}}]}
        low=state('small original',100,2,3,'pm_no_organization')
        high=state('large original',200,6,9,'pm_general_training')
        rebel=state('rebel',150,4,8,'pm_no_organization')
        rt.country['states']=[low,high,rebel]
        self.add_staff(low,'peasants',10000,30000)
        self.add_staff(high,'peasants',90000,270000)
        reserve(rt,king,prince);answer(rt)
        rt.country['states']=[low,high]
        _,rebels=split(rt,native_rebel_states=[rebel])
        self.assertEqual(['building_logging_camp'],[b['type'] for b in low['buildings']])
        for country,regular,conscript in ((rt.country,8,15),(rebels,4,5)):
            military={b['type']:b for st in country['states'] for b in st['buildings']
                      if b['type']!='building_logging_camp'}
            self.assertEqual(regular,military['building_barrack']['level'])
            self.assertEqual(conscript,military['building_sb_court_muster']['level'])
            self.assertEqual({'pm_general_training'},military['building_barrack']['production_methods'])
        self.assertEqual(6,sum(b['level'] for st in (low,high,rebel) for b in st['buildings']
                               if b['type']=='building_logging_camp'))

    def test_pair_share_clamps_and_ignores_third_party_uncommitted_and_popularity(self):
        for i,r,want in ((300,100,.25),(200,200,.5),(100,300,.75),(900,1,.1),(1,900,.75)):
            rt,king,prince,third,neutral=court(i,r)
            king['popularity']=-100;prince['popularity']=100
            reserve(rt,king,prince)
            self.assertEqual(i,rt.country['vars']['sb_court_dynastic_incumbent_weight_var'])
            self.assertEqual(r,rt.country['vars']['sb_court_dynastic_rival_weight_var'])
            self.assertAlmostEqual(want,rt.country['vars']['sb_court_dynastic_target_var'])
            self.assertFalse(any(x is third or x is neutral for x in rt.country['sb_court_dynastic_rival_members']))
        rt.country['vars'].update(sb_court_dynastic_incumbent_weight_var=0,sb_court_dynastic_rival_weight_var=0)
        self.assertEqual(0,rt.calc(VALUES['sb_court_dynastic_claimant_share'],rt.country))

    def test_current_and_future_pledges_select_different_houses(self):
        rt,king,prince,third,house=court()
        house['vars'].update(sb_court_endorsement_var=1,sb_court_successor_pledge_scope=prince)
        reserve(rt,king,prince)
        self.assertIn(house,rt.country['sb_court_dynastic_incumbent_members'])
        self.assertEqual(200,rt.country['vars']['sb_court_dynastic_incumbent_weight_var'])
        rt.run('sb_court_cancel_dynastic_crisis')
        rt.run('sb_court_dismiss_dynastic_choice')
        reserve(rt,third,prince,2)
        self.assertIn(house,rt.country['sb_court_dynastic_rival_members'])
        self.assertEqual(200,rt.country['vars']['sb_court_dynastic_rival_weight_var'])

    def test_house_aggregate_once_and_frozen_quotes(self):
        rt,king,prince,_,house=court()
        house['vars'].update(sb_court_endorsement_var=-1,sb_court_claimant_scope=prince)
        junior=character('junior',4,40,1)
        junior['owner']=rt.country;junior['vars']['sb_court_home_scope']=rt.country
        rt.country['members'].append(junior)
        reserve(rt,king,prince)
        self.assertEqual(230,rt.country['vars']['sb_court_dynastic_rival_weight_var']) # 100 + 100 + (40-10)
        self.assertEqual(1,sum(x is junior for x in rt.country['sb_court_dynastic_rival_members']))
        house['prominence']=1;rt.backing()
        self.assertEqual(230,rt.country['vars']['sb_court_dynastic_rival_weight_var'])

    def test_live_thresholds_concurrency_and_strongest_selection(self):
        rt,king,prince,third,_=court(200,100)
        self.assertNotIn('sb_court_dynasty_test_var',rt.country['vars'])
        rt.country['vars']['sb_prerogative_var']=-49.99
        rt.run('sb_court_check_claimant_challenge');self.assertNotIn('sb_court_dynastic_crisis_var',rt.country['vars'])
        rt.country['vars']['sb_prerogative_var']=-50
        for flag in ('coup_event_active','sb_court_civil_war_var','sb_court_action_open_var','sb_court_accession_open_var','sb_court_dynastic_victory_cooldown_var'):
            rt.country['vars'][flag]=1
            rt.run('sb_court_check_claimant_challenge');self.assertNotIn('sb_court_dynastic_crisis_var',rt.country['vars'])
            rt.country['vars'].pop(flag)
        rt.run('sb_court_check_claimant_challenge')
        self.assertIs(prince,rt.country['vars']['sb_court_dynastic_rival_scope'])
        for value,want in ((24.999,False),(25,True)):
            prince['vars']['sb_court_current_share_var']=value
            self.assertEqual(want,rt.condition(TRIGGERS['sb_court_organised_rival'],prince))
        for value,want in ((0,False),(25,False),(29.999,False),(30,True)):
            prince['vars']['sb_court_pledged_share_var']=value
            self.assertEqual(want,rt.condition(TRIGGERS['sb_court_major_candidate'],prince))

    def test_ai_choice_uses_greater_frozen_backing_and_incumbent_tie_break(self):
        event=statements(find_object((ROOT/'events/sb_court_succession_events.txt').read_text(encoding='utf-8-sig'),'sb_court_succession.004'))
        options=[dict((k,v) for k,_,v in body) for key,_,body in event if key=='option'][:2]
        for incumbent,rival,choice in ((300,100,0),(100,300,1),(100,100,0),(100,100.01,1)):
            with self.subTest(incumbent=incumbent,rival=rival):
                rt,king,prince,*_=court(incumbent,rival);reserve(rt,king,prince)
                rt.country['player']=False
                # Live Prominence/Popularity must not change the quoted coalitions.
                king['prominence']=999;prince['prominence']=1
                king['popularity']=100;prince['popularity']=-100
                weights=[]
                for option in options:
                    self.assertTrue(rt.condition(option['trigger'],rt.country))
                    chance=dict((k,v) for k,_,v in option['ai_chance'])
                    modifier=dict((k,v) for k,_,v in chance['modifier'])
                    weights.append(float(chance['base'])+(float(modifier['add']) if rt.condition(modifier['trigger'],rt.country) else 0))
                self.assertEqual([100,0] if choice==0 else [0,100],weights)
                rt.effect(options[choice]['hidden_effect'],rt.country)
                self.assertEqual(choice==1,'sb_court_dynastic_back_claimant_var' in rt.country['vars'])
                _,rebels=split(rt)
                self.assertIs(prince if choice==1 else king,rt.country['ruler'])
                self.assertIs(king if choice==1 else prince,rebels['ruler'])
                self.assertEqual([],getattr(rt,'switches',[]))

    def test_prerogative_follows_incumbent_and_claimant_for_either_country_assignment(self):
        for player,back_claimant,start in product((False,True),(False,True),(-75,25)):
            rt,king,prince,*_=court();rt.country['player']=player
            reserve(rt,king,prince);answer(rt,back_claimant)
            rt.country['vars']['sb_prerogative_var']=start
            _,rebels=split(rt)
            incumbent,claimant=(rebels,rt.country) if back_claimant else (rt.country,rebels)
            self.assertIs(king,incumbent['ruler']);self.assertIs(prince,claimant['ruler'])
            self.assertEqual(start,incumbent['vars']['sb_prerogative_var'])
            self.assertEqual(0,claimant['vars']['sb_prerogative_var'])
            incumbent['vars']['sb_prerogative_var']=start+1
            claimant['vars']['sb_prerogative_var']=12
            rt.run('sb_court_track_dynastic_war')
            self.assertEqual(start+1,incumbent['vars']['sb_prerogative_var'])
            self.assertEqual(12,claimant['vars']['sb_prerogative_var'])
            self.assertNotIn('sb_prerogative_var',rt.scopes['root']['vars'])

    def test_live_contested_death_opens_one_faction_choice_without_manual_opt_in(self):
        rt,king,prince,third,_=court(200,200)
        king['alive']=False;third['prominence']=200
        rt.country['vars']['sb_court_dunn_offer_var']=1
        rt.country['vars']['sb_court_recognized_heir_scope']=prince
        rt.scopes['sb_court_outgoing']=king
        rt.run('sb_court_capture_accession')
        rt.run('sb_court_reconcile_succession')
        rt.run('sb_court_reconcile_succession')
        self.assertEqual(['sb_court_succession.004'],rt.country['events'])
        self.assertIs(prince,rt.country['vars']['sb_court_dynastic_nominee_scope'])
        self.assertIs(third,rt.country['vars']['sb_court_dynastic_rival_scope'])
        self.assertEqual(2,rt.country['vars']['sb_court_dynastic_reason_var'])
        self.assertNotIn('sb_court_dynasty_test_var',rt.country['vars'])

    def test_retirement_uses_the_saved_pledged_distribution_and_opens_both_princes(self):
        # 1 August 1856 checkpoint: 756 represented, 596 pledged, 185/248
        # for Cetshwayo/Mbuyazi. Cetshwayo was only 24.47% of the old total.
        rt,king,cetshwayo,mbuyazi,neutral=court(100,185)
        king['template']='ZUL_mpande_zulu'
        cetshwayo['template']='ZUL_cetshwayo_heir'
        mbuyazi.update(template='ZUL_mbuyazi_heir',prominence=223)
        neutral['prominence']=60
        other=character('third prince',5,138,-1,1)
        other.update(owner=rt.country,template='ZUL_gqugqu_claimant')
        other['vars'].update(sb_court_home_scope=rt.country,sb_court_claimant_scope=other)
        rt.country['members'].append(other)
        rt.country['vars']['sb_court_recognized_heir_scope']=mbuyazi
        rt.country['game_date']=18560731
        rt.backing()
        self.assertEqual(756,rt.country['vars']['sb_court_weight_var'])
        self.assertEqual(596,rt.country['vars']['sb_court_pledged_weight_var'])
        self.assertAlmostEqual(185/596*100,cetshwayo['vars']['sb_court_pledged_share_var'])
        rt.run('sb_court_reconcile_succession')
        self.assertEqual([],rt.country.get('events',[]))
        rt.country['game_date']=18560801
        rt.run('sb_court_reconcile_succession');rt.run('sb_court_reconcile_succession')
        self.assertEqual(['sb_court_succession.004'],rt.country['events'])
        self.assertIs(mbuyazi,rt.country['vars']['sb_court_dynastic_nominee_scope'])
        self.assertIs(cetshwayo,rt.country['vars']['sb_court_dynastic_rival_scope'])
        self.assertEqual(248,rt.country['vars']['sb_court_dynastic_incumbent_weight_var'])
        self.assertEqual(185,rt.country['vars']['sb_court_dynastic_rival_weight_var'])
        self.assertTrue(rt.condition(TRIGGERS['sb_court_mpande_retirement'],rt.country))
        self.assertNotIn('sb_court_retired_var',king['vars'])
        self.assertNotIn('sb_court_dynastic_crisis_var',rt.scopes['root']['vars'])

    def test_open_peaceful_accession_previews_and_routes_a_new_major_rival(self):
        rt,king,nominee,rival,_=court(100,200)
        king['template']='ZUL_mpande_zulu'
        nominee['template']='ZUL_mbuyazi_heir'
        rival['template']='ZUL_cetshwayo_heir'
        rt.country.update(game_date=18560801)
        rt.country['vars']['sb_court_recognized_heir_scope']=nominee
        rt.run('sb_court_reconcile_succession')
        self.assertEqual(['sb_court_succession.001'],rt.country['events'])
        rt.scopes['sb_court_nominee']=nominee
        self.assertTrue(rt.condition(TRIGGERS['sb_court_displayed_accession_valid'],rt.country))
        self.assertFalse(rt.condition(TRIGGERS['sb_court_displayed_accession_contested'],rt.country))
        rival['prominence']=60  # 85/285 = 29.82%, above the old 25% but below 30%.
        rt.backing()
        self.assertFalse(rt.condition(TRIGGERS['sb_court_displayed_accession_contested'],rt.country))
        rival['prominence']=100
        rt.backing()
        self.assertTrue(rt.condition(TRIGGERS['sb_court_displayed_accession_contested'],rt.country))
        rt.run('sb_court_answer_accession');rt.run('sb_court_answer_accession')
        self.assertEqual(['sb_court_succession.001','sb_court_succession.004'],rt.country['events'])
        self.assertIs(king,rt.country['ruler'])
        self.assertFalse(rt.condition(TRIGGERS['sb_court_displayed_accession_valid'],rt.country))

    def test_retirement_presentation_requires_living_incumbent_mpande(self):
        rt,king,prince,*_=court()
        self.assertFalse(rt.condition(TRIGGERS['sb_court_mpande_retirement'],rt.country))
        rt.country['vars']['sb_court_predecessor_scope']=king
        self.assertFalse(rt.condition(TRIGGERS['sb_court_mpande_retirement'],rt.country))
        king['template']='ZUL_mpande_zulu'
        self.assertTrue(rt.condition(TRIGGERS['sb_court_mpande_retirement'],rt.country))
        king['alive']=False
        self.assertFalse(rt.condition(TRIGGERS['sb_court_mpande_retirement'],rt.country))
        king['alive']=True;rt.country['ruler']=prince
        self.assertFalse(rt.condition(TRIGGERS['sb_court_mpande_retirement'],rt.country))

    def test_contested_retirement_removes_mpandes_claim_when_the_princes_take_power(self):
        for back_claimant in (False,True):
            rt,king,prince,third,_=court(200,200)
            king['template']='ZUL_mpande_zulu'
            prince['template']='ZUL_cetshwayo_heir'
            third['template']='ZUL_mbuyazi_heir'
            rt.country['vars']['sb_court_predecessor_scope']=king
            reserve(rt,prince,third,reason=2);answer(rt,back_claimant)
            self.assertNotIn('sb_court_retired_var',king['vars'])
            _,rebels=split(rt)
            self.assertTrue(king['alive']);self.assertTrue(king['retired'])
            self.assertIn('sb_court_claim_renounced_var',king['vars'])
            self.assertNotIn('sb_court_claimant_scope',king['vars'])
            self.assertNotIn('sb_court_claimant_trait',king.get('traits',set()))
            self.assertFalse(rt.condition(TRIGGERS['sb_court_dynastic_candidate'],king))
            self.assertIs(third if back_claimant else prince,rt.country['ruler'])
            self.assertIs(prince if back_claimant else third,rebels['ruler'])
            self.assertTrue(prince['alive']);self.assertTrue(third['alive'])
            rt.run('sb_court_track_dynastic_war');rt.run('sb_court_retire_mpande')
            self.assertTrue(king['alive'])
            rt.run('sb_court_record_dynastic_end')
            rt.run('sb_court_resolve_dynastic_win')
            self.assertTrue(king['alive']);self.assertTrue(king['retired'])
            self.assertNotIn('sb_court_claimant_scope',king['vars'])
            self.assertNotIn('sb_court_claimant_trait',king.get('traits',set()))
            self.assertFalse(rt.condition(TRIGGERS['sb_court_dynastic_candidate'],king))

    def test_movement_once_exact_demand_and_exact_organising_object(self):
        rt,king,prince,_,_=court();reserve(rt,king,prince);answer(rt)
        answer(rt);self.assertEqual(1,len(rt.country['movements']))
        own=organising_war(rt)
        unrelated={'id':'other','type':'revolution','vars':{},'political_movement':{'id':'other-movement'},'progress':0}
        rt.country['wars'].insert(0,unrelated)
        own['political_movement']['most_desired_law']='law_type:law_monarchy'
        rt.run('sb_court_progress_dynastic_crisis');self.assertEqual(0,own['progress'])
        own['political_movement']['most_desired_law']='law_type:law_sb_contested_crown'
        rt.run('sb_court_progress_dynastic_crisis');rt.run('sb_court_progress_dynastic_crisis')
        self.assertEqual(1,own['progress']);self.assertEqual(0,unrelated['progress'])
        self.assertIs(own,rt.country['vars']['sb_court_dynastic_preparing_war_scope'])

    def test_dead_displayed_participant_cancels_without_substitution(self):
        rt,king,prince,third,_=court();reserve(rt,king,prince)
        prince['alive']=False;answer(rt,True)
        self.assertNotIn('sb_court_dynastic_crisis_var',rt.country['vars'])
        self.assertEqual([],rt.country['movements']);self.assertTrue(third['alive'])

    def test_claimant_activism_growth_is_local_and_removed_on_cancellation(self):
        rt,king,prince,_,_=court()
        unrelated={'id':'ordinary movement','type':'movement_sb_zulu_royal','owner':rt.country,'vars':{}}
        rt.country['movements'].append(unrelated)
        reserve(rt,king,prince);answer(rt)
        claimant=rt.country['vars']['sb_court_dynastic_movement_scope']
        self.assertIn('sb_court_claimant_mobilisation',claimant['modifiers'])
        self.assertNotIn('sb_court_claimant_mobilisation',unrelated.get('modifiers',{}))
        self.assertNotIn('sb_court_claimant_mobilisation',rt.country.get('modifiers',{}))
        rt.run('sb_court_cancel_dynastic_crisis')
        self.assertNotIn('sb_court_claimant_mobilisation',claimant['modifiers'])

    def test_frozen_house_side_commander_transfer_keeps_selected_prince_in_main_tag(self):
        rt,king,prince,third,house=court();house['general']=True
        house['vars'].update(sb_court_endorsement_var=-1,sb_court_claimant_scope=prince)
        reserve(rt,king,prince);answer(rt,True)
        house['vars']['sb_court_endorsement_var']=0 # Quote remains authoritative through the split.
        _,rebels=split(rt);rt.run('sb_court_track_dynastic_war')
        self.assertIs(house['owner'],rt.country);self.assertTrue(house['general'])
        self.assertIs(king,rebels['ruler']);self.assertIs(prince,rt.country['ruler'])
        self.assertEqual(1,house['vars']['sb_court_endorsement_var'])
        self.assertNotIn('sb_court_claimant_scope',house['vars'])
        self.assertIs(third['vars']['sb_court_claimant_scope'],third)
        self.assertEqual([],getattr(rt,'switches',[]))
        self.assertTrue(rt.country['player'])

    def test_split_and_monthly_reconciliation_use_the_original_countrys_war_list(self):
        rt,king,prince,_,_=court();reserve(rt,king,prince);answer(rt)
        war,rebels=split(rt)
        for side in (rt.country,rebels):
            self.assertIs(war,side['vars'].get('sb_court_dynastic_war_scope'))
            rt.run('sb_court_reconcile_dynastic_record',side)
            self.assertIs(war,side['vars'].get('sb_court_dynastic_war_scope'))
        self.assertIs(prince,rebels['ruler'])
        self.assertIs(king,rt.country['ruler'])

    def test_generated_heads_die_but_frozen_princes_and_children_survive_both_choices(self):
        for back_claimant in (False,True):
            for generated in (False,True):
                with self.subTest(back_claimant=back_claimant,generated=generated):
                    rt,king,prince,third,_=court()
                    child=character('Cetshwayo',0,0,age=4)
                    child['template']='ZUL_cetshwayo_heir'
                    child['owner']=rt.country;child['vars']['sb_court_home_scope']=rt.country
                    rt.country['members'].append(child)
                    reserve(rt,king,prince);answer(rt,back_claimant)
                    native_ruler=character('generated ruler',0,50) if generated else third
                    native_heir=character('generated heir',0,0,age=2) if generated else child
                    _,rebels=split(rt,native_ruler=native_ruler,native_heir=native_heir)
                    self.assertEqual(not generated,native_ruler['alive'])
                    self.assertEqual(not generated,native_heir['alive'])
                    self.assertTrue(all(c['alive'] for c in (king,prince,third,child)))
                    self.assertIs(prince if back_claimant else king,rt.country['ruler'])
                    self.assertIs(king if back_claimant else prince,rebels['ruler'])
                    for side in (rt.country,rebels):
                        # A faction with only its own contender still blocks generated heirs.
                        side['members']=[side['ruler']]
                        rt.run('sb_court_update_heir_blocker',side)
                        rt.run('sb_court_set_dynastic_head',side)
                        self.assertIn('no_heirs',side['vars'])
                        self.assertIs(side['ruler'],side['vars']['sb_court_incumbent_scope'])
                        self.assertFalse(any(k.startswith('sb_court_dynastic_generated_') for k in side['vars']))

    def test_late_generated_ruler_is_replaced_without_changing_the_recorded_faction(self):
        for back_claimant in (False,True):
            rt,king,prince,_,_=court();reserve(rt,king,prince);answer(rt,back_claimant)
            _,rebels=split(rt)
            handler=statements(find_object((ROOT/'common/on_actions/sb_court_on_actions.txt').read_text(encoding='utf-8-sig'),'sb_court_on_ruler_selected'))
            body=dict((k,v) for k,_,v in handler)['effect']
            for side in (rt.country,rebels):
                generated=character('late native ruler',0,50);generated['owner']=side
                side['ruler']=generated
                rt.effect(body,generated)
                self.assertFalse(generated['alive'])
                self.assertIs(side['vars']['sb_court_dynastic_candidate_scope'],side['ruler'])
                self.assertNotIn('sb_court_selecting_head_var',side['vars'])

    def test_rebel_target_tracks_the_opposing_coalition_for_each_player_choice(self):
        for incumbent,claimant in ((300,100),(200,200),(100,300),(900,1),(1,900)):
            for back_claimant in (False,True):
                with self.subTest(incumbent=incumbent,claimant=claimant,back_claimant=back_claimant):
                    rt,king,prince,_,_=court(incumbent,claimant);reserve(rt,king,prince)
                    # A changed live coalition must not change the reserved allocation.
                    king['prominence']=1;prince['prominence']=1
                    answer(rt,back_claimant)
                    rebel_share=(incumbent if back_claimant else claimant)/(incumbent+claimant)
                    self.assertAlmostEqual(max(.10,min(.75,rebel_share)),rt.country['vars']['sb_court_dynastic_target_var'])

    def test_third_party_and_unrepresented_patron_survive_native_physical_allocation(self):
        rt,king,prince,third,neutral=court()
        adviser=character('unrepresented adviser',0,5,1)
        adviser['owner']=rt.country;adviser['vars']['sb_court_home_scope']=rt.country
        rt.country['members'].append(adviser)
        reserve(rt,king,prince);answer(rt)
        _,rebels=split(rt,(third,neutral,adviser))
        self.assertIs(third['vars']['sb_court_claimant_scope'],third)
        self.assertEqual(-1,third['vars']['sb_court_endorsement_var'])
        self.assertEqual(0,neutral['vars']['sb_court_endorsement_var'])
        self.assertNotIn('sb_court_claimant_scope',adviser['vars'])
        self.assertEqual(1,adviser['vars']['sb_court_endorsement_var'])
        self.assertIs(rt.country,adviser['owner']) # Even a zero-weight pledged adviser follows his side.
        self.assertIs(rt.country,adviser['vars']['sb_court_home_scope'])

    def test_each_choice_adds_only_rival_agitator_and_cancellation_preserves_existing_role(self):
        for rebels in (False,True):
            for already_agitator in (False,True):
                rt,king,prince,third,_=court()
                prince['agitator']=already_agitator
                prince['ideology']='ideology_moderate'
                reserve(rt,king,prince)
                quote=rt.country['vars']['sb_court_dynastic_target_var']
                answer(rt,rebels);answer(rt,rebels)
                self.assertTrue(prince['agitator'])
                self.assertFalse(king['agitator']);self.assertFalse(third['agitator'])
                self.assertEqual('ideology_moderate',prince['ideology'])
                self.assertEqual(quote,rt.country['vars']['sb_court_dynastic_target_var'])
                source=(ROOT/'common/political_movements/sb_court_dynastic_test.txt').read_text(encoding='utf-8-sig')
                support=statements(child(source,'character_support_trigger'))
                for actor in (king,prince,third):
                    self.assertEqual(actor is prince,rt.condition(support,actor))
                rt.run('sb_court_cancel_dynastic_crisis')
                self.assertEqual(already_agitator,prince['agitator'])
                self.assertFalse(any(k.startswith('sb_court_dynastic_') for k in prince['vars']))

    def test_progress_waits_for_named_prince_to_join_the_exact_movement(self):
        rt,king,prince,_,_=court();reserve(rt,king,prince);answer(rt)
        war=organising_war(rt)
        prince.pop('political_movement')
        rt.run('sb_court_progress_dynastic_crisis');self.assertEqual(0,war['progress'])
        prince['political_movement']={'id':'different'}
        rt.run('sb_court_progress_dynastic_crisis');self.assertEqual(0,war['progress'])
        prince['political_movement']=war['political_movement']
        rt.run('sb_court_progress_dynastic_crisis');self.assertEqual(1,war['progress'])

    def test_victory_removes_only_new_defeated_ig_penalties_for_either_winner(self):
        for back_claimant,rebel_win in product((False,True),repeat=2):
            rt,king,prince,*_=court()
            old={'strength':-.25,'expiry':'1844.1.1'}
            rt.country['ig:ig_devout']['modifiers']['revolution_lost_ig']=old
            rt.country['ig:ig_landowners']['modifiers']['modifier_patronized_politician']=.1
            reserve(rt,king,prince);answer(rt,back_claimant)
            _,rebels=split(rt)
            winner=rebels if rebel_win else rt.country
            self.assertIn('sb_court_dynastic_prior_defeat_var',winner['ig:ig_devout']['vars'])
            # Native OnRevolutionEnd has already added the current conflict's penalties.
            for kind in ('ig_armed_forces','ig_rural_folk'):
                winner['ig:'+kind]['modifiers']['revolution_lost_ig']=-1
            rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win',winner)
            self.assertEqual(old,winner['ig:ig_devout']['modifiers']['revolution_lost_ig'])
            self.assertEqual(.1,winner['ig:ig_landowners']['modifiers']['modifier_patronized_politician'])
            for kind in ('ig_armed_forces','ig_rural_folk'):
                self.assertNotIn('revolution_lost_ig',winner['ig:'+kind]['modifiers'])
            for side in (rt.country,rebels):
                self.assertNotIn('sb_court_dynastic_igs_snapshotted_var',side['vars'])
                for kind in IG_TYPES:
                    self.assertNotIn('sb_court_dynastic_prior_defeat_var',side['ig:'+kind]['vars'])
                    self.assertNotIn('sb_court_claimant_armed_forces',side['ig:'+kind]['modifiers'])
            rt.run('sb_court_resolve_dynastic_win',winner)
            self.assertEqual(old,winner['ig:ig_devout']['modifiers']['revolution_lost_ig'])
            self.assertFalse(any(k.startswith('ig:') for k in rt.scopes['root']))

    def test_cancellation_or_missing_snapshot_does_not_erase_existing_ig_penalty(self):
        for cancel in (False,True):
            rt,king,prince,*_=court();reserve(rt,king,prince);answer(rt)
            rt.country['ig:ig_devout']['modifiers']['revolution_lost_ig']=-.4
            if cancel: rt.run('sb_court_cancel_dynastic_crisis')
            else:
                _,rebels=split(rt)
                rt.country['vars'].pop('sb_court_dynastic_igs_snapshotted_var')
                rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win')
            self.assertEqual(-.4,rt.country['ig:ig_devout']['modifiers']['revolution_lost_ig'])

    def test_victory_prerogative_is_capped_and_paid_once_only_on_option_click(self):
        core=definitions('common/scripted_effects/sb_institutions_effects.txt')
        values=definitions('common/script_values/sb_institutions_values.txt')
        event=statements(find_object((ROOT/'events/sb_court_succession_events.txt').read_text(encoding='utf-8-sig'),'sb_court_succession.005'))
        option=next(v for k,_,v in event if k=='option')
        option=[n for n in option if n[0] not in ('name','default_option','custom_tooltip')]
        # Existing IR/lifecycle tests cover eligibility and initialisation; execute
        # the shipped payment and clamp with an already initialised eligible court.
        with patch.dict(EFFECTS,{'sb_change_prerogative':core['sb_change_prerogative'],'sb_institutions_initialize':[]}), \
             patch.dict(VALUES,{'sb_prerogative_clamped':values['sb_prerogative_clamped']}), \
             patch.dict(TRIGGERS,{'sb_institutions_eligible':[('always','=','yes')]}):
            for rebel_win,start in product((False,True),(-75,-50,95,100)):
                rt,king,prince,*_=court();reserve(rt,king,prince);answer(rt)
                _,rebels=split(rt);winner=rebels if rebel_win else rt.country
                winner['vars']['sb_prerogative_var']=start
                rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win',winner)
                self.assertEqual(start,winner['vars']['sb_prerogative_var'])
                self.assertEqual(1,winner['events'].count('sb_court_succession.005'))
                rt.effect(option,winner)
                self.assertEqual(min(100,start+10),winner['vars']['sb_prerogative_var'])
                rt.effect(option,winner);rt.run('sb_court_resolve_dynastic_win',winner)
                self.assertEqual(min(100,start+10),winner['vars']['sb_prerogative_var'])
                self.assertNotIn('sb_court_dynastic_victory_scope',winner['vars'])
                self.assertNotIn('sb_prerogative_var',rt.scopes['root']['vars'])

    def test_victory_protects_actual_winner_before_popup_and_expires_without_refresh(self):
        cooldown='sb_court_dynastic_victory_cooldown_var'
        for back_claimant,rebel_win in product((False,True),repeat=2):
            rt,king,prince,*_=court();reserve(rt,king,prince);answer(rt,back_claimant)
            _,rebels=split(rt)
            winner,loser=(rebels,rt.country) if rebel_win else (rt.country,rebels)
            rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win',winner)
            self.assertIn(cooldown,winner['vars'])
            self.assertNotIn(cooldown,loser['vars'])
            self.assertNotIn(cooldown,rt.scopes['root']['vars'])
            winner['wars']=[]  # Native removal of the ended conflict.
            winner['vars']['sb_prerogative_var']=-75
            self.assertFalse(rt.condition(TRIGGERS['sb_court_dynastic_can_challenge'],winner))
            # An unanswered victory popup does not postpone protection.
            self.assertIn('sb_court_dynastic_victory_scope',winner['vars'])
            rt.run('sb_court_resolve_dynastic_win',winner)
            self.assertEqual([(cooldown,18)],[x for x in winner['timed_writes'] if x[0]==cooldown])
            winner['vars'].pop(cooldown)  # Native timed-variable expiry.
            self.assertTrue(rt.condition(TRIGGERS['sb_court_dynastic_can_challenge'],winner))

    def test_cancelled_crisis_has_no_victory_protection(self):
        rt,king,prince,*_=court();reserve(rt,king,prince);answer(rt)
        rt.run('sb_court_cancel_dynastic_crisis')
        self.assertNotIn('sb_court_dynastic_victory_cooldown_var',rt.country['vars'])

    def test_full_snapshot_restores_survivors_and_executes_frozen_house_members(self):
        for back_claimant,rebel_win in product((False,True),repeat=2):
            rt,king,prince,third,ndlela=court()
            ndlela['id']='Ndlela kaSompisi';ndlela['vars']['sb_court_endorsement_var']=1
            child=character('Cetshwayo',0,0,age=4)
            child['template']='ZUL_cetshwayo_heir'
            child['vars']['sb_court_successor_pledge_scope']=third
            neutral=character('uncommitted adviser',0,5)
            junior=character('Ndlela house member',4,20)
            supporter=character('Mpande backer',7,50,-1)
            supporter['vars'].update(sb_court_claimant_scope=prince,sb_court_successor_pledge_scope=third)
            natural=character('natural death',0,0)
            for actor in (child,neutral,junior,supporter,natural):
                actor['owner']=rt.country;actor['vars']['sb_court_home_scope']=rt.country
                rt.country['members'].append(actor)
            reserve(rt,king,prince);answer(rt,back_claimant)
            snapshot=rt.country['sb_court_dynastic_roster']
            self.assertEqual(len(snapshot),len({id(x) for x in snapshot}))
            _,rebels=split(rt,(third,child,neutral))
            natural['alive']=False
            # Native removal/allocation must not turn this into a different political court.
            for actor in (third,child,neutral,supporter):
                actor['vars'].update(sb_court_following_var=999,sb_court_alignment_var=2,sb_court_endorsement_var=1,sb_court_claimant_scope=king)
                actor['vars'].pop('sb_court_successor_pledge_scope',None)
            third['is_in_void']=True
            neutral['is_in_exile_pool']=True
            rt.country['members']=[];rebels['members']=[]
            rt.run('sb_court_record_dynastic_end')
            winner=rebels if rebel_win else rt.country
            loser=rt.country if rebel_win else rebels
            prince_win=back_claimant != rebel_win
            rt.run('sb_court_resolve_dynastic_win',winner)
            rt.run('sb_court_resolve_dynastic_win',winner)
            for actor in (king,ndlela,junior): self.assertEqual(not prince_win,actor['alive'],actor['id'])
            for actor in (prince,supporter): self.assertEqual(prince_win,actor['alive'],actor['id'])
            for actor in (third,child,neutral):
                self.assertTrue(actor['alive']);self.assertIs(winner,actor['owner'])
                self.assertIs(winner,actor['vars']['sb_court_home_scope'])
                self.assertFalse(any(k.startswith('sb_court_dynastic_') for k in actor['vars']))
            self.assertIs(third,third['vars']['sb_court_claimant_scope'])
            self.assertEqual(-1,third['vars']['sb_court_endorsement_var'])
            self.assertEqual(3,third['vars']['sb_court_following_var'])
            self.assertEqual(1,third['vars']['sb_court_alignment_var'])
            self.assertIs(third,child['vars']['sb_court_successor_pledge_scope'])
            self.assertEqual(0,neutral['vars']['sb_court_endorsement_var'])
            self.assertNotIn('sb_court_claimant_scope',neutral['vars'])
            self.assertFalse(third['is_in_void']);self.assertFalse(neutral['is_in_exile_pool'])
            self.assertFalse(natural['alive'])
            # Characters of the abolished country would be killed by native DeathCleanup.
            self.assertFalse(any(x['alive'] and x['owner'] is loser for x in snapshot))
            self.assertEqual(1,winner['events'].count('sb_court_succession.005'))

    def test_unregistered_cast_survives_without_fabricated_court_records(self):
        rt,king,prince,_,_=court()
        outsider={'id':'new local character','alive':True,'vars':{},'owner':rt.country}
        rt.country['characters']=list(rt.country['members'])+[outsider]
        reserve(rt,king,prince);answer(rt);_,rebels=split(rt)
        rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win',rebels)
        self.assertTrue(outsider['alive']);self.assertIs(rebels,outsider['owner'])
        self.assertEqual({},outsider['vars'])

    def test_succession_war_uses_future_pledges_for_the_death_roster(self):
        rt,old_king,nominee,rival,backer=court()
        old_king['alive']=False
        backer['vars'].update(sb_court_endorsement_var=-1,sb_court_claimant_scope=rival,sb_court_successor_pledge_scope=nominee)
        rival_backer=character('next reign rival backer',7,70,1)
        rival_backer['owner']=rt.country
        rival_backer['vars'].update(sb_court_home_scope=rt.country,sb_court_successor_pledge_scope=rival)
        rt.country['members'].append(rival_backer)
        reserve(rt,nominee,rival,2);answer(rt);_,rebels=split(rt)
        self.assertTrue(any(x is backer for x in rt.country['sb_court_dynastic_incumbent_members']))
        self.assertTrue(any(x is rival_backer for x in rt.country['sb_court_dynastic_rival_members']))
        rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win',rebels)
        self.assertFalse(nominee['alive']);self.assertFalse(backer['alive'])
        self.assertTrue(rival_backer['alive']);self.assertIs(rival,rebels['ruler'])
        self.assertEqual(1,rival_backer['vars']['sb_court_endorsement_var'])

    def test_preexisting_void_and_foreign_exile_are_not_summoned_or_reset(self):
        rt,king,prince,third,neutral=court()
        third['is_in_void']=True
        neutral['owner']={'id':'CAP','vars':{}}
        neutral['is_in_exile_pool']=True
        old_owner=neutral['owner']
        rt.country['characters']=[king,prince,third]
        reserve(rt,king,prince);answer(rt);_,rebels=split(rt)
        rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win',rebels)
        self.assertTrue(third['is_in_void']);self.assertIs(rebels,third['owner'])
        self.assertTrue(neutral['is_in_exile_pool']);self.assertIs(old_owner,neutral['owner'])

    def test_ai_has_same_conflict_without_play_as(self):
        rt,king,prince,_,_=court();rt.country['player']=False
        reserve(rt,king,prince);answer(rt,True);_,rebels=split(rt)
        self.assertIs(prince,rt.country['ruler']);self.assertIs(king,rebels['ruler'])
        self.assertEqual([],getattr(rt,'switches',[]))

    def test_supply_assistance_follows_ai_control_of_actual_factions(self):
        modifier='sb_court_dynastic_ai_supply'
        for back_claimant in (False,True):
            rt,king,prince,_,_=court();reserve(rt,king,prince);answer(rt,back_claimant)
            rt.run('sb_court_reconcile_dynastic_supply')
            self.assertNotIn(modifier,rt.country.get('modifiers',{}))
            _,rebels=split(rt)
            self.assertNotIn(modifier,rt.country.get('modifiers',{}))
            self.assertEqual(1,rebels['modifiers'][modifier])
            rt.country['player']=False;rebels['player']=True
            for _ in range(2):
                rt.run('sb_court_reconcile_dynastic_record')
                rt.run('sb_court_reconcile_dynastic_record',rebels)
            self.assertEqual(1,rt.country['modifiers'][modifier])
            self.assertNotIn(modifier,rebels['modifiers'])
            rt.run('sb_court_reconcile_dynastic_supply',rt.scopes['root'])
            self.assertNotIn(modifier,rt.scopes['root'].get('modifiers',{}))

    def test_ai_supply_ends_with_exact_war_or_missing_war_recovery(self):
        modifier='sb_court_dynastic_ai_supply'
        for lost_record in (False,True):
            rt,king,prince,_,_=court();rt.country['player']=False
            reserve(rt,king,prince);answer(rt);_,rebels=split(rt)
            for side in (rt.country,rebels): self.assertEqual(1,side['modifiers'][modifier])
            rt.scopes['target']={'id':'unrelated','vars':{}}
            rt.run('sb_court_record_dynastic_end')
            for side in (rt.country,rebels): self.assertIn(modifier,side['modifiers'])
            if lost_record:
                rt.country['wars']=[]
                rt.run('sb_court_reconcile_dynastic_record',rebels)
            else:
                rt.scopes['target']=rebels
                rt.run('sb_court_record_dynastic_end')
            for side in (rt.country,rebels): self.assertNotIn(modifier,side['modifiers'])

    def test_pending_or_cancelled_crisis_gets_no_ai_supply(self):
        rt,king,prince,_,_=court();rt.country['player']=False
        reserve(rt,king,prince);answer(rt);organising_war(rt)
        rt.run('sb_court_reconcile_dynastic_record')
        self.assertNotIn('sb_court_dynastic_ai_supply',rt.country.get('modifiers',{}))
        rt.run('sb_court_cancel_dynastic_crisis')
        self.assertNotIn('sb_court_dynastic_ai_supply',rt.country.get('modifiers',{}))

    def test_both_actual_winners_restore_law_preserve_third_prince_and_do_not_award_partition(self):
        for back_claimant,rebel_win in product((False,True),repeat=2):
            for social in (False,True):
                rt,king,prince,third,king_backer=court()
                king_backer['vars']['sb_court_endorsement_var']=1
                rival_backer=character('rival house',7,45,-1)
                rival_backer['owner']=rt.country
                rival_backer['vars'].update(sb_court_home_scope=rt.country,sb_court_claimant_scope=prince)
                rt.country['members'].append(rival_backer)
                original='law_type:law_social_monarchy' if social else 'law_type:law_monarchy'
                rt.country['laws']={original,'law_type:law_autocracy'}
                reserve(rt,king,prince);answer(rt,back_claimant);_,rebels=split(rt)
                self.assertIn('law_type:law_sb_contested_social_crown' if social else 'law_type:law_sb_contested_crown',rebels['laws'])
                rt.run('sb_court_record_dynastic_end')
                winner=rebels if rebel_win else rt.country
                prince_win=back_claimant != rebel_win
                rt.run('sb_court_resolve_dynastic_win',winner)
                rt.run('sb_court_resolve_dynastic_win',winner)
                self.assertIs(prince if prince_win else king,winner['ruler'])
                self.assertFalse((king if prince_win else prince)['alive']);self.assertTrue(third['alive'])
                self.assertEqual(1,(rival_backer if prince_win else king_backer)['vars']['sb_court_endorsement_var'])
                self.assertFalse((king_backer if prince_win else rival_backer)['alive'])
                self.assertTrue((rival_backer if prince_win else king_backer)['alive'])
                for side in (rt.country,rebels):
                    self.assertIn(original,side['laws'])
                    self.assertNotIn('sb_court_dynastic_crisis_var',side['vars'])
                    self.assertNotIn('sb_court_dynastic_ai_supply',side.get('modifiers',{}))
                    self.assertNotIn('sb_zululand_contest_result_var',side['vars'])
                    self.assertEqual({'ideology_patriotic','ideology_jingoist'},side['ig:ig_armed_forces']['ideologies'])
                    for kind in IG_TYPES:
                        ig=side['ig:'+kind]
                        self.assertNotIn('sb_court_claimant_armed_forces',ig['modifiers'])
                        self.assertNotIn('ideology_sb_contested_crown',ig['ideologies'])
                        self.assertNotIn('ideology_sb_contested_social_crown',ig['ideologies'])
                self.assertEqual(1,winner.get('events',[]).count('sb_court_succession.005'))

    def test_unrelated_end_cannot_resolve_and_abandoned_war_has_no_winner(self):
        rt,king,prince,_,_=court();reserve(rt,king,prince);answer(rt);_,rebels=split(rt)
        rt.scopes['target']={'id':'unrelated','vars':{}}
        rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win')
        self.assertTrue(king['alive'] and prince['alive']);self.assertIn('sb_court_dynastic_crisis_var',rt.country['vars'])
        rt.country['wars']=[];rebels['wars']=[]
        rt.run('sb_court_reconcile_dynastic_record')
        self.assertTrue(king['alive'] and prince['alive'])
        self.assertIn('law_type:law_monarchy',rebels['laws'])
        self.assertNotIn('sb_court_dynastic_resolved_var',rt.country['vars'])

    def test_unrelated_split_does_not_claim_our_organising_revolution(self):
        rt,king,prince,_,_=court();reserve(rt,king,prince);answer(rt)
        organising_war(rt)
        rt.scopes['target']={'id':'other-rebels','vars':{'civil_war_type_var':'movement_type:movement_absolutist'},
                             'civil_war_origin_country':rt.country,'wars':[]}
        rt.run('sb_court_track_dynastic_war')
        self.assertNotIn('sb_court_dynastic_war_scope',rt.country['vars'])
        self.assertEqual([],getattr(rt,'switches',[]))

    def test_purge_exposure_reserves_the_displayed_rival_without_a_rolled_winner(self):
        rt,king,prince,third,_=court()
        rt.country['vars'].update(sb_court_action_actor_scope=prince,sb_court_offer_rival_share_var=25)
        rt.run('sb_court_coercion_exposed')
        self.assertIs(prince,rt.country['vars']['sb_court_dynastic_rival_scope'])
        self.assertEqual(3,rt.country['vars']['sb_court_dynastic_reason_var'])
        self.assertTrue(king['alive'] and prince['alive'] and third['alive'])
        self.assertEqual(['sb_court_succession.004'],rt.country['events'])

    def test_minority_contest_preserves_child_and_replaces_dead_regent(self):
        rt,king,child,rival,head=court()
        child['age']=2;child['template']='ZUL_uthumbu_claimed_son'
        head['vars']['sb_court_successor_pledge_scope']=child
        second=character('second pledged house',8,80)
        second['owner']=rt.country
        second['vars'].update(sb_court_home_scope=rt.country,sb_court_successor_pledge_scope=child)
        rt.country['members'].append(second)
        rt.country['vars']['sb_court_recognized_heir_scope']=child
        reserve(rt,child,rival,2);answer(rt);_,rebels=split(rt)
        self.assertIs(head,rt.country['ruler']);self.assertIs(child,rt.country['heir'])
        self.assertNotIn('sb_court_representative_var',child['vars'])
        head['alive']=False
        rt.run('sb_court_set_dynastic_head')
        self.assertIs(second,rt.country['ruler']);self.assertIs(child,rt.country['heir'])
        self.assertTrue(child['alive'])

    def test_contender_death_during_war_does_not_cancel_or_create_victory(self):
        rt,king,prince,third,_=court();reserve(rt,king,prince);answer(rt);_,rebels=split(rt)
        prince['alive']=False
        rt.run('sb_court_reconcile_dynastic_record')
        self.assertIn('sb_court_dynastic_war_scope',rt.country['vars'])
        self.assertTrue(king['alive'])
        rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win',rebels)
        self.assertNotIn('sb_court_succession.005',rebels.get('events',[]))
        self.assertIs(third,rebels['vars']['sb_court_accession_nominee_scope'])
        self.assertIn('sb_court_succession.001',rebels['events'])

    def test_installed_incumbent_keeps_heir_but_losing_roster_has_no_exile_exception(self):
        rt,king,prince,third,_=court()
        rt.country['vars']['sb_court_recognized_heir_scope']=third
        rt.country['vars']['sb_court_privileges_this_reign_var']=1
        reserve(rt,king,prince);answer(rt);_,rebels=split(rt)
        prince['is_in_exile_pool']=True
        rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win')
        self.assertFalse(prince['alive'])
        self.assertIs(third,rt.country['vars']['sb_court_recognized_heir_scope'])
        self.assertIn('sb_court_privileges_this_reign_var',rt.country['vars'])
        self.assertNotIn('coup_event_active',rt.country['vars'])

    def test_institutional_exit_and_missing_movement_cancel_pending_once(self):
        for invalidation in ('institutions','movement'):
            rt,king,prince,_,_=court();reserve(rt,king,prince);answer(rt)
            if invalidation=='institutions': rt.country['vars'].pop('sb_institutions_active_var')
            else: rt.country['vars'].pop('sb_court_dynastic_movement_scope')
            rt.run('sb_court_progress_dynastic_crisis');rt.run('sb_court_progress_dynastic_crisis')
            self.assertNotIn('sb_court_dynastic_crisis_var',rt.country['vars'])
            self.assertNotIn('coup_event_active',rt.country['vars'])
            self.assertEqual(1,len(rt.country['movements']))
            self.assertTrue(king['alive'] and prince['alive'])

    def test_sponsor_is_confined_to_the_answered_crisis_and_preserves_leaders(self):
        for social in (False,True):
            rt,king,prince,_,_=court()
            if social: rt.country['laws']={'law_type:law_social_monarchy','law_type:law_autocracy'}
            originals={kind:set(rt.country['ig:'+kind]['ideologies']) for kind in IG_TYPES}
            leaders={kind:dict(rt.country['ig:'+kind]['leader']) for kind in IG_TYPES}
            foreign={'id':'foreign-AF','type':'ig_armed_forces','vars':{},'ideologies':{'ideology_jingoist'},'modifiers':{}}
            rt.scopes['root']['ig:ig_armed_forces']=foreign
            rt.run('sb_court_reconcile_claimant_sponsor')
            for kind in IG_TYPES: self.assertEqual(originals[kind],rt.country['ig:'+kind]['ideologies'])
            reserve(rt,king,prince)
            rt.run('sb_court_reconcile_claimant_sponsor')
            for kind in IG_TYPES:
                self.assertEqual(originals[kind],rt.country['ig:'+kind]['ideologies'])
                self.assertEqual({},rt.country['ig:'+kind]['modifiers']) # open choice has no penalty
            quote=rt.country['vars']['sb_court_dynastic_target_var']
            answer(rt)
            expected='ideology_sb_contested_social_crown' if social else 'ideology_sb_contested_crown'
            for kind in IG_TYPES:
                self.assertEqual(originals[kind]|{expected},rt.country['ig:'+kind]['ideologies'])
                self.assertEqual({'sb_court_claimant_armed_forces':1},rt.country['ig:'+kind]['modifiers'])
            for _ in range(3): rt.run('sb_court_progress_dynastic_crisis')
            for kind in IG_TYPES:
                self.assertEqual(originals[kind]|{expected},rt.country['ig:'+kind]['ideologies'])
                self.assertEqual({'sb_court_claimant_armed_forces':1},rt.country['ig:'+kind]['modifiers'])
                self.assertEqual(leaders[kind],rt.country['ig:'+kind]['leader'])
            self.assertEqual({'ideology_jingoist'},foreign['ideologies'])
            self.assertEqual({},foreign['modifiers'])
            self.assertEqual(quote,rt.country['vars']['sb_court_dynastic_target_var'])
            rt.run('sb_court_cancel_dynastic_crisis')
            for kind in IG_TYPES:
                self.assertEqual(originals[kind],rt.country['ig:'+kind]['ideologies'])
                self.assertEqual({},rt.country['ig:'+kind]['modifiers'])

    def test_split_does_not_transfer_characters_to_their_existing_country(self):
        for backing_prince in (False,True):
            rt,king,prince,*_=court();reserve(rt,king,prince);answer(rt,backing_prince)
            split(rt)
            self.assertTrue(rt.transfers)
            for actor,old,new in rt.transfers: self.assertNotEqual(old,new,actor)

    def test_victory_transfers_only_survivors_owned_by_another_country(self):
        for backing_prince,rebel_win in product((False,True),repeat=2):
            with self.subTest(backing_prince=backing_prince,rebel_win=rebel_win):
                rt,king,prince,third,_=court();reserve(rt,king,prince);answer(rt,backing_prince)
                _,rebels=split(rt,(third,))
                winner=rebels if rebel_win else rt.country
                rt.run('sb_court_record_dynastic_end')
                rt.transfers=[]
                rt.run('sb_court_resolve_dynastic_win',winner)
                for actor,old,new in rt.transfers: self.assertNotEqual(old,new,actor)
                self.assertTrue(third['alive']);self.assertIs(winner,third['owner'])
                count=len(rt.transfers)
                rt.run('sb_court_resolve_dynastic_win',winner)
                self.assertEqual(count,len(rt.transfers))

    def test_either_side_choice_keeps_approval_cost_until_resolution(self):
        for back_prince,inherit in product((False,True),repeat=2):
            rt,king,prince,*_=court();reserve(rt,king,prince);answer(rt,back_prince)
            _,rebels=split(rt,inherit_sponsor=inherit)
            for side in (rt.country,rebels):
                for kind in IG_TYPES: self.assertEqual(1,side['ig:'+kind]['modifiers']['sb_court_claimant_armed_forces'])
            rt.run('sb_court_reconcile_dynastic_record')
            for kind in IG_TYPES: self.assertEqual(1,rt.country['ig:'+kind]['modifiers']['sb_court_claimant_armed_forces'])
            rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win')
            for side in (rt.country,rebels):
                for kind in IG_TYPES: self.assertNotIn('sb_court_claimant_armed_forces',side['ig:'+kind]['modifiers'])

    def test_both_displayed_options_apply_the_all_ig_penalty(self):
        source=(ROOT/'events/sb_court_succession_events.txt').read_text(encoding='utf-8-sig')
        event=statements(find_object(source,'sb_court_succession.004'))
        for suffix in ('a','b'):
            option=next(v for k,_,v in event if k=='option' and ('name','=','sb_court_succession.004.'+suffix) in v)
            fields=dict((k,v) for k,_,v in option)
            rt,king,prince,*_=court();reserve(rt,king,prince)
            self.assertTrue(rt.condition(fields['trigger'],rt.country))
            rt.effect(fields['hidden_effect'],rt.country)
            for kind in IG_TYPES:
                self.assertEqual({'sb_court_claimant_armed_forces':1},rt.country['ig:'+kind]['modifiers'])

    def test_abandoned_native_war_removes_sponsorship_from_both_countries(self):
        rt,king,prince,_,_=court();reserve(rt,king,prince);answer(rt);_,rebels=split(rt)
        rt.country['wars']=[];rebels['wars']=[]
        rt.run('sb_court_reconcile_dynastic_record')
        for side in (rt.country,rebels):
            self.assertEqual({'ideology_patriotic','ideology_jingoist'},side['ig:ig_armed_forces']['ideologies'])
            for kind in IG_TYPES:
                self.assertNotIn('sb_court_claimant_armed_forces',side['ig:'+kind]['modifiers'])
                self.assertNotIn('ideology_sb_contested_crown',side['ig:'+kind]['ideologies'])

    def test_poll_slot_is_single_across_cancelled_and_reopened_episodes(self):
        rt,king,prince,_,_=court();reserve(rt,king,prince);answer(rt)
        rt.run('sb_court_cancel_dynastic_crisis')
        reserve(rt,king,prince)
        self.assertNotIn('sb_court_dynastic_crisis_var',rt.country['vars'])
        rt.country['movements'].clear() # native disband_trigger, supplied callback boundary
        reserve(rt,king,prince);answer(rt)
        self.assertEqual(1,rt.country['events'].count('sb_court_succession.991'))
        source=(ROOT/'events/sb_court_succession_events.txt').read_text(encoding='utf-8-sig')
        poll=dict((k,v) for k,_,v in statements(find_object(source,'sb_court_succession.991')))
        rt.effect(poll['immediate'],rt.country)
        self.assertEqual(2,rt.country['events'].count('sb_court_succession.991')) # one next delivery
        rt.run('sb_court_cancel_dynastic_crisis');rt.effect(poll['immediate'],rt.country)
        self.assertNotIn('sb_court_dynastic_poll_queued_var',rt.country['vars'])
        self.assertEqual(2,rt.country['events'].count('sb_court_succession.991'))

    def test_dismissing_old_participants_cannot_cancel_a_different_pending_choice(self):
        rt,king,prince,third,_=court();reserve(rt,king,prince)
        rt.run('sb_court_cancel_dynastic_crisis');reserve(rt,king,third)
        self.assertNotIn('sb_court_dynastic_crisis_var',rt.country['vars'])
        rt.run('sb_court_dismiss_dynastic_choice');reserve(rt,king,third)
        rt.scopes['sb_court_rival']=prince
        self.assertFalse(rt.condition(TRIGGERS['sb_court_displayed_dynastic_pair'],rt.country))
        rt.run('sb_court_dismiss_dynastic_choice')
        self.assertIs(third,rt.country['vars']['sb_court_dynastic_rival_scope'])


class ClaimantContracts(unittest.TestCase):
    def test_supply_uses_native_consumption_modifier_and_existing_icons(self):
        modifiers=definitions('common/static_modifiers/sb_court_dynastic_modifiers.txt')
        supply=dict((k,v) for k,_,v in modifiers['sb_court_dynastic_ai_supply'])
        self.assertEqual({'icon','unit_supply_consumption_mult'},set(supply))
        self.assertEqual(-0.5,float(supply['unit_supply_consumption_mult']))
        icons=[supply['icon']]+[v for body in definitions('common/static_modifiers/sb_institutions_modifiers.txt').values()
                               for k,_,v in body if k=='icon']
        self.assertEqual(4,len(icons))
        for icon in icons: self.assertTrue((GAME/icon.strip('"')).is_file(),icon)

    def test_succession_events_use_existing_native_windows(self):
        gui=(GAME/'gui/eventwindow.gui').read_text(encoding='utf-8-sig')
        windows=set(re.findall(r'event_window\s*=\s*\{\s*name\s*=\s*"([^"]+)"',gui))
        source=(ROOT/'events/sb_court_succession_events.txt').read_text(encoding='utf-8-sig')
        for window in re.findall(r'(?m)^\s*gui_window\s*=\s*(\w+)',source):
            self.assertIn(window,windows)
        victory=dict((k,v) for k,_,v in statements(find_object(source,'sb_court_succession.005')))
        self.assertEqual('scope:sb_court_victor',victory['left_icon'])

    def test_trial_opposition_stances_and_native_sponsor_limits(self):
        # Arithmetic from the inspected gate, not a claim that this harness creates native wars.
        pins=json.loads((ROOT/'Docs/compatibility/zulu_contested_crown_contracts_1_14_5.json').read_text())['native_defines']
        stances={'strongly_disapprove':0,'disapprove':1,'neutral':2,'approve':3,'strongly_approve':4}
        penalty=float(dict((k,v) for k,_,v in definitions('common/static_modifiers/sb_court_dynastic_modifiers.txt')['sb_court_claimant_armed_forces'])['interest_group_approval_add'])
        self.assertEqual(-20,penalty)
        for name,body in definitions('common/ideologies/sb_court_claimant_ideologies.txt').items():
            laws=dict((k,v) for k,_,v in body)['lawgroup_governance_principles']
            positions={law:stances[stance] for law,_,stance in laws}
            contested=next(k for k in positions if k.startswith('law_sb_'))
            original=next(k for k in positions if not k.startswith('law_sb_'))
            self.assertEqual(4,positions[contested])
            self.assertEqual(0,positions[original])
            # DP's opposition trial retains native gates: do not claim guaranteed Royalist support.
            delta=abs(positions[original]-4)*pins['IG_MAX_IDEOLOGICAL_DELTA_TO_JOIN_CIVIL_WAR_LEADER_FACTOR']/2
            self.assertGreater(delta,pins['IG_MAX_IDEOLOGICAL_DELTA_TO_JOIN_CIVIL_WAR_ANGRY'])
            neutral_delta=abs(positions[original]-2)*pins['IG_MAX_IDEOLOGICAL_DELTA_TO_JOIN_CIVIL_WAR_LEADER_FACTOR']/2
            self.assertLessEqual(neutral_delta,pins['IG_MAX_IDEOLOGICAL_DELTA_TO_JOIN_CIVIL_WAR_ANGRY'])
        observed=json.loads((ROOT/'Docs/compatibility/evidence/zulu_claimant_af_lock_2026_10_28.json').read_text())
        self.assertLessEqual(observed['approval']+penalty,pins['APPROVAL_THRESHOLD_ANGRY'])
        self.assertGreater(observed['supporting_clout_fraction'],pins['IG_SUPPORTING_MOVEMENT_MIN_SUPPORTING_CLOUT'])
        # Explicit sponsor selection must not pretend it bypasses the native 5% gate.
        self.assertEqual(.05,pins['IG_SUPPORTING_MOVEMENT_MIN_SUPPORTING_CLOUT'])

    def test_all_interest_groups_can_pressure_and_sponsor_the_claimant_war(self):
        movement=(ROOT/'common/political_movements/sb_court_dynastic_test.txt').read_text(encoding='utf-8-sig')
        gate=statements(child(child(movement,'revolution'),'interest_group_can_join'))
        rt,*_=court()
        pressure=statements(child(movement,'can_pressure_interest_group'))
        for kind in IG_TYPES:
            self.assertTrue(rt.condition(gate,{'type':kind,'vars':{}}))
            self.assertTrue(rt.condition(pressure,{'type':kind,'vars':{}}))

    def test_crisis_pressure_cannot_rewrite_ordinary_character_ideologies(self):
        movement=(ROOT/'common/political_movements/sb_court_dynastic_test.txt').read_text(encoding='utf-8-sig')
        self.assertEqual([],statements(child(movement,'character_ideologies')))

    def test_claimant_activism_gives_recruitment_time_before_native_organising(self):
        source=(GAME/'common/defines/00_defines.txt').read_text(encoding='utf-8-sig')
        def native(name):
            return float(re.search(r'(?m)^\s*'+name+r'\s*=\s*([.0-9]+)',source)[1])
        fields=dict((k,v) for k,_,v in definitions('common/static_modifiers/sb_court_dynastic_modifiers.txt')['sb_court_claimant_mobilisation'])
        # +400% turns native 0.01 into 0.05. Organising can start at 75%,
        # before full activism: this is a rate/threshold check, not a war simulator.
        rate=native('MOVEMENT_WEEKLY_RADICALISM_CHANGE')*(1+float(fields.get('political_movement_activism_growth_mult',0)))
        self.assertAlmostEqual(0.05,rate)
        organise=native('MIN_RADICALISM_FOR_CIVIL_WAR_PROGRESSION')
        start=native('MIN_RADICALISM_FOR_CIVIL_WAR_START')
        self.assertEqual((0.75,1.0),(organise,start))
        self.assertLess(14*rate,organise)
        self.assertAlmostEqual(organise,15*rate)
        self.assertLess(19*rate,start)
        self.assertAlmostEqual(start,20*rate)

    def test_claimant_attraction_is_a_single_crisis_only_movement_modifier(self):
        modifiers=definitions('common/static_modifiers/sb_court_dynastic_modifiers.txt')
        fields=dict((k,v) for k,_,v in modifiers['sb_court_claimant_mobilisation'])
        self.assertEqual(1,float(fields['political_movement_pop_attraction_mult']))
        self.assertNotIn('political_movement_pop_attraction_mult',dict((k,v) for k,_,v in modifiers['sb_court_claimant_armed_forces']))
        rt,king,prince,*_=court();reserve(rt,king,prince);answer(rt)
        movement=rt.country['vars']['sb_court_dynastic_movement_scope']
        self.assertEqual({'sb_court_claimant_mobilisation':1},movement['modifiers'])
        for _ in range(8): rt.run('sb_court_progress_dynastic_crisis')
        self.assertEqual({'sb_court_claimant_mobilisation':1},movement['modifiers'])
        self.assertNotIn('sb_court_claimant_mobilisation',rt.country.get('modifiers',{}))
        rt.run('sb_court_cancel_dynastic_crisis')
        self.assertNotIn('sb_court_claimant_mobilisation',movement['modifiers'])

    def test_current_native_and_cmf_contracts_are_mandatory_and_match(self):
        data=json.loads((ROOT/'Docs/compatibility/zulu_contested_crown_contracts_1_14_5.json').read_text())
        self.assertTrue(GAME.is_dir(),'Current game contracts are mandatory, not historical optional evidence')
        for base,items in ((GAME,data['contracts']),(ROOT.parent/'Community Mod Framework',data['cmf_contracts'])):
            for contract in items:
                p=base/contract['path']
                payload=find_object(p.read_text(encoding='utf-8-sig'),contract['key']).encode() if 'key' in contract else p.read_bytes()
                self.assertEqual(contract['sha256'],hashlib.sha256(payload).hexdigest(),str(p))
        defines=(GAME/'common/defines/00_defines.txt').read_text(encoding='utf-8-sig')
        for key,expected in data['native_defines'].items():
            found=float(re.search(r'(?m)^\s*'+key+r'\s*=\s*([-.0-9]+)',defines)[1])
            self.assertEqual(expected,found,key)

    def test_law_demand_stays_evaluable_but_manual_enactment_is_cancelled(self):
        rt,*_=court()
        handler=statements(find_object((ROOT/'common/on_actions/sb_court_on_actions.txt').read_text(encoding='utf-8-sig'),'sb_court_block_ordinary_contested_enactment'))
        fields=dict((k,v) for k,_,v in handler)
        for law,cancel in (('law_sb_contested_crown',True),('law_sb_contested_social_crown',True),('law_monarchy',False),('law_parliamentary_republic',False)):
            rt.country['enacting']='law_type:'+law
            if rt.condition(fields['trigger'],rt.country): rt.effect(fields['effect'],rt.country)
            self.assertEqual(not cancel,'enacting' in rt.country)
        self.assertFalse(rt.condition(TRIGGERS['sb_court_dynastic_law_available'],rt.country))
        rt.country['vars']['sb_court_dynastic_crisis_var']=1
        self.assertTrue(rt.condition(TRIGGERS['sb_court_dynastic_law_available'],rt.country))
        rt.country['vars'].pop('sb_institutions_zulu_profile_var');rt.country['id']='FRA'
        self.assertFalse(rt.condition(TRIGGERS['sb_court_dynastic_law_available'],rt.country))

    def test_temporary_laws_keep_institutional_reach_and_do_not_reopen_exited_systems(self):
        from tests.test_zulu_institutions_core import Runtime
        for law,ir in (('law_sb_contested_crown',50),('law_sb_contested_social_crown',40)):
            rt=Runtime();rt.zul['laws'].discard('law_monarchy');rt.zul['laws'].add(law)
            rt.call('sb_institutions_reconcile')
            self.assertIn('sb_institutions_active_var',rt.zul['vars'])
            self.assertEqual(ir,rt.calc('sb_institutional_reach'))
            rt.zul['laws'].add('law_technocracy');rt.call('sb_institutions_reconcile')
            self.assertNotIn('sb_institutions_active_var',rt.zul['vars'])

    def test_laws_are_independent_narrow_and_copy_native_modifiers(self):
        own=extract_top_level_blocks((ROOT/'common/laws/06_sb_contested_crown.txt').read_text(encoding='utf-8-sig'))
        native=extract_top_level_blocks((GAME/'common/laws/00_governance_principles.txt').read_text(encoding='utf-8-sig'))
        for key,parent in (('law_sb_contested_crown','law_monarchy'),('law_sb_contested_social_crown','law_social_monarchy')):
            self.assertNotIn('parent =',own[key])
            self.assertEqual(statements(child(native[parent],'modifier')),statements(child(own[key],'modifier')))
            self.assertEqual([('always','=','no')],statements(child(own[key],'can_impose')))
        for body in definitions('common/ideologies/sb_court_claimant_ideologies.txt').values():
            self.assertEqual({'icon','priority','lawgroup_governance_principles'},{k for k,_,v in body})

    def test_target_is_geographical_not_a_scripted_army_bonus(self):
        movement=(ROOT/'common/political_movements/sb_court_dynastic_test.txt').read_text(encoding='utf-8-sig')
        revolution=statements(child(movement,'revolution'))
        weights=dict((k,v) for k,_,v in revolution)
        self.assertEqual([('value','=','owner.var:sb_court_dynastic_target_var')],weights['target_fraction_of_states'])
        state=str(weights['state_weight'])
        self.assertEqual(('value','=','sb_court_dynastic_state_weight'),weights['state_weight'][0])
        self.assertIn('mog_plp_movement_all_general_state_weight_mult',state)
        for bias in ('is_capital','urbanization','clout'): self.assertNotIn(bias,state)
        effects=(ROOT/'common/scripted_effects/sb_court_dynastic_effects.txt').read_text()
        for forbidden in ('create_diplomatic_play','create_military_formation','transfer_military_formation','sb_zululand_resolve_','set_ideology ='):
            self.assertNotIn(forbidden,effects)

    def test_old_coup_is_archived_and_not_executable(self):
        for directory in ('common','events','gui'):
            for p in (ROOT/directory).rglob('*'):
                if p.is_file() and p.suffix in ('.txt','.gui'):
                    text=p.read_text(encoding='utf-8-sig')
                    for old in ('sb_court_try_start_coup','je_sb_court_coup','sb_court_coup_resist','sb_court_start_dynastic_prototype'):
                        self.assertNotIn(old,text,str(p))
        self.assertTrue((ROOT/'Docs/retired/zulu_court_coup_2026_10_27/common/journal_entries/sb_court_coup.txt').is_file())


if __name__ == '__main__': unittest.main()
