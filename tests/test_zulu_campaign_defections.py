"""Named campaign defections: preview, button execution and stale participants."""
import unittest

from tests.test_blood_river_outcome_events import OutcomeRuntime, EVENTS as BLOOD_EVENTS
from tests.test_zulu_swazi_outcome_events import SwaziRuntime, EVENTS as SWAZI_EVENTS


class CampaignDefections(unittest.TestCase):
    def test_both_event_options_preview_and_apply_the_same_reserved_houses(self):
        for campaign,base,events,event in (
            ('blood_river',OutcomeRuntime,BLOOD_EVENTS,'sb_natal_crisis.082'),
            ('swazi',SwaziRuntime,SWAZI_EVENTS,'sb_swazi_frontier.098'),
        ):
            for change in ('none','withdrawn','dead','agitator','zero','new_ruler','dead_rival'):
                with self.subTest(campaign=campaign,change=change):
                    class PreviewRuntime(base):
                        capture = False
                        def effect(self,nodes,scope,prev=None):
                            for node in self.branches(nodes,scope,prev):
                                key,_,value=node
                                if self.capture and key=='hidden_effect':continue
                                if self.capture and key=='show_as_tooltip':self.effect(value,scope,prev)
                                elif self.capture and key=='custom_tooltip':self.tooltips.append((value,scope['id']))
                                else:super().effect([node],scope,prev)
                    rt=PreviewRuntime();z=rt.country;king=z['ruler'];prince=z['members'][1]
                    neutral,other_neutral,loyal,strong_loyal=z['members'][2:]
                    for actor,weight in zip((neutral,other_neutral,loyal,strong_loyal),(60,40,20,90)):
                        actor['prominence']=weight
                    for actor in (loyal,strong_loyal):actor['vars']['sb_court_endorsement_var']=1
                    if campaign=='blood_river':
                        rt.resolve(('target',));rt.open('070',rt.ora);rt.answer('070',rt.ora)
                        self.assertTrue(rt.open('082',z))
                        answer=lambda:rt.answer('082',z)
                    else:
                        self.assertEqual(event,rt.queue(2));self.assertTrue(rt.open_outcome(event))
                        answer=lambda:rt.answer_outcome(event)
                    self.assertEqual(1,loyal['vars']['sb_court_endorsement_var'])
                    self.assertEqual(0,neutral['vars']['sb_court_endorsement_var'])
                    if change=='withdrawn':loyal['vars']['sb_court_endorsement_var']=0
                    if change=='dead':loyal['alive']=False
                    if change=='agitator':loyal['agitator']=True
                    if change=='zero':loyal['prominence']=0
                    if change=='new_ruler':king['alive']=False;z['ruler']=prince
                    if change=='dead_rival':prince['alive']=False
                    rt.capture=True;rt.tooltips=[]
                    option=next(v for k,_,v in events[event] if k=='option')
                    rt.effect([n for n in option if n[0] not in ('name','default_option','trigger','ai_chance')],z)
                    self.assertEqual(change=='none',('sb_court_campaign_defector_tt',loyal['id']) in rt.tooltips)
                    self.assertEqual(change!='dead_rival',('sb_court_campaign_opposition_tt',neutral['id']) in rt.tooltips)
                    self.assertEqual(change not in ('new_ruler','dead_rival'),('sb_court_campaign_defector_tt',strong_loyal['id']) in rt.tooltips)
                    rt.capture=False
                    answer();answer()
                    self.assertEqual(-1 if change=='none' else (0 if change=='withdrawn' else 1),loyal['vars']['sb_court_endorsement_var'])
                    self.assertEqual(1 if change=='new_ruler' else (0 if change=='dead_rival' else -1),neutral['vars']['sb_court_endorsement_var'])
                    self.assertEqual(1 if change in ('new_ruler','dead_rival') else -1,strong_loyal['vars']['sb_court_endorsement_var'])
                    self.assertEqual(0,other_neutral['vars']['sb_court_endorsement_var'])
                    if change=='none':self.assertIs(prince,loyal['vars']['sb_court_claimant_scope'])
                    self.assertEqual(-10 if campaign=='blood_river' else -15,z['vars']['sb_prerogative_var'])
                    self.assertEqual({},rt.play['vars'])


    def test_ndlela_is_protected_in_both_defection_slots_and_both_campaigns(self):
        for campaign,base in (('blood_river',OutcomeRuntime),('swazi',SwaziRuntime)):
            for ndlela_weight in (1,25,100):
                with self.subTest(campaign=campaign,ndlela_weight=ndlela_weight):
                    rt=base();z=rt.country;prince=z['members'][1]
                    ndlela,first,second,neutral=z['members'][2:]
                    ndlela['template']='ZUL_ndlela_kasompisi'
                    for actor,weight in ((ndlela,ndlela_weight),(first,20),(second,30),(neutral,60)):
                        actor['prominence']=weight
                    for actor in (ndlela,first,second):actor['vars']['sb_court_endorsement_var']=1
                    z['vars']['sb_prerogative_var']=-50
                    if campaign=='blood_river':
                        rt.resolve(('target',));rt.open('070',rt.ora);rt.answer('070',rt.ora)
                        self.assertTrue(rt.open('082',z));rt.answer('082',z);rt.answer('082',z)
                    else:
                        event=rt.queue(2);self.assertTrue(rt.open_outcome(event))
                        rt.answer_outcome(event);rt.answer_outcome(event)
                    self.assertEqual(1,ndlela['vars']['sb_court_endorsement_var'])
                    for actor in (first,second,neutral):
                        self.assertEqual(-1,actor['vars']['sb_court_endorsement_var'])
                        self.assertIs(prince,actor['vars']['sb_court_claimant_scope'])
                    self.assertEqual(-75 if campaign=='blood_river' else -80,z['vars']['sb_prerogative_var'])

if __name__=='__main__':unittest.main()
