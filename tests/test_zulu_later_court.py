"""Execute the later-court transactions against native-boundary fixtures.

Native country creation, subject eligibility, territorial transfer and play creation
are primitives here, not claims of engine/UI verification. The shipped scripts
supply the conditions, actor routing, prices, receipts and order of operations.
"""
import unittest
from tests.test_zulu_dunn_event import DunnRuntime
from tests.test_zulu_court_politics import EFFECTS, VALUES, TRIGGERS, definitions
from tests.test_zulu_frontier_followup import field

VALUES.update(definitions('common/script_values/sb_hamu_bargain_values.txt'))
PROVINCES = ('xE1E455','xE882CE','xBE6FEE','x904EBE','x9E9742')
RESIDUAL = ('x1A084B','x41C070','x88FAD4','xBFA16B')


class LaterCourtRuntime(DunnRuntime):
    def __init__(self):
        super().__init__(18600101)
        self.sponsor = {'id':'TRN','alive':True,'vars':{},'states':[{'state_region':'s:STATE_EAST_TRANSVAAL'}],
                        'gold_reserves':10,'gold_reserves_limit':10000,'can_have_subjects':True,'player':True}
        self.countries['c:TRN'] = self.sponsor
        self.countries['c:GBR']['ruler'] = self.country['ruler']
        self.global_vars['sb_swazi_boer_border_resolved_global_var'] = 1
        self.hamu = self.actor('SB_ZUL_hamu',6,26,1)
        self.global_vars['sb_court_hamu_identity_scope'] = self.hamu
        self.house = self.actor('Independent chief',11,40,0)
        self.house['prominence'] = 100
        self.country['ruler'] = self.cetshwayo
        self.country['states'] = []
        self.provinces = {p:{'id':p,'state':{'owner':self.country}} for p in PROVINCES+RESIDUAL}
        self.region = {'id':'STATE_ZULULAND','vars':{}}
        self.subject_allowed = True
        self.defer_subject = False
        self.defer_country_alive = False
        self.transfers = []

    def ref(self,key,scope,prev=None):
        if key.startswith('p:'):
            name,_,tail=key[2:].partition('.')
            obj=self.provinces.get(name)
            return self.ref(tail,obj,prev) if tail else obj
        if key == 'region_state:NRP':return {'owner':self.countries.get('c:NRP'),'vars':{}}
        if key.startswith('s:STATE_ZULULAND'):
            if '.region_state:NRP' in key:
                return {'owner':self.countries.get('c:NRP'),'vars':{}}
            return self.region
        return super().ref(key,scope,prev)

    def condition(self,nodes,scope,prev=None):
        branch=None
        for node in nodes:
            key,op,value=node
            if key=='trigger_if':
                branch=self.condition(field(value,'limit'),scope,prev)
                if branch and not self.condition([n for n in value if n[0]!='limit'],scope,prev):return False
                continue
            if key=='trigger_else':
                if branch is False and not self.condition(value,scope,prev):return False
                continue
            if key in ('can_have_subjects','is_player','is_ai','in_default'):
                actual=not scope.get('player',True) if key=='is_ai' else scope.get(key,scope.get('player',False) if key=='is_player' else False)
                result=actual == (value=='yes')
            elif key == 'container_exists': result=False
            elif key in ('is_direct_subject_of','is_subject_of'):
                result=scope.get('overlord') is self.ref(value,scope,prev)
            elif key == 'is_subject_type': result=scope.get('subject_type') == value
            elif key == 'is_subject': result=('overlord' in scope) == (value=='yes')
            elif key == 'can_have_as_subject': result=self.subject_allowed
            elif key in ('has_truce_with','has_war_with'): result=False
            else: result=super().condition([node],scope,prev)
            if not result:return False
        return True

    def effect(self,nodes,scope,prev=None):
        for node in self.branches(nodes,scope,prev):
            key,op,value=node
            if key == 'create_country':
                nrp={'id':'NRP','alive':not self.defer_country_alive,'vars':{},'states':[],'members':[],'characters':[]}
                self.countries['c:NRP']=nrp
                self.provinces['xE1E455']['state']['owner']=nrp
                self.effect(field(value,'on_created'),nrp,scope)
            elif key == 'can_have_as_subject': raise AssertionError('trigger used as effect')
            elif key == 'create_diplomatic_pact':
                if not self.defer_subject:
                    target=self.ref(field(value,'country'),scope,prev)
                    target.update(overlord=scope,subject_type='subject_type_sb_boer_confederal_partner')
            elif key == 'sb_nrp_apply_boer_republic_setup': scope.setdefault('setup_calls',[]).append('boer')
            elif key == 'set_owner_of_provinces':
                target=self.ref(field(value,'country'),scope,prev)
                for p,_,_ in field(value,'provinces'):
                    self.provinces[p]['state']['owner']=target
                    self.transfers.append((p,target['id']))
            elif key == 'set_state_type': scope['state_type']=value
            elif key == 'create_diplomatic_play':
                target=self.ref(field(value,'target_country'),scope,prev)
                self.participants=[scope,target]
                self.play={'id':'real_play','type':field(value,'type'),'initiator':scope,'target':target,'vars':{}}
                old=dict(self.scopes)
                self.scopes.update(root=self.play,initiator=scope,target=target)
                self.effect(EFFECTS['sb_hamu_configure_boundary_play'],self.play)
                self.scopes=old
            elif key in ('add_target_backers','add_initiator_backers'):
                self.participants.extend(self.ref(x,scope,prev) for x,_,_ in value)
                scope.setdefault(key,[]).append(value)
            elif key in ('add_war_goal','remove_war_goal'):
                if key=='add_war_goal':assert any(self.ref(field(value,'holder'),scope,prev) is p for p in self.participants), 'nonparticipant holder'
                scope.setdefault(key,[]).append(value)
            elif key == 'overlord':
                obj=self.ref(key,scope,prev)
                if obj is not None:self.effect(value,obj,scope)
            elif key.startswith(('p:','s:','region_state:')):
                obj=self.ref(key,scope,prev)
                if obj is not None:self.effect(value,obj,scope)
            else:super().effect([node],scope,prev)

    def run(self,name,scope=None):self.effect(EFFECTS[name],scope if scope is not None else self.country)
    def offer(self):self.run('sb_hamu_open_offer',self.sponsor)
    def accept(self):self.offer();self.run('sb_hamu_accept_offer',self.sponsor)
    def accede(self):
        self.country['ruler']=self.hamu
        self.run('sb_hamu_record_accession')
    def fulfil(self):self.accept();self.accede();self.run('sb_hamu_contract_monthly',self.sponsor)


