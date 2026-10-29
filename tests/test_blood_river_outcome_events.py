"""Execute terminal receipts and outcome events; native popup delivery remains DP's check."""
import re
import unittest

from tests.test_zulu_court_event_package import EventRuntime, fields
from tests.test_zulu_court_politics import character, definitions
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import extract_top_level_blocks, find_object
from tools.validate import ROOT


# Container tags are search metadata, not executable clauses; this interpreter
# parses keyed script statements and deliberately omits those bare-value lists.
STORY = {key: statements(re.sub(r'\btags\s*=\s*\{[^}]*\}', '', body))
         for key, body in extract_top_level_blocks(
             (ROOT/'common/scripted_effects/sb_story_war_effects.txt').read_text(encoding='utf-8-sig')).items()}
DYNASTY = definitions('common/scripted_effects/sb_zulu_dynasty_effects.txt')
FIREARMS = definitions('common/scripted_effects/sb_firearms_effects.txt')
LAAGER = statements(find_object((ROOT/'common/scripted_effects/sb_natalia_effects.txt').read_text(encoding='utf-8-sig'), 'sb_clear_ora_blood_river_laager'))
TRIGGERS = definitions('common/scripted_triggers/sb_natal_interwar_triggers.txt')
TRIGGERS.update(definitions('common/scripted_triggers/sb_swazi_triggers.txt'))
EVENT_TEXT = (ROOT/'events/sb_natal_crisis_events.txt').read_text(encoding='utf-8-sig')
EVENTS = {f'sb_natal_crisis.{number}': statements(find_object(EVENT_TEXT, f'sb_natal_crisis.{number}'))
          for number in ('070', '080', '081', '082')}


class OutcomeRuntime(EventRuntime):
    def __init__(self):
        king = character('Dingane', 1, 50, 1, 1)
        king['template'] = 'ZUL_dingane'
        prince = character('Mpande', 0, 50, -1, 1)
        prince['template'] = 'ZUL_mpande_zulu'
        prince['vars']['sb_court_claimant_scope'] = prince
        super().__init__([king, prince] + [character(f'chief{i}', i+10, 30) for i in range(4)])
        self.country.update(alive=True)
        self.country['vars']['sb_prerogative_var'] = 15
        self.ora = {'id': 'ORA', 'alive': True, 'vars': {}, 'ruler': character('Boer ruler', 0, 50)}
        self.play = {'id': 'play', 'vars': {}, 'type': 'dp_sb_natal_crisis',
                     'initiator': self.country, 'target': self.ora}
        self.countries = {'c:ORA': self.ora, 'c:ZUL': self.country}
        self.containers = {}
        self.globals = {'sb_natal_story_war_active_global_var'}
        self.contexts = {}
        for actor in (self.country, self.ora):
            actor['vars']['sb_natal_story_play_scope'] = self.play
        self.scopes['root'] = self.play
        self.backing()

    def ref(self, key, scope, prev=None):
        if key.lower() == 'root': return self.scopes['root']
        if key == 'PREV': return prev
        if key.startswith(('container:', 'c:')):
            name, _, tail = key.partition('.')
            target = self.containers.get(name[10:]) if name.startswith('container:') else self.countries.get(name)
            return self.ref(tail, target, scope) if tail and target is not None else target
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        branch = None
        for node in nodes:
            key, _, value = node
            if key == 'trigger_if':
                branch = self.condition(fields(value)['limit'], scope, prev)
                if branch and not self.condition([n for n in value if n[0] != 'limit'], scope, prev): return False
                continue
            if key == 'trigger_else':
                if branch is False and not self.condition(value, scope, prev): return False
                continue
            if key in TRIGGERS: result = self.condition(TRIGGERS[key], scope, prev) == (value == 'yes')
            elif key == 'container_exists': result = value in self.containers
            elif key == 'has_global_variable': result = value in self.globals
            elif key == 'is_country_alive': result = scope.get('alive', False) == (value == 'yes')
            elif key == 'country_definition': result = scope['id'] == value.removeprefix('cd:')
            elif key == 'is_diplomatic_play_type': result = scope.get('type') == value
            else: result = super().condition([node], scope, prev)
            if not result: return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, _, value = node
            if key == 'sb_clear_ora_blood_river_laager':
                self.effect(LAAGER, scope, prev)
            elif key.startswith('sb_found_natalia_after_'):
                scope.setdefault('settlements', []).append(key)
                scope['vars']['sb_natal_path_resolved_var'] = 1
            elif key == 'sb_zulu_maybe_open_swazi_question':
                scope.setdefault('swazi_checks', []).append(self.condition(TRIGGERS['sb_zulu_swazi_question_is_due'], scope))
            elif key in ('sb_sync_firearms_progress_bar', 'sb_sync_iron_age_weapons_penalty'):
                pass  # Native modifier/bar rendering is not simulated.
            elif key in STORY or key in DYNASTY or key in FIREARMS:
                self.effect(STORY.get(key, DYNASTY.get(key, FIREARMS.get(key))), scope, prev)
            elif key == 'create_container':
                f = fields(value)
                target = {'id': f['name'], 'vars': {}, 'parent': self.ref(f['parent'], scope, prev)}
                self.containers[f['name']] = target
                self.effect(f['on_created'], target, scope)
            elif key == 'destroy_container': self.containers.pop(scope['id'])
            elif key in ('initiator', 'target') or key.startswith(('container:', 'c:')):
                target = self.ref(key, scope, prev)
                if target is not None: self.effect(value, target, scope)
            elif key == 'set_global_variable': self.globals.add(value)
            elif key == 'remove_global_variable': self.globals.discard(value)
            elif key == 'clamp_variable':
                f = fields(value)
                scope['vars'][f['name']] = max(float(f['min']), min(float(f['max']), scope['vars'][f['name']]))
            else: super().effect([node], scope, prev)

    def resolve(self, accepted=(), backdown=None):
        self.scopes['root'] = self.play
        if backdown:
            self.scopes['actor'] = backdown
            self.effect(STORY['sb_story_humiliation_record_back_down'], self.play)
        else:
            for side in accepted: self.globals.add(f'sb_natal_story_{side}_demand_accepted_global_var')
        self.effect(STORY['sb_story_humiliation_resolve'], self.play)

    def open(self, number, actor):
        event = fields(EVENTS[f'sb_natal_crisis.{number}'])
        self.scopes['root'] = actor
        if not self.condition(event['trigger'], actor): return False
        self.effect(event['immediate'], actor)
        self.contexts[number] = dict(self.scopes)
        return True

    def answer(self, number, actor):
        self.scopes = dict(self.contexts[number])
        option = next(v for k, _, v in EVENTS[f'sb_natal_crisis.{number}']
                      if k == 'option' and fields(v).get('default_option') == 'yes')
        if not self.condition(fields(option)['trigger'], actor): return False
        self.effect([n for n in option if n[0] not in ('name', 'default_option', 'trigger', 'ai_chance')], actor)
        return True


