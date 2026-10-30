"""Execute Natal/Swazi eligibility, weekly market supply and on-demand heir creation.

Native shipment accounting, portrait rendering and scheduling remain DP checks.
"""
from pathlib import Path
import unittest

from tests.test_zulu_court_politics import CourtRuntime, character, definitions, EFFECTS
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import find_object

ROOT = Path(__file__).resolve().parents[1]


def block(path, key):
    return statements(find_object((ROOT/path).read_text(encoding='utf-8-sig'), key))


def field(nodes, key):
    return next(v for k, _, v in nodes if k == key)


EXTRA_TRIGGERS = definitions('common/scripted_triggers/sb_firearms_triggers.txt')
EXTRA_TRIGGERS.update(definitions('common/scripted_triggers/sb_swazi_triggers.txt'))
EXTRA_EFFECTS = definitions('common/scripted_effects/sb_zulu_dynasty_effects.txt')
EXTRA_EFFECTS.update(definitions('common/scripted_effects/sb_zulu_dynasty_succession_effects.txt'))
EXTRA_EFFECTS.update(definitions('common/scripted_effects/sb_firearms_effects.txt'))
for name in ('sb_natal_archive_zulu_firearms', 'sb_natal_restore_archived_zulu_firearms',
             'sb_british_archive_preannex_zulu_firearms', 'sb_british_clear_preannex_zulu_firearms',
             'sb_british_transfer_archived_zulu_firearms_to_natal'):
    EXTRA_EFFECTS[name] = block('common/scripted_effects/sb_natal_interwar_effects.txt', name)
EXTRA_EFFECTS['sb_swazi_apply_guns_for_land_bonus'] = block(
    'common/scripted_effects/sb_swazi_effects.txt', 'sb_swazi_apply_guns_for_land_bonus')
for name in ('sb_cleanup_swazi_defensive_muster_for_play', 'sb_swazi_end_defensive_muster'):
    EXTRA_EFFECTS[name] = block('common/scripted_effects/sb_swazi_effects.txt', name)


