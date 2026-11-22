"""Execute the shipped annual/deck/choice scripts. Native delivery is DP's test."""
from pathlib import Path
import itertools
import random
import unittest
from tests.test_zulu_court_politics import character, definitions, EFFECTS, TRIGGERS, VALUES, COURT_MODIFIERS
from tests.test_zulu_court_rework import ReworkRuntime, court
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import extract_top_level_blocks, find_object

ROOT = Path(__file__).resolve().parents[1]
EVENT_TEXT = (ROOT/'events/sb_zulu_court_events.txt').read_text(encoding='utf-8-sig')
EVENTS = {f'sb_zulu_court.{n}': statements(find_object(EVENT_TEXT,f'sb_zulu_court.{n}')) for n in (200,201,210,211,212,213,214,215)}
COURT_MODIFIERS.update(definitions('common/static_modifiers/sb_court_episode_modifiers.txt'))

def fields(nodes): return {k:v for k,_,v in nodes}
def options(event): return [v for k,_,v in EVENTS[event] if k=='option']

class EventRuntime(ReworkRuntime):
    def __init__(self,members):
        super().__init__(members)
        self.preview=False
        self.rng=random.Random(47); self.rolls=[]; self.choices=[]
        self.country.update(month=1,game_date=18370101,year=1837,gold_reserves_limit=100000,gold_reserves=200000,is_player=True)
        self.country['laws']={'law_type:law_monarchy','law_type:law_autocracy'}
        self.country['journals']={'je_sb_adopt_firearms'}
        self.scopes['sb_court_country']=self.country
    def ref(self,key,scope,prev=None):
        if key in ('game_date','month','year'): return self.country[key]
        return super().ref(key,scope,prev)
    def condition(self,nodes,scope,prev=None):
        out=[]
        branch=None
        for key,op,value in nodes:
            if key=='trigger_if':
                branch=self.condition(fields(value)['limit'],scope,prev)
                if branch: out.append(self.condition([n for n in value if n[0]!='limit'],scope,prev))
                continue
            if key=='trigger_else':
                if branch is False: out.append(self.condition(value,scope,prev))
                continue
            if (key=='this' or key.startswith(('var:','scope:'))) and isinstance(value,str) and value.startswith(('var:','scope:')):
                if self.ref(value,scope,prev) is None:
                    raise AssertionError('comparison reads missing RHS: '+value)
            if self.preview and key.startswith('var:') and op!='?=' and self.ref(key,scope,prev) is None:
                raise AssertionError('preview reads missing variable: '+key)
            if key=='hidden_trigger': out.append(self.condition(value,scope,prev))
            elif key=='has_journal_entry': out.append(value in scope.get('journals',set()))
            elif key in ('is_player','is_ai'): out.append(scope.get(key,False)==(value=='yes'))
            elif key=='any_in_list':
                f=fields(value); name='members' if f['variable']=='sb_court_members' else f['variable']
                count=sum(self.condition([n for n in value if n[0] not in ('variable','count')],m,scope) for m in scope.get(name,[]))
                bound=next(((o,v) for k,o,v in value if k=='count'),('>=','1'))
                out.append(count>=int(bound[1]) if bound[0]=='>=' else count==int(bound[1]))
            else: out.append(super().condition([(key,op,value)],scope,prev))
        return all(out)
    def effect(self,nodes,scope,prev=None):
        for node in self.branches(nodes,scope,prev):
            key,op,value=node
            if self.preview:
                if key=='change_variable':
                    name=fields(value)['name']
                    if name not in scope['vars']:
                        raise AssertionError('preview reads missing counter: '+name)
                    continue
                if key in ('set_variable','remove_variable','trigger_event','save_scope_as'):
                    continue
                if key=='sb_institutions_recalculate':
                    # Separate backing tests cover this helper; preview this event's scheduler.
                    continue
            if key=='random_list':
                choices=[]
                for weight,_,body in value:
                    f=fields(body)
                    if self.condition(f.get('trigger',[]),scope,prev):
                        # Native CalcChanceIfEnabled truncates fixed-point weights to integers.
                        amount=int(float(weight)+self.calc(f.get('modifier',[]),scope,prev))
                        self.assert_weight(amount)
                        choices.append((amount,[n for n in body if n[0] not in ('modifier','trigger')]))
                if self.preview:
                    # Hover previews inspect possible branches without rolling or mutating.
                    for weight,body in choices:
                        if weight>0:self.effect(body,scope,prev)
                    continue
                self.choices.append([w for w,_ in choices])
                point=(self.rolls.pop(0) if self.rolls else self.rng.random())*sum(w for w,_ in choices)
                for weight,body in choices:
                    if point<weight:
                        self.effect(body,scope,prev);break
                    point-=weight
            elif key=='random_in_list':
                f=fields(value);name='members' if f['variable']=='sb_court_members' else f['variable']
                choices=[m for m in scope.get(name,[]) if self.condition(f.get('limit',[]),m,scope)]
                if choices:self.effect([n for n in value if n[0] not in ('variable','limit')],self.rng.choice(choices),scope)
            elif key=='change_variable':
                f=fields(value);name=f.pop('name')
                for action,amount in f.items():
                    val=self.ref(amount,scope,prev)
                    if action=='add': scope['vars'][name]+=val
                    elif action=='subtract': scope['vars'][name]-=val
                    else: raise AssertionError(action)
            elif key=='set_variable' and isinstance(value,list) and any(k in ('days','months','years') for k,_,_ in value):
                f=fields(value);super().effect([node],scope,prev)
                duration=sum(self.ref(f.get(k,'0'),scope,prev)*factor for k,factor in [('days',1),('months',30),('years',365)])
                scope.setdefault('timers',{})[f['name']]=duration
            elif key=='add_modifier' and isinstance(value,list) and 'days' in fields(value):
                f=fields(value)
                if f['days'].startswith('var:'):
                    raise AssertionError('modifier duration requires a named value')
                scope.setdefault('modifier_days',{})[f['name']]=self.ref(f['days'],scope,prev)
                super().effect([node],scope,prev)
            elif key=='sb_boost_firearms_progress_minor':scope['firearms_grants']=scope.get('firearms_grants',0)+1
            elif key=='sb_change_prerogative':scope['vars']['sb_prerogative_var']=scope['vars'].get('sb_prerogative_var',0)+float(fields(value)['VALUE'])
            elif key=='custom_tooltip':pass
            elif key=='show_as_tooltip':pass
            elif key=='remove_trait':scope.setdefault('traits',set()).discard(value)
            else: super().effect([node],scope,prev)
    def assert_weight(self,w):
        if w<0:raise AssertionError(('negative probability',w))
    def fire(self,n):
        for k,_,v in EVENTS[f'sb_zulu_court.{n}']:
            if k=='immediate':self.effect(v,self.country)
    def answer(self,n,suffix):
        option=next(o for o in options(f'sb_zulu_court.{n}') if fields(o)['name']==(suffix if suffix.startswith('sb_') else f'sb_zulu_court.{n}.{suffix}'))
        if not self.condition(fields(option).get('trigger',[]),self.country):return False
        self.effect([node for node in option if node[0] in ('hidden_effect','show_as_tooltip')],self.country)
        after=fields(EVENTS[f'sb_zulu_court.{n}']).get('after',[]);self.effect(after,self.country)
        return True

