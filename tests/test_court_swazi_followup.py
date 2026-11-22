"""Execute event draws, exact-play goal eligibility and repeated mobilisation."""
from collections import Counter
from pathlib import Path
import unittest

from tests.test_zulu_court_event_package import setup, fields, EventRuntime
from tests.test_zulu_court_politics import EFFECTS, definitions
from tests.test_zulu_institutions_laws import GAME, statements
from tools.check_override_inventory import find_object

ROOT = Path(__file__).resolve().parents[1]
SWAZI = definitions('common/scripted_triggers/sb_swazi_triggers.txt')
NATALIA = {'sb_ensure_ora_ai_natal_front_commitment': statements(find_object(
    (ROOT / 'common/scripted_effects/sb_natalia_effects.txt').read_text(encoding='utf-8-sig'),
    'sb_ensure_ora_ai_natal_front_commitment'))}


def pick(rt, alternate=False):
    destination = 'sb_court_episode_other_candidate_scope' if alternate else 'sb_court_episode_candidate_scope'
    rt.effect(statements('effect = { sb_court_pick_episode_prince = { DESTINATION = '
                         + destination + ' EXCLUDE_FIRST = ' + ('yes' if alternate else 'no') + ' } }'), rt.country)
    return rt.country['vars'].get(destination)


class PopularityDraws(unittest.TestCase):
    def test_integer_weight_draw_uses_relative_popularity_without_list_order_bias(self):
        for first_q, second_q, expected in ((0, 100, 1/3), (-50, 50, 1/4), (25, 0, 5/9), (0, 0, 1/2)):
            for reverse in (False, True):
                with self.subTest(popularity=(first_q, second_q), reverse=reverse):
                    rt, king, p, r, chiefs = setup()
                    p['popularity'], r['popularity'] = first_q, second_q
                    if reverse:
                        rt.country['members'].reverse()
                    picked = 0
                    # Integrate the last reservoir draw across evenly spaced quantiles.
                    for i in range(360):
                        rt.rolls = [0, (i + .5) / 360]
                        picked += pick(rt) is p
                    self.assertAlmostEqual(expected, picked / 360, delta=1/360)
                    self.assertNotIn('sb_court_episode_draw_weight_var', rt.country['vars'])
                    self.assertEqual({}, rt.scopes['root']['vars'])  # Foreign event ROOT.

    def test_zero_weights_fallback_exclusion_and_missing_candidate(self):
        rt, king, p, r, chiefs = setup()
        p['popularity'], r['popularity'] = -100, 0
        for _ in range(20):
            self.assertIs(r, pick(rt))
            self.assertIs(p, pick(rt, alternate=True))
            self.assertIs(r, rt.country['vars']['sb_court_episode_candidate_scope'])
        r['popularity'] = -100
        seen = Counter(pick(rt)['id'] for _ in range(100))
        self.assertEqual({p['id'], r['id']}, set(seen))
        p['alive'] = False
        r['age'] = 15
        self.assertIsNone(pick(rt))
        self.assertIsNone(pick(rt, alternate=True))

    def test_both_episode_destinations_are_weighted_and_preview_does_not_reroll(self):
        for card in (210, 214):
            rt, king, p, r, chiefs = setup()
            chiefs[0]['vars']['sb_court_endorsement_var'] = 1
            p['popularity'], r['popularity'] = -100, 100
            rt.country['vars'].update(sb_court_deck_card_var=card, sb_court_episode_card_var=card,
                                      sb_court_episode_open_var=1, sb_court_episode_ruler_scope=king)
            rt.effect(EFFECTS['sb_court_deck_deliver'], rt.country)
            self.assertIs(r, rt.country['vars']['sb_court_episode_candidate_scope'])
            if card == 210:
                self.assertIs(p, rt.country['vars']['sb_court_episode_other_candidate_scope'])
            rt.fire(card)
            p['popularity'], r['popularity'] = 100, -100
            if card == 214:
                loser = rt.country['vars']['sb_court_episode_other_scope']
                self.assertTrue(rt.answer(card, 'a'))
                self.assertIs(r, loser['vars']['sb_court_claimant_scope'])
            else:
                self.assertIs(r, rt.scopes['sb_court_episode_candidate'])

    def test_existing_patron_and_incumbent_episodes_do_not_choose_another_prince(self):
        rt, king, p, r, chiefs = setup()
        chiefs[0]['vars']['sb_court_endorsement_var'] = 1
        chiefs[1]['vars'].update(sb_court_endorsement_var=-1, sb_court_claimant_scope=p)
        p['popularity'], r['popularity'] = -100, 100
        for card, expected in ((212, king), (213, p)):
            rt.country['vars']['sb_court_deck_card_var'] = card
            rt.effect(EFFECTS['sb_court_deck_deliver'], rt.country)
            self.assertIs(expected, rt.country['vars']['sb_court_episode_candidate_scope'])