class HamuContractTests(unittest.TestCase):
    def test_foreign_root_quote_debt_and_once_only_backing(self):
        rt=LaterCourtRuntime();rt.offer()
        self.assertEqual(10000,rt.sponsor['vars']['sb_hamu_grant_var'])
        rt.sponsor['gold_reserves_limit']=50000
        rt.run('sb_hamu_accept_offer',rt.sponsor)
        self.assertEqual(-9990,rt.sponsor['gold_reserves'])
        self.assertIs(rt.hamu,rt.house['vars']['sb_court_claimant_scope'])
        rt.run('sb_hamu_accept_offer',rt.sponsor)
        self.assertEqual(-9990,rt.sponsor['gold_reserves'])
        self.assertEqual({},rt.scopes['root']['vars'])

    def test_stale_house_does_not_replace_or_steal_another_house(self):
        rt=LaterCourtRuntime();rt.offer();rt.house['vars']['sb_court_endorsement_var']=1
        rt.run('sb_hamu_accept_offer',rt.sponsor)
        self.assertNotIn('sb_hamu_backer_joined_var',rt.sponsor['vars'])
        self.assertEqual(1,rt.house['vars']['sb_court_endorsement_var'])
        self.assertIn('sb_hamu_contract_var',rt.sponsor['vars'])

    def test_stale_prince_or_land_cancels_payment(self):
        for bad in ('dead','renounced','foreign_land','earlier_promise'):
            rt=LaterCourtRuntime();rt.offer()
            if bad=='dead':rt.hamu['alive']=False
            elif bad=='renounced':rt.hamu['vars']['sb_court_claim_renounced_var']=1
            elif bad=='foreign_land':rt.provinces['x9E9742']['state']['owner']=rt.countries['c:NAL']
            else:rt.global_vars['sb_nrp_chiefdoms_promise_var']=1
            rt.run('sb_hamu_accept_offer',rt.sponsor)
            self.assertEqual(10,rt.sponsor['gold_reserves'],bad)
            self.assertNotIn('sb_hamu_contract_var',rt.sponsor['vars'],bad)

    def test_stop_resume_subsidy_retains_paid_promise_without_second_house(self):
        rt=LaterCourtRuntime();rt.accept()
        rt.run('sb_hamu_start_funding',rt.sponsor)
        rt.run('sb_hamu_stop_funding',rt.sponsor)
        self.assertIn('sb_hamu_promise_live_var',rt.global_vars)
        self.assertNotIn('sb_hamu_subsidy_cost',rt.sponsor['modifiers'])
        self.assertNotIn('sb_hamu_boer_patronage',rt.hamu['modifiers'])
        rt.run('sb_hamu_start_funding',rt.sponsor)
        self.assertEqual({'sb_hamu_boer_patronage':1},rt.hamu['modifiers'])
        self.assertEqual(-9990,rt.sponsor['gold_reserves'])

    def test_dead_renounced_missing_prince_and_sponsor_release_reservation(self):
        for bad in ('dead','renounced','missing','sponsor'):
            rt=LaterCourtRuntime();rt.accept();rt.run('sb_hamu_start_funding',rt.sponsor)
            if bad=='dead':rt.hamu['alive']=False
            elif bad=='renounced':rt.hamu['vars']['sb_court_claim_renounced_var']=1
            elif bad=='missing':rt.sponsor['vars'].pop('sb_hamu_prince_scope')
            else:rt.sponsor['alive']=False
            rt.run('sb_hamu_contract_monthly',rt.sponsor)
            self.assertIn('sb_hamu_failed_var',rt.sponsor['vars'],bad)
            self.assertNotIn('sb_hamu_promise_live_var',rt.global_vars,bad)
            self.assertNotIn('sb_hamu_subsidy_cost',rt.sponsor['modifiers'],bad)

    def test_existing_earned_chiefdom_promise_blocks_offer(self):
        for receipt in ('sb_nrp_chiefdoms_promise_var','sb_nrp_chiefdoms_earned_var','sb_nrp_reward_consumed_var'):
            rt=LaterCourtRuntime();rt.global_vars[receipt]=1;rt.offer()
            self.assertNotIn('sb_hamu_offer_open_var',rt.sponsor['vars'])

    def test_actual_accession_yields_coastal_confederal_partner_once(self):
        rt=LaterCourtRuntime();rt.fulfil();nrp=rt.countries['c:NRP']
        self.assertIs(rt.sponsor,nrp['overlord'])
        self.assertEqual('subject_type_sb_boer_confederal_partner',nrp['subject_type'])
        self.assertTrue(all(rt.provinces[p]['state']['owner'] is nrp for p in PROVINCES))
        self.assertTrue(all(rt.provinces[p]['state']['owner'] is rt.country for p in RESIDUAL))
        self.assertIn('sb_nrp_reward_consumed_var',rt.global_vars)
        rt.run('sb_hamu_contract_monthly',rt.sponsor)
        self.assertEqual(1,rt.sponsor['events'].count('sb_hamu_bargain.003'))
        self.assertNotIn('sb_nrp_boundary_pending_var',nrp['vars'])
        self.assertNotIn('sb_nrp_union_wait_var',nrp['vars'])

    def test_native_subject_creation_can_retry_without_ceding_coast(self):
        rt=LaterCourtRuntime();rt.accept();rt.accede();rt.defer_subject=True
        rt.run('sb_hamu_contract_monthly',rt.sponsor)
        self.assertIs(rt.country,rt.provinces['x9E9742']['state']['owner'])
        self.assertNotIn('sb_hamu_fulfilled_var',rt.sponsor['vars'])
        rt.defer_subject=False;rt.run('sb_hamu_finalise_nrp',rt.sponsor)
        self.assertIn('sb_hamu_fulfilled_var',rt.sponsor['vars'])
        self.assertEqual(['boer'],rt.countries['c:NRP']['setup_calls'])

    def test_faction_head_does_not_earn_land_and_authentic_split_survives(self):
        rt=LaterCourtRuntime();rt.accept()
        rebel={'id':'R01','alive':True,'vars':{'sb_court_dynastic_opponent_scope':rt.country},'ruler':rt.hamu}
        rt.provinces['x9E9742']['state']['owner']=rebel
        # The war controller only installs this head; it has not called completed accession.
        rt.run('sb_hamu_contract_monthly',rt.sponsor)
        self.assertNotIn('sb_hamu_earned_var',rt.sponsor['vars'])
        self.assertNotIn('sb_hamu_failed_var',rt.sponsor['vars'])

    def test_earned_reunion_waits_for_loser_but_not_third_party(self):
        rt=LaterCourtRuntime();rt.accept()
        loser={'id':'R01','alive':False,'vars':{}}
        rt.country['vars']['sb_court_dynastic_opponent_scope']=loser
        rt.accede();rt.provinces['x9E9742']['state']['owner']=loser
        rt.run('sb_hamu_contract_monthly',rt.sponsor)
        self.assertNotIn('sb_hamu_failed_var',rt.sponsor['vars'])
        rt.provinces['x9E9742']['state']['owner']=rt.countries['c:NAL']
        rt.run('sb_hamu_contract_monthly',rt.sponsor)
        self.assertIn('sb_hamu_failed_var',rt.sponsor['vars'])
        self.assertNotIn('c:NRP',rt.countries)

    def test_british_gate_is_dormant_then_actual_overlord_receives_choice(self):
        rt=LaterCourtRuntime();rt.fulfil();nrp=rt.countries['c:NRP']
        rt.run('sb_hamu_boundary_monthly',nrp)
        self.assertNotIn('sb_hamu_boundary_offer_var',rt.sponsor['vars'])
        rt.country['overlord']=rt.countries['c:GBR']
        rt.run('sb_hamu_boundary_monthly',nrp)
        self.assertIn('sb_hamu_boundary_offer_var',rt.sponsor['vars'])
        rt.effect([('sb_hamu_answer_boundary','=',[('ACCEPT','=','yes')])],rt.sponsor)
        self.assertIs(rt.sponsor,nrp['overlord'])
        self.assertIs(rt.country,rt.provinces['x9E9742']['state']['owner'])
        self.assertIs(nrp,rt.provinces['xBE6FEE']['state']['owner'])
        self.assertNotIn('sb_nrp_union_wait_var',nrp['vars'])

    def test_changed_overlord_reissues_pending_demand(self):
        rt=LaterCourtRuntime();rt.fulfil();nrp=rt.countries['c:NRP']
        rt.country['overlord']=rt.countries['c:GBR'];rt.run('sb_hamu_boundary_monthly',nrp)
        new={'id':'NEW','alive':True,'vars':{}}
        nrp['overlord']=new;rt.run('sb_hamu_boundary_monthly',nrp)
        self.assertNotIn('sb_hamu_boundary_offer_var',rt.sponsor['vars'])
        self.assertIn('sb_hamu_boundary_offer_var',new['vars'])

    def test_refusal_configures_only_its_real_play_and_target(self):
        rt=LaterCourtRuntime();rt.fulfil();nrp=rt.countries['c:NRP']
        rt.country['overlord']=rt.countries['c:GBR'];rt.run('sb_hamu_boundary_monthly',nrp)
        rt.effect([('sb_hamu_answer_boundary','=',[('ACCEPT','=','no')])],rt.sponsor)
        self.assertIs(rt.sponsor,rt.play['target'])
        self.assertIs(rt.play,nrp['vars']['sb_hamu_boundary_play_scope'])
        self.assertEqual(1,len(rt.play['add_war_goal']))
        self.assertEqual(1,len(rt.play['remove_war_goal']))

    def test_incomplete_country_creation_callback_defers_without_losing_receipt(self):
        rt=LaterCourtRuntime();rt.accept();rt.accede();rt.defer_country_alive=True
        rt.run('sb_hamu_contract_monthly',rt.sponsor)
        self.assertIn('sb_hamu_setup_pending_var',rt.sponsor['vars'])
        self.assertIs(rt.country,rt.provinces['x9E9742']['state']['owner'])
        rt.countries['c:NRP']['alive']=True
        rt.run('sb_hamu_finalise_nrp',rt.sponsor)
        self.assertIn('sb_hamu_fulfilled_var',rt.sponsor['vars'])

    def test_existing_authoritative_border_receipt_is_accepted(self):
        rt=LaterCourtRuntime();rt.global_vars.pop('sb_swazi_boer_border_resolved_global_var')
        rt.countries['c:SWZ']['vars']={'sb_swazi_boer_pressure_resolved_var':1}
        rt.offer()
        self.assertIn('sb_swazi_boer_border_resolved_global_var',rt.global_vars)
        self.assertIn('sb_hamu_offer_open_var',rt.sponsor['vars'])

    def test_subject_released_while_popup_or_refusal_waits(self):
        for refused in (False,True):
            rt=LaterCourtRuntime();rt.fulfil();nrp=rt.countries['c:NRP']
            rt.country['overlord']=rt.countries['c:GBR'];rt.run('sb_hamu_boundary_monthly',nrp)
            if refused:
                rt.countries['c:GBR']['is_active_in_diplomatic_play']=True
                rt.effect([('sb_hamu_answer_boundary','=',[('ACCEPT','=','no')])],rt.sponsor)
            nrp.pop('overlord');rt.run('sb_hamu_boundary_monthly',nrp)
            self.assertNotIn('sb_hamu_boundary_offer_var',rt.sponsor['vars'])
            self.assertNotIn('sb_hamu_boundary_refused_var',nrp['vars'])
            self.assertNotIn('sb_hamu_boundary_open_var',nrp['vars'])

    def test_new_overlord_does_not_inherit_a_refusal(self):
        rt=LaterCourtRuntime();rt.fulfil();nrp=rt.countries['c:NRP']
        rt.country['overlord']=rt.countries['c:GBR'];rt.run('sb_hamu_boundary_monthly',nrp)
        rt.countries['c:GBR']['is_active_in_diplomatic_play']=True
        rt.effect([('sb_hamu_answer_boundary','=',[('ACCEPT','=','no')])],rt.sponsor)
        new={'id':'NEW','alive':True,'vars':{}};nrp['overlord']=new
        rt.countries['c:GBR']['is_active_in_diplomatic_play']=False
        rt.run('sb_hamu_boundary_monthly',nrp)
        self.assertNotIn('sb_hamu_boundary_refused_var',nrp['vars'])
        self.assertIn('sb_hamu_boundary_offer_var',new['vars'])
        self.assertFalse(hasattr(rt,'play'))