def setup():
    king=character('Dingane',1,50,1,1);king['template']='ZUL_dingane';king['popularity']=-50
    prince=character('Mpande',0,50,-1,1);prince['template']='ZUL_mpande_zulu';prince['vars']['sb_court_claimant_scope']=prince
    rival=character('Gqugqu',0,50,-1,1);rival['template']='ZUL_gqugqu_claimant';rival['vars']['sb_court_claimant_scope']=rival
    people=[king,prince,rival]+[character('chief'+str(i),i+10,30,0,0) for i in range(5)]
    rt=EventRuntime(people);rt.backing()
    return rt,king,prince,rival,people[3:]

class AnnualTransitions(unittest.TestCase):
    def test_claimants_keep_their_allegiance_and_card_when_other_houses_withdraw(self):
        rt,king,prince,rival,chiefs=setup()
        chiefs[0]['vars'].update(sb_court_endorsement_var=-1,sb_court_claimant_scope=rival)
        # Force the withdrawal branch for every committed actor who gets a roll.
        rt.rolls=[0]*200
        rt.effect(EFFECTS['sb_court_annual_allegiances'],rt.country)
        for candidate in (prince,rival):
            self.assertEqual(-1,candidate['vars']['sb_court_endorsement_var'])
            self.assertIs(candidate,candidate['vars']['sb_court_claimant_scope'])
            self.assertIn('sb_court_claimant_trait',candidate['traits'])
            self.assertEqual(75,rt.ref('prominence',candidate))
            self.assertGreaterEqual(candidate['vars']['sb_court_current_weight_var'],75)
            self.assertGreaterEqual(candidate['vars']['sb_court_coalition_weight_var'],75)
            self.assertNotIn(candidate,rt.country['sb_court_annual_current_changes'])
            self.assertNotIn(candidate,rt.country['sb_court_annual_future_changes'])
            self.assertIn(candidate,rt.country['sb_court_current_patrons'])
            self.assertIn(candidate,rt.country['sb_court_future_patrons'])
        self.assertEqual(0,chiefs[0]['vars']['sb_court_endorsement_var'])
        self.assertIn(chiefs[0],rt.country['sb_court_annual_current_changes'])
        self.assertIs(rival,chiefs[1]['vars']['sb_court_claimant_scope'])

    def test_annual_exclusion_preserves_a_princes_existing_support_for_his_father(self):
        rt,king,prince,rival,chiefs=setup()
        son=character('Cetshwayo',0,30,-1,1,age=16)
        son['template']='ZUL_cetshwayo_heir'
        son['owner']=rt.country
        son['vars'].update(sb_court_home_scope=rt.country,sb_court_claimant_scope=prince)
        rt.country['members'].append(son)
        rt.backing();rt.rolls=[0]*200
        rt.effect(EFFECTS['sb_court_annual_allegiances'],rt.country)
        self.assertEqual(-1,son['vars']['sb_court_endorsement_var'])
        self.assertIs(prince,son['vars']['sb_court_claimant_scope'])
        self.assertIn('sb_court_endorsement_claimant_trait',son['traits'])
        self.assertIn('sb_court_claimant_trait',son['traits'])
        self.assertNotIn(son,rt.country['sb_court_annual_current_changes'])

    def test_mpandes_sons_are_future_patrons_but_not_current_opposition(self):
        rt,king,prince,rival,chiefs=setup()
        rt.country['ruler']=prince
        sons=[]
        for name,template in [('Cetshwayo','ZUL_cetshwayo_heir'),('Mbuyazi','ZUL_mbuyazi_heir')]:
            son=character(name,0,40,-1,1,age=18)
            son.update(template=template,owner=rt.country)
            son['vars'].update(sb_court_home_scope=rt.country,sb_court_claimant_scope=son)
            rt.country['members'].append(son);sons.append(son)
        rt.backing();rt.rolls=[99]*200
        rt.effect(EFFECTS['sb_court_annual_allegiances'],rt.country)
        for son in sons:
            self.assertFalse(any(p is son for p in rt.country['sb_court_current_patrons']))
            self.assertTrue(any(p is son for p in rt.country['sb_court_future_patrons']))
            self.assertEqual(1,son['vars']['sb_court_endorsement_var'])

    def test_probability_boundaries_from_shipped_values(self):
        rt,king,prince,rival,chiefs=setup();actor=chiefs[0]
        for current,best in itertools.product([0,.1,.25,.5,.7,1],repeat=2):
            actor['vars'].update(sb_court_roll_current_var=current,sb_court_roll_alternative_var=best,sb_court_roll_best_var=max(current,best))
            withdraw=rt.calc(VALUES['sb_court_withdraw_chance'],actor)
            switch=rt.calc(VALUES['sb_court_switch_chance'],actor)
            stay=rt.calc(VALUES['sb_court_stay_chance'],actor)
            self.assertAlmostEqual(100,withdraw+switch+stay)
            self.assertGreaterEqual(stay,95);self.assertGreaterEqual(withdraw,.5)
            self.assertLessEqual(rt.calc(VALUES['sb_court_join_chance'],actor),20)
            if best==0:self.assertEqual(0,switch)
        for q,a in [(-150,0),(-50,.25),(0,.5),(100,1),(200,1)]:
            king['popularity']=q;self.assertEqual(a,rt.calc(VALUES['sb_court_patron_attraction'],king))
    def test_optional_left_hand_scope_cannot_hide_an_unset_right_hand_patron(self):
        rt,king,p,r,chiefs=setup()
        rt.scopes['sb_court_annual_actor']=chiefs[0]
        with self.assertRaisesRegex(AssertionError,'missing RHS'):
            rt.condition(statements('limit = { NOT = { this ?= scope:sb_court_annual_actor.var:sb_court_annual_old_current_scope } }'),king)
        rt.rolls=[0]*200
        rt.effect(EFFECTS['sb_court_annual_allegiances'],rt.country)
        self.assertEqual(-1,chiefs[0]['vars']['sb_court_endorsement_var'])
        self.assertIs(r,chiefs[0]['vars']['sb_court_claimant_scope'])
        self.assertIs(r,chiefs[0]['vars']['sb_court_successor_pledge_scope'])
        self.assertIn(chiefs[0],rt.country['sb_court_annual_current_changes'])
        self.assertIn(chiefs[0],rt.country['sb_court_annual_future_changes'])

    def test_withdrawn_future_pledge_releases_its_council_promise(self):
        rt,king,p,r,chiefs=setup();actor=chiefs[0]
        actor['vars']['sb_court_council_promise_scope']=p
        actor['vars']['sb_court_successor_pledge_scope']=p
        rt.effect(EFFECTS['sb_court_reconcile_future_promise'],actor)
        self.assertIs(p,actor['vars']['sb_court_council_promise_scope'])
        actor['vars'].pop('sb_court_successor_pledge_scope')
        rt.effect(EFFECTS['sb_court_reconcile_future_promise'],actor)
        self.assertNotIn('sb_court_council_promise_scope',actor['vars'])
        rt.effect(EFFECTS['sb_court_reconcile_future_promise'],actor)

    def test_native_integer_weights_preserve_fractional_attraction_and_withdrawal(self):
        rt,king,p,r,chiefs=setup();actor=chiefs[0]
        rt.scopes['sb_court_annual_actor']=actor
        for patron,attraction in ((king,.05),(p,.50),(r,.55)):
            patron['vars']['sb_court_annual_attraction_var']=attraction
        rt.country['sb_court_current_patrons']=[king,p,r]
        rt.rolls=[0]*20
        rt.effect(statements('effect = { sb_court_roll_record = { RECORD = current PATRONS = sb_court_current_patrons } }'),actor)
        self.assertEqual([1100000,8900000],rt.choices[0])
        self.assertEqual([5000,0],rt.choices[1])
        self.assertEqual([50000,5000],rt.choices[2])
        self.assertEqual([55000,55000],rt.choices[3])
        self.assertIs(r,actor['vars']['sb_court_annual_new_current_scope'])
        actor['vars']['sb_court_annual_old_current_scope']=king
        rt.choices.clear();rt.rolls=[0]*20
        rt.effect(statements('effect = { sb_court_roll_record = { RECORD = current PATRONS = sb_court_current_patrons } }'),actor)
        self.assertEqual([97500,250000,9652500],rt.choices[0])
        self.assertNotIn('sb_court_annual_new_current_scope',actor['vars'])

    def test_annual_snapshot_separate_records_and_repeat_callback(self):
        rt,king,prince,rival,chiefs=setup()
        chiefs[0]['vars']['sb_court_endorsement_var']=1
        chiefs[0]['vars']['sb_court_successor_pledge_scope']=prince
        rt.rolls=[0]*200
        rt.effect(EFFECTS['sb_court_annual_allegiances'],rt.country)
        self.assertEqual(['sb_zulu_court.200'],rt.country['events'])
        self.assertEqual(1,king['vars']['sb_court_endorsement_var'])
        self.assertIs(prince,chiefs[0]['vars']['sb_court_annual_old_future_scope'])
        self.assertIs(king,chiefs[0]['vars']['sb_court_annual_old_current_scope'])
        for p in [prince,rival]:self.assertNotIn('sb_court_successor_pledge_scope',p['vars'])
        states=[dict(c['vars']) for c in chiefs]
        rt.effect(EFFECTS['sb_court_annual_allegiances'],rt.country)
        self.assertEqual(states,[c['vars'] for c in chiefs])
        self.assertEqual({},rt.scopes['root']['vars'])
    def test_unchanged_harvest_is_silent_but_next_changed_year_reports_once(self):
        rt,king,p,r,chiefs=setup()
        rt.rolls=[.999]*200
        rt.effect(EFFECTS['sb_court_annual_allegiances'],rt.country)
        self.assertEqual([],rt.country.get('events',[]))
        self.assertEqual([],rt.country['sb_court_annual_current_changes'])
        self.assertEqual([],rt.country['sb_court_annual_future_changes'])
        self.assertIn('sb_court_annual_checked_var',rt.country['vars'])
        rt.country.update(year=1838,game_date=18380101)
        rt.country['vars'].pop('sb_court_annual_checked_var')
        rt.rolls=[0]*200
        rt.effect(EFFECTS['sb_court_annual_allegiances'],rt.country)
        self.assertEqual(['sb_zulu_court.200'],rt.country['events'])
        rt.effect(EFFECTS['sb_court_annual_allegiances'],rt.country)
        self.assertEqual(['sb_zulu_court.200'],rt.country['events'])
    def test_uncommitted_agitators_and_nonpositive_backers_do_not_join_annually(self):
        rt,king,p,r,chiefs=setup()
        chiefs[0]['agitator']=True
        chiefs[1]['prominence']=0
        chiefs[2]['prominence']=-10
        rt.backing();rt.rolls=[0]*200
        rt.effect(EFFECTS['sb_court_annual_allegiances'],rt.country)
        for c in chiefs[:3]:
            self.assertEqual(0,c['vars']['sb_court_endorsement_var'])
            self.assertNotIn('sb_court_successor_pledge_scope',c['vars'])
    def test_zero_attraction_no_recruitment_and_accession_freeze(self):
        rt,king,prince,rival,chiefs=setup()
        for p in [king,prince,rival]:p['popularity']=-100
        for c in chiefs:c['vars']['sb_court_alignment_var']=1
        rt.effect(EFFECTS['sb_court_annual_allegiances'],rt.country)
        self.assertTrue(all(c['vars']['sb_court_endorsement_var']==0 for c in chiefs))
        self.assertTrue(all('sb_court_successor_pledge_scope' not in c['vars'] for c in chiefs))
        for marker in ['sb_court_accession_open_var','sb_court_dynastic_war_scope','sb_court_civil_war_var']:
            rt.country['vars'].pop('sb_court_annual_checked_var',None);rt.country['vars'][marker]=1
            before=len(rt.choices);rt.effect(EFFECTS['sb_court_annual_allegiances'],rt.country)
            self.assertEqual(before,len(rt.choices));rt.country['vars'].pop(marker)
    def test_voluntary_future_departure_ends_only_that_promise(self):
        rt,king,prince,rival,chiefs=setup();c=chiefs[0]
        c['vars'].update(sb_court_endorsement_var=1,sb_court_personal_council_scope=king,sb_court_successor_pledge_scope=rival,sb_court_council_promise_scope=prince)
        rt.effect(EFFECTS['sb_court_reconcile_future_promise'],c)
        self.assertNotIn('sb_court_council_promise_scope',c['vars'])
        self.assertIs(king,c['vars']['sb_court_personal_council_scope'])
        rt.effect(EFFECTS['sb_court_withdraw_personal'],c)
        self.assertIs(rival,c['vars']['sb_court_successor_pledge_scope'])

