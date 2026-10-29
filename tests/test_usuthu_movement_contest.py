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



def evaluate(nodes, state, actor='ZUL', event_root='GBR', movement=None):
    """Evaluate the shipped peaceful-settlement predicate, including absence."""
    variables = {'sb_prerogative_var': state['p']}
    if state.get('participant'): variables['sb_zululand_usuthu_contest_var'] = 1
    if state.get('institutions', True): variables['sb_institutions_active_var'] = 1
    if state.get('war'): variables['sb_court_civil_war_var'] = 'rebel'
    if state.get('accommodation'): variables['sb_court_accommodation_var'] = state['accommodation']
    if state.get('result'): variables['sb_zululand_contest_result_var'] = state['result']
    def check(key, op, value):
        if key == 'NOT': return not evaluate(value, state, actor, event_root, movement)
        if key in ('OR', 'AND'):
            results = [evaluate([n], state, actor, event_root, movement) for n in value]
            return any(results) if key == 'OR' else all(results)
        if key == 'sb_zululand_chiefdoms_situation_active': return state['active'] == (value == 'yes')
        if key == 'has_variable': return value in variables
        if key == 'has_law': return value in state['laws']
        if key.startswith('var:'):
            actual, expected = variables.get(key[4:]), float(value)
            if actual is None: return False
            return {'=': actual == expected, '>=': actual >= expected, '<': actual < expected}[op]
        if key == 'any_political_movement':
            return any(evaluate(value, state, actor, event_root, m) for m in state['movements'])
        if key == 'is_political_movement_type': return movement[0] == value
        if key == 'political_movement_support': return movement[1] >= float(value)
        raise AssertionError((key, op, value))
    return all(check(*n) for n in nodes)


def dispatch(state, event_root='GBR', entry='sb_zululand_check_political_settlement'):
    """Execute real branching and resolver reservation; aftermath is separately checked."""
    actions = []
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
            elif key in ('sb_zululand_resolve_chiefly_contest', 'sb_zululand_resolve_royal_contest'):
                execute(parse(object_block(EFFECTS, key)))
            elif key == 'set_variable':
                d = {k:v for k,o,v in value}
                assert d['name'] == 'sb_zululand_contest_result_var'
                state['result'] = int(d['value'])
            elif key == 'sb_zululand_finalize_political_contest':
                assert state['result'] in (1, 2)
                actions.append((state['country'], state['result']))
                state['active'] = False
            else: raise AssertionError(key)
    execute(parse(object_block(EFFECTS, entry)))
    return actions


