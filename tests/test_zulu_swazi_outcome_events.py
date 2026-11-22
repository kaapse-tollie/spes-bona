"""Zulu's terminal Swazi result is reserved once and applied by its own event option."""
from pathlib import Path
import unittest
from tests.test_blood_river_outcome_events import DYNASTY, OutcomeRuntime
from tests.test_zulu_court_event_package import fields, COURT_MODIFIERS
from tests.test_zulu_court_politics import definitions
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import find_object

SUCCESSION = definitions('common/scripted_effects/sb_zulu_dynasty_succession_effects.txt')
EVENT_SOURCE = (Path(__file__).resolve().parents[1]/'events/sb_swazi_frontier_events.txt').read_text(encoding='utf-8-sig')
EVENTS = {key:statements(find_object(EVENT_SOURCE,key)) for key in ('sb_swazi_frontier.097','sb_swazi_frontier.098')}
ROOT = Path(__file__).resolve().parents[1]

class SwaziRuntime(OutcomeRuntime):
    def effect(self,nodes,scope,prev=None):
        for node in self.branches(nodes,scope,prev):
            key,_,value=node
            if key in SUCCESSION:
                body=SUCCESSION[key]
                if isinstance(value,list):
                    def subst(nodes):
                        params=fields(value)
                        if isinstance(nodes,list):return [(subst(k),op,subst(v)) for k,op,v in nodes]
                        for k,v in params.items():nodes=nodes.replace('$'+k+'$',v)
                        return nodes
                    body=subst(body)
                self.effect(body,scope,prev)
            elif key=='s:STATE_EAST_TRANSVAAL':
                self.country.setdefault('claims',[]).append(key)
            elif key=='custom_tooltip':
                scope.setdefault('tooltips',[]).append(value)
            else: super().effect([node],scope,prev)
    def condition(self,nodes,scope,prev=None):
        for node in nodes:
            if node[0]=='sb_is_zulu_dynasty_country':
                if scope['id'] not in ('ZUL','NGN'):return False
        return super().condition([n for n in nodes if n[0]!='sb_is_zulu_dynasty_country'],scope,prev)
    def queue(self,result):
        event='sb_swazi_frontier.'+('097' if result==1 else '098')
        self.effect(statements('effect = { sb_zulu_queue_swazi_campaign_outcome = { RESULT = '+str(result)+' } }'),self.country)
        return event
    def open_outcome(self,event):
        body=fields(EVENTS[event]);self.scopes['root']=self.country
        if not self.condition(body['trigger'],self.country):return False
        self.effect(body['immediate'],self.country)
        self.contexts[event]=dict(self.scopes)
        return True
    def answer_outcome(self,event):
        self.scopes=dict(self.contexts[event])
        option=next(v for k,_,v in EVENTS[event] if k=='option')
        self.effect([n for n in option if n[0] not in ('name','default_option','ai_chance')],self.country)

