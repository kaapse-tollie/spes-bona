"""Hamu's signed promise across the actual constitutional-war handoff.

Execute the shipped territorial predicates, accession receipt and war resolver.
Native revolution selection, subject conversion and wider situation cleanup are
fixture boundaries; these checks do not establish engine callback ordering.
"""
import unittest

from tests.test_zulu_later_court import LaterCourtRuntime, PROVINCES
from tests.test_zulu_court_politics import definitions
from tests.test_zulu_frontier_followup import field


WAR = definitions('common/scripted_effects/sb_court_constitutional_war_effects.txt')
SETTLEMENT = definitions('common/scripted_effects/sb_zululand_settlement_effects.txt')


class ConstitutionalContractRuntime(LaterCourtRuntime):
    def __init__(self, royal_rebels=False, contest=True):
        self.contest = False  # Parent setup recalculates the court before partition exists.
        super().__init__()
        self.accept()
        self.contest = contest
        self.rebel = {'id': 'R01', 'alive': True, 'vars': {}, 'members': [],
                      'movements': [], 'states': [], 'ruler': self.cetshwayo}
        self.royal, self.chiefs = ((self.rebel, self.country) if royal_rebels
                                   else (self.country, self.rebel))
        for side, opponent, alignment in ((self.royal, self.chiefs, 1),
                                           (self.chiefs, self.royal, 2)):
            side['vars'].update(sb_court_civil_war_var=opponent,
                                sb_court_war_alignment_var=alignment,
                                sb_institutions_zulu_profile_var=1)
            if contest:
                side['vars']['sb_zululand_usuthu_contest_var'] = 1
        self.royal['vars']['sb_court_restoration_claimant_scope'] = self.hamu
        self.royal['ruler'] = self.hamu
        self.hamu['owner'] = self.royal
        self.hamu['vars']['sb_court_home_scope'] = self.royal
        for i, province in enumerate(PROVINCES):
            self.provinces[province]['state']['owner'] = self.royal if i < 3 else self.chiefs

    def condition(self, nodes, scope, prev=None):
        for node in nodes:
            key, _, value = node
            if key == 'sb_zululand_chiefdoms_situation_active':
                result = self.contest == (value == 'yes')
            else:
                result = super().condition([node], scope, prev)
            if not result:
                return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, _, value = node
            if key in WAR:
                self.effect(WAR[key], scope, prev)
            elif key in ('sb_zululand_resolve_royal_contest', 'sb_zululand_resolve_chiefly_contest',
                         'sb_zululand_finalize_political_contest'):
                self.effect(SETTLEMENT[key], scope, prev)
            elif key in ('sb_institutions_reconcile', 'sb_institutions_recalculate',
                         'sb_zululand_apply_post_annex_incorporation', 'change_subject_type'):
                pass  # Institutional modifiers and NAL rewards are independently tested.
            elif key == 'sb_zululand_cleanup_situation':
                self.contest = False
            elif key == 'every_scope_state':
                for state in scope['states']:
                    if self.condition(field(value, 'limit'), state, scope):
                        self.effect([n for n in value if n[0] != 'limit'], state, scope)
            elif key == 'create_diplomatic_pact' and field(value, 'type') == 'puppet':
                self.ref(field(value, 'country'), scope, prev)['overlord'] = scope
            else:
                super().effect([node], scope, prev)

    def win(self):
        # Separate native callbacks must not share temporary saved scopes.
        self.scopes = {'root': self.countries['c:GBR'], 'target': self.chiefs}
        self.effect(WAR['sb_court_record_war_end'], self.royal)
        self.scopes = {'root': self.countries['c:GBR']}
        self.effect(WAR['sb_court_resolve_won_war'], self.royal)


