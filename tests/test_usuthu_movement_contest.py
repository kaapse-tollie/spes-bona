"""Script-derived contest checks; not a simulation of Victoria's political engine."""
import re
import unittest
from tests.test_zululand_postwar_settlement import object_block, text
from tests.test_natal_zululand_gameplay_contract import object_block_from_source

EFFECTS = 'common/scripted_effects/sb_zululand_settlement_effects.txt'
TRIGGERS = 'common/scripted_triggers/sb_zululand_settlement_triggers.txt'


def parse(source):
    tokens = re.findall(r'\?=|>=|<=|!=|[=<>]|[{}]|"[^"\n]*"|[^\s{}=<>!]+', re.sub(r'#[^\n]*', '', source))
    pos = 0
    def body():
        nonlocal pos
        result = []
        while pos < len(tokens) and tokens[pos] != '}':
            key, op = tokens[pos:pos+2]
            pos += 2
            value = tokens[pos]
            pos += 1
            if value == '{':
                value = body()
                assert tokens[pos] == '}'
                pos += 1
            result.append((key, op, value))
        return result
    return body()[0][2]


def evaluate(nodes, state, actor='NAL', event_root='GBR'):
    def check(key, op, value):
        if key == 'NOT': return not evaluate(value, state, actor, event_root)
        if key in ('AND', 'OR'):
            results = [evaluate([n], state, actor, event_root) for n in value]
            return all(results) if key == 'AND' else any(results)
        if key.startswith('c:'): return evaluate(value, state, key[2:], event_root)
        if key == 'country_definition': return value == 'cd:' + actor
        if key == 'is_country_alive': return state.get('alive', True) == (value == 'yes')
        if key == 'is_direct_subject_of': return state.get('subject', True) and value == 'c:NAL'
        if key == 'is_subject_type': return state.get('chiefdoms', True) and value == 'subject_type_sb_zulu_chiefdoms'
        if key == 'has_global_variable':
            return (state['active'] if value.endswith('open_global_var') else not state['active'])
        if key == 'container_exists': return state['active']
        if key == 'has_variable':
            if value == 'sb_zululand_contest_deadline_var': return not state.get('deadline_expired', state['months'] >= 120)
            assert value == 'sb_zululand_terminal_event_pending_var'
            return state['pending']
        if key.startswith('sb_zululand_'):
            return evaluate(parse(object_block(TRIGGERS, key)), state, actor, event_root) == (value == 'yes')
        if key == 'any_political_movement':
            return state.get('movement', True) and evaluate(value, state, 'movement', event_root)
        if key == 'is_political_movement_type': return value == 'movement_royalist_absolutist'
        if key == 'political_movement_radicalism': return state['activism'] >= float(value)
        if key == 'has_law': return state.get('monarchy', False)
        if key == 'container:sb_zululand_chiefdoms_state.var:sb_zululand_situation_months_var':
            return state['months'] >= float(value)
        raise AssertionError((key, op, value))
    return all(check(*node) for node in nodes)


def dispatch(state, event_root='GBR'):
    """Execute the actual queue's small if/effect vocabulary, including its lease."""
    events = []
    def execute(nodes):
        matched = False
        for key, op, value in nodes:
            if key in ('if', 'else_if'):
                if key == 'if': matched = False
                if matched: continue
                limit = next(v for k, o, v in value if k == 'limit')
                if evaluate(limit, state, event_root=event_root):
                    matched = True
                    execute([n for n in value if n[0] != 'limit'])
            elif key == 'set_variable':
                assert value == 'sb_zululand_terminal_event_pending_var'
                state['pending'] = True
            elif key == 'trigger_event':
                events.append(next(v for k, o, v in value if k == 'id'))
            else: raise AssertionError(key)
    execute(parse(object_block(EFFECTS, 'sb_zululand_queue_terminal_outcome')))
    return events


