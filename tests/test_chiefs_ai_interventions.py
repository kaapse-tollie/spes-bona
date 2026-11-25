"""Execute the Thirteen Chiefs policy, including its native-scope and event handoffs."""
from copy import deepcopy
import unittest
from unittest.mock import patch

from tests.test_chiefdoms_houses_and_prices import BribeRuntime, character
from tests.test_chiefdoms_playtest_november import EVENTS, VALUES, calculate, field
from tests.test_chiefdoms_refinement import Contest, E, defs, entity

DYNAMIC = 'sb_frontier_ai_behavior_dynamic_historical'
STRICT = 'sb_frontier_ai_behavior_strict_historical'
OFF = 'sb_frontier_ai_behavior_off'
POLICE = 'sb_zululand_policing_active_var'
PATRONAGE = 'sb_zululand_chief_patronage_active_var'
SPONSOR = 'sb_zululand_usuthu_sponsorship_active_var'
VOLUNTEERS = 'sb_zululand_boer_volunteers_active_var'
COMMITMENT = 'sb_zululand_boer_commitment_var'
COST = 'sb_zululand_bribe_cost_var'
TARGET = 'sb_zululand_bribe_target_scope'


def weights(runtime, event, country):
    result = []
    for key, _, option in EVENTS[event]:
        if key != 'option':
            continue
        chance = field(option, 'ai_chance')
        weight = float(field(chance, 'base'))
        for name, _, modifier in chance:
            if name == 'modifier' and runtime.condition(field(modifier, 'trigger'), country):
                for operation, _, amount in modifier:
                    if operation == 'add':
                        weight += float(amount)
                    elif operation == 'factor':
                        weight *= float(amount)
        result.append(weight)
    return result


class PolicyContest(Contest):
    def __init__(self, mode=DYNAMIC):
        super().__init__()
        self.mode = mode
        for country in (self.nal, self.trn):
            country.update(is_ai=True, principal=0, credit=100000, in_default=False,
                           gold_reserves=0, net_total_income=0, authority=100)
        self.trn['pops'] = [entity('Boer Servicemen', culture='cu:boer', pop_type='soldiers', total_size=500)]
        self.zul['capital'] = entity('Zulu capital', state_region='s:STATE_ZULULAND')
        self.zul['states'] = [self.zul['capital']]
        self.royals = self.royal(0)
        self.chiefs = entity('amaKhosi', owner=self.zul, movement_type='movement_sb_zulu_chiefly')
        self.zul['movements'].append(self.chiefs)
        self.container['vars'][COMMITMENT] = 0
        self.scopes.update(journal_entry=self.journal, root=self.britain)

    def ref(self, key, ctx, prev=None):
        if key in VALUES:
            return calculate(self, key, ctx)
        return super().ref(key, ctx, prev)

    def monthly(self):
        # Exercise the shipped controller, including commitment, resolution and bids.
        # These independent UI/incident deliveries have their own native event fixtures.
        self.scopes = {'journal_entry': self.journal, 'root': self.britain}
        with patch.dict(E, {name: [] for name in (
                'sb_zululand_refresh_chiefdoms_participants', 'sb_zululand_schedule_boer_appeal',
                'sb_zululand_schedule_next_incident', 'sb_zululand_apply_chiefdoms_progress_to_all')}):
            self.run('sb_zululand_chiefdoms_monthly_housekeeping', self.nal)

    def weekly(self):
        self.journal['journal_entry_age'] += 7
        self.run('sb_chiefs_weekly_update', self.britain)