class CourtDeckAndChoices(unittest.TestCase):
    def make_all_cards_eligible(self):
        rt,king,p,r,chiefs=setup()
        chiefs[0]['vars']['sb_court_endorsement_var']=1
        chiefs[1]['vars'].update(sb_court_endorsement_var=-1,sb_court_claimant_scope=p)
        return rt,king,p,r,chiefs
    def test_six_cards_without_replacement_delays_and_duplicate_cleanup(self):
        rt,*_=self.make_all_cards_eligible();seen=[]
        for _ in range(6):
            rt.effect(EFFECTS['sb_court_deck_draw'],rt.country)
            n=rt.country['vars']['sb_court_deck_card_var'];seen.append(n)
            rt.country['vars'].update(sb_court_episode_open_var=1,sb_court_episode_card_var=n,sb_court_episode_ruler_scope=rt.country['ruler'])
            rt.effect(EFFECTS['sb_court_deck_deliver'],rt.country)
            rt.country['vars'].pop('sb_court_deck_card_var')
            rt.effect(EFFECTS['sb_court_episode_cleanup'],rt.country)
            self.assertIn(rt.country['timers']['sb_court_deck_wait_var'],range(180,721,30))
            count=len(rt.choices);rt.effect(EFFECTS['sb_court_episode_cleanup'],rt.country);self.assertEqual(count,len(rt.choices))
        self.assertEqual(set(range(210,216)),set(seen))
    def test_ineligible_reserved_card_uses_existing_due_time(self):
        rt,*_=self.make_all_cards_eligible()
        rt.country['vars'].update(sb_court_deck_started_var=1,sb_court_deck_card_var=215,sb_court_firearms_reward_var=1)
        rt.effect(EFFECTS['sb_court_deck_monthly'],rt.country)
        self.assertNotEqual(215,rt.country['vars']['sb_court_episode_card_var'])
        self.assertNotIn('sb_court_deck_wait_var',rt.country['vars'])
        self.assertEqual(1,len(rt.country['events']))
        rt.effect(EFFECTS['sb_court_deck_monthly'],rt.country)
        self.assertEqual(1,len(rt.country['events']))
    def deliver(self,n):
        rt,king,p,r,chiefs=self.make_all_cards_eligible()
        rt.country['vars'].update(sb_court_deck_card_var=n,sb_court_episode_card_var=n,sb_court_episode_open_var=1,sb_court_episode_ruler_scope=king)
        rt.effect(EFFECTS['sb_court_deck_deliver'],rt.country);rt.fire(n)
        return rt,king,p,r,chiefs
    def test_incident_after_preview_never_reads_execution_only_deck_counter(self):
        for n,exhausted in itertools.product(range(210,216),(False,True)):
            with self.subTest(card=n,exhausted=exhausted):
                rt,*_=self.deliver(n)
                rt.country['vars'].pop('sb_court_deck_card_var')
                if exhausted:
                    for card in range(210,216):rt.country['vars'][f'sb_court_card_{card}_used_var']=1
                before=dict(rt.country['vars']);random_state=rt.rng.getstate()
                rt.preview=True
                rt.effect(fields(EVENTS[f'sb_zulu_court.{n}'])['after'],rt.country)
                self.assertEqual(before,rt.country['vars'])
                self.assertEqual(random_state,rt.rng.getstate())
                self.assertNotIn('sb_court_deck_available_var',rt.country['vars'])
                self.assertNotIn('sb_court_deck_wait_var',rt.country['vars'])
                self.assertEqual({},rt.scopes['root']['vars'])
    def test_empty_and_single_card_decks_clean_up_the_temporary_counter(self):
        rt,king,p,r,chiefs=self.make_all_cards_eligible()
        rt.country['members']=[king]
        rt.effect(EFFECTS['sb_court_deck_draw'],rt.country)
        self.assertNotIn('sb_court_deck_card_var',rt.country['vars'])
        self.assertNotIn('sb_court_deck_available_var',rt.country['vars'])
        # With only a prince, the reputation card is the sole eligible scene.
        rt.country['members'].append(p)
        rt.country['vars'].update(sb_court_deck_last_var=211,sb_court_card_211_used_var=1)
        rt.effect(EFFECTS['sb_court_deck_draw'],rt.country)
        self.assertEqual(211,rt.country['vars']['sb_court_deck_card_var'])
        self.assertNotIn('sb_court_deck_available_var',rt.country['vars'])
        self.assertEqual({},rt.scopes['root']['vars'])
    def test_action_portraits_resolve_the_named_subject(self):
        text=(ROOT/'events/sb_court_politics_events.txt').read_text(encoding='utf-8-sig')
        events={f'sb_court_politics.{n}': statements(find_object(text,f'sb_court_politics.{n}'))
                for n in ('001','002','003')}
        for number in ('001','002','003'):
            with self.subTest(event=number):
                rt,king,prince,*_=setup()
                rt.country['vars'].update(sb_court_action_actor_scope=prince)
                event=fields(events[f'sb_court_politics.{number}'])
                rt.effect(event['immediate'],rt.country)
                self.assertEqual('event_window_1char_tabloid',event['gui_window'])
                self.assertNotIn('event_image',event)
                self.assertIs(king if number=='001' else prince,rt.ref(event['left_icon'],rt.country))
    def test_disputed_award_distinct_houses_and_no_free_valid_escape(self):
        rt,*_=self.deliver(214);a=rt.country['vars']['sb_court_episode_actor_scope'];b=rt.country['vars']['sb_court_episode_other_scope']
        self.assertIsNot(a,b);self.assertFalse(rt.answer(214,'z'))
        self.assertTrue(rt.answer(214,'a'))
        self.assertEqual(1,a['vars']['sb_court_endorsement_var']);self.assertEqual(-1,b['vars']['sb_court_endorsement_var'])
    def test_dead_target_or_changed_ruler_cannot_charge(self):
        for change in ['dead','ruler']:
            rt,*_=self.deliver(215);cash=rt.country['gold_reserves']
            if change=='dead':rt.country['vars']['sb_court_episode_actor_scope']['alive']=False
            if change=='ruler':rt.country['ruler']=rt.country['members'][1]
            self.assertFalse(rt.answer(215,'b'));self.assertEqual(cash,rt.country['gold_reserves'])
    def test_paid_incidents_use_frozen_quotes_with_debt_and_charge_once(self):
        for n,choice in ((211,'b'),(214,'c'),(215,'b')):
            for cash in (200000,0,-5000):
                with self.subTest(card=n,cash=cash):
                    rt,*_=self.deliver(n)
                    price=rt.country['vars']['sb_court_episode_price_var']
                    rt.country['gold_reserves_limit']*=2
                    rt.country['gold_reserves']=cash
                    self.assertTrue(rt.answer(n,choice))
                    self.assertEqual(cash-price,rt.country['gold_reserves'])
                    self.assertFalse(rt.answer(n,choice))
                    self.assertEqual(cash-price,rt.country['gold_reserves'])
                    self.assertEqual([f'sb_zulu_court.{n}'],rt.country['events'])
                    self.assertNotIn('sb_court_episode_open_var',rt.country['vars'])
                    self.assertIn('sb_court_deck_wait_var',rt.country['vars'])
                    if n==215:self.assertEqual(1,rt.country['firearms_grants'])
    def test_guns_reward_once_and_concession_original_expiry(self):
        rt,*_=self.deliver(215)
        m={'type':'movement_sb_zulu_chiefly','vars':{},'owner':rt.country};rt.country['movements']=[m]
        self.assertTrue(rt.answer(215,'a'));self.assertEqual(1,rt.country['firearms_grants'])
        expiry=rt.country['vars']['sb_court_guns_until_var']
        rt.country['game_date']+=100
        m['modifiers'].clear();rt.effect(EFFECTS['sb_court_sync_chiefly_concessions'],rt.country)
        self.assertEqual(expiry,rt.country['vars']['sb_court_guns_until_var'])
        self.assertIn('sb_court_chiefly_gun_contacts',m['modifiers'])
        self.assertEqual(expiry-rt.country['game_date'],m['modifier_days']['sb_court_chiefly_gun_contacts'])
        self.assertFalse(rt.condition(TRIGGERS['sb_court_card_215_eligible'],rt.country))
    def test_future_bargain_does_not_change_present_allegiance(self):
        rt,king,p,r,chiefs=self.deliver(210);a=rt.country['vars']['sb_court_episode_actor_scope']
        rt.answer(210,'b');self.assertEqual(1,a['vars']['sb_court_endorsement_var'])
        self.assertIn(a['vars']['sb_court_successor_pledge_scope'],[p,r])
    def test_council_requires_the_backers_own_fifty_prominence_and_grants_no_attraction(self):
        for card,answer in ((210,'c'),(212,'b')):
            for prominence in (0,49.99,50,100):
                with self.subTest(card=card,prominence=prominence):
                    rt,king,*_=self.deliver(card)
                    actor=rt.country['vars']['sb_court_episode_actor_scope']
                    actor['prominence']=prominence
                    actor['vars']['sb_court_represented_weight_var']=500  # Household total does not qualify its leader.
                    beneficiary=rt.country['vars']['sb_court_episode_other_candidate_scope'] if card==210 else king
                    beneficiary['prominence']=100
                    movement={'type':'movement_sb_zulu_chiefly','vars':{},'owner':rt.country}
                    rt.country['movements']=[movement]
                    before=actor['vars']['sb_court_endorsement_var']
                    self.assertEqual(prominence>=50,rt.answer(card,answer))
                    if prominence>=50:
                        if card==210:
                            self.assertIs(beneficiary,actor['vars']['sb_court_successor_pledge_scope'])
                            self.assertIs(beneficiary,actor['vars']['sb_court_council_promise_scope'])
                            self.assertEqual(before,actor['vars']['sb_court_endorsement_var'])
                            self.assertNotIn('law_type:law_sb_chiefly_council',rt.country['laws'])
                        else:
                            self.assertEqual(1,actor['vars']['sb_court_endorsement_var'])
                            self.assertIs(king,actor['vars']['sb_court_personal_council_scope'])
                            self.assertIn('law_type:law_sb_chiefly_council',rt.country['laws'])
                    else:
                        self.assertNotIn('sb_court_council_promise_scope',actor['vars'])
                        self.assertNotIn('sb_court_personal_council_scope',actor['vars'])
                        self.assertEqual(before,actor['vars']['sb_court_endorsement_var'])
                    self.assertNotIn('sb_court_privileges_until_var',rt.country['vars'])
                    self.assertNotIn('sb_court_privileges_this_reign_var',rt.country['vars'])
                    self.assertEqual({},movement.get('modifiers',{}))
    def test_blocking_succession_pledge_spends_prerogative_once(self):
        for prerogative in (10,50,100):
            with self.subTest(prerogative=prerogative):
                rt,*_=self.deliver(210)
                actor=rt.country['vars']['sb_court_episode_actor_scope']
                rt.country['vars']['sb_prerogative_var']=prerogative
                self.assertTrue(rt.answer(210,'z'))
                self.assertEqual(prerogative-10,rt.country['vars']['sb_prerogative_var'])
                self.assertNotIn('sb_court_successor_pledge_scope',actor['vars'])
                self.assertEqual(1,actor['vars']['sb_court_endorsement_var'])
                rt.answer(210,'z')
                self.assertEqual(prerogative-10,rt.country['vars']['sb_prerogative_var'])
    def test_insufficient_prerogative_cannot_block_and_default_allows_the_pledge(self):
        default=next(o for o in options('sb_zulu_court.210') if fields(o).get('default_option')=='yes')
        self.assertEqual('sb_zulu_court.210.a',fields(default)['name'])
        for prerogative in (-100,0,9.99):
            with self.subTest(prerogative=prerogative):
                rt,*_=self.deliver(210)
                actor=rt.country['vars']['sb_court_episode_actor_scope']
                candidate=rt.country['vars']['sb_court_episode_candidate_scope']
                rt.country['vars']['sb_prerogative_var']=prerogative
                self.assertFalse(rt.answer(210,'z'))
                self.assertTrue(rt.answer(210,fields(default)['name']))
                self.assertIs(candidate,actor['vars']['sb_court_successor_pledge_scope'])
                self.assertEqual(prerogative,rt.country['vars']['sb_prerogative_var'])
    def test_blocked_pledge_revalidates_cost_and_stale_participants(self):
        for change in ('cost','actor','ruler'):
            with self.subTest(change=change):
                rt,king,p,*_=self.deliver(210)
                rt.country['vars']['sb_prerogative_var']=10
                option=next(o for o in options('sb_zulu_court.210') if fields(o)['name']=='sb_zulu_court.210.z')
                self.assertTrue(rt.condition(fields(option).get('trigger',[]),rt.country))
                if change=='cost':rt.country['vars']['sb_prerogative_var']=9
                if change=='actor':rt.country['vars']['sb_court_episode_actor_scope']['alive']=False
                if change=='ruler':rt.country['ruler']=p
                before=rt.country['vars']['sb_prerogative_var']
                rt.effect(fields(option).get('hidden_effect',[]),rt.country)
                self.assertEqual(before,rt.country['vars']['sb_prerogative_var'])
                if change!='cost':self.assertTrue(rt.answer(210,'z'))
    def test_routine_refusals_cost_five_prerogative_once_without_forcing_a_concession(self):
        for card,prerogative in itertools.product((212,213,215),(-50,0,5,50)):
            with self.subTest(card=card,prerogative=prerogative):
                rt,*_=self.deliver(card)
                rt.country['vars']['sb_prerogative_var']=prerogative
                def commitments():
                    return [(c['vars']['sb_court_endorsement_var'],c['vars']['sb_court_alignment_var'],
                             id(c['vars'].get('sb_court_claimant_scope')),id(c['vars'].get('sb_court_successor_pledge_scope')))
                            for c in rt.country['members']]
                before=commitments()
                laws=set(rt.country['laws'])
                self.assertTrue(rt.answer(card,'z'))
                self.assertEqual(prerogative-5,rt.country['vars']['sb_prerogative_var'])
                self.assertEqual(before,commitments())
                self.assertEqual(laws,rt.country['laws'])
                self.assertNotIn('sb_court_firearms_reward_var',rt.country['vars'])
                self.assertEqual({},rt.scopes['root']['vars'])
                self.assertTrue(rt.answer(card,'z'))
                self.assertEqual(prerogative-5,rt.country['vars']['sb_prerogative_var'])
    def test_invalidated_routine_refusals_remain_free_to_dismiss(self):
        for card,change in itertools.product((212,213,215),('actor','ruler','episode')):
            with self.subTest(card=card,change=change):
                rt,king,prince,*_=self.deliver(card)
                rt.country['vars']['sb_prerogative_var']=20
                if change=='actor':rt.country['vars']['sb_court_episode_actor_scope']['alive']=False
                if change=='ruler':rt.country['ruler']=prince
                if change=='episode':rt.country['vars'].pop('sb_court_episode_open_var')
                self.assertTrue(rt.answer(card,'z'))
                self.assertEqual(20,rt.country['vars']['sb_prerogative_var'])
    def test_council_execution_rechecks_prominence_after_the_popup_opens(self):
        for card,answer in ((210,'c'),(212,'b')):
            rt,*_=self.deliver(card)
            actor=rt.country['vars']['sb_court_episode_actor_scope'];actor['prominence']=50
            option=next(o for o in options(f'sb_zulu_court.{card}') if fields(o)['name']==f'sb_zulu_court.{card}.{answer}')
            self.assertTrue(rt.condition(fields(option)['trigger'],rt.country))
            actor['prominence']=49
            before=actor['vars']['sb_court_endorsement_var'];laws=set(rt.country['laws'])
            rt.effect(fields(option)['hidden_effect'],rt.country)
            self.assertEqual(before,actor['vars']['sb_court_endorsement_var'])
            self.assertNotIn('sb_court_council_promise_scope',actor['vars'])
            self.assertNotIn('sb_court_personal_council_scope',actor['vars'])
            self.assertEqual(laws,rt.country['laws'])
    def test_shared_council_helper_cannot_bypass_prominence_or_add_privileges(self):
        for card in (210,212):
            rt,king,*_=self.deliver(card)
            actor=rt.country['vars']['sb_court_episode_actor_scope'];actor['prominence']=49
            before=actor['vars']['sb_court_endorsement_var'];laws=set(rt.country['laws'])
            rt.effect([('sb_court_chiefly_bargain','=',[('COUNCIL','=','yes'),('PRIVILEGES','=','no')])],rt.country)
            self.assertEqual(before,actor['vars']['sb_court_endorsement_var'])
            self.assertNotIn('sb_court_successor_pledge_scope',actor['vars'])
            self.assertNotIn('sb_court_personal_council_scope',actor['vars'])
            self.assertNotIn('sb_court_privileges_until_var',rt.country['vars'])
            self.assertEqual(laws,rt.country['laws'])
    def test_chiefly_episode_needs_an_available_bargain_for_its_selected_actor(self):
        rt,king,p,r,chiefs=setup();chief=chiefs[0]
        rt.country['members']=[king,p,r,chief]
        rt.country['vars']['sb_court_privileges_this_reign_var']=1
        for prominence,eligible in ((49,False),(50,True)):
            chief['prominence']=prominence
            self.assertEqual(eligible,rt.condition(TRIGGERS['sb_court_card_212_eligible'],rt.country))
            self.assertEqual(eligible,rt.condition(TRIGGERS['sb_court_episode_chief'],chief))
        rt.country['laws'].add('law_type:law_sb_chiefly_council')
        self.assertFalse(rt.condition(TRIGGERS['sb_court_card_212_eligible'],rt.country))
        rt.country['vars'].pop('sb_court_privileges_this_reign_var')
        chief['prominence']=25
        self.assertTrue(rt.condition(TRIGGERS['sb_court_card_212_eligible'],rt.country))
    def test_competing_house_scenes_show_the_two_distinct_saved_people(self):
        for card in (213,214):
            rt,*_=self.deliver(card)
            event=fields(EVENTS[f'sb_zulu_court.{card}'])
            self.assertEqual('event_window_2char',event['gui_window'])
            left=rt.ref(event['left_icon'],rt.country);right=rt.ref(event['right_icon'],rt.country)
            self.assertIs(left,rt.country['vars']['sb_court_episode_actor_scope'])
            self.assertIs(right,rt.country['vars']['sb_court_episode_other_scope'])
            self.assertIsNot(left,right)
            self.assertTrue(left['alive'] and right['alive'])
    def test_one_breach_popularity_penalty_and_unrelated_pledges_survive(self):
        rt,king,p,r,chiefs=setup()
        for c in chiefs[:2]:c['vars'].update(sb_court_endorsement_var=1,sb_court_personal_council_scope=king,sb_court_successor_pledge_scope=p)
        rt.effect(EFFECTS['sb_court_reconcile_bargains'],rt.country)
        self.assertEqual(['sb_zulu_court.201'],rt.country['events'])
        for c in chiefs[:2]:self.assertIs(p,c['vars']['sb_court_successor_pledge_scope'])
        rt.effect(EFFECTS['sb_court_reconcile_bargains'],rt.country)
        self.assertEqual(1,len(rt.country['events']))

