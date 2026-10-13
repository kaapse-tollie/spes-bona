"""Port seizure must reach a valid British play without claiming its own land."""
import unittest

from tests.test_natal_zululand_gameplay_contract import (
    named_option,
    nested_blocks,
    object_block,
    object_block_from_source,
)


class PortNatalResponseTests(unittest.TestCase):
    def launch_option(self):
        return named_option(
            object_block('events/sb_natal_crisis_events.txt', 'sb_natal_crisis.114'),
            'sb_natal_crisis.114.a',
        )

    def test_seizure_and_cape_ownership_are_alternative_routes(self):
        outer = nested_blocks(self.launch_option(), 'if')[0]
        eligibility = object_block_from_source(outer, 'limit')
        alternatives = object_block_from_source(eligibility, 'OR')
        seized = object_block_from_source(alternatives, 'AND')
        self.assertIn('has_variable = sb_natalia_port_natal_raid_taken_var', seized)
        self.assertIn('p:x279045.state.owner = scope:natalia', seized)
        self.assertNotIn('c:CAP', seized)
        self.assertIn('is_subject_of = root', alternatives)
        self.assertIn('p:x279045.state.owner = this', alternatives)
        # Wars/plays are temporary blockers, not grounds for terminal cleanup.
        self.assertNotIn('is_at_war', eligibility)
        self.assertNotIn('is_active_in_diplomatic_play', eligibility)

    def test_seized_port_uses_native_demand_selection_but_refusal_returns_natal(self):
        plays = nested_blocks(self.launch_option(), 'create_diplomatic_play')
        self.assertEqual(2, len(plays))
        for play in plays:
            self.assertIn('type = dp_make_protectorate', play)
            self.assertIn('target_country = scope:natalia', play)
        self.assertNotIn('add_war_goal', plays[0])
        self.assertIn('type = return_state', plays[1])
        self.assertIn('holder = scope:natalia', plays[1])
        self.assertIn('target_country = c:CAP', plays[1])
        self.assertIn('target_state = s:STATE_NATAL.region_state:CAP', plays[1])
        branch = next(b for b in nested_blocks(self.launch_option(), 'if')
                      if object_block_from_source(b, 'limit').strip() ==
                      'limit = { p:x279045.state.owner = scope:natalia }')
        self.assertIn(plays[0], branch)
        self.assertNotIn(plays[1], branch)

    def test_blocked_or_failed_launch_retries_without_duplicating_a_live_play(self):
        option = self.launch_option()
        retries = [b for b in nested_blocks(option, 'if')
                   if 'id = sb_natal_crisis.114 days = 30' in b]
        self.assertTrue(retries, 'British response must retry temporary launch blockers')
        retry = retries[-1]
        self.assertIn('NOT = { exists = scope:natalia_british_play }', retry)
        self.assertIn('NOT = { has_war_with = scope:natalia }', retry)
        self.assertNotIn('remove_variable', retry)
        lookup = object_block_from_source(option, 'random_diplomatic_play')
        for condition in ('is_diplomatic_play_type = dp_make_protectorate',
                          'initiator = root', 'target = scope:natalia'):
            self.assertIn(condition, lookup)
        self.assertIn('save_temporary_scope_as = natalia_british_play', lookup)
        self.assertLess(option.index(lookup), option.index(retry))
        readiness = next(object_block_from_source(b, 'limit')
                         for b in nested_blocks(option, 'if')
                         if 'aggressive_diplomatic_plays_permitted' in object_block_from_source(b, 'limit'))
        for condition in ('is_at_war = no', 'is_active_in_diplomatic_play = no',
                          'NOT = { has_truce_with = scope:natalia }',
                          'has_variable = sb_natalia_ultimatum_truce_var'):
            self.assertIn(condition, readiness)

    def test_britains_unrelated_war_does_not_block_the_natal_response(self):
        option = self.launch_option()
        readiness = next(object_block_from_source(b, 'limit')
                         for b in nested_blocks(option, 'if')
                         if 'aggressive_diplomatic_plays_permitted' in object_block_from_source(b, 'limit'))
        britain_checks = readiness
        for natal_check in nested_blocks(readiness, 'scope:natalia'):
            britain_checks = britain_checks.replace(natal_check, '')
        # GBR may be fighting Russia while NAL is free to receive this play.
        # Keep NAL's existing readiness checks, but do not require global peace
        # or absence from every active play (which includes ongoing wars) for GBR.
        self.assertNotIn('is_at_war = no', britain_checks)
        self.assertNotIn('is_active_in_diplomatic_play = no', britain_checks)
        self.assertIn('NOT = { has_war_with = scope:natalia }', britain_checks)
        duplicate = object_block_from_source(britain_checks, 'any_diplomatic_play')
        self.assertIn('initiator = root', duplicate)
        self.assertIn('target = scope:natalia', duplicate)
        self.assertIn('scope:natalia = { is_at_war = no is_active_in_diplomatic_play = no }', readiness)

    def test_zulu_seizure_requires_a_british_port_and_response_does_not(self):
        decision = object_block('common/decisions/sb_zulu_decisions.txt', 'zulu_raid_port_natal')
        possible = object_block_from_source(decision, 'possible')
        self.assertIn('is_subject = no', possible)
        self.assertIn('is_active_in_diplomatic_play = no', possible)
        self.assertIn('p:x279045.state.owner = c:CAP', possible)
        self.assertIn('p:x279045.state.owner = c:GBR', possible)
        response = object_block('events/sb_natal_crisis_events.txt', 'sb_natal_crisis.085')
        self.assertNotIn('p:x279045.state.owner', response)
        self.assertIn('create_diplomatic_play = { type = dp_annex_war target_country = c:ZUL }', response)
        self.assertIn('id = sb_natal_crisis.085 days = 30', response)


if __name__ == '__main__':
    unittest.main()
