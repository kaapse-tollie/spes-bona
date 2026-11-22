"""Execute the Klip refugee scripts. Native moves are recorded at their requested headcounts."""
from collections import Counter
import unittest
from unittest.mock import patch

from tests.test_natal_zululand_gameplay_contract import named_option, object_block
from tests.test_zulu_court_politics import CourtRuntime, EFFECTS as COURT_EFFECTS, definitions
from tests.test_zulu_institutions_laws import statements

TAGS = ('TRN', 'ORA', 'ZPB', 'LYD')
STANDARD = 'sb_trigger_natal_refugee_migration_effect'
PUNITIVE = 'sb_klip_river_move_punitive_refugees'
EFFECTS = definitions('common/scripted_effects/sb_natalia_colony_effects.txt')
EFFECTS.update(definitions('common/scripted_effects/sb_klip_river_county_effects.txt'))
EFFECTS.update(definitions('common/scripted_effects/sb_boer_leadership_effects.txt'))
POLITICS = definitions('common/scripted_triggers/sb_martinus_confederation_triggers.txt')


class RefugeeRuntime(CourtRuntime):
    def __init__(self, eligible, size=6000):
        super().__init__([])
        self.countries = {}
        self.arrivals = Counter()
        self.events = []
        self.plays = []
        for tag in (*TAGS, 'NAL', 'ZUL', 'GBR'):
            state = {'id': tag, 'pops': []}
            self.countries[tag] = {
                'id': tag, 'alive': tag in eligible or tag not in TAGS,
                'capital': state, 'states': [state], 'vars': {},
            }
        self.scopes['root'] = self.countries['GBR']
        self.port_owner = self.countries['NAL']
        for tag in ('NAL', 'ZUL'):
            self.add_pop(tag, size)
            self.add_pop(tag, 5000, culture='cu:zulu')

    def add_pop(self, tag, size, culture='cu:boer', state_index=0):
        pop = {'origin': tag, 'total_size': size, 'culture': culture, 'vars': {}}
        self.countries[tag]['states'][state_index]['pops'].append(pop)
        return pop

    def ref(self, key, scope, prev=None):
        if key == 'p:x279045.state.owner':
            return self.port_owner
        if key.startswith('c:'):
            tag, _, link = key[2:].partition('.')
            country = self.countries.get(tag)
            return self.ref(link, country) if link else country
        if key.startswith(('cu:', 'ig:', 'flag:')):
            return key
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        for key, op, value in nodes:
            if key in POLITICS:
                if self.condition(POLITICS[key], scope, prev) != (value == 'yes'):
                    return False
            elif key in ('any_scope_character', 'any_scope_war', 'any_diplomatic_play'):
                items = {'any_scope_character': scope.get('characters', []),
                         'any_scope_war': scope.get('wars', []), 'any_diplomatic_play': self.plays}[key]
                if not any(self.condition(value, item, scope) for item in items):
                    return False
            elif key == 'is_diplomatic_play_type':
                if scope['type'] != value:
                    return False
            elif not super().condition([(key, op, value)], scope, prev):
                return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, op, value = node
            if key.startswith('c:') or key == 'capital':
                target = self.ref(key, scope, prev)
                if target is not None:
                    self.effect(value, target, scope)
                elif op != '?=':
                    raise AssertionError(f'Missing required scope {key}')
            elif key in ('every_scope_state', 'every_scope_pop', 'random_scope_character'):
                collection = {'every_scope_state': 'states', 'every_scope_pop': 'pops',
                              'random_scope_character': 'characters'}[key]
                limit = next((v for k, _, v in value if k == 'limit'), [])
                for item in list(scope.get(collection, [])):
                    if self.condition(limit, item, scope):
                        self.effect([n for n in value if n[0] != 'limit'], item, scope)
                        if key == 'random_scope_character':
                            break
            elif key == 'random_character':
                limit = next(v for k, _, v in value if k == 'limit')
                people = (person for country in self.countries.values()
                          for person in country.get('characters', []))
                chosen = next((person for person in people if self.condition(limit, person, scope)), None)
                if chosen is not None:
                    self.effect([n for n in value if n[0] != 'limit'], chosen, scope)
            elif key == 'save_temporary_scope_as':
                self.scopes[value] = scope
            elif key == 'save_temporary_scope_value_as':
                fields = {k: v for k, _, v in value}
                amount = fields['value']
                self.scopes[fields['name']] = (self.calc(amount, scope, prev) if isinstance(amount, list)
                                               else self.ref(amount, scope, prev))
            elif key == 'move_partial_pop':
                fields = {k: v for k, _, v in value}
                target = self.ref(fields['state'], scope, prev)
                amount = self.ref(fields['population'], scope, prev)
                assert target is not None and amount == int(amount) and 0 < amount <= scope['total_size']
                scope['total_size'] -= int(amount)
                self.arrivals[scope['origin'], target['id'], scope['culture']] += int(amount)
            elif key == 'trigger_event':
                fields = {k: v for k, _, v in value}
                self.events.append((fields['id'], scope['id'], int(fields['days'])))
            elif key == 'transfer_character':
                scope['owner'] = self.ref(value, scope, prev)
            elif key == 'set_interest_group':
                scope['interest_group'] = self.ref(value, scope, prev)
            else:
                super().effect([node], scope, prev)

    def call(self, effect, tag):
        self.effect(EFFECTS[effect], self.countries[tag])

    def totals(self, tag):
        return tuple(self.arrivals[tag, destination, 'cu:boer'] for destination in TAGS)


