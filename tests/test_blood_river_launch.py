"""Evaluate Blood River's actual launch guards; engine delivery remains DP's check."""
import re
import unittest

from tests.test_1_14_story_war_routes import object_block
from tests.test_usuthu_movement_contest import parse

EFFECTS = 'common/scripted_effects/sb_story_war_effects.txt'
TRIGGERS = 'common/scripted_triggers/sb_natal_interwar_triggers.txt'
EVENTS = 'events/sb_natal_crisis_events.txt'


def field(nodes, key):
    return next(value for name, _, value in nodes if name == key)


class LaunchContext:
    def __init__(self, route='refusal'):
        self.route = route
        self.root = 'ORA' if route == 'refusal' else 'ZUL'
        self.generation = f'sb_natal_{route}_generation_state'
        self.receipt = f'sb_natal_{route}_receipt_scope'
        self.scopes = {self.receipt: self.generation, 'zulu_kingdom': 'ZUL'}
        self.variables = {actor: {} for actor in ('ORA', 'ZUL', self.generation)}
        for actor in ('ORA', 'ZUL'):
            self.variables[actor][f'sb_natal_{route}_generation_scope'] = self.generation
            if route == 'guns_bargain':
                self.variables[actor]['sb_natal_guns_bargain_war_var'] = True
        self.variables['ORA']['sb_natal_diplomacy_started_var'] = True
        for suffix in ('generation_pending', 'popup_receipt'):
            self.variables[self.generation][f'sb_natal_{route}_{suffix}_var'] = True
        self.wars = {'ORA': {'PHL', 'BST'}, 'ZUL': set()}
        self.plays = []
        self.truces = set()
        self.globals = set()

    def reference(self, name, actor):
        if name.lower() == 'root': return self.root
        if name == 'this': return actor
        if name.startswith(('c:', 'container:')): return name.split(':', 1)[1]
        if name.startswith('scope:'): return self.scopes.get(name[6:])
        if name.startswith('var:'): return self.variables[actor].get(name[4:])
        raise AssertionError(name)

    def evaluate(self, nodes, actor):
        def check(key, op, value):
            if key == 'NOT': return not any(self.evaluate([n], actor) for n in value)
            if key == 'OR': return any(self.evaluate([n], actor) for n in value)
            if key == 'AND': return self.evaluate(value, actor)
            if key.startswith(('c:', 'scope:', 'var:', 'container:')):
                target = self.reference(key, actor)
                if isinstance(value, list):
                    return target is not None and self.evaluate(value, target)
                return target == self.reference(value, actor)
            if key == 'exists': return self.reference(value, actor) in self.variables
            if key == 'container_exists': return value == self.generation
            if key == 'has_variable': return value in self.variables[actor]
            if key == 'has_global_variable': return value in self.globals
            if key == 'country_definition': return value == 'cd:' + actor
            if key == 'ruler': return self.evaluate(value, actor)
            if key in ('is_country_alive', 'is_character_alive', 'aggressive_diplomatic_plays_permitted'):
                return value == 'yes'
            if key == 'is_subject': return value == 'no'
            if key == 'is_at_war': return bool(self.wars[actor]) == (value == 'yes')
            if key == 'has_war_with': return value[2:] in self.wars[actor]
            if key == 'has_truce_with': return frozenset((actor, value[2:])) in self.truces
            if key == 'is_active_in_diplomatic_play':
                return any(actor in (p['initiator'], p['target']) for p in self.plays) == (value == 'yes')
            if key == 'is_diplomatic_play_enemy_of':
                return any({actor, value[2:]} == {p['initiator'], p['target']} for p in self.plays)
            if key == 'any_diplomatic_play': return any(self.evaluate(value, p) for p in self.plays)
            if key == 'is_diplomatic_play_type': return actor['type'] == value
            if key in ('initiator', 'target'): return actor[key] == self.reference(value, actor)
            if key == 'any_scope_state': return self.evaluate(value, actor)
            if key == 'state_region': return value == 's:STATE_NATAL'
            if key.startswith('sb_natal_story_'):
                return self.evaluate(parse(object_block(TRIGGERS, key)), actor) == (value == 'yes')
            raise AssertionError((key, op, value))
        return all(check(*node) for node in nodes)

    def gate(self, effect):
        branch = field(parse(object_block(EFFECTS, effect)), 'if')
        return self.evaluate(field(branch, 'limit'), 'ZUL')

    def reserve_launch(self):
        branch = field(parse(object_block(EFFECTS, 'sb_natal_story_begin_exact_launch')), 'if')
        assert self.evaluate(field(branch, 'limit'), 'ZUL')
        # Read the two actual reservation writes and their scope from the script.
        for key, _, value in branch:
            if key == 'set_variable': self.variables['ZUL'][value] = True
            elif key == 'c:ORA': self.variables['ORA'][field(value, 'set_variable')] = True

    def recovery_calls(self):
        calls = []
        def walk(nodes, actor):
            matched = False
            for key, _, value in nodes:
                if key in ('if', 'else_if', 'else'):
                    if key == 'if': matched = False
                    if not matched and (key == 'else' or self.evaluate(field(value, 'limit'), actor)):
                        matched = True
                        walk([node for node in value if node[0] != 'limit'], actor)
                elif key.startswith(('c:', 'container:')):
                    walk(value, self.reference(key, actor))
                elif key == 'save_scope_as': self.scopes[value] = actor
                elif key == 'sb_natal_story_recover_finished_play':
                    walk(parse(object_block(EFFECTS,key)),actor)
                elif key.startswith('sb_natal_story_'): calls.append(key)
                else: raise AssertionError(key)
        walk(parse(object_block(EFFECTS, 'sb_natal_story_recover_generation')), self.root)
        return calls