class CampaignConsequences(unittest.TestCase):
    def test_uncommitted_frontier_pool_excludes_agitators_and_nonpositive_prominence(self):
        for prominence,agitator in itertools.product((-10,0,1,50),(False,True)):
            with self.subTest(prominence=prominence,agitator=agitator):
                rt,king,p,r,chiefs=setup();c=chiefs[0]
                rt.country['members']=[king,p,r,c]
                c.update(prominence=prominence,agitator=agitator)
                rt.effect(EFFECTS['sb_court_prepare_frontier_choice'],rt.country)
                eligible=prominence>0 and not agitator
                self.assertEqual(eligible,'sb_court_frontier_neutral' in rt.scopes)
                rt.effect(EFFECTS['sb_court_frontier_support'],rt.country)
                self.assertEqual(1 if eligible else 0,c['vars']['sb_court_endorsement_var'])
                self.assertNotIn('template',c)  # Eligible generated figures still participate.
                self.assertEqual({},rt.scopes['root']['vars'])
    def test_klip_broker_filters_new_backers_at_selection_and_resolution(self):
        for prominence,agitator in itertools.product((-10,0,1,50),(False,True)):
            with self.subTest(prominence=prominence,agitator=agitator):
                rt,king,p,r,chiefs=setup();c=chiefs[0]
                rt.country['members']=[king,p,r,c]
                c.update(prominence=prominence,agitator=agitator)
                rt.effect(EFFECTS['sb_court_prepare_frontier_choice'],rt.country)
                eligible=prominence>0 and not agitator
                self.assertEqual(eligible,'sb_court_frontier_broker' in rt.scopes)
                rt.scopes['sb_court_frontier_broker']=c  # Previously selected before becoming ineligible.
                rt.effect(EFFECTS['sb_court_klip_broker'],rt.country)
                self.assertEqual(1 if eligible else 0,c['vars']['sb_court_endorsement_var'])
                self.assertEqual(eligible,'sb_court_frontier_broker' in c.get('modifiers',{}))
    def test_new_opposition_prefers_current_backing_over_future_promises(self):
        rt,king,p,r,chiefs=setup()
        for c in chiefs[:2]:
            c['vars'].update(sb_court_endorsement_var=1,sb_court_successor_pledge_scope=p)
        chiefs[2]['vars'].update(sb_court_endorsement_var=-1,sb_court_claimant_scope=r)
        rt.backing()
        self.assertGreater(p['vars']['sb_court_rival_weight_var'],r['vars']['sb_court_rival_weight_var'])
        self.assertGreater(r['vars']['sb_court_current_weight_var'],p['vars']['sb_court_current_weight_var'])
        rt.effect(EFFECTS['sb_court_choose_opposition_patron'],rt.country)
        self.assertIs(r,rt.country['vars']['sb_court_selected_patron_scope'])
    def test_permanent_credit_actual_ruler_two_distinct_houses_and_idempotence(self):
        rt,king,p,r,chiefs=setup();king['modifiers']={'sb_zulu_dynastic_crisis':1}
        body=statements('effect = { sb_court_campaign_result = { CAMPAIGN = blood_river OUTCOME = victory WON = yes DEFEAT_PREROGATIVE = -30 } }')
        rt.effect(body,rt.country)
        self.assertIn('sb_court_blood_river_victory',king['modifiers']);self.assertNotIn('sb_zulu_dynastic_crisis',king['modifiers'])
        self.assertEqual(2,sum(c['vars']['sb_court_endorsement_var']==1 for c in chiefs))
        rt.country['ruler']=p;rt.effect(body,rt.country)
        self.assertNotIn('sb_court_blood_river_victory',p.get('modifiers',{}))
        self.assertEqual({},rt.scopes['root']['vars'])
    def test_generic_defeat_still_recruits_two_and_campaign_penalties_stay_permanent(self):
        rt,king,p,r,chiefs=setup()
        rt.effect(statements('effect = { sb_court_generic_war_result = { WON = no } }'),rt.country)
        self.assertEqual(2,sum(c['vars']['sb_court_endorsement_var']==-1 for c in chiefs))
        for campaign in ('blood_river','swazi'):
            self.assertEqual('-25',fields(COURT_MODIFIERS['sb_court_'+campaign+'_defeat'])['character_popularity_add'])

    def test_two_losses_recruit_largest_neutral_and_two_smallest_allies_except_ndlela(self):
        rt,king,p,r,chiefs=setup()
        for chief,weight in zip(chiefs,(90,20,30,60,40)):
            chief['prominence']=weight
        for chief in chiefs[:3]:chief['vars']['sb_court_endorsement_var']=1
        chiefs[0]['template']='ZUL_ndlela_kasompisi'
        for campaign,neutral,defectors in [('blood_river',chiefs[3],chiefs[1:3]),('swazi',chiefs[4],[])]:
            body=statements('effect = { sb_court_campaign_result = { CAMPAIGN = '+campaign+' OUTCOME = defeat WON = no DEFEAT_PREROGATIVE = -30 } }')
            rt.effect(body,rt.country)
            self.assertEqual([neutral['id']],[c['id'] for c in rt.country['sb_court_'+campaign+'_changes']])
            self.assertEqual([c['id'] for c in defectors],[c['id'] for c in rt.country['sb_court_'+campaign+'_defectors']])
            self.assertIs(p,neutral['vars']['sb_court_claimant_scope'])
            for defector in defectors:self.assertIs(p,defector['vars']['sb_court_claimant_scope'])
            rt.effect(body,rt.country)  # Repeated acknowledgement cannot recruit more houses.
        self.assertEqual(-60,rt.country['vars']['sb_prerogative_var'])
        self.assertEqual(1,chiefs[0]['vars']['sb_court_endorsement_var'])
        self.assertEqual(4,sum(c['vars']['sb_court_endorsement_var']==-1 for c in chiefs))
        self.assertTrue(all(c['vars'].get('sb_court_claimant_scope') is p for c in chiefs[1:]))
        self.assertEqual({},rt.scopes['root']['vars'])

    def test_campaign_rank_uses_whole_house_weight_and_preserves_future_pledges(self):
        for campaign in ('blood_river','swazi'):
            with self.subTest(campaign=campaign):
                rt,king,p,r,chiefs=setup()
                for chief,weight in zip(chiefs,(50,40,30,35,80)):chief['prominence']=weight
                for chief in chiefs[2:]:chief['vars']['sb_court_endorsement_var']=1
                for head in (chiefs[1],chiefs[2]):
                    member=character(head['id']+' member',head['vars']['sb_court_following_var'],25)
                    member['owner']=rt.country;member['vars']['sb_court_home_scope']=rt.country
                    rt.country['members'].append(member)
                for chief in (chiefs[1],chiefs[3]):chief['vars']['sb_court_successor_pledge_scope']=r
                rt.effect(statements('effect = { sb_court_campaign_result = { CAMPAIGN = '+campaign+' OUTCOME = defeat WON = no DEFEAT_PREROGATIVE = -30 } }'),rt.country)
                self.assertEqual([chiefs[1]['id']],[c['id'] for c in rt.country['sb_court_'+campaign+'_changes']])
                self.assertEqual([chiefs[3]['id'],chiefs[2]['id']],[c['id'] for c in rt.country['sb_court_'+campaign+'_defectors']])
                self.assertEqual(-1,chiefs[2]['vars']['sb_court_endorsement_var'])
                self.assertEqual(1,chiefs[4]['vars']['sb_court_endorsement_var'])
                for chief in (chiefs[1],chiefs[3]):
                    self.assertIs(p,chief['vars']['sb_court_claimant_scope'])
                    self.assertIs(r,chief['vars']['sb_court_successor_pledge_scope'])

    def test_defeat_reserves_once_and_does_not_reselect_after_prominence_changes(self):
        rt,king,p,r,chiefs=setup()
        for chief,weight in zip(chiefs,(90,20,30,60,40)):chief['prominence']=weight
        for chief in chiefs[:3]:chief['vars']['sb_court_endorsement_var']=1
        prepare=statements('effect = { sb_court_prepare_campaign_result = { CAMPAIGN = blood_river WON = no } }')
        rt.effect(prepare,rt.country)
        self.assertEqual([1,1,1,0,0],[c['vars']['sb_court_endorsement_var'] for c in chiefs])
        chiefs[0]['prominence']=10;chiefs[4]['prominence']=95
        rt.effect(prepare,rt.country)
        rt.effect(statements('effect = { sb_court_campaign_result = { CAMPAIGN = blood_river OUTCOME = defeat WON = no DEFEAT_PREROGATIVE = -30 } }'),rt.country)
        self.assertEqual([1,-1,-1,-1,0],[c['vars']['sb_court_endorsement_var'] for c in chiefs])

    def test_ineligible_supporters_are_excluded_from_defeat_ranking(self):
        for invalid in ('dead','minor','agitator','zero','retired','foreign','ndlela'):
            with self.subTest(invalid=invalid):
                rt,king,p,r,chiefs=setup();target=chiefs[0]
                target['vars']['sb_court_endorsement_var']=1;target['prominence']=10
                chiefs[1]['vars']['sb_court_endorsement_var']=1
                if invalid=='dead':target['alive']=False
                if invalid=='minor':target['age']=12
                if invalid=='agitator':target['agitator']=True
                if invalid=='zero':target['prominence']=0
                if invalid=='retired':target['vars']['sb_court_retired_var']=1
                if invalid=='foreign':target['owner']={'id':'CAP'}
                if invalid=='ndlela':target['template']='ZUL_ndlela_kasompisi'
                rt.effect(statements('effect = { sb_court_prepare_campaign_result = { CAMPAIGN = swazi WON = no } }'),rt.country)
                self.assertEqual([chiefs[1]['id']],[c['id'] for c in rt.country['sb_court_swazi_defectors']])

    def test_missing_defeat_pool_does_not_substitute_extra_neutrals_or_supporters(self):
        for neutral_count,has_rival in ((0,True),(1,True),(4,True),(5,True),(2,False)):
            with self.subTest(neutral_count=neutral_count,has_rival=has_rival):
                rt,king,p,r,chiefs=setup()
                for chief in chiefs[neutral_count:]:chief['vars']['sb_court_endorsement_var']=1
                if not has_rival:p['alive']=False;r['alive']=False
                rt.effect(statements('effect = { sb_court_campaign_result = { CAMPAIGN = swazi OUTCOME = defeat WON = no DEFEAT_PREROGATIVE = -30 } }'),rt.country)
                self.assertEqual(int(neutral_count>0 and has_rival),len(rt.country['sb_court_swazi_changes']))
                self.assertEqual(min(2,5-neutral_count) if has_rival else 0,len(rt.country['sb_court_swazi_defectors']))
                expected=(int(neutral_count>0)+min(2,5-neutral_count)) if has_rival else 0
                self.assertEqual(expected,sum(c['vars']['sb_court_endorsement_var']==-1 for c in chiefs))

    def test_saved_defeat_cannot_build_a_sons_opposition_after_mpandes_accession(self):
        rt,king,mpande,rival,chiefs=setup()
        son=character('Cetshwayo',0,90,-1,1,age=18)
        son.update(template='ZUL_cetshwayo_heir',owner=rt.country)
        son['vars'].update(sb_court_home_scope=rt.country,sb_court_claimant_scope=son)
        rt.country['members'].append(son)
        rt.effect(statements('effect = { sb_court_prepare_campaign_result = { CAMPAIGN = swazi WON = no } }'),rt.country)
        self.assertIs(son,rt.country['vars']['sb_court_swazi_patron_scope'])
        rt.country['ruler']=mpande
        rt.effect(statements('effect = { sb_court_campaign_result = { CAMPAIGN = swazi OUTCOME = defeat WON = no DEFEAT_PREROGATIVE = -30 } }'),rt.country)
        self.assertFalse(any(c['vars'].get('sb_court_claimant_scope') is son for c in chiefs))


