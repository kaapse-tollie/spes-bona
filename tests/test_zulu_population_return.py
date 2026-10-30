"""Execute the shipped post-war moves; native merge/employment remain DP checks."""
from collections import Counter
from itertools import product
from pathlib import Path
import unittest

from tests import test_zulu_contested_crown as claimant
from tests.test_zulu_contested_crown import ClaimantRuntime, court, reserve, answer, split
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import find_object


ROOT = Path(__file__).resolve().parents[1]
SHARE = 'sb_court_population_natal_share_var'
PENDING = 'sb_court_population_return_pending_var'
RECEIPT = statements(find_object((ROOT/'events/sb_court_population_return_events.txt').read_text(encoding='utf-8-sig'), 'sb_court_population_return.001'))


def population(state):
    return sum(p['workforce'] + p['dependants'] for p in state.get('pops', []))


def composition(states):
    result = Counter()
    for state in states:
        for pop in state.get('pops', []):
            result[(pop['type'], pop['culture'], pop['religion'])] += pop['workforce'] + pop['dependants']
    return result


class PopulationRuntime(ClaimantRuntime):
    def ref(self, key, scope, prev=None):
        if key == 'state_population' and scope is not None and 'pops' in scope:
            return population(scope)
        return super().ref(key, scope, prev)


