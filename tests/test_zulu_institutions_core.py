"""Execute the authored institutional values and lifecycle subset, not the V3 engine.

Fixtures supply native law families, movement support, and court cooperation. The
actual source determines clamps, arithmetic, eligibility, state and modifier writes.
"""
from copy import deepcopy
from pathlib import Path
import re
import unittest

from tests.je_outcomes import outcome_field, outcome_nodes

from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import extract_top_level_blocks, find_object

ROOT = Path(__file__).resolve().parents[1]


def definitions(path):
    return {key: statements(body) for key, body in extract_top_level_blocks((ROOT/path).read_text(encoding='utf-8-sig')).items()}


VALUES = definitions('common/script_values/sb_institutions_values.txt')
TRIGGERS = definitions('common/scripted_triggers/sb_institutions_triggers.txt')
TRIGGERS.update(definitions('common/scripted_triggers/sb_court_dynastic_triggers.txt'))
EFFECTS = definitions('common/scripted_effects/sb_institutions_effects.txt')
MODIFIERS = definitions('common/static_modifiers/sb_institutions_modifiers.txt')
BASE_LAWS = {
    'law_monarchy', 'law_traditionalism', 'law_no_police',
    'law_autocracy', 'law_hereditary_bureaucrats', 'law_sb_amabutho_system',
}
PARENTS = {
    'law_sb_amabutho_system': 'law_peasant_levies',
    'test_local_variant': 'law_local_police',
    'test_agrarian_variant': 'law_agrarianism',
    'test_technocracy_variant': 'law_technocracy',
    'test_social_monarchy_variant': 'law_social_monarchy',
}


def country(tag='ZUL', laws=None):
    return {'tag': tag, 'laws': set(BASE_LAWS if laws is None else laws), 'vars': {}, 'modifiers': {}, 'movements': [], 'journals': set(), 'cooperation': 0}