@patch.dict(COURT_EFFECTS, EFFECTS)
class KlipRiverRefugeeTests(unittest.TestCase):
    def test_both_departures_with_every_set_of_living_republics(self):
        # TRN, ORA, ZPB, LYD out of 6,000 in each source. Zero means ineligible.
        cases = (
            (0, 0, 0, 0), (5700, 0, 0, 0), (0, 5700, 0, 0), (0, 0, 5700, 0), (0, 0, 0, 5700),
            (5130, 570, 0, 0), (4275, 0, 1425, 0), (4275, 0, 0, 1425),
            (0, 570, 5130, 0), (0, 570, 0, 5130), (0, 0, 2850, 2850),
            (3990, 570, 1140, 0), (3990, 570, 0, 1140), (3800, 0, 950, 950),
            (0, 570, 2565, 2565), (3610, 570, 760, 760),
        )
        for expected in cases:
            eligible = [tag for tag, amount in zip(TAGS, expected) if amount]
            for route in (STANDARD, PUNITIVE):
                with self.subTest(eligible=eligible, route=route):
                    world = RefugeeRuntime(eligible)
                    actor = 'ZUL' if route == PUNITIVE else 'GBR'
                    world.call(route, actor)
                    world.scopes = {'root': world.countries['GBR']}
                    world.call(route, actor)
                    for tag in ('NAL', 'ZUL'):
                        shares = expected if tag == 'NAL' or route == PUNITIVE else (0, 0, 0, 0)
                        self.assertEqual(shares, world.totals(tag))
                        boer, zulu = world.countries[tag]['states'][0]['pops']
                        self.assertEqual(6000 - sum(shares), boer['total_size'])
                        self.assertEqual(5000, zulu['total_size'])

    def test_missing_capital_and_whole_person_remainders(self):
        world = RefugeeRuntime(TAGS, size=10000)
        world.countries['ZPB']['capital'] = None
        world.countries['LYD']['alive'] = False
        world.call(STANDARD, 'ORA')
        self.assertEqual((8550, 950, 0, 0), world.totals('NAL'))
        self.assertEqual(500, world.countries['NAL']['states'][0]['pops'][0]['total_size'])

        for size, expected in ((1, (0, 0, 0, 0)), (2, (1, 0, 0, 0)), (8, (5, 0, 1, 1)),
                               (12, (7, 1, 2, 1)), (10000, (6017, 950, 1267, 1266))):
            with self.subTest(size=size):
                world = RefugeeRuntime(TAGS, size=size)
                world.call(STANDARD, 'TRN')
                self.assertEqual(expected, world.totals('NAL'))
        world = RefugeeRuntime(('ORA', 'ZPB', 'LYD'), size=13)
        world.call(STANDARD, 'ORA')
        self.assertEqual((0, 1, 6, 5), world.totals('NAL'))
        world = RefugeeRuntime(TAGS, size=8)
        world.countries['NAL']['states'].append({'id': 'inland Natal', 'pops': []})
        inland = world.add_pop('NAL', 12, state_index=1)
        world.call(STANDARD, 'LYD')
        self.assertEqual((12, 1, 3, 2), world.totals('NAL'))
        self.assertEqual(1, inland['total_size'])

    def test_standard_receiver_popup_and_immediate_fallback(self):
        followup = 'sb_trigger_selected_natal_refugee_receiver_followup'
        for host in TAGS:
            with self.subTest(host=host):
                world = RefugeeRuntime(TAGS)
                world.scopes['natal_refugee_receiver'] = world.countries[host]
                world.call(followup, 'NAL')
                expected = (3610, 570, 760, 760)
                if host in ('ORA', 'TRN'):
                    event_id = 'sb_natal_crisis.116' if host == 'ORA' else 'sb_natal_crisis.117'
                    self.assertEqual([(event_id, host, 1)], world.events)
                    self.assertEqual((0, 0, 0, 0), world.totals('NAL'))
                    world.countries['LYD']['capital'] = None  # Eligibility changes while the popup is open.
                    expected = (3990, 570, 1140, 0)
                    event = object_block('events/sb_natal_crisis_events.txt', event_id)
                    option = statements(named_option(event, event_id + '.a'))
                    world.scopes['root'] = world.countries[host]
                    world.effect(next(v for k, _, v in option if k == 'hidden_effect'), world.countries[host])
                else:
                    self.assertEqual([], world.events)
                self.assertEqual(expected, world.totals('NAL'))

    def test_punitive_host_controls_the_leader_and_notice(self):
        for host_survives in (True, False):
            for natal_survives in (True, False):
                with self.subTest(host_survives=host_survives, natal_survives=natal_survives):
                    world = RefugeeRuntime(('TRN', 'ORA', 'ZPB'))
                    world.countries['ZPB']['alive'] = host_survives
                    world.countries['NAL']['alive'] = natal_survives
                    world.countries['ZUL']['vars']['sb_klip_river_refugee_receiver_zpb_var'] = 1
                    home = world.countries['NAL' if natal_survives else 'ZUL']
                    leader = {'owner': home, 'alive': True, 'vars': {'sb_klip_river_deferred_exile_var': 1}}
                    home['characters'] = [leader]
                    world.call('sb_klip_river_finalize_punitive_zulu_victory', 'ZUL')
                    shares = (3990, 570, 1140, 0) if host_survives else (5130, 570, 0, 0)
                    self.assertEqual(shares, world.totals('ZUL'))
                    self.assertEqual(shares if natal_survives else (0, 0, 0, 0), world.totals('NAL'))
                    self.assertIs(world.countries['ZPB'] if host_survives else home, leader['owner'])
                    self.assertEqual([('sb_klip_river_county.082', 'ZPB', 1)] if host_survives else [], world.events)

    def test_zulu_monthly_departure_when_natal_loses_its_last_state(self):
        name = 'sb_on_klip_river_zulu_exodus_monthly'
        handler = dict((k, v) for k, _, v in statements(object_block(
            'common/on_actions/sb_regional_on_action_handlers.txt', name)))
        world = RefugeeRuntime(('TRN', 'ORA'), size=10000)
        zulu, natal = world.countries['ZUL'], world.countries['NAL']
        active = 'sb_klip_river_punitive_active_var'
        punitive = {'type': 'dp_sb_klip_river_punitive_expedition'}
        unrelated = {'type': 'dp_conquer_state'}
        zulu['vars'][active] = 1
        zulu['vars']['sb_klip_river_refugee_receiver_trn_var'] = 1
        world.port_owner = zulu
        self.assertFalse(world.condition(handler['trigger'], zulu))  # Living Natal handles its own settlement.
        natal['alive'] = False
        world.plays = [punitive]
        self.assertFalse(world.condition(handler['trigger'], zulu))
        world.plays = [unrelated]
        zulu['wars'] = [{'diplomatic_play': punitive}]
        self.assertFalse(world.condition(handler['trigger'], zulu))
        zulu['wars'] = [{'diplomatic_play': unrelated}]
        world.port_owner = world.countries['GBR']
        self.assertFalse(world.condition(handler['trigger'], zulu))
        world.port_owner = zulu
        self.assertTrue(world.condition(handler['trigger'], zulu))
        world.effect(handler['effect'], zulu)
        self.assertFalse(world.condition(handler['trigger'], zulu))
        self.assertEqual((8550, 950, 0, 0), world.totals('ZUL'))
        self.assertEqual((0, 0, 0, 0), world.totals('NAL'))
        self.assertEqual([('sb_klip_river_county.082', 'TRN', 1)], world.events)
