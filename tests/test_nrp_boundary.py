"""Exercise the Vryheid decision with the player in either capital."""
import unittest
from unittest.mock import patch

from tests.test_zulu_court_politics import EFFECTS, TRIGGERS, definitions
from tests.test_zulu_frontier_followup import block, field
from tests.test_zulu_later_court import LaterCourtRuntime, PROVINCES, SETTLEMENT_EFFECTS, SETTLEMENT_TRIGGERS


class BoundaryRuntime(LaterCourtRuntime):
    def __init__(self):
        super().__init__()
        self.nrp = self.countries['c:NRP'] = {
            'id': 'NRP', 'alive': True, 'player': False, 'game_date': 18851001, 'characters': [],
            'vars': {'sb_nrp_boundary_pending_var': 1},
            'ruler': {'culture': 'cu:zulu', 'vars': {}, 'historical': False},
        }
        self.nal = self.countries['c:NAL']
        self.britain = self.countries['c:GBR']
        self.nal.update(overlord=self.britain, subject_type='subject_type_colony')
        self.country.update(overlord=self.nal, states=[{'state_region': 's:STATE_ZULULAND'}])
        for actor in (self.country, self.nal, self.britain):
            actor.update(is_at_war=True, is_active_in_diplomatic_play=True, has_war_with={'SEL', 'SIA'})
        self.britain['aggressive_diplomatic_plays_permitted'] = True
        for province in PROVINCES:
            self.provinces[province]['state']['owner'] = self.nrp
        self.global_vars.update(sb_zululand_live_zul_scope=self.country,
                                sb_nrp_chiefdoms_earned_var=1, sb_nrp_reward_consumed_var=1)

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, _, value = node
            if key == 'create_character':
                spec = {k: v for k, _, v in value}
                name = spec.get('template')
                if name:
                    template = block('common/character_templates/sb_cape_and_colonial_characters.txt', name)
                    spec.update({k: v.strip('"') for k, _, v in template if isinstance(v, str)})
                    self.used_templates.add(name)
                assert scope is self.nrp and spec['ig_leader'] == spec['ruler'] == 'yes'
                assert spec['interest_group'] == 'ig_armed_forces'
                actor = {'template': name, 'culture': spec['culture'], 'owner': scope, 'alive': True,
                         'historical': spec.get('historical') == 'yes', 'ig_leader': True, 'vars': {}}
                scope['characters'].append(actor)
                scope['ruler'] = actor
                if 'save_scope_as' in spec: self.scopes[spec['save_scope_as']] = actor
            elif key == 'set_as_interest_group_leader': scope['ig_leader'] = True
            elif key in ('sb_ensure_commandant_general_ruler_command', 'sb_nrp_seed_livestock_ranch',
                         'add_claim', 'set_state_type'):
                pass  # Native army, building, claim and incorporation bookkeeping.
            elif key == 'save_temporary_scope_as':
                self.scopes[value] = scope
            elif key == 'create_diplomatic_play':
                super().effect([node], scope, prev)
                with patch.dict(self.scopes, root=self.play, initiator=scope, target=self.play['target']):
                    self.run('sb_nrp_configure_started_boundary_play', self.play)
            elif key == 'random_scope_state':
                for state in scope['states']:
                    if self.condition(field(value, 'limit'), state, scope):
                        self.effect([n for n in value if n[0] != 'limit'], state, scope)
                        break
            else:
                super().effect([node], scope, prev)

    def ref(self, key, scope, prev=None):
        if key == 's:STATE_ZULULAND.region_state:NAL':
            return next((state for state in self.nal.get('states', [])
                         if state['state_region'] == 's:STATE_ZULULAND'), None)
        if key.startswith('cu:'):
            return key
        if key in ('yes', 'no'):
            return key == 'yes'
        if key == 'is_historical':
            return scope['historical']
        if key == 'is_interest_group_leader': return scope.get('ig_leader',False)
        return super().ref(key, scope, prev)