class HamuConstitutionalSettlementTests(unittest.TestCase):
    def test_both_faction_orientations_keep_signed_promise_without_earning_it(self):
        for royal_rebels in (False, True):
            with self.subTest(royal_rebels=royal_rebels):
                rt = ConstitutionalContractRuntime(royal_rebels)
                rt.run('sb_hamu_contract_monthly', rt.sponsor)
                self.assertNotIn('sb_hamu_failed_var', rt.sponsor['vars'])
                self.assertNotIn('sb_hamu_earned_var', rt.sponsor['vars'])
                self.assertIn('sb_hamu_promise_live_var', rt.global_vars)
                self.assertNotIn('c:NRP', rt.countries)

    def test_foreign_or_unrelated_rebel_owner_still_invalidates_each_province(self):
        for province in PROVINCES:
            for unrelated_rebel in (False, True):
                with self.subTest(province=province, unrelated_rebel=unrelated_rebel):
                    rt = ConstitutionalContractRuntime()
                    foreign = rt.countries['c:NAL']
                    if unrelated_rebel:
                        foreign['vars']['sb_court_civil_war_var'] = rt.sponsor
                    rt.provinces[province]['state']['owner'] = foreign
                    rt.run('sb_hamu_contract_monthly', rt.sponsor)
                    self.assertIn('sb_hamu_failed_var', rt.sponsor['vars'])
                    self.assertNotIn('sb_hamu_promise_live_var', rt.global_vars)

    def test_actual_win_retains_exact_loser_until_reunion_and_cedes_once(self):
        for royal_rebels in (False, True):
            for contest in (False, True):
                with self.subTest(royal_rebels=royal_rebels, contest=contest):
                    rt = ConstitutionalContractRuntime(royal_rebels, contest)
                    rt.win()
                    self.assertIn('sb_hamu_earned_var', rt.sponsor['vars'])
                    self.assertIs(rt.royal, rt.sponsor['vars']['sb_hamu_court_scope'])
                    self.assertIs(rt.chiefs, rt.sponsor['vars']['sb_hamu_reunion_scope'])
                    for side in (rt.royal, rt.chiefs):
                        for name in ('sb_court_civil_war_var', 'sb_court_war_ended_var', 'sb_court_war_alignment_var'):
                            self.assertNotIn(name, side['vars'])
                    # Native removal can precede the last ownership update.
                    rt.chiefs['alive'] = False
                    rt.run('sb_hamu_contract_monthly', rt.sponsor)
                    self.assertNotIn('sb_hamu_failed_var', rt.sponsor['vars'])
                    self.assertNotIn('c:NRP', rt.countries)
                    # A repeated accession/war callback must preserve the captured loser.
                    rt.run('sb_hamu_record_accession', rt.royal)
                    rt.win()
                    self.assertIs(rt.chiefs, rt.sponsor['vars']['sb_hamu_reunion_scope'])
                    for province in PROVINCES:
                        rt.provinces[province]['state']['owner'] = rt.royal
                    rt.run('sb_hamu_contract_monthly', rt.sponsor)
                    rt.run('sb_hamu_contract_monthly', rt.sponsor)
                    self.assertIn('sb_hamu_fulfilled_var', rt.sponsor['vars'])
                    self.assertEqual(1, rt.sponsor['events'].count('sb_hamu_bargain.003'))
                    self.assertTrue(all(rt.provinces[p]['state']['owner'] is rt.countries['c:NRP'] for p in PROVINCES))
                    self.assertEqual({}, rt.countries['c:GBR']['vars'])

    def test_earned_receipt_does_not_excuse_real_loss_after_war(self):
        for province in PROVINCES:
            with self.subTest(province=province):
                rt = ConstitutionalContractRuntime(royal_rebels=True)
                rt.win()
                rt.provinces[province]['state']['owner'] = rt.countries['c:NAL']
                rt.run('sb_hamu_contract_monthly', rt.sponsor)
                self.assertIn('sb_hamu_failed_var', rt.sponsor['vars'])
                self.assertNotIn('c:NRP', rt.countries)

    def test_later_conflict_cannot_replace_earned_reunion_identity(self):
        for marker in ('sb_court_civil_war_var', 'sb_court_dynastic_opponent_scope'):
            with self.subTest(marker=marker):
                rt = ConstitutionalContractRuntime()
                rt.win()
                rt.royal['vars'][marker] = rt.countries['c:NAL']
                rt.run('sb_hamu_record_accession', rt.royal)
                self.assertIs(rt.chiefs, rt.sponsor['vars']['sb_hamu_reunion_scope'])
                rt.provinces[PROVINCES[-1]]['state']['owner'] = rt.countries['c:NAL']
                rt.run('sb_hamu_contract_monthly', rt.sponsor)
                self.assertIn('sb_hamu_failed_var', rt.sponsor['vars'])

    def test_unmatched_end_callback_or_another_king_cannot_earn_hamus_promise(self):
        rt = ConstitutionalContractRuntime()
        rt.scopes['target'] = rt.countries['c:NAL']
        rt.effect(WAR['sb_court_record_war_end'], rt.royal)
        rt.effect(WAR['sb_court_resolve_won_war'], rt.royal)
        self.assertNotIn('sb_hamu_earned_var', rt.sponsor['vars'])
        rt.royal['vars']['sb_court_restoration_claimant_scope'] = rt.cetshwayo
        rt.win()
        self.assertNotIn('sb_hamu_earned_var', rt.sponsor['vars'])
        self.assertNotIn('sb_hamu_reunion_scope', rt.sponsor['vars'])


if __name__ == '__main__':
    unittest.main()