class FrontierRuntime(CourtRuntime):
    def __init__(self):
        king = character('Dingane', 1, 50, 1, 1)
        king['template'] = 'ZUL_dingane'
        super().__init__([king])
        self.country.update(characters=list(self.country['members']), alive=True,
                            laws={'law_type:law_monarchy', 'law_type:law_autocracy'},
                            journals={'je_sb_zulu_kingdom', 'je_sb_adopt_firearms'},
                            treaties=[], market={'mg:small_arms': {'market_goods_sell_orders': 0, 'shortage': False}})
        self.country['vars']['sb_prerogative_var'] = 0
        self.countries = {'c:ZUL': self.country,
                          'c:ORA': {'id': 'ORA', 'vars': {}},
                          'c:SWZ': {'id': 'SWZ', 'alive': True,
                                    'states': [{'state_region': 's:STATE_EAST_TRANSVAAL'}]}}
        self.created = 0

    def ref(self, key, scope, prev=None):
        if key == 'root': return self.scopes['root']
        if key.startswith('c:'):
            name, _, tail = key.partition('.')
            country = self.countries.get(name)
            return self.ref(tail, country, prev) if tail and country is not None else country
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        branch = None
        for node in nodes:
            key, _, value = node
            if key == 'save_temporary_scope_as':
                self.scopes[value] = scope
                continue
            if key == 'trigger_if':
                branch = self.condition(field(value, 'limit'), scope, prev)
                if branch and not self.condition([n for n in value if n[0] != 'limit'], scope, prev): return False
                continue
            if key == 'trigger_else':
                if branch is False and not self.condition(value, scope, prev): return False
                continue
            if key in EXTRA_TRIGGERS:
                result = self.condition(EXTRA_TRIGGERS[key], scope, prev) == (value == 'yes')
            elif key.startswith('any_scope_') and key in ('any_scope_treaty', 'any_scope_article', 'any_scope_character'):
                collection = {'any_scope_treaty': 'treaties', 'any_scope_article': 'articles', 'any_scope_character': 'characters'}[key]
                result = any(self.condition(value, target, scope) for target in scope.get(collection, []))
            elif key == 'binds': result = any(c is self.ref(value, scope, prev) for c in scope['parties'])
            elif key in ('input_goods', 'has_type', 'state_region'):
                result = scope.get(key) == value
            elif key == 'market_goods_has_goods_shortage': result = scope['shortage'] == (value == 'yes')
            elif key == 'country_definition': result = scope['id'] == value.removeprefix('cd:')
            elif key == 'is_diplomatic_play_type': result = scope.get('type') == value
            elif key in ('initiator', 'target') and isinstance(value, str):
                other = self.ref(value, scope, prev)
                if other is None: raise AssertionError('Invalid country on right side: ' + value)
                result = scope.get(key) is other
            elif key == 'has_journal_entry': result = value in scope.get('journals', set())
            elif key in ('is_country_alive', 'is_subject', 'is_at_war', 'is_active_in_diplomatic_play'):
                result = scope.get('alive' if key == 'is_country_alive' else key, False) == (value == 'yes')
            else: result = super().condition([node], scope, prev)
            if not result: return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, _, value = node
            if key in ('sb_sync_firearms_progress_bar', 'sb_sync_iron_age_weapons_penalty',
                       'sb_repair_iron_age_weapons_penalty'):
                # Native JE rendering/modifier application are outside this interpreter.
                scope.setdefault('native_syncs', []).append(key)
            elif key.startswith('c:') or key in ('initiator', 'target'):
                target = self.ref(key, scope, prev)
                if target is not None: self.effect(value, target, scope)
            elif key == 'clamp_variable':
                f = {k:v for k, _, v in value}
                scope['vars'][f['name']] = max(float(f['min']), min(float(f['max']), scope['vars'][f['name']]))
            elif key == 'add_journal_entry':
                name = field(value, 'type')
                scope['journals'].add(name)
                self.effect(field(block('common/journal_entries/1-04_sb_firearms_acquisition.txt', name), 'immediate'), scope)
            elif key in EXTRA_EFFECTS:
                self.effect(EXTRA_EFFECTS[key], scope, prev)
            elif key == 'create_character':
                creation = {k:v for k, _, v in value}
                template = creation['template']
                data = block('common/character_templates/sb_zulu_dynasty_characters.txt', template)
                age = int(field(data, 'age'))
                actor = {'id': 'Uthumbu', 'template': template, 'vars': {}, 'alive': True,
                         'age': age, 'owner': scope, 'historical': field(data, 'historical')}
                scope['characters'].append(actor)
                self.created += 1
                # Callback-local scopes are not the creation effect's exported handle.
                outer_scopes = self.scopes
                self.scopes = dict(outer_scopes, root=actor)
                try:
                    self.effect(creation.get('on_created', []), actor, scope)
                finally:
                    self.scopes = outer_scopes
                if 'save_scope_as' in creation:
                    self.scopes[creation['save_scope_as']] = actor
            elif key == 'random_scope_character':
                limit = field(value, 'limit')
                selected = next((a for a in scope['characters'] if self.condition(limit, a, scope)), None)
                if selected is not None: self.effect([n for n in value if n[0] != 'limit'], selected, scope)
            elif key == 'sb_change_prerogative':
                scope['vars']['sb_prerogative_var'] += float(field(value, 'VALUE'))
            elif key == 'set_interest_group': scope['interest_group'] = value
            elif key in ('custom_tooltip', 'show_as_tooltip'): pass  # Execution does not apply previews.
            elif key == 'add_trait' and value in ('honorable', 'innovative'): scope.setdefault('traits', set()).add(value)
            elif key == 'remove_trait': scope.setdefault('traits', set()).discard(value)
            else: super().effect([node], scope, prev)

    def due(self):
        return self.condition(EXTRA_TRIGGERS['sb_zulu_swazi_question_is_due'], self.country)



