"""Execute the two shipment choices; native rendering/expiry remain DP checks."""
import unittest

from tests.test_zulu_dunn_event import DunnRuntime, DUNN_TRIGGERS
from tests.test_zulu_court_rework import ReworkRuntime
from tests.test_zulu_court_politics import COURT_MODIFIERS, definitions
from tests.test_zulu_frontier_followup import block, field


EVENT = block('events/sb_court_dunn_events.txt', 'sb_court_dunn.002')
OPTIONS = {field(v, 'name'): v for k, _, v in EVENT if k == 'option'}
MODIFIERS = definitions('common/static_modifiers/sb_court_episode_modifiers.txt')
DEATH = field(block('common/on_actions/sb_court_on_actions.txt', 'sb_court_on_character_death'), 'effect')


class ShipmentRuntime(DunnRuntime, ReworkRuntime):
    def __init__(self):
        super().__init__()
        self.country['ruler']['template'] = 'ZUL_cetshwayo_heir'
        self.rival = self.actor('ZUL_gqugqu_claimant', house=0, alignment=1)
        self.rival['vars'].update(sb_court_endorsement_var=-1, sb_court_claimant_scope=self.rival)
        self.ally = self.actor('allied_house', house=20)
        self.ally['prominence'] = 60
        self.ally['vars']['sb_court_endorsement_var'] = 1
        self.opponent = self.actor('opposing_house', house=21)
        self.opponent['prominence'] = 80
        self.opponent['vars'].update(sb_court_endorsement_var=-1, sb_court_claimant_scope=self.rival)
        self.dunn = self.actor('SB_ZUL_john_dunn')
        self.dunn['vars']['sb_court_dunn_admitted_var'] = 1
        self.global_vars['sb_court_dunn_identity_scope'] = self.dunn
        self.roll = .5
        self.rolls = 0
        self.deaths = []
        self.backing()

    def ref(self, key, scope, prev=None):
        value = super().ref(key, scope, prev)
        if key == 'prominence' and value is not None:
            for name, multiplier in scope.get('modifiers', {}).items():
                # Other test modules can register these definitions in the shared
                # runtime first. Never count a source modifier twice during discovery.
                if name in COURT_MODIFIERS: continue
                for modifier, _, amount in MODIFIERS.get(name, []):
                    if modifier == 'character_prominence_add': value += float(amount) * multiplier
            # Installed NCharacter.MAX_PROMINENCE; coalition values separately floor at zero.
            return min(100, value)
        return value

    def condition(self, nodes, scope, prev=None):
        for node in nodes:
            key, _, value = node
            if key == 'is_ai': result = scope.get('ai', False) == (value == 'yes')
            elif key == 'has_game_rule': result = value in self.country.get('rules', set())
            else: result = super().condition([node], scope, prev)
            if not result: return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, _, value = node
            if key == 'random_list': self.rolls += 1
            super().effect([node], scope, prev)
            if key == 'kill_character':
                self.deaths.append(scope)
                # Explicitly exercise the shipped death hook; the base interpreter does not.
                self.effect(DEATH, scope)

    def open(self):
        # Each native event has its own saved context, not the previous year's targets.
        self.scopes = {'root': self.scopes['root']}
        self.effect([('sb_court_offer_dunn_delivery', '=', [('DAYS', '=', '0')])], self.dunn)
        self.effect(field(EVENT, 'immediate'), self.country)

    def valid(self): return self.condition(DUNN_TRIGGERS['sb_court_dunn_faction_delivery_valid'], self.country)

    def choose(self, choice): self.effect(field(OPTIONS['sb_court_dunn.002.' + choice], 'hidden_effect'), self.country)


