"""Persistent branches and foreign quotes execute the shipped effects and values."""
import unittest
from unittest.mock import patch
from tests.test_zulu_court_rework import ReworkRuntime
from tests.test_zulu_court_politics import character, definitions, EFFECTS, ACTIONS, TRIGGERS as COURT_TRIGGERS
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import find_object
from tests.test_chiefdoms_refinement import ROOT, source

VALUES = definitions('common/script_values/sb_zululand_drift_values.txt')
SETTLEMENT = definitions('common/scripted_effects/sb_zululand_settlement_effects.txt')
TRIGGERS = definitions('common/scripted_triggers/sb_zululand_settlement_triggers.txt')


class BribeRuntime(ReworkRuntime):
    def ref(self, key, scope, prev=None):
        if key in VALUES:
            return self.calc(VALUES[key], scope, prev)
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        if len(nodes) == 1:
            key, op, value = nodes[0]
            if key == 'sb_zululand_contest_interventions_available':
                # Exact pact/territory/lifecycle is executed in test_chiefdoms_refinement.
                return self.interventions == (value == 'yes')
            if key in ('sb_zululand_can_bribe_chief', 'sb_zululand_neutral_chief'):
                return self.condition(TRIGGERS[key], scope, prev) == (value == 'yes')
        if len(nodes) > 1:
            return all(self.condition([n], scope, prev) for n in nodes)
        return super().condition(nodes, scope, prev)

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, _, value = node
            if key in ('sb_zululand_offer_chief_bribe', 'sb_zululand_close_bribe_offer'):
                self.effect(SETTLEMENT[key], scope, prev)
            else:
                super().effect([node], scope, prev)