class BloodRiverOutcomeEvents(unittest.TestCase):
    def stranded_play(self, route='guns', accepted=('initiator',)):
        rt = OutcomeRuntime(); z = rt.country; ora = rt.ora
        prefix = 'sb_natal_guns_bargain' if route == 'guns' else 'sb_natal_refusal'
        actor,counterparty = (z,ora) if route == 'guns' else (ora,z)
        receipt = {'id': prefix+'_generation_state', 'vars': {
            prefix+'_generation_actor_scope': actor,
            prefix+'_generation_counterparty_scope': counterparty}}
        rt.containers[receipt['id']] = receipt
        for country in (z,ora):
            # A dead handle retains the variable in the save, but has no object.
            country['vars'].update(sb_natal_story_play_scope=None,sb_natal_war_active_var=1)
            country['vars'][prefix+'_generation_scope'] = receipt
        for side in accepted:rt.globals.add(f'sb_natal_story_{side}_demand_accepted_global_var')
        rt.scopes['root'] = {'id':'unrelated-monthly-country','vars':{}}
        return rt

    def test_deleted_play_recovers_recorded_outcomes_once_from_either_route(self):
        for route in ('guns','refusal'):
            for accepted,event in ((('initiator',),'080'),(('target',),'070'),(('initiator','target'),'081')):
                with self.subTest(route=route,accepted=accepted):
                    rt=self.stranded_play(route,accepted)
                    recipient=rt.ora if event=='070' else rt.country
                    rt.effect(STORY['sb_natal_story_recover_generation'],rt.scopes['root'])
                    self.assertEqual(1,recipient.get('events',[]).count('sb_natal_crisis.'+event))
                    self.assertIs(recipient,rt.containers['sb_natal_terminal_outcome_state']['parent'])
                    self.assertNotIn('sb_court_blood_river_result_var',rt.country['vars'])
                    self.assertNotIn('sb_firearms_supply_weeks_var',rt.country['vars'])
                    for actor in (rt.country,rt.ora):
                        self.assertNotIn('sb_natal_story_play_scope',actor['vars'])
                        self.assertNotIn('sb_natal_war_active_var',actor['vars'])
                    self.assertNotIn('sb_natal_story_war_active_global_var',rt.globals)
                    self.assertEqual({'sb_natal_terminal_outcome_state'},set(rt.containers))
                    rt.effect(STORY['sb_natal_story_recover_generation'],rt.scopes['root'])
                    self.assertEqual(1,recipient['events'].count('sb_natal_crisis.'+event))
                    self.assertEqual({},rt.scopes['root']['vars'])

    def test_recovery_requires_an_ended_play_and_accepted_demands(self):
        for invalid in ('live-zulu','live-boer','missing-play-variable','no-accepted-demand','no-generation','finished'):
            with self.subTest(invalid=invalid):
                rt=self.stranded_play()
                if invalid=='live-zulu':rt.country['vars']['sb_natal_story_play_scope']=rt.play
                if invalid=='live-boer':rt.ora['vars']['sb_natal_story_play_scope']=rt.play
                if invalid=='missing-play-variable':rt.country['vars'].pop('sb_natal_story_play_scope')
                if invalid=='no-accepted-demand':rt.globals.discard('sb_natal_story_initiator_demand_accepted_global_var')
                if invalid=='no-generation':rt.containers.clear()
                if invalid=='finished':rt.globals.add('sb_natal_story_war_resolved_global_var')
                rt.effect(STORY['sb_natal_story_recover_generation'],rt.scopes['root'])
                self.assertNotIn('sb_natal_terminal_outcome_state',rt.containers)
                self.assertNotIn('sb_court_blood_river_result_var',rt.country['vars'])

    def test_deleted_play_recovery_uses_original_participants_after_retag_and_during_other_wars(self):
        rt=self.stranded_play();z=rt.country;ora=rt.ora
        z['id']='NGN';ora['id']='SAF'
        z['is_at_war']=True;ora['is_at_war']=True
        rt.countries={'c:ZUL':{'id':'replacement-ZUL','vars':{}},'c:ORA':{'id':'replacement-ORA','vars':{}}}
        rt.effect(STORY['sb_natal_story_recover_generation'],rt.scopes['root'])
        self.assertIn('sb_natal_crisis.080',z['events'])
        self.assertTrue(rt.open('080',z))
        self.assertTrue(rt.answer('080',z))
        self.assertFalse(rt.answer('080',z))
        self.assertIn('sb_court_blood_river_victory',z['ruler']['modifiers'])
        self.assertAlmostEqual(10.4,z['vars']['sb_firearms_supply_weeks_var'])
        for replacement in rt.countries.values():self.assertEqual({},replacement['vars'])

    def test_accepted_demand_preserves_the_sovereign_before_delayed_recovery(self):
        rt=self.stranded_play();z=rt.country;king,prince=z['members'][:2]
        # Record the actual enforcement while its play still exists.
        rt.globals.discard('sb_natal_story_initiator_demand_accepted_global_var')
        for actor in (z,rt.ora):actor['vars']['sb_natal_story_play_scope']=rt.play
        rt.scopes.update(root=z,diplomatic_play=rt.play,target_country=rt.ora)
        rt.effect(STORY['sb_story_humiliation_record_enforcement'],z)
        self.assertIs(king,z['vars']['sb_court_blood_river_ruler_scope'])
        z['ruler']=prince
        for actor in (z,rt.ora):actor['vars']['sb_natal_story_play_scope']=None
        rt.scopes['root']={'id':'foreign-watchdog','vars':{}}
        rt.effect(STORY['sb_natal_story_recover_generation'],rt.scopes['root'])
        self.assertTrue(rt.open('080',z))
        self.assertNotIn('sb_court_blood_river_victory',king.get('modifiers',{}))
        self.assertTrue(rt.answer('080',z))
        self.assertIn('sb_court_blood_river_victory',king['modifiers'])
        self.assertNotIn('sb_court_blood_river_victory',prince.get('modifiers',{}))

    def test_timer_alone_cannot_supply_a_recovery_victory(self):
        rt=self.stranded_play(accepted=());z=rt.country
        for actor in (z,rt.ora):actor['vars']['sb_natal_story_play_scope']=rt.play
        rt.scopes.update(root=z,diplomatic_play=rt.play,target_country=rt.ora,enforced_by_timer=True)
        rt.effect(STORY['sb_story_humiliation_record_enforcement'],z)
        self.assertNotIn('sb_natal_story_initiator_demand_accepted_global_var',rt.globals)
        for actor in (z,rt.ora):actor['vars']['sb_natal_story_play_scope']=None
        rt.effect(STORY['sb_natal_story_recover_generation'],z)
        self.assertNotIn('sb_natal_terminal_outcome_state',rt.containers)

    def test_monthly_hook_recovers_the_stranded_play_without_a_second_queue(self):
        rt=self.stranded_play();z=rt.country
        handler=fields(statements(find_object(
            (ROOT/'common/on_actions/sb_regional_on_action_handlers.txt').read_text(encoding='utf-8-sig'),
            'sb_on_natal_story_orphan_monthly')))
        self.assertTrue(rt.condition(handler['trigger'],z))
        rt.effect(handler['effect'],z)
        self.assertEqual(1,z['events'].count('sb_natal_crisis.080'))
        for actor in (z,rt.ora):self.assertFalse(rt.condition(handler['trigger'],actor))

    def test_backdown_and_enforced_defeat_wait_for_the_zulu_event(self):
        for backdown in (True, False):
            with self.subTest(backdown=backdown):
                rt = OutcomeRuntime(); z = rt.country; king = z['ruler']
                rt.resolve(backdown=z if backdown else None, accepted=('target',))
                self.assertNotIn('sb_court_blood_river_result_var', z['vars'])
                self.assertNotIn('sb_firearms_supply_weeks_var', z['vars'])
                self.assertEqual(15, z['vars']['sb_prerogative_var'])
                self.assertTrue(rt.open('070', rt.ora))
                self.assertTrue(rt.answer('070', rt.ora))
                self.assertFalse(rt.answer('070', rt.ora))
                self.assertEqual(['sb_found_natalia_after_blood_river'], rt.ora['settlements'])
                self.assertNotIn('sb_court_blood_river_result_var', z['vars'])
                self.assertFalse(rt.condition(TRIGGERS['sb_zulu_swazi_question_is_due'], z))
                self.assertTrue(rt.open('082', z))
                self.assertNotIn('sb_firearms_supply_weeks_var', z['vars'])
                self.assertNotIn('sb_court_blood_river_defeat', king.get('modifiers', {}))
                self.assertNotIn('sb_zulu_blood_river_defeat_var', z['vars'])
                self.assertEqual(15, z['vars']['sb_prerogative_var'])
                self.assertEqual(1, len(z['sb_court_blood_river_changes']))
                self.assertFalse(rt.open('082', z))
                self.assertTrue(rt.answer('082', z))
                self.assertIn('sb_court_blood_river_defeat', king['modifiers'])
                self.assertIn('sb_zulu_blood_river_defeat_var', z['vars'])
                self.assertEqual(-10, z['vars']['sb_prerogative_var'])
                self.assertAlmostEqual(10.4, z['vars']['sb_firearms_supply_weeks_var'])
                self.assertEqual(6, z['vars']['sb_firearms_progress_months_var'])
                self.assertEqual([True], z['swazi_checks'])
                self.assertFalse(rt.answer('082', z))
                self.assertEqual({}, rt.containers)
                for actor in (z, rt.ora): self.assertNotIn('sb_natal_terminal_outcome_scope', actor['vars'])
                self.assertEqual({}, rt.play['vars'])
                self.assertNotIn('sb_firearms_supply_weeks_var', rt.ora['vars'])

    def test_victory_waits_for_event_and_preserves_the_result_sovereign(self):
        for backdown in (True, False):
            rt = OutcomeRuntime(); z = rt.country; king, prince = z['members'][:2]
            rt.resolve(backdown=rt.ora if backdown else None, accepted=('initiator',))
            self.assertNotIn('sb_court_blood_river_result_var', z['vars'])
            self.assertIs(king, z['vars']['sb_court_blood_river_ruler_scope'])
            z['ruler'] = prince
            self.assertTrue(rt.open('080', z))
            self.assertNotIn('sb_court_blood_river_victory', king.get('modifiers', {}))
            self.assertNotIn('sb_court_blood_river_victory', prince.get('modifiers', {}))
            self.assertNotIn('sb_firearms_supply_weeks_var', z['vars'])
            self.assertTrue(rt.answer('080', z))
            self.assertIn('sb_court_blood_river_victory', king['modifiers'])
            self.assertNotIn('sb_court_blood_river_victory', prince.get('modifiers', {}))
            self.assertFalse(rt.answer('080', z))
            self.assertAlmostEqual(10.4, z['vars']['sb_firearms_supply_weeks_var'])

    def test_white_peace_and_mutual_settlement_learn_firearms_without_political_rewards(self):
        for accepted in ((), ('initiator', 'target')):
            rt = OutcomeRuntime(); z = rt.country
            rt.resolve(accepted)
            self.assertNotIn('sb_firearms_supply_weeks_var', z['vars'])
            self.assertTrue(rt.open('081', z))
            self.assertNotIn('sb_firearms_supply_weeks_var', z['vars'])
            self.assertFalse(rt.open('081', z))
            self.assertTrue(rt.answer('081', z))
            self.assertFalse(rt.answer('081', z))
            rt.effect(DYNASTY['sb_zulu_apply_blood_river_neutral'], z)
            self.assertAlmostEqual(10.4, z['vars']['sb_firearms_supply_weeks_var'])
            self.assertIn('sb_court_blood_river_result_var', z['vars'])
            self.assertNotIn('sb_zulu_blood_river_victory_var', z['vars'])
            self.assertNotIn('sb_court_blood_river_changes', z)
            self.assertNotIn('sb_court_blood_river_victory', z['ruler'].get('modifiers', {}))
            self.assertNotIn('sb_court_blood_river_defeat', z['ruler'].get('modifiers', {}))
            self.assertEqual(15, z['vars']['sb_prerogative_var'])
            self.assertNotIn('sb_firearms_supply_weeks_var', rt.ora['vars'])

    def test_neutral_firearms_progress_caps_and_requires_an_active_programme(self):
        for active, modernized in ((True, False), (False, False), (True, True)):
            with self.subTest(active=active, modernized=modernized):
                rt = OutcomeRuntime(); z = rt.country
                z['vars']['sb_firearms_supply_weeks_var'] = 103
                rt.resolve()
                self.assertTrue(rt.open('081', z))
                self.assertEqual(103, z['vars']['sb_firearms_supply_weeks_var'])
                # Eligibility is evaluated when the option executes, not frozen on opening.
                if not active: z['journals'].clear()
                if modernized: z['vars']['sb_firearms_modernized_var'] = 1
                self.assertTrue(rt.answer('081', z))
                self.assertEqual(104 if active and not modernized else 103,
                                 z['vars']['sb_firearms_supply_weeks_var'])

    def test_swazi_defeat_applies_thirty_once(self):
        rt = OutcomeRuntime(); z = rt.country
        succession = definitions('common/scripted_effects/sb_zulu_dynasty_succession_effects.txt')
        rt.effect(succession['sb_zulu_apply_swazi_campaign_defeat'], z)
        self.assertEqual(-15, z['vars']['sb_prerogative_var'])
        rt.effect(succession['sb_zulu_apply_swazi_campaign_defeat'], z)
        self.assertEqual(-15, z['vars']['sb_prerogative_var'])

    def test_retry_and_duplicate_callbacks_do_not_grant_or_repeat_a_settlement(self):
        rt = OutcomeRuntime(); z = rt.country
        z['vars']['sb_natal_guns_bargain_war_var'] = 1
        rt.resolve(('target',)); rt.resolve(('target',))
        self.assertEqual(1, rt.ora['events'].count('sb_natal_crisis.070'))
        rt.open('070', rt.ora); rt.answer('070', rt.ora)
        self.assertEqual(['sb_found_natalia_after_guns_bargain_rejection'], rt.ora['settlements'])
        # An undelivered popup can be retried by the other country's watchdog.
        z['vars'].pop('sb_natal_terminal_outcome_delivery_queued_var')
        rt.scopes['root'] = rt.ora
        rt.effect(STORY['sb_natal_story_recover_terminal_outcome'], rt.ora)
        self.assertEqual(2, z['events'].count('sb_natal_crisis.082'))
        self.assertNotIn('sb_firearms_supply_weeks_var', z['vars'])
        rt.open('082', z)
        self.assertEqual(15, z['vars']['sb_prerogative_var'])
        self.assertNotIn('sb_firearms_supply_weeks_var', z['vars'])
        self.assertTrue(rt.answer('082', z))
        self.assertFalse(rt.answer('082', z))
        self.assertAlmostEqual(10.4, z['vars']['sb_firearms_supply_weeks_var'])
        self.assertEqual(-10, z['vars']['sb_prerogative_var'])

    def test_dead_recipient_is_cleared_without_defeat_rewards(self):
        rt = OutcomeRuntime(); z = rt.country
        rt.resolve(('target',)); z['alive'] = False
        rt.open('070', rt.ora); rt.answer('070', rt.ora)
        self.assertEqual({}, rt.containers)
        self.assertNotIn('sb_court_blood_river_result_var', z['vars'])
        self.assertNotIn('sb_firearms_supply_weeks_var', z['vars'])

    def test_dead_sovereign_and_completed_firearms_do_not_reward_replacements(self):
        rt = OutcomeRuntime(); z = rt.country; king, prince = z['members'][:2]
        rt.resolve(('initiator',))
        king['alive'] = False
        z['ruler'] = prince
        z['journals'].clear()
        z['vars']['sb_firearms_modernized_var'] = 1
        rt.open('080', z)
        self.assertNotIn('sb_court_blood_river_victory', prince.get('modifiers', {}))
        self.assertNotIn('sb_firearms_supply_weeks_var', z['vars'])
        self.assertEqual([], z['sb_court_blood_river_changes'])
        self.assertTrue(rt.answer('080', z))
        self.assertNotIn('sb_firearms_supply_weeks_var', z['vars'])

    def test_expired_outcome_options_cannot_grant_firearms(self):
        for number, accepted in (('080', ('initiator',)), ('081', ()), ('082', ('target',))):
            with self.subTest(event=number):
                rt = OutcomeRuntime(); z = rt.country
                rt.resolve(accepted)
                if number == '082':
                    rt.open('070', rt.ora); rt.answer('070', rt.ora)
                self.assertTrue(rt.open(number, z))
                z['vars'].pop('sb_natal_terminal_outcome_popup_receipt_var')
                self.assertFalse(rt.answer(number, z))
                self.assertNotIn('sb_firearms_supply_weeks_var', z['vars'])
                self.assertNotIn('sb_court_blood_river_result_var', z['vars'])
                self.assertEqual(15, z['vars']['sb_prerogative_var'])
                self.assertNotIn('sb_court_blood_river_defeat', z['ruler'].get('modifiers', {}))
                self.assertNotIn('sb_court_blood_river_victory', z['ruler'].get('modifiers', {}))

    def test_firearms_tooltip_preview_without_an_initial_counter(self):
        rt = OutcomeRuntime(); z = rt.country
        rt.preview = True
        rt.effect(DYNASTY['sb_boost_firearms_progress_minor'], z)
        self.assertNotIn('sb_firearms_supply_weeks_var', z['vars'])
        self.assertNotIn('sb_firearms_progress_months_var', z['vars'])

    def test_open_popup_reserves_houses_but_only_click_changes_them(self):
        for number, accepted, count in (('080', ('initiator',), 2), ('082', ('target',), 1)):
            with self.subTest(event=number):
                rt = OutcomeRuntime(); z = rt.country
                rt.resolve(accepted)
                if number == '082': rt.open('070', rt.ora); rt.answer('070', rt.ora)
                self.assertTrue(rt.open(number, z))
                planned = list(z['sb_court_blood_river_changes'])
                self.assertEqual(count, len(planned))
                self.assertEqual(count, len({c['id'] for c in planned}))
                self.assertTrue(all(c['vars']['sb_court_endorsement_var'] == 0 for c in planned))
                # A stale house is skipped, without substituting a different unpreviewed house.
                planned[0]['alive'] = False
                self.assertTrue(rt.answer(number, z))
                self.assertEqual(0, planned[0]['vars']['sb_court_endorsement_var'])
                for actor in z['members'][2:]:
                    if not any(actor is target for target in planned):
                        self.assertEqual(0, actor['vars']['sb_court_endorsement_var'])

    def test_patron_death_during_popup_does_not_redirect_the_coalition(self):
        rt = OutcomeRuntime(); z = rt.country
        rt.resolve(('target',)); rt.open('070', rt.ora); rt.answer('070', rt.ora)
        rt.open('082', z)
        z['vars']['sb_court_blood_river_patron_scope']['alive'] = False
        self.assertTrue(rt.answer('082', z))
        self.assertEqual(-10, z['vars']['sb_prerogative_var'])
        self.assertTrue(all(c['vars']['sb_court_endorsement_var'] == 0 for c in z['members'][2:]))


if __name__ == '__main__': unittest.main()