class DunnAndPrincesTests(unittest.TestCase):
    def admitted(self):
        rt=LaterCourtRuntime();rt.country['game_date']=18550101
        rt.country['ruler']['template']='ZUL_mpande_zulu'
        # Keep the two princes distinct from the incumbent in this fixture.
        rt.country['ruler']=rt.country['members'][0]
        rt.country['ruler']['template']='ZUL_mpande_zulu'
        rt.cetshwayo['template']='ZUL_cetshwayo_heir'
        rt.run('sb_court_prepare_dunn_offer')
        dunn=rt.country['vars']['sb_court_dunn_visitor_scope']
        rt.run('sb_court_accept_dunn_offer')
        return rt,dunn

    def test_admission_opposition_and_two_weeks_once(self):
        rt,dunn=self.admitted()
        self.assertIs(rt.cetshwayo,rt.house['vars']['sb_court_successor_pledge_scope'])
        self.assertIs(rt.mbuyazi,dunn['vars']['sb_court_successor_pledge_scope'])
        rt.effect([('sb_court_answer_dunn_delivery','=','yes')],rt.country)
        self.assertEqual(2,rt.country['vars']['sb_firearms_supply_weeks_var'])
        rt.effect([('sb_court_answer_dunn_delivery','=','yes')],rt.country)
        self.assertEqual(2,rt.country['vars']['sb_firearms_supply_weeks_var'])
        rt.run('sb_court_dunn_trade_monthly')
        self.assertEqual(1,rt.country['events'].count('sb_court_dunn.002'))
        dunn['vars'].pop('sb_court_dunn_delivery_year_var')
        rt.run('sb_court_dunn_trade_monthly')
        self.assertEqual(2,rt.country['events'].count('sb_court_dunn.002'))
        self.assertEqual({'sb_court_trader'} & dunn['traits'],{'sb_court_trader'})

    def test_delivery_caps_and_stops_after_completion(self):
        rt,dunn=self.admitted();rt.country['vars']['sb_firearms_supply_weeks_var']=259
        rt.effect([('sb_court_answer_dunn_delivery','=','yes')],rt.country)
        self.assertEqual(260,rt.country['vars']['sb_firearms_supply_weeks_var'])
        dunn['vars'].pop('sb_court_dunn_delivery_year_var')
        rt.country['vars']['sb_firearms_modernized_var']=1
        rt.run('sb_court_dunn_trade_monthly')
        self.assertEqual(1,rt.country['events'].count('sb_court_dunn.002'))

    def test_first_delivery_is_reserved_for_three_days_then_annual_delivery_is_immediate(self):
        rt,dunn=self.admitted()
        self.assertEqual(('sb_court_dunn.002',3),rt.country['event_schedule'][-1])
        self.assertNotIn('sb_firearms_supply_weeks_var',rt.country['vars'])
        rt.run('sb_court_dunn_trade_monthly')
        self.assertEqual(1,rt.country['events'].count('sb_court_dunn.002'))
        rt.run('sb_court_answer_dunn_delivery')
        self.assertEqual(2,rt.country['vars']['sb_firearms_supply_weeks_var'])
        dunn['vars'].pop('sb_court_dunn_delivery_year_var')
        rt.run('sb_court_dunn_trade_monthly')
        self.assertEqual(('sb_court_dunn.002',0),rt.country['event_schedule'][-1])

    def test_delayed_delivery_revalidates_trader_owner_and_unfinished_firearms(self):
        from tests.test_zulu_institutions_laws import statements
        from tools.check_override_inventory import find_object
        from tests.test_zulu_court_politics import ROOT
        event=statements(find_object((ROOT/'events/sb_court_dunn_events.txt').read_text(encoding='utf-8-sig'),'sb_court_dunn.002'))
        for invalid in ('dead','foreign','completed'):
            with self.subTest(invalid=invalid):
                rt,dunn=self.admitted()
                if invalid=='dead':dunn['alive']=False
                elif invalid=='foreign':dunn['owner']=rt.countries['c:NAL']
                else:rt.country['vars']['sb_firearms_modernized_var']=1
                self.assertFalse(rt.condition(field(event,'trigger'),rt.country))
                rt.run('sb_court_answer_dunn_delivery')
                self.assertNotIn('sb_firearms_supply_weeks_var',rt.country['vars'])

    def test_declined_dunn_no_longer_counts_as_zulu_house(self):
        rt=LaterCourtRuntime();rt.country['ruler']=rt.country['members'][0]
        rt.run('sb_court_prepare_dunn_offer')
        dunn=rt.country['vars']['sb_court_dunn_visitor_scope']
        rt.run('sb_court_decline_dunn_offer');rt.backing()
        self.assertNotIn('sb_court_registered_var',dunn['vars'])
        self.assertNotIn('sb_court_home_scope',dunn['vars'])
        self.assertNotIn('sb_court_representative_var',dunn['vars'])
        self.assertIs(rt.countries['c:NAL'],dunn['owner'])

    def test_stale_judgement_is_not_immunity_in_another_war(self):
        rt,dunn=self.admitted()
        rt.scopes['sb_court_dynastic_winner']=rt.country
        rt.country['sb_court_dynastic_roster']=[dunn]
        rt.country['vars'].update(sb_court_dynastic_candidate_scope=rt.cetshwayo,sb_court_dynastic_nominee_scope=rt.mbuyazi,sb_court_dynastic_rival_scope=rt.cetshwayo)
        rt.run('sb_court_reserve_dunn_judgement')
        self.assertIn('sb_court_dunn_judgement_var',dunn['vars'])
        rt.country['vars']['sb_court_dynastic_candidate_scope']=rt.hamu
        rt.run('sb_court_reserve_dunn_judgement')
        self.assertNotIn('sb_court_dunn_judgement_var',dunn['vars'])

    def test_mthonga_not_declared_during_delayed_mpande_retirement(self):
        rt=LaterCourtRuntime();m=rt.actor('SB_ZUL_mthonga',0,18,1)
        m['vars']['sb_court_deferred_dynast_var']=1
        rt.global_vars['sb_court_mthonga_created_var']=1
        rt.country['year']=1857
        rt.country['ruler']=rt.country['members'][0]
        rt.run('sb_court_later_princes_monthly')
        self.assertNotIn('sb_court_mthonga_declared_var',m['vars'])
        rt.country['ruler']=rt.cetshwayo
        rt.run('sb_court_later_princes_monthly')
        self.assertIn('sb_court_mthonga_declared_var',m['vars'])
        self.assertIn('sb_court_claimant_trait',m['traits'])
        self.assertNotIn('sb_court_successor_pledge_scope',rt.house['vars'])


if __name__=='__main__':unittest.main()