class HousesAndPrices(unittest.TestCase):
    def test_institutional_exit_keeps_partition_cards_but_cleans_old_court_actions(self):
        king = character('king', 15, 40, 1, 1)
        actor = character('prince', 18, 30, -1, 1)
        actor['traits'] = {'sb_court_claimant_trait'}
        actor['modifiers'] = {'sb_court_junior_status': 1}
        rt = ReworkRuntime([king, actor])
        rt.country['vars'].update(sb_court_action_open_var=1, sb_court_accession_open_var=1,
                                 sb_court_owns_heir_blocker_var=1, no_heirs=1)
        with patch.dict(COURT_TRIGGERS, {'sb_chiefs_contest_country': [('always', '=', 'yes')]}):
            rt.effect(ACTIONS['sb_court_suspend'], rt.country)
        self.assertIn('sb_court_claimant_trait', actor['traits'])
        self.assertIn('sb_court_junior_status', actor['modifiers'])
        for key in ('sb_court_action_open_var', 'sb_court_accession_open_var', 'no_heirs'):
            self.assertNotIn(key, rt.country['vars'])

    def test_authored_branches_leave_other_houses_and_unaffiliated_members_intact(self):
        cases = [('ZUL_dingane', 15), ('ZUL_uthumbu_claimed_son', 15),
                 ('ZUL_mpande_zulu', 16), ('ZUL_gqugqu_claimant', 17),
                 ('ZUL_cetshwayo_heir', 18), ('ZUL_dinuzulu_heir', 18),
                 ('ZUL_solomon_heir', 18), ('ZUL_mbuyazi_heir', 19),
                 ('ZUL_mbuyazi_successor', 19)]
        for template, expected in cases:
            actor = character(template, 0, 30)
            actor['template'] = template
            rt = ReworkRuntime([actor])
            rt.effect(EFFECTS['sb_court_assign_authored_house'], actor)
            self.assertEqual(expected, actor['vars']['sb_court_following_var'])
        for original in range(15):
            actor = character('unlisted', original, 30)
            rt = ReworkRuntime([actor])
            rt.effect(EFFECTS['sb_court_assign_authored_house'], actor)
            self.assertEqual(original, actor['vars']['sb_court_following_var'])

    def test_kingship_does_not_reassign_branch_or_duplicate_junior_candidate_weight(self):
        king = character('Dingane', 15, 40, 1, 1)
        prince = character('Cetshwayo', 18, 80, -1, 1)
        junior = character('Dinuzulu', 18, 15, -1, 1)
        prince['template'], junior['template'] = 'ZUL_cetshwayo_heir', 'ZUL_dinuzulu_heir'
        prince['vars']['sb_court_claimant_scope'] = prince
        junior['vars']['sb_court_claimant_scope'] = junior
        rt = ReworkRuntime([king, prince, junior])
        rt.backing()
        self.assertEqual(175, rt.country['vars']['sb_court_weight_var'])
        self.assertEqual(135, prince['vars']['sb_court_coalition_weight_var'])
        self.assertEqual(0, junior['vars']['sb_court_coalition_weight_var'])
        self.assertEqual([junior], prince['sb_court_house_members'])
        for ruler in (prince, king, prince):
            rt.country['ruler'] = ruler
            rt.backing()
            self.assertEqual([15, 18, 18], [a['vars']['sb_court_following_var'] for a in (king, prince, junior)])

    def test_junior_contender_is_never_on_both_sides_of_reserved_dynastic_war(self):
        king = character('king', 15, 40, 1, 1)
        head = character('head', 18, 80, 1, 1)
        rival = character('rival', 18, 15, -1, 1)
        rival['template'] = 'ZUL_dinuzulu_heir'
        rival['vars']['sb_court_claimant_scope'] = rival
        rt = ReworkRuntime([king, head, rival])
        rt.country['vars'].update(sb_court_dynastic_nominee_scope=king,
                                 sb_court_dynastic_rival_scope=rival,
                                 sb_court_dynastic_reason_var=1)
        rt.effect(EFFECTS['sb_court_snapshot_dynastic_coalitions'], rt.country)
        self.assertIn(rival, rt.country['sb_court_dynastic_rival_members'])
        self.assertFalse(any(a is rival for a in rt.country['sb_court_dynastic_incumbent_members']))
        self.assertEqual(0, rt.country['vars']['sb_court_dynastic_rival_weight_var'])

    def quote(self, q=50, payer_id='NAL'):
        king = character('king', 15, 40, 1, 1)
        head = character('chief', 2, q)
        rt = BribeRuntime([king, head])
        rt.interventions = True
        rt.global_vars['sb_zululand_live_zul_scope'] = rt.country
        rt.country['gold_reserves_limit'] = 900000
        rt.backing()
        payer = dict(id=payer_id, vars={}, gold_reserves_limit=100000, gold_reserves=2000)
        rt.effect([('sb_zululand_offer_chief_bribe', '=', 'yes')], payer)
        return rt, payer, head

    def confirm(self, rt, payer):
        event = statements(find_object(source('events/sb_zululand_settlement_events.txt'), 'sb_zululand_settlement.116'))
        option = next(v for k, _, v in event if k == 'option')
        rt.effect(next(v for k, _, v in option if k == 'hidden_effect'), payer)

    def test_foreign_quote_uses_actual_payer_capacity_and_half_curve(self):
        for q, ratio in [(10, .2), (25, .3125), (50, .5), (75, .65), (100, .8)]:
            rt, payer, head = self.quote(q)
            self.assertAlmostEqual(100000*ratio, payer['vars']['sb_zululand_bribe_cost_var'])
            self.assertIs(head, payer['vars']['sb_zululand_bribe_target_scope'])
            self.assertEqual({}, rt.scopes['root']['vars'])

    def test_quote_is_frozen_debt_allowed_and_only_constitution_changes(self):
        for payer_id, alignment in [('NAL', 2), ('TRN', 1)]:
            rt, payer, head = self.quote(payer_id=payer_id)
            original_endorsement = head['vars']['sb_court_endorsement_var']
            payer['gold_reserves_limit'] = 999999
            head['prominence'] = 95
            self.confirm(rt, payer)
            self.assertEqual(-48000, payer['gold_reserves'])
            self.assertEqual(alignment, head['vars']['sb_court_alignment_var'])
            self.assertEqual(original_endorsement, head['vars']['sb_court_endorsement_var'])
            self.confirm(rt, payer)
            self.assertEqual(-48000, payer['gold_reserves'])

    def test_dead_aligned_or_unavailable_quote_never_charges(self):
        for invalid in ('dead', 'aligned', 'closed'):
            rt, payer, head = self.quote()
            if invalid == 'dead': head['alive'] = False
            elif invalid == 'aligned': head['vars']['sb_court_alignment_var'] = 1
            else: rt.interventions = False
            self.confirm(rt, payer)
            self.assertEqual(2000, payer['gold_reserves'])
            self.assertNotIn('sb_zululand_bribe_open_var', payer['vars'])


if __name__ == '__main__': unittest.main()