class PolicyTests(unittest.TestCase):
    def test_natal_fiscal_states_and_policing_boundaries(self):
        for net, cash, debt, active, expected in [
            (1, 10, 0, False, True), (1, 0, 0, False, False),
            (-1, 10, 0, True, True), (-1, 10, 0, False, False),
            (-1, 0, 0, True, False), (-1, 10, 1, True, False),
            (1, 0, 1, True, True), (1, 0, 1, False, False), (0, 0, 1, True, True),
        ]:
            with self.subTest(net=net, cash=cash, debt=debt, active=active):
                rt = PolicyContest()
                rt.nal.update(net_total_income=net, gold_reserves=cash, principal=debt)
                if active:
                    rt.run('sb_zululand_start_chief_patronage', rt.nal)
                rt.monthly()
                self.assertEqual(expected, PATRONAGE in rt.nal['vars'])
        rt = PolicyContest()
        for activism, authority, expected in [
            (.699, 100, False), (.70, 99, False), (.70, 100, True),
            (.401, 0, True), (.40, 0, False), (.78, 100, True), (.78, -1, False),
        ]:
            rt.royals['political_movement_radicalism'] = activism
            rt.nal['authority'] = authority
            rt.monthly()
            self.assertEqual(expected, POLICE in rt.nal['vars'])

    def test_strict_stands_down_inherited_actions_and_off_keeps_legacy_policy(self):
        rt = PolicyContest(STRICT)
        rt.nal.update(net_total_income=10000, gold_reserves=100000)
        rt.royals['political_movement_radicalism'] = .90
        rt.run('sb_zululand_start_policing', rt.nal)
        rt.run('sb_zululand_start_chief_patronage', rt.nal)
        rt.weekly()
        rt.monthly()
        self.assertFalse({POLICE, PATRONAGE}.intersection(rt.nal['vars']))
        self.assertFalse(rt.condition([('sb_chiefs_ai_can_seek_bribe', '=', 'yes')], rt.nal))
        rt = PolicyContest(OFF)
        rt.trn.update(net_total_income=-100, net_fixed_income=0, gold_reserves=1)
        rt.monthly()
        self.assertIn(SPONSOR, rt.trn['vars'])
        self.assertNotIn(VOLUNTEERS, rt.trn['vars'])

    def test_trn_sponsorship_transitions_and_weekly_stand_down(self):
        for initial in (False, True):
            for net, debt, expected_off, expected_on in [
                (1, 0, True, True), (0, 0, False, True), (-1, 0, False, True),
                (-1, 9999, False, True), (-1, 10000, False, False), (0, 10000, False, True),
                (250, 40000, False, True), (251, 40000, True, True),
                (251, 49999, True, True), (251, 50000, False, True),
            ]:
                with self.subTest(active=initial, net=net, debt=debt):
                    rt = PolicyContest()
                    rt.trn.update(net_total_income=net, principal=debt)
                    if initial:
                        rt.run('sb_zululand_start_usuthu_sponsorship', rt.trn)
                    rt.monthly()
                    self.assertEqual(expected_on if initial else expected_off, SPONSOR in rt.trn['vars'])
        rt = PolicyContest()
        rt.trn.update(net_total_income=300, principal=40000)
        rt.monthly()
        rt.trn['net_total_income'] = -1
        rt.weekly()
        self.assertNotIn(SPONSOR, rt.trn['vars'])
        self.assertIn(VOLUNTEERS, rt.trn['vars'])

    def test_new_subsidies_get_first_claim_on_income(self):
        for tag, cost in [('NAL', 500), ('TRN', 250)]:
            for net in (cost, cost + 1):
                rt = PolicyContest()
                payer = rt.nal if tag == 'NAL' else rt.trn
                payer.update(net_total_income=net, gold_reserves=10000)
                rt.royals['political_movement_radicalism'] = .60
                with patch.dict(E, {'sb_zululand_offer_chief_bribe': [('set_variable', '=', 'offered')]}):
                    rt.monthly()
                    self.assertEqual(net > cost, 'offered' in payer['vars'])
                    payer['vars'].pop('offered', None)
                    payer['net_total_income'] = 1  # Next reported balance includes the subsidy.
                    rt.monthly()
                    self.assertIn('offered', payer['vars'])

    def test_commando_commitment_and_appeal(self):
        for funding, months in [(0, 34), (1000, 20)]:
            rt = PolicyContest(STRICT)
            rt.trn['net_total_income'] = funding
            for _ in range(months - 1):
                rt.monthly()
            self.assertLess(rt.container['vars'][COMMITMENT], 100)
            rt.monthly()
            self.assertEqual(100, rt.container['vars'][COMMITMENT])
            self.assertIn('sb_zululand_boer_committed_var', rt.container['vars'])
        for mode in (DYNAMIC, STRICT, OFF):
            rt = PolicyContest(mode)
            rt.trn.update(in_default=True, principal=90000, net_total_income=-3000)
            pop = rt.trn['pops'][0]
            tswana = entity('Tswana Servicemen', culture='cu:tswana', pop_type='soldiers', total_size=8873)
            rt.trn['pops'].append(tswana)
            event = EVENTS['sb_zululand_settlement.115']
            for size in (499, 500):
                pop['total_size'] = size
                available = rt.condition(field(event, 'trigger'), rt.trn)
                self.assertEqual(size == 500, available)
                with patch.dict(E, {'sb_zululand_apply_chiefdoms_progress_to_all': [], 'sb_zululand_finish_situation_event': []}):
                    if available:
                        rt.effect(field(event, 'immediate'), rt.trn)
                        self.assertEqual(500, rt.zul['capital']['arrivals'])
                        self.assertFalse(rt.condition(field(event, 'trigger'), rt.trn))
                        rt.effect(field(field(event, 'option'), 'hidden_effect'), rt.trn)
                        rt.run('sb_zululand_accept_boer_appeal', rt.trn)
                self.assertEqual(20 if available else 0, rt.container['vars'][COMMITMENT])
                self.assertEqual(500 if available else 0, rt.zul['capital'].get('arrivals', 0))
                self.assertEqual(0 if available else 499, pop['total_size'])
                self.assertEqual(8873, tswana['total_size'])

    def test_delayed_appeal_waits_for_boers_and_an_old_held_notice_delivers_once(self):
        pending = 'sb_zululand_boer_appeal_pending_var'
        lease = 'sb_zululand_incident_pending_var'
        scheduler = field(E['sb_zululand_schedule_boer_appeal'], 'if')
        choices = field(field(scheduler, 'if'), 'random_list')
        for mode, ai, eligible_weights in ((DYNAMIC, True, [50]), (STRICT, True, [50]),
                                           (OFF, False, [50]), (OFF, True, [50, 50])):
            rt = PolicyContest(mode)
            rt.trn['is_ai'] = ai
            rt.nal['vars'][pending] = 1
            pop = rt.trn['pops'][0]
            pop['total_size'] = 499
            rt.run('sb_zululand_schedule_boer_appeal', rt.nal)
            self.assertIn(pending, rt.nal['vars'])
            self.assertNotIn(lease, rt.nal['vars'])
            available = [(int(weight), body) for weight, _, body in choices if rt.condition(
                next((value for key, _, value in body if key == 'trigger'), []), rt.nal)]
            self.assertEqual(eligible_weights, [weight for weight, _ in available])
            notice = field(field(available[0][1], 'c:TRN'), 'trigger_event')
            self.assertEqual(('sb_zululand_settlement.115', '1', 'yes'),
                             tuple(field(notice, key) for key in ('id', 'days', 'popup')))
            pop['total_size'] = 500
            rt.run('sb_zululand_schedule_boer_appeal', rt.nal)
            self.assertIn(lease, rt.nal['vars'])
            # An offer held across an upgrade already ran its former immediate block.
            option = field(EVENTS['sb_zululand_settlement.115'], 'option')
            with patch.dict(E, {'sb_zululand_apply_chiefdoms_progress_to_all': [],
                                'sb_zululand_finish_situation_event': []}):
                for _ in range(2):
                    rt.effect(field(option, 'hidden_effect'), rt.trn)
            self.assertEqual((500, 20), (rt.zul['capital']['arrivals'], rt.container['vars'][COMMITMENT]))
            self.assertNotIn(pending, rt.nal['vars'])

    def test_split_moves_effects_and_withdrawal_releases_them(self):
        rt = PolicyContest()
        rt.royals['political_movement_radicalism'] = .80
        rt.nal.update(net_total_income=1000, gold_reserves=1000)
        rt.trn['net_total_income'] = 1000
        rt.monthly()
        rebel = entity('REB', alive=True, capital=entity('rebel capital'))
        royal = entity('rebel uSuthu', owner=rebel, movement_type='movement_sb_zulu_royal', political_movement_radicalism=.80)
        chiefly = entity('rebel chiefs', owner=rebel, movement_type='movement_sb_zulu_chiefly')
        rebel['movements'] = [royal, chiefly]
        rt.container['vars']['sb_chiefs_rebels_scope'] = rebel
        royal_mods = {'sb_usuthu_sponsorship', 'sb_usuthu_policing', 'sb_usuthu_volunteers'}
        for side in (1, 2):
            rebel['vars']['sb_court_war_alignment_var'] = side
            rt.weekly()
            self.assertEqual(royal_mods, (royal if side == 1 else rt.royals)['modifiers'])
            self.assertFalse((rt.royals if side == 1 else royal).get('modifiers'))
            self.assertIn('sb_zululand_chiefly_patronage', (chiefly if side == 2 else rt.chiefs)['modifiers'])
        rt.trn['states'].clear()
        rt.weekly()
        self.assertFalse({SPONSOR, VOLUNTEERS}.intersection(rt.trn['vars']))
        self.assertEqual({'sb_usuthu_policing'}, rt.royals['modifiers'])

    def test_transferred_state_releases_or_takes_on_volunteer_mortality(self):
        rt = PolicyContest()
        rt.monthly()
        state = rt.trn['states'][0]
        handler = defs('common/on_actions/sb_regional_on_action_handlers.txt')['sb_on_chiefs_volunteer_state_owner_change']
        for owner, expected in ((rt.nal, False), (rt.trn, True)):
            state['owner'] = owner
            self.assertTrue(rt.condition(field(handler, 'trigger'), state))
            rt.effect(field(handler, 'effect'), state)
            self.assertEqual(expected, 'sb_zululand_boer_volunteer_mortality' in state['modifiers'])

    def test_human_keeps_orders_until_the_contest_closes(self):
        rt = PolicyContest(STRICT)
        rt.nal.update(is_ai=False, net_total_income=-1000, principal=80000)
        rt.trn.update(is_ai=False, net_total_income=4000)
        rt.run('sb_zululand_start_chief_patronage', rt.nal)
        rt.run('sb_zululand_start_policing', rt.nal)
        rt.monthly()
        rt.weekly()
        self.assertTrue({POLICE, PATRONAGE}.issubset(rt.nal['vars']))
        self.assertFalse({VOLUNTEERS, SPONSOR}.intersection(rt.trn['vars']))
        rt.run('sb_zululand_stop_contest_interventions', rt.britain)
        self.assertFalse(rt.nal['modifiers'])
        self.assertFalse(rt.royals['modifiers'])
        self.assertFalse(rt.chiefs['modifiers'])

    def test_appeal_sends_families_and_mobilisation_to_the_royal_faction(self):
        rt = PolicyContest()
        zululand = entity('royalists in Zululand', state_region='s:STATE_ZULULAND')
        rebels = entity('royal rebels', alive=True, capital=entity('foreign capital'), states=[zululand])
        rebels['vars']['sb_court_war_alignment_var'] = 1
        rt.container['vars']['sb_chiefs_rebels_scope'] = rebels
        royalists = entity('rebel uSuthu', movement_type='movement_sb_zulu_royal', owner=rebels)
        rebels['movements'] = [royalists]
        with patch.dict(E, {'sb_zululand_apply_chiefdoms_progress_to_all': [], 'sb_zululand_finish_situation_event': []}):
            rt.run('sb_zululand_accept_boer_appeal', rt.trn)
        self.assertEqual(500, zululand['arrivals'])
        self.assertNotIn('arrivals', rebels['capital'])
        self.assertNotIn('arrivals', rt.zul['capital'])
        self.assertIn('sb_zululand_incident_mobilization', royalists['modifiers'])


