"""Execute backing, signed target modifiers and AI gates; native convergence is not simulated."""
import unittest
from tests.test_zulu_court_politics import CourtRuntime, character, EFFECTS, VALUES, definitions
from tests.test_chiefdoms_playtest_november import ReconciliationContest, calculate

MODIFIER = 'sb_chiefs_prominence_pressure'
ROYAL = 'sb_court_royal_political_weight_var'
CHIEFLY = 'sb_court_chiefly_political_weight_var'
SETTLEMENT = definitions('common/scripted_effects/sb_zululand_settlement_effects.txt')


def movement(owner, kind='royal'):
    return dict(type='movement_sb_zulu_' + kind, owner=owner, vars={}, modifiers={})


class PressureCourt(CourtRuntime):
    def __init__(self, members=()):
        super().__init__(list(members))
        self.country['alive'] = True
        self.global_vars.update(sb_zululand_chiefdoms_open_global_var=1,
                                sb_zululand_live_zul_scope=self.country)
        self.state = dict(vars={'sb_chiefs_origin_scope': self.country})
        self.containers['sb_zululand_chiefdoms_state'] = self.state
        self.royal = movement(self.country)
        self.chiefly = movement(self.country, 'chiefly')
        self.country['movements'] = [self.royal, self.chiefly]

    def update(self):
        self.effect(EFFECTS['sb_chiefs_update_prominence_pressure'], self.scopes['root'])

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, _, value = node
            if key in ('sb_zululand_stop_contest_interventions','sb_institutions_recalculate'): pass  # Separate aid lifecycle tests.
            elif key.startswith('c:'): pass  # No Natal country record in this modifier fixture.
            elif key == 'destroy_container':
                self.containers = {k:v for k,v in self.containers.items() if v is not scope}
            else: super().effect([node], scope, prev)


class ProminencePressureTests(unittest.TestCase):
    def test_returned_agitator_stays_in_political_backing_once(self):
        head = character('head', 18, 80, alignment=1)
        junior = character('junior', 18, 55, alignment=2, agitator=True)
        chief = character('chief', 9, 100, alignment=2)
        neutral = character('neutral', 10, 50)
        rt = PressureCourt([head, junior, chief, neutral])
        junior['owner'] = dict(id='CAP', vars={})
        rt.backing()
        self.assertEqual(125, rt.country['vars'][ROYAL])  # Head 80 + junior 55−10.
        self.assertEqual(100, rt.country['vars'][CHIEFLY])
        self.assertEqual(125, rt.country['vars']['sb_court_royal_weight_var'])
        junior['owner'] = rt.country
        for _ in range(3): rt.backing()
        self.assertEqual(125, rt.country['vars'][ROYAL])
        self.assertEqual(80, rt.country['vars']['sb_court_royal_weight_var'])
        self.assertAlmostEqual(.025, rt.royal['modifiers'][MODIFIER])
        junior['alive'] = False
        rt.backing()
        self.assertEqual(80, rt.country['vars'][ROYAL])
        self.assertAlmostEqual(-.02, rt.royal['modifiers'][MODIFIER])

    def test_signed_caps_ties_and_repeated_updates_preserve_other_modifiers(self):
        rt = PressureCourt()
        rt.royal['modifiers']['sb_usuthu_volunteers'] = 1
        for royal, chiefly, expected in ((358,100,.258),(100,358,-.258),(600,100,.30),
                                          (100,600,-.30),(400,100,.30),(100,100,0)):
            rt.country['vars'].update({ROYAL:royal, CHIEFLY:chiefly})
            for _ in range(3): rt.update()
            self.assertAlmostEqual(expected, rt.royal['modifiers'].get(MODIFIER,0))
            self.assertEqual(1, rt.royal['modifiers']['sb_usuthu_volunteers'])
            self.assertNotIn(MODIFIER, rt.chiefly['modifiers'])
        self.assertNotIn(MODIFIER, rt.royal['modifiers'])
        self.assertEqual({}, rt.scopes['root']['vars'])

    def test_both_split_orientations_route_to_the_actual_royal_movement(self):
        for rebel_alignment in (1,2):
            rt = PressureCourt()
            rt.country['vars'].update({ROYAL:200, CHIEFLY:100})
            rebel = dict(id='rebel', alive=True, vars={ROYAL:350, CHIEFLY:80,
                         'sb_court_war_alignment_var':rebel_alignment})
            rebel['movements'] = [movement(rebel)]
            rt.state['vars']['sb_chiefs_rebels_scope'] = rebel
            rt.royal['modifiers'][MODIFIER] = .1
            rt.update()
            target = rebel['movements'][0] if rebel_alignment == 1 else rt.royal
            other = rt.royal if rebel_alignment == 1 else rebel['movements'][0]
            self.assertAlmostEqual(.25 if rebel_alignment == 1 else .12, target['modifiers'][MODIFIER])
            self.assertNotIn(MODIFIER, other['modifiers'])
            rebel['alive'] = False
            rt.update()
            self.assertAlmostEqual(.1, rt.royal['modifiers'][MODIFIER])
            self.assertNotIn(MODIFIER, rebel['movements'][0]['modifiers'])

    def test_cleanup_runs_before_losing_country_handles_and_is_repeat_safe(self):
        rt = PressureCourt(); rt.country['vars'].update({ROYAL:358,CHIEFLY:100})
        rt.update()
        for _ in range(2): rt.effect(SETTLEMENT['sb_zululand_cleanup_situation'], rt.scopes['root'])
        self.assertNotIn(MODIFIER, rt.royal['modifiers'])
        self.assertNotIn('sb_zululand_chiefdoms_state', rt.containers)
        rt.update()
        self.assertNotIn(MODIFIER, rt.royal['modifiers'])

    def test_missing_movement_or_backing_does_not_create_state(self):
        rt = PressureCourt(); rt.update()
        self.assertNotIn(MODIFIER, rt.royal['modifiers'])
        rt.country['vars'].update({ROYAL:358,CHIEFLY:100})
        rt.country['movements'] = []
        rt.update()
        self.assertEqual([], rt.country['movements'])

    def test_transferred_house_is_not_counted_in_both_courts(self):
        royal = character('royal head',18,80,alignment=1)
        chief = character('chiefly head',9,100,alignment=2)
        rt = PressureCourt([royal,chief])
        rebel = dict(id='rebel',alive=True,vars={'sb_court_war_alignment_var':1},
                     members=[royal],ruler=royal,movements=[])
        royal['owner'] = rebel
        royal['vars']['sb_court_home_scope'] = rebel
        rebel['movements'] = [movement(rebel)]
        rt.state['vars']['sb_chiefs_rebels_scope'] = rebel
        rt.backing()
        rt.effect(EFFECTS['sb_court_calculate_backing'],rebel)
        self.assertEqual(0,rt.country['vars'][ROYAL])
        self.assertEqual(100,rt.country['vars'][CHIEFLY])
        self.assertEqual(80,rebel['vars'][ROYAL])
        self.assertEqual(0,rebel['vars'][CHIEFLY])
        self.assertAlmostEqual(-.02,rebel['movements'][0]['modifiers'][MODIFIER])

    def test_alignment_change_updates_pressure_without_changing_actual_activism(self):
        royal = character('royal head',18,80,alignment=1)
        chief = character('chiefly head',9,100,alignment=2)
        rt = PressureCourt([royal,chief]);rt.royal['political_movement_radicalism'] = .6
        rt.backing()
        self.assertAlmostEqual(-.02,rt.royal['modifiers'][MODIFIER])
        rt.effect(EFFECTS['sb_court_align_royal'],chief)
        rt.backing()
        self.assertAlmostEqual(.18,rt.royal['modifiers'][MODIFIER])
        self.assertEqual(.6,rt.royal['political_movement_radicalism'])


