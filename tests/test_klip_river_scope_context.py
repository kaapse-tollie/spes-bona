"""Exercise Klip actor references with a foreign event/callback ROOT.

This models reference identity only; engine creation and event delivery still
require fresh-game testing. It deliberately reads references from runtime script.
"""
import re
import unittest

from tests.test_natal_zululand_gameplay_contract import (
    object_block, object_block_from_source, nested_blocks, named_option,
)

EFFECTS = 'common/scripted_effects/sb_klip_river_county_effects.txt'
TRIGGERS = 'common/scripted_triggers/sb_klip_river_county_triggers.txt'


def resolve(reference, current, root, captures):
    if reference == 'root':
        return root
    if reference == 'this':
        return current
    if reference.startswith('c:'):
        return reference[2:]
    if reference.startswith('scope:'):
        return captures[reference[6:]]
    raise AssertionError(f'Unmodelled actor reference: {reference}')


def entry_captures(effect, current):
    # Only declarations at the helper's entry, before its first guarded branch.
    prefix = effect.split('\n\tif = {', 1)[0]
    return {name: current for name in re.findall(r'save_temporary_scope_as = (\w+)', prefix)}


class KlipRiverScopeContextTests(unittest.TestCase):
    def test_zulu_response_creates_from_natal_owned_provinces(self):
        option = named_option(object_block('events/sb_klip_river_county_events.txt',
                                          'sb_klip_river_county.020'),
                              'sb_klip_river_county.020.b')
        self.assertRegex(option, r'c:NAL\s*\?=\s*\{\s*sb_klip_river_create_county = yes')
        create = object_block(EFFECTS, 'sb_klip_river_create_county')
        gate = object_block_from_source(create, 'limit')
        refs = re.findall(r'p:(xDE0EDE|x552449)\.state.owner = (\S+)', gate)
        self.assertEqual(2, len(refs))
        for event_root in ('ZUL', 'NAL', 'diplomatic_play_123'):
            with self.subTest(root=event_root):
                owners = {p: resolve(ref, 'NAL', event_root, entry_captures(create, 'NAL'))
                          for p, ref in refs}
                self.assertEqual({'xDE0EDE': 'NAL', 'x552449': 'NAL'}, owners)
                self.assertNotEqual({'xDE0EDE': 'ZUL', 'x552449': 'ZUL'}, owners)

    def test_rollback_returns_land_to_exact_caller_even_after_retag(self):
        rollback = object_block(EFFECTS, 'sb_klip_river_rollback_created_county_attempt')
        refs = re.findall(r'country = (\S+) provinces = \{ (xDE0EDE|x552449) \}', rollback)
        self.assertEqual(2, len(refs))
        for current in ('NAL', 'former_NAL_now_SAF'):
            for event_root in ('ZUL', 'diplomatic_play_123'):
                with self.subTest(current=current, root=event_root):
                    for ref, province in refs:
                        self.assertEqual(current, resolve(ref, current, event_root,
                                                          entry_captures(rollback, current)))
        self.assertIn('country = scope:sb_klip_river_attempt_original_xbb_owner', rollback)

    def test_both_response_receipts_capture_the_natal_caller(self):
        for route in ('secession', 'punitive'):
            with self.subTest(route=route):
                queue = object_block(EFFECTS, f'sb_klip_river_queue_{route}_delivery')
                # The declaration belongs to the NAL queue, not a nested ZUL scope.
                self.assertIn(f'\n\t\t\tsave_scope_as = sb_klip_river_{route}_receipt_scope', queue)
                bound = object_block(TRIGGERS, f'sb_klip_river_{route}_bound_delivery_receipt')
                self.assertIn(f'this = scope:sb_klip_river_{route}_receipt_scope', bound)
                for event_root in ('NAL', 'ZUL', 'diplomatic_play_123'):
                    captures = {f'sb_klip_river_{route}_receipt_scope': 'NAL'}
                    self.assertEqual('NAL', resolve(f'scope:sb_klip_river_{route}_receipt_scope',
                                                   'NAL', event_root, captures))
                    left, right = re.search(r'(this) = (scope:\S+)', bound).groups()
                    for current in ('NAL', 'replacement_NAL'):
                        self.assertEqual(current == 'NAL',
                                         resolve(left, current, event_root, captures)
                                         == resolve(right, current, event_root, captures))
                self.assertNotIn('container', queue)

    def test_punitive_callback_checks_pending_state_on_its_actual_holder(self):
        queue = object_block(EFFECTS, 'sb_klip_river_queue_punitive_delivery')
        self.assertIn('country_definition = cd:NAL', object_block_from_source(queue, 'limit'))
        self.assertIn('set_variable = sb_klip_river_punitive_delivery_pending_var', queue)
        configure = object_block(EFFECTS, 'sb_klip_river_configure_started_play')
        punitive = nested_blocks(configure, 'else_if')[0]
        gate = object_block_from_source(punitive, 'limit')
        actors = dict(re.findall(r'scope:(initiator|target)\s*\?=\s*\{([^{}]+)\}', gate))
        holders = {'initiator': 'NAL', 'target': 'ZUL'}
        readers = [holders[actor] for actor, checks in actors.items()
                   if 'has_variable = sb_klip_river_punitive_delivery_pending_var' in checks]
        self.assertEqual(['NAL'], readers)
        self.assertIn('value = root', punitive)  # The callback must still bind the actual play.

    def test_preflight_and_invalidation_do_not_depend_on_callers_root(self):
        for name in ('sb_klip_river_county_setup_valid', 'sb_klip_river_secession_preflight',
                     'sb_klip_river_punitive_preflight',
                     'sb_klip_river_secession_delivery_currently_permanently_invalid',
                     'sb_klip_river_punitive_delivery_currently_permanently_invalid'):
            with self.subTest(trigger=name):
                trigger = object_block(TRIGGERS, name)
                self.assertNotRegex(trigger, r'\broot\b')
                self.assertRegex(trigger, r'p:x[0-9A-F]+\.state.owner = c:NAL')
        secession = object_block(TRIGGERS, 'sb_klip_river_secession_preflight')
        self.assertIn('initiator = c:ZUL target = c:NAL', secession)
        punitive = object_block(TRIGGERS, 'sb_klip_river_punitive_preflight')
        self.assertIn('initiator = c:NAL target = c:ZUL', punitive)

    def test_failed_initial_creation_gate_has_a_terminal_fallback(self):
        create = object_block(EFFECTS, 'sb_klip_river_create_county')
        fallbacks = nested_blocks(create, 'else_if')
        self.assertEqual(1, len(fallbacks))
        fallback = fallbacks[0]
        for guard in ('has_variable = sb_klip_river_county_pending_var',
                      'NOT = { exists = c:KLR }',
                      'NOT = { has_variable = sb_klip_river_county_creation_lease_var }'):
            self.assertIn(guard, fallback)
        self.assertIn('sb_klip_river_prepare_standard_boer_flight = yes', fallback)


if __name__ == '__main__':
    unittest.main()
