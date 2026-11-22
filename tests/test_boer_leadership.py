"""Execute the leadership handoffs with native character offices and delayed deliveries modelled."""
from copy import deepcopy
from datetime import date
import unittest
from unittest.mock import patch

from tests.test_klip_river_refugees import COURT_EFFECTS, EFFECTS, RefugeeRuntime
from tests.test_natal_zululand_gameplay_contract import named_option, object_block, object_block_from_source
from tests.test_zulu_court_politics import GAME, definitions
from tests.test_zulu_institutions_laws import statements

EVENTS = 'events/sb_boer_republics_events.txt'
TREK = 'common/scripted_effects/sb_trek_migration.txt'
NATAL = 'common/scripted_effects/sb_natalia_effects.txt'
HISTORY = 'common/history/characters/ora - oranje.txt'
TEMPLATES = 'common/character_templates/sb_southern_africa_character_template_overrides.txt'
BIRTHDAY = 'sb_marthinus_35th_birthday'
MANDATE = 'sb_marthinus_groot_boere_mandate'
SON = 'TRN_marthinus_wessel_pretorius'
FATHER = 'TRN_andries_pretorius'
HENDRIK = 'ORA_hendrik_potgieter'
SCHOEMAN = 'TRN_stephanus_schoeman'
LO, AF = 'ig_landowners', 'ig_armed_forces'
ADOPT = 'sb_boer_republics.130'
APPOINT = 'sb_boer_republics.132'
RETURN = 'sb_boer_republics.133'
BIRTHDAY_EFFECT = dict((k, v) for k, _, v in definitions(
    'common/on_actions/sb_boer_story_on_action_handlers.txt')[BIRTHDAY])['effect']
START = statements(object_block(HISTORY, 'c:ORA ?'))


def fields(nodes):
    return {k: v for k, _, v in nodes}


def option(event, choice='a', path=EVENTS):
    return statements(named_option(object_block(path, event), event + '.' + choice))


def founder_offices(path, effect):
    """Extract the contiguous character transaction from the actual, larger territory grant."""
    def search(nodes):
        keys = [n[0] for n in nodes]
        if 'sb_receive_boer_founder' in keys:
            first = keys.index('sb_receive_boer_founder')
            last = first
            while last < len(nodes):
                name, _, body = nodes[last]
                if name not in ('sb_receive_boer_founder', 'sb_receive_klip_boer_return') and not (
                    name.startswith('scope:sb_') or name in ('if', 'else') and 'sb_northern_' in str(body)
                ):
                    break
                last += 1
            return nodes[first:last]
        for _, _, body in nodes:
            if isinstance(body, list) and (found := search(body)):
                return found
    result = search(statements(object_block(path, effect)))
    assert result, effect
    return result


