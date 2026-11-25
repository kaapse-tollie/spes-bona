"""Source-executed fixes; native JE age, popup timing and rendering need DP replay."""
import datetime
import unittest
from unittest.mock import patch
from tests.test_chiefdoms_refinement import Contest, E, T, defs, entity, source
from tools.check_override_inventory import find_object
from tests.test_zulu_institutions_laws import statements

VALUES = defs('common/script_values/sb_zululand_drift_values.txt')
RULES = defs('common/scripted_triggers/sb_game_rule_triggers.txt')
EVENTS = {key: statements(find_object(source('events/sb_zululand_settlement_events.txt'), key))
          for key in ('sb_zululand_settlement.115', 'sb_zululand_settlement.116')}


def field(nodes, name):
    return next(value for key, _, value in nodes if key == name)


def calculate(rt, name, scope):
    """The few arithmetic operators and scope changes used by these UI values."""
    result = 0
    def walk(nodes, ctx, prev=None):
        nonlocal result
        matched = False
        for key, _, value in nodes:
            if key in ('if', 'else_if', 'else'):
                if key == 'if': matched = False
                if not matched and (key == 'else' or rt.condition(field(value, 'limit'), ctx, prev)):
                    matched = True
                    walk([n for n in value if n[0] != 'limit'], ctx, prev)
            elif key in ('value', 'add', 'subtract', 'multiply', 'min', 'max'):
                amount = calculate(rt, value, ctx) if value in VALUES else rt.ref(value, ctx, prev)
                if key == 'value': result = amount
                elif key == 'add': result += amount
                elif key == 'subtract': result -= amount
                elif key == 'multiply': result *= amount
                elif key == 'min': result = max(result, amount)
                else: result = min(result, amount)
            elif key == 'every_political_movement':
                for movement in ctx.get('movements', []):
                    if rt.condition(field(value, 'limit'), movement, ctx):
                        walk([n for n in value if n[0] != 'limit'], movement, ctx)
            else:
                target = rt.ref(key, ctx, prev)
                if target is not None: walk(value, target, ctx)
    walk(VALUES[name], scope)
    return result


class ReconciliationContest(Contest):
    mode = 'sb_frontier_ai_behavior_dynamic_historical'

    def condition(self, nodes, ctx, prev=None):
        results = []
        for key, op, value in nodes:
            if key in RULES:
                result = self.condition(RULES[key], ctx, prev) == (value == 'yes')
            elif key == 'has_game_rule': result = self.mode == value
            elif key == 'radical_fraction':
                culture = field(value, 'culture')
                threshold = float(field(value, 'value'))
                result = ctx.get('radical_fractions', {}).get(culture, 0) >= threshold
            elif key == 'is_character_alive': result = ctx.get('alive', False) == (value == 'yes')
            elif key in ('is_in_exile_pool', 'is_in_void'): result = ctx.get(key, False) == (value == 'yes')
            else: result = super().condition([(key, op, value)], ctx, prev)
            results.append(result)
        return all(results)


