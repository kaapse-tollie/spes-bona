"""Source comparisons for the 1850 fixes, not an emulation of engine UI/timers."""
from itertools import product
from pathlib import Path
import operator
import unittest

from tests.test_zulu_institutions_laws import statements, GAME
from tests.test_court_swazi_followup import FrontierRuntime, SWAZI
from tools.check_override_inventory import find_object

ROOT = Path(__file__).resolve().parents[1]
OLD = statements((ROOT / 'Docs/compatibility/evidence/1_15_0_playtest_1850_fixes_2026_11_07/cape_completion_before.txt').read_text())


def definition(path, key):
    return statements(find_object((ROOT / path).read_text(encoding='utf-8-sig'), key))


def fields(nodes):
    return {k: v for k, _, v in nodes}


def condition(nodes, case):
    results = []
    for key, op, value in nodes:
        if key == 'text': continue
        if key == 'OR': result = any(condition([n], case) for n in value)
        elif key == 'NOT': result = not any(condition([n], case) for n in value)
        elif key in ('AND', 'hidden_trigger', 'custom_tooltip', 'scope:journal_entry', 'c:XHO'):
            result = condition(value, case)
        elif key == 'has_variable': result = value in case['variables']
        elif key == 'has_law': result = case['law']
        elif key == 'is_country_alive': result = case['xhosa_alive']
        elif key == 'has_modifier': result = True
        elif key == 'game_date': result = {'<': operator.lt, '>=': operator.ge}[op](case['date'], value)
        elif key == '"scripted_bar_progress(sb_cape_balance_bar)"':
            result = {'<=': operator.le, '>=': operator.ge}[op](case['bar'], int(value))
        else: raise AssertionError(('unhandled condition', key))
        results.append(result)
    return all(results)


def trace(nodes, case, event=None):
    """Compare ordered real effects; description-only blocks cannot execute."""
    result, taken = [], False
    for key, op, value in nodes:
        if key in ('if', 'else_if', 'else'):
            if key == 'if': taken = False
            f = fields(value)
            run = not taken and (key == 'else' or condition(f['limit'], case))
            if run:
                taken = True
                result += trace([n for n in value if n[0] != 'limit'], case, event)
        elif key == 'hidden_effect': result += trace(value, case, event)
        elif key == 'show_as_tooltip': pass
        elif key == 'sb_cape_finish_politics':
            result += trace(definition('common/scripted_effects/sb_cape_politics_effects.txt', key), case, fields(value)['EVENT'])
        elif key == 'trigger_event':
            f = fields(value)
            result.append((key, {**f, 'id': event if f['id'] == '$EVENT$' else f['id']}))
        elif isinstance(value, list): result.append((key, trace(value, case, event)))
        else: result.append((key, value))
    return result


class CapeCompletionEquivalence(unittest.TestCase):
    def test_exhaustive_boundaries_priority_dispatch_and_ordered_cleanup(self):
        old = fields(OLD)
        journal = definition('common/journal_entries/1-01_sb_cape_politics.txt', 'je_sb_cape_politics')
        endings = [fields(v) for k, _, v in journal if k == 'outcome' and fields(v).get('color') == '"gold_positive"']
        self.assertEqual(5, len(endings))
        flags = ('sb_cape_liberal_revolution_settler_outcome_var', 'sb_albany_sanctioned_var', 'sb_albany_refused_var')
        seen = set()
        for bar, law, alive, date, a, b, c in product(
                (-100, -90, -89, -31, -30, 0, 30, 31, 89, 90, 100),
                (False, True), (False, True), ('1879.1.1', '1880.1.1', '1885.1.1'),
                (False, True), (False, True), (False, True)):
            case = dict(bar=bar, law=law, xhosa_alive=alive, date=date,
                        variables={f for f, enabled in zip(flags, (a, b, c)) if enabled})
            eligible = [e for e in endings if condition(e['trigger'], case)]
            self.assertEqual(int(condition(old['trigger'], case)), len(eligible), case)
            if eligible:
                actual = trace(eligible[0]['effect'], case)
                self.assertEqual(trace(old['effect'], case), actual, case)
                dispatches = [v['id'] for k, v in actual if k == 'trigger_event']
                self.assertEqual(1, len(dispatches))
                seen.update(dispatches)
        self.assertEqual({f'sb_cape.{n}' for n in ('125', '100', '101', '102', '104')}, seen)

    def test_shared_effect_keeps_every_original_pre_and_post_dispatch_operation(self):
        hidden = fields(fields(OLD)['effect'])['hidden_effect']
        new = definition('common/scripted_effects/sb_cape_politics_effects.txt', 'sb_cape_finish_politics')
        self.assertEqual(['hidden_effect', 'trigger_event', 'hidden_effect'], [k for k, _, _ in new])
        self.assertEqual(hidden[:1], new[0][2])
        self.assertEqual(hidden[7:], new[2][2])  # Includes JE modifier cleanup, not just country variables.