class SwaziTimingTests(unittest.TestCase):
    def test_honour_choice_records_context_without_an_aftermath_popup(self):
        rt = FrontierRuntime(); c = rt.country; ora = rt.countries['c:ORA']
        rt.scopes['boer_republic'] = ora
        ora['vars']['sb_retief_petition_var'] = 1
        c['ruler']['traits'] = {'ruthless'}
        event = block('events/sb_natal_crisis_events.txt', 'sb_natal_crisis.020')
        option = next(v for k, _, v in event if k == 'option' and field(v, 'name') == 'sb_natal_crisis.020.a')
        rt.effect([n for n in option if n[0] not in ('name', 'ai_chance')], c)
        self.assertIn('sb_zulu_swazi_ai_honour_deal_var', c['vars'])
        self.assertNotIn('sb_zulu_swazi_ai_honour_deal_var', ora['vars'])
        self.assertNotIn('sb_retief_petition_var', ora['vars'])
        self.assertEqual({'honorable'}, c['ruler']['traits'])
        self.assertEqual(['sb_natal_crisis.030'], ora['events'])
        self.assertEqual([], c.get('events', []))
        # The ordinary monthly handoff still waits for ORA's actual settlement.
        rt.effect(EXTRA_EFFECTS['sb_zulu_monthly_dynasty_housekeeping'], c)
        self.assertEqual([], c.get('events', []))
        ora['vars']['sb_natal_path_resolved_var'] = 1
        c['vars']['sb_prerogative_var'] = 10
        rt.effect(EXTRA_EFFECTS['sb_zulu_monthly_dynasty_housekeeping'], c)
        self.assertEqual([], c.get('events', []))
        c['vars']['sb_prerogative_var'] = -10
        rt.effect(EXTRA_EFFECTS['sb_zulu_monthly_dynasty_housekeeping'], c)
        rt.effect(EXTRA_EFFECTS['sb_zulu_monthly_dynasty_housekeeping'], c)
        self.assertEqual(['sb_swazi_frontier.094'], c['events'])
        self.assertEqual('GBR', rt.scopes['root']['id'])
        self.assertNotIn('sb_zulu_swazi_ai_honour_deal_var', rt.scopes['root']['vars'])

    def test_start_waits_for_natal_and_threshold_includes_minus_ten(self):
        rt = FrontierRuntime()
        for p in (-100, -10, 0):
            rt.country['vars']['sb_prerogative_var'] = p
            self.assertFalse(rt.due())
        rt.country['vars']['sb_zulu_swazi_ai_guns_south_var'] = 1
        self.assertFalse(rt.due())
        rt.countries['c:ORA']['vars']['sb_natal_path_resolved_var'] = 1
        for p,expected in ((-100,True),(-10.01,True),(-10,True),(-9.99,False),(0,False),(4.19663,False),(10,False)):
            with self.subTest(prerogative=p):
                rt.country['vars']['sb_prerogative_var'] = p
                self.assertEqual(expected,rt.due())

    def test_all_resolved_routes_and_independent_victory_white_peace(self):
        for route in ('honour_deal', 'guns_south', 'lost_blood_river', 'won_blood_river', 'white_peace'):
            with self.subTest(route=route):
                rt = FrontierRuntime()
                rt.country['vars']['sb_prerogative_var'] = -10
                rt.country['vars'][f'sb_zulu_swazi_ai_{route}_var'] = 1
                if route in ('honour_deal', 'guns_south'):
                    rt.countries['c:ORA']['vars']['sb_natal_path_resolved_var'] = 1
                self.assertTrue(rt.due())
                rt.country['vars']['sb_prerogative_var'] = 100
                self.assertEqual(route in ('won_blood_river', 'white_peace'), rt.due())
                rt.country['ruler']['template'] = 'ZUL_mpande_zulu'
                self.assertFalse(rt.due())

    def test_ora_withdrawal_is_resolved_and_missing_prerogative_is_safe(self):
        rt = FrontierRuntime()
        rt.country['vars']['sb_prerogative_var'] = -10
        rt.countries['c:ORA']['vars']['sb_natal_path_resolved_var'] = 1
        self.assertTrue(rt.due())
        del rt.country['vars']['sb_prerogative_var']
        self.assertFalse(rt.due())

    def test_pending_offer_recovers_without_reopening_an_answered_question(self):
        rt = FrontierRuntime()
        c = rt.country
        c['vars']['sb_prerogative_var'] = -10
        c['vars']['sb_zulu_swazi_ai_honour_deal_var'] = 1
        rt.countries['c:ORA']['vars']['sb_natal_path_resolved_var'] = 1
        rt.effect(EXTRA_EFFECTS['sb_zulu_maybe_open_swazi_question'], c)
        event = block('events/sb_swazi_frontier_events.txt', 'sb_swazi_frontier.094')
        self.assertTrue(rt.condition(field(event, 'trigger'), c))
        c['vars']['sb_prerogative_var'] = -9.99
        self.assertFalse(rt.condition(field(event, 'trigger'), c))
        monthly = field(block('common/on_actions/sb_boer_story_on_action_handlers.txt', 'sb_on_trek_monthly_pulse_country'), 'effect')
        rt.effect(monthly[:2], c)
        self.assertNotIn('sb_zulu_swazi_outcome_delivery_pending_var', c['vars'])
        self.assertIn('sb_zulu_swazi_ai_honour_deal_var', c['vars'])
        c['vars']['sb_prerogative_var'] = -10
        rt.effect(EXTRA_EFFECTS['sb_zulu_maybe_open_swazi_question'], c)
        self.assertEqual(2, len(c['events']))
        # The delivered popup owns the decision even if the target changes meanwhile.
        c['vars'].update(sb_zulu_swazi_outcome_popup_receipt_var=1, sb_prerogative_var=15)
        rt.effect(monthly[:2], c)
        self.assertIn('sb_zulu_swazi_outcome_delivery_pending_var', c['vars'])
        c['vars'].pop('sb_zulu_swazi_outcome_delivery_pending_var')
        c['vars']['sb_prerogative_var'] = -10
        rt.effect(EXTRA_EFFECTS['sb_zulu_maybe_open_swazi_question'], c)
        self.assertEqual(2, len(c['events']))

    def test_presenting_uthumbu_does_not_open_swazi_at_non_negative_prerogative(self):
        for start in (50,54.19663,100):
            with self.subTest(start=start):
                rt = FrontierRuntime(); c = rt.country
                c['vars'].update(sb_prerogative_var=start,sb_zulu_swazi_ai_honour_deal_var=1)
                rt.countries['c:ORA']['vars']['sb_natal_path_resolved_var'] = 1
                rt.effect(EFFECTS['sb_court_introduce_uthumbu'], c)
                self.assertEqual(start-50,c['vars']['sb_prerogative_var'])
                self.assertEqual(1,rt.created)
                self.assertFalse(rt.due())
                rt.effect(EXTRA_EFFECTS['sb_zulu_monthly_dynasty_housekeeping'], c)
                self.assertNotIn('sb_swazi_frontier.094',c.get('events',[]))


