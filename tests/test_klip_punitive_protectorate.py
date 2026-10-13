"""Evaluate the actual two-demand gates; engine goal enforcement remains DP-tested."""
import unittest
from copy import deepcopy

from tests.test_klip_river_colonial_delivery import expression
from tests.test_natal_zululand_gameplay_contract import (
    object_block, object_block_from_source, nested_blocks, text,
)

EFFECTS = 'common/scripted_effects/sb_klip_river_county_effects.txt'
TRIGGERS = 'common/scripted_triggers/sb_klip_river_county_triggers.txt'
NATAL = 'common/scripted_triggers/sb_natal_interwar_triggers.txt'
ZUL = 'common/scripted_triggers/sb_zululand_settlement_triggers.txt'
ACTIVE = 'sb_klip_river_punitive_active_var'
ROUTE = 'sb_natal_klip_river_settlement_var'
ENDED = 'sb_klip_river_punitive_ended_var'
RESOLVED = 'sb_natal_zulu_settlement_resolved_var'


def world():
    return {'flags': {ACTIVE, ROUTE}, 'play_exists': True, 'protectorate': False,
            'owners': {'xBBCA32': 'ZUL', 'xDE0EDE': 'NAL', 'x552449': 'NAL',
                       'x279045': 'NAL'}, 'zulu_alive': True, 'zululand_owner': 'ZUL',
            'war': True, 'play': True}


def trigger(name, state, actor='NAL'):
    path = NATAL if name == 'sb_natal_zulu_settlement_ready' else (
        ZUL if name.startswith('sb_zululand_') else TRIGGERS)
    return evaluate(expression(object_block(path, name)), state, actor)


def evaluate(nodes, state, actor='NAL'):
    def check(key, value):
        if key == 'OR':
            return any(evaluate([node], state, actor) for node in value)
        if key == 'NOT':
            return not evaluate(value, state, actor)
        if key == 'AND':
            return evaluate(value, state, actor)
        if key.startswith('sb_'):
            return trigger(key, state, actor) == (value == 'yes')
        if key.startswith('c:'):
            return evaluate(value, state, key[2:])
        if key.startswith('p:'):
            return state['owners'][key[2:].split('.')[0]] == value[2:]
        if key == 'country_definition':
            return value == 'cd:' + actor
        if key == 'has_variable':
            return value in state['flags']
        if key == 'exists':
            assert value == 'var:sb_klip_river_punitive_play_scope'
            return state['play_exists']
        if key == 'is_direct_subject_of':
            return actor == 'ZUL' and value == 'c:NAL' and state['protectorate']
        if key == 'is_subject_type':
            return state['protectorate'] and value == 'subject_type_protectorate'
        if key == 'owns_entire_state_region':
            return state['zululand_owner'] == actor
        facts = {'is_country_alive': actor != 'ZUL' or state['zulu_alive'],
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


class KlipPunitiveProtectorateTests(unittest.TestCase):
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
                    state['protectorate'] = True
                self.assertEqual('success' if index else 'pending', selected_outcome(state))
            self.assertTrue(trigger('sb_natal_zulu_settlement_ready', state))
            for change in ('territory', 'protectorate'):
                reversed_state = deepcopy(state)
                if change == 'territory':
                    reversed_state['owners']['xBBCA32'] = 'ZUL'
                else:
                    reversed_state['protectorate'] = False
                self.assertFalse(trigger('sb_natal_zulu_settlement_ready', reversed_state))
            state['flags'].discard(ACTIVE)  # Actual terminal cleanup consumes this marker.
            self.assertEqual('pending', selected_outcome(state))
            state['flags'].add(RESOLVED)
            self.assertFalse(trigger('sb_natal_zulu_settlement_ready', state))

    def test_partial_terminal_results_never_become_success(self):
        for returned, protectorate in ((False, False), (True, False), (False, True)):
            state = world()
            state['protectorate'] = protectorate
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
        state['protectorate'] = True
        self.assertTrue(trigger('sb_natal_zulu_settlement_ready', state))


if __name__ == '__main__':
    unittest.main()