class JoinRuntime(FrontierRuntime):
    def __init__(self, members):
        super().__init__(members)
        self.containers = {}

    def ref(self, key, scope, prev=None):
        if key.startswith('container:'):
            name, _, tail = key[10:].partition('.')
            target = self.containers.get(name)
            return self.ref(tail, target, scope) if tail and target is not None else target
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        results, branch = [], None
        for key, op, value in nodes:
            if key == 'NOT':
                # V3 CNotTrigger rejects ANY true child: NOT is NOR, not NAND.
                results.append(not any(self.condition([n], scope, prev) for n in value))
            elif key == 'container_exists':
                results.append(value in self.containers)
            elif key == 'trigger_if':
                branch = self.condition(fields(value)['limit'], scope, prev)
                if branch:
                    results.append(self.condition([n for n in value if n[0] != 'limit'], scope, prev))
            elif key == 'trigger_else':
                if branch is False: results.append(self.condition(value, scope, prev))
            elif key == 'any_diplomatic_play':
                results.append(any(self.condition(value, play, scope) for play in self.plays))
            else: results.append(super().condition([(key, op, value)], scope, prev))
        return all(results)


class NataliaJoinRestriction(unittest.TestCase):
    def setup_side(self):
        rt = JoinRuntime([])
        nal = {'id': 'NAL', 'vars': {}}
        swz = {'id': 'SWZ', 'vars': {'sb_zulu_swazi_war_active_var': 1}}
        zul = {'id': 'ZUL', 'vars': {'sb_zulu_swazi_war_active_var': 1}}
        play = {'id': 'marked', 'type': 'dp_conquer_state', 'initiator': zul, 'target': swz}
        zul['vars']['sb_zulu_swazi_play_scope'] = play
        rt.plays = [play]
        # No undocumented scope:diplomatic_play is supplied by this rule.
        rt.scopes.update(root=nal, initiator=zul, enemy_country=zul, target_country=swz)
        return rt, nal, swz, zul, play

    def allowed(self, rt, holder):
        return rt.condition(SWAZI['sb_swazi_defender_join_allowed'], holder)

    def test_exact_authored_defending_side_is_blocked_even_with_foreign_root(self):
        rt, nal, swz, zul, play = self.setup_side()
        self.assertFalse(self.allowed(rt, nal))
        rt.scopes['root'] = {'id': 'unrelated-preview-country', 'vars': {}}
        self.assertFalse(self.allowed(rt, nal))
        self.assertNotIn('diplomatic_play', rt.scopes)

    def test_other_actors_sides_plays_and_stale_records_remain_eligible(self):
        for case in ('other_joiner', 'zulu_side', 'different_target', 'different_initiator',
                     'unmarked', 'finished', 'dead_play', 'stale_record', 'wrong_play_type', 'wrong_play_target'):
            with self.subTest(case=case):
                rt, nal, swz, zul, play = self.setup_side()
                if case == 'other_joiner': nal = {'id': 'GBR', 'vars': {}}
                elif case == 'zulu_side': rt.scopes.update(target_country=zul, enemy_country=swz)
                elif case == 'different_target': rt.scopes['target_country'] = {'id': 'GZA', 'vars': {}}
                elif case == 'different_initiator': rt.scopes['initiator'] = swz
                elif case == 'unmarked': zul['vars'].pop('sb_zulu_swazi_play_scope')
                elif case == 'finished': swz['vars'].clear()
                elif case == 'dead_play': rt.plays = []
                elif case == 'stale_record': zul['vars']['sb_zulu_swazi_play_scope'] = {'id': 'old-play'}
                elif case == 'wrong_play_type': play['type'] = 'dp_humiliation'
                elif case == 'wrong_play_target': play['target'] = nal
                self.assertTrue(self.allowed(rt, nal))

    def test_native_joining_eligibility_is_preserved_after_removing_single_guard(self):
        self.assertIsNotNone(GAME)
        source = (ROOT / 'common/scripted_rules/zz_sb_swazi_join_rules.txt').read_text(encoding='utf-8-sig')
        actual = statements(find_object(source, 'can_join_side_in_diplomatic_play', directive='REPLACE'))
        expected = statements(find_object((GAME / 'common/scripted_rules/00_scripted_rules.txt').read_text(encoding='utf-8-sig'), 'can_join_side_in_diplomatic_play'))
        self.assertEqual(('custom_tooltip', '=', [('text', '=', 'sb_natalia_swazi_defender_blocked_tt'),
                                                ('sb_swazi_defender_join_allowed', '=', 'yes')]), actual[1])
        self.assertEqual(('custom_tooltip', '=', [('text', '=', 'sb_chiefs_foreign_armies_excluded_tt'), ('sb_chiefs_foreign_join_allowed', '=', 'yes')]), actual[0])
        self.assertEqual(expected, actual[2:])


