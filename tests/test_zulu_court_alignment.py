"""Constitutional eligibility must not erase the court's separate personal commitments."""
import unittest

from tests.test_zulu_court_politics import ROOT, EFFECTS, TRIGGERS, character, definitions
from tests.test_zulu_court_rework import ReworkRuntime
from tests.test_zulu_institutions_laws import child, statements
from tools.check_override_inventory import find_object


EXCLUDED = ('ig_industrialists', 'ig_intelligentsia', 'ig_trade_unions')


def court(ideology='ideology_moderate', alignment=0, contest=False, ig='ig_landowners'):
    king = character('king', 1, 50, 1, 1)
    actor = character('chief', 2, 50, 1, alignment)
    actor.update(ideology=ideology, interest_group={'type': ig})
    rt = ReworkRuntime([king, actor])
    if contest:
        rt.country['journal_entries'] = {'je_sb_zululand_chiefdoms'}
    return rt, actor


class CourtAlignmentTests(unittest.TestCase):
    def test_excluded_igs_cannot_join_either_constitutional_faction(self):
        for ig in EXCLUDED:
            for helper in ('sb_court_align_royal', 'sb_court_align_chiefly'):
                with self.subTest(ig=ig, helper=helper):
                    rt, actor = court('ideology_royalist', contest=True, ig=ig)
                    rt.effect(EFFECTS[helper], actor)
                    self.assertEqual(0, actor['vars']['sb_court_alignment_var'])
                    self.assertEqual('ideology_royalist', actor['ideology'])
                    self.assertIn('sb_court_alignment_neutral_trait', actor['traits'])

    def test_new_ig_membership_clears_alignment_but_retains_personal_backing(self):
        for ig in EXCLUDED:
            rt, actor = court(alignment=1)
            prince = character('prince', 0, 40, -1, 1)
            prince.update(template='ZUL_mpande_zulu', owner=rt.country)
            prince['vars']['sb_court_home_scope'] = rt.country
            rt.country['members'].append(prince)
            actor['vars']['sb_court_successor_pledge_scope'] = prince
            rt.backing()
            before = rt.country['vars']['sb_court_incumbent_weight_var']
            actor['interest_group']['type'] = ig
            rt.backing()
            self.assertEqual(0, actor['vars']['sb_court_alignment_var'])
            self.assertEqual(1, actor['vars']['sb_court_endorsement_var'])
            self.assertIs(prince, actor['vars']['sb_court_successor_pledge_scope'])
            self.assertEqual(before, rt.country['vars']['sb_court_incumbent_weight_var'])
            self.assertIn('sb_court_alignment_neutral_trait', actor['traits'])

    def test_native_movement_membership_rejects_excluded_igs_before_monthly_refresh(self):
        movements = (ROOT/'common/political_movements/sb_zulu_constitutional_movements.txt').read_text(encoding='utf-8-sig')
        for side, alignment in (('royal', 1), ('chiefly', 2)):
            movement = find_object(movements, f'movement_sb_zulu_{side}')
            support = statements(child(movement, 'character_support_trigger'))
            rt, actor = court(alignment=alignment)
            self.assertTrue(rt.condition(support, actor))
            for ig in EXCLUDED:
                actor['interest_group']['type'] = ig
                self.assertFalse(rt.condition(support, actor))

    def test_excluded_dynast_keeps_claim_despite_neutral_alignment(self):
        rt, prince = court('ideology_royalist', alignment=1, ig='ig_industrialists')
        prince['template'] = 'ZUL_mpande_zulu'
        prince['vars'].update(sb_court_endorsement_var=-1, sb_court_claimant_scope=prince)
        rt.backing()
        self.assertEqual(0, prince['vars']['sb_court_alignment_var'])
        self.assertTrue(rt.condition(TRIGGERS['sb_court_dynastic_candidate'], prince))
        self.assertIn('sb_court_claimant_trait', prince['traits'])
        self.assertEqual(prince['prominence']+25,rt.ref('prominence',prince))

    def test_registration_and_annual_roll_respect_the_exclusion(self):
        for ig in EXCLUDED:
            rt, actor = court(ig=ig)
            rt.scopes['sb_court_country'] = rt.country
            rt.effect([('sb_court_register_character', '=', [
                ('FOLLOWING', '=', '2'), ('ALIGNMENT', '=', '1'), ('ENDORSEMENT', '=', '1')])], actor)
            self.assertEqual(0, actor['vars']['sb_court_alignment_var'])
            rt.country['movements'] = [{'type': 'movement_sb_zulu_royal', 'political_movement_support': 1}]
            rt.roll = 0  # Guaranteed royal result if this representative were allowed to roll.
            rt.effect(EFFECTS['sb_court_annual_alignment'], rt.country)
            self.assertEqual(0, actor['vars']['sb_court_alignment_var'])

    def test_other_igs_and_characters_without_an_ig_remain_eligible(self):
        for ig in ('ig_landowners', 'ig_armed_forces', 'ig_devout', 'ig_petty_bourgeoisie', 'ig_rural_folk', None):
            rt, actor = court(ig=ig)
            if ig is None:
                actor.pop('interest_group')
            rt.effect(EFFECTS['sb_court_align_chiefly'], actor)
            self.assertEqual(2, actor['vars']['sb_court_alignment_var'])
            self.assertEqual('ideology_moderate', actor['ideology'])

    def test_royalist_and_chiefist_follow_their_new_alignment(self):
        rt, actor = court('ideology_royalist', alignment=1)
        rt.effect(EFFECTS['sb_court_align_chiefly'], actor)
        self.assertEqual('ideology_sb_chiefist', actor['ideology'])
        rt.effect(EFFECTS['sb_court_align_royal'], actor)
        self.assertEqual('ideology_royalist', actor['ideology'])

    def test_moderate_conversion_requires_a_change_during_the_home_contest(self):
        for side, expected in (('royal', 'ideology_royalist'), ('chiefly', 'ideology_sb_chiefist')):
            for active in (False, True):
                rt, actor = court(contest=active)
                actor['owner'] = {'id': 'CAP', 'vars': {}}
                rt.scopes['root'] = {'id': 'NAL', 'vars': {}}
                rt.effect(EFFECTS[f'sb_court_align_{side}'], actor)
                self.assertEqual(expected if active else 'ideology_moderate', actor['ideology'])
            rt, actor = court(alignment=1 if side == 'royal' else 2, contest=True)
            rt.effect(EFFECTS[f'sb_court_align_{side}'], actor)
            self.assertEqual('ideology_moderate', actor['ideology'])

    def test_unrelated_ideologies_and_monthly_refresh_are_not_converted(self):
        for ideology in ('ideology_traditionalist', 'ideology_reformer', 'ideology_jingoist'):
            for side in ('royal', 'chiefly'):
                rt, actor = court(ideology, contest=True)
                rt.effect(EFFECTS[f'sb_court_align_{side}'], actor)
                rt.backing()
                self.assertEqual(ideology, actor['ideology'])
        rt, actor = court(alignment=2, contest=True)
        rt.backing()
        self.assertEqual('ideology_moderate', actor['ideology'])

    def test_neutral_chief_selection_skips_excluded_igs(self):
        rt, blocked = court(ig='ig_intelligentsia')
        rt.country['ruler']['vars']['sb_court_alignment_var'] = 1
        eligible = character('eligible', 3, 10)
        eligible.update(owner=rt.country, ideology='ideology_royalist')
        eligible['vars']['sb_court_home_scope'] = rt.country
        rt.country['members'].append(eligible)
        rt.effect(EFFECTS['sb_court_align_neutral_chiefly'], rt.country)
        self.assertEqual(0, blocked['vars']['sb_court_alignment_var'])
        self.assertEqual(2, eligible['vars']['sb_court_alignment_var'])
        foreign = definitions('common/scripted_triggers/sb_zululand_settlement_triggers.txt')['sb_zululand_neutral_chief']
        self.assertIn(('sb_court_alignment_eligible', '=', 'yes'), foreign)

    def test_chiefist_is_explicitly_assigned_and_matches_constitutional_stances(self):
        chiefist = definitions('common/ideologies/sb_court_character_ideologies.txt')['ideology_sb_chiefist']
        movement = definitions('common/ideologies/sb_zulu_constitutional_ideologies.txt')['ideology_sb_zulu_chiefly']
        self.assertIn(('character_ideology', '=', 'yes'), chiefist)
        self.assertIn(('country_trigger', '=', [('always', '=', 'no')]), chiefist)
        self.assertEqual([n for n in movement if n[0].startswith('lawgroup_')],
                         [n for n in chiefist if n[0].startswith('lawgroup_')])

    def test_chiefly_head_selection_rechecks_ig_before_cached_alignment(self):
        rt, blocked = court(alignment=2, ig='ig_intelligentsia')
        rt.country['laws'] = {'law_type:law_sb_federated_chiefdoms'}
        rt.country['vars']['sb_court_chiefly_head_scope'] = blocked
        eligible = character('eligible', 3, 10, 0, 2)
        eligible.update(owner=rt.country)
        eligible['vars']['sb_court_home_scope'] = rt.country
        rt.country['members'].append(eligible)
        rt.effect(EFFECTS['sb_court_select_chiefly_head'], rt.country)
        self.assertIs(eligible, rt.country['ruler'])
        self.assertIs(eligible, rt.country['vars']['sb_court_chiefly_head_scope'])


if __name__ == '__main__':
    unittest.main()
