"""Execute recognition against real house weights and separate current/future pledges."""
import unittest

from tests.test_zulu_frontier_followup import FrontierRuntime, block, field
from tests.test_zulu_court_politics import character, EFFECTS, TRIGGERS


class RecognitionRuntime(FrontierRuntime):
    def condition(self, nodes, scope, prev=None):
        for key, _, value in nodes:
            if key == 'is_ai' and scope.get('is_ai', False) != (value == 'yes'):
                return False
        return super().condition([n for n in nodes if n[0] != 'is_ai'], scope, prev)

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            if node[0] == 'sb_institutions_recalculate':
                # IR/modifier application has separate source-execution tests.
                self.backing()
            else:
                super().effect([node], scope, prev)


def add(rt, name, weight, endorsement=1, template=None, age=35, following=0):
    actor = character(name, following, weight, endorsement, 1, age=age)
    actor.update(owner=rt.country)
    if template: actor['template'] = template
    actor['vars']['sb_court_home_scope'] = rt.country
    rt.country['members'].append(actor)
    rt.country['characters'].append(actor)
    return actor


def setup():
    rt = RecognitionRuntime()
    prince = add(rt, 'Mpande', 45, -1, 'ZUL_mpande_zulu')
    prince['vars']['sb_court_claimant_scope'] = prince
    rt.country['vars']['sb_court_recognized_heir_scope'] = prince
    # Individual representatives incur the existing -10 junior-status modifier.
    houses = [add(rt, name, weight) for name, weight in [('A',50),('B',40),('C',30),('D',20)]]
    return rt, prince, houses


def pledge(rt):
    rt.effect(EFFECTS['sb_court_back_recognized_heir'], rt.country)
    rt.backing()


class RecognitionBackingTests(unittest.TestCase):
    def test_half_the_supporters_prominence_preserves_current_allegiance_and_root(self):
        rt, prince, houses = setup()
        pledge(rt)
        chosen = [h for h in houses if h['vars'].get('sb_court_successor_pledge_scope') is prince]
        self.assertEqual(['A','D'], [h['id'] for h in chosen])
        self.assertEqual(50, sum(h['vars']['sb_court_represented_weight_var'] for h in chosen))
        self.assertTrue(all(h['vars']['sb_court_endorsement_var'] == 1 for h in houses))
        self.assertEqual(150, rt.country['ruler']['vars']['sb_court_current_weight_var'])
        self.assertEqual('GBR', rt.scopes['root']['id'])
        self.assertEqual({}, rt.scopes['root']['vars'])
        self.assertFalse(any(k.startswith('sb_court_recognition_') for k in rt.country['vars']))
        pledge(rt)
        self.assertEqual(chosen, [h for h in houses if h['vars'].get('sb_court_successor_pledge_scope') is prince])

    def test_existing_promises_count_and_rival_pledges_are_preserved(self):
        rt, prince, houses = setup()
        rival = add(rt, 'Gqugqu', 45, -1, 'ZUL_gqugqu_claimant')
        rival['vars']['sb_court_claimant_scope'] = rival
        houses[0]['vars']['sb_court_successor_pledge_scope'] = prince
        houses[1]['vars']['sb_court_successor_pledge_scope'] = rival
        pledge(rt)
        self.assertIs(rival, houses[1]['vars']['sb_court_successor_pledge_scope'])
        self.assertIs(prince, houses[3]['vars']['sb_court_successor_pledge_scope'])
        self.assertNotIn('sb_court_successor_pledge_scope', houses[2]['vars'])

    def test_exiled_support_still_belongs_to_its_registered_court(self):
        rt, prince, houses = setup()
        houses[0]['owner'] = {'id': 'CAP', 'vars': {}}
        houses[0]['is_in_exile_pool'] = True
        pledge(rt)
        self.assertIs(prince, houses[0]['vars']['sb_court_successor_pledge_scope'])
        self.assertEqual('CAP', houses[0]['owner']['id'])
        self.assertEqual({}, houses[0]['owner']['vars'])

    def test_house_is_not_split_and_uncommitted_or_opposing_houses_are_not_recruited(self):
        rt, prince, houses = setup()
        houses[0]['vars']['sb_court_following_var'] = 10
        junior = add(rt, 'junior', 30, following=10)
        neutral = add(rt, 'neutral', 90, 0)
        opponent = add(rt, 'opponent', 80, -1)
        opponent['vars']['sb_court_claimant_scope'] = prince
        pledge(rt)
        self.assertEqual(70, houses[0]['vars']['sb_court_represented_weight_var'])
        self.assertIs(prince, houses[0]['vars']['sb_court_successor_pledge_scope'])
        for actor in (junior, neutral, opponent, rt.country['ruler']):
            self.assertNotIn('sb_court_successor_pledge_scope', actor['vars'])

    def test_recognition_and_newborn_introduction_both_apply_the_support(self):
        for newborn in (False, True):
            rt, prince, houses = setup()
            rt.country['vars']['sb_prerogative_var'] = 100
            if newborn:
                rt.effect(EFFECTS['sb_court_introduce_uthumbu'], rt.country)
                prince = rt.country['heir']
                self.assertEqual(0, prince['age'])
                self.assertEqual(50, rt.country['vars']['sb_prerogative_var'])
            else:
                rt.scopes['candidate'] = prince
                rt.effect([('sb_court_recognize_candidate', '=', [('CANDIDATE','=','scope:candidate')])], rt.country)
                self.assertEqual(75, rt.country['vars']['sb_prerogative_var'])
            chosen = [h for h in houses if h['vars'].get('sb_court_successor_pledge_scope') is prince]
            self.assertEqual(50, sum(h['vars']['sb_court_represented_weight_var'] for h in chosen))
            # The newborn route has no later institutional recalc: its court
            # projection must already include these promises on the same click.
            self.assertEqual(50, sum(h['vars']['sb_court_represented_weight_var'] for h in prince['sb_court_supporters']))

    def test_dead_and_ineligible_supporters_and_empty_pool(self):
        rt, prince, houses = setup()
        houses[0]['alive'] = False
        houses[1]['agitator'] = True
        houses[2]['prominence'] = 0
        houses[3]['vars']['sb_court_endorsement_var'] = 0
        pledge(rt)
        self.assertFalse(any('sb_court_successor_pledge_scope' in h['vars'] for h in houses))