class Runtime:
    def __init__(self):
        self.root = country('GBR', {'law_parliamentary_republic'})
        self.zul = country()
        self.globals = {'sb_institutions_lobby_ready_global_var': True}
        self.calls = []
        self.params = {}

    def number(self, value, scope, prev=None):
        if isinstance(value, list): return self.value(value, scope, prev)
        if value.startswith('var:'): return scope['vars'][value[4:]]
        if value.startswith('prev.'): return self.number(value[5:], prev)
        if value.startswith('$'): return self.params[value.strip('$')]
        if value in VALUES: return self.value(VALUES[value], scope, prev)
        if value == 'sb_court_royal_support': return sum(m.get('support', 0) for m in scope['movements'] if m['type'] == 'movement_sb_zulu_royal')
        if value == 'sb_court_chiefly_support': return sum(m.get('support', 0) for m in scope['movements'] if m['type'] == 'movement_sb_zulu_chiefly')
        if value == 'political_movement_support': return scope['support']
        if value == 'political_movement_radicalism': return scope['activism']
        return float(value)

    def condition(self, nodes, scope):
        results = []
        for key, op, value in nodes:
            if key == 'custom_tooltip': result = self.condition([n for n in value if n[0] != 'text'], scope)
            elif key == 'NOT': result = not any(self.condition([n], scope) for n in value)
            elif key == 'OR': result = any(self.condition([n], scope) for n in value)
            elif key == 'NOR': result = not any(self.condition([n], scope) for n in value)
            elif key == 'AND': result = self.condition(value, scope)
            elif key in TRIGGERS: result = self.condition(TRIGGERS[key], scope) == (value == 'yes')
            elif key == 'sb_is_zulu_dynasty_country': result = scope.get('tag') == 'ZUL' or (scope.get('tag') == 'NGN' and 'sb_ngu_inherited_zul_content_var' in scope['vars'])
            elif key == 'sb_chiefs_contest_country': result = scope.get('partition_contest', False) == (value == 'yes')
            elif key == 'has_variable': result = value in scope['vars']
            elif key == 'has_modifier': result = value in scope['modifiers']
            elif key == 'has_global_variable': result = value in self.globals
            elif key == 'is_country_alive': result = scope.get('alive', True) == (value == 'yes')
            elif key == 'has_journal_entry': result = value in scope['journals']
            elif key in ('has_law', 'has_law_or_variant'):
                laws = set(scope['laws'])
                if key == 'has_law_or_variant': laws |= {PARENTS[l] for l in laws if l in PARENTS}
                result = value.removeprefix('law_type:') in laws
            elif key == 'any_political_movement': result = any(self.condition(value, m) for m in scope['movements'])
            elif key == 'is_political_movement_type': result = value == scope['type']
            elif key == 'owner': result = self.condition(value, scope.get('owner', self.zul))
            elif key == 'always': result = value == 'yes'
            else:
                left = self.number(key, scope); right = self.number(value, scope)
                result = {'=': left == right, '>': left > right, '>=': left >= right, '<': left < right, '<=': left <= right}[op]
            results.append(result)
        return all(results)

    def branches(self, nodes, scope):
        matched = False
        for key, op, value in nodes:
            if key in ('if', 'else_if', 'else'):
                if key == 'if': matched = False
                if matched: continue
                limit = next((v for k, _, v in value if k == 'limit'), [])
                if self.condition(limit, scope):
                    matched = True
                    yield from self.branches([n for n in value if n[0] != 'limit'], scope)
            else: yield key, op, value

    def value(self, nodes, scope, prev=None):
        result = 0
        for key, op, value in self.branches(nodes, scope):
            if key == 'every_political_movement':
                limit = next((v for k, _, v in value if k == 'limit'), [])
                for movement in scope['movements']:
                    if self.condition(limit, movement):
                        result += self.value([n for n in value if n[0] != 'limit'], movement, scope)
                continue
            amount = self.number(value, scope, prev)
            if key == 'value': result = amount
            elif key == 'add': result += amount
            elif key == 'subtract': result -= amount
            elif key == 'multiply': result *= amount
            elif key == 'divide': result /= amount
            elif key == 'min': result = max(result, amount)
            elif key == 'max': result = min(result, amount)
            else: raise AssertionError(key)
        return result

    def effect(self, nodes, scope, prev=None):
        for key, op, value in self.branches(nodes, scope):
            if key == 'hidden_effect': self.effect(value, scope, prev)
            elif key in EFFECTS: self.effect(EFFECTS[key], scope, prev)
            elif key == 'set_variable':
                if isinstance(value, str): scope['vars'][value] = True
                else:
                    fields = {k: v for k, _, v in value}
                    scope['vars'][fields['name']] = self.number(fields['value'], scope, prev)
            elif key == 'change_variable':
                fields = {k: v for k, _, v in value}
                scope['vars'][fields['name']] += self.number(fields['add'], scope, prev)
            elif key == 'remove_variable': scope['vars'].pop(value, None)
            elif key == 'add_modifier':
                fields = {k: v for k, _, v in value}
                scope['modifiers'][fields['name']] = self.number(fields.get('multiplier', '1'), scope, prev)
            elif key == 'remove_modifier':
                # Native removal reports a script error when the modifier is absent.
                if value not in scope['modifiers']: raise AssertionError(('absent modifier', value))
                del scope['modifiers'][value]
            elif key == 'every_political_movement':
                limit = next((v for k, _, v in value if k == 'limit'), [])
                for movement in scope['movements']:
                    if self.condition(limit, movement): self.effect([n for n in value if n[0] != 'limit'], movement, scope)
            elif key == 'create_political_movement':
                kind = next(v for k, _, v in value if k == 'type')
                scope['movements'].append({'type': kind, 'modifiers': {}, 'support': 0, 'vars': {}})
            elif key == 'add_journal_entry':
                # Native JE activation accesses the country AI before its scripted immediate.
                if not scope.get('ai_ready', True): raise AssertionError('journal activation before country AI creation')
                journal = next(v for k, _, v in value if k == 'type')
                if journal in scope['journals']: raise AssertionError(('duplicate journal', journal))
                scope['journals'].add(journal)
            elif key == 'je:je_sb_zulu_kingdom':
                if 'je_sb_zulu_kingdom' in scope['journals']:
                    self.effect(value, {'owner': scope}, scope)
            elif key == 'set_bar_progress':
                fields = {k: v for k, _, v in value}
                scope['owner']['bar'] = self.number(fields['value'], scope, prev)
            elif key == 'owner': self.effect(value, scope['owner'], scope)
            elif key == 'sb_court_calculate_backing': scope['vars']['sb_prerogative_cooperation_var'] = scope['cooperation']
            # Native law cleanup is traced, not simulated by this institutional fixture.
            elif key in ('scripted_effect_parties_disappearence', 'cleanup_voting_strength_modifiers'):
                self.calls.append((key, scope['tag']))
            # Court identity/callback behaviour is executed in test_zulu_court_rework;
            # the minor-heir grant is covered in test_zulu_recognition_backing.
            elif key in ('sb_court_check_claimant_challenge', 'sb_court_reconcile_dynastic_record', 'sb_court_update_heir_blocker', 'sb_court_ensure_roster', 'sb_court_select_chiefly_head', 'sb_court_monthly_housekeeping', 'sb_court_sync_chiefly_concessions', 'sb_court_annual_allegiances', 'sb_court_reconcile_minor_backing', 'sb_court_mpande_sons_come_of_age', 'sb_court_deck_monthly', 'sb_court_suspend', 'sb_zululand_suspend_contest_interventions', 'sb_zulu_monthly_dynasty_housekeeping', 'sb_zululand_check_political_settlement'):
                self.calls.append((key, scope['tag']))
            else: raise AssertionError(key)

    def call(self, name, scope=None): self.effect(EFFECTS[name], self.zul if scope is None else scope)
    def calc(self, name, scope=None): return self.value(VALUES[name], self.zul if scope is None else scope)