class PopulationReturn(unittest.TestCase):
    def case(self, natal=2000, mainland=10000):
        rt, king, prince, third, neutral = court(300, 100)
        rt.__class__ = PopulationRuntime
        helper = claimant.ClaimantBehaviour()
        zululand, klip = helper.recruitment_states(rt, [(4, 0), (0, 0)])
        zululand.update(state_region='s:STATE_ZULULAND', pops=[])
        klip.update(state_region='s:STATE_NATAL', pops=[])
        helper.add_staff(zululand, 'peasants', mainland // 4, mainland - mainland // 4)
        helper.add_staff(klip, 'peasants', natal // 4, natal - natal // 4)
        return rt, king, prince, zululand, klip

    @staticmethod
    def move(rt, source, destination, fraction):
        rt.scopes['fixture_destination'] = destination
        for pop in list(source['pops']):
            rt.effect([('move_partial_pop', '=', [('state', '=', 'scope:fixture_destination'),
                                                 ('population_ratio', '=', str(fraction))])], pop)

    @staticmethod
    def merge(winner, loser, states):
        # Native reunion is supplied explicitly: these tests do not prove its timing.
        winner['states'] = list(states)
        loser['states'] = []
        for state in states:
            state['owner'] = winner
            for pop in state['pops']:
                pop['owner'] = winner

    @staticmethod
    def receipt(rt, winner):
        fields = dict((k, v) for k, _, v in RECEIPT)
        if rt.condition(fields['trigger'], winner):
            rt.effect(fields['immediate'], winner)

    def assert_no_receipt(self, country):
        self.assertFalse(any(k.startswith('sb_court_population_') for k in country['vars']))

    def assert_ratio(self, natal, mainland, share):
        # Native per-Pop workforce/dependant rounding can leave a few people either side.
        tolerance = 2 * sum(len(s['pops']) for s in (natal, mainland))
        self.assertAlmostEqual(population(natal), (population(natal) + population(mainland)) * share,
                               delta=tolerance)


    @staticmethod
    def barracks(state):
        return sum(b['level'] for b in state['buildings'] if b['type'] == 'building_barrack')

    def test_cancelled_preparation_returns_barracks_without_moving_people(self):
        rt, king, prince, mainland, natal = self.case()
        reserve(rt, king, prince)
        answer(rt)
        self.assertEqual((3, 1), (self.barracks(mainland), self.barracks(natal)))
        before = composition((mainland, natal))
        rt.run('sb_court_cancel_dynastic_crisis')
        self.assertEqual((4, 0), (self.barracks(mainland), self.barracks(natal)))
        self.assertEqual(before, composition((mainland, natal)))
        self.assertFalse(any(k.startswith('sb_court_barracks_') for k in rt.country['vars']))

    def test_barracks_receipt_reverses_only_wartime_relocation(self):
        for natal_original, mainland_original, natal_wartime, extra in ((0,4,1,0),(0,4,2,2),(4,1,1,2)):
            rt, _, _, mainland, natal = self.case()
            for state, level in ((mainland,mainland_original),(natal,natal_original)):
                state['buildings'] = [{'type':'building_barrack','level':level,'vars':{},'production_methods':{'pm_general_training'}}] if level else []
            rt.run('sb_court_start_barracks_receipt')
            rt.run('sb_court_begin_barracks_relocation')
            total = natal_original + mainland_original
            for state, level in ((mainland,total-natal_wartime),(natal,natal_wartime)):
                state['buildings'] = [{'type':'building_barrack','level':level,'vars':{},'production_methods':{'pm_general_training'}}]
            rt.run('sb_court_record_barracks_relocation')
            for state in (mainland,natal): state['buildings'][0]['level'] += extra
            rt.run('sb_court_schedule_population_return')
            self.assertEqual((mainland_original+extra,natal_original+extra),(self.barracks(mainland),self.barracks(natal)))
            self.assertFalse(any(k.startswith('sb_court_barracks_') for k in rt.country['vars']))
            operations = list(rt.demolitions)
            rt.run('sb_court_schedule_population_return')
            self.assertEqual(operations,rt.demolitions)

    def test_construction_and_demolition_between_preparation_and_split_are_preserved(self):
        for build, demolish, natal_original, expected in ((2,False,0,(4,2)),(0,True,0,(3,0)),(0,True,2,(4,1))):
            rt,king,prince,mainland,natal = self.case(mainland=100000)
            if natal_original:
                natal['buildings'] = [{'type':'building_barrack','level':natal_original,'vars':{},'production_methods':{'pm_no_organization'}}]
            reserve(rt,king,prince)
            answer(rt)
            if demolish:
                b=next(b for b in natal['buildings'] if b['type']=='building_barrack')
                b['level']-=1
                natal['buildings']=[b for b in natal['buildings'] if b['level']>0]
            else:
                next(b for b in natal['buildings'] if b['type']=='building_barrack')['level'] += build
            rt.country['states'] = [mainland]
            _, rebels = split(rt,native_rebel_states=[natal])
            self.merge(rt.country,rebels,[mainland,natal])
            rt.run('sb_court_record_dynastic_end')
            rt.run('sb_court_resolve_dynastic_win')
            self.assertEqual(expected,(self.barracks(mainland),self.barracks(natal)))

    def test_demolished_wartime_barracks_are_not_recreated(self):
        for remaining in (0,1):
            rt, _, _, mainland, natal = self.case()
            rt.run('sb_court_start_barracks_receipt')
            rt.run('sb_court_begin_barracks_relocation')
            mainland['buildings'][0]['level'] = 2
            natal['buildings'] = [{'type':'building_barrack','level':2,'vars':{},'production_methods':{'pm_no_organization'}}]
            rt.run('sb_court_record_barracks_relocation')
            if remaining: natal['buildings'][0]['level'] = remaining
            else: natal['buildings'] = []
            rt.run('sb_court_schedule_population_return')
            self.assertEqual((2+remaining,0),(self.barracks(mainland),self.barracks(natal)))

    def test_no_barracks_receipt_does_not_guess_an_old_saves_original_distribution(self):
        rt, _, _, mainland, natal = self.case()
        natal['buildings'] = [{'type':'building_barrack','level':2,'vars':{},'production_methods':set()}]
        rt.country['vars'][SHARE] = 1/6
        rt.run('sb_court_schedule_population_return')
        self.assertEqual((4,2),(self.barracks(mainland),self.barracks(natal)))

    def test_returns_surviving_population_in_both_directions_without_recreating_losses(self):
        for from_natal in (False, True):
            rt, _, _, mainland, natal = self.case()
            claimant.ClaimantBehaviour().add_staff(mainland, 'officers', 25, 75, 'sotho', 'protestant')
            rt.run('sb_court_snapshot_population_ratio')
            share = rt.country['vars'][SHARE]
            self.move(rt, natal if from_natal else mainland, mainland if from_natal else natal, .5)
            for state in (mainland, natal):
                for pop in state['pops']:
                    pop['workforce'] = int(pop['workforce'] * .8)
                    pop['dependants'] = int(pop['dependants'] * .8)
            survivors = composition((mainland, natal))
            self.assertLess(sum(survivors.values()), 12100)
            rt.run('sb_court_schedule_population_return')
            self.assert_ratio(natal, mainland, share)
            self.assertEqual(survivors, composition((mainland, natal)))
            self.assert_no_receipt(rt.country)

    def test_both_victors_receive_snapshot_and_return_after_native_reunion(self):
        for backing_prince, rebel_wins in product((False, True), repeat=2):
            with self.subTest(backing_prince=backing_prince, rebel_wins=rebel_wins):
                rt, king, prince, mainland, natal = self.case(mainland=100000)
                reserve(rt, king, prince)
                answer(rt, backing_prince)
                share = rt.country['vars'][SHARE]
                self.assertAlmostEqual(2000 / 102000, share)
                rt.country['states'] = [mainland]
                _, rebels = split(rt, native_rebel_states=[natal])
                self.assertEqual(share, rebels['vars'][SHARE])
                winner, loser = (rebels, rt.country) if rebel_wins else (rt.country, rebels)
                survivors = composition((mainland, natal))
                self.merge(winner, loser, [mainland, natal])
                rt.run('sb_court_record_dynastic_end')
                rt.run('sb_court_resolve_dynastic_win', winner)
                self.assertEqual((4,0),(self.barracks(mainland),self.barracks(natal)))
                self.assert_ratio(natal, mainland, share)
                self.assertEqual(survivors, composition((mainland, natal)))
                self.assert_no_receipt(winner)
                self.assert_no_receipt(loser)
                moves = list(rt.pop_moves)
                rt.run('sb_court_resolve_dynastic_win', winner)
                self.receipt(rt, winner)
                self.assertEqual(moves, rt.pop_moves)
                self.assertEqual({}, rt.scopes['root']['vars'])

    def test_return_receipt_survives_court_cleanup_until_ownership_merges(self):
        for rebel_wins in (False, True):
            rt, king, prince, mainland, natal = self.case(mainland=100000)
            reserve(rt, king, prince)
            answer(rt)
            share = rt.country['vars'][SHARE]
            rt.country['states'] = [mainland]
            _, rebels = split(rt, native_rebel_states=[natal])
            winner, loser = (rebels, rt.country) if rebel_wins else (rt.country, rebels)
            rt.run('sb_court_record_dynastic_end')
            rt.run('sb_court_resolve_dynastic_win', winner)
            self.assertEqual(2, winner['vars'][PENDING])
            self.assertNotIn('sb_court_dynastic_opponent_scope', winner['vars'])
            self.assertIs(loser, winner['vars']['sb_court_population_opponent_scope'])
            self.assert_no_receipt(loser)
            self.merge(winner, loser, [mainland, natal])
            survivors = composition((mainland, natal))
            self.receipt(rt, winner)
            self.assertEqual((4,0),(self.barracks(mainland),self.barracks(natal)))
            self.assert_ratio(natal, mainland, share)
            self.assertEqual(survivors, composition((mainland, natal)))
            self.assert_no_receipt(winner)

    def test_waits_if_opponent_still_owns_a_relevant_portion(self):
        rt, _, _, mainland, natal = self.case()
        rt.run('sb_court_snapshot_population_ratio')
        opponent = {'id': 'REB', 'vars': {}, 'states': [{'state_region': 's:STATE_NATAL', 'vars': {}}]}
        rt.country['vars']['sb_court_dynastic_opponent_scope'] = opponent
        self.move(rt, mainland, natal, .5)
        before = len(rt.pop_moves)
        rt.run('sb_court_schedule_population_return')
        self.assertEqual(before, len(rt.pop_moves))
        self.assertEqual(2, rt.country['vars'][PENDING])
        opponent['states'] = []
        self.receipt(rt, rt.country)
        self.assert_ratio(natal, mainland, 1/6)

    def test_missing_region_abandons_after_two_retries_without_touching_foreign_land(self):
        rt, _, _, mainland, natal = self.case()
        rt.run('sb_court_snapshot_population_ratio')
        foreign = {'id': 'NAL', 'vars': {}, 'states': [natal]}
        natal['owner'] = foreign
        for pop in natal['pops']: pop['owner'] = foreign
        rt.country['states'] = [mainland]
        original = composition((mainland, natal))
        rt.run('sb_court_schedule_population_return')
        self.assertEqual(2, rt.country['vars'][PENDING])
        self.receipt(rt, rt.country)
        self.assertEqual(1, rt.country['vars'][PENDING])
        self.receipt(rt, rt.country)
        self.assert_no_receipt(rt.country)
        self.assertEqual(['sb_court_population_return.001'] * 2, rt.country['events'])
        self.assertEqual(original, composition((mainland, natal)))
        self.assertFalse(getattr(rt, 'pop_moves', []))

    def test_no_snapshot_means_no_migration_for_one_state_or_unrelated_region(self):
        for missing in ('s:STATE_NATAL', 's:STATE_ZULULAND'):
            rt, king, prince, mainland, natal = self.case()
            rt.country['states'] = [s for s in rt.country['states'] if s['state_region'] != missing]
            reserve(rt, king, prince)
            answer(rt)
            self.assertNotIn(SHARE, rt.country['vars'])
            rt.run('sb_court_schedule_population_return')
            self.assertFalse(getattr(rt, 'pop_moves', []))
            self.assert_no_receipt(rt.country)
        rt, _, _, mainland, natal = self.case()
        natal['state_region'] = 's:STATE_TRANSVAAL'
        rt.run('sb_court_snapshot_population_ratio')
        self.assert_no_receipt(rt.country)

    def test_zero_population_and_zero_donor_do_not_divide_by_zero(self):
        rt, _, _, mainland, natal = self.case(natal=0, mainland=0)
        rt.run('sb_court_snapshot_population_ratio')
        self.assert_no_receipt(rt.country)
        for share in (0, .25, 1):
            rt.country['vars'][SHARE] = share
            rt.run('sb_court_schedule_population_return')
            self.assert_no_receipt(rt.country)
        for natal_size, mainland_size in ((0, 1000), (1000, 0)):
            rt, _, _, mainland, natal = self.case(natal=natal_size, mainland=mainland_size)
            rt.country['vars'][SHARE] = .25
            rt.run('sb_court_schedule_population_return')
            self.assert_ratio(natal, mainland, .25)

    def test_aggregate_regions_rediscover_current_state_ids_and_leave_other_states_alone(self):
        rt, _, _, mainland, natal = self.case()
        helper = claimant.ClaimantBehaviour()
        extra = {'id': 'transvaal', 'owner': rt.country, 'vars': {}, 'state_region': 's:STATE_TRANSVAAL', 'pops': []}
        helper.add_staff(extra, 'labourers', 100, 300)
        rt.country['states'].append(extra)
        rt.run('sb_court_snapshot_population_ratio')
        self.move(rt, mainland, natal, .5)
        mainland['id'] = 'merged-mainland'
        natal['id'] = 'merged-natal'
        untouched = composition((extra,))
        rt.run('sb_court_schedule_population_return')
        self.assert_ratio(natal, mainland, 1/6)
        self.assertEqual(untouched, composition((extra,)))
        self.assertTrue(all(old != 'transvaal' and new != 'transvaal' for _, old, new, _, _ in rt.pop_moves))

    def test_cancel_before_war_discards_snapshot_without_moving_people(self):
        rt, king, prince, mainland, natal = self.case()
        reserve(rt, king, prince)
        answer(rt)
        self.assertIn(SHARE, rt.country['vars'])
        rt.run('sb_court_cancel_dynastic_crisis')
        self.assert_no_receipt(rt.country)
        self.assertFalse(getattr(rt, 'pop_moves', []))


if __name__ == '__main__':
    unittest.main()
