"""Execute the sale and river hooks. Fixtures supply the native border split and Pop merges."""
from copy import deepcopy
from itertools import product
import re
import unittest
from unittest.mock import patch

from tests.test_klip_river_refugees import RefugeeRuntime
from tests.test_natal_zululand_gameplay_contract import named_option, object_block
from tests.test_zulu_court_politics import CourtRuntime, EFFECTS, TRIGGERS, definitions
from tests.test_zulu_institutions_laws import statements


SALE = definitions('common/scripted_effects/sb_swazi_effects.txt')
OUTSIDE = 'sb_swazi_district_has_outside_owner'
HOOKS = definitions('common/on_actions/sb_orange_river.txt')
RIVER = 'state_trait_sb_orange_river'
REGIONS = ('NORTHERN_CAPE', 'BECHUANALAND', 'GRIQUALAND_WEST', 'NAMAQUALAND')
DISTRICTS = ('x73CDE8', 'x25A652', 'x50A011', 'x452304')
EVENTS = 'events/sb_swazi_border_events.txt'


def fields(nodes):
    return {key: value for key, _, value in nodes}


class BorderRuntime(RefugeeRuntime):
    def __init__(self):
        CourtRuntime.__init__(self, [])
        self.countries = {tag: {'id': tag, 'vars': {}} for tag in ('SWZ', 'TRN', 'CAP')}
        self.fragments = {tag: {'id': tag, 'pops': []} for tag in self.countries}
        self.regions = {name: {'id': name, 'traits': [], 'states': []}
                        for name in (*REGIONS, 'BOTSWANA', 'EAST_TRANSVAAL')}
        self.districts = dict.fromkeys(DISTRICTS, 'SWZ')
        self.lots = {district: [] for district in DISTRICTS}
        self.people = []
        self.cultures = {}
        self.religions = {}
        self.locals = {}
        self.maps = {}
        self.lists = {}
        self.moves = []
        self.grants = []
        self.hidden = 0
        self.loses_last_province = False

    def pop(self, tag, culture, faith, size):
        pop = {'id': len(self.people), 'total_size': size,
               'culture': self.cultures.setdefault(culture, {'id': culture}),
               'religion': self.religions.setdefault(faith, {'id': faith})}
        self.people.append(pop)
        self.fragments[tag]['pops'].append(pop)
        return pop

    def ref(self, key, scope, prev=None):
        key = key.strip('"')
        if key.startswith('p:'):
            return self.countries[self.districts[key.split('.')[0][2:]]]
        if key.startswith('region_state:'):
            return self.fragments.get(key.split(':')[1])
        if key.startswith('s:STATE_'):
            return self.regions[key[8:]]
        if key.startswith('local_var:'):
            return self.locals[key[10:]]
        lookup = re.fullmatch(r'(culture\.variable_map|local_variable_map)\((\w+)\|([^)]*)\)', key)
        if lookup:
            kind, name, target = lookup.groups()
            maps = self.maps if kind == 'local_variable_map' else scope['culture']['maps']
            return maps[name][self.ref(target, scope, prev)['id']]
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        for key, op, value in nodes:
            if key == 'has_variable_map':
                ok = value in scope.get('maps', {})
            elif key in ('is_key_in_variable_map', 'is_key_in_local_variable_map'):
                args = fields(value)
                maps = self.maps if key == 'is_key_in_local_variable_map' else scope.get('maps', {})
                ok = self.ref(args['target'], scope, prev)['id'] in maps.get(args['name'], {})
            elif key == 'has_state_trait':
                ok = value in scope['region']['traits']
            else:
                ok = super().condition([(key, op, value)], scope, prev)
            if not ok:
                return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, op, value = node
            args = fields(value) if isinstance(value, list) else {}
            if key == 'hidden_effect':
                self.hidden += 1
                self.effect(value, scope, prev)
                self.hidden -= 1
            elif key.startswith(('s:STATE_', 'region_state:')) or key in ('culture', 'religion'):
                target = self.ref(key, scope, prev)
                if target is not None:
                    self.effect(value, target, scope)
                else:
                    assert op == '?='
            elif key == 'set_local_variable':
                val = args['value']
                self.locals[args['name']] = self.calc(val, scope, prev) if isinstance(val, list) else self.ref(val, scope, prev)
            elif key == 'change_local_variable':
                name = args.pop('name')
                operation, operand = next(iter(args.items()))
                amount = self.ref(operand, scope, prev)
                if operation == 'add':
                    self.locals[name] += amount
                elif operation == 'subtract':
                    self.locals[name] -= amount
                else:
                    assert operation == 'modulo'
                    self.locals[name] %= amount
            elif key in ('add_to_variable_map', 'add_to_local_variable_map'):
                maps = self.maps if key == 'add_to_local_variable_map' else scope.setdefault('maps', {})
                target = self.ref(args['key'], scope, prev)['id']
                entries = maps.setdefault(args['name'], {})
                assert target not in entries
                entries[target] = self.ref(args['value'], scope, prev)
            elif key == 'remove_from_variable_map':
                del scope['maps'][args['name']][self.ref(args['key'], scope, prev)['id']]
            elif key == 'clear_variable_map':
                scope.get('maps', {}).pop(value, None)
            elif key == 'add_to_temporary_list':
                self.lists.setdefault(value, []).append(scope)
            elif key == 'every_in_list':
                for item in self.lists.get(args['list'], []):
                    if self.condition(args.get('limit', []), item, scope):
                        self.effect([n for n in value if n[0] not in ('list', 'limit')], item, scope)
            elif key == 'set_owner_of_provinces':
                assert scope is self.regions['EAST_TRANSVAAL'] and args['country'] == 'c:TRN'
                districts = [district for token, _, _ in args['provinces'] for district in token.strip('"').split()]
                changing = tuple(district for district in districts if self.districts[district] != 'TRN')
                if changing:
                    self.grants.append(changing)
                for district in districts:
                    if self.districts[district] != 'TRN':
                        self.fragments.setdefault('TRN', {'id': 'TRN', 'pops': []})
                        for donor, receiver, count in self.lots[district]:
                            if all(pop is not receiver for pop in self.fragments['TRN']['pops']):
                                self.fragments['TRN']['pops'].append(receiver)
                            donor['total_size'] -= count
                            receiver['total_size'] += count
                        self.districts[district] = 'TRN'
                if self.loses_last_province and 'SWZ' not in self.districts.values():
                    self.fragments.pop('SWZ', None)
            elif key == 'move_partial_pop':
                count = self.ref(args['population'], scope, prev)
                assert self.hidden and 0 < count <= scope['total_size'] and int(count) == count
                assert self.ref(args['state'], scope, prev) is self.fragments['SWZ']
                self.moves.append((scope['id'], int(count)))
                scope['total_size'] -= count
                self.pop('SWZ', scope['culture']['id'], scope['religion']['id'], count)
            elif key == 'add_state_trait':
                scope['traits'].append(value)
            elif key in ('remove_claim', 'change_relations', 'create_bidirectional_truce', 'custom_description',
                         'sb_create_trn_swz_firearms_treaty', 'sb_swazi_apply_guns_for_land_bonus'):
                continue
            else:
                super().effect([node], scope, prev)

    def accept(self):
        self.scopes = {'root': self.countries['TRN']}
        self.locals.clear()
        self.lists.clear()
        self.maps.clear()
        option = statements(named_option(object_block(EVENTS, 'sb_swazi_border.3'), 'sb_swazi_border.3.a'))
        self.effect([n for n in option if n[0] == 'c:SWZ'], self.scopes['root'])


