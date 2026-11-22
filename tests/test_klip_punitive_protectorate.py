"""Evaluate the actual two-demand gates; engine goal enforcement remains DP-tested."""
import unittest
from copy import deepcopy
from decimal import Decimal, ROUND_DOWN
from functools import lru_cache

from tests.test_klip_river_colonial_delivery import expression
from tests.test_natal_zululand_gameplay_contract import (
    object_block, object_block_from_source, nested_blocks, text,
)
from tools.check_override_inventory import find_object

EFFECTS = 'common/scripted_effects/sb_klip_river_county_effects.txt'
TRIGGERS = 'common/scripted_triggers/sb_klip_river_county_triggers.txt'
NATAL = 'common/scripted_triggers/sb_natal_interwar_triggers.txt'
ZUL = 'common/scripted_triggers/sb_zululand_settlement_triggers.txt'
ACTIVE = 'sb_klip_river_punitive_active_var'
ROUTE = 'sb_natal_klip_river_settlement_var'
ENDED = 'sb_klip_river_punitive_ended_var'
RESOLVED = 'sb_natal_zulu_settlement_resolved_var'
KLIP_RESOLVED = 'sb_klip_river_county_resolved_var'
VICTORY = 'sb_klip_river_final_evidence_1_var'
ZUL_EFFECTS = 'common/scripted_effects/sb_zululand_settlement_effects.txt'
NATAL_EFFECTS = 'common/scripted_effects/sb_natal_interwar_effects.txt'
ENTHUSIASM_EFFECT = 'common/scripted_effects/zz_sb_movement_enthusiasm_override.txt'


