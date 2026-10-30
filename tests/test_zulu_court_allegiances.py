"""Present allegiance and future pledges share prominence, not a denominator."""
from pathlib import Path
import unittest
from tests.test_zulu_court_politics import CourtRuntime, character, VALUES, EFFECTS
from tests.test_zulu_institutions_laws import statements, child
from tools.check_override_inventory import find_object

ROOT = Path(__file__).resolve().parents[1]


def divided_court():
    king = character('Dingane', 1, 50, 1, 1)
    prince = character('Mpande', 0, 25, -1, 1)  # 25 + 25 claimant = 50 in this balanced fixture
    prince['template'] = 'ZUL_mpande_zulu'
    prince['vars']['sb_court_claimant_scope'] = prince
    neutral = character('neutral house', 2, 100)
    loyalist = character('loyal house', 3, 50, 1)
    loyalist['vars']['sb_court_successor_pledge_scope'] = prince
    rt = CourtRuntime([king, prince, neutral, loyalist])
    rt.backing()
    return rt, king, prince, neutral, loyalist


class CourtAllegiances(unittest.TestCase):
    def test_king_and_supporters_are_currently_pledged_even_with_other_future_promises(self):
        rt, king, prince, neutral, loyalist = divided_court()
        for _ in range(3):
            rt.backing()
            self.assertEqual(250, rt.country['vars']['sb_court_weight_var'])
            self.assertEqual(150, rt.country['vars']['sb_court_current_pledged_weight_var'])
            self.assertEqual(100, rt.country['vars']['sb_court_current_unpledged_weight_var'])
            self.assertEqual(100, king['vars']['sb_court_current_weight_var'])
            self.assertEqual(50, prince['vars']['sb_court_current_weight_var'])
            self.assertEqual([loyalist], king['sb_court_current_supporters'])
            self.assertEqual([], prince['sb_court_current_supporters'])
            self.assertEqual([loyalist], prince['sb_court_supporters'])
            self.assertEqual(100, prince['vars']['sb_court_coalition_weight_var'])
            self.assertEqual(100, rt.country['vars']['sb_court_pledged_weight_var'])
            self.assertEqual(150, rt.country['vars']['sb_court_unpledged_weight_var'])
            self.assertAlmostEqual(100, sum(p['vars']['sb_court_current_share_var'] for p in (king, prince)))
            self.assertEqual(100, prince['vars']['sb_court_pledged_share_var'])
            self.assertEqual({}, rt.scopes['root']['vars'])

    def test_quarter_discount_only_affects_present_backing_and_keeps_popularity_separate(self):
        rt, king, prince, neutral, loyalist = divided_court()
        self.assertEqual(175, rt.calc(VALUES['sb_court_backing_denominator'], rt.country))
        self.assertAlmostEqual(200 / 7, rt.country['vars']['sb_prerogative_cooperation_var'])
        king['popularity'] = 40
        rt.backing()
        self.assertAlmostEqual(200 / 7 + 20, rt.country['vars']['sb_prerogative_cooperation_var'])
        neutral['vars']['sb_court_successor_pledge_scope'] = prince
        rt.backing()
        self.assertEqual(200, rt.country['vars']['sb_court_pledged_weight_var'])
        self.assertEqual(100, rt.country['vars']['sb_court_current_unpledged_weight_var'])
        self.assertAlmostEqual(200 / 7 + 20, rt.country['vars']['sb_prerogative_cooperation_var'])
        loyalist['vars']['sb_court_endorsement_var'] = 0
        rt.backing()
        self.assertEqual(150, rt.country['vars']['sb_court_current_unpledged_weight_var'])
        self.assertEqual(20, rt.country['vars']['sb_prerogative_cooperation_var'])

    def test_house_members_contribute_once_through_current_head(self):
        rt, king, prince, neutral, loyalist = divided_court()
        junior = character('junior', 3, 30, -1)
        junior['vars'].update(sb_court_claimant_scope=prince, sb_court_home_scope=rt.country)
        junior['owner'] = rt.country
        rt.country['members'].append(junior)
        rt.backing()
        self.assertEqual(70, loyalist['vars']['sb_court_represented_weight_var'])
        self.assertEqual(120, king['vars']['sb_court_current_weight_var'])
        self.assertEqual([loyalist], king['sb_court_current_supporters'])
        self.assertEqual(50, prince['vars']['sb_court_current_weight_var'])
        self.assertEqual(270, rt.country['vars']['sb_court_weight_var'])
        junior['prominence'] = 60
        rt.backing()
        self.assertEqual(100, junior['vars']['sb_court_represented_weight_var'])
        self.assertEqual(50, king['vars']['sb_court_current_weight_var'])
        self.assertEqual(150, prince['vars']['sb_court_current_weight_var'])
        self.assertEqual([junior], prince['sb_court_current_supporters'])

    def test_dead_claimants_and_exiled_followings_reconcile_without_stale_lists(self):
        rt, king, prince, neutral, loyalist = divided_court()
        loyalist['vars'].update(sb_court_endorsement_var=-1, sb_court_claimant_scope=prince)
        prince['owner'] = {'id': 'CAP'}
        rt.backing()
        self.assertEqual(100, prince['vars']['sb_court_current_weight_var'])
        self.assertEqual([loyalist], prince['sb_court_current_supporters'])
        self.assertAlmostEqual(-200 / 7, rt.country['vars']['sb_prerogative_cooperation_var'])
        prince['alive'] = False
        rt.backing()
        self.assertEqual(0, prince['vars']['sb_court_current_weight_var'])
        self.assertEqual([], prince['sb_court_current_supporters'])
        self.assertEqual(50, rt.country['vars']['sb_court_current_pledged_weight_var'])
        self.assertEqual(150, rt.country['vars']['sb_court_current_unpledged_weight_var'])
        self.assertAlmostEqual(400 / 7, rt.country['vars']['sb_prerogative_cooperation_var'])

    def test_empty_neutral_and_full_opposition_boundaries(self):
        empty = CourtRuntime([])
        empty.backing()
        self.assertEqual(0, empty.country['vars']['sb_prerogative_cooperation_var'])
        rt = CourtRuntime([character('neutral', 1, 50)])
        rt.backing()
        self.assertEqual(0, rt.country['vars']['sb_court_current_pledged_weight_var'])
        self.assertEqual(0, rt.country['vars']['sb_prerogative_cooperation_var'])
        self.assertEqual(0, rt.country['ruler']['vars']['sb_court_current_share_var'])
        rt, king, prince, neutral, loyalist = divided_court()
        king['prominence'] = 0
        loyalist['alive'] = False
        neutral['alive'] = False
        king['popularity'] = -100
        rt.backing()
        self.assertEqual(-100, rt.country['vars']['sb_prerogative_cooperation_var'])

    def test_split_courts_do_not_overwrite_each_others_backing(self):
        rt, king, prince, neutral, loyalist = divided_court()
        loyalist['vars'].update(sb_court_endorsement_var=-1, sb_court_claimant_scope=prince)
        rebel = {'id': 'REV', 'vars': {}, 'ruler': prince, 'members': list(rt.country['members']), 'movements': []}
        prince['vars'].update(sb_court_home_scope=rebel, sb_court_endorsement_var=1)
        prince['owner'] = rebel
        for _ in range(3):
            rt.effect(EFFECTS['sb_court_calculate_backing'], rebel)
            rt.backing()
            self.assertEqual(100, rt.country['vars']['sb_court_current_pledged_weight_var'])
            self.assertEqual(50, rt.country['vars']['sb_court_external_opposition_var'])
            self.assertEqual(0, rt.country['vars']['sb_prerogative_cooperation_var'])
            self.assertEqual(25, prince['vars']['sb_court_current_weight_var'])
            self.assertEqual([], prince['sb_court_current_supporters'])
            self.assertEqual(25, rebel['vars']['sb_court_current_pledged_weight_var'])
            self.assertEqual(100, rebel['vars']['sb_prerogative_cooperation_var'])

    def test_current_view_includes_incumbent_and_rejects_foreign_and_minor_candidates(self):
        rt, king, prince, neutral, loyalist = divided_court()
        for actor in (king, prince):
            self.assertTrue(rt.roster_shown('sb_court_roster_allegiance', actor))
        for actor in (neutral, loyalist):
            self.assertFalse(rt.roster_shown('sb_court_roster_allegiance', actor))
        prince['vars']['sb_court_home_scope'] = rt.scopes['root']
        self.assertFalse(rt.roster_shown('sb_court_roster_allegiance', prince))
        prince['vars']['sb_court_home_scope'] = rt.country
        prince['age'] = 12
        rt.backing()
        self.assertFalse(rt.roster_shown('sb_court_roster_allegiance', prince))
        self.assertEqual(0, rt.country['vars']['sb_court_pledged_weight_var'])
        self.assertEqual(0, prince['vars']['sb_court_current_weight_var'])
        rt.country['vars']['sb_court_recognized_heir_scope'] = prince
        loyalist['vars']['sb_court_successor_pledge_scope'] = prince
        rt.backing()
        self.assertEqual(50, rt.country['vars']['sb_court_pledged_weight_var'])
        self.assertEqual(0, prince['vars']['sb_court_current_weight_var'])
        self.assertFalse(rt.roster_shown('sb_court_roster_allegiance', prince))


if __name__ == '__main__':
    unittest.main()