class ChiefdomsJoinRestriction(unittest.TestCase):
    def setup_side(self):
        rt = JoinRuntime([])
        foreign = {'id': 'GBR', 'vars': {}}
        origin, rebels = ({'id': name, 'vars': {}} for name in ('ZUL', 'rebel-ZUL'))
        war = {'id': 'chiefdoms-war'}
        rt.global_vars.update(sb_zululand_chiefdoms_open_global_var=1,
                              sb_zululand_live_zul_scope=origin)
        rt.containers['sb_zululand_chiefdoms_state'] = {'vars': {
            'sb_chiefs_native_test_var': 1, 'sb_chiefs_origin_scope': origin,
            'sb_chiefs_rebels_scope': rebels, 'sb_chiefs_war_scope': war}}
        rt.scopes.update(root=foreign, target_country=origin, enemy_country=rebels)
        return rt, foreign, origin, rebels

    def allowed(self, rt, holder):
        nodes = definition('common/scripted_triggers/sb_chiefdoms_contest_triggers.txt',
                           'sb_chiefs_foreign_join_allowed')
        return rt.condition(nodes, holder)

    def test_not_truth_table_matches_native_negated_or(self):
        rt = JoinRuntime([])
        for a, b in product((False, True), repeat=2):
            nodes = [('NOT', '=', [('always', '=', 'yes' if a else 'no'),
                                   ('always', '=', 'yes' if b else 'no')])]
            self.assertEqual(not (a or b), rt.condition(nodes, rt.country))
            self.assertEqual(not (a and b), rt.condition([('NOT', '=', [('AND', '=', nodes[0][2])])], rt.country))

    def test_fresh_ottoman_montenegro_preview_allows_unrelated_joiners(self):
        rt = JoinRuntime([])
        tur, mon = ({'id': name, 'vars': {}} for name in ('TUR', 'MON'))
        for target, enemy in ((tur, mon), (mon, tur)):
            rt.scopes.update(target_country=target, enemy_country=enemy, initiator=tur)
            for tag in ('GBR', 'RUS', 'FRA', 'NGF', 'SPA', 'AUS', 'POR', 'NAL'):
                joiner = {'id': tag, 'vars': {}}
                rt.scopes['root'] = joiner
                self.assertTrue(self.allowed(rt, joiner), tag)
                self.assertTrue(rt.condition(SWAZI['sb_swazi_defender_join_allowed'], joiner), tag)

    def test_only_foreign_joiners_to_exact_test_pair_are_blocked(self):
        rt, foreign, origin, rebels = self.setup_side()
        for target, enemy in ((origin, rebels), (rebels, origin)):
            rt.scopes.update(target_country=target, enemy_country=enemy)
            self.assertFalse(self.allowed(rt, foreign))
            self.assertTrue(self.allowed(rt, origin))
            self.assertTrue(self.allowed(rt, rebels))

    def test_missing_inactive_and_unrelated_conflicts_never_veto(self):
        for case in ('no_container', 'no_open_flag', 'resolved', 'event_mode', 'no_origin',
                     'no_rebels', 'no_war', 'no_target', 'no_enemy', 'one_side', 'other_play'):
            with self.subTest(case=case):
                rt, foreign, origin, rebels = self.setup_side()
                saved = rt.containers['sb_zululand_chiefdoms_state']['vars']
                if case == 'no_container': rt.containers.clear()
                elif case == 'no_open_flag': rt.global_vars.pop('sb_zululand_chiefdoms_open_global_var')
                elif case == 'resolved': rt.global_vars['sb_zululand_chiefdoms_resolved_global_var'] = 1
                elif case == 'event_mode': saved.pop('sb_chiefs_native_test_var')
                elif case in ('no_origin', 'no_rebels', 'no_war'):
                    saved.pop('sb_chiefs_' + case.removeprefix('no_') + '_scope')
                elif case == 'no_target': rt.scopes.pop('target_country')
                elif case == 'no_enemy': rt.scopes.pop('enemy_country')
                elif case == 'one_side': rt.scopes['enemy_country'] = foreign
                elif case == 'other_play':
                    rt.scopes.update(target_country={'id': 'TUR', 'vars': {}},
                                     enemy_country={'id': 'MON', 'vars': {}})
                self.assertTrue(self.allowed(rt, foreign))


if __name__ == '__main__':
    unittest.main()