class UsuthuMovementContestTests(unittest.TestCase):
    def state(self, activism=.5, months=1, **kw):
        return dict(active=True, pending=False, activism=activism, months=months, **kw)

    def test_threshold_and_deadline_from_script_with_foreign_event_root(self):
        for activism, months, expected in ((.989, 119, []), (.99, 1, ['sb_zululand_settlement.121']),
                                          (.99, 120, ['sb_zululand_settlement.121']),
                                          (.5, 120, ['sb_zululand_settlement.120'])):
            for root in ('NAL', 'TRN', 'GBR'):
                self.assertEqual(expected, dispatch(self.state(activism, months), root))

    def test_pending_delivery_and_held_popup_cannot_select_both_endings(self):
        state = self.state(.99, 120)
        self.assertEqual(['sb_zululand_settlement.121'], dispatch(state))
        state['activism'] = .2
        state['months'] += 1
        self.assertEqual([], dispatch(state))
        # Event immediate closes the contest; its acknowledgement has no mutation.
        state.update(active=False, pending=False)
        self.assertEqual([], dispatch(state))
        for event in (120, 121):
            source = object_block('events/sb_zululand_settlement_events.txt', f'sb_zululand_settlement.{event}')
            nodes = parse(source)
            option = next(v for k, o, v in nodes if k == 'option')
            self.assertEqual({'name', 'default_option', 'custom_tooltip'}, {k for k, o, v in option})

    def test_actual_monarchy_reconciles_early_and_invalid_participants_do_not_win(self):
        self.assertEqual(['sb_zululand_settlement.121'], dispatch(self.state(monarchy=True)))
        for kw in ({'alive': False}, {'subject': False}, {'chiefdoms': False}):
            self.assertEqual([], dispatch(self.state(.99, 120, **kw)))

    def test_suppression_and_nondecaying_setup_use_native_modifier_contract(self):
        mods = 'common/static_modifiers/sb_modifiers.txt'
        suppressed = object_block(mods, 'sb_usuthu_suppressed')
        self.assertIn('political_movement_pop_attraction_mult = -1.00', suppressed)
        self.assertIn('political_movement_radicalism_add = -0.20', suppressed)
        outcome = object_block(EFFECTS, 'sb_zululand_apply_zibhebhu_victory')
        self.assertIn('years = 10 is_decaying = yes', outcome)
        movement = text('common/scripted_effects/sb_usuthu_politics_effects.txt')
        self.assertIn('add_modifier = { name = sb_usuthu_royalist_networks }', movement)
        self.assertIn('political_movement_pop_attraction_mult = 0.50', object_block(mods, 'sb_usuthu_royalist_networks'))
        self.assertIn('remove_modifier = sb_usuthu_royalist_networks', object_block(EFFECTS, 'sb_zululand_cleanup_situation'))

    def test_only_usuthu_contest_blocks_its_native_wars(self):
        movement = object_block('common/political_movements/zz_sb_absolutist_override.txt', 'REPLACE:movement_royalist_absolutist')
        for kind in ('revolution', 'secession'):
            branch = object_block_from_source(movement, kind)
            possible = parse(object_block_from_source(branch, 'possible'))
            self.assertIn(('owner', '=', [('NOT', '=', [('has_variable', '=', 'sb_zululand_usuthu_contest_var')])]), possible)
        ideology = text('common/ideologies/sb_usuthu_ideology.txt')
        for law in ('monarchy', 'autocracy'):
            self.assertIn(f'law_{law} = strongly_approve', ideology)
        for law in ('chiefdom', 'elder_council'):
            self.assertIn(f'law_{law} = strongly_disapprove', ideology)

    def test_native_lobbies_and_canonical_ruler_are_scoped_to_zululand(self):
        setup = text('common/scripted_effects/sb_usuthu_politics_effects.txt')
        for lobby in ('pro_overlord', 'anti_overlord'):
            self.assertIn(f'type = lobby_{lobby}', setup)
        for ig in ('landowners', 'armed_forces', 'devout', 'industrialists', 'intelligentsia', 'petty_bourgeoisie'):
            self.assertIn(f'add_interest_group = ig:ig_{ig}', setup)
        exile = object_block(EFFECTS, 'sb_zululand_mark_and_exile_royal_house')
        self.assertEqual(1, exile.count('create_character = { template = ZUL_zibhebhu_kamaphitha }'))
        self.assertNotIn('ZUL_zibhebhu_ka_mapitha', text(EFFECTS) + text('common/character_templates/sb_zulu_dynasty_characters.txt'))
        self.assertIn('set_interest_group = c:ZUL.ig:ig_petty_bourgeoisie', exile)
        self.assertIn('set_character_as_ruler = yes', exile)
        self.assertIn('has_global_variable = sb_zululand_zibhebhu_died_var', exile)

    def test_commitment_cap_does_not_cancel_movement_interventions(self):
        mark = object_block('common/scripted_effects/sb_usuthu_politics_effects.txt', 'sb_zululand_mark_boer_commitment')
        self.assertNotIn('stop_', mark)
        self.assertIn('sb_zululand_boer_committed_var', mark)
        for action in ('policing', 'usuthu_sponsorship', 'boer_volunteers'):
            for op in ('start', 'stop'):
                self.assertIn('is_political_movement_type = movement_royalist_absolutist', object_block(EFFECTS, f'sb_zululand_{op}_{action}'))



    def test_global_journal_weekly_pulse_selects_natal_explicitly(self):
        pulse = object_block_from_source(text('common/journal_entries/1-14_sb_zululand_chiefdoms.txt'), 'on_weekly_pulse')
        self.assertIn('c:NAL ?= { sb_zululand_queue_terminal_outcome = yes }', pulse)
        self.assertNotIn('country_definition', pulse)

    def test_claimant_weight_is_not_overwritten_by_base_value(self):
        weight = object_block_from_source(text('common/political_movements/zz_sb_absolutist_override.txt'), 'character_support_weight')
        self.assertLess(weight.index('value = 200'), weight.index('add = 10000'))

    def test_custom_lobby_names_preserve_unrelated_native_functions(self):
        from pathlib import Path
        from tools.check_override_inventory import extract_top_level_blocks
        game = Path('/Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game')
        path = 'common/customizable_localization/00_ep1_custom_loc.txt'
        if not (game/path).exists(): self.skipTest('Installed Vanilla unavailable')
        upstream = extract_top_level_blocks((game/path).read_text(encoding='utf-8-sig'))
        mod = extract_top_level_blocks(text(path))
        self.assertEqual(upstream.keys(), mod.keys())
        changed = {k for k in upstream if upstream[k] != mod[k]}
        self.assertEqual({'flavored_name_lobby_pro_overlord', 'flavored_name_lobby_anti_overlord'}, changed)
        for name, marker, label in [('pro', 'loyalist', 'sb_zululand_loyalist_lobby_name'), ('anti', 'restorationist', 'sb_zululand_restorationist_lobby_name')]:
            key = f'flavored_name_lobby_{name}_overlord'
            first = object_block_from_source(mod[key], 'text')
            self.assertIn(f'sb_zululand_{marker}_lobby_var', first)
            self.assertIn('sb_zululand_usuthu_contest_var', first)
            self.assertIn(label, first)
            restored = mod[key].replace(first, '', 1).replace('random_valid = no', 'random_valid = yes')
            self.assertEqual(re.sub(r'\s+', '', upstream[key]), re.sub(r'\s+', '', restored))
        self.assertNotIn('REPLACE:', text(path))

    def test_held_incident_revalidates_before_moving_volunteers(self):
        accept = object_block(EFFECTS, 'sb_zululand_accept_boer_appeal')
        self.assertLess(accept.index('sb_zululand_trn_is_eligible_participant'), accept.index('sb_zululand_move_boer_volunteers_to_zululand'))
        self.assertIn('c:NAL ?= { sb_zululand_chiefdoms_runtime_valid = yes }', object_block(TRIGGERS, 'sb_zululand_trn_is_eligible_participant'))
        finish = object_block(EFFECTS, 'sb_zululand_finish_situation_event')
        self.assertLess(finish.index('sb_zululand_chiefdoms_runtime_valid'), finish.index('sb_zululand_set_followup_incident_wait'))


    def test_monthly_incidents_recheck_contest_after_immediate_terminal_cleanup(self):
        monthly = parse(object_block(EFFECTS, 'sb_zululand_chiefdoms_monthly_housekeeping'))
        active_body = monthly[0][2]
        after_queue = active_body[next(i for i,n in enumerate(active_body) if n[0] == 'sb_zululand_queue_terminal_outcome') + 1:]
        incident_gate = next(v for k,o,v in after_queue if k == 'if')
        limit = next(v for k,o,v in incident_gate if k == 'limit')
        state = self.state(.99, 120)
        state.update(active=False, pending=False)
        self.assertFalse(evaluate(limit, state))
        self.assertTrue(evaluate(limit, self.state(.5, 1)))


    def test_deadline_is_elapsed_calendar_time_not_number_of_first_of_month_pulses(self):
        start = object_block(EFFECTS, 'sb_zululand_open_chiefdoms_situation')
        self.assertIn('name = sb_zululand_contest_deadline_var years = 10', start)
        self.assertEqual([], dispatch(self.state(months=120, deadline_expired=False)))
        self.assertEqual(['sb_zululand_settlement.120'], dispatch(self.state(months=119, deadline_expired=True)))
        self.assertEqual(['sb_zululand_settlement.121'], dispatch(self.state(.99, months=120, deadline_expired=True)))

    def test_royal_identities_are_captured_before_laws_change_and_chief_installed_after(self):
        setup = object_block(EFFECTS, 'sb_zululand_choose_thirteen_chiefdoms')
        self.assertNotIn('activate_law', setup)
        exile = object_block(EFFECTS, 'sb_zululand_mark_and_exile_royal_house')
        self.assertLess(exile.index('save_scope_as = sb_zululand_exile_heir'), exile.index('activate_law = law_type:law_chiefdom'))
        self.assertLess(exile.index('transfer_character = c:CAP'), exile.index('activate_law = law_type:law_chiefdom'))
        self.assertLess(exile.index('activate_law = law_type:law_elder_council'), exile.index('set_character_as_ruler = yes'))


    def test_native_absolutist_override_preserves_the_effective_cmf_body(self):
        from pathlib import Path
        from tools.check_override_inventory import find_object
        from tests.test_1_14_3_compatibility import tokens
        cmf = Path(__file__).resolve().parents[2] / 'Community Mod Framework/common/political_movements/ycom_00_ideological_movements.txt'
        if not cmf.exists(): self.skipTest('Installed CMF unavailable')
        upstream = find_object(cmf.read_text(encoding='utf-8-sig'), 'movement_royalist_absolutist', directive='REPLACE')
        body = text('common/political_movements/zz_sb_absolutist_override.txt')
        body = body[body.index('REPLACE:'):]
        # Undo the five scoped lifecycle/presentation-support changes and the
        # added revolution gate; every other CMF token must remain intact.
        modified = body
        for field in ('disband_trigger', 'creation_trigger', 'on_created', 'character_support_weight'):
            body = body.replace(object_block_from_source(body, field), object_block_from_source(upstream, field), 1)
        body = body.replace('possible = { owner = { NOT = { has_variable = sb_zululand_usuthu_contest_var } } }', '', 1)
        body = body.replace('owner = { NOT = { has_variable = sb_zululand_usuthu_contest_var } }', '', 1)
        self.assertEqual(tokens(upstream), tokens(body))
        for field in ('character_ideologies', 'pop_support_trigger', 'pop_support_weight'):
            self.assertEqual(tokens(object_block_from_source(upstream, field)), tokens(object_block_from_source(modified, field)))
        for kind in ('revolution', 'secession'):
            self.assertEqual(tokens(object_block_from_source(object_block_from_source(upstream, kind), 'state_weight')), tokens(object_block_from_source(object_block_from_source(modified, kind), 'state_weight')))

if __name__ == '__main__': unittest.main()