class LeadershipRuntime(RefugeeRuntime):
    def __init__(self, eligible=('TRN', 'ORA')):
        super().__init__(eligible, size=10000)
        self.countries['CAP'] = {'id': 'CAP', 'alive': True, 'vars': {}}
        for country in self.countries.values():
            country.update(characters=[], groups={})
        self.people = {}
        self.deliveries = {}
        self.rewards = []
        self.youth_removals = 0
        self.host = 'TRN'

    def ref(self, key, scope, prev=None):
        if scope is not None and key.startswith('ig:'):
            name, _, tail = key[3:].partition('.')
            group = scope['groups'].setdefault(name, {'type': name})
            return self.ref(tail, group) if tail else group
        return super().ref(key, scope, prev)

    def person(self, tag, template, group=LO):
        assert template not in self.people
        country = self.countries[tag]
        actor = dict(id=template, template=template, owner=country, alive=True, vars={}, traits=set(),
                     interest_group=self.ref('ig:' + group, country), age=16 if template == SON else 40)
        country['characters'].append(actor)
        self.people[template] = actor
        return actor

    def condition(self, nodes, scope, prev=None):
        for key, op, value in nodes:
            if key == 'is_interest_group_leader':
                result = (scope['interest_group'].get('leader') is scope) == (value == 'yes')
            elif key == 'is_template_used':
                result = value in self.people
            elif key == 'NAND':
                result = not self.condition(value, scope, prev)
            elif key == 'any_scope_treaty':
                result = False  # No test countries have pre-existing treaties.
            else:
                result = super().condition([(key, op, value)], scope, prev)
            if not result:
                return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, op, value = node
            if key in ('name', 'ai_chance', 'default_option', 'custom_tooltip'):
                continue
            if key == 'trigger_event':
                args = fields(value)
                destination = args.get('id') or args['on_action']
                self.events.append((destination, scope['id'], int(args['days'])))
                self.deliveries[destination] = (scope, self.scopes.copy())
            elif key == 'transfer_character':
                owner = self.ref(value, scope, prev)
                old = scope['owner']['characters']
                old[:] = [person for person in old if person is not scope]
                owner['characters'].append(scope)
                scope['owner'] = owner
            elif key == 'add_character_role':
                scope[value] = True
            elif key == 'remove_character_role':
                if value == 'ruler':
                    scope['owner']['ruler'] = None
                scope[value] = False
            elif key in ('set_as_interest_group_leader', 'remove_as_interest_group_leader'):
                scope['interest_group']['leader'] = scope if key == 'set_as_interest_group_leader' else None
            elif key == 'remove_trait' and value == 'sb_youth':
                scope['traits'].remove(value)
                self.youth_removals += 1
            elif key == 'add_trait':
                scope['traits'].add(value)
            elif key == 'add_modifier' and fields(value)['name'] == MANDATE:
                duration = int(fields(value)['months'])
                scope.setdefault('modifiers', {})[MANDATE] = duration
                self.rewards.append((scope['id'], duration))
            elif key == 'random_country':
                chosen = self.countries.get(self.host)
                if chosen and self.condition(fields(value)['limit'], chosen, scope):
                    self.effect([n for n in value if n[0] != 'limit'], chosen, scope)
            elif key == 'create_character':
                args = fields(value)
                person = self.person(scope['id'], args['template'], args['interest_group'])
                self.effect(args['on_created'], person, scope)
            else:
                super().effect([node], scope, prev)

    def deliver(self, event):
        country, saved = self.deliveries[event]
        self.scopes = dict(saved, root=country)
        if event == BIRTHDAY:
            self.effect(BIRTHDAY_EFFECT, country)
        else:
            path = {
                'sb_natal_crisis': 'events/sb_natal_crisis_events.txt',
                'sb_klip_river_county': 'events/sb_klip_river_county_events.txt',
                'sb_boer_republics': EVENTS,
            }[event.split('.')[0]]
            self.effect(option(event, path=path), country)

    def advance_months(self, person, months):
        modifiers = person.get('modifiers', {})
        for name, remaining in list(modifiers.items()):
            if months >= remaining:
                del modifiers[name]
            else:
                modifiers[name] = remaining - months

    def adopt(self, choice='a'):
        self.scopes = {'root': self.countries['TRN']}
        self.effect(option(ADOPT, choice), self.countries['TRN'])

    def depart(self, route):
        self.scopes = {'root': self.countries['GBR']}
        if route == 'ordinary':
            self.call('sb_klip_river_execute_standard_boer_flight', 'NAL')
        else:
            self.countries['ZUL']['vars']['sb_klip_river_refugee_receiver_' + self.host.lower() + '_var'] = 1
            self.call('sb_klip_river_finalize_punitive_zulu_victory', 'ZUL')


