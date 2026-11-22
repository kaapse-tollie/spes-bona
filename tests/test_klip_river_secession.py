"""Exercise the shipped appeal and play-start branches with either defensive leader."""
import unittest
from unittest.mock import patch

from tests import test_klip_punitive_protectorate as settlement
from tests.test_blood_river_launch import LaunchContext, field
from tests.test_klip_river_colonial_delivery import EFFECTS, TRIGGERS
from tests.test_natal_zululand_gameplay_contract import (
    named_option, object_block, shortest_named_block_containing,
)
from tests.test_zulu_institutions_laws import statements

EVENTS = 'events/sb_klip_river_county_events.txt'
PREFIX = 'sb_klip_river_'
APPEAL = PREFIX + 'ora_appeal_pending_var'
PLEDGE = PREFIX + 'ora_backed_var'
PENDING = PREFIX + 'secession_delivery_pending_var'
LEASE = PREFIX + 'secession_launch_lease_var'
SETTLEMENT = PREFIX + 'secession_settlement_pending_var'


def script(path, name):
    return statements(object_block(path, name))


def natal_monthly_settlement(state):
    settlement.run_effect(PREFIX + 'cleanup_orphaned_runtime', state)
    settlement.run_effect('sb_natal_schedule_zulu_settlement', state)


