"""Execute shipped court records, quotes and succession reservations; engine wars remain pending."""
from pathlib import Path
import unittest
from tests.test_zulu_court_politics import CourtRuntime, character, EFFECTS, VALUES, TRIGGERS
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import find_object

ROOT = Path(__file__).resolve().parents[1]


class ReworkRuntime(CourtRuntime):
    def ref(self, key, scope, prev=None):
        if key.count('.') == 2 and all(part.isdigit() for part in key.split('.')):
            year,month,day = map(int,key.split('.'))
            return year*10000+month*100+day
        return super().ref(key,scope,prev)

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, op, value = node
            if key == 'sb_institutions_recalculate':
                self.backing()
            elif key == 'sb_court_ensure_roster':
                # Character creation/registration is exercised by the existing roster tests.
                self.backing()
            elif key == 'exile_character_with_role_cleanup':
                scope['is_in_exile_pool'] = True
            elif key == 'remove_character_role':
                scope[value] = False
                if value == 'heir' and scope['owner'].get('heir') is scope:
                    scope['owner'].pop('heir')
            elif key == 'post_notification':
                scope.setdefault('notifications',[]).append(value)
            elif key == 'random_list':
                choices = []
                for weight, _, body in value:
                    fields = dict((k, v) for k, _, v in body)
                    if not self.condition(fields.get('trigger', []), scope, prev): continue
                    amount = float(weight)
                    if 'modifier' in fields: amount += self.calc(fields['modifier'], scope, prev)
                    choices.append((amount, [n for n in body if n[0] not in ('modifier', 'trigger')]))
                point = getattr(self, 'roll', 0) * sum(w for w, _ in choices)
                for weight, body in choices:
                    if point < weight:
                        self.effect(body, scope, prev)
                        break
                    point -= weight
            else:
                super().effect([node], scope, prev)


def court(q=50):
    king = character('Dingane', 1, 50, 1, 1)
    prince = character('Mpande', 0, 60, -1, 1)  # Preserve this fixture's 85 total with the +25 claimant card.
    prince['template'] = 'ZUL_mpande_zulu'
    prince['vars']['sb_court_claimant_scope'] = prince
    chief = character('chief', 10, q)
    chief['vars']['sb_court_successor_pledge_scope'] = prince
    rt = ReworkRuntime([king, prince, chief])
    rt.country.update(gold_reserves_limit=100000, gold_reserves=200000)
    rt.country['laws'] = {'law_type:law_monarchy', 'law_type:law_autocracy'}
    rt.scopes['actor'] = rt.country
    rt.backing()
    return rt, king, prince, chief


def quote_confrontation(rt, prince):
    # Match an actual registered claimant, then execute the shipped quotation.
    if prince['vars'].get('sb_court_endorsement_var') == -1:
        prince['vars'].setdefault('sb_court_claimant_scope', prince)
    rt.country['vars'].update(sb_court_action_actor_scope=prince,
        sb_court_offer_ruler_scope=rt.country['ruler'], sb_court_action_open_var=1)
    rt.effect(EFFECTS['sb_court_quote_confrontation'], rt.country)