class FirearmsSupplyTests(unittest.TestCase):
    def test_dynastic_rebel_inherits_supply_progress_before_journal_initialisation(self):
        for inherited_journal in (False,True):
            rt=FrontierRuntime()
            source=rt.country
            source['vars'].update(sb_firearms_supply_weeks_var=26,sb_firearms_je_seeded_var=1)
            rebels={'id':'ZUL','vars':{},'journals':{'je_sb_adopt_firearms'} if inherited_journal else set(),
                    'market':{'mg:small_arms':{'market_goods_sell_orders':1,'shortage':False}}}
            rt.scopes['sb_court_dynastic_original']=source
            rt.effect(EFFECTS['sb_court_copy_dynastic_firearms'],rebels)
            self.assertEqual({'je_sb_adopt_firearms'},rebels['journals'])
            self.assertEqual(26,rebels['vars']['sb_firearms_supply_weeks_var'])
            self.assertAlmostEqual(6,rebels['vars']['sb_firearms_progress_months_var'])
            self.assertIn('sb_repair_iron_age_weapons_penalty',rebels['native_syncs'])
            weekly=field(field(block('common/journal_entries/1-04_sb_firearms_acquisition.txt','je_sb_adopt_firearms'),'on_weekly_pulse'),'effect')
            rt.effect(weekly,source);rt.effect(weekly,rebels)
            self.assertEqual(26,source['vars']['sb_firearms_supply_weeks_var'])
            self.assertEqual(27,rebels['vars']['sb_firearms_supply_weeks_var'])
            self.assertNotIn('sb_firearms_supply_weeks_var',rt.scopes['root']['vars'])

    def test_dynastic_rebel_inherits_completed_firearms_without_reopening_journal(self):
        rt=FrontierRuntime();rt.country['journals'].discard('je_sb_adopt_firearms')
        rt.country['vars']['sb_firearms_modernized_var']=1
        rebels={'id':'ZUL','vars':{'sb_firearms_applied_tier_var':6},'journals':set(),
                'modifiers':{'sb_iron_age_weapons_6':1}}
        rt.scopes['sb_court_dynastic_original']=rt.country
        rt.effect(EFFECTS['sb_court_copy_dynastic_firearms'],rebels)
        self.assertIn('sb_firearms_modernized_var',rebels['vars'])
        self.assertFalse(rebels['journals']);self.assertFalse(rebels['modifiers'])
        self.assertNotIn('sb_firearms_applied_tier_var',rebels['vars'])
        self.assertNotIn('events',rebels)

    def test_dynastic_copy_does_not_create_an_unrelated_firearms_journal(self):
        rt=FrontierRuntime();rt.country['journals'].discard('je_sb_adopt_firearms')
        rebels={'id':'ZUL','vars':{},'journals':set()}
        rt.scopes['sb_court_dynastic_original']=rt.country
        rt.effect(EFFECTS['sb_court_copy_dynastic_firearms'],rebels)
        self.assertFalse(rebels['vars']);self.assertFalse(rebels['journals'])

    def journal(self):
        return block('common/journal_entries/1-04_sb_firearms_acquisition.txt', 'je_sb_adopt_firearms')

    def tick(self, rt):
        rt.effect(field(field(self.journal(), 'on_weekly_pulse'), 'effect'), rt.country)

    def start(self, rt, tag='ZUL'):
        rt.country['id'] = tag
        rt.effect(field(self.journal(), 'immediate'), rt.country)

    def test_market_supply_and_no_shortage_do_not_require_treaties_or_factories(self):
        rt = FrontierRuntime()
        self.assertEqual([], rt.country['treaties'])
        for amount, shortage, expected in ((0, False, False), (1, True, False), (0.1, False, True)):
            with self.subTest(amount=amount, shortage=shortage):
                rt.country['market']['mg:small_arms'].update(market_goods_sell_orders=amount, shortage=shortage)
                self.assertEqual(expected, rt.condition(EXTRA_TRIGGERS['sb_has_firearms_market_supply'], rt.country))
        self.assertEqual('GBR', rt.scopes['root']['id'])
        rt.country['market'] = {}
        self.assertFalse(rt.condition(EXTRA_TRIGGERS['sb_has_firearms_market_supply'], rt.country))

    def test_260_qualifying_weeks_interruptions_pause_and_completion_stops(self):
        rt = FrontierRuntime(); c = rt.country
        self.start(rt)
        arms = c['market']['mg:small_arms']
        arms['market_goods_sell_orders'] = 1
        for _ in range(40): self.tick(rt)
        for amount, shortage in ((0, False), (1, True)):
            arms.update(market_goods_sell_orders=amount, shortage=shortage)
            for _ in range(10): self.tick(rt)
            self.assertEqual(40, c['vars']['sb_firearms_supply_weeks_var'])
        arms.update(market_goods_sell_orders=1, shortage=False)
        for _ in range(219): self.tick(rt)
        self.assertFalse(rt.condition(field(self.journal(), 'complete'), c))
        self.tick(rt)
        self.assertTrue(rt.condition(field(self.journal(), 'complete'), c))
        self.assertEqual(60, c['vars']['sb_firearms_progress_months_var'])
        self.tick(rt)
        self.assertEqual(260, c['vars']['sb_firearms_supply_weeks_var'])
        rt.effect(field(self.journal(), 'on_complete'), c)
        self.assertIn('sb_firearms_modernized_var', c['vars'])
        self.assertNotIn('sb_firearms_supply_weeks_var', c['vars'])
        rt.effect(EXTRA_EFFECTS['sb_boost_firearms_progress_50'], c)
        self.assertNotIn('sb_firearms_supply_weeks_var', c['vars'])

    def test_completion_preview_does_not_apply_event_rewards_or_prerogative(self):
        event = block('events/sb_firearms_events.txt', 'sb_firearms.001')
        option = field(event, 'option')
        for innovative in (False, True):
            with self.subTest(innovative=innovative):
                rt = FrontierRuntime(); c = rt.country
                self.start(rt)
                c['ruler']['traits'] = {'innovative'} if innovative else set()
                rt.effect(field(self.journal(), 'on_complete'), c)
                self.assertNotIn('sb_new_tactics', c.get('modifiers', {}))
                self.assertEqual(innovative, 'innovative' in c['ruler']['traits'])
                self.assertEqual(['sb_firearms.001'], c['events'])
                rt.effect([n for n in option if n[0] != 'name'], c)
                self.assertIn('sb_new_tactics', c['modifiers'])
                self.assertEqual({'innovative'}, c['ruler']['traits'])
                self.assertEqual(0, c['vars']['sb_prerogative_var'])
                self.assertNotIn('sb_new_tactics', rt.scopes['root'].get('modifiers', {}))

    def test_seeds_and_all_authored_rewards_keep_percentages(self):
        rt = FrontierRuntime(); self.start(rt, 'BST')
        self.assertAlmostEqual(24, rt.country['vars']['sb_firearms_progress_months_var'])
        for name, percent in (
                ('sb_apply_port_natal_raid_firearms_windfall', 10),
                ('sb_boost_firearms_progress_raid', 5), ('sb_boost_firearms_progress_10', 10),
                ('sb_boost_firearms_progress_50', 50), ('sb_boost_firearms_progress_minor', 10),
                ('sb_swazi_apply_guns_for_land_bonus', 40)):
            with self.subTest(reward=name):
                rt = FrontierRuntime(); self.start(rt)
                rt.effect(EXTRA_EFFECTS[name], rt.country)
                self.assertAlmostEqual(percent * .6, rt.country['vars']['sb_firearms_progress_months_var'])
        rt.country['vars']['sb_firearms_supply_weeks_var'] = 250
        rt.effect(EXTRA_EFFECTS['sb_boost_firearms_progress_50'], rt.country)
        self.assertEqual(260, rt.country['vars']['sb_firearms_supply_weeks_var'])
        self.assertEqual(60, rt.country['vars']['sb_firearms_progress_months_var'])

    def test_all_authored_tags_share_gate_and_unrelated_tags_do_not_qualify(self):
        rt = FrontierRuntime()
        for tag in ('ZUL', 'BST', 'SWZ', 'GZA', 'NGN', 'ORA', 'GBR'):
            rt.country['id'] = tag
            self.assertEqual(tag in ('ZUL', 'BST', 'SWZ', 'GZA', 'NGN'), rt.condition(
                EXTRA_TRIGGERS['sb_is_firearms_acquisition_country'], rt.country))
        self.assertNotIn('on_monthly_pulse', [k for k, _, _ in self.journal()])

    def test_natal_and_british_archives_restore_once_with_foreign_root(self):
        for british in (False, True):
            with self.subTest(british=british):
                rt = FrontierRuntime(); c = rt.country
                self.start(rt)
                c['vars']['sb_firearms_supply_weeks_var'] = 104
                rt.effect(EXTRA_EFFECTS['sb_update_firearms_progress'], c)
                natal = {'id': 'NAL', 'alive': True, 'vars': {'sb_natalia_british_colony_resolved_var': 1}}
                rt.countries['c:NAL'] = natal
                if british:
                    gbr = {'id': 'GBR', 'vars': {}}
                    rt.countries['c:GBR'] = gbr
                    rt.scopes['root'] = {'id': 'ORA', 'vars': {}}
                    rt.effect(EXTRA_EFFECTS['sb_british_archive_preannex_zulu_firearms'], gbr)
                    rt.effect(EXTRA_EFFECTS['sb_british_transfer_archived_zulu_firearms_to_natal'], gbr)
                    self.assertNotIn('sb_british_zulu_firearms_archive_var', gbr['vars'])
                else:
                    rt.effect(EXTRA_EFFECTS['sb_natal_archive_zulu_firearms'], c)
                c['journals'].remove('je_sb_adopt_firearms')
                for name in list(c['vars']):
                    if name.startswith('sb_firearms_'): del c['vars'][name]
                rt.effect(EXTRA_EFFECTS['sb_natal_restore_archived_zulu_firearms'], c)
                self.assertEqual(104, c['vars']['sb_firearms_supply_weeks_var'])
                self.assertAlmostEqual(24, c['vars']['sb_firearms_progress_months_var'])
                self.assertNotIn('sb_natal_zulu_firearms_archived_var', natal['vars'])
                c['vars']['sb_firearms_supply_weeks_var'] = 50
                rt.effect(EXTRA_EFFECTS['sb_natal_restore_archived_zulu_firearms'], c)
                self.assertEqual(50, c['vars']['sb_firearms_supply_weeks_var'])