class OpeningPackagesAndLifecycle(unittest.TestCase):
    def test_thirteen_packages_and_native_child_bookkeeping(self):
        expected={
            'ZUL_dingane':{'reserved','ruthless','basic_political_operator'},
            'ZUL_mpande_zulu':{'tactful','basic_political_operator','sb_fecund'},
            'ZUL_gqugqu_claimant':{'basic_political_operator'},
            'ZUL_mkabayi':{'tactful','elder','experienced_political_operator'},
            'ZUL_ndlela_kasompisi':{'ambitious','tactful','elder'},
            'ZUL_zulu_kanogandaya':{'imposing','brave','popular_commander'},
            'SB_ZUL_dambuza':{'basic_political_operator'},'SB_ZUL_mawa':{'elder'},
            'SB_ZUL_nongalaza':{'basic_political_operator'},'SB_ZUL_sotobe':{'basic_diplomat'},
            'ZUL_uthumbu_claimed_son':set(),'ZUL_cetshwayo_heir':set(),'ZUL_mbuyazi_heir':set()}
        import re
        found={}
        for path in (ROOT/'common/character_templates').glob('*.txt'):
            source=path.read_text(encoding='utf-8-sig')
            for name in expected:
                if re.search(r'(?m)^(?:REPLACE:)?'+name+r'\s*=',source):
                    obj=find_object(source,('REPLACE:' if 'REPLACE:'+name in source else '')+name)
                    found[name]=obj
        self.assertEqual(set(expected),set(found))
        for name,traits in expected.items():
            obj=found[name]
            self.assertEqual(traits,set(re.search(r'\btraits\s*=\s*\{([^}]+|)\}',obj)[1].split()))
            self.assertIn('trait_generation = { sb_court_authored_initial_traits = yes }',obj)
        generation=(ROOT/'common/scripted_effects/sb_court_trait_effects.txt').read_text(encoding='utf-8-sig')
        self.assertIn('is_adult = no',generation);self.assertIn('add_trait = trait_child',generation)
        self.assertIn('add_experience = trait_value',generation);self.assertNotIn('add_random_trait',generation)
        self.assertFalse((ROOT/'common/character_templates/00_default_template.txt').exists())
    def test_committed_record_withdraws_switches_or_stays_once(self):
        for roll,outcome in [(0,'withdraw'),(.01,'switch'),(.5,'stay')]:
            rt,king,p,r,chiefs=setup();a=chiefs[0]
            for patron in [king,p,r]:patron['vars']['sb_court_annual_attraction_var']=rt.calc(VALUES['sb_court_patron_attraction'],patron)
            rt.country['sb_court_current_patrons']=[king,p,r]
            a['vars']['sb_court_annual_old_current_scope']=king
            rt.scopes['sb_court_annual_actor']=a
            rt.rolls=[roll,.5,.5]
            rt.effect(statements('effect = { sb_court_roll_record = { RECORD = current PATRONS = sb_court_current_patrons } }'),a)
            new=a['vars'].get('sb_court_annual_new_current_scope')
            if outcome=='withdraw':self.assertIsNone(new)
            elif outcome=='switch':self.assertIn(new,[p,r])
            else:self.assertIs(king,new)
            self.assertEqual(0,a['vars']['sb_court_endorsement_var']) # snapshot is not applied early
            self.assertAlmostEqual(100,sum(rt.choices[0])/100000)
    def test_deck_exit_reentry_and_unrelated_war(self):
        rt,*_=setup()
        rt.effect(EFFECTS['sb_court_deck_monthly'],rt.country)
        pending=rt.country['vars']['sb_court_deck_card_var'];timer=rt.country['timers']['sb_court_deck_wait_var']
        rt.country['vars'].pop('sb_institutions_active_var')
        rt.country['vars'].pop('sb_court_deck_wait_var') # due date passes while suspended
        rt.effect(EFFECTS['sb_court_deck_monthly'],rt.country)
        self.assertEqual(pending,rt.country['vars']['sb_court_deck_card_var'])
        self.assertEqual(timer,rt.country['timers']['sb_court_deck_wait_var'])
        self.assertNotIn('events',rt.country)
        rt.country['vars']['sb_institutions_active_var']=1;rt.country['is_at_war']=True
        rt.effect(EFFECTS['sb_court_deck_monthly'],rt.country)
        self.assertEqual(1,len(rt.country['events']))
    def test_dead_or_minor_claimants_never_supply_new_destinations(self):
        rt,king,p,r,chiefs=setup();p['alive']=False;r['age']=12
        # The already-acknowledged minor pledge stays with the regency controller.
        chiefs[0]['vars']['sb_court_successor_pledge_scope']=r
        rt.country['vars']['sb_court_recognized_heir_scope']=r
        rt.effect(EFFECTS['sb_court_annual_allegiances'],rt.country)
        self.assertEqual([king],rt.country['sb_court_current_patrons'])
        self.assertEqual([],rt.country['sb_court_future_patrons'])
        self.assertIs(r,chiefs[0]['vars']['sb_court_successor_pledge_scope'])


if __name__ == "__main__":
    unittest.main()