class UsuthuMovementContestTests(unittest.TestCase):
    def state(self, side=2, support=.049, **kwargs):
        laws = ({'law_type:law_sb_federated_chiefdoms', 'law_type:law_sb_chiefly_council'} if side == 2
                else {'law_type:law_monarchy', 'law_type:law_autocracy'})
        opposition = 'movement_sb_zulu_royal' if side == 2 else 'movement_sb_zulu_chiefly'
        return dict(active=True, participant=True, country='ZUL', p=50, laws=laws, movements=[(opposition, support)], **kwargs)

    def test_complete_constitution_support_and_prerogative_boundaries(self):
        for side in (1, 2):
            for p, support, wins in ((49.99,.01,False),(50,.05,False),(50,.0499,True),(99,.8,False)):
                state = self.state(side, support); state['p'] = p
                self.assertEqual([('ZUL',side)] if wins else [], dispatch(state))
        state = self.state(); state['laws'] = {'law_type:law_monarchy','law_type:law_sb_chiefly_council'}
        self.assertEqual([], dispatch(state))

    def test_actual_actor_is_independent_of_foreign_event_root(self):
        for root in ('GBR','NAL','WAR'):
            state=self.state();state['country']='REV_ZUL'
            self.assertEqual([('REV_ZUL',2)],dispatch(state,root))

    def test_only_recorded_participants_can_resolve_the_contest(self):
        for side in ('royal','chiefly'):
            entry=f'sb_zululand_resolve_{side}_contest'
            unrelated=self.state(); unrelated.update(country='NGN', participant=False)
            self.assertEqual([],dispatch(unrelated,entry=entry))
            actual=self.state(); actual.update(country='REV_ZUL',p=-80)
            self.assertEqual([('REV_ZUL',1 if side=='royal' else 2)],dispatch(actual,entry=entry))
        unrelated=self.state(); unrelated.update(country='NGN',participant=False)
        self.assertEqual([],dispatch(unrelated))
        copied=object_block('common/scripted_effects/sb_court_constitutional_war_effects.txt','sb_court_track_revolution')
        self.assertIn('set_variable = sb_zululand_usuthu_contest_var',copied)

    def test_war_absence_and_institutional_exit_do_not_fake_consolidation(self):
        for kw in ({'war':True},{'institutions':False},{'result':1}):
            state=self.state(**kw);state['movements']=[]
            self.assertEqual([],dispatch(state))
        state=self.state();state['movements']=[]
        self.assertEqual([('ZUL',2)],dispatch(state))

    def test_explicit_accommodation_is_for_the_incumbent_side(self):
        for side in (1,2):
            self.assertEqual([('ZUL',side)],dispatch(self.state(side,.9,accommodation=side)))
            self.assertEqual([],dispatch(self.state(side,.9,accommodation=3-side)))

    def test_result_is_reserved_before_any_callback_and_never_reawarded(self):
        state=self.state()
        self.assertEqual([('ZUL',2)],dispatch(state))
        state['laws']={'law_type:law_monarchy','law_type:law_autocracy'}
        state['movements']=[]
        self.assertEqual([],dispatch(state))
        for side in ('royal','chiefly'):
            source=object_block(EFFECTS,f'sb_zululand_resolve_{side}_contest')
            self.assertLess(source.index('set_variable ='), source.index('sb_zululand_finalize_political_contest = yes'))
            for accidental_gate in ('sb_prerogative_var','political_movement_support','is_at_war'):
                self.assertNotIn(accidental_gate,source)

    def test_no_deadline_instant_activism_or_scripted_claimant_death(self):
        source=text(EFFECTS)
        for retired in ('sb_zululand_contest_deadline_var','sb_zululand_claimant_is_killed',
                        'sb_zululand_prepare_crown_successor','political_movement_radicalism >= 0.99',
                        'sb_zululand_situation_months_var','add_liberty_desire'):
            self.assertNotIn(retired,source)
        self.assertNotIn('sb_zululand_settlement.113 =',text('events/sb_zululand_settlement_events.txt'))

    def test_partition_has_no_early_victory_or_future_cast_creation(self):
        choice=object_block(EFFECTS,'sb_zululand_choose_thirteen_chiefdoms')
        for premature in ('sb_zululand_zibhebhu_victory_var','sb_zululand_post_annex_incorporation_pending_var'):
            self.assertNotIn(premature,choice)
        exile=object_block(EFFECTS,'sb_zululand_mark_and_exile_royal_house')
        self.assertLess(exile.index('sb_court_ensure_roster'),exile.index('exile_character_with_role_cleanup'))
        self.assertLess(exile.index('save_scope_as = sb_zululand_exile_heir'),exile.index('exile_character_with_role_cleanup'))
        self.assertLess(exile.index('activate_law = law_type:law_sb_chiefly_council'),exile.index('sb_court_select_chiefly_head'))
        for manufactured in ('create_character','ig_petty_bourgeoisie','ZUL_zibhebhu_kamaphitha'):
            self.assertNotIn(manufactured,exile)

    def test_foreign_interventions_keep_commitment_and_use_native_movements(self):
        setup=text('common/scripted_effects/sb_usuthu_politics_effects.txt')
        for forced in ('create_political_lobby','add_lobby_member','royalist_networks','create_political_movement'):
            self.assertNotIn(forced,setup)
        patron=object_block('common/scripted_effects/sb_usuthu_politics_effects.txt','sb_zululand_start_chief_patronage')
        self.assertIn('movement_sb_zulu_chiefly',patron)
        self.assertNotIn('movement_sb_zulu_royal',patron)
        for action in ('policing','usuthu_sponsorship','boer_volunteers'):
            for op in ('start','stop'):
                self.assertIn('movement_sb_zulu_royal',object_block(EFFECTS,f'sb_zululand_{op}_{action}'))
        mark=object_block('common/scripted_effects/sb_usuthu_politics_effects.txt','sb_zululand_mark_boer_commitment')
        self.assertIn('>= 100',mark)
        self.assertNotIn('stop_',mark)

    def test_institutional_exit_stops_costs_without_settling_or_reseeding(self):
        suspend=object_block(EFFECTS,'sb_zululand_suspend_contest_interventions')
        self.assertIn('has_variable = sb_zululand_usuthu_contest_var',suspend)
        self.assertIn('this = global_var:sb_zululand_live_zul_scope',suspend)
        self.assertIn('sb_zululand_stop_contest_interventions = yes',suspend)
        for resets in ('cleanup_situation','resolve_','create_political_movement','remove_variable'):
            self.assertNotIn(resets,suspend)
        stop=object_block(EFFECTS,'sb_zululand_stop_contest_interventions')
        for action in ('policing','chief_patronage','usuthu_sponsorship','boer_volunteers'):
            self.assertIn(f'sb_zululand_stop_{action} = yes',stop)
        core=object_block('common/scripted_effects/sb_institutions_effects.txt','sb_institutions_clear_effects')
        self.assertIn('sb_zululand_suspend_contest_interventions = yes',core)
        participant=object_block(TRIGGERS,'sb_zululand_chiefdoms_involved_actor')
        self.assertIn('this = global_var:sb_zululand_live_zul_scope',participant)
        self.assertNotIn('country_definition = cd:ZUL',participant)
        for number in (110,112):
            incident=object_block('events/sb_zululand_settlement_events.txt',f'sb_zululand_settlement.{number}')
            self.assertIn('limit = { sb_zululand_contest_interventions_available = yes }',incident)
        appeal=object_block(EFFECTS,'sb_zululand_accept_boer_appeal')
        self.assertIn('sb_zululand_contest_interventions_available = yes',appeal)
        self.assertIn('any_scope_pop = { is_pop_type = soldiers total_size >= 500 }',appeal)

    def test_terminal_notifications_do_not_repeat_outcomes(self):
        for number in (120,121,122,123):
            event=object_block('events/sb_zululand_settlement_events.txt',f'sb_zululand_settlement.{number}')
            self.assertIn('NOT = { has_variable = sb_zululand_result_notice_seen_var }',event)
            self.assertNotIn('resolve_',event)
            self.assertNotIn('finalize_',event)
        dispatcher=object_block(EFFECTS,'sb_zululand_finalize_political_contest')
        self.assertLess(dispatcher.index('sb_zululand_cleanup_situation'),dispatcher.index('trigger_event'))
        self.assertLess(dispatcher.index('set_global_variable = sb_zululand_chiefdoms_resolved_global_var'),dispatcher.index('activate_law'))

    def test_bribe_revalidates_the_presented_candidate_before_payment(self):
        offer=object_block(EFFECTS,'sb_zululand_offer_chief_bribe')
        self.assertIn('order_by = prominence',offer)
        self.assertIn('name = sb_zululand_bribe_target_scope value = scope:sb_chief_bribe_candidate',offer)
        event=object_block('events/sb_zululand_settlement_events.txt','sb_zululand_settlement.116')
        self.assertEqual(2,event.count('gold_reserves >= var:sb_zululand_bribe_cost_var'))
        self.assertEqual(2,event.count('sb_zululand_neutral_chief = yes'))
        self.assertIn('add_treasury = sb_zululand_bribe_payment',event)
        self.assertIn('default_option = yes',event)
        neutral = object_block(TRIGGERS,'sb_zululand_neutral_chief')
        self.assertIn('owner ?= global_var:sb_zululand_live_zul_scope',neutral)
        self.assertNotIn('scope:sb_court_country',neutral)

    def test_civilwar_survivor_drives_nrp_holder_and_state(self):
        create=object_block(EFFECTS,'sb_nrp_create_greater_republic')
        goals=object_block(EFFECTS,'sb_nrp_add_boundary_war_goals')
        buildings=object_block(EFFECTS,'sb_nrp_return_building_type_to_zul')
        self.assertIn('p:xE1E455.state.owner = global_var:sb_zululand_live_zul_scope',create)
        self.assertIn('holder = global_var:sb_zululand_live_zul_scope type = return_state',goals)
        self.assertIn('sb_nrp_capture_zulu_state = yes',goals)
        self.assertIn('scope:sb_nrp_setup_actor.var:sb_nrp_relocated_building_levels_var',buildings)
        self.assertNotIn('ROOT',buildings)
        refugees=object_block(EFFECTS,'sb_zululand_unload_zulu_refugees')
        self.assertIn('state = scope:sb_zululand_refugee_destination',refugees)
        self.assertNotIn('region_state:ZUL',refugees)

if __name__ == '__main__': unittest.main()