class SwaziOutcomes(unittest.TestCase):
    def test_both_outcomes_wait_for_the_event_and_cannot_be_applied_twice(self):
        for result,label,count in ((1,'victory',2),(2,'defeat',1)):
            with self.subTest(result=result):
                rt=SwaziRuntime();z=rt.country;king=z['ruler']
                event=rt.queue(result);rt.queue(result)
                self.assertEqual([event],z['events'])
                self.assertNotIn('sb_court_swazi_result_var',z['vars'])
                self.assertNotIn('sb_court_swazi_'+label,king.get('modifiers',{}))
                self.assertEqual(15,z['vars']['sb_prerogative_var'])
                self.assertTrue(rt.open_outcome(event))
                self.assertEqual(count,len(z['sb_court_swazi_changes']))
                self.assertNotIn('sb_court_swazi_'+label,king.get('modifiers',{}))
                self.assertEqual(15,z['vars']['sb_prerogative_var'])
                self.assertNotIn('sb_court_swazi_result_var',z['vars'])
                self.assertTrue(all(c['vars']['sb_court_endorsement_var']==0 for c in z['sb_court_swazi_changes']))
                rt.answer_outcome(event);rt.answer_outcome(event)
                self.assertIn('sb_court_swazi_'+label,king['modifiers'])
                self.assertEqual(15 if result==1 else -15,z['vars']['sb_prerogative_var'])
                self.assertNotIn('sb_court_swazi_outcome_pending_var',z['vars'])
                self.assertFalse(rt.open_outcome(event));rt.queue(result)
                self.assertEqual([event],z['events'])
                self.assertEqual({},rt.play['vars'])
                if result==1:self.assertEqual(['s:STATE_EAST_TRANSVAAL'],z['claims'])
                else:self.assertNotIn('claims',z)

    def test_prior_blood_river_defeat_alone_increases_swazi_defeat_shock(self):
        for prior in ('defeat','victory','neutral'):
            for initial in (15,-40):
                with self.subTest(prior=prior,initial=initial):
                    rt=SwaziRuntime();z=rt.country
                    # ROOT remains the diplomatic play: the history belongs to ZUL.
                    rt.effect(DYNASTY['sb_zulu_apply_blood_river_'+prior],z)
                    self.assertEqual(prior=='defeat','sb_zulu_blood_river_defeat_var' in z['vars'])
                    self.assertEqual(-10 if prior=='defeat' else 15,z['vars']['sb_prerogative_var'])
                    # Choosing a Swazi campaign clears the temporary AI context.
                    if prior=='defeat':
                        rt.effect(DYNASTY['sb_zulu_mark_swazi_question_after_blood_river_loss'],z)
                    rt.effect(DYNASTY['sb_zulu_clear_swazi_question_ai_context'],z)
                    self.assertNotIn('sb_zulu_swazi_ai_lost_blood_river_var',z['vars'])
                    z['vars']['sb_prerogative_var']=initial
                    event=rt.queue(2)
                    self.assertTrue(rt.open_outcome(event))
                    self.assertEqual(initial,z['vars']['sb_prerogative_var'])
                    rt.answer_outcome(event);rt.answer_outcome(event)
                    self.assertEqual(initial-(50 if prior=='defeat' else 30),z['vars']['sb_prerogative_var'])
                    tooltip='sb_swazi_frontier.098.prerogative'+('_after_blood_river' if prior=='defeat' else '')
                    self.assertEqual([tooltip],[t for t in z['tooltips'] if t.startswith('sb_swazi_frontier.098.prerogative')])
                    self.assertEqual({},rt.play['vars'])
                    self.assertNotIn('sb_zulu_blood_river_defeat_var',rt.ora['vars'])

    def test_swazi_victory_after_blood_river_defeat_has_no_extra_shock(self):
        rt=SwaziRuntime();z=rt.country
        rt.effect(DYNASTY['sb_zulu_apply_blood_river_defeat'],z)
        event=rt.queue(1)
        self.assertTrue(rt.open_outcome(event))
        rt.answer_outcome(event)
        self.assertEqual(-10,z['vars']['sb_prerogative_var'])

    def test_successor_does_not_receive_the_old_rulers_credit_or_blame(self):
        for result in (1,2):
            rt=SwaziRuntime();z=rt.country;king=z['ruler'];event=rt.queue(result)
            z['ruler']=z['members'][1]
            self.assertTrue(rt.open_outcome(event))
            name='sb_court_swazi_'+('victory' if result==1 else 'defeat')
            self.assertNotIn(name,king.get('modifiers',{}))
            rt.answer_outcome(event)
            self.assertIn(name,king['modifiers'])
            self.assertNotIn(name,z['ruler'].get('modifiers',{}))
            self.assertIs(king,rt.scopes['sb_court_outcome_portrait'])

    def test_dead_ruler_has_no_modifier_and_picture_uses_the_successor(self):
        rt=SwaziRuntime();z=rt.country;king=z['ruler'];event=rt.queue(2)
        king['alive']=False;z['ruler']=z['members'][1]
        self.assertTrue(rt.open_outcome(event))
        rt.answer_outcome(event)
        self.assertNotIn('sb_court_swazi_defeat',king.get('modifiers',{}))
        self.assertIs(z['ruler'],rt.scopes['sb_court_outcome_portrait'])

    def test_terminal_handlers_queue_both_backdowns_and_war_results(self):
        source=(ROOT/'common/on_actions/sb_diplomatic_play_on_action_handlers.txt').read_text()
        self.assertEqual(2,source.count('RESULT = 1'))
        self.assertEqual(2,source.count('RESULT = 2'))
        self.assertNotIn('sb_zulu_apply_swazi_campaign_victory = yes',source)
        self.assertNotIn('sb_zulu_apply_swazi_campaign_defeat = yes',source)
        timer_source=find_object(source,'sb_on_spes_bona_wargoal_enforced_by_timer')
        timer=fields(statements(timer_source))['effect']
        self.assertEqual('enforced_by_timer',fields(timer)['save_temporary_scope_as'])
        self.assertEqual({'save_temporary_scope_as','if','sb_klip_river_handle_wargoal_enforced','sb_bechuanaland_track_crisis_wargoal_enforcement'},set(fields(timer)))
        self.assertNotIn('sb_zulu_swazi_',timer_source)

if __name__=='__main__':unittest.main()
