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



class UsuthuMovementContestTests(unittest.TestCase):







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
        prepare=object_block('common/scripted_effects/sb_court_politics_effects.txt','sb_court_prepare_partition')
        self.assertIn('sb_court_ensure_roster = yes',prepare)
        self.assertLess(exile.index('sb_court_prepare_partition'),exile.index('exile_character_with_role_cleanup'))
        self.assertLess(exile.index('save_scope_as = sb_zululand_exile_heir'),exile.index('exile_character_with_role_cleanup'))
        self.assertLess(exile.index('activate_law = law_type:law_sb_chiefly_council'),exile.index('sb_court_select_chiefly_head'))
        admission = next(branch for key, _, body in parse(exile) if key == 'c:ZUL'
                         for child, _, branch in body if child == 'if'
                         and any(field == 'create_character' for field, _, _ in branch))
        gate = next(body for key, _, body in admission if key == 'limit')
        self.assertIn(('game_date', '>=', '1877.1.1'), gate)
        self.assertIn(('game_date', '<=', '1897.1.1'), gate)
        self.assertIn(('NOT', '=', [('is_template_used', '=', 'ZUL_zibhebhu_kamaphitha')]), gate)
        self.assertIn(('NOT', '=', [('has_global_variable', '=', 'sb_zululand_zibhebhu_seen_var')]), gate)
        self.assertNotIn('ig_petty_bourgeoisie', exile)

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
        self.assertNotIn('gold_reserves >=',event)
        self.assertGreaterEqual(event.count('has_variable = sb_zululand_bribe_open_var'),3)
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