class DunnShipmentTests(unittest.TestCase):
    def test_opening_quotes_same_camp_without_awarding_either_choice(self):
        rt = ShipmentRuntime()
        before = rt.country['vars']['sb_court_weight_var']
        rt.open()
        self.assertTrue(rt.valid())
        self.assertIs(rt.ally, rt.scopes['sb_court_dunn_ally'])
        self.assertIs(rt.opponent, rt.scopes['sb_court_dunn_opponent'])
        self.assertIs(rt.rival, rt.scopes['sb_court_dunn_enemy_prince'])
        self.assertEqual(before, rt.country['vars']['sb_court_weight_var'])
        self.assertNotIn('sb_firearms_supply_weeks_var', rt.country['vars'])
        self.assertNotIn('sb_court_dunn_armed_following', rt.ally.get('modifiers', {}))
        self.assertEqual(0, rt.rolls)
        self.assertEqual({}, rt.scopes['root']['vars'])

    def test_wide_distribution_consumes_the_only_receipt(self):
        rt = ShipmentRuntime(); rt.open(); rt.choose('a'); rt.choose('a'); rt.choose('b')
        self.assertEqual(2, rt.country['vars']['sb_firearms_supply_weeks_var'])
        self.assertEqual(0, rt.rolls)
        self.assertNotIn('sb_court_dunn_delivery_open_var', rt.dunn['vars'])
        self.assertIn('sb_court_dunn_delivered_guns_var', rt.dunn['vars'])
        self.assertIn('sb_court_dunn_delivery_year_var', rt.dunn['vars'])
        self.assertNotIn('sb_court_dunn_outgunned', rt.opponent.get('modifiers', {}))

    def test_faction_grants_pair_and_exactly_one_independent_roll(self):
        for roll, dies in ((0, True), (.0099, True), (.01, False), (.9999, False)):
            with self.subTest(roll=roll):
                rt = ShipmentRuntime(); rt.roll = roll
                rt.ally['vars']['sb_court_successor_pledge_scope'] = rt.mbuyazi
                rt.opponent['vars']['sb_court_successor_pledge_scope'] = rt.mbuyazi
                rt.open(); rt.choose('b'); rt.choose('b'); rt.choose('a')
                self.assertEqual(70, rt.ref('prominence', rt.ally))
                self.assertEqual(70, rt.ref('prominence', rt.opponent))
                self.assertEqual(1, rt.rolls)
                self.assertEqual(dies, not rt.rival['alive'])
                self.assertEqual([rt.rival] if dies else [], rt.deaths)
                self.assertTrue(rt.ally['alive'] and rt.opponent['alive'] and rt.mbuyazi['alive'])
                self.assertNotIn('sb_firearms_supply_weeks_var', rt.country['vars'])
                self.assertNotIn('sb_court_dunn_delivery_open_var', rt.dunn['vars'])
                self.assertIs(rt.mbuyazi, rt.ally['vars']['sb_court_successor_pledge_scope'])
                self.assertIs(rt.mbuyazi, rt.opponent['vars']['sb_court_successor_pledge_scope'])
                for actor in (rt.ally, rt.opponent): self.assertEqual('5', actor['modifier_terms'][-1]['years'])

    def test_lethal_result_releases_only_dead_princes_commitments(self):
        rt = ShipmentRuntime(); rt.roll = 0
        rt.opponent['vars'].update(sb_court_successor_pledge_scope=rt.rival, sb_court_council_promise_scope=rt.rival)
        rt.ally['vars']['sb_court_successor_pledge_scope'] = rt.mbuyazi
        rt.open(); rt.choose('b')
        self.assertEqual(0, rt.opponent['vars']['sb_court_endorsement_var'])
        for key in ('sb_court_claimant_scope', 'sb_court_successor_pledge_scope', 'sb_court_council_promise_scope'):
            self.assertNotIn(key, rt.opponent['vars'])
        self.assertIs(rt.mbuyazi, rt.ally['vars']['sb_court_successor_pledge_scope'])
        self.assertIn(('sb_court_politics.900', 1), rt.country['event_schedule'])
        self.assertFalse(any('settlement' in e or 'nrp' in e for e in rt.country.get('events', [])))

    def test_named_targets_revalidate_without_substitution_or_consumption(self):
        cases = ('ally_dead', 'ally_defected', 'ally_foreign', 'ally_exiled', 'ally_minor',
                 'ally_agitator', 'ally_zero', 'ally_not_representative', 'opponent_loyal',
                 'opponent_new_patron', 'prince_dead', 'prince_loyal', 'prince_renounced',
                 'prince_foreign', 'new_ruler', 'court_inactive', 'accession', 'dynastic', 'civil_war', 'action')
        for invalid in cases:
            with self.subTest(invalid=invalid):
                rt = ShipmentRuntime(); rt.open()
                if invalid == 'ally_dead': rt.ally['alive'] = False
                elif invalid == 'ally_defected': rt.ally['vars']['sb_court_endorsement_var'] = 0
                elif invalid == 'ally_foreign': rt.ally['owner'] = rt.scopes['root']
                elif invalid == 'ally_exiled': rt.ally['is_in_exile_pool'] = True
                elif invalid == 'ally_minor': rt.ally['age'] = 15
                elif invalid == 'ally_agitator': rt.ally['agitator'] = True
                elif invalid == 'ally_zero': rt.ally['prominence'] = 0
                elif invalid == 'ally_not_representative': rt.ally['vars'].pop('sb_court_representative_var')
                elif invalid == 'opponent_loyal': rt.opponent['vars']['sb_court_endorsement_var'] = 1
                elif invalid == 'opponent_new_patron': rt.opponent['vars']['sb_court_claimant_scope'] = rt.mbuyazi
                elif invalid == 'prince_dead': rt.rival['alive'] = False
                elif invalid == 'prince_loyal': rt.rival['vars']['sb_court_endorsement_var'] = 1
                elif invalid == 'prince_renounced': rt.rival['vars']['sb_court_claim_renounced_var'] = 1
                elif invalid == 'prince_foreign': rt.rival['owner'] = rt.scopes['root']
                elif invalid == 'new_ruler': rt.country['ruler'] = rt.mbuyazi
                elif invalid == 'court_inactive': rt.country['vars'].pop('sb_institutions_active_var')
                else: rt.country['vars'][{'accession':'sb_court_accession_open_var', 'dynastic':'sb_court_dynastic_crisis_var', 'civil_war':'sb_court_civil_war_var', 'action':'sb_court_action_open_var'}[invalid]] = 1
                self.assertFalse(rt.valid())
                rt.choose('b')
                self.assertEqual(0, rt.rolls)
                self.assertIn('sb_court_dunn_delivery_open_var', rt.dunn['vars'])
                rt.choose('a')
                self.assertEqual(2, rt.country['vars']['sb_firearms_supply_weeks_var'])

    def test_future_pledges_and_constitutional_opposition_are_not_current_enemies(self):
        rt = ShipmentRuntime()
        rt.rival['vars']['sb_court_endorsement_var'] = 1
        rt.opponent['vars'].update(sb_court_endorsement_var=1, sb_court_alignment_var=2, sb_court_successor_pledge_scope=rt.rival)
        rt.open()
        self.assertFalse(rt.valid())
        self.assertNotIn('sb_court_dunn_enemy_prince', rt.scopes)
        self.assertNotIn('sb_court_dunn_opponent', rt.scopes)
        rt.choose('a')
        self.assertEqual(2, rt.country['vars']['sb_firearms_supply_weeks_var'])

    def test_refresh_does_not_stack_and_fresh_recipients_are_preferred(self):
        rt = ShipmentRuntime(); rt.open(); rt.choose('b')
        # Next year's event may refresh the same characters; no automatic weekly draw.
        rt.run('sb_court_dunn_trade_monthly')
        self.assertEqual(1, rt.rolls)
        rt.dunn['vars'].pop('sb_court_dunn_delivery_year_var')
        rt.open(); rt.choose('b')
        self.assertEqual((70, 70), (rt.ref('prominence', rt.ally), rt.ref('prominence', rt.opponent)))
        self.assertEqual(2, len(rt.ally['modifier_terms']))
        fresh = rt.actor('fresh_ally', house=22)
        fresh['vars']['sb_court_endorsement_var'] = 1
        rt.dunn['vars'].pop('sb_court_dunn_delivery_year_var')
        rt.open()
        self.assertIs(fresh, rt.scopes['sb_court_dunn_ally'])
        rt.choose('b')
        self.assertEqual(30, rt.ref('prominence', fresh))
        self.assertEqual(70, rt.ref('prominence', rt.ally))

    def test_prominence_cap_and_renewal_at_cap(self):
        rt = ShipmentRuntime(); rt.ally['prominence'] = 95
        rt.open(); rt.choose('b')
        self.assertEqual(100, rt.ref('prominence', rt.ally))
        rt.dunn['vars'].pop('sb_court_dunn_delivery_year_var')
        rt.open()
        self.assertTrue(rt.valid())
        rt.choose('b')
        self.assertEqual(100, rt.ref('prominence', rt.ally))
        self.assertEqual(2, len(rt.ally['modifier_terms']))
        rt = ShipmentRuntime(); rt.ally['prominence'] = 100; rt.open()
        self.assertFalse(rt.valid())

    def test_mpande_sons_protected_and_gqugqu_still_targetable(self):
        for ai in (False, True):
            for rule in ('sb_frontier_ai_behavior_strict_historical', 'sb_frontier_ai_behavior_dynamic_historical'):
                for prince in ('ZUL_cetshwayo_heir', 'ZUL_mbuyazi_heir', 'ZUL_gqugqu_claimant'):
                    with self.subTest(ai=ai, rule=rule, prince=prince):
                        rt = ShipmentRuntime()
                        rt.country.update(ai=ai, rules={rule})
                        rt.country['ruler']['template'] = 'ZUL_mpande_zulu'
                        rt.rival['template'] = prince
                        rt.open()
                        self.assertEqual(prince == 'ZUL_gqugqu_claimant', rt.valid())

    def test_princes_own_house_is_a_valid_opposing_member(self):
        rt = ShipmentRuntime()
        rt.opponent['vars']['sb_court_endorsement_var'] = 0
        rt.open()
        self.assertTrue(rt.valid())
        self.assertIs(rt.rival, rt.scopes['sb_court_dunn_opponent'])
        before = rt.ref('prominence', rt.rival)
        rt.choose('b')
        self.assertEqual(before - 10, rt.ref('prominence', rt.rival))
        self.assertEqual(1, rt.rolls)

    def test_house_weight_counts_each_modified_member_once(self):
        rt = ShipmentRuntime()
        junior = rt.actor('allied_junior', house=20)
        junior['prominence'] = 30
        rt.open()
        before = rt.ally['vars']['sb_court_represented_weight_var']
        rt.choose('b')
        self.assertEqual(before + 10, rt.ally['vars']['sb_court_represented_weight_var'])
        self.assertNotIn('sb_court_dunn_armed_following', junior.get('modifiers', {}))
        # No independent P award or direct commitment/constitution conversion.
        self.assertEqual(0, rt.country['vars']['sb_prerogative_var'])
        self.assertEqual(1, rt.ally['vars']['sb_court_endorsement_var'])
        self.assertEqual(-1, rt.opponent['vars']['sb_court_endorsement_var'])
        self.assertEqual(0, rt.ally['vars']['sb_court_alignment_var'])

    def test_finished_firearms_and_missing_trader_cancel_both_choices(self):
        for invalid in ('finished', 'dead', 'foreign'):
            rt = ShipmentRuntime(); rt.open()
            if invalid == 'finished': rt.country['vars']['sb_firearms_modernized_var'] = 1
            elif invalid == 'dead': rt.dunn['alive'] = False
            else: rt.dunn['owner'] = rt.scopes['root']
            rt.choose('a'); rt.choose('b')
            self.assertNotIn('sb_firearms_supply_weeks_var', rt.country['vars'])
            self.assertEqual(0, rt.rolls)


if __name__ == '__main__': unittest.main()