class Secession(LaunchContext):
    def __init__(self):
        self.root = 'ZUL'
        self.variables = {tag: {} for tag in ('ZUL', 'NAL', 'GBR', 'KLR', 'ORA')}
        self.overlords = {'NAL': 'GBR'}
        self.natal_can_protect_zul = True
        self.wars = {tag: set() for tag in self.variables}
        self.scopes = {}
        self.plays = []
        self.truces = set()
        self.events = []

    def evaluate(self, nodes, actor):
        for key, op, value in nodes:
            if key.startswith(PREFIX):
                result = self.evaluate(script(TRIGGERS, key), actor) == (value == 'yes')
            elif key in ('initiator_is', 'target_is'):
                result = actor[key.removesuffix('_is')] == self.reference(value, actor)
            elif key in ('any_scope_target_ally', 'any_scope_initiator_ally'):
                side = key.split('_')[2]
                result = any(self.evaluate(value, tag) for tag in actor[side + '_allies'])
            elif key == 'play_participant_has_war_goal_of_type_against':
                goal = (actor, field(value, 'type'), self.reference(field(value, 'target'), actor))
                result = any(goal in play['goals'] for play in self.plays)
            elif key == 'is_subject':
                result = (actor in self.overlords) == (value == 'yes')
            elif key in ('is_direct_subject_of', 'is_subject_of'):
                result = self.overlords.get(actor) == self.reference(value, actor)
            elif key == 'can_have_as_subject':
                assert actor == 'NAL' and field(value, 'who') == 'c:ZUL'
                assert field(value, 'type') == 'subject_type_protectorate'
                result = self.natal_can_protect_zul
            elif key == 'this':
                result = actor == self.reference(value, actor)
            elif key.endswith('.state.owner'):
                owner = 'NAL' if key.startswith('p:x279045.') else 'KLR'
                result = owner == self.reference(value, actor)
            elif key == 'is_ai':
                result = value == 'no'
            else:
                result = super().evaluate([(key, op, value)], actor)
            if not result:
                return False
        return True

    def can_receive(self, event_id, recipient):
        with patch.object(self, 'root', recipient):
            return self.evaluate(field(script(EVENTS, event_id), 'trigger'), recipient)

    def apply(self, nodes, actor):
        taken = False
        for key, _, value in nodes:
            if key in ('if', 'else_if', 'else'):
                if key == 'if':
                    taken = False
                if not taken and (key == 'else' or self.evaluate(field(value, 'limit'), actor)):
                    self.apply([n for n in value if n[0] != 'limit'], actor)
                    taken = True
            elif key.startswith(('c:', 'scope:')):
                self.apply(value, self.reference(key, actor))
            elif key == 'set_variable':
                if isinstance(value, str):
                    self.variables[actor][value] = True
                else:
                    data = {k: v for k, _, v in value}
                    self.variables[actor][data['name']] = self.reference(data['value'], actor) if 'value' in data else True
            elif key == 'remove_variable':
                self.variables[actor].pop(value, None)
            elif key in ('save_scope_as', 'save_temporary_scope_as'):
                self.scopes[value] = actor
            elif key == 's:STATE_NATAL.region_state:NAL':
                self.apply(value, 'Natal state')
            elif key == 'trigger_event':
                event_id = field(value, 'id')
                if self.can_receive(event_id, actor):
                    self.events.append((actor, event_id, int(field(value, 'days'))))
            elif key in ('add_initiator_backers', 'add_target_backers'):
                side = key.split('_')[1]
                for tag, _, _ in value:
                    backer = self.reference(tag, actor)
                    assert backer != actor[side]
                    if self.overlords.get(actor[side]) == backer:
                        backer, actor[side] = actor[side], backer
                    actor[side + '_allies'].add(backer)
            elif key == 'create_diplomatic_pact':
                assert field(value, 'type') == 'protectorate'
                self.overlords[self.reference(field(value, 'country'), actor)] = actor
            elif key == 'add_war_goal':
                goal = (self.reference(field(value, 'holder'), actor), field(value, 'type'),
                        self.reference(field(value, 'target_country'), actor))
                actor['goals'].append(goal)
                if ('primary_demand', '=', 'yes') in value:
                    actor['primary_goals'].add(goal)
            elif key == PREFIX + 'create_county':
                # Start at verified creation. Province splitting and the muster have separate tests.
                creation = object_block(EFFECTS, key)
                success = statements(shortest_named_block_containing(creation, 'if', 'effect_starting_politics_conservative'))
                county_setup = next(i for i, entry in enumerate(success) if entry[0] == 'c:KLR')
                self.apply(success[county_setup + 1:], actor)
            elif key not in ('sb_court_klip_broker', PREFIX + 'roll_coalition_boost'):
                self.apply(script(EFFECTS, key), actor)

    def recognise_county(self):
        event = object_block(EVENTS, 'sb_klip_river_county.020')
        option = named_option(event, 'sb_klip_river_county.020.b')
        self.apply(field(statements(option), 'hidden_effect'), 'ZUL')

    def answer(self, support):
        self.root = 'ORA'
        event = object_block(EVENTS, 'sb_klip_river_county.004')
        option = named_option(event, 'sb_klip_river_county.004.' + ('a' if support else 'b'))
        for key, _, nodes in statements(option):
            if key == 'hidden_effect':
                self.apply(nodes, 'ORA')
        self.apply(field(statements(event), 'after'), 'ORA')

    def opening(self, leader):
        play = dict(type='dp_sb_klip_river_secession', initiator='ZUL', target=leader, initiator_allies=set(),
                    target_allies={'NAL'} if leader == 'GBR' else set(), goals=[('ZUL', 'annex_country', 'NAL')],
                    primary_goals={('ZUL', 'annex_country', 'NAL')})
        self.plays.append(play)
        self.root = play
        self.scopes.update(initiator='ZUL', target=leader)
        self.variables['ZUL'][LEASE] = True
        return play