class FrontierRuntime(EventRuntime):
    def ref(self, key, scope, prev=None):
        if key == 'root':
            return self.scopes['root']
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        results = []
        for key, op, value in nodes:
            if key in ('is_army', 'is_mobilized', 'is_at_war'):
                results.append(scope.get(key, False) == (value == 'yes'))
            elif key in ('initiator_is', 'target_is'):
                results.append(scope[key.removesuffix('_is')] is self.ref(value, scope, prev))
            elif key == 'is_diplomatic_play_type':
                results.append(scope['type'] == value)
            else:
                results.append(super().condition([(key, op, value)], scope, prev))
        return all(results)

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, op, value = node
            if key == 'every_military_formation':
                for formation in scope['formations']:
                    if self.condition(fields(value)['limit'], formation, scope):
                        self.effect([n for n in value if n[0] != 'limit'], formation, scope)
            elif key == 'fully_mobilize_army':
                if not scope['is_army'] or scope['is_mobilized']:
                    raise AssertionError('formation cannot be mobilised')
                scope['calls'] += 1
                scope['is_mobilized'] = True
            else:
                super().effect([node], scope, prev)


def frontier():
    rt = FrontierRuntime([])
    swz = {'id': 'SWZ', 'vars': {}}
    zul = {'id': 'ZUL', 'vars': {'sb_zulu_swazi_war_active_var': 1}}
    play = {'type': 'dp_conquer_state', 'initiator': zul, 'target': swz}
    swazi_state, zulu_state = {'id': 'SWZ state'}, {'id': 'ZUL state'}
    zul['vars'].update(sb_zulu_swazi_play_scope=play, sb_zulu_swazi_target_state_scope=swazi_state)
    rt.scopes.update(root=swz, diplomatic_play=play, target_country=zul, target_state=zulu_state)
    return rt, swz, zul, play, swazi_state