def game_day(date):
    """Native script durations use whole game days (365/year, 30/month)."""
    year, month, day = map(int, date.split('.')[:3])
    return year * 365 + sum((31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[:month - 1]) + day - 1


def variables(state, actor):
    if isinstance(actor, dict):
        return actor.setdefault('variables', {})
    return state.setdefault('variables', {}).setdefault(actor, {})


def script_value(value, state, actor, previous=None):
    if value == 'game_date':
        return Decimal(game_day(state['date']))
    if value.startswith('owner.'):
        return script_value(value[6:], state, actor['owner'], actor)
    if value.startswith('prev.'):
        return script_value(value[5:], state, previous)
    if value.startswith('var:'):
        return variables(state, actor)[value[4:]]
    if value == 'sb_natal_movement_remaining_days':
        formula = expression(object_block('common/script_values/sb_natal_movement_values.txt', value))
        assert len(formula) == 1 and formula[0][0] == 'value'
        return script_value(formula[0][1], state, actor, previous)
    return Decimal(value)


def world():
    return {'flags': {ACTIVE, ROUTE}, 'foreign_flags': {'GBR': set(), 'ZUL': {ACTIVE}},
            'date': '1850.6.6',
            'play_exists': True, 'subject_type': None, 'overlord': None,
            'natal_overlord': 'GBR', 'events': [],
            'owners': {'xBBCA32': 'ZUL', 'xDE0EDE': 'NAL', 'x552449': 'NAL',
                       'x279045': 'NAL'}, 'zulu_alive': True, 'zululand_owner': 'ZUL',
            'war': True, 'play': True}


def subjugate(state, overlord='NAL'):
    state.update(subject_type='subject_type_protectorate', overlord=overlord)


def country_flags(state, actor):
    if isinstance(actor, dict):
        return actor.setdefault('flags', set())
    return state['flags'] if actor == 'NAL' else state['foreign_flags'][actor]


def trigger(name, state, actor='NAL', root='NAL'):
    path = NATAL if name.startswith('sb_natal_') else (
        ZUL if name.startswith('sb_zululand_') else TRIGGERS)
    return evaluate(expression(object_block(path, name)), state, actor, root)


def evaluate(nodes, state, actor='NAL', root='NAL'):
    def check(key, value):
        if key == 'OR':
            return any(evaluate([node], state, actor, root) for node in value)
        if key == 'NOT':
            return not any(evaluate([node], state, actor, root) for node in value)
        if key == 'AND':
            return evaluate(value, state, actor, root)
        if key == 'owner':
            return evaluate(value, state, actor['owner'], root)
        if key == 'any_political_movement':
            return any(evaluate(value, state, movement, root)
                       for movement in state.get('movements', []) if movement['owner'] == actor)
        if key in ('is_political_movement_type', 'culture'):
            return actor['type' if key == 'is_political_movement_type' else 'culture'] == value
        if key.startswith('sb_'):
            return trigger(key, state, actor, root) == (value == 'yes')
        if key.startswith('c:'):
            return evaluate(value, state, key[2:], root)
        if key.startswith('p:'):
            return state['owners'][key[2:].split('.')[0]] == value[2:]
        if key == 'country_definition':
            return value == 'cd:' + actor
        if key == 'has_global_variable':
            return value in state.get('globals', {})
        if key == 'has_variable':
            return value in country_flags(state, actor)
        if key.endswith(' >'):
            return script_value(key[:-2], state, actor) > script_value(value, state, actor)
        if key == 'exists':
            if value.startswith('global_var:'):
                return value[11:] in state.get('globals', {})
            assert value == 'var:sb_klip_river_punitive_play_scope'
            return state['play_exists']
        parents = {'NAL': state['natal_overlord'], 'ZUL': state['overlord']}
        if key in ('is_direct_subject_of', 'is_subject_of'):
            expected = root if value.lower() == 'root' else value[2:]
            parent = parents.get(actor)
            while parent:
                if parent == expected:
                    return True
                if key == 'is_direct_subject_of':
                    break
                parent = parents.get(parent)
            return False
        if key == 'is_subject_type':
            return actor == 'ZUL' and state['subject_type'] == value
        if key == 'has_modifier':
            if isinstance(actor, dict):
                return value in actor['modifiers']
            return False  # No pre-existing Chiefdoms modifier in the founding fixture.
        if key == 'owns_entire_state_region':
            return state['zululand_owner'] == actor
        alive = {'ZUL': state['zulu_alive'], 'KLR': state.get('county_alive', False)}
        facts = {'is_country_alive': alive.get(actor, True),
                 'is_subject': parents.get(actor) is not None,
                 'is_at_war': state['war'], 'is_active_in_diplomatic_play': state['play']}
        return facts[key] == (value == 'yes')
    return all(check(key, value) for key, value in nodes)


def selected_outcome(state):
    effect = object_block(EFFECTS, 'sb_klip_river_reconcile_punitive_settlement')
    branches = [nested_blocks(effect, kind)[0] for kind in ('if', 'else_if')]
    for outcome, branch in zip(('success', 'terminal_failure'), branches):
        if evaluate(expression(object_block_from_source(branch, 'limit')), state):
            return outcome
    return 'pending'


@lru_cache(None)
def effect_nodes(name):
    path = (ENTHUSIASM_EFFECT if name == 'add_movement_enthusiasm_modifier' else
            'common/scripted_effects/sb_boer_leadership_effects.txt' if name == 'sb_restore_punitive_andries' else
            EFFECTS if name.startswith('sb_klip_river_') else
            NATAL_EFFECTS if name.startswith('sb_natal_') else ZUL_EFFECTS)
    return expression(find_object(text(path), name, directive='REPLACE' if path == ENTHUSIASM_EFFECT else None))


def run_effect(name, state, actor='NAL', root='NAL', nodes=None, arguments=None, previous=None):
    """Execute the actual handoff/settlement script, with foreign ROOT preserved.

    Movement creation and modifier writes are recorded; native recruitment and
    survival are not simulated. Character/economic packages remain outside this
    lifecycle fixture, and dispatch is not emulated as an engine popup.
    """
    excluded_packages = {
        'sb_natal_restore_archived_zulu_firearms', 'sb_natal_archive_zulu_firearms',
        'sb_zululand_archive_preannexation_royal_house',
        'sb_zululand_begin_natal_incorporation', 'sb_zululand_mark_and_exile_royal_house',
        'sb_zululand_setup_usuthu_politics', 'sb_zululand_open_chiefdoms_situation',
    }

    def execute(nodes, current, previous):
        taken = False
        for key, value in nodes:
            if key in ('if', 'else_if', 'else'):
                if key == 'if':
                    taken = False
                condition = next((v for k, v in value if k == 'limit'), [])
                if not taken and evaluate(condition, state, current, root):
                    execute([(k, v) for k, v in value if k != 'limit'], current, previous)
                    taken = True
            elif key.startswith('c:'):
                execute(value, key[2:], current)
            elif key == 'owner':
                execute(value, current['owner'], current)
            elif key == 'hidden_effect':
                execute(value, current, previous)
            elif key == 'every_political_movement':
                condition = next((v for k, v in value if k == 'limit'), [])
                for movement in state.get('movements', []):
                    if movement['owner'] == current and evaluate(condition, state, movement, root):
                        execute([(k, v) for k, v in value if k != 'limit'], movement, current)
            elif key == 'create_political_movement':
                movement = dict(value, owner=current, modifiers={})
                state.setdefault('movements', []).append(movement)
                if state.get('native_enthusiasm_on_create'):
                    run_effect('add_movement_enthusiasm_modifier', state, movement, root)
            elif key == 'add_movement_enthusiasm_modifier':
                run_effect(key, state, current, root, previous=previous)
            elif key == 'add_modifier' and isinstance(current, dict):
                modifier = dict(value)
                # Native duration fields look up a named value; bare var: links fail on load.
                for unit in ('days', 'months', 'years'):
                    if unit in modifier:
                        assert ':' not in modifier[unit], ('invalid duration value', modifier[unit])
                duration = next(script_value(modifier[unit], state, current, previous) * days
                                for unit, days in (('days', 1), ('months', 30), ('years', 365))
                                if unit in modifier)
                start = game_day(state['date'])
                current['modifiers'][modifier['name']] = {
                    'start': start, 'end': start + int(duration),
                    'multiplier': script_value(modifier.get('multiplier', '1'), state, current, previous),
                    'decaying': modifier.get('is_decaying') == 'yes',
                }
            elif key == 'remove_modifier':
                current['modifiers'].pop(value, None)
            elif key == 'change_relations':
                change = dict(value)
                state.setdefault('relation_changes', []).append(
                    (current, change['country'][2:], int(change['value'])))
            elif key == 'add_loyalists':
                state.setdefault('loyalist_changes', []).append((current, dict(value)))
            elif key.startswith('s:') or key in ('add_modifier', 'add_radicals'):
                continue
            elif key == 'set_variable':
                data = {'name': value} if isinstance(value, str) else dict(value)
                country_flags(state, current).add(data['name'])
                if 'value' in data:
                    variables(state, current)[data['name']] = script_value(data['value'], state, current, previous)
            elif key == 'change_variable':
                data = dict(value)
                old = variables(state, current)[data['name']]
                operation, operand = next((k, v) for k, v in value if k != 'name')
                operand = script_value(operand, state, current, previous)
                result = {'add': lambda: old + operand, 'subtract': lambda: old - operand,
                          'divide': lambda: old / operand}[operation]()
                variables(state, current)[data['name']] = result.quantize(Decimal('.00001'), rounding=ROUND_DOWN)
            elif key == 'remove_variable':
                country_flags(state, current).discard(value)
                variables(state, current).pop(value, None)
            elif key == 'transfer_subject':
                assert value == 'c:ZUL'
                if state.get('transfer_succeeds', True):
                    state['overlord'] = current
            elif key == 'change_subject_type':
                assert current == 'ZUL'
                state['subject_type'] = value
            elif key == 'annex':
                assert current == 'NAL' and value == 'c:ZUL'
                state.update(zulu_alive=False, overlord=None, subject_type=None, zululand_owner='NAL')
            elif key == 'trigger_event':
                state['events'].append((dict(value)['id'], current, frozenset(state['flags'])))
            elif key in excluded_packages:
                continue
            elif key.startswith('sb_'):
                run_effect(key, state, current, root, arguments=value, previous=previous)
            else:
                raise AssertionError((key, value))
    def substitute(value):
        if isinstance(value, list):
            return [(substitute(k), substitute(v)) for k, v in value]
        for parameter, replacement in (arguments if isinstance(arguments, list) else []):
            value = value.replace('$' + parameter + '$', replacement)
        return value

    execute(substitute(effect_nodes(name) if nodes is None else nodes), actor, previous)


class KlipPunitiveProtectorateTests(unittest.TestCase):
    def test_crown_relations_replace_only_zulus_loyalists_once_despite_foreign_root(self):
        for root in ('NAL', 'ZUL', 'GBR', 'diplomatic_play_123'):
            with self.subTest(root=root):
                state = world()
                state['flags'].clear()
                subjugate(state)
                for _ in range(2):
                    run_effect('sb_zululand_choose_subordinate_crown', state, actor='NAL', root=root)
                self.assertEqual([('ZUL', 'NAL', 15), ('ZUL', 'GBR', 15)],
                                 state.get('relation_changes', []))
                self.assertEqual([('NAL', {'value': '0.10', 'culture': 'cu:zulu'})],
                                 state.get('loyalist_changes', []))
                self.assertEqual(('NAL', 'subject_type_protectorate', True),
                                 (state['overlord'], state['subject_type'], state['zulu_alive']))

    def test_two_natal_demands_and_distinct_zulu_counter_demand(self):
        play = object_block('common/diplomatic_plays/sb_diplomatic_plays.txt',
                            'dp_sb_klip_river_punitive_expedition')
        self.assertIn('war_goal = make_protectorate', play)
        configure = object_block(EFFECTS, 'sb_klip_river_configure_started_play')
        punitive = nested_blocks(configure, 'else_if')[0]
        goals = [dict(expression(b)) for b in nested_blocks(punitive, 'add_war_goal')]
        natal = next(g for g in goals if g['holder'] == 'c:NAL')
        self.assertEqual(('return_state', 'c:ZUL', 's:STATE_NATAL.region_state:ZUL', 'yes'),
                         tuple(natal[k] for k in ('type', 'target_country', 'target_state', 'primary_demand')))
        counter = next(g for g in goals if g['holder'] == 'c:ZUL')
        self.assertEqual('c:NAL', counter['target_country'])
        self.assertEqual('scope:sb_klip_river_punitive_frozen_state', counter['target_state'])
        self.assertNotIn('primary_demand', counter)
        self.assertIn('add_initiator_backers = { c:GBR }', punitive)
        self.assertNotIn('archive', punitive)

    def test_each_timer_order_requires_both_results_and_rechecks_reversal(self):
        for order in (('territory', 'protectorate'), ('protectorate', 'territory')):
            state = world()
            for index, demand in enumerate(order):
                self.assertEqual('pending', selected_outcome(state))
                self.assertFalse(trigger('sb_natal_zulu_settlement_ready', state))
                if demand == 'territory':
                    state['owners']['xBBCA32'] = 'NAL'
                else:
                    subjugate(state)
                self.assertEqual('success' if index else 'pending', selected_outcome(state))
            self.assertTrue(trigger('sb_natal_zulu_settlement_ready', state))
            for change in ('territory', 'protectorate'):
                reversed_state = deepcopy(state)
                if change == 'territory':
                    reversed_state['owners']['xBBCA32'] = 'ZUL'
                else:
                    reversed_state.update(subject_type=None, overlord=None)
                self.assertFalse(trigger('sb_natal_zulu_settlement_ready', reversed_state))
            state['flags'].discard(ACTIVE)  # Actual terminal cleanup consumes this marker.
            self.assertEqual('pending', selected_outcome(state))
            state['flags'].add(RESOLVED)
            self.assertFalse(trigger('sb_natal_zulu_settlement_ready', state))

    def test_partial_terminal_results_never_become_success(self):
        for returned, protectorate in ((False, False), (True, False), (False, True)):
            state = world()
            if protectorate:
                subjugate(state)
            if returned:
                state['owners']['xBBCA32'] = 'NAL'
            for terminal in ('callback', 'deleted_play'):
                final = deepcopy(state)
                if terminal == 'callback':
                    final['flags'].add(ENDED)
                else:
                    final['play_exists'] = False
                self.assertEqual('terminal_failure', selected_outcome(final))
                final['flags'].discard(ACTIVE)
                self.assertFalse(trigger('sb_natal_zulu_settlement_ready', final))
        evidence = object_block(EFFECTS, 'sb_klip_river_record_punitive_final_evidence')
        state = world()
        state['owners']['x279045'] = 'ZUL'
        defeat = nested_blocks(evidence, 'else_if')[0]
        self.assertTrue(evaluate(dict(expression(defeat))['limit'], state))
        self.assertIn('set_variable = sb_klip_river_final_evidence_2_var', defeat)

    def test_callbacks_match_exact_play_and_defer_negative_outcomes(self):
        for name in ('sb_klip_river_handle_backdown', 'sb_klip_river_handle_war_end'):
            effect = object_block(EFFECTS, name)
            branch = next(b for b in nested_blocks(effect, 'else_if')
                          if 'dp_sb_klip_river_punitive_expedition' in b)
            self.assertIn('var:sb_klip_river_punitive_play_scope = root', branch)
            self.assertNotIn('scope:actor', object_block_from_source(branch, 'limit'))
            self.assertIn('set_variable = ' + ENDED, branch)
            self.assertNotIn('finalize_punitive', branch)
        clear = object_block(EFFECTS, 'sb_klip_river_clear_punitive_runtime')
        self.assertIn('remove_variable = ' + ACTIVE, clear)
        self.assertNotIn('remove_variable = ' + ROUTE, text(EFFECTS))
        housekeeping = object_block(EFFECTS, 'sb_klip_river_cleanup_orphaned_runtime')
        self.assertIn('sb_klip_river_reconcile_punitive_settlement = yes', housekeeping)

    def test_three_live_country_options_and_no_crown_recreation(self):
        event = object_block('events/sb_natal_interwar_events.txt', 'sb_natal_interwar.030')
        self.assertEqual(3, len(nested_blocks(event, 'option')))
        self.assertIn('desc = sb_natal_interwar.030.d', event)
        path = 'common/scripted_effects/sb_zululand_settlement_effects.txt'
        crown = object_block(path, 'sb_zululand_choose_subordinate_crown')
        for forbidden in ('restore_preannexation', 'restore_protectorate', 'create_character', 'transfer_character'):
            self.assertNotIn(forbidden, crown)
        chiefdoms = object_block(path, 'sb_zululand_choose_thirteen_chiefdoms')
        self.assertIn('subject_type_sb_zulu_chiefdoms', chiefdoms)
        self.assertNotIn('restore_protectorate', chiefdoms)
        direct = object_block(path, 'sb_zululand_choose_direct_natal_administration')
        self.assertIn('annex = c:ZUL', direct)
        # British handoff still admits an ordinary live protectorate independently.
        state = world()
        state['flags'] = set()
        subjugate(state)
        self.assertTrue(trigger('sb_natal_zulu_settlement_ready', state))

    def test_british_goal_is_victory_but_does_not_open_natal_government_early(self):
        for ended in (False, True):
            with self.subTest(ended=ended):
                state = world()
                state['owners']['xBBCA32'] = 'NAL'
                subjugate(state, 'GBR')
                if ended:
                    state['flags'].add(ENDED)
                self.assertEqual('success', selected_outcome(state))
                run_effect('sb_klip_river_reconcile_punitive_settlement', state)
                self.assertIn(VICTORY, state['flags'])
                self.assertNotIn(ACTIVE, state['flags'])
                self.assertEqual(['sb_klip_river_county.080'], [e[0] for e in state['events']])
                self.assertEqual('GBR', state['overlord'])
                self.assertFalse(trigger('sb_natal_zulu_settlement_ready', state))

    def test_handoff_and_monthly_orders_preserve_victory_through_every_government_choice(self):
        for monthly_first in (False, True):
            for choice in ('direct_natal_administration', 'thirteen_chiefdoms', 'subordinate_crown'):
                with self.subTest(monthly_first=monthly_first, choice=choice):
                    state = world()
                    state['flags'].add(ENDED)
                    state['owners']['xBBCA32'] = 'NAL'
                    subjugate(state, 'GBR')
                    if monthly_first:
                        run_effect('sb_klip_river_reconcile_punitive_settlement', state)
                    run_effect('sb_zululand_handoff_to_natal', state, actor='GBR', root='GBR')
                    self.assertEqual('NAL', state['overlord'])
                    self.assertIn(VICTORY, state['flags'])
                    self.assertNotIn(ACTIVE, state['flags'])
                    self.assertNotIn(KLIP_RESOLVED, state['foreign_flags']['GBR'])
                    government = [e for e in state['events'] if e[0] == 'sb_natal_interwar.030']
                    self.assertEqual(1, len(government))
                    self.assertEqual('NAL', government[0][1])
                    self.assertIn(KLIP_RESOLVED, government[0][2])
                    run_effect('sb_zululand_choose_' + choice, state)
                    for _ in range(3):
                        run_effect('sb_klip_river_reconcile_punitive_settlement', state)
                    self.assertIn(VICTORY, state['flags'])
                    self.assertNotIn('sb_klip_river_final_evidence_0_var', state['flags'])
                    self.assertEqual(['sb_klip_river_county.080', 'sb_natal_interwar.030'],
                                     [e[0] for e in state['events']])

    def test_british_victory_requires_the_real_territory_and_subject_relationship(self):
        for missing in ('territory', 'protectorate', 'british_natal', 'allied_overlord'):
            with self.subTest(missing=missing):
                state = world()
                state['flags'].add(ENDED)
                state['owners']['xBBCA32'] = 'NAL'
                subjugate(state, 'GBR')
                if missing == 'territory':
                    state['owners']['xBBCA32'] = 'ZUL'
                elif missing == 'protectorate':
                    state['subject_type'] = 'subject_type_puppet'
                elif missing == 'british_natal':
                    state['natal_overlord'] = None
                else:
                    state['overlord'] = 'FRA'
                self.assertEqual('terminal_failure', selected_outcome(state))
                self.assertFalse(trigger('sb_natal_zulu_settlement_ready', state))

    def test_ordinary_british_handoff_does_not_invent_a_klip_result(self):
        state = world()
        state['flags'].clear()
        subjugate(state, 'GBR')
        run_effect('sb_zululand_handoff_to_natal', state, actor='GBR', root='GBR')
        self.assertNotIn(KLIP_RESOLVED, state['flags'])
        self.assertEqual(['sb_natal_interwar.030'], [e[0] for e in state['events']])


if __name__ == '__main__':
    unittest.main()