class NRPBoundaryTests(unittest.TestCase):
    def setUp(self):
        natal = definitions('common/scripted_triggers/sb_natal_interwar_triggers.txt')
        triggers = dict(SETTLEMENT_TRIGGERS, sb_natal_has_responsible_government=natal['sb_natal_has_responsible_government'])
        for registry, entries in ((EFFECTS, SETTLEMENT_EFFECTS), (TRIGGERS, triggers)):
            patcher = patch.dict(registry, entries)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_pending_1885_settlement_reaches_the_player_once_despite_asian_wars(self):
        for play_nrp in (False, True):
            for local_demand in (False, True):
                with self.subTest(play_nrp=play_nrp, local_demand=local_demand):
                    rt = BoundaryRuntime()
                    rt.nrp['player'], rt.sponsor['player'] = play_nrp, not play_nrp
                    if local_demand:
                        rt.nal['subject_type'] = 'subject_type_dominion'
                    recipient = rt.nrp if play_nrp else rt.sponsor
                    rt.run('sb_nrp_open_boundary_demand', rt.nrp)
                    self.assertIs(rt.sponsor, rt.nrp['overlord'])
                    founder = rt.nrp['ruler']
                    self.assertEqual(('NRP_lucas_meyer', 'cu:boer'), (founder['template'], founder['culture']))
                    self.assertIs(rt.nal if local_demand else rt.britain, rt.nrp['vars']['sb_nrp_boundary_initiator_scope'])
                    event = block('events/sb_zululand_settlement_events.txt', 'sb_zululand_settlement.210')
                    for actor in (rt.nrp, rt.sponsor, rt.nal):
                        self.assertEqual(actor is recipient, rt.condition(field(event, 'trigger'), actor))
                    self.assertFalse(rt.condition(TRIGGERS['sb_nrp_boundary_current_launch_authority'], rt.nrp))
                    rt.run('sb_nrp_open_boundary_demand', rt.nrp)
                    self.assertEqual(['sb_zululand_settlement.210'], recipient['events'])
                    self.assertIs(founder, rt.nrp['ruler'])
                    other = rt.sponsor if play_nrp else rt.nrp
                    self.assertNotIn('sb_zululand_settlement.210', other.get('events', []))

    def test_local_enemies_and_truces_delay_the_letter(self):
        for actor, relation, target in (('britain', 'has_war_with', 'NRP'), ('nal', 'has_war_with', 'TRN'),
                                        ('britain', 'is_diplomatic_play_enemy_of', 'TRN'), ('britain', 'has_truce_with', 'TRN')):
            rt = BoundaryRuntime()
            country = getattr(rt, actor)
            country[relation] = {target}
            rt.run('sb_nrp_open_boundary_demand', rt.nrp)
            self.assertNotIn('sb_nrp_boundary_event_open_var', rt.nrp['vars'])
            self.assertIn('sb_nrp_boundary_pending_var', rt.nrp['vars'])
            country[relation].clear()
            rt.run('sb_nrp_open_boundary_demand', rt.nrp)
            self.assertEqual(['sb_zululand_settlement.210'], rt.sponsor['events'])
        rt = BoundaryRuntime()
        rt.nal['overlord'] = rt.countries['c:ORA']
        rt.run('sb_nrp_open_boundary_demand', rt.nrp)
        self.assertNotIn('sb_nrp_boundary_event_open_var', rt.nrp['vars'])

    def test_acceptance_returns_three_districts_and_the_petition_reaches_pretoria(self):
        for rebellion, play_nrp in ((False, False), (True, True)):
            rt = BoundaryRuntime()
            rt.nrp['player'], rt.sponsor['player'] = play_nrp, not play_nrp
            if rebellion:
                rt.nrp['vars']['sb_nrp_direct_annexation_rebellion_var'] = 1
                del rt.global_vars['sb_zululand_live_zul_scope']
                rt.nal['states'] = [{'state_region': 's:STATE_ZULULAND', 'owner': rt.nal}]
            rt.run('sb_nrp_open_boundary_demand', rt.nrp)
            player = rt.nrp if play_nrp else rt.sponsor
            event_id = 'sb_zululand_settlement.' + ('230' if rebellion else '210')
            self.assertEqual([event_id], player['events'])
            event = block('events/sb_zululand_settlement_events.txt', event_id)
            with patch.dict(rt.scopes, root=player):
                self.assertTrue(rt.condition(field(event, 'trigger'), player))
                rt.effect(field(field(event, 'option'), 'hidden_effect'), player)
            notice = block('events/sb_zululand_settlement_events.txt', 'sb_zululand_settlement.231')
            with patch.dict(rt.scopes, root=rt.nal):
                self.assertTrue(rt.condition(field(notice, 'trigger'), rt.nal))
                rt.effect(field(notice, 'immediate'), rt.nal)
                self.assertFalse(rt.condition(field(notice, 'trigger'), rt.nal))
            self.assertEqual(3, len(rt.transfers))
            self.assertEqual({rt.nal['id'] if rebellion else rt.country['id']}, {owner for _, owner in rt.transfers})
            del rt.nrp['vars']['sb_nrp_union_wait_var']  # Two years later.
            rt.run('sb_nrp_monthly_housekeeping', rt.nrp)
            petition = block('events/sb_zululand_settlement_events.txt', 'sb_zululand_settlement.220')
            self.assertTrue(rt.condition(field(petition, 'trigger'), rt.nrp))
            answer = field(petition, 'option')
            rt.effect([n for n in answer if n[0] in ('remove_variable', 'if')], rt.nrp)
            decision = block('events/sb_zululand_settlement_events.txt', 'sb_zululand_settlement.221')
            with patch.dict(rt.scopes, root=rt.sponsor):
                self.assertTrue(rt.condition(field(decision, 'trigger'), rt.sponsor))

    def test_protected_refusal_waits_then_targets_pretoria_with_vryheid_on_its_side(self):
        rt = BoundaryRuntime()
        rt.run('sb_nrp_open_boundary_demand', rt.nrp)
        rt.run('sb_nrp_refuse_boundary_demand', rt.nrp)
        self.assertIn('sb_nrp_boundary_refused_var', rt.nrp['vars'])
        self.assertNotIn('sb_zululand_settlement.211', rt.sponsor['events'])
        rt.britain.update(is_at_war=False, is_active_in_diplomatic_play=False)
        rt.run('sb_nrp_monthly_housekeeping', rt.nrp)
        self.assertIs(rt.sponsor, rt.play['target'])
        self.assertIs(rt.play, rt.nrp['vars']['sb_nrp_boundary_play_scope'])
        self.assertIn(rt.nrp, rt.participants)
        self.assertEqual(['return_state', 'return_state'], [field(goal, 'type') for goal in rt.play['add_war_goal']])

    def test_founder_lifetime_and_player_independence(self):
        for date, historical in ((18621118, False), (18621119, True), (19020807, True), (19020808, False)):
            rt = BoundaryRuntime()
            rt.nrp['game_date'] = date
            rt.run('sb_nrp_install_founding_commandant', rt.nrp)
            self.assertEqual(historical, rt.nrp['ruler']['historical'])
            self.assertEqual('cu:boer', rt.nrp['ruler']['culture'])
        rt = BoundaryRuntime()
        rt.run('sb_nrp_reconcile_pending_foundation', rt.nrp)
        del rt.nrp['overlord'], rt.nrp['subject_type']
        rt.run('sb_nrp_reconcile_pending_foundation', rt.nrp)
        self.assertNotIn('overlord', rt.nrp)

    def test_first_government_replaces_the_placeholder_and_leaves_later_successors(self):
        rt = BoundaryRuntime()
        placeholder = {'template':'default', 'culture':'cu:boer', 'historical':False, 'vars':{}}
        rt.nrp['ruler'] = placeholder
        rt.nrp['vars'].update(sb_nrp_founding_government_set_var=1, sb_nrp_boundary_not_before_var=1)
        rt.nrp['game_date'] = 18860217
        rt.run('sb_nrp_monthly_housekeeping', rt.nrp)
        meyer = rt.nrp['ruler']
        self.assertEqual('NRP_lucas_meyer', meyer['template'])
        self.assertTrue(meyer['historical'])
        rt.nrp['ruler'] = placeholder
        rt.run('sb_nrp_confirm_founding_commandant', rt.nrp)
        self.assertIs(placeholder, rt.nrp['ruler'])
        self.assertEqual(1, len(rt.nrp['characters']))

    def test_founding_confirmation_reuses_living_meyer_after_a_government_refresh(self):
        rt = BoundaryRuntime()
        rt.nrp['vars']['sb_nrp_founding_government_set_var'] = 1
        rt.run('sb_nrp_install_founding_commandant', rt.nrp)
        meyer = rt.nrp['ruler']
        rt.scopes.clear()  # Next day / reload.
        rt.nrp['ruler'] = {'template': 'another_commandant', 'culture': 'cu:boer', 'historical': True}
        rt.run('sb_nrp_confirm_founding_commandant', rt.nrp)
        self.assertIs(meyer, rt.nrp['ruler'])
        self.assertEqual([meyer], rt.nrp['characters'])

    def test_legacy_boundary_timer_can_check_the_founder_before_the_monthly_pulse(self):
        rt = BoundaryRuntime()
        rt.nrp['vars'].update(sb_nrp_founding_government_set_var=1, sb_nrp_boundary_not_before_var=1)
        rt.nrp['ruler'] = {'template': 'default', 'culture': 'cu:boer', 'historical': False}
        timer = block('events/sb_zululand_settlement_events.txt', 'sb_zululand_settlement.209')
        rt.effect(field(timer, 'immediate'), rt.nrp)
        self.assertEqual('NRP_lucas_meyer', rt.nrp['ruler']['template'])
        self.assertEqual(1, len(rt.nrp['characters']))

    def test_only_surviving_boer_households_fill_the_concession(self):
        for already_there, donors, expected in ((0,[350,150],500),(204,[185,300],500),
                                                (88,[70,50],208),(520,[100],520)):
            with self.subTest(already_there=already_there,donors=donors):
                rt = BoundaryRuntime()
                source = rt.country['states'][0]
                source.update(owner=rt.country, pops=[{'culture':'cu:boer','total_size':n} for n in donors])
                tswana = {'culture':'cu:tswana','total_size':8873}
                source['pops'].append(tswana)
                rt.nrp_state['pops'] = [{'culture':'cu:boer','total_size':already_there}]
                move = [('sb_nrp_settle_boer_households','=',[('TARGET','=','500')])]
                for _ in range(2):
                    rt.effect(move,source)
                actual = sum(p['total_size'] for p in rt.nrp_state['pops'])
                self.assertEqual(expected,actual)
                self.assertEqual(sum(donors)+already_there,actual + sum(p['total_size'] for p in source['pops'] if p['culture']=='cu:boer'))
                self.assertEqual(8873,tswana['total_size'])

    def test_land_grant_settles_the_dispatch_once_from_the_surviving_grantor(self):
        for annexed in (False, True):
            for dispatched in (False, True):
                with self.subTest(annexed=annexed, dispatched=dispatched):
                    rt = BoundaryRuntime()
                    rt.scopes['root'] = rt.britain
                    del rt.global_vars['sb_nrp_reward_consumed_var']
                    rt.nal['vars']['sb_nrp_setup_pending_var'] = 1
                    if dispatched:
                        rt.nal['vars']['sb_nrp_volunteer_households_due_var'] = 1
                    if annexed:
                        del rt.global_vars['sb_zululand_live_zul_scope']
                        rt.nal['vars']['sb_nrp_direct_annexation_rebellion_pending_var'] = 1
                        rt.nal['states'] = [{'state_region': 's:STATE_ZULULAND'}]
                    grantor = rt.nal if annexed else rt.country
                    residual = {'culture': 'cu:boer', 'total_size': 447}
                    grantor['states'][0].update(owner=grantor, pops=[residual])
                    rt.nrp_state['pops'] = [{'culture': 'cu:boer', 'total_size': 53}]
                    with patch.dict(EFFECTS, {'sb_nrp_return_inherited_buildings_to_zul': []}):
                        for _ in range(2):
                            rt.run('sb_nrp_finalize_greater_republic', rt.nal)
                    population = sum(pop['total_size'] for pop in rt.nrp_state['pops'])
                    self.assertEqual(500 if dispatched else 53, population)
                    self.assertEqual(500, population + residual['total_size'])
                    self.assertEqual(5, len(rt.transfers))
                    self.assertNotIn('sb_nrp_volunteer_households_due_var', rt.nal['vars'])

    def test_gazetted_boundary_corrects_the_old_pair_once_and_respects_foreign_land(self):
        for rightful in (True,False):
            rt = BoundaryRuntime()
            rt.nrp['vars']['sb_nrp_boundary_cutback_accepted_var'] = 1
            recipient = rt.country if rightful else rt.britain
            for province in ('xE1E455','x904EBE','x9E9742'):
                rt.provinces[province]['state']['owner'] = recipient
            for _ in range(2): rt.run('sb_nrp_correct_legacy_boundary',rt.nrp)
            self.assertEqual(2 if rightful else 0,len(rt.transfers))
            self.assertIs(rt.nrp if rightful else recipient,rt.provinces['xE1E455']['state']['owner'])
            self.assertIs(recipient if rightful else rt.nrp,rt.provinces['xBE6FEE']['state']['owner'])
            if rightful:
                # A later transfer restores the old geometry. The treaty has already run.
                rt.provinces['xE1E455']['state']['owner'] = recipient
                rt.provinces['xBE6FEE']['state']['owner'] = rt.nrp
                rt.run('sb_nrp_correct_legacy_boundary', rt.nrp)
                self.assertEqual(2, len(rt.transfers))
                self.assertIs(recipient, rt.provinces['xE1E455']['state']['owner'])

    def test_cutback_retains_the_surviving_community_after_the_native_state_split(self):
        rt = BoundaryRuntime()
        survivors = {'culture': 'cu:boer', 'total_size': 300}
        rt.nrp_state['pops'] = [survivors]
        local = {'culture': 'cu:zulu', 'total_size': 8000}
        source = rt.country['states'][0]
        source.update(owner=rt.country, pops=[local])
        native = rt.effect

        def split(nodes, scope, prev=None):
            native(nodes, scope, prev)
            if scope is rt.region and any(key == 'set_owner_of_provinces' for key, _, _ in nodes):
                survivors['total_size'] -= 120
                source['pops'].append({'culture': 'cu:boer', 'total_size': 120})

        with patch.object(rt, 'effect', side_effect=split):
            rt.run('sb_nrp_return_boundary_districts', rt.country)
        self.assertEqual(3, len(rt.transfers))
        self.assertEqual(300, sum(pop['total_size'] for pop in rt.nrp_state['pops']))
        self.assertEqual(8000, sum(pop['total_size'] for pop in source['pops']))
        self.assertEqual(8000, local['total_size'])