class SwaziGoalSelection(unittest.TestCase):
    def allowed(self, rt, holder):
        return rt.condition(SWAZI['sb_swazi_conquest_target_allowed'], holder)

    def test_blocks_added_conquest_but_preserves_native_territorial_recovery(self):
        for launch in (False, True):
            rt, swz, zul, play, swazi_state = frontier()
            if launch:
                zul['vars'].pop('sb_zulu_swazi_play_scope')
                zul['vars']['sb_zulu_swazi_launch_lease_var'] = 1
            self.assertFalse(self.allowed(rt, swz))
            rt.scopes['target_state'] = swazi_state
            self.assertTrue(self.allowed(rt, swz))

    def test_unrelated_plays_holders_targets_and_missing_scopes_remain_allowed(self):
        for case in ('other_play', 'other_holder', 'other_target', 'no_play', 'no_target', 'finished', 'no_markers'):
            with self.subTest(case=case):
                rt, swz, zul, play, state = frontier()
                holder = swz
                if case == 'other_play': rt.scopes['diplomatic_play'] = dict(play)
                elif case == 'other_holder': holder = {'id': 'GBR', 'vars': {}}
                elif case == 'other_target': rt.scopes['target_country'] = {'id': 'ORA', 'vars': {}}
                elif case == 'no_play': rt.scopes.pop('diplomatic_play')
                elif case == 'no_target': rt.scopes.pop('target_country')
                elif case == 'finished': zul['vars'].pop('sb_zulu_swazi_war_active_var')
                else: zul['vars'].clear()
                self.assertTrue(self.allowed(rt, holder))
        rt, swz, zul, play, state = frontier()
        rt.scopes.update(root=zul, target_country=swz, target_state=state)
        self.assertTrue(self.allowed(rt, zul))  # Zulu's primary conquest.

    def test_launch_lease_does_not_match_a_different_play(self):
        for field, value in (('type', 'dp_humiliation'), ('initiator', {'id': 'ORA'}), ('target', {'id': 'NAL'})):
            rt, swz, zul, play, state = frontier()
            zul['vars'].pop('sb_zulu_swazi_play_scope')
            zul['vars']['sb_zulu_swazi_launch_lease_var'] = 1
            play[field] = value
            self.assertTrue(self.allowed(rt, swz))

    def test_override_preserves_native_definition_apart_from_scoped_guards(self):
        self.assertIsNotNone(GAME)
        self.assertFalse((ROOT.parent / 'Community Mod Framework/common/war_goal_types/03_conquer_state.txt').exists())
        source = (GAME / 'common/war_goal_types/03_conquer_state.txt').read_text(encoding='utf-8-sig')
        override = find_object((ROOT / 'common/war_goal_types/zz_sb_swazi_conquest_override.txt').read_text(encoding='utf-8-sig'), 'conquer_state', directive='REPLACE')
        self.assertEqual(2, override.count('sb_swazi_conquest_target_allowed = yes'))
        stripped = override.replace('REPLACE:conquer_state', 'conquer_state', 1).replace('\n\t\tsb_swazi_conquest_target_allowed = yes', '')
        self.assertEqual(find_object(source, 'conquer_state'), stripped)


class MobilisationAndWarnings(unittest.TestCase):
    def test_monthly_retry_skips_mobilised_armies_and_navies(self):
        rt = FrontierRuntime([])
        country = rt.country
        country.update(id='ORA', is_ai=True, is_at_war=True)
        country['vars'].update(sb_natal_war_active_var=1, sb_ora_blood_river_force_floor_created_var=1)
        country['formations'] = [dict(is_army=army, is_mobilized=mobilised, calls=0) for army, mobilised in ((True, True), (True, False), (False, False))]
        for _ in range(3):
            rt.effect(NATALIA['sb_ensure_ora_ai_natal_front_commitment'], country)
        self.assertEqual([0, 1, 0], [f['calls'] for f in country['formations']])
        for field, value in (('id', 'NAL'), ('is_ai', False), ('is_at_war', False)):
            old = country[field]
            country[field] = value
            country['formations'][1]['is_mobilized'] = False
            rt.effect(NATALIA['sb_ensure_ora_ai_natal_front_commitment'], country)
            self.assertEqual([0, 1, 0], [f['calls'] for f in country['formations']])
            country[field] = old

    def test_ui_snapshots_remain_and_dead_cleanup_is_removed(self):
        self.assertNotIn('sb_court_play_rebels_var', (ROOT / 'common/scripted_effects/sb_court_actions_effects.txt').read_text())
        for variable, path in (('sb_court_annual_weight_var', 'sb_zulu_court_l_english.yml'), ('sb_court_pledged_share_var', 'sb_court_politics_l_english.yml')):
            self.assertIn("Var('" + variable + "')", (ROOT / 'localization/english' / path).read_text())


if __name__ == '__main__':
    unittest.main()