class InstitutionalArithmeticTests(unittest.TestCase):
    def test_current_effects_use_applied_modifiers_and_handle_zero_and_reformed_army(self):
        custom = definitions('common/customizable_localization/sb_court_custom_loc.txt')['sb_prerogative_current_effects']
        rt = Runtime(); rt.call('sb_institutions_reconcile')

        def selected_text():
            for key, _, body in custom:
                if key != 'text': continue
                fields = {k: v for k, _, v in body}
                if rt.condition(fields.get('trigger', []), rt.zul):
                    return fields['localization_key']

        self.assertEqual('sb_prerogative_effects_active', selected_text())
        for score in (-100, 50):
            rt.zul['vars']['sb_prerogative_var'] = score
            rt.call('sb_institutions_recalculate')
            self.assertEqual('sb_prerogative_effects_active', selected_text())
            self.assertEqual(score / 100, rt.zul['modifiers']['sb_prerogative_political'])
        rt.zul['laws'].remove('law_sb_amabutho_system')
        rt.zul['laws'].add('law_professional_army')
        rt.call('sb_institutions_recalculate')
        self.assertNotIn('sb_prerogative_military', rt.zul['modifiers'])
        self.assertEqual('sb_prerogative_effects_active', selected_text())
        loc = (ROOT/'localization/english/sb_institutions_l_english.yml').read_text(encoding='utf-8-sig')
        active = next(line for line in loc.splitlines() if line.startswith(' sb_prerogative_effects_active:'))
        for modifier in ('sb_prerogative_base_legitimacy', 'sb_prerogative_political', 'sb_prerogative_military'):
            self.assertIn(f"JournalEntry.GetCountry.GetTimedModifier('{modifier}').GetDesc", active)
        self.assertNotIn('GetStaticModifier', active)
        rt.call('sb_institutions_clear_effects')
        self.assertEqual('sb_prerogative_effects_none', selected_text())

    def test_internal_recalculation_does_not_expose_modifier_replacement_effects(self):
        for name in ('sb_institutions_recalculate', 'sb_institutions_clear_effects'):
            self.assertEqual(['hidden_effect'], [k for k, _, _ in EFFECTS[name]])
        court = definitions('common/scripted_effects/sb_court_politics_effects.txt')
        self.assertEqual(['hidden_effect'], [k for k, _, _ in court['sb_court_calculate_backing']])

    def test_type_title_is_context_free_and_live_heading_uses_the_actual_owner(self):
        # IsInGame is true even when a preview only supplies JournalEntryType.
        loc = {}
        for path in ('sb_l_english.yml', 'sb_institutions_l_english.yml'):
            for line in (ROOT/'localization/english'/path).read_text(encoding='utf-8-sig').splitlines():
                match = re.fullmatch(r'\s*(\w+):\d* "(.*)"', line)
                if match: loc[match[1]] = match[2]
        self.assertEqual('Prerogative', loc['je_sb_zulu_kingdom'])
        # The context-free key is used in the lobby, type-only in-game hovers
        # and foreign-country previews. No selector can dereference a missing JE.
        self.assertNotRegex(loc['je_sb_zulu_kingdom'], r'[\[$]')
        self.assertTrue(loc['sb_prerogative_live_readout'].startswith('$sb_prerogative_country_title$:'))
        self.assertEqual("[JournalEntry.GetCountry.GetCustom('sb_prerogative_title')]", loc['sb_prerogative_country_title'])
        self.assertNotIn('GetPlayer', loc['sb_prerogative_country_title'])
        custom = definitions('common/customizable_localization/sb_court_custom_loc.txt')['sb_prerogative_title']
        choices = [{k: v for k, _, v in body} for key, _, body in custom if key == 'text']
        rt = Runtime()
        for tag in ('ZUL', 'NGN'):
            for law, other_law, expected in (
                ('law_monarchy', 'law_sb_federated_chiefdoms', 'Royal Prerogative'),
                ('law_sb_federated_chiefdoms', 'law_monarchy', 'Chiefly Prerogative'),
                ('law_social_monarchy', 'law_sb_federated_chiefdoms', 'Royal Prerogative'),
            ):
                rt.root['laws'] = {other_law}
                owner = country(tag, {law})
                selected = next(c['localization_key'] for c in choices if rt.condition(c.get('trigger', []), owner))
                self.assertEqual(expected, loc[selected])

    def test_institutional_reach_has_named_condition(self):
        tooltip = next(body for key, _, body in TRIGGERS['sb_institutions_eligible'] if key == 'custom_tooltip')
        self.assertIn(('text', '=', 'sb_institutions_reach_positive_tt'), tooltip)
        self.assertIn(('sb_institutional_reach', '>', '0'), tooltip)

    def test_current_country_readout_uses_actual_activism_without_intervention_pressure(self):
        rt = Runtime()
        rt.root['movements'] = [{'type': 'movement_sb_zulu_royal', 'support': .9, 'activism': .99}]
        rt.zul['movements'] = [
            {'type': 'movement_sb_zulu_royal', 'support': .12, 'activism': .24},
            {'type': 'movement_sb_zulu_chiefly', 'support': .35, 'activism': .67},
            {'type': 'movement_sb_zulu_traditionalist', 'support': .42, 'activism': .18},
            {'type': 'movement_liberal', 'support': .2, 'activism': 1},
        ]
        self.assertEqual(.24, rt.calc('sb_institutions_royal_activism'))
        self.assertEqual(.67, rt.calc('sb_institutions_chiefly_activism'))
        rt.zul['movements'] = []
        self.assertEqual(0, rt.calc('sb_institutions_royal_activism'))

    def test_cap_after_offset_and_parent_variant_mapping(self):
        rt = Runtime()
        self.assertEqual(50, rt.calc('sb_institutional_reach'))
        rt.zul['laws'].discard('law_no_police'); rt.zul['laws'].add('law_local_police')
        self.assertEqual(50, rt.calc('sb_institutional_reach'))
        rt.zul['laws'].discard('law_traditionalism'); rt.zul['laws'].add('law_agrarianism')
        self.assertEqual(50, rt.calc('sb_institutional_reach'))
        rt.zul['laws'].discard('law_agrarianism'); rt.zul['laws'].add('test_agrarian_variant')
        rt.zul['laws'].discard('law_local_police'); rt.zul['laws'].add('test_local_variant')
        self.assertEqual(50, rt.calc('sb_institutional_reach'))

    def test_modernization_accumulates_then_clamps(self):
        rt = Runtime()
        rt.zul['laws'] = {'law_social_monarchy', 'law_interventionism', 'law_militarized_police', 'law_census_voting', 'law_elected_bureaucrats', 'law_professional_army'}
        self.assertEqual(0, rt.calc('sb_institutional_reach'))
        rt.zul['laws'] = {'law_monarchy', 'law_agrarianism', 'law_local_police', 'law_landed_voting', 'law_appointed_bureaucrats', 'law_sb_amabutho_system'}
        self.assertEqual(35, rt.calc('sb_institutional_reach'))
        rt.zul['laws'].remove('law_sb_amabutho_system'); rt.zul['laws'].add('law_professional_army')
        self.assertEqual(30, rt.calc('sb_institutional_reach'))

    def test_explicit_exits_are_separate_from_universal_suffrage_arithmetic(self):
        rt = Runtime()
        rt.zul['laws'] -= {'law_autocracy', 'law_no_police'}
        rt.zul['laws'] |= {'law_local_police', 'law_universal_suffrage'}
        self.assertEqual(5, rt.calc('sb_institutional_reach'))
        self.assertTrue(rt.condition(TRIGGERS['sb_institutions_eligible'], rt.zul))
        for law in ('law_technocracy', 'law_single_party_state', 'law_anarchy', 'test_technocracy_variant'):
            rt.zul['laws'].discard('law_universal_suffrage'); rt.zul['laws'].add(law)
            self.assertFalse(rt.condition(TRIGGERS['sb_institutions_eligible'], rt.zul), law)
            rt.zul['laws'].remove(law)
        rt.zul['laws'].remove('law_monarchy'); rt.zul['laws'].add('law_parliamentary_republic')
        self.assertFalse(rt.condition(TRIGGERS['sb_institutions_eligible'], rt.zul))

    def test_continuous_modifier_endpoints_morale_sign_and_army_reform(self):
        rt = Runtime(); rt.call('sb_institutions_reconcile')
        for p, reach in [(100, 50), (-100, 50), (50, 25), (-50, 25), (0, 50)]:
            rt.zul['vars']['sb_prerogative_var'] = p
            rt.zul['vars']['sb_institutional_reach_var'] = reach
            scale = rt.calc('sb_prerogative_effect_scale')
            self.assertAlmostEqual(p / 100 * reach / 50, scale)
            mods = {}
            for name, nodes in MODIFIERS.items():
                multiplier = rt.calc('sb_institutional_effect_scale') if name == 'sb_prerogative_base_legitimacy' else scale
                for key, _, amount in nodes:
                    if key != 'icon':
                        mods[key] = mods.get(key, 0) + float(amount) * multiplier
            self.assertAlmostEqual((p / 2 - 25) * reach / 50, mods['country_legitimacy_base_add'])
            self.assertAlmostEqual(-mods['building_training_rate_mult'], mods['unit_morale_loss_mult'])
        rt.zul['vars']['sb_prerogative_var'] = -100
        rt.call('sb_institutions_recalculate')
        self.assertEqual(-1, rt.zul['modifiers']['sb_prerogative_political'])
        rt.zul['laws'].remove('law_sb_amabutho_system'); rt.zul['laws'].add('law_professional_army')
        rt.call('sb_institutions_reconcile')
        self.assertNotIn('sb_prerogative_military', rt.zul['modifiers'])
        self.assertAlmostEqual(-.9, rt.zul['modifiers']['sb_prerogative_political'])

    def test_supported_target_and_monthly_convergence_never_accumulate_past_target(self):
        rt = Runtime(); rt.call('sb_institutions_reconcile')
        rt.zul['cooperation'] = 40
        rt.zul['movements'][0]['support'] = .4
        rt.zul['movements'][1]['support'] = .2
        rt.zul['movements'][2]['support'] = .9
        rt.call('sb_institutions_recalculate')
        self.assertAlmostEqual(35, rt.zul['vars']['sb_prerogative_target_var'])
        previous = 0
        for _ in range(120):
            rt.call('sb_institutions_monthly_update')
            current = rt.zul['vars']['sb_prerogative_var']
            self.assertGreaterEqual(current, previous)
            self.assertLessEqual(current - previous, 4.000001)
            self.assertLessEqual(current, 35)
            previous = current
        self.assertAlmostEqual(35, previous, places=5)
        rt.zul['laws'].remove('law_monarchy'); rt.zul['laws'].add('law_sb_federated_chiefdoms')
        self.assertAlmostEqual(-20, rt.calc('sb_prerogative_movement_balance'))

    def test_spending_and_events_respect_hard_endpoints(self):
        rt = Runtime(); rt.call('sb_institutions_reconcile')
        rt.params['VALUE'] = 200; rt.call('sb_change_prerogative')
        self.assertEqual(100, rt.zul['vars']['sb_prerogative_var'])
        rt.params['VALUE'] = -25; rt.call('sb_change_prerogative')
        self.assertEqual(75, rt.zul['vars']['sb_prerogative_var'])
        rt.params['VALUE'] = -400; rt.call('sb_change_prerogative')
        self.assertEqual(-100, rt.zul['vars']['sb_prerogative_var'])

    def test_zero_is_neutral_for_spending_and_monthly_arithmetic(self):
        rt = Runtime(); rt.call('sb_institutions_reconcile')
        rt.zul['vars']['sb_prerogative_var'] = 25
        rt.params['VALUE'] = -25; rt.call('sb_change_prerogative')
        self.assertEqual(0, rt.zul['vars']['sb_prerogative_var'])
        self.assertNotIn('sb_prerogative_political', rt.zul['modifiers'])
        self.assertNotIn('sb_prerogative_military', rt.zul['modifiers'])
        # A capped opposing drift can land exactly on zero too.
        rt.zul['vars']['sb_prerogative_var'] = 4
        rt.zul['cooperation'] = -100
        rt.call('sb_institutions_monthly_update')
        self.assertEqual(0, rt.zul['vars']['sb_prerogative_var'])
        self.assertEqual(50, rt.zul['bar'])