class KlipRiverSecessionTests(unittest.TestCase):
    def test_appeal_controls_ora_but_klip_always_joins(self):
        configure = field(script(EFFECTS, PREFIX + 'configure_started_play'), 'if')
        settlement = object_block(EFFECTS, PREFIX + 'finalize_reduced_natalia')
        protectorate = statements(shortest_named_block_containing(settlement, 'if', 'create_diplomatic_pact'))
        for leader in ('NAL', 'GBR'):
            for decision in ('accept', 'decline', 'unavailable', 'subjugated_after_acceptance'):
                with self.subTest(leader=leader, decision=decision):
                    world = Secession()
                    if decision == 'unavailable':
                        del world.variables['ORA']
                    world.recognise_county()
                    if decision != 'unavailable':
                        self.assertEqual([('ORA', 'sb_klip_river_county.004', 6)], world.events)
                        self.assertTrue(world.can_receive('sb_klip_river_county.004', 'ORA'))
                        world.apply(script(EFFECTS, PREFIX + 'queue_secession_delivery'), 'NAL')
                        self.assertEqual(1, len(world.events))
                        world.answer(decision in ('accept', 'subjugated_after_acceptance'))
                    if decision == 'subjugated_after_acceptance':
                        world.overlords['ORA'] = 'GBR'
                    self.assertEqual([('NAL', 'sb_klip_river_county.050', 1)],
                                     [event for event in world.events if event[0] == 'NAL'])
                    self.assertNotIn(APPEAL, world.variables['NAL'])
                    play = world.opening(leader)
                    self.assertTrue(world.evaluate(field(configure, 'limit'), play))
                    world.apply([n for n in configure if n[0] != 'limit'], play)
                    self.assertEqual({'KLR', 'ORA'} if decision == 'accept' else {'KLR'}, play['initiator_allies'])
                    self.assertEqual('GBR', play['target'])
                    self.assertEqual({'NAL'}, play['target_allies'])
                    self.assertEqual('ORA' if decision == 'accept' else None, world.overlords.get('KLR'))
                    self.assertEqual(decision == 'accept', PLEDGE in world.variables['KLR'])
                    self.assertEqual([('ZUL', 'annex_country', 'NAL'), ('NAL', 'annex_country', 'KLR'),
                                      ('NAL', 'make_protectorate', 'ZUL')], play['goals'])
                    self.assertIn(('NAL', 'make_protectorate', 'ZUL'), play['primary_goals'])
                    self.assertIn(SETTLEMENT, world.variables['NAL'])
                    self.assertIs(play, world.variables['NAL'][PREFIX + 'secession_play_scope'])
                    self.assertEqual('NAL', world.variables['NAL'][PREFIX + 'secession_target_scope'])
                    self.assertNotIn(PENDING, world.variables['NAL'])
                    self.assertFalse(world.evaluate(field(configure, 'limit'), play))
                    # If the wartime pact lapses, victory only restores it for an actual backer.
                    world.overlords.pop('KLR', None)
                    world.overlords.pop('ORA', None)
                    self.assertEqual(decision == 'accept', world.evaluate(field(protectorate, 'limit'), 'KLR'))

    def test_britain_presses_only_the_protectorate_if_natal_cannot_hold_it(self):
        configure = field(script(EFFECTS, PREFIX + 'configure_started_play'), 'if')
        for leader in ('NAL', 'GBR'):
            with self.subTest(leader=leader):
                world = Secession()
                world.variables['NAL'][PENDING] = True
                world.natal_can_protect_zul = False
                play = world.opening(leader)
                world.apply([('if', '=', configure)], play)
                self.assertEqual([('ZUL', 'annex_country', 'NAL'), ('NAL', 'annex_country', 'KLR'),
                                  ('GBR', 'make_protectorate', 'ZUL')], play['goals'])
                self.assertIn(('GBR', 'make_protectorate', 'ZUL'), play['primary_goals'])

    def test_government_choice_follows_the_settled_secession_terms(self):
        government = 'sb_natal_interwar.030'
        event = dict(settlement.expression(object_block('events/sb_natal_interwar_events.txt', government)))
        for holder in ('NAL', 'GBR', 'FRA', None):
            for county in ('annexed', 'independent', 'missing_province', 'survives_elsewhere'):
                with self.subTest(holder=holder, county=county):
                    state = settlement.world()
                    active = PREFIX + 'secession_active_var'
                    state['flags'] = {active, SETTLEMENT}
                    state['county_alive'] = county in ('independent', 'survives_elsewhere')
                    state['owners']['xBBCA32'] = {'independent': 'KLR', 'missing_province': 'ORA'}.get(county, 'NAL')
                    if holder:
                        settlement.subjugate(state, holder)

                    natal_monthly_settlement(state)
                    self.assertEqual([], state['events'])
                    self.assertEqual(holder, state['overlord'])
                    state['flags'].remove(active)  # Exact play's terminal cleanup.
                    state.update(war=False, play=False)
                    natal_monthly_settlement(state)
                    natal_monthly_settlement(state)
                    won = holder in ('NAL', 'GBR') and county == 'annexed'
                    self.assertEqual('NAL' if won else holder, state['overlord'])
                    self.assertEqual([(government, 'NAL')] if won else [],
                                     [(event_id, tag) for event_id, tag, _ in state['events']])
                    self.assertEqual(won, settlement.evaluate(event['trigger'], state))
                    self.assertNotIn(SETTLEMENT, state['flags'])

    def test_british_handoff_waits_for_klip_and_a_partial_peace_cannot_claim_a_later_conquest(self):
        british = object_block(settlement.ZUL, 'sb_zululand_under_british_postwar_control')
        natal_gate = dict(settlement.expression(british))['c:NAL']
        state = settlement.world()
        state['flags'] = {SETTLEMENT, 'sb_natalia_british_colony_resolved_var'}
        settlement.subjugate(state, 'GBR')
        state.update(county_alive=True, war=False, play=False)
        self.assertFalse(settlement.evaluate(natal_gate, state, actor='NAL', root='GBR'))
        natal_monthly_settlement(state)
        self.assertTrue(settlement.evaluate(natal_gate, state, actor='NAL', root='GBR'))
        state['county_alive'] = False
        state['owners']['xBBCA32'] = 'NAL'
        natal_monthly_settlement(state)
        self.assertEqual('GBR', state['overlord'])
        self.assertEqual([], state['events'])

    def test_exact_war_end_and_late_peace_terms_reach_the_same_natal_event(self):
        end = field(script(EFFECTS, PREFIX + 'handle_war_end'), 'if')
        world = Secession()
        play = world.opening('GBR')
        world.variables['NAL'].update({PREFIX + 'secession_play_scope': play, PREFIX + 'secession_active_var': True})
        guard = field(end, 'limit')
        for actor in ('ZUL', 'ORA'):
            world.scopes['actor'] = actor
            self.assertTrue(world.evaluate(guard, play))
        world.root = 'unrelated_play'
        self.assertFalse(world.evaluate(guard, play))

        # Run the actual country-scoped settlement call with the play as foreign ROOT.
        reconcile = PREFIX + 'reconcile_secession_settlement'
        end_call = next(nodes for key, _, nodes in end if key == 'c:NAL' and nodes[0][0] == reconcile)
        for last in ('county', 'protectorate', 'neither'):
            state = settlement.world()
            state['flags'] = {SETTLEMENT}
            state['county_alive'] = last == 'county'
            state['owners']['xBBCA32'] = 'KLR' if state['county_alive'] else 'NAL'
            if last != 'protectorate':
                settlement.subjugate(state, 'GBR')
            settlement.run_effect(reconcile, state, root='secession play',
                                  nodes=[(key, value) for key, _, value in end_call])
            self.assertEqual(last == 'neither', bool(state['events']))
            state['owners']['xBBCA32'] = 'NAL'
            state['county_alive'] = False
            if last == 'protectorate':
                settlement.subjugate(state, 'GBR')
            natal_monthly_settlement(state)
            self.assertEqual('NAL', state['overlord'])
            self.assertEqual([('sb_natal_interwar.030', 'NAL')], [(e[0], e[1]) for e in state['events']])

    def test_a_delayed_british_transfer_keeps_the_earned_settlement(self):
        state = settlement.world()
        state['flags'] = {SETTLEMENT}
        state['owners']['xBBCA32'] = 'NAL'
        settlement.subjugate(state, 'GBR')
        state.update(war=False, play=False, transfer_succeeds=False)
        natal_monthly_settlement(state)
        self.assertIn(SETTLEMENT, state['flags'])
        self.assertEqual([], state['events'])
        state['transfer_succeeds'] = True
        natal_monthly_settlement(state)
        self.assertEqual('NAL', state['overlord'])
        self.assertEqual([('sb_natal_interwar.030', 'NAL')], [(e[0], e[1]) for e in state['events']])

    def test_a_late_flag_cannot_recover_an_unqueued_appeal(self):
        event_id = 'sb_klip_river_county.004'
        creation = object_block(EFFECTS, PREFIX + 'create_county')
        dispatch = statements(shortest_named_block_containing(creation, 'c:ORA', event_id))
        for present, missing in ((APPEAL, PENDING), (PENDING, APPEAL)):
            with self.subTest(missing=missing):
                world = Secession()
                natal = world.variables['NAL']
                natal[present] = True
                world.apply(dispatch, 'ORA')
                natal[missing] = True
                self.assertTrue(world.can_receive(event_id, 'ORA'))
                self.assertEqual([], world.events)

    def test_duplicate_guard_and_callback_agree_on_defenders(self):
        preflight = script(TRIGGERS, PREFIX + 'secession_preflight')
        duplicates = next(value for key, _, value in preflight if key == 'NOT' and value[0][0] == 'any_diplomatic_play')
        configure = field(field(script(EFFECTS, PREFIX + 'configure_started_play'), 'if'), 'limit')
        for leader, allies, parent, expected in (
            ('NAL', set(), 'GBR', True), ('GBR', {'NAL'}, 'GBR', True),
            ('GBR', set(), 'GBR', False), ('GBR', {'NAL'}, 'FRA', False), ('FRA', {'NAL'}, 'GBR', False),
        ):
            with self.subTest(leader=leader, allies=allies, parent=parent):
                world = Secession()
                world.variables['NAL'][PENDING] = True
                world.overlords['NAL'] = parent
                play = world.opening(leader)
                play['target_allies'] = allies
                self.assertEqual(expected, world.evaluate(duplicates, 'NAL'))
                self.assertEqual(expected, world.evaluate(configure, play))
                play['goals'] = [('ZUL', 'annex_country', 'GBR')]
                self.assertFalse(world.evaluate(duplicates, 'NAL'))
                self.assertFalse(world.evaluate(configure, play))
                play['goals'] = [('ZUL', 'annex_country', 'NAL')]
                play['type'] = 'dp_annex_war'
                self.assertFalse(world.evaluate(duplicates, 'NAL'))

    def test_held_appeal_cannot_pledge_or_restart_after_ora_becomes_ineligible(self):
        world = Secession()
        world.recognise_county()
        self.assertEqual([('ORA', 'sb_klip_river_county.004', 6)], world.events)
        world.overlords['ORA'] = 'GBR'
        self.assertFalse(world.can_receive('sb_klip_river_county.004', 'ORA'))
        world.apply(script(EFFECTS, PREFIX + 'queue_secession_delivery'), 'NAL')
        self.assertNotIn(APPEAL, world.variables['NAL'])
        self.assertEqual(('NAL', 'sb_klip_river_county.050', 1), world.events[-1])
        before = list(world.events)
        world.answer(True)
        self.assertNotIn(PLEDGE, world.variables['ORA'])
        self.assertEqual(before, world.events)

    def test_launch_lease_belongs_to_zul_and_backdown_belongs_to_the_tracked_play(self):
        world = Secession()
        world.variables['NAL'][PENDING] = True
        launch = field(field(script(EFFECTS, PREFIX + 'start_secession_play'), 'if'), 'limit')
        self.assertTrue(world.evaluate(launch, 'NAL'))
        world.variables['ZUL'][LEASE] = True
        self.assertFalse(world.evaluate(launch, 'NAL'))

        defence = field(field(script(EFFECTS, PREFIX + 'handle_backdown'), 'if'), 'limit')
        play = world.opening('GBR')
        world.variables['NAL'][PREFIX + 'secession_play_scope'] = play
        world.scopes['actor'] = 'GBR'
        self.assertTrue(world.evaluate(defence, play))
        world.scopes['actor'] = 'ORA'
        self.assertFalse(world.evaluate(defence, play))
        world.scopes['actor'] = 'GBR'
        world.root = 'unrelated_play'
        self.assertFalse(world.evaluate(defence, play))