class ChiefdomsPlaytest(unittest.TestCase):
    def test_natal_returns_refugees_before_the_claimant_reward_relieves_unrest(self):
        class NatalReview(ReconciliationContest):
            def ref(self,key,ctx,prev=None):
                if key in VALUES: return calculate(self,key,ctx)
                if key == 's:STATE_NATAL.region_state:NAL': return self.natal_state
                return super().ref(key,ctx,prev)

            def effect(self,nodes,ctx,prev=None):
                for node in nodes:
                    if node[0] == 'add_loyalists':
                        ctx['radical_fractions']['cu:zulu'] = .1367
                    else: super().effect([node],ctx,prev)

        # The separate court handoff tests execute the character transfer. Start this
        # receipt with the claimant physically home, as in the February checkpoint.
        rt = NatalReview()
        rt.nal.update(is_ai=True, sb_natal_has_shepstone_system=True, radical_fractions={'cu:zulu':.2667})
        rt.claimant.update(owner=rt.zul,alive=True)
        rt.claimant['vars']['sb_zululand_claimant_returned_var'] = 1
        peasants = entity('households',culture='cu:zulu',pop_type='peasants',total_size=1000)
        artisans = entity('artisans',culture='cu:zulu',pop_type='machinists',total_size=100)
        rt.natal_state = entity('Natal',pops=[peasants,artisans])
        zululand = entity('Zululand',state_region='s:STATE_ZULULAND')
        rt.zul['states'] = [zululand]
        settlement = E['sb_zululand_return_exiled_claimant']
        body = next(node for node in field(settlement,'if') if node[0]=='if'
                    and ('set_variable','=','sb_zululand_claimant_returned_var') in node[2])
        native = ('change_relations','add_fervor','sb_natal_make_fully_accepted_pops_loyalist_5',
                  'sb_natal_sync_repealed_shepstone_zulu_movement_attraction','sb_zululand_refugee_recruitment')
        with patch.dict(E,{key:[] for key in native}):
            rt.effect([body],rt.nal)
            rt.run('sb_zululand_review_ai_refugee_return',rt.nal)
        self.assertIn('sb_zululand_refugees_unloaded_var',rt.nal['vars'])
        self.assertEqual((800,100,200),(peasants['total_size'],artisans['total_size'],zululand['arrivals']))
        self.assertLess(rt.nal['radical_fractions']['cu:zulu'],.2)

    def test_reconciliation_ai_waits_for_unrest_or_historical_delay(self):
        rt = ReconciliationContest(); movement = rt.royal(1)
        rt.nal['radical_fractions'] = {'cu:zulu': .1999}
        self.assertEqual(0, calculate(rt, 'sb_zululand_reconciliation_ai_chance', rt.nal))
        rt.nal['radical_fractions']['cu:zulu'] = .2
        self.assertEqual(25, calculate(rt, 'sb_zululand_reconciliation_ai_chance', rt.nal))
        rt.active = False
        self.assertEqual(0, calculate(rt, 'sb_zululand_reconciliation_ai_chance', rt.nal))
        rt.active = True
        rt.mode = 'sb_frontier_ai_behavior_strict_historical'
        rt.journal['journal_entry_age'] = 1094
        self.assertEqual(0, calculate(rt, 'sb_zululand_reconciliation_ai_chance', rt.nal))
        movement['political_movement_radicalism'] = 0
        rt.journal['journal_entry_age'] = 1095
        rt.nal['radical_fractions']['cu:zulu'] = 0
        self.assertEqual(25, calculate(rt, 'sb_zululand_reconciliation_ai_chance', rt.nal))
        rt.mode = 'sb_frontier_ai_behavior_off'
        movement['political_movement_radicalism'] = 1
        self.assertEqual(0, calculate(rt, 'sb_zululand_reconciliation_ai_chance', rt.nal))

    def test_activism_uses_zulu_movement_from_every_viewer(self):
        rt = Contest(); rt.royal(.81)
        rt.trn['movements'] = [entity('sponsor movement', movement_type='movement_sb_zulu_royal', political_movement_radicalism=.12)]
        for viewer in (rt.trn, rt.nal, rt.britain, rt.zul):
            self.assertEqual(.81, calculate(rt, 'sb_usuthu_activism', viewer))

    def test_original_deadline_survives_frozen_legacy_markers_and_foreign_views(self):
        rt = Contest()
        rt.container['vars'].update(sb_chiefs_review_wait_var=('timed', 3650),
                                    sb_chiefs_weekly_tick_var=('timed', 6))
        start = datetime.date(1879, 12, 30)
        for age in (0, 31, 120, 3649, 3650, 3700):
            rt.journal['journal_entry_age'] = age
            for viewer in (rt.nal, rt.zul, rt.trn, rt.britain):
                remaining = calculate(rt, 'sb_chiefs_review_days_left', viewer)
                self.assertEqual(max(3650-age, 0), remaining)
                if age <= 3650:
                    self.assertEqual(start+datetime.timedelta(days=3650),
                                     start+datetime.timedelta(days=age+remaining))
                self.assertEqual(age >= 3650, rt.condition(T['sb_chiefs_review_due'], viewer))
        rt.journal['journal_entry_age'] = 3650
        rt.tick()
        self.assertEqual([('ZUL', 2)], rt.results)

    def test_weekly_deduplication_does_not_depend_on_expiring_container_variables(self):
        rt = Contest(); movement = rt.royal(.5)
        rt.container['vars']['sb_chiefs_weekly_tick_var'] = ('timed', 6)
        rt.scopes['journal_entry'] = rt.journal
        rt.run('sb_chiefs_weekly_update', rt.britain)
        self.assertEqual(0, rt.journal['vars']['sb_chiefs_last_weekly_age_var'])
        movement['political_movement_radicalism'] = 1
        rt.run('sb_chiefs_weekly_update', rt.trn)
        self.assertEqual([], rt.results)
        rt.journal['journal_entry_age'] = 7
        rt.run('sb_chiefs_weekly_update', rt.nal)
        self.assertEqual([('ZUL', 1)], rt.results)
        rt.run('sb_chiefs_weekly_update', rt.zul)
        self.assertEqual(1, len(rt.results))

    def test_shared_overlord_gate_uses_current_realm_and_indirect_subjects(self):
        for patron in ('GBR', 'FRA'):
            for indirect in (False, True):
                rt = Contest(); overlord = entity(patron, alive=True)
                rt.nal['overlord'] = overlord
                self.assertTrue(rt.condition(T['sb_zululand_chiefdoms_involved_actor'], rt.trn))
                rt.trn['overlord'] = entity('middle', overlord=overlord) if indirect else overlord
                for rule in ('sb_zululand_chiefdoms_involved_actor',
                             'sb_zululand_trn_is_eligible_participant',
                             'sb_zululand_contest_interventions_available',
                             'sb_nrp_chiefdoms_promise_available'):
                    self.assertFalse(rt.condition(T[rule], rt.trn), rule)
                self.assertTrue(rt.condition(T['sb_zululand_chiefdoms_involved_actor'], rt.nal))
                self.assertTrue(rt.condition(T['sb_zululand_contest_interventions_available'], rt.nal))
        for natal_subject in (False, True):
            rt = Contest()
            rt.trn['overlord'] = rt.britain
            if natal_subject: rt.nal['overlord'] = entity('FRA', alive=True)
            self.assertTrue(rt.condition(T['sb_zululand_trn_is_eligible_participant'], rt.trn))
        rt.nal['alive'] = False
        self.assertFalse(rt.condition(T['sb_chiefs_boer_shares_natal_overlord'], rt.trn))

    def test_withdrawal_stops_only_boer_costs_and_forfeits_even_full_commitment(self):
        rt = Contest(); rt.nal['overlord'] = rt.britain; rt.trn['overlord'] = rt.britain
        rt.scopes['root'] = entity('foreign')
        rt.globals['sb_nrp_chiefdoms_promise_var'] = 1
        rt.container['vars'].update(sb_zululand_boer_commitment_var=100, sb_zululand_boer_committed_var=1)
        rt.trn['vars'].update(sb_zululand_usuthu_sponsorship_active_var=1,
                              sb_zululand_boer_volunteers_active_var=1,
                              sb_zululand_bribe_open_var=1, sb_zululand_bribe_cost_var=100000)
        rt.trn['modifiers'] = {'sb_zululand_usuthu_sponsorship_cost', 'unrelated'}
        rt.trn['states'][0]['modifiers'] = {'sb_zululand_boer_volunteer_mortality'}
        rt.nal['modifiers'] = {'sb_zululand_policing_cost', 'sb_zululand_chiefly_patronage_cost'}
        for country in (rt.zul, entity('rebels', alive=True)):
            country['movements'] = [entity('usuthu', movement_type='movement_sb_zulu_royal',
                modifiers={'sb_usuthu_sponsorship', 'sb_usuthu_volunteers', 'other'})]
        rebels = country; rt.container['vars']['sb_chiefs_rebels_scope'] = rebels
        rt.run('sb_zululand_enforce_boer_withdrawal', rt.scopes['root'])
        self.assertEqual(0, rt.container['vars']['sb_zululand_boer_commitment_var'])
        self.assertNotIn('sb_zululand_boer_committed_var', rt.container['vars'])
        self.assertNotIn('sb_nrp_chiefdoms_promise_var', rt.globals)
        self.assertEqual({'sb_zululand_bribe_open_var': 1, 'sb_zululand_bribe_cost_var': 100000}, rt.trn['vars'])
        self.assertEqual({'unrelated'}, rt.trn['modifiers'])
        self.assertEqual(set(), rt.trn['states'][0]['modifiers'])
        for country in (rt.zul, rebels): self.assertEqual({'other'}, country['movements'][0]['modifiers'])
        self.assertEqual(2, len(rt.nal['modifiers']))
        self.assertEqual({}, rt.scopes['root']['vars'])
        rt.trn.pop('overlord')
        rt.run('sb_zululand_enforce_boer_withdrawal', rt.nal)
        self.assertFalse(rt.condition(T['sb_zululand_trn_is_eligible_participant'], rt.trn))
        self.assertFalse(rt.condition(T['sb_nrp_chiefdoms_promise_available'], rt.nal))
        option = field(EVENTS['sb_zululand_settlement.116'], 'option')
        rt.effect(field(option, 'hidden_effect'), rt.trn)
        self.assertEqual({}, rt.trn['vars'])

    def test_held_bribe_cannot_charge_after_becoming_subject_before_cleanup(self):
        rt = Contest(); rt.nal['overlord'] = rt.britain; rt.trn['overlord'] = rt.britain
        rt.trn['gold_reserves'] = 2000
        rt.trn['vars'].update(sb_zululand_bribe_open_var=1, sb_zululand_bribe_cost_var=100000,
                              sb_zululand_bribe_target_scope=entity('chief'))
        option = field(EVENTS['sb_zululand_settlement.116'], 'option')
        rt.effect(field(option, 'hidden_effect'), rt.trn)
        self.assertEqual(2000, rt.trn['gold_reserves'])
        self.assertEqual({}, rt.trn['vars'])
        rt.run('sb_zululand_accept_boer_appeal', rt.trn)  # No soldier move or commitment.
        rt.run('sb_nrp_create_greater_republic', rt.nal)  # No country creation/land transfer.
        self.assertNotIn('sb_nrp_setup_pending_var', rt.nal['vars'])

    def test_pending_creation_revalidates_and_clears_its_lease_without_transferring_land(self):
        class Pending(Contest):
            def ref(self, key, ctx, prev=None):
                if key == 'c:NRP': return self.nrp
                return super().ref(key, ctx, prev)
        rt = Pending(); rt.nrp = entity('NRP', alive=True)
        rt.nal['overlord'] = rt.britain; rt.trn['overlord'] = rt.britain
        rt.nal['vars']['sb_nrp_setup_pending_var'] = 1
        rt.run('sb_nrp_finalize_greater_republic', rt.nal)
        self.assertNotIn('sb_nrp_setup_pending_var', rt.nal['vars'])
        self.assertNotIn('sb_nrp_reward_consumed_var', rt.globals)
        self.assertEqual({}, rt.nrp['vars'])

    def test_appeal_default_remains_available_after_withdrawal(self):
        rt = Contest(); rt.nal['overlord'] = rt.britain; rt.trn['overlord'] = rt.britain
        defaults = [body for key, _, body in EVENTS['sb_zululand_settlement.115']
                    if key == 'option' and ('default_option', '=', 'yes') in body]
        self.assertEqual(1, len(defaults))
        option = defaults[0]
        self.assertEqual('sb_zululand_settlement.115.a', field(option, 'name'))
        self.assertEqual(1, sum(key == 'option' for key, _, _ in EVENTS['sb_zululand_settlement.115']))
        self.assertFalse(any(key == 'trigger' for key, _, _ in option))
        self.assertFalse(rt.condition(T['sb_zululand_trn_is_eligible_participant'], rt.trn))

    def test_movement_totals_follow_the_faction_not_the_observer(self):
        rt = Contest(); rt.zul['vars'].update(sb_court_royal_political_weight_var=209, sb_court_chiefly_political_weight_var=100,
                                             sb_court_royal_weight_var=159, sb_court_chiefly_weight_var=50)
        rt.trn['vars'].update(sb_court_royal_political_weight_var=999, sb_court_chiefly_political_weight_var=999)
        for viewer in (rt.trn, rt.nal, rt.britain, rt.zul):
            self.assertEqual(209, calculate(rt, 'sb_chiefs_royal_prominence', viewer))
            self.assertEqual(100, calculate(rt, 'sb_chiefs_chiefly_prominence', viewer))
        rebel = entity('rebels', alive=True)
        rebel['vars'].update(sb_court_war_alignment_var=1, sb_court_royal_political_weight_var=150,
                             sb_court_chiefly_political_weight_var=10)
        rt.container['vars']['sb_chiefs_rebels_scope'] = rebel
        self.assertEqual(150, calculate(rt, 'sb_chiefs_royal_prominence', rt.trn))
        self.assertEqual(100, calculate(rt, 'sb_chiefs_chiefly_prominence', rt.trn))
        rebel['alive'] = False
        self.assertEqual(209, calculate(rt, 'sb_chiefs_royal_prominence', rt.trn))
        rt.zul['vars'].pop('sb_court_royal_political_weight_var')
        self.assertEqual(0, calculate(rt, 'sb_chiefs_royal_prominence', rt.trn))

    def test_only_partition_relationship_gets_half_tribute(self):
        actions = defs('common/diplomatic_actions/sb_subject_relationships.txt')
        pact = field(actions['sb_zulu_chiefdoms'], 'pact')
        self.assertEqual('0.15', field(pact, 'income_transfer'))
        self.assertEqual('yes', field(pact, 'income_transfer_based_on_second_country'))
        self.assertIn('change_subject_type = subject_type_puppet',
                      find_object(source('common/scripted_effects/sb_zululand_settlement_effects.txt'),
                                  'sb_zululand_finalize_political_contest'))

if __name__ == '__main__': unittest.main()