class InstitutionalLifecycleTests(unittest.TestCase):
    def test_neutral_recalculation_and_repeated_exit_do_not_remove_absent_modifiers(self):
        rt = Runtime()
        for _ in range(3): rt.call('sb_institutions_reconcile')
        self.assertEqual({'sb_prerogative_base_legitimacy': 1}, rt.zul['modifiers'])
        rt.zul['laws'].remove('law_monarchy'); rt.zul['laws'].add('law_parliamentary_republic')
        for _ in range(3): rt.call('sb_institutions_reconcile')
        self.assertEqual({}, rt.zul['modifiers'])

    def test_history_law_activation_does_not_add_the_history_authored_journal_twice(self):
        rt = Runtime(); rt.globals.clear()
        source = statements(find_object((ROOT/'common/on_actions/sb_institutions_on_actions.txt').read_text(encoding='utf-8-sig'), 'sb_on_institutions_law'))
        trigger = next(v for k, _, v in source if k == 'trigger')
        effect = next(v for k, _, v in source if k == 'effect')
        law = {'owner': rt.zul}
        self.assertFalse(rt.condition(trigger, law))
        if rt.condition(trigger, law): rt.effect(effect, law)
        rt.effect([('add_journal_entry', '=', [('type', '=', 'je_sb_zulu_kingdom')])], rt.zul)
        rt.globals['sb_institutions_lobby_ready_global_var'] = True
        rt.call('sb_institutions_reconcile')
        rt.call('sb_institutions_reconcile')
        self.assertEqual({'je_sb_zulu_kingdom'}, rt.zul['journals'])

    def test_reentry_retains_political_commitments_rewards_and_seed_marker(self):
        rt = Runtime(); before_root = deepcopy(rt.root)
        rt.call('sb_institutions_reconcile')
        rt.zul['vars']['sb_prerogative_var'] = 67
        rt.zul['vars']['earned_reward'] = True
        rt.zul['vars']['recorded_claimant'] = 123
        rt.zul['movements'][0]['support'] = .35
        rt.call('sb_institutions_recalculate')
        original = deepcopy(rt.zul['movements'])
        rt.zul['laws'].remove('law_monarchy'); rt.zul['laws'].add('law_parliamentary_republic')
        rt.call('sb_institutions_reconcile')
        self.assertNotIn('sb_institutions_active_var', rt.zul['vars'])
        self.assertIn(('sb_court_suspend', 'ZUL'), rt.calls)
        self.assertNotIn(('sb_zululand_suspend_contest_interventions', 'ZUL'), rt.calls)
        self.assertEqual({}, rt.zul['modifiers'])
        rt.zul['journals'].clear()  # Native invalidation removes the JE.
        rt.zul['laws'].remove('law_parliamentary_republic'); rt.zul['laws'].add('law_monarchy')
        rt.call('sb_institutions_reconcile')
        self.assertEqual(67, rt.zul['vars']['sb_prerogative_var'])
        self.assertTrue(rt.zul['vars']['earned_reward'])
        self.assertEqual(123, rt.zul['vars']['recorded_claimant'])
        self.assertEqual(original, rt.zul['movements'])
        self.assertEqual(before_root, rt.root)

    def test_seeding_does_not_refresh_existing_or_recreate_lost_movements(self):
        rt = Runtime()
        rt.zul['movements'] = [{'type': 'movement_sb_zulu_royal', 'support': .22, 'vars': {}, 'modifiers': {'native_initial_enthusiasm': .1}}]
        original = deepcopy(rt.zul['movements'][0])
        rt.call('sb_institutions_reconcile')
        self.assertEqual(original, rt.zul['movements'][0])
        self.assertEqual(3, len(rt.zul['movements']))
        rt.zul['movements'].pop(1)
        rt.call('sb_institutions_reconcile')
        self.assertEqual(2, len(rt.zul['movements']))
        self.assertNotIn('disband_political_movement', (ROOT/'common/scripted_effects/sb_institutions_effects.txt').read_text())

    def test_ngn_profile_boundary_and_unrelated_country_negative(self):
        rt = Runtime(); unrelated = country('GZA'); before = deepcopy(unrelated)
        rt.call('sb_institutions_reconcile', unrelated)
        self.assertEqual(before, unrelated)
        ngn = country('NGN'); rt.call('sb_institutions_reconcile', ngn)
        self.assertFalse(ngn['vars'])
        ngn['vars']['sb_ngu_inherited_zul_content_var'] = True
        rt.call('sb_institutions_reconcile', ngn)
        self.assertIn('sb_institutions_active_var', ngn['vars'])

    def test_journal_invalidation_is_not_completion_and_does_not_reset_political_state(self):
        source = (ROOT/'common/journal_entries/1-03_sb_zulu_kingdom.txt').read_text(encoding='utf-8-sig')
        from tests.test_zulu_institutions_laws import child
        for terminal in ('complete =', 'on_complete =', 'fail =', 'on_fail =', 'timeout ='):
            self.assertNotIn(terminal, source)
        invalid = statements(outcome_field(source, 'invalid', 'effect'))
        rt = Runtime(); rt.call('sb_institutions_reconcile')
        rt.zul['vars']['sb_prerogative_var'] = 71
        rt.zul['vars']['earned_reward'] = True
        before = deepcopy(rt.zul['vars'])
        rt.effect(invalid, rt.zul)
        expected = {k: v for k, v in before.items() if k != 'sb_institutions_active_var'}
        self.assertEqual(expected, rt.zul['vars'])
        self.assertEqual({}, rt.zul['modifiers'])
        rt.zul['journals'].clear()
        rt.call('sb_institutions_reconcile')
        self.assertIn('je_sb_zulu_kingdom', rt.zul['journals'])
        self.assertEqual(71, rt.zul['vars']['sb_prerogative_var'])

    def test_inherited_laws_do_not_initialise_an_unfinished_rebel_country(self):
        source = statements(find_object((ROOT/'common/on_actions/sb_institutions_on_actions.txt').read_text(encoding='utf-8-sig'), 'sb_on_institutions_law'))
        hook = {k: v for k, _, v in source}
        for tag, inherited_profile in (('ZUL', False), ('REB', True)):
            with self.subTest(tag=tag):
                rt = Runtime()
                original = deepcopy(rt.zul)
                rebels = country(tag)
                rebels.update(alive=False, ai_ready=False)
                if inherited_profile: rebels['vars']['sb_institutions_zulu_profile_var'] = True
                before = deepcopy(rebels)
                law = {'owner': rebels}
                # CreateCountry inherits laws before transferring land and creating the AI.
                for _ in range(len(BASE_LAWS)):
                    if rt.condition(hook['trigger'], law): rt.effect(hook['effect'], law)
                self.assertEqual(before, rebels)
                self.assertEqual(original, rt.zul)
                self.assertNotIn('vars', law)
                # The existing post-split reconciliation runs after native creation completes.
                rebels.update(alive=True, ai_ready=True)
                rt.call('sb_institutions_reconcile', rebels)
                rt.call('sb_institutions_reconcile', rebels)
                self.assertEqual({'je_sb_zulu_kingdom'}, rebels['journals'])
                self.assertEqual(3, len(rebels['movements']))
                self.assertTrue(rebels['vars']['sb_institutions_active_var'])
                self.assertEqual(original, rt.zul)

    def test_direct_law_activation_waits_for_history_and_country_creation(self):
        laws = definitions('common/laws/05_sb_chiefly_constitution.txt')
        hook = {k: v for k, _, v in statements(find_object((ROOT/'common/on_actions/sb_institutions_on_actions.txt').read_text(encoding='utf-8-sig'), 'sb_on_institutions_law'))}
        for law_name, definition in laws.items():
            activation = next(v for k, _, v in definition if k == 'on_activate')
            for tag in ('ZUL', 'REB'):
                for lobby_ready, alive in ((True, False), (False, True), (False, False)):
                    with self.subTest(law=law_name, tag=tag, lobby_ready=lobby_ready, alive=alive):
                        rt = Runtime(); original = deepcopy(rt.zul); foreign = deepcopy(rt.root)
                        if not lobby_ready: rt.globals.clear()
                        owner = country(tag)
                        owner['laws'].discard('law_monarchy' if law_name == 'law_sb_federated_chiefdoms' else 'law_autocracy')
                        owner['laws'].add(law_name)
                        owner.update(alive=alive, ai_ready=alive)
                        if tag == 'REB': owner['vars']['sb_institutions_zulu_profile_var'] = True
                        before = deepcopy(owner); law = {'owner': owner}
                        for _ in range(2):
                            # LawType.on_activate enters the country directly; the on-action
                            # separately supplies a Law root. Both paths must be safe.
                            rt.effect(activation, owner)
                            if rt.condition(hook['trigger'], law): rt.effect(hook['effect'], law)
                        self.assertEqual(before, owner)
                        self.assertEqual(original, rt.zul)
                        self.assertEqual(foreign, rt.root)
                        self.assertNotIn('vars', law)
                        if not lobby_ready:
                            # History owns the opening entry before the bootstrap runs.
                            owner.update(alive=True, ai_ready=True)
                            rt.effect([('add_journal_entry', '=', [('type', '=', 'je_sb_zulu_kingdom')])], owner)
                        owner.update(alive=True, ai_ready=True)
                        rt.globals['sb_institutions_lobby_ready_global_var'] = True
                        # Existing bootstrap/post-split reconciliation and later reforms
                        # must still initialise once, even when both callbacks repeat.
                        for _ in range(2):
                            rt.call('sb_institutions_reconcile', owner)
                            rt.effect(activation, owner)
                            if rt.condition(hook['trigger'], law): rt.effect(hook['effect'], law)
                        self.assertEqual({'je_sb_zulu_kingdom'}, owner['journals'])
                        self.assertEqual(3, len(owner['movements']))
                        self.assertTrue(owner['vars']['sb_institutions_active_var'])
                        self.assertEqual(original, rt.zul)
                        self.assertEqual(foreign, rt.root)

    def test_law_callback_still_handles_reforms_and_reentry_for_finished_countries(self):
        hook = {k: v for k, _, v in statements(find_object((ROOT/'common/on_actions/sb_institutions_on_actions.txt').read_text(encoding='utf-8-sig'), 'sb_on_institutions_law'))}
        rt = Runtime(); law = {'owner': rt.zul}
        for royal in (True, False, True):
            rt.zul['laws'].difference_update({'law_monarchy', 'law_parliamentary_republic'})
            rt.zul['laws'].add('law_monarchy' if royal else 'law_parliamentary_republic')
            self.assertTrue(rt.condition(hook['trigger'], law))
            rt.effect(hook['effect'], law)
            self.assertEqual(royal, 'sb_institutions_active_var' in rt.zul['vars'])
            self.assertEqual(royal, 'sb_prerogative_base_legitimacy' in rt.zul['modifiers'])
        for owner in (country('GZA'), dict(rt.zul, alive=False)):
            self.assertFalse(rt.condition(hook['trigger'], {'owner': owner}))

    def test_law_callback_enters_owner_instead_of_evaluating_country_predicates_on_law_root(self):
        rt = Runtime(); before = deepcopy(rt.root)
        source = statements(find_object((ROOT/'common/on_actions/sb_institutions_on_actions.txt').read_text(encoding='utf-8-sig'), 'sb_on_institutions_law'))
        trigger = next(v for k, _, v in source if k == 'trigger')
        effect = next(v for k, _, v in source if k == 'effect')
        law = {'owner': rt.zul}
        self.assertTrue(rt.condition(trigger, law))
        rt.effect(effect, law)
        self.assertIn('sb_institutions_active_var', rt.zul['vars'])
        self.assertNotIn('vars', law)
        self.assertEqual(before, rt.root)


if __name__ == '__main__':
    unittest.main()