class SwaziCleanupTests(unittest.TestCase):
    def context(self):
        rt = FrontierRuntime(); zulu = rt.country; swazi = rt.countries['c:SWZ']
        play = {'type': 'dp_conquer_state', 'initiator': zulu, 'target': swazi}
        rt.scopes['root'] = play
        zulu['vars'].update(sb_zulu_swazi_play_scope=play, sb_zulu_swazi_disarray_from_muster_var=1)
        zulu['modifiers'] = {'sb_zulu_swazi_frontier_disarray': 1}
        swazi.update(vars={'sb_swazi_defensive_muster_var': 1, 'sb_swazi_ai_history_muster_selected_var': 1},
                     modifiers={'sb_swazi_frontier_muster': 1})
        return rt, play, zulu, swazi

    def test_cleans_exact_participants_after_swz_tag_disappears(self):
        for annexed in (False, True):
            with self.subTest(annexed=annexed):
                rt, play, zulu, swazi = self.context()
                if annexed:
                    swazi['alive'] = False
                    del rt.countries['c:SWZ']
                for _ in range(2):
                    rt.effect(EXTRA_EFFECTS['sb_cleanup_swazi_defensive_muster_for_play'], play)
                    self.assertEqual({}, swazi['vars'])
                    self.assertEqual({}, swazi['modifiers'])
                    self.assertEqual({}, zulu['modifiers'])
                    self.assertNotIn('sb_zulu_swazi_disarray_from_muster_var', zulu['vars'])
                    self.assertIs(play, zulu['vars']['sb_zulu_swazi_play_scope'])

    def test_unrelated_play_wrong_participants_and_missing_handles_do_not_clean(self):
        for invalid in ('other_play', 'wrong_type', 'wrong_target', 'missing_target', 'missing_initiator'):
            with self.subTest(invalid=invalid):
                rt, play, zulu, swazi = self.context()
                if invalid == 'other_play': zulu['vars']['sb_zulu_swazi_play_scope'] = {'id': 'another-play'}
                if invalid == 'wrong_type': play['type'] = 'dp_humiliation'
                if invalid == 'wrong_target': play['target'] = {'id': 'ORA', 'vars': {}}
                if invalid == 'missing_target': del play['target']
                if invalid == 'missing_initiator': del play['initiator']
                rt.effect(EXTRA_EFFECTS['sb_cleanup_swazi_defensive_muster_for_play'], play)
                self.assertIn('sb_swazi_defensive_muster_var', swazi['vars'])
                self.assertIn('sb_zulu_swazi_disarray_from_muster_var', zulu['vars'])