class BribeTests(unittest.TestCase):
    def setUp(self):
        self.king = character('king', 15, 40, 1, 1)
        self.top = character('senior', 2, 100)
        self.next = character('junior', 3, 50)
        self.rt = BribeRuntime([self.king, self.top, self.next])
        self.rt.mode = DYNAMIC
        self.rt.interventions = True
        self.rt.global_vars['sb_zululand_live_zul_scope'] = self.rt.country
        self.rt.country['movements'] = [dict(type='movement_sb_zulu_royal', political_movement_radicalism=0)]
        self.rt.backing()

    def payer(self, tag, **budget):
        country = dict(id=tag, vars={}, is_ai=True, principal=0, credit=100000,
                       net_total_income=1, gold_reserves=0, gold_reserves_limit=4000)
        country.update(budget)
        return country

    def offer(self, payer):
        self.rt.effect([('sb_zululand_offer_chief_bribe', '=', 'yes')], payer)
        return payer['vars'].get(TARGET)

    def pay(self, payer):
        option = field(EVENTS['sb_zululand_settlement.116'], 'option')
        self.rt.effect(field(option, 'hidden_effect'), payer)

    def test_transvaal_buys_best_affordable_at_zero_activism(self):
        for mode in (DYNAMIC, STRICT):
            self.rt.mode = mode
            payer = self.payer('TRN', principal=8000)
            self.assertIs(self.next, self.offer(payer))
            self.assertEqual(2000, payer['vars'][COST])
            self.assertEqual([100, 0], weights(self.rt, 'sb_zululand_settlement.116', payer))
            payer = self.payer('TRN', principal=8001)
            self.assertIsNone(self.offer(payer))
            self.assertNotIn('events', payer)
            self.assertIsNone(self.offer(self.payer('TRN', net_total_income=0)))
            self.assertIsNone(self.offer(self.payer('TRN', credit=0, gold_reserves=1999)))
            self.assertIs(self.next, self.offer(self.payer('TRN', credit=0, gold_reserves=2000)))

    def test_natal_bribes_only_above_half_in_cash_and_stays_with_top_house(self):
        payer = self.payer('NAL', gold_reserves=3200)
        self.rt.country['movements'][0]['political_movement_radicalism'] = .50
        self.assertIsNone(self.offer(payer))
        self.rt.country['movements'][0]['political_movement_radicalism'] = .501
        self.assertIsNone(self.offer(self.payer('NAL', gold_reserves=3199)))
        self.assertIsNone(self.offer(self.payer('NAL', gold_reserves=9999, principal=1)))
        self.assertIs(self.top, self.offer(payer))
        self.assertIsNone(self.offer(self.payer('NAL', net_total_income=-1, gold_reserves=9999)))
        self.rt.mode = STRICT
        self.assertEqual([0, 100], weights(self.rt, 'sb_zululand_settlement.116', payer))
        self.pay(payer)
        self.assertEqual(3200, payer['gold_reserves'])

    def test_competing_offers_and_reload_recheck_frozen_quote(self):
        self.rt.country['movements'][0]['political_movement_radicalism'] = .8
        nal, trn = self.payer('NAL', gold_reserves=3200), self.payer('TRN', gold_reserves=5000)
        self.assertIs(self.top, self.offer(nal))
        self.assertIs(self.top, self.offer(trn))
        self.assertIs(self.top, self.offer(trn))  # Existing offer is still held.
        self.assertEqual(1, len(trn['events']))
        self.rt, nal, trn = deepcopy((self.rt, nal, trn))
        self.rt.scopes.clear()
        trn['gold_reserves_limit'] = 1
        head = trn['vars'][TARGET]
        head['prominence'] = 10
        self.pay(trn)
        self.pay(nal)
        self.pay(trn)
        self.assertEqual(1, head['vars']['sb_court_alignment_var'])
        self.assertEqual((3200, 1800), (nal['gold_reserves'], trn['gold_reserves']))
        self.assertNotIn(TARGET, nal['vars'])

    def test_pending_offer_rechecks_live_budget_and_participation(self):
        for field_name, new_value in [('principal', 8001), ('eligible', False), ('in_default', True), ('net_total_income', 0)]:
            payer = self.payer('TRN', principal=8000)
            self.assertIs(self.next, self.offer(payer))
            payer[field_name] = new_value
            self.assertEqual([0, 100], weights(self.rt, 'sb_zululand_settlement.116', payer))
            self.pay(payer)
            self.assertEqual(0, payer['gold_reserves'])
            self.assertNotIn(COST, payer['vars'])

    def test_competing_and_repeated_answers_during_payment_only_charge_the_winner(self):
        self.rt.country['movements'][0]['political_movement_radicalism'] = .8
        payer = self.payer('TRN', gold_reserves=5000)
        rival = self.payer('NAL', gold_reserves=3200)
        chief = self.offer(payer)
        self.assertIs(chief, self.offer(rival))
        original_ref = self.rt.ref
        callbacks = []

        def reenter_on_debit(key, scope, prev=None):
            if key == 'scope:sb_chiefs_payment' and scope is payer and not callbacks:
                callbacks.append(key)
                self.pay(payer)
                self.pay(rival)
            return original_ref(key, scope, prev)

        with patch.object(self.rt, 'ref', side_effect=reenter_on_debit):
            self.pay(payer)
        self.assertTrue(callbacks)
        self.assertEqual(1800, payer['gold_reserves'])
        self.assertEqual(3200, rival['gold_reserves'])
        self.assertEqual(1, chief['vars']['sb_court_alignment_var'])
