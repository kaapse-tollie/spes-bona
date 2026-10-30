"""Execute quotes, both rolls and independent expiries; native wars remain DP's check."""
import unittest
from tests.test_zulu_court_rework import ReworkRuntime, quote_confrontation, ROOT
from tests.test_zulu_court_politics import character, EFFECTS, VALUES, TRIGGERS
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import find_object

EVENT_SOURCE = (ROOT/'events/sb_court_politics_events.txt').read_text(encoding='utf-8-sig')
EVENTS = {name: statements(find_object(EVENT_SOURCE,name)) for name in ('sb_court_politics.008','sb_court_politics.009')}


class CoercionRuntime(ReworkRuntime):
    def __init__(self, members):
        super().__init__(members)
        self.day = 0
        self.expiries = []

    def condition(self, nodes, scope, prev=None):
        for key,op,value in nodes:
            if key == 'is_ai': result=(not scope.get('player',True)) == (value=='yes')
            elif key == 'has_game_rule': result=value in scope.get('rules',set())
            else: result=super().condition([(key,op,value)],scope,prev)
            if not result: return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, _, body = node
            if key in ('set_variable', 'add_modifier', 'trigger_event') and isinstance(body, list):
                f = {k:v for k,_,v in body}
                if 'years' in f or 'days' in f:
                    days = float(f.get('years', 0))*365 + float(f.get('days', 0))
                    name = f.get('name', f.get('id'))
                    if key == 'trigger_event' and name not in ('sb_court_politics.008','sb_court_politics.009'):
                        raise AssertionError(name)
                    self.expiries.append((self.day+days, key, name, scope))
            super().effect([node], scope, prev)

    def advance(self, days):
        end = self.day + days
        while any(item[0] <= end for item in self.expiries):
            entry = min(self.expiries, key=lambda item:item[0])
            self.expiries.remove(entry)
            self.day, kind, name, scope = entry
            if kind == 'set_variable': scope['vars'].pop(name, None)
            elif kind == 'add_modifier': scope.get('modifiers', {}).pop(name, None)
            else:
                immediate = next(body for key,_,body in EVENTS[name] if key == 'immediate')
                self.effect(immediate, scope)
        self.day = end


def opening():
    king = character('Dingane',1,100,1,1)
    prince = character('Mpande',0,30,-1,1)
    prince['template'] = 'ZUL_mpande_zulu'
    prince['vars']['sb_court_claimant_scope'] = prince
    rival = character('Gqugqu',0,30,-1,1)
    rival['template'] = 'ZUL_gqugqu_claimant'
    rival['vars']['sb_court_claimant_scope'] = rival
    ndlela = character('Ndlela',3,81,1,1)
    dambuza = character('Dambuza',0,25,1)
    rt = CoercionRuntime([king,prince,rival,ndlela,dambuza])
    rt.country.update(laws={'law_type:law_monarchy'}, authority=-100)
    rt.country['vars']['sb_prerogative_var'] = 100
    rt.backing()
    return rt,king,prince,rival,ndlela


def attempt(rt, prince, purge, roll):
    rt.roll = roll
    quote_confrontation(rt,prince)
    rt.effect([('sb_court_confrontation','=',[('PURGE','=', 'yes' if purge else 'no')])],rt.country)


