"""Held-popup reservation and the original, single-option Klip follow-ups."""
import unittest

from tests.test_natal_zululand_gameplay_contract import (
    object_block, object_block_from_source, nested_blocks,
)
from tests.test_klip_river_colonial_delivery import expression

EFFECTS = 'common/scripted_effects/sb_klip_river_county_effects.txt'
EVENTS = 'events/sb_klip_river_county_events.txt'


def marker_condition(nodes, flags, day, ready=True):
    def check(key, value):
        if key == 'NOT':
            return not marker_condition(value, flags, day, ready)
        if key == 'has_variable':
            return value in flags and (flags[value] is None or flags[value] > day)
        if key.endswith('_preflight'):
            return ready
        raise AssertionError((key, value))
    return all(check(k, v) for k, v in nodes)


def run_marker_effects(nodes, flags, day):
    for key, value in nodes:
        if key == 'if':
            limit = next(v for k, v in value if k == 'limit')
            if marker_condition(limit, flags, day):
                run_marker_effects([(k, v) for k, v in value if k != 'limit'], flags, day)
        elif key == 'remove_variable':
            flags.pop(value, None)
        elif key == 'set_variable':
            if isinstance(value, str):
                flags[value] = None
            else:
                fields = dict(value)
                flags[fields['name']] = day + int(fields['days'])
        elif key.startswith('c:'):
            # Country scopes only rebuild localization in these immediate blocks.
            continue
        else:
            raise AssertionError((key, value))


class KlipRiverOptionTooltipTests(unittest.TestCase):
    def test_each_followup_has_one_original_option_with_its_tooltip(self):
        for route, number in (('secession', '050'), ('punitive', '060')):
            with self.subTest(route=route):
                event = object_block(EVENTS, 'sb_klip_river_county.' + number)
                options = nested_blocks(event, 'option')
                self.assertEqual(1, len(options))
                option = options[0]
                self.assertIn(f'name = sb_klip_river_county.{number}.a', option)
                self.assertIn(f'custom_tooltip = sb_klip_river_county_{number}_tt', option)
                self.assertNotIn('trigger =', option)
                effect = object_block_from_source(option, 'hidden_effect')
                self.assertIn(f'limit = {{ sb_klip_river_{route}_bound_delivery_receipt = yes }}', effect)
                self.assertIn(f'sb_klip_river_{route}_delivery_currently_permanently_invalid = yes', effect)
                self.assertIn(f'sb_klip_river_start_{route}_play = yes', effect)
                self.assertIn(f'remove_variable = sb_klip_river_{route}_delivery_queued_var', effect)

    def test_open_popup_remains_reserved_across_all_three_months(self):
        for route, number in (('secession', '050'), ('punitive', '060')):
            with self.subTest(route=route):
                queue = object_block(EFFECTS, f'sb_klip_river_queue_{route}_delivery')
                dispatch = [b for b in nested_blocks(queue, 'if')
                            if f'NOT = {{ has_variable = sb_klip_river_{route}_delivery_queued_var }}'
                            in object_block_from_source(b, 'limit')][0]
                gate = expression(object_block_from_source(dispatch, 'limit'))
                marker = f'sb_klip_river_{route}_delivery_queued_var'
                flags = {}
                self.assertTrue(marker_condition(gate, flags, 0))
                # Read the actual dispatch timeout, then the event's immediate effects.
                write = object_block_from_source(dispatch, 'set_variable')
                run_marker_effects([('set_variable', expression(write))], flags, 0)
                event = object_block(EVENTS, 'sb_klip_river_county.' + number)
                run_marker_effects(expression(object_block_from_source(event, 'immediate')), flags, 1)
                for monthly_day in (21, 51, 81):
                    self.assertFalse(marker_condition(gate, flags, monthly_day))
                self.assertIsNone(flags[marker])  # Open reservation has no timeout.
                # Answering releases the marker. Busy conditions still prevent reissue.
                flags.pop(marker)
                self.assertFalse(marker_condition(gate, flags, 82, ready=False))
                self.assertTrue(marker_condition(gate, flags, 83, ready=True))

    def test_failed_dispatch_can_retry_after_its_short_timeout(self):
        route = 'punitive'
        queue = object_block(EFFECTS, f'sb_klip_river_queue_{route}_delivery')
        dispatch = [b for b in nested_blocks(queue, 'if')
                    if 'delivery_queued_var' in object_block_from_source(b, 'limit')][0]
        gate = expression(object_block_from_source(dispatch, 'limit'))
        flags = {}
        run_marker_effects([('set_variable', expression(object_block_from_source(dispatch, 'set_variable')))], flags, 0)
        self.assertFalse(marker_condition(gate, flags, 1))
        # No immediate ran: delivery was lost. The next monthly pulse may retry.
        self.assertTrue(marker_condition(gate, flags, 21))

    def test_both_delivery_paths_supply_the_zulu_localization_scope(self):
        queue = object_block(EFFECTS, 'sb_klip_river_queue_punitive_delivery')
        event = object_block(EVENTS, 'sb_klip_river_county.060')
        immediate = object_block_from_source(event, 'immediate')
        for source in (queue, immediate):
            self.assertIn('c:ZUL ?= { save_scope_as = sb_klip_zulu_scope }', source)
            self.assertNotIn('container:', source)


if __name__ == '__main__':
    unittest.main()