class NatalReturnAITests(unittest.TestCase):
    def test_dynamic_order_and_live_radical_recheck(self):
        rt = ReconciliationContest()
        rt.nal['radical_fractions'] = {'cu:zulu':.2}
        rt.claimant.update(owner=rt.zul, alive=True)
        claimant = 'sb_zululand_reconciliation_ai_chance'; refugees = 'sb_zululand_refugee_ai_chance'
        self.assertEqual(25, calculate(rt, claimant, rt.nal))
        self.assertEqual(0, calculate(rt, refugees, rt.nal))
        rt.nal['vars']['sb_zululand_claimant_returned_var'] = 1
        self.assertEqual(0, calculate(rt, refugees, rt.nal))  # Old country receipt is insufficient.
        rt.nal['sb_chiefs_royal_house'] = [rt.claimant]
        self.assertEqual(25, calculate(rt, refugees, rt.nal))
        rt.nal['radical_fractions']['cu:zulu'] = .1999
        self.assertEqual(0, calculate(rt, claimant, rt.nal))
        self.assertEqual(0, calculate(rt, refugees, rt.nal))
        rt.nal['radical_fractions']['cu:zulu'] = .2
        rt.claimant['owner'] = rt.britain
        self.assertEqual(0, calculate(rt, refugees, rt.nal))
        rt.claimant['owner'] = rt.zul
        rt.claimant['is_in_exile_pool'] = True
        self.assertEqual(0, calculate(rt, refugees, rt.nal))

    def test_natal_zulu_population_strict_delay_and_off(self):
        rt = ReconciliationContest()
        rt.zul['radical_fractions'] = {'cu:zulu':.9}
        rt.trn['radical_fractions'] = {'cu:zulu':.9}
        rt.nal['radical_fractions'] = {'cu:boer':.9,'cu:zulu':.1}
        for value in ('sb_zululand_reconciliation_ai_chance','sb_zululand_refugee_ai_chance'):
            self.assertEqual(0, calculate(rt,value,rt.nal))
            self.assertEqual(0, calculate(rt,value,rt.trn))
            rt.mode = 'sb_frontier_ai_behavior_strict_historical'
            rt.journal['journal_entry_age'] = 1094
            self.assertEqual(0, calculate(rt,value,rt.nal))
            rt.journal['journal_entry_age'] = 1095
            self.assertEqual(25, calculate(rt,value,rt.nal))
            rt.mode = 'sb_frontier_ai_behavior_off'
            rt.nal['radical_fractions']['cu:zulu'] = .9
            self.assertEqual(0, calculate(rt,value,rt.nal))
            rt.mode = 'sb_frontier_ai_behavior_dynamic_historical'
            rt.nal['radical_fractions']['cu:zulu'] = .1


if __name__ == '__main__': unittest.main()