class CourtCoercion(unittest.TestCase):
    def test_current_loyalty_blocks_both_actions_even_if_it_changes_after_the_quote(self):
        for purge in (False,True):
            rt,king,prince,rival,_=opening()
            quote_confrontation(rt,prince)
            prince['vars']['sb_court_endorsement_var']=1
            prince['vars']['sb_court_successor_pledge_scope']=rival
            self.assertFalse(rt.condition(TRIGGERS['sb_court_coercion_target_valid'],prince))
            rt.effect([('sb_court_confrontation','=',[('PURGE','=','yes' if purge else 'no')])],rt.country)
            self.assertTrue(prince['alive'])
            self.assertEqual(100,rt.country['vars']['sb_prerogative_var'])
            self.assertFalse(prince.get('sb_court_purge_rulers'))
            self.assertNotIn('sb_court_renunciation_cooldown_var',prince['vars'])
            self.assertNotIn('sb_court_authority_commitment_var',rt.country['vars'])
            prince['vars']['sb_court_endorsement_var']=0
            self.assertTrue(rt.condition(TRIGGERS['sb_court_coercion_target_valid'],prince))

    def test_historical_mpande_waits_for_purge_then_chooses_it(self):
        source=(ROOT/'common/character_interactions/sb_court_interactions.txt').read_text(encoding='utf-8-sig')
        interaction=dict((k,v) for k,_,v in statements(find_object(source,'sb_court_confront_rival')))
        options=[dict((k,v) for k,_,v in body) for key,_,body in statements(find_object(EVENT_SOURCE,'sb_court_politics.003')) if key=='option']

        def event_weights(rt):
            result={}
            for option in options:
                if not rt.condition(option.get('trigger',[]),rt.country): continue
                chance=option['ai_chance']
                weight=float(next(v for k,_,v in chance if k=='base'))
                for key,_,body in chance:
                    if key!='modifier':continue
                    fields=dict((k,v) for k,_,v in body)
                    if not rt.condition(fields.get('trigger',[]),rt.country):continue
                    weight=(weight+float(fields.get('add',0)))*float(fields.get('factor',1))
                result[option['name']]=weight
            return result

        for rule in ('strict_historical','dynamic_historical'):
            rt,king,_,rival,_=opening()
            king['template']='ZUL_mpande_zulu'
            rt.country.update(player=False,rules={'sb_frontier_ai_behavior_'+rule})
            rt.scopes['actor']=rt.country
            rt.country['vars']['sb_prerogative_var']=49
            self.assertEqual(0,rt.calc(interaction['ai_chance'],rival))
            rt.country['vars']['sb_prerogative_var']=50
            self.assertTrue(rt.condition(interaction['possible'],rival))
            self.assertEqual(100,rt.calc(interaction['ai_chance'],rival))
            quote_confrontation(rt,rival)
            self.assertEqual({'sb_court_politics.003.a':0,'sb_court_politics.003.c':100,'sb_court_politics.003.b':0},event_weights(rt))
            rt.country['vars']['sb_prerogative_var']=49
            self.assertEqual({'sb_court_politics.003.a':0,'sb_court_politics.003.b':40},event_weights(rt))
            rt.country['vars']['sb_prerogative_var']=50
            rival['sb_court_purge_rulers']=[king]
            self.assertEqual(0,rt.calc(interaction['ai_chance'],rival))
            self.assertEqual({'sb_court_politics.003.a':0,'sb_court_politics.003.b':40},event_weights(rt))

        for player,rule,king_template,target_template in (
            (True,'strict_historical','ZUL_mpande_zulu','ZUL_gqugqu_claimant'),
            (False,'off','ZUL_mpande_zulu','ZUL_gqugqu_claimant'),
            (False,'strict_historical','ZUL_dingane','ZUL_gqugqu_claimant'),
            (False,'strict_historical','ZUL_mpande_zulu','ZUL_cetshwayo_heir'),
        ):
            rt,king,_,rival,_=opening()
            king['template']=king_template;rival['template']=target_template
            rt.country.update(player=player,rules={'sb_frontier_ai_behavior_'+rule})
            quote_confrontation(rt,rival)
            self.assertEqual(1,rt.calc(interaction['ai_chance'],rival))
            self.assertFalse(rt.condition(TRIGGERS['sb_court_ai_mpande_purge_target'],rival))
            self.assertEqual({'sb_court_politics.003.a':50,'sb_court_politics.003.c':10,'sb_court_politics.003.b':40},event_weights(rt))

    def test_historical_ai_mpande_preserves_both_sons_but_can_confront_gqugqu(self):
        for rule in ('strict_historical','dynamic_historical'):
            for template in ('ZUL_cetshwayo_heir','ZUL_mbuyazi_heir'):
                for purge in (False,True):
                    rt,king,son,gqugqu,_=opening()
                    king['template']='ZUL_mpande_zulu';son['template']=template
                    rt.country.update(player=True,rules={'sb_frontier_ai_behavior_'+rule})
                    # A quote opened under player control must be revalidated after AI takeover.
                    quote_confrontation(rt,son)
                    rt.country['player']=False
                    self.assertFalse(rt.condition(TRIGGERS['sb_court_coercion_target_valid'],son))
                    self.assertTrue(rt.condition(TRIGGERS['sb_court_coercion_target_valid'],gqugqu))
                    rt.roll=0
                    rt.effect([('sb_court_confrontation','=',[('PURGE','=','yes' if purge else 'no')])],rt.country)
                    self.assertTrue(son['alive'])
                    self.assertNotIn('sb_court_claim_renounced_var',son['vars'])
                    self.assertNotIn('sb_court_renunciation_cooldown_var',son['vars'])
                    self.assertFalse(son.get('sb_court_purge_rulers'))
                    self.assertEqual(100,rt.country['vars']['sb_prerogative_var'])
                    self.assertNotIn('sb_court_authority_commitment_var',rt.country['vars'])
                    attempt(rt,gqugqu,False,0)
                    self.assertIn('sb_court_claim_renounced_var',gqugqu['vars'])

    def test_reconciled_loyal_sons_are_protected_for_players_and_off_mode_too(self):
        for player,rule,ruler in ((True,'dynamic_historical','ZUL_mpande_zulu'),
                                  (False,'off','ZUL_mpande_zulu'),
                                  (False,'strict_historical','ZUL_dingane')):
            for template in ('ZUL_cetshwayo_heir','ZUL_mbuyazi_heir'):
                rt,king,son,_,_=opening()
                king['template']=ruler;son['template']=template
                rt.country.update(player=player,rules={'sb_frontier_ai_behavior_'+rule})
                self.assertTrue(rt.condition(TRIGGERS['sb_court_coercion_target_valid'],son))
                attempt(rt,son,False,0)
                if ruler == 'ZUL_mpande_zulu':
                    self.assertEqual(1,son['vars']['sb_court_endorsement_var'])
                    self.assertNotIn('sb_court_claim_renounced_var',son['vars'])
                    self.assertEqual(100,rt.country['vars']['sb_prerogative_var'])
                else:
                    self.assertIn('sb_court_claim_renounced_var',son['vars'])

    def test_successor_preview_does_not_shadow_a_permanent_country_scope(self):
        source=(ROOT/'common/scripted_buttons/sb_court_buttons.txt').read_text(encoding='utf-8-sig')
        button=dict((k,v) for k,_,v in statements(find_object(source,'sb_court_recognize_successor_button')))
        self.assertNotIn('save_temporary_scope_as',str(button['possible']))
        rt,king,son,rival,_=opening()
        king['template']='ZUL_mpande_zulu';son['template']='ZUL_cetshwayo_heir'
        rival['vars']['sb_court_claim_renounced_var']=1
        rt.scopes['sb_court_country']=rt.scopes['root'] # Permanent foreign event target.
        self.assertTrue(rt.condition(button['possible'],rt.country))
        self.assertIs(rt.scopes['root'],rt.scopes['sb_court_country'])
        son['vars']['sb_court_home_scope']=rt.scopes['root']
        self.assertFalse(rt.condition(button['possible'],rt.country))
        son['vars']['sb_court_home_scope']=rt.country;son['age']=1
        self.assertTrue(rt.condition(button['possible'],rt.country)) # Designation still permits children.
        son['vars']['sb_court_claim_renounced_var']=1
        self.assertFalse(rt.condition(button['possible'],rt.country))
        self.assertIs(rt.scopes['root'],rt.scopes['sb_court_country'])

    def test_opening_odds_and_exact_complements(self):
        rt,king,prince,rival,_ = opening()
        self.assertEqual(196,rt.country['vars']['sb_court_incumbent_weight_var'])
        self.assertEqual(306,rt.country['vars']['sb_court_current_pledged_weight_var'])
        for target in (prince,rival):
            quote_confrontation(rt,target)
            v=rt.country['vars']
            self.assertEqual((78.1,64.1),(v['sb_court_offer_submission_var'],v['sb_court_offer_capture_var']))
            self.assertAlmostEqual(100,v['sb_court_offer_submission_var']+v['sb_court_offer_refusal_var'])
            self.assertAlmostEqual(100,v['sb_court_offer_capture_var']+v['sb_court_offer_escape_var'])
            self.assertAlmostEqual(55/306*100,v['sb_court_offer_rival_share_var'])
        self.assertNotIn('sb_court_authority_commitment_var',rt.country['vars'])

    def test_purge_is_strictly_harder_including_zero_backing_edges(self):
        rt,_,prince,_,_ = opening()
        rt.country['vars']['sb_court_action_actor_scope']=prince
        for k in (0,1,25,100,500):
            for r in (0,1,25,100,500):
                if k+r==0:continue
                rt.country['vars']['sb_court_incumbent_weight_var']=k
                prince['vars']['sb_court_current_weight_var']=r
                revoke=rt.calc(VALUES['sb_court_submission_chance'],rt.country)
                purge=rt.calc(VALUES['sb_court_capture_chance'],rt.country)
                self.assertLess(purge,revoke)
                self.assertTrue(10<=revoke<=90 and 5<=purge<=85)

    def test_failed_renunciation_leaves_purge_available_and_stacks_authority(self):
        rt,king,prince,_,_ = opening()
        attempt(rt,prince,False,.999)
        self.assertEqual(75,rt.country['vars']['sb_prerogative_var'])
        self.assertEqual(100,rt.country['modifiers']['sb_court_committed_authority'])
        self.assertTrue(prince['alive'])
        self.assertFalse(prince.get('is_in_exile_pool',False))
        self.assertEqual(65,rt.ref('prominence',prince))
        self.assertFalse(prince.get('sb_court_purge_rulers'))
        self.assertNotIn('sb_court_public_discredit',king.get('modifiers',{}))
        attempt(rt,prince,True,.999)
        self.assertEqual(25,rt.country['vars']['sb_prerogative_var'])
        self.assertEqual(300,rt.country['modifiers']['sb_court_committed_authority'])
        self.assertTrue(prince['is_in_exile_pool'])
        self.assertIs(prince,prince['vars']['sb_court_claimant_scope'])
        self.assertEqual([king],prince['sb_court_purge_rulers'])
        self.assertNotIn('sb_court_authority_commitment_var',rt.scopes['root']['vars'])

    def test_purge_does_not_consume_renunciation_and_is_once_per_ruler(self):
        rt,king,prince,_,_ = opening()
        attempt(rt,prince,True,.999)
        self.assertNotIn('sb_court_renunciation_cooldown_var',prince['vars'])
        prince['is_in_exile_pool']=False  # A later genuine return; no migration.
        rt.country['vars']['sb_prerogative_var']=100
        attempt(rt,prince,True,0)
        self.assertTrue(prince['alive'])
        self.assertEqual(100,rt.country['vars']['sb_prerogative_var'])
        attempt(rt,prince,False,.999)
        self.assertEqual(75,rt.country['vars']['sb_prerogative_var'])
        new=character('new ruler',1,100,1,1)
        new.update(owner=rt.country)
        new['vars']['sb_court_home_scope']=rt.country
        rt.country['members'].append(new)
        rt.country['ruler']=new
        rt.country['vars']['sb_prerogative_var']=100
        attempt(rt,prince,True,.999)
        self.assertEqual([king,new],prince['sb_court_purge_rulers'])
        prince['is_in_exile_pool']=False
        rt.country['ruler']=king
        rt.country['vars']['sb_prerogative_var']=100
        attempt(rt,prince,True,0)
        self.assertTrue(prince['alive'])
        self.assertEqual(100,rt.country['vars']['sb_prerogative_var'])

    def test_ten_year_cooldown_and_independent_authority_expiries(self):
        rt,_,prince,rival,_ = opening()
        attempt(rt,prince,False,.999)
        rt.advance(365)
        attempt(rt,rival,True,0)
        self.assertFalse(rival['alive'])
        self.assertEqual(300,rt.country['modifiers']['sb_court_committed_authority'])
        rt.advance(3284)
        rt.country['vars']['sb_prerogative_var']=100
        attempt(rt,prince,False,.999)
        self.assertEqual(100,rt.country['vars']['sb_prerogative_var'])
        rt.advance(1)
        self.assertNotIn('sb_court_renunciation_cooldown_var',prince['vars'])
        self.assertNotIn('sb_court_claim_defended',prince['modifiers'])
        self.assertEqual(200,rt.country['modifiers']['sb_court_committed_authority'])
        attempt(rt,prince,False,.999)
        self.assertEqual(300,rt.country['modifiers']['sb_court_committed_authority'])
        # Institutional exit does not refund already committed Authority.
        rt.country['vars'].pop('sb_institutions_active_var')
        rt.advance(365)
        self.assertEqual(100,rt.country['modifiers']['sb_court_committed_authority'])
        rt.advance(3285)
        self.assertNotIn('sb_court_committed_authority',rt.country['modifiers'])
        self.assertNotIn('sb_court_authority_commitment_var',rt.country['vars'])

    def test_renunciation_releases_targeted_pledges_and_preserves_house_and_constitution(self):
        rt,king,prince,rival,ndlela = opening()
        ndlela['vars']['sb_court_successor_pledge_scope']=prince
        backer=character('prince supporter',9,40,-1,2)
        backer.update(owner=rt.country)
        backer['vars'].update(sb_court_home_scope=rt.country,sb_court_claimant_scope=prince,sb_court_successor_pledge_scope=rival)
        rt.country['members'].append(backer)
        prince['heir']=True
        rt.country['heir']=prince
        rt.country['vars']['sb_court_recognized_heir_scope']=prince
        attempt(rt,prince,False,0)
        self.assertEqual(0,prince['vars']['sb_court_endorsement_var'])
        self.assertEqual(0,backer['vars']['sb_court_endorsement_var'])
        self.assertEqual(2,backer['vars']['sb_court_alignment_var'])
        self.assertIs(rival,backer['vars']['sb_court_successor_pledge_scope'])
        self.assertEqual(1,ndlela['vars']['sb_court_endorsement_var'])
        self.assertNotIn('sb_court_successor_pledge_scope',ndlela['vars'])
        self.assertTrue(prince['alive'])
        self.assertEqual(30,rt.ref('prominence',prince))
        self.assertNotIn('sb_court_junior_status',prince.get('modifiers',{}))
        self.assertNotIn('heir',rt.country)

    def test_quote_change_reconfirms_and_invalid_participant_does_not_charge(self):
        for mutation in ('weight','death','ruler','owner','prototype'):
            rt,king,prince,rival,ndlela=opening()
            quote_confrontation(rt,prince)
            if mutation=='weight':ndlela['prominence']+=10
            elif mutation=='death':prince['alive']=False
            elif mutation=='ruler':rt.country['ruler']=rival
            elif mutation=='owner':prince['owner']=rt.scopes['root']
            else:prince['prominence']+=100
            rt.effect([('sb_court_confrontation','=',[('PURGE','=','yes')])],rt.country)
            self.assertEqual(100,rt.country['vars']['sb_prerogative_var'])
            self.assertFalse(prince.get('sb_court_purge_rulers'))
            self.assertNotIn('sb_court_authority_commitment_var',rt.country['vars'])
            if mutation=='weight':self.assertEqual(2,rt.country['events'].count('sb_court_politics.003'))

    def test_war_threshold_uses_current_pledged_pool_not_future_or_uncommitted(self):
        rt,king,prince,rival,ndlela=opening()
        king['prominence']=101
        prince['prominence']=59  # (59+25) / (197 + 55 + 84) = exactly 25%.
        ndlela['vars']['sb_court_successor_pledge_scope']=prince
        neutral=character('neutral',8,100)
        neutral.update(owner=rt.country)
        neutral['vars']['sb_court_home_scope']=rt.country
        rt.country['members'].append(neutral)
        quote_confrontation(rt,prince)
        self.assertEqual(25,prince['vars']['sb_court_current_share_var'])
        self.assertTrue(rt.condition([('sb_court_can_attempt_purge','=','yes')],prince))
        self.assertTrue(rt.condition([('sb_court_can_request_renunciation','=','yes')],prince))
        self.assertTrue(rt.condition([('sb_court_can_attempt_purge','=','yes')],prince))
        prince['prominence']-=1
        rt.backing()
        self.assertTrue(rt.condition([('sb_court_can_attempt_purge','=','yes')],prince))

    def test_living_ruler_conflict_places_whole_houses_by_current_allegiance(self):
        rt,king,prince,rival,ndlela=opening()
        head=character('opposing head',10,80,-1)
        head['vars']['sb_court_claimant_scope']=prince
        junior=character('loyal junior',10,20,1)
        for person in (head,junior):
            person['owner']=rt.country
            person['vars']['sb_court_home_scope']=rt.country
            rt.country['members'].append(person)
        ndlela['vars']['sb_court_successor_pledge_scope']=prince
        rt.backing()
        rt.country['vars'].update(sb_court_dynastic_nominee_scope=king,
            sb_court_dynastic_rival_scope=prince,sb_court_dynastic_reason_var=3)
        rt.effect(EFFECTS['sb_court_snapshot_dynastic_coalitions'],rt.country)
        rebels=rt.country['sb_court_dynastic_rival_members']
        for person,expected in ((king,False),(prince,True),(rival,False),
                                (ndlela,False),(head,True),(junior,True)):
            self.assertEqual(expected,any(p is person for p in rebels),person['id'])
        rt.country['vars']['sb_court_dynastic_reason_var']=2
        rt.effect(EFFECTS['sb_court_snapshot_dynastic_coalitions'],rt.country)
        self.assertTrue(any(p is ndlela for p in rt.country['sb_court_dynastic_rival_members']))



if __name__ == '__main__':
    unittest.main()