class RecognitionAITests(unittest.TestCase):
    def setUp(self):
        self.rt = RecognitionRuntime()
        self.rt.country['is_ai'] = True
        self.rt.country['ruler'].update(id='Mpande', template='ZUL_mpande_zulu')
        self.rt.country['vars']['sb_prerogative_var'] = 100
        self.rt.scopes['sb_court_country'] = self.rt.country
        self.sons = [add(self.rt, name, weight, -1, template) for name, weight, template in (
            ('Cetshwayo', 45, 'ZUL_cetshwayo_heir'), ('Mbuyazi', 60, 'ZUL_mbuyazi_heir'))]
        self.other = add(self.rt, 'Gqugqu', 90, -1, 'ZUL_gqugqu_claimant')
        for prince in self.sons + [self.other]:
            prince['vars']['sb_court_claimant_scope'] = prince
        self.options = [v for k, _, v in block('events/sb_court_politics_events.txt',
                                             'sb_court_politics.001') if k == 'option']

    def button_weight(self):
        button = block('common/scripted_buttons/sb_court_buttons.txt',
                       'sb_court_recognize_successor_button')
        return self.rt.calc(field(button, 'ai_chance'), self.rt.country)

    def eligible(self, prince):
        return self.rt.condition(TRIGGERS['sb_court_recognisable_successor'], prince)

    def recognise(self, prince):
        self.rt.scopes['candidate'] = prince
        self.rt.effect([('sb_court_recognize_candidate', '=',
                         [('CANDIDATE', '=', 'scope:candidate')])], self.rt.country)

    def option_weight(self, option):
        trigger = next((v for k, _, v in option if k == 'trigger'), [])
        if not self.rt.condition(trigger, self.rt.country):
            return 0
        chance = field(option, 'ai_chance')
        weight = float(field(chance, 'base'))
        for key, _, modifier in chance:
            if key == 'modifier' and self.rt.condition(field(modifier, 'trigger'), self.rt.country):
                weight += float(field(modifier, 'add'))
        return weight

    def test_dingane_never_opens_or_resolves_ai_recognition(self):
        self.rt.country['ruler']['template'] = 'ZUL_dingane'
        self.assertEqual(0, self.button_weight())
        self.assertFalse(any(self.eligible(p) for p in self.sons + [self.other]))
        self.recognise(self.sons[0])
        self.assertEqual(100, self.rt.country['vars']['sb_prerogative_var'])
        self.assertNotIn('sb_court_recognized_heir_scope', self.rt.country['vars'])

    def test_mpande_weights_follow_identity_in_every_candidate_slot(self):
        self.assertEqual(1, self.button_weight())
        self.assertFalse(self.eligible(self.other))
        candidates = self.options[:-1]
        self.assertEqual(12, len(candidates))
        for option in candidates:
            # The source's option trigger identifies its saved candidate slot.
            slot = next(k[4:] for k, _, _ in field(option, 'trigger') if k.startswith('var:'))
            for prince, expected in zip(self.sons + [self.other], (66, 33, 0)):
                with self.subTest(slot=slot, prince=prince['id']):
                    self.rt.country['vars'][slot] = prince
                    self.assertEqual(expected, self.option_weight(option))
            self.rt.country['vars'].pop(slot)
        self.assertEqual(0, self.option_weight(self.options[-1]))

    def test_selection_excludes_other_princes_and_spends_once(self):
        self.rt.effect([('sb_court_prepare_succession_choice', '=', 'yes')], self.rt.country)
        variables = self.rt.country['vars']
        self.assertIs(self.sons[1], variables['sb_court_action_actor_scope'])
        self.assertIs(self.sons[0], variables['sb_court_second_candidate_scope'])
        self.assertNotIn('sb_court_third_candidate_scope', variables)
        self.recognise(self.sons[0])
        self.assertEqual(75, variables['sb_prerogative_var'])
        self.assertIs(self.sons[0], variables['sb_court_recognized_heir_scope'])
        self.assertEqual(0, self.button_weight())
        self.recognise(self.sons[1])
        self.assertEqual(75, variables['sb_prerogative_var'])
        self.assertIs(self.sons[0], variables['sb_court_recognized_heir_scope'])

    def test_missing_sons_dead_heir_and_stale_selection(self):
        cetshwayo, mbuyazi = self.sons
        cetshwayo['alive'] = False
        self.rt.country['vars']['sb_court_recognized_heir_scope'] = cetshwayo
        self.assertEqual(1, self.button_weight())
        self.assertTrue(self.eligible(mbuyazi))
        self.assertFalse(self.eligible(cetshwayo))
        mbuyazi['vars']['sb_court_claim_renounced_var'] = 1
        self.assertEqual(0, self.button_weight())
        self.assertEqual(10, self.option_weight(self.options[-1]))
        self.recognise(mbuyazi)
        self.assertEqual(100, self.rt.country['vars']['sb_prerogative_var'])
        self.assertIs(cetshwayo, self.rt.country['vars']['sb_court_recognized_heir_scope'])

    def test_human_redesignation_other_rulers_and_foreign_preview_scope(self):
        for ruler in ('ZUL_dingane', 'ZUL_mpande_zulu'):
            self.rt.country['is_ai'] = False
            self.rt.country['ruler']['template'] = ruler
            self.assertTrue(self.eligible(self.other))
            self.recognise(self.sons[0])
            self.recognise(self.sons[1])
            self.assertIs(self.sons[1], self.rt.country['vars']['sb_court_recognized_heir_scope'])
        self.rt.country['is_ai'] = True
        self.rt.country['ruler']['template'] = 'ZUL_dinuzulu_heir'
        self.assertTrue(self.eligible(self.other))
        self.rt.country['vars']['sb_court_action_actor_scope'] = self.other
        self.assertEqual(50, self.option_weight(self.options[0]))
        self.assertEqual(10, self.option_weight(self.options[-1]))
        self.rt.country['ruler']['template'] = 'ZUL_mpande_zulu'
        self.rt.country['vars'].pop('sb_court_recognized_heir_scope')
        self.rt.scopes['sb_court_country'] = self.rt.scopes['root']
        self.assertEqual(1, self.button_weight())
        self.assertEqual({}, self.rt.scopes['root']['vars'])


if __name__ == '__main__':
    unittest.main()