class CourtReworkBehaviour(unittest.TestCase):
    def test_princes_own_prominence_and_distinct_share_denominators(self):
        rt,king,prince,chief=court()
        self.assertEqual(185,rt.country['vars']['sb_court_weight_var'])  # 50 + (60+25) + 50
        self.assertEqual(135,rt.country['vars']['sb_court_pledged_weight_var'])
        self.assertEqual(50,rt.country['vars']['sb_court_unpledged_weight_var'])
        self.assertEqual(135,prince['vars']['sb_court_coalition_weight_var'])
        self.assertEqual(100,prince['vars']['sb_court_pledged_share_var'])
        self.assertEqual([chief],prince['sb_court_supporters'])
        self.assertIn('sb_court_house_leader_var',prince['vars'])
        self.assertEqual(0,chief['vars']['sb_court_endorsement_var'])

    def test_head_death_preserves_house_but_does_not_bequeath_pledge(self):
        rt,king,prince,chief=court()
        successor=character('next-householder',10,40)
        successor['owner']=rt.country
        successor['vars']['sb_court_home_scope']=rt.country
        rt.country['members'].append(successor)
        rt.backing()
        self.assertEqual(80,chief['vars']['sb_court_represented_weight_var'])  # 50+(40-10)
        self.assertEqual([successor],chief['sb_court_house_members'])
        self.assertEqual(165,prince['vars']['sb_court_coalition_weight_var'])
        chief['alive']=False
        rt.backing()
        self.assertEqual(175,rt.country['vars']['sb_court_weight_var'])
        self.assertEqual(85,prince['vars']['sb_court_coalition_weight_var'])
        self.assertNotIn('sb_court_junior_status',successor.get('modifiers',{}))
        self.assertNotIn('sb_court_successor_pledge_scope',successor['vars'])

    def test_major_threshold_uses_succession_pledged_prominence(self):
        rt,king,prince,chief=court(q=20)
        prince['prominence']=0  # +25 claimant bonus plus a pledged house of 20.
        king['prominence']=105
        other=character('other prince',0,80,-1,1)
        other.update(owner=rt.country,template='ZUL_gqugqu_claimant')
        other['vars'].update(sb_court_home_scope=rt.country,sb_court_claimant_scope=other)
        rt.country['members'].append(other)
        rt.backing()
        self.assertEqual(30,prince['vars']['sb_court_pledged_share_var'])
        self.assertTrue(rt.condition(TRIGGERS['sb_court_major_candidate'],prince))
        king['prominence']=1000  # No future pledge: cannot dilute either prince.
        rt.backing()
        self.assertEqual(30,prince['vars']['sb_court_pledged_share_var'])
        self.assertTrue(rt.condition(TRIGGERS['sb_court_major_candidate'],prince))
        other['prominence']+=1
        rt.backing()
        self.assertFalse(rt.condition(TRIGGERS['sb_court_major_candidate'],prince))

    def test_confrontation_deduplicates_own_house_and_present_future_backing(self):
        rt,_,prince,chief=court()
        prince['vars']['sb_court_claimant_scope']=prince
        chief['vars'].update(sb_court_endorsement_var=-1,sb_court_claimant_scope=prince)
        rt.backing()
        self.assertEqual(135,prince['vars']['sb_court_rival_weight_var'])
        chief['vars'].pop('sb_court_successor_pledge_scope')
        rt.backing()
        self.assertEqual(85,prince['vars']['sb_court_coalition_weight_var'])
        self.assertEqual(135,prince['vars']['sb_court_rival_weight_var'])
        self.assertEqual(100,rt.country['vars']['sb_court_unpledged_weight_var'])

    def test_renunciation_releases_promises_and_bonus_without_awarding_loyalty(self):
        rt,_,prince,chief=court()
        chief['vars']['sb_court_council_promise_scope']=prince
        prince['vars']['sb_court_claim_renounced_var']=1
        rt.backing()
        self.assertNotIn('sb_court_successor_pledge_scope',chief['vars'])
        self.assertNotIn('sb_court_council_promise_scope',chief['vars'])
        self.assertEqual(0,chief['vars']['sb_court_endorsement_var'])
        self.assertEqual(160,rt.country['vars']['sb_court_unpledged_weight_var'])
        self.assertEqual(0,rt.country['vars']['sb_court_pledged_weight_var'])
        self.assertEqual(0,prince['vars']['sb_court_pledged_share_var'])
        self.assertFalse(rt.condition(TRIGGERS['sb_court_major_candidate'],prince))
        self.assertNotIn('sb_court_claimant_trait',prince['traits'])
        self.assertNotIn('sb_court_junior_status',prince.get('modifiers',{}))

    def test_price_curve_clamps_and_uses_capacity_not_current_cash(self):
        for q, fraction in ((-5,.4),(10,.4),(25,.625),(50,1),(75,1.3),(100,1.6),(200,1.6)):
            with self.subTest(q=q):
                rt, _, _, chief = court(q)
                rt.country['vars']['sb_court_action_actor_scope'] = chief
                self.assertAlmostEqual(100000*fraction, rt.calc(VALUES['sb_court_patronage_price'],rt.country))
                rt.country['gold_reserves'] = 0
                self.assertAlmostEqual(100000*fraction, rt.calc(VALUES['sb_court_patronage_price'],rt.country))

    def test_purchase_guarantees_only_current_allegiance_and_charges_once(self):
        rt, _, prince, chief = court()
        rt.effect(EFFECTS['sb_court_open_pledge_quote'], chief)
        self.assertEqual(100000, rt.country['vars']['sb_court_offer_price_var'])
        rt.effect(EFFECTS['sb_court_confirm_pledge'], rt.country)
        self.assertEqual(100000, rt.country['gold_reserves'])
        self.assertEqual(1, chief['vars']['sb_court_endorsement_var'])
        self.assertEqual(0, chief['vars']['sb_court_alignment_var'])
        self.assertEqual(50, chief['prominence'])
        self.assertIs(prince, chief['vars']['sb_court_successor_pledge_scope'])
        rt.effect(EFFECTS['sb_court_confirm_pledge'], rt.country)
        self.assertEqual(100000, rt.country['gold_reserves'])
        self.assertEqual({}, rt.scopes['root']['vars'])

    def test_quote_is_frozen_despite_capacity_and_prominence_changes(self):
        rt, _, _, chief = court()
        rt.effect(EFFECTS['sb_court_open_pledge_quote'], chief)
        chief['prominence'] = 75
        rt.country['gold_reserves_limit'] *= 2
        rt.effect(EFFECTS['sb_court_confirm_pledge'], rt.country)
        self.assertEqual(100000, rt.country['gold_reserves'])
        self.assertEqual(1,chief['vars']['sb_court_endorsement_var'])
        self.assertEqual(['sb_court_politics.002'], rt.country['events'])
        rt.effect(EFFECTS['sb_court_confirm_pledge'], rt.country)
        self.assertEqual(100000, rt.country['gold_reserves'])

    def test_pledge_uses_native_treasury_debt_when_cash_is_insufficient(self):
        for cash in (150000, 100000, 10000, 0, -20000):
            with self.subTest(cash=cash):
                rt,king,prince,chief=court()
                rt.country['gold_reserves']=cash
                rt.effect(EFFECTS['sb_court_open_pledge_quote'],chief)
                quote=rt.country['vars']['sb_court_offer_price_var']
                rt.effect(EFFECTS['sb_court_confirm_pledge'],rt.country)
                self.assertEqual(cash-quote,rt.country['gold_reserves'])
                self.assertEqual(1,chief['vars']['sb_court_endorsement_var'])
                rt.effect(EFFECTS['sb_court_confirm_pledge'],rt.country)
                self.assertEqual(cash-quote,rt.country['gold_reserves'])
        event=(ROOT/'events/sb_court_politics_events.txt').read_text(encoding='utf-8-sig')
        self.assertNotIn('gold_reserves >=',find_object(event,'sb_court_politics.002'))

    def test_coercion_spends_its_distinct_cost_once_regardless_of_roll(self):
        for purge in ('yes','no'):
            for p in (0,24,25,49,50,100):
                for roll in (0,.99):
                    with self.subTest(p=p,purge=purge,roll=roll):
                        rt,king,prince,chief=court(q=10)
                        prince['prominence']=0;king['prominence']=100
                        rt.country['vars'].update(sb_court_action_actor_scope=prince,sb_court_offer_ruler_scope=king,sb_prerogative_var=p)
                        rt.roll=roll
                        attempt=[('sb_court_confrontation','=',[('PURGE','=',purge)])]
                        quote_confrontation(rt,prince)
                        rt.effect(attempt,rt.country)
                        cost=50 if purge=='yes' else 25
                        self.assertEqual(p-cost if p>=cost else p,rt.country['vars']['sb_prerogative_var'])
                        used=bool(prince.get('sb_court_purge_rulers',[])) if purge=='yes' else 'sb_court_renunciation_cooldown_var' in prince['vars']
                        self.assertEqual(p>=cost,used)
                        if p<cost:
                            self.assertTrue(prince['alive'])
                            self.assertFalse(prince.get('is_in_exile_pool',False))
                        # Restored purchasing power cannot purchase a second attempt this reign.
                        if p>=cost:
                            rt.country['vars'].update(sb_court_action_actor_scope=prince,sb_court_offer_ruler_scope=king,sb_prerogative_var=100)
                            quote_confrontation(rt,prince)
                            rt.effect(attempt,rt.country)
                            self.assertEqual(100,rt.country['vars']['sb_prerogative_var'])
        # Participant invalidation must not consume the cost either.
        rt,king,prince,chief=court(q=10)
        prince['alive']=False
        rt.country['vars'].update(sb_court_action_actor_scope=prince,sb_court_offer_ruler_scope=king,sb_prerogative_var=100)
        quote_confrontation(rt,prince)
        rt.effect([('sb_court_confrontation','=',[('PURGE','=','yes')])],rt.country)
        self.assertEqual(100,rt.country['vars']['sb_prerogative_var'])

    def test_dead_foreign_nonrepresentative_and_changed_ruler_targets_never_charge(self):
        for invalidation in ('dead','foreign','replaced','different-king','agitator','zero','negative','missing-price'):
            with self.subTest(invalidation=invalidation):
                rt, _, prince, chief = court()
                rt.effect(EFFECTS['sb_court_open_pledge_quote'], chief)
                if invalidation == 'dead': chief['alive'] = False
                if invalidation == 'foreign': chief['owner'] = {'id':'CAP'}
                if invalidation == 'replaced':
                    chief['vars']['sb_court_following_var'] = 1
                    rt.country['ruler']['prominence'] = 100
                if invalidation == 'different-king': rt.country['ruler'] = prince
                if invalidation == 'agitator': chief['agitator'] = True
                if invalidation == 'zero': chief['prominence'] = 0
                if invalidation == 'negative': chief['prominence'] = -10
                if invalidation == 'missing-price': rt.country['vars'].pop('sb_court_offer_price_var')
                before = rt.country['gold_reserves']
                rt.effect(EFFECTS['sb_court_confirm_pledge'], rt.country)
                self.assertEqual(before, rt.country['gold_reserves'])

    def test_capture_is_idempotent_and_preserves_third_candidate(self):
        rt, king, prince, chief = court()
        rival = character('Gqugqu',0,35,-1,1)
        rival.update(owner=rt.country,template='ZUL_gqugqu_claimant')
        rival['vars']['sb_court_home_scope'] = rt.country
        rt.country['members'].append(rival)
        rt.country['vars']['sb_court_recognized_heir_scope'] = prince
        rt.scopes['sb_court_outgoing'] = king
        rt.effect(EFFECTS['sb_court_capture_accession'], rt.country)
        self.assertEqual([prince,rival], rt.country['sb_court_accession_candidates'])
        self.assertIs(prince, rt.country['vars']['sb_court_accession_nominee_scope'])
        rt.scopes['sb_court_outgoing'] = rival
        rt.effect(EFFECTS['sb_court_capture_accession'], rt.country)
        self.assertIs(king, rt.country['vars']['sb_court_predecessor_scope'])

    def test_submission_and_capture_use_current_backing_and_ignore_popularity(self):
        rt, king, prince, _ = court()
        quote_confrontation(rt,prince)
        for popularity in (-100,0,100):
            king['popularity'] = popularity
            self.assertEqual(37, rt.calc(VALUES['sb_court_submission_chance'],rt.country))
            self.assertEqual(22.7, rt.calc(VALUES['sb_court_capture_chance'],rt.country))

    def test_open_retirement_choice_is_reserved_then_reconciles_only_actual_pledges(self):
        rt, king, prince, chief = court()
        king['template'] = 'ZUL_mpande_zulu'
        prince['template'] = 'ZUL_cetshwayo_heir'
        rt.country.update(game_date=18560630)
        rt.country['vars']['sb_court_recognized_heir_scope'] = prince
        rt.effect(EFFECTS['sb_court_reconcile_succession'],rt.country)
        self.assertEqual([],rt.country.get('events',[]))
        rt.country['game_date'] = 18560701
        rt.country['vars']['sb_court_dunn_offer_var']=1
        rt.effect(EFFECTS['sb_court_reconcile_succession'],rt.country)
        self.assertEqual([],rt.country.get('events',[]))
        self.assertNotIn('sb_court_accession_open_var',rt.country['vars'])
        rt.country['vars'].pop('sb_court_dunn_offer_var')
        rt.effect(EFFECTS['sb_court_reconcile_succession'],rt.country)
        rt.effect(EFFECTS['sb_court_reconcile_succession'],rt.country)
        self.assertEqual(['sb_court_succession.001'],rt.country['events'])
        rt.scopes['sb_court_nominee'] = prince
        rt.effect(EFFECTS['sb_court_answer_accession'],rt.country)
        self.assertIs(prince,rt.country['ruler'])
        self.assertTrue(king['alive'])
        self.assertTrue(king['retired'])
        self.assertIn('sb_court_claim_renounced_var',king['vars'])
        self.assertNotIn('sb_court_claimant_scope',king['vars'])
        self.assertNotIn('sb_court_claimant_trait',king.get('traits',set()))
        self.assertFalse(rt.condition(TRIGGERS['sb_court_living_dynast'],king))
        self.assertFalse(rt.condition(TRIGGERS['sb_court_dynastic_candidate'],king))
        self.assertEqual(1,chief['vars']['sb_court_endorsement_var'])
        self.assertEqual(0,king['vars']['sb_court_endorsement_var'])
        self.assertNotIn('sb_court_accession_open_var',rt.country['vars'])
        rt.effect(EFFECTS['sb_court_answer_accession'],rt.country)
        self.assertEqual(['sb_court_succession.001'],rt.country['events'])

    def test_changed_or_dead_nominee_does_not_install_through_stale_popup(self):
        rt,king,prince,chief = court()
        rt.scopes['sb_court_outgoing'] = king
        rt.effect(EFFECTS['sb_court_capture_accession'],rt.country)
        rt.country['vars']['sb_court_accession_popup_var'] = 1
        rt.scopes['sb_court_nominee'] = prince
        prince['alive'] = False
        rt.effect(EFFECTS['sb_court_answer_accession'],rt.country)
        self.assertIs(king,rt.country['ruler'])
        self.assertNotIn('sb_court_accession_open_var',rt.country['vars'])

    def test_accession_resets_prerogative_once_without_resetting_the_same_sovereign(self):
        for start in (-75, 60):
            rt,king,prince,_ = court()
            rt.country['vars'].update(sb_prerogative_var=start, sb_prerogative_last_change_var=4)
            rt.scopes['sb_court_successor'] = prince
            rt.effect(EFFECTS['sb_court_install_successor'],rt.country)
            self.assertIs(prince,rt.country['ruler'])
            self.assertEqual(0,rt.country['vars']['sb_prerogative_var'])
            self.assertEqual(0,rt.country['vars']['sb_prerogative_last_change_var'])
            rt.country['vars']['sb_prerogative_var'] = 12
            rt.effect(EFFECTS['sb_court_install_successor'],rt.country)
            self.assertEqual(12,rt.country['vars']['sb_prerogative_var'])
            self.assertNotIn('sb_prerogative_var',rt.scopes['root']['vars'])

    def test_institutional_exit_invalidates_open_accession(self):
        rt,king,prince,_ = court()
        rt.scopes['sb_court_outgoing'] = king
        rt.effect(EFFECTS['sb_court_capture_accession'],rt.country)
        rt.scopes['sb_court_nominee'] = prince
        rt.country['vars'].pop('sb_institutions_active_var')
        rt.effect(EFFECTS['sb_court_answer_accession'],rt.country)
        self.assertIs(king,rt.country['ruler'])
        self.assertNotIn('sb_court_accession_open_var',rt.country['vars'])

    def test_native_fallback_resets_only_a_new_royal_ruler_in_the_authored_country(self):
        source=(ROOT/'common/on_actions/sb_court_on_actions.txt').read_text(encoding='utf-8-sig')
        hook=dict((k,v) for k,_,v in statements(find_object(source,'sb_court_on_ruler_selected')))['effect']
        for authored in (False,True):
            rt,king,prince,_=court()
            rt.country['ruler']=prince
            rt.country['vars'].update(sb_court_incumbent_scope=king,sb_prerogative_var=60,sb_prerogative_last_change_var=4)
            if not authored:rt.country['id']='FRA'
            rt.effect(hook,prince)
            self.assertEqual(0 if authored else 60,rt.country['vars']['sb_prerogative_var'])
            rt.country['vars']['sb_prerogative_var']=12
            rt.effect(hook,prince)
            self.assertEqual(12,rt.country['vars']['sb_prerogative_var'])

    def test_contested_accession_reserves_live_choice_and_blocks_other_negotiations(self):
        rt,king,prince,chief = court()
        rival = character('Gqugqu',0,35,-1,1)
        rival.update(owner=rt.country,template='ZUL_gqugqu_claimant')
        rival['vars']['sb_court_home_scope'] = rt.country
        rt.country['members'].append(rival)
        rt.country['vars']['sb_court_recognized_heir_scope'] = rival
        rt.scopes['sb_court_outgoing'] = king
        rt.effect(EFFECTS['sb_court_capture_accession'],rt.country)
        self.assertNotIn('sb_court_accession_deferred_var',rt.country['vars'])
        self.assertIn('sb_court_accession_open_var',rt.country['vars'])
        self.assertFalse(rt.condition(TRIGGERS['sb_court_can_negotiate'],rt.country))
        self.assertIs(king,rt.country['ruler'])
        # Capture reserves the episode; the monthly reconciliation opens its choice.
        self.assertEqual([],rt.country.get('events',[]))

    def test_minor_regent_is_highest_pledged_adult_and_replaced_on_death(self):
        rt,king,minor,chief = court()
        minor.update(age=12,template='ZUL_uthumbu_claimed_son')
        rt.country['vars']['sb_court_recognized_heir_scope'] = minor
        adult = character('other-pledged-adult',12,70)
        adult.update(owner=rt.country)
        adult['vars'].update(sb_court_home_scope=rt.country,sb_court_successor_pledge_scope=minor)
        rt.country['members'].append(adult)
        rt.scopes['sb_court_successor'] = minor
        rt.effect(EFFECTS['sb_court_install_successor'],rt.country)
        self.assertIs(adult,rt.country['ruler'])
        self.assertIs(minor,rt.country['heir'])
        self.assertTrue(rt.condition(TRIGGERS['sb_court_dynastic_candidate'],minor))
        self.assertEqual(0,minor['vars']['sb_court_following_var'])
        self.assertEqual(0,rt.country['vars']['sb_prerogative_var'])
        rt.country['vars']['sb_prerogative_var'] = 35
        adult['alive'] = False
        rt.effect(EFFECTS['sb_court_reconcile_regency'],rt.country)
        self.assertIs(chief,rt.country['ruler'])
        self.assertIs(minor,rt.country['heir'])
        self.assertEqual(35,rt.country['vars']['sb_prerogative_var'])
        rt.country['vars']['sb_court_privileges_this_reign_var'] = 1
        minor['age'] = 18
        rt.effect(EFFECTS['sb_court_reconcile_regency'],rt.country)
        self.assertIs(minor,rt.country['ruler'])
        self.assertNotIn('modifier_regency',rt.country['modifiers'])
        self.assertTrue(chief['alive'])
        self.assertIn('sb_court_privileges_this_reign_var',rt.country['vars'])
        self.assertEqual(35,rt.country['vars']['sb_prerogative_var'])

    def test_council_promise_is_fulfilled_before_checking_for_repudiation(self):
        rt,king,prince,chief = court()
        chief['vars']['sb_court_council_promise_scope'] = prince
        rt.scopes['sb_court_outgoing'] = king
        rt.effect(EFFECTS['sb_court_capture_accession'],rt.country)
        # Native succession may already have selected the beneficiary while our popup is open.
        rt.country['ruler'] = prince
        rt.effect(EFFECTS['sb_court_reconcile_succession'],rt.country)
        self.assertIs(prince,chief['vars']['sb_court_council_promise_scope'])
        rt.scopes['sb_court_nominee'] = prince
        rt.effect(EFFECTS['sb_court_answer_accession'],rt.country)
        self.assertIn('law_type:law_sb_chiefly_council',rt.country['laws'])
        self.assertIn('law_type:law_monarchy',rt.country['laws'])
        rt.country['laws'].remove('law_type:law_sb_chiefly_council')
        rt.effect(EFFECTS['sb_court_reconcile_bargains'],rt.country)
        self.assertEqual(0,chief['vars']['sb_court_endorsement_var'])
        self.assertIn('sb_court_broken_undertaking',chief['modifiers'])
        self.assertNotIn('sb_court_council_promise_scope',chief['vars'])

    def test_failed_coercion_cannot_be_rerolled_in_the_same_reign(self):
        rt,king,prince,chief = court(q=10)
        prince['prominence']=0
        king['prominence']=100  # Keep this fixture below the major-rival boundary with the claimant card.
        rt.country['vars'].update(sb_court_action_actor_scope=prince,sb_court_offer_ruler_scope=king,sb_prerogative_var=100)
        rt.roll = .999
        quote_confrontation(rt,prince)
        rt.effect([('sb_court_confrontation','=',[('PURGE','=','yes')])],rt.country)
        self.assertTrue(prince['is_in_exile_pool'])
        self.assertTrue(prince['alive'])
        self.assertEqual([king],prince['sb_court_purge_rulers'])
        self.assertNotIn('sb_court_public_discredit',king.get('modifiers',{}))
        prince['is_in_exile_pool'] = False
        rt.country['vars'].update(sb_court_action_actor_scope=prince,sb_court_offer_ruler_scope=king,sb_prerogative_var=100)
        rt.roll = 0
        quote_confrontation(rt,prince)
        rt.effect([('sb_court_confrontation','=',[('PURGE','=','yes')])],rt.country)
        self.assertTrue(prince['alive'])

    def test_submission_removes_the_renounced_native_heir_but_preserves_the_person(self):
        rt,king,prince,chief = court(q=10)
        prince['prominence']=0
        king['prominence']=100  # Keep this fixture below the major-rival boundary with the claimant card.
        prince['heir'] = True
        rt.country['heir'] = prince
        rt.country['vars'].update(sb_court_action_actor_scope=prince,sb_court_offer_ruler_scope=king,sb_court_recognized_heir_scope=prince,sb_prerogative_var=100)
        rt.roll = 0
        quote_confrontation(rt,prince)
        rt.effect([('sb_court_confrontation','=',[('PURGE','=','no')])],rt.country)
        self.assertTrue(prince['alive'])
        self.assertIn('sb_court_claim_renounced_var',prince['vars'])
        self.assertNotIn('heir',rt.country)
        self.assertNotIn('sb_court_recognized_heir_scope',rt.country['vars'])
        self.assertNotIn('sb_court_successor_pledge_scope',chief['vars'])

    def test_heir_blocker_covers_living_children_and_exiles_but_not_exhausted_lines(self):
        rt, king, prince, chief = court()
        rt.effect(EFFECTS['sb_court_update_heir_blocker'],rt.country)
        self.assertIn('no_heirs',rt.country['vars'])
        self.assertIn('sb_court_owns_heir_blocker_var',rt.country['vars'])
        prince['is_in_exile_pool']=True
        rt.effect(EFFECTS['sb_court_update_heir_blocker'],rt.country)
        self.assertIn('no_heirs',rt.country['vars'])
        prince['alive']=False
        child=character('Cetshwayo',0,15,0,1,age=10)
        child.update(owner=rt.country,template='ZUL_cetshwayo_heir')
        child['vars']['sb_court_home_scope']=rt.country
        rt.country['members'].append(child)
        rt.effect(EFFECTS['sb_court_update_heir_blocker'],rt.country)
        self.assertIn('no_heirs',rt.country['vars'])
        child['alive']=False
        rt.effect(EFFECTS['sb_court_update_heir_blocker'],rt.country)
        self.assertNotIn('no_heirs',rt.country['vars'])
        self.assertNotIn('sb_court_owns_heir_blocker_var',rt.country['vars'])
        self.assertEqual({},rt.scopes['root']['vars'])

    def test_heir_blocker_releases_on_exit_preserves_external_policy_and_reenters(self):
        rt,_,_,_=court()
        rt.effect(EFFECTS['sb_court_update_heir_blocker'],rt.country)
        rt.country['vars'].pop('sb_institutions_active_var')
        rt.effect(EFFECTS['sb_court_update_heir_blocker'],rt.country)
        self.assertNotIn('no_heirs',rt.country['vars'])
        rt.country['vars']['sb_institutions_active_var']=1
        rt.effect(EFFECTS['sb_court_update_heir_blocker'],rt.country)
        self.assertIn('no_heirs',rt.country['vars'])
        rt.country['laws']={'law_type:law_sb_federated_chiefdoms'}
        rt.effect(EFFECTS['sb_court_update_heir_blocker'],rt.country)
        self.assertNotIn('no_heirs',rt.country['vars'])
        rt.country['vars']['no_heirs']=1  # Another route owns this block.
        rt.effect(EFFECTS['sb_court_update_heir_blocker'],rt.country)
        self.assertIn('no_heirs',rt.country['vars'])
        self.assertNotIn('sb_court_owns_heir_blocker_var',rt.country['vars'])

    def test_authored_heir_and_regency_survive_cmf_birth_callback(self):
        # Stress the ordering even if the engine delivers on_heir_born during
        # set_heir. CMF's real callback kills a newborn while no_heirs exists.
        from tests.test_zulu_court_politics import definitions
        authored=definitions('common/scripted_effects/sb_zulu_dynasty_succession_effects.txt')['sb_zulu_assign_new_heir_scope']
        class HeirRuntime(ReworkRuntime):
            def effect(self,nodes,scope,prev=None):
                for node in self.branches(nodes,scope,prev):
                    key,_,value=node
                    if key=='set_heir' and 'no_heirs' in scope['vars']:
                        self.ref(value,scope,prev)['alive']=False
                    if key!='set_interest_group':
                        super().effect([node],scope,prev)
        rt,king,prince,chief=court()
        sim=HeirRuntime([king,prince,chief])
        sim.country['laws']=rt.country['laws']
        sim.scopes['new_heir_scope']=prince
        sim.effect(EFFECTS['sb_court_update_heir_blocker'],sim.country)
        self.assertIn('no_heirs',sim.country['vars'])
        sim.effect(authored,sim.country)
        self.assertTrue(prince['alive'])
        self.assertIs(prince,sim.country['heir'])
        self.assertIn('no_heirs',sim.country['vars'])
        child=character('Cetshwayo',0,15,0,1,age=10)
        child.update(owner=sim.country,template='ZUL_cetshwayo_heir')
        child['vars']['sb_court_home_scope']=sim.country
        sim.country['members'].append(child)
        sim.country['vars']['sb_court_minor_sovereign_scope']=child
        chief['vars']['sb_court_successor_pledge_scope']=child
        sim.effect(EFFECTS['sb_court_choose_regent'],sim.country)
        self.assertIs(child,sim.country['heir'])
        self.assertTrue(child['alive'])
        self.assertIn('no_heirs',sim.country['vars'])
        # An ordinary generated appointment is still suppressed.
        sim.scopes['generated_child']=character('generated',0,1,age=0)
        sim.effect([('set_heir','=','scope:generated_child')],sim.country)
        self.assertFalse(sim.scopes['generated_child']['alive'])

    def test_purge_reports_actual_capture_or_escape_and_does_not_repeat(self):
        for roll,notification,alive in ((0,'sb_court_rival_killed',False),(.99,'sb_court_rival_fled',True)):
            rt,king,prince,chief=court(q=10)
            prince['prominence']=0
            king['prominence']=100  # Keep this fixture below the major-rival boundary with the claimant card.
            rt.country['vars'].update(sb_court_action_actor_scope=prince,sb_court_offer_ruler_scope=king,sb_prerogative_var=100)
            rt.roll=roll
            quote_confrontation(rt,prince)
            rt.effect([('sb_court_confrontation','=',[('PURGE','=','yes')])],rt.country)
            self.assertEqual(alive,prince['alive'])
            self.assertEqual([notification],rt.country['notifications'])
            self.assertIs(prince,rt.scopes['sb_court_actor'])
            if alive:
                self.assertTrue(prince['is_in_exile_pool'])
                self.assertNotIn('sb_court_public_discredit',king.get('modifiers',{}))
            rt.country['vars'].update(sb_court_action_actor_scope=prince,sb_court_offer_ruler_scope=king,sb_prerogative_var=100)
            quote_confrontation(rt,prince)
            rt.effect([('sb_court_confrontation','=',[('PURGE','=','yes')])],rt.country)
            self.assertEqual([notification],rt.country['notifications'])

    def test_recognise_preview_never_reads_execution_only_counter(self):
        from tests.test_zulu_court_politics import ACTIONS
        class PreviewRuntime(ReworkRuntime):
            def effect(self,nodes,scope,prev=None):
                for node in self.branches(nodes,scope,prev):
                    key,_,value=node
                    if key=='change_variable':
                        name=dict((k,v) for k,_,v in value)['name']
                        if name not in scope['vars']:
                            raise AssertionError('preview reads missing counter: '+name)
                    elif key not in ('set_variable','remove_variable','trigger_event'):
                        super().effect([node],scope,prev)
            def condition(self,nodes,scope,prev=None):
                for key,op,value in nodes:
                    if key.startswith('var:') and op!='?=' and self.ref(key,scope,prev) is None:
                        raise AssertionError('preview reads missing variable: '+key)
                return super().condition(nodes,scope,prev)
        rt,king,prince,chief=court()
        preview=PreviewRuntime([king,prince,chief])
        before=dict(preview.country['vars'])
        preview.effect(ACTIONS['sb_court_prepare_succession_choice'],preview.country)
        self.assertEqual(before,preview.country['vars'])
        self.assertNotIn('events',preview.country)