@patch.dict(EFFECTS, SALE)
@patch.dict(TRIGGERS, {OUTSIDE: definitions('common/scripted_triggers/sb_swazi_triggers.txt')[OUTSIDE]})
class SwaziFoodSecurityTests(unittest.TestCase):
    def test_all_partial_ownerships_keep_each_native_split_together(self):
        for owners in product(('SWZ', 'TRN', 'CAP'), repeat=4):
            with self.subTest(owners=owners):
                world = BorderRuntime()
                world.districts.update(zip(DISTRICTS, owners))
                expected = [tuple(d for d in DISTRICTS if world.districts[d] == seller) for seller in ('CAP', 'SWZ')]
                world.accept()
                self.assertEqual(world.grants, [batch for batch in expected if batch])

    def test_merged_transvaal_residents_and_held_acceptance(self):
        world = BorderRuntime()
        seller = world.pop('SWZ', 'swazi', 'animist', 10000)
        buyer = world.pop('TRN', 'swazi', 'animist', 138681)
        world.lots[DISTRICTS[0]] = [(seller, buyer, 4000)]
        for replay in (deepcopy(world), world):
            replay.accept()
            replay.accept()
            self.assertEqual(replay.moves, [(buyer['id'], 2000)])
            self.assertEqual(sum(p['total_size'] for p in replay.fragments['SWZ']['pops']), 8000)
            self.assertEqual(replay.people[buyer['id']]['total_size'], 140681)
            self.assertTrue(all(not culture.get('maps') for culture in replay.cultures.values()))

    def test_odd_heads_across_cultures_and_faiths_and_third_party(self):
        world = BorderRuntime()
        for i, (culture, faith, n) in enumerate((('swazi', 'animist', 3), ('swazi', 'protestant', 1), ('tsonga', 'animist', 1))):
            seller = world.pop('SWZ', culture, faith, n + 5)
            buyer = world.pop('TRN', culture, faith, 100)
            world.lots[DISTRICTS[i]].append((seller, buyer, n))
        outside = world.pop('CAP', 'swazi', 'protestant', 501)
        world.districts[DISTRICTS[3]] = 'CAP'
        world.lots[DISTRICTS[3]].append((outside, world.people[3], 501))
        old_total = sum(p['total_size'] for p in world.people)
        unrelated = world.pop('TRN', 'swazi', 'catholic', 5000)
        world.accept()
        self.assertEqual(world.moves, [(1, 1), (3, 1)])
        self.assertEqual(unrelated['total_size'], 5000)
        self.assertEqual(world.people[3]['total_size'], 601)
        self.assertEqual(sum(p['total_size'] for p in world.people), old_total + 5000)

    def test_new_fragment_no_remnant_and_terminal_sale(self):
        for missing_remnant, resolved, expected in ((False, False, 2), (True, False, 0), (False, True, 0)):
            world = BorderRuntime()
            world.fragments.pop('TRN')
            world.loses_last_province = missing_remnant
            if resolved:
                world.countries['SWZ']['vars']['sb_swazi_boer_pressure_resolved_var'] = 1
            seller = world.pop('SWZ', 'tsonga', 'animist', 5)
            # The recipient fragment and its first Pop are created by the native transfer.
            buyer = dict(seller, id=99, total_size=0)
            world.lots[DISTRICTS[0]] = [(seller, buyer, 5)]
            world.accept()
            self.assertEqual(sum(n for _, n in world.moves), expected)
        self.assertNotIn('sb_swazi_apply_boer_buy_time_settlement', named_option(object_block(EVENTS, 'sb_swazi_border.3'), 'sb_swazi_border.3.b'))

    def test_no_swazi_transfer_and_silent_acceptance(self):
        world = BorderRuntime()
        world.pop('SWZ', 'swazi', 'animist', 6000)
        resident = world.pop('TRN', 'swazi', 'animist', 10000)
        world.districts = dict.fromkeys(DISTRICTS, 'TRN')
        world.accept()
        self.assertEqual((world.moves, resident['total_size']), ([], 10000))

        region = fields(SALE['sb_swazi_settle_boer_frontier'])['s:STATE_EAST_TRANSVAAL']
        visible = [node for node in region if node[0] != 'hidden_effect']
        self.assertEqual([key for key, _, _ in visible], ['set_owner_of_provinces', 'remove_claim'])
        provinces = fields(fields(visible)['set_owner_of_provinces'])['provinces']
        self.assertEqual(tuple(province for province, _, _ in provinces), DISTRICTS)
        offer = named_option(object_block(EVENTS, 'sb_swazi_border.2'), 'sb_swazi_border.2.a')
        self.assertIn('id = sb_swazi_border.3 days = 5', offer)
        self.assertNotIn('sb_swazi_count_cession', offer)

    def test_orange_river_start_backfill_and_new_owner(self):
        trait = fields(definitions('common/state_traits/sb_state_traits.txt')[RIVER])
        self.assertEqual(trait['modifier'], [('building_subsistence_output_mult', '=', '0.05')])
        self.assertTrue(trait['icon'].endswith('/river.dds"'))
        for hook in ('on_game_started', 'on_monthly_pulse'):
            world = BorderRuntime()
            for region in world.regions.values():
                region['states'] = [{'region': region}]
            if hook == 'on_monthly_pulse':
                world.regions['NORTHERN_CAPE']['traits'].append(RIVER)
            for entry in (hook, 'on_monthly_pulse'):
                for action, _, _ in fields(HOOKS[entry])['on_actions']:
                    body = fields(HOOKS[action])
                    if world.condition(body['trigger'], {}):
                        world.effect(body['effect'], {})
            for name in REGIONS:
                self.assertEqual(world.regions[name]['traits'], [RIVER])
            bechuanaland = world.regions['BECHUANALAND']
            bechuanaland['states'].append({'region': bechuanaland})
            self.assertTrue(all(world.condition([('has_state_trait', '=', RIVER)], state) for state in bechuanaland['states']))
            self.assertEqual(world.regions['BOTSWANA']['traits'], [])