@patch.dict(COURT_EFFECTS, {**EFFECTS, **definitions('common/scripted_effects/sb_boer_commandant_effects.txt')})
class BoerLeadershipTests(unittest.TestCase):
    def new_son(self, world, tag='TRN'):
        son = world.person('ORA', SON)
        start = next(fields(v) for k, _, v in START if k == 'create_character' and fields(v)['template'] == SON)
        world.effect(start['on_created'], son)
        if tag != 'ORA':
            world.effect([('sb_move_boer_politician', '=', [('TAG', '=', tag), ('GROUP', '=', LO)])], son)
        return son

    def test_cast_transfers_and_founders_in_either_order(self):
        starts = {fields(body)['template']: fields(body) for k, _, body in START if k == 'create_character'}
        self.assertEqual({HENDRIK, SCHOEMAN, SON, FATHER, 'ORA_gerrit_maritz', 'ORA_piet_retief'}, set(starts))
        self.assertEqual(('yes', 'yes', LO), (starts['ORA_gerrit_maritz']['ruler'],
                         fields(statements(object_block(TEMPLATES, 'ORA_gerrit_maritz')))['ig_leader'],
                         fields(statements(object_block(TEMPLATES, 'ORA_gerrit_maritz')))['interest_group']))
        self.assertEqual(('no', 'yes', AF), tuple(starts[HENDRIK][k] for k in ('ruler', 'ig_leader', 'interest_group')))
        west = founder_offices(TREK, 'sb_spawn_transvaal_republic_v2')
        natal = founder_offices(NATAL, 'sb_found_natalia_after_blood_river')
        north = founder_offices(TREK, 'sb_found_zoutpansberg_republic')
        east = founder_offices(TREK, 'sb_found_lydenburg_republic')
        for natal_first in (True, False):
            for hendrik_survives in (True, False):
                with self.subTest(natal_first=natal_first, hendrik_survives=hendrik_survives):
                    world = LeadershipRuntime()
                    son = self.new_son(world, 'ORA')
                    father = world.person('ORA', FATHER)
                    hendrik = world.person('ORA', HENDRIK, AF)
                    schoeman = world.person('ORA', SCHOEMAN, AF)
                    trn = world.countries['TRN']
                    if natal_first:
                        world.effect(natal, world.countries['NAL'])
                    world.effect(west, trn)
                    self.assertIs(trn['ruler'], hendrik)
                    self.assertIs(world.ref('ig:' + AF + '.leader', trn), hendrik)
                    self.assertIs(trn, son['owner'])
                    self.assertIn('sb_youth', son['traits'])
                    self.assertIs(trn, schoeman['owner'])
                    if not natal_first:
                        self.assertIs(world.ref('ig:' + LO + '.leader', trn), father)
                        world.effect(natal, world.countries['NAL'])
                    self.assertIs(world.countries['NAL']['ruler'], father)
                    hendrik['alive'] = hendrik_survives
                    north_country = world.countries['ZPB']
                    world.effect(north, north_country)
                    self.assertIs(north_country['ruler'], hendrik if hendrik_survives else schoeman)
                    self.assertIs(world.ref('ig:' + AF + '.leader', north_country), schoeman)
                    self.assertIsNot(son, trn.get('ruler'))
                    self.assertIs(father['owner'], world.countries['NAL'])
                    world.effect(east, world.countries['LYD'])
                    self.assertEqual('LYD_cornelis_potgieter', world.countries['LYD']['ruler']['template'])
        for choice in ('a', 'b'):
            self.assertIn('sb_found_lydenburg_republic', str(option('sb_boer_republics.131', choice)))

    def test_birthdays_and_personal_bonus(self):
        trait = fields(definitions('common/character_traits/sb_character_traits.txt')['sb_youth'])
        self.assertEqual({'character_popularity_add': '-25', 'character_prominence_add': '-25'},
                         fields(trait['character_modifier']))
        self.assertEqual(('personality', '0', '0', 'no'), (trait['type'], trait['weight'], trait['value'],
                                                          fields(trait['possible'])['always']))
        self.assertTrue(trait['texture'].endswith('/inexperienced.dds"'))
        self.assertTrue((GAME / trait['texture'].strip('"')).is_file())
        vanilla = (GAME / 'common/character_traits/personality_traits.txt').read_text(encoding='utf-8-sig')
        native = {name: fields(fields(statements(object_block_from_source(vanilla, name)))['character_modifier'])
                  for name in ('trait_child', 'brave', 'reckless')}
        self.assertEqual(native['trait_child'], fields(trait['character_modifier']))
        self.assertEqual(10, sum(int(item['character_popularity_add']) for item in native.values()))
        self.assertEqual('15', fields(definitions('common/static_modifiers/sb_modifiers.txt')[MANDATE])[
            'character_popularity_add'])
        delay = 18 * 365 + (date(1854, 9, 17) - date(1854, 1, 1)).days
        for order in ('birthday only', 'appointment first', 'both on birthday', 'birthday first'):
            with self.subTest(order=order):
                world = LeadershipRuntime()
                self.new_son(world)
                self.assertEqual([(BIRTHDAY, SON, delay)], world.events)
                world = deepcopy(world)
                son = world.people[SON]
                son['age'] = 34
                world.deliver(BIRTHDAY)  # September 16.
                self.assertIn('sb_youth', son['traits'])
                if order in ('birthday only', 'birthday first'):
                    son['age'] = 35
                    world.deliver(BIRTHDAY)
                    self.assertNotIn('sb_youth', son['traits'])
                    self.assertEqual([], world.rewards)
                    self.assertIsNone(world.ref('ig:' + LO + '.leader', world.countries['TRN']))
                    if order == 'birthday only':
                        self.assertEqual(1, world.youth_removals)
                        continue
                world.depart('ordinary')
                world.adopt()
                if order == 'both on birthday':
                    son['age'] = 35
                world.deliver(APPOINT)
                self.assertNotIn('sb_youth', son['traits'])
                son['age'] = 35
                world.deliver(BIRTHDAY)
                world.deliver(APPOINT)
                self.assertEqual([(SON, 48)], world.rewards)
                self.assertEqual(1, world.youth_removals)
                self.assertEqual(48, son['modifiers'][MANDATE])
                self.assertIs(son, world.ref('ig:' + LO + '.leader', world.countries['TRN']))
                self.assertEqual({MANDATE}, set(son['modifiers']))
                world.advance_months(son, 47)
                self.assertEqual(1, son['modifiers'][MANDATE])
                world.advance_months(son, 1)
                world.deliver(APPOINT)
                self.assertEqual([(SON, 48)], world.rewards)
                self.assertEqual({}, son['modifiers'])
                self.assertNotIn('sb_youth', son['traits'])
                self.assertIs(son, son['interest_group']['leader'])

    def test_milestone_orders_hosts_and_held_notices(self):
        for route in ('ordinary', 'punitive'):
            for first in ('migration', 'constitution'):
                for host in ('TRN', 'ORA', 'ZPB'):
                    with self.subTest(route=route, first=first, host=host):
                        world = LeadershipRuntime(('ORA', 'TRN', 'ZPB') if route == 'ordinary' else ('ORA', 'TRN'))
                        world.host = host  # ZPB survives in the ordinary case and is lost in the punitive case.
                        self.new_son(world)
                        world.person('NAL', FATHER)
                        if first == 'constitution':
                            world.adopt()
                        world.depart(route)
                        self.assertIs(world.people[FATHER], world.ref('ig:' + LO + '.leader', world.countries['TRN']))
                        households_wait = route == 'ordinary' and host in ('TRN', 'ORA')
                        before = sum(world.totals('NAL'))
                        self.assertEqual(0 if households_wait else 9500, before)
                        if first == 'migration':
                            world.adopt()
                        world = deepcopy(world)
                        notices = [event for event in world.events if event[0] != BIRTHDAY]
                        expected = [(RETURN, 'TRN', 1)]
                        if host == 'ORA':
                            expected.append(('sb_natal_crisis.116' if route == 'ordinary' else 'sb_klip_river_county.082', host, 1))
                        if first == 'migration':
                            expected.append((APPOINT, 'TRN', 3))
                        self.assertCountEqual(expected, notices)
                        if first == 'migration':
                            world.deliver(APPOINT)  # Acknowledge a held father's notice after the son's appointment.
                        world.deliver(RETURN)
                        world.deliver(RETURN)
                        if route == 'ordinary' and host == 'ORA':
                            world.deliver('sb_natal_crisis.116')
                        world.depart(route)
                        world.adopt()
                        self.assertEqual(9500, sum(world.totals('NAL')))
                        self.assertEqual(9500 if route == 'punitive' else 0, sum(world.totals('ZUL')))
                        self.assertEqual([(SON, 48)], world.rewards)
                        self.assertIs(world.people[SON], world.ref('ig:' + LO + '.leader', world.countries['TRN']))
                        self.assertEqual(len(notices) + 1, len(world.events))

    def test_organic_success_absent_father_and_frontier_choice(self):
        for has_father in (True, False):
            world = LeadershipRuntime()
            son = self.new_son(world)
            son['interest_group']['leader'] = son
            world.person('ORA', 'ORA_marthinus_wessel_pretorius')  # Separate campaign character.
            if has_father:
                world.person('NAL', FATHER)
            world.adopt('b')
            world.depart('ordinary')
            self.assertIs(son, son['interest_group']['leader'])
            self.assertEqual([], world.rewards)
            self.assertIn('sb_youth', son['traits'])
            world.adopt()
            world.deliver(APPOINT)
            self.assertEqual([(SON, 48)], world.rewards)
        world = LeadershipRuntime()
        self.new_son(world)
        world.adopt()
        world.depart('punitive')
        world.deliver(RETURN)
        self.assertEqual([(SON, 48)], world.rewards)

    def test_free_state_character_cannot_receive_the_western_appointment(self):
        world = LeadershipRuntime()
        other = world.person('TRN', 'ORA_marthinus_wessel_pretorius')
        world.adopt()
        world.depart('ordinary')
        self.assertEqual(set(), other['traits'])
        self.assertNotIn(RETURN, world.deliveries)
        self.assertNotIn(APPOINT, world.deliveries)
        self.assertNotIn(BIRTHDAY, world.deliveries)
        self.assertEqual([], world.rewards)

    def test_punitive_last_state_late_west_and_staying(self):
        world = LeadershipRuntime(('ORA',))
        father = world.person('NAL', FATHER)
        world.call('sb_shelter_punitive_andries', 'NAL')
        self.assertIs(father['owner'], world.countries['CAP'])
        world.call('sb_klip_river_clear_punitive_runtime', 'GBR')
        self.assertIs(father['owner'], world.countries['NAL'])
        self.assertNotIn('sb_klip_boers_departed', world.global_vars)
        world.call('sb_klip_river_finalize_secession_white_peace', 'NAL')
        self.assertNotIn('sb_klip_boers_departed', world.global_vars)
        world.call('sb_shelter_punitive_andries', 'NAL')
        world.countries['NAL']['alive'] = False
        world.host = 'ZPB'
        world.depart('punitive')
        self.assertEqual((0, 9500, 0, 0), world.totals('ZUL'))
        self.assertEqual((0, 0, 0, 0), world.totals('NAL'))
        self.new_son(world, 'ORA')
        world.countries['TRN']['alive'] = True
        world.effect(founder_offices(TREK, 'sb_spawn_transvaal_republic_v2'), world.countries['TRN'])
        self.assertIs(father['owner'], world.countries['TRN'])
        world.adopt()
        world.deliver(APPOINT)
        self.assertEqual([(SON, 48)], world.rewards)

    def test_lost_ordinary_host_releases_households_only_once(self):
        housekeeping = EFFECTS['sb_klip_river_county_monthly_housekeeping']
        recovery = [node for node in housekeeping if 'sb_klip_household_notice_host' in str(node)]
        self.assertEqual(1, len(recovery))
        for host, survivor in (('ORA', 'TRN'), ('TRN', 'ORA')):
            world = LeadershipRuntime()
            world.host = host
            self.new_son(world)
            world.person('NAL', FATHER)
            world.depart('ordinary')
            natal = world.countries['NAL']
            world.effect(recovery, natal)
            self.assertEqual(0, sum(world.totals('NAL')))
            world.countries[host]['alive'] = False
            world.effect(recovery, natal)
            world.effect(recovery, natal)
            self.assertEqual(9500, world.arrivals['NAL', survivor, 'cu:boer'])
            self.assertEqual(500, natal['states'][0]['pops'][0]['total_size'])

    def test_old_pending_receipts_and_candidate_lost_while_held(self):
        for old_receipt in ('sb_natal_crisis.116', 'sb_natal_crisis.117', 'sb_klip_river_county.082'):
            world = LeadershipRuntime()
            self.new_son(world)
            world.person('ORA', FATHER)
            trn = world.countries['TRN']
            if old_receipt.endswith('116'):
                trn['modifiers'] = {'sb_trek_centralizing_republic': 1}
            else:
                marker = 'sb_lydenburg_spawn_var' if old_receipt.endswith('117') else 'sb_lydenburg_spawned_var'
                trn['vars'][marker] = 1
            host = world.countries['ORA'] if old_receipt.endswith('116') else trn
            world.deliveries[old_receipt] = (host, {})
            world = deepcopy(world)
            world.deliver(old_receipt)
            if old_receipt.endswith('116'):  # Oranje keeps its own notice and TRN receives its return.
                world.deliver(RETURN)
            else:
                self.assertNotIn(RETURN, world.deliveries)
            world.deliver(old_receipt)
            self.assertEqual([(SON, 48)], world.rewards)
            self.assertEqual(0 if old_receipt.endswith('082') else 9500, sum(world.totals('NAL')))
            self.assertNotIn(APPOINT, world.deliveries)

        # An old punitive distribution on ZUL proves migration preceded today's constitutional vote.
        world = LeadershipRuntime()
        self.new_son(world)
        world.person('ORA', FATHER)
        world.countries['ZUL']['vars']['sb_klip_river_boer_population_moved_var'] = 1
        world.countries['NAL']['alive'] = False
        world.adopt()
        self.assertIn((APPOINT, 'TRN', 3), world.events)
        self.assertIs(world.people[FATHER], world.ref('ig:' + LO + '.leader', world.countries['TRN']))

        # A dead or emigrated son cannot be appointed by a held notice; the wagons still arrive.
        for unavailable in ('dead', 'abroad'):
            world = LeadershipRuntime()
            son = self.new_son(world)
            world.person('NAL', FATHER)
            world.adopt()
            world.depart('ordinary')
            if unavailable == 'dead':
                son['alive'] = False
            else:
                world.effect([('transfer_character', '=', 'c:ORA')], son)
            world.deliver(RETURN)
            self.assertEqual([], world.rewards)
            self.assertEqual(9500, sum(world.totals('NAL')))
            self.assertIs(world.people[FATHER], world.ref('ig:' + LO + '.leader', world.countries['TRN']))