class BloodRiverLaunchTests(unittest.TestCase):
    def test_rally_is_one_available_default_through_the_full_popup_lifetime(self):
        for route, number, option_name in (('refusal', '050', 'b'), ('guns_bargain', '026', 'a')):
            with self.subTest(route=route):
                world = LaunchContext(route)
                event = parse(object_block(EVENTS, f'sb_natal_crisis.{number}'))
                rally = [value for key, _, value in event if key == 'option'
                         and field(value, 'name') == f'sb_natal_crisis.{number}.{option_name}']
                self.assertEqual(1, len(rally), 'Do not disguise requeue as a second Rally choice')
                self.assertEqual('yes', field(rally[0], 'default_option'))
                self.assertTrue(world.evaluate(field(rally[0], 'trigger'), world.root))
                self.assertEqual('yes', field(field(rally[0], 'hidden_effect') if route == 'guns_bargain'
                                             else field(rally[0], 'scope:zulu_kingdom'),
                                             'sb_natal_story_begin_exact_launch'))
                immediate = field(event, 'immediate')
                receipt = field(immediate, f'scope:{world.receipt}')
                self.assertGreater(int(field(field(receipt, 'set_variable'), 'months')),
                                   int(field(event, 'duration')))
                del world.variables[world.generation][f'sb_natal_{route}_generation_pending_var']
                self.assertFalse(world.evaluate(field(rally[0], 'trigger'), world.root))

    def test_unrelated_wars_and_plays_do_not_block_reservation_or_launch(self):
        for route in ('refusal', 'guns_bargain'):
            for busy in ('ORA', 'ZUL'):
                with self.subTest(route=route, busy=busy):
                    world = LaunchContext(route)
                    world.wars[busy] = {'PHL', 'BST'}
                    world.plays = [dict(type='dp_conquer_state', initiator=busy, target='BST')]
                    self.assertTrue(world.gate('sb_natal_story_begin_exact_launch'))
                    world.reserve_launch()
                    self.assertTrue(world.gate('sb_natal_story_attempt_exact_launch'))
                    self.assertFalse(world.gate('sb_natal_story_begin_exact_launch'))

    def test_selected_escalation_waits_for_only_the_actual_counterparty_conflict(self):
        for conflict in ('war', 'truce', 'play', 'reverse_play'):
            with self.subTest(conflict=conflict):
                world = LaunchContext()
                if conflict == 'war': world.wars['ZUL'].add('ORA')
                elif conflict == 'truce': world.truces.add(frozenset(('ZUL', 'ORA')))
                else:
                    actors = ('ZUL', 'ORA') if conflict == 'play' else ('ORA', 'ZUL')
                    world.plays = [dict(type='dp_conquer_state', initiator=actors[0], target=actors[1])]
                world.reserve_launch()
                self.assertFalse(world.gate('sb_natal_story_attempt_exact_launch'))
                world.wars['ZUL'].clear()
                world.plays.clear()
                world.truces.clear()
                self.assertTrue(world.gate('sb_natal_story_attempt_exact_launch'))
                world.variables['ZUL']['sb_natal_story_play_scope'] = 'admitted_play'
                self.assertFalse(world.gate('sb_natal_story_attempt_exact_launch'))

    def test_watchdog_distinguishes_open_lost_answered_and_admitted_delivery(self):
        for route in ('refusal', 'guns_bargain'):
            with self.subTest(route=route):
                world = LaunchContext(route)
                self.assertEqual([], world.recovery_calls())
                del world.variables[world.generation][f'sb_natal_{route}_popup_receipt_var']
                self.assertEqual([f'sb_natal_story_requeue_{route}_delivery'], world.recovery_calls())
                world.reserve_launch()
                self.assertEqual(['sb_natal_story_queue_launch_retry'], world.recovery_calls())
                retry = parse(object_block(EFFECTS, 'sb_natal_story_queue_launch_retry'))
                branch = field(retry, 'if')
                self.assertTrue(world.evaluate(field(branch, 'limit'), 'ZUL'))
                queued = field(field(branch, 'set_variable'), 'name')
                world.variables['ZUL'][queued] = True
                self.assertFalse(world.evaluate(field(branch, 'limit'), 'ZUL'))
                self.assertEqual('sb_natal_crisis.099', field(field(branch, 'trigger_event'), 'id'))
                world.variables['ZUL']['sb_natal_story_play_scope'] = 'admitted_play'
                self.assertEqual([], world.recovery_calls())

    def test_receipt_actor_and_parent_are_current_country_under_foreign_root(self):
        for route, actor, root in (('refusal', 'ORA', 'ZUL'), ('guns_bargain', 'ZUL', 'ORA')):
            with self.subTest(route=route):
                world = LaunchContext(route)
                world.root = root
                source = object_block(EFFECTS, f'sb_natal_story_begin_{route}_generation')
                # This small assignment parser does not consume bare tag lists.
                source = re.sub(r'tags\s*=\s*\{[^}]*\}', '', source)
                branch = next(value for key, _, value in parse(source)
                    if key == 'if' and any(k == 'create_container' for k, _, _ in value))
                for key, _, value in branch:
                    if key == 'save_scope_as': world.scopes[value] = actor
                    elif key in ('ROOT', 'c:ORA', 'c:ZUL') and isinstance(value, list):
                        for name, _, capture in value:
                            if name == 'save_scope_as': world.scopes[capture] = world.reference(key, actor)
                self.assertEqual(actor, world.scopes[f'sb_natal_{route}_generation_actor'])
                self.assertEqual(root, world.scopes[f'sb_natal_{route}_generation_counterparty'])
                parent = field(field(branch, 'create_container'), 'parent')
                self.assertEqual(actor, world.reference(parent, actor))


if __name__ == '__main__':
    unittest.main()