class CourtReworkContracts(unittest.TestCase):
    def text(self,rel): return (ROOT/rel).read_text(encoding='utf-8-sig')

    def test_native_war_is_live_with_profile_guard_and_never_foreign_play(self):
        effects=self.text('common/scripted_effects/sb_court_dynastic_effects.txt')
        prototype=find_object(effects,'sb_court_reserve_dynastic_crisis')
        self.assertIn('sb_court_dynastic_enabled = yes',prototype)
        self.assertNotIn('create_diplomatic_play',effects)
        victory=find_object(effects,'sb_court_resolve_dynastic_win')
        self.assertNotIn('sb_zululand_resolve_',victory)
        self.assertNotIn('annex =',victory)
        self.assertIn('var:sb_court_dynastic_opponent_scope ?= scope:target',effects)
        self.assertIn('variable = sb_court_dynastic_rival_members',victory)
        self.assertIn('variable = sb_court_dynastic_incumbent_members',victory)
        self.assertIn('sb_court_restore_dynastic_roster = yes',victory)
        writers=[]
        for folder in ('common','events'):
            for file in (ROOT/folder).rglob('*.txt'):
                if 'set_variable = sb_court_dynasty_test_var' in file.read_text(encoding='utf-8-sig'):writers.append(file.name)
        self.assertEqual([],writers)
        enabled=find_object(self.text('common/scripted_triggers/sb_court_dynastic_triggers.txt'),'sb_court_dynastic_enabled')
        self.assertIn('sb_institutions_profile_country = yes',enabled)
        debug_event=find_object(self.text('events/sb_court_succession_events.txt'),'sb_court_succession.990')
        self.assertIn('orphan = yes',debug_event)

    def test_retirement_regency_and_concurrency_contracts(self):
        s=self.text('common/scripted_effects/sb_court_succession_effects.txt')
        self.assertIn('game_date >= 1856.7.1',s)
        self.assertIn('resign_and_retire = yes',s)
        self.assertNotIn('set_character_immortal',s)
        self.assertNotIn('is_at_war = no',s)
        self.assertIn('is_adult = yes',s)
        self.assertIn('is_adult = no',s)
        self.assertIn('var:sb_court_successor_pledge_scope ?= scope:sb_court_country.var:sb_court_minor_sovereign_scope',s)
        self.assertIn('order_by = prominence',s)
        self.assertIn('sb_court_accession_popup_var',s)

    def test_court_section_is_bounded_scrollable_and_keeps_viewed_country(self):
        gui=self.text('gui/sb_prerogative_progress_bars.gui') + self.text('gui/sb_court_house_roster.gui')
        self.assertEqual(4,gui.count('section_header_button = {'))
        self.assertEqual(4,gui.count('blockoverride "onclick_showmore"'))
        self.assertEqual(4,gui.count('blockoverride "onclick_showless"'))
        self.assertNotIn('window = {',gui)
        from tools.check_override_inventory import extract_braced_object
        import re
        panels=[extract_braced_object(gui,m.start())
                for m in re.finditer(r'\bscrollbox\s*=\s*\{',gui)]
        self.assertEqual(3,len(panels))
        for name,panel in zip(('current','succession','houses'),panels):
            self.assertIn(f'name = sb_court_{name}_panel',panel)
            if name != 'houses':
                self.assertIn(f"GetVariableSystem.Toggle('sb_court_{name}_open')",gui)
            else:
                self.assertIn("Concatenate('sb_court_houses_', Country.GetIDString)",panel)
            self.assertIn('size = { 504 560 }',panel)
            self.assertIn('blockoverride "scrollbox_content"',panel)
        self.assertNotIn('GetVariableSystem.Set',gui)  # All three start closed.
        self.assertNotIn('sb_court_window_open',gui)
        self.assertIn("GetList('sb_court_current_supporters')",panels[0])
        self.assertNotIn("GetList('sb_court_supporters')",panels[0])
        self.assertIn("GetList('sb_court_supporters')",panels[1])
        self.assertNotIn("GetList('sb_court_current_supporters')",panels[1])
        self.assertIn("Character.GetCustom('sb_court_roster_endorsement')",panels[0])
        for summary,panel in zip(('sb_court_challenge_summary','sb_court_succession_summary'),panels):
            self.assertIn(f"JournalEntry.GetCountry.GetCustom('{summary}')",gui)
            self.assertNotIn(summary,panel)  # Visible even with its panel closed.
        # A popup layer never takes a child out of its flow. Constrain every
        # explicitly sized child and use the native scrollbar-bearing template.
        for width in re.findall(r'size\s*=\s*\{\s*(\d+)\s+\d+\s*\}',gui):
            self.assertLessEqual(int(width),504)
        native=(Path.home()/'Library/Application Support/Steam/steamapps/common/Victoria 3/game/gui/frontend/shared/lists.gui').read_text(encoding='utf-8-sig')
        scrollbox=native[native.index('type scrollbox = scrollarea'):]
        self.assertIn('scrollbar_vertical = {',scrollbox)
        self.assertIn('scrollbarpolicy_horizontal = always_off',scrollbox)
        self.assertNotIn('GetPlayer',gui)
        self.assertIn('JournalEntry.GetCountry.MakeScope',gui)
        interactions=self.text('common/character_interactions/sb_court_interactions.txt')
        self.assertNotIn('REPLACE:',interactions)
        self.assertNotIn('authority',interactions)
        self.assertIn('scope:actor',interactions)

    def test_old_event_callers_retired_and_annual_reservation_precedes_selection(self):
        s=self.text('common/scripted_effects/sb_court_episodes_effects.txt')
        self.assertLess(s.index('set_variable = sb_court_episode_open_var'),s.index('trigger_event ='))
        self.assertNotIn('sb_zulu_court.200',self.text('common/scripted_effects/sb_zulu_dynasty_succession_effects.txt'))
        events=self.text('events/sb_zulu_court_events.txt')
        # Allegiance outcomes retain the pledge veto and three approved refusal penalties.
        veto=next(body for key,_,body in statements(find_object(events,'sb_zulu_court.210'))
                  if key=='option' and ('name','=','sb_zulu_court.210.z') in body)
        self.assertIn('sb_change_prerogative',repr(veto))
        self.assertEqual(4,events.count('sb_change_prerogative'))
        self.assertIn('has_variable = sb_court_firearms_reward_var',self.text('common/scripted_triggers/sb_court_episode_triggers.txt'))
        self.assertNotIn('sb_court_annual_episode',s)


if __name__ == '__main__': unittest.main()