class UthumbuCreationTests(unittest.TestCase):
    def test_creates_registers_and_designates_one_fictional_child(self):
        rt = FrontierRuntime()
        c = rt.country
        c['vars'].update(sb_prerogative_var=50, no_heirs=1, sb_court_owns_heir_blocker_var=1)
        foreign_root = rt.countries['c:ORA']
        rt.scopes['root'] = foreign_root
        history = (ROOT/'common/history/characters/zul - zulu.txt').read_text(encoding='utf-8-sig')
        self.assertNotIn('template = ZUL_uthumbu_claimed_son', history)
        rt.effect(EFFECTS['sb_court_introduce_uthumbu'], c)
        son = c['heir']
        self.assertEqual((1, 0, 'no'), (rt.created, son['age'], son['historical']))
        self.assertEqual(0, c['vars']['sb_prerogative_var'])
        self.assertIs(son, c['vars']['sb_court_recognized_heir_scope'])
        self.assertIn('no_heirs', c['vars'])
        self.assertIs(c, son['vars']['sb_court_home_scope'])
        self.assertIs(foreign_root, rt.scopes['root'])
        self.assertEqual({}, foreign_root['vars'])
        self.assertEqual(2, len(c['members']))
        c['vars']['sb_prerogative_var'] = 100
        rt.effect(EFFECTS['sb_court_introduce_uthumbu'], c)
        self.assertEqual(1, rt.created)
        self.assertEqual(100, c['vars']['sb_prerogative_var'])

    def test_wrong_ruler_and_insufficient_prerogative_do_not_create(self):
        rt = FrontierRuntime()
        rt.country['vars']['sb_prerogative_var'] = 49.99
        rt.effect(EFFECTS['sb_court_introduce_uthumbu'], rt.country)
        self.assertEqual(0, rt.created)
        rt.country['vars']['sb_prerogative_var'] = 100
        rt.country['ruler']['template'] = 'ZUL_mpande_zulu'
        rt.effect(EFFECTS['sb_court_introduce_uthumbu'], rt.country)
        self.assertEqual(0, rt.created)

    def test_existing_identity_is_reused_without_second_registration(self):
        rt = FrontierRuntime()
        son = character('existing-Uthumbu', 0, 0, age=8)
        son.update(template='ZUL_uthumbu_claimed_son', owner=rt.country)
        son['vars']['sb_court_home_scope'] = rt.country
        rt.country['members'].append(son)
        rt.country['characters'].append(son)
        rt.country['vars']['sb_prerogative_var'] = 100
        rt.effect(EFFECTS['sb_court_introduce_uthumbu'], rt.country)
        self.assertIs(son, rt.country['heir'])
        self.assertEqual((0, 2), (rt.created, len(rt.country['members'])))
        self.assertEqual(8, son['age'])
        self.assertEqual(50, rt.country['vars']['sb_prerogative_var'])


if __name__ == '__main__':
    unittest.main()
