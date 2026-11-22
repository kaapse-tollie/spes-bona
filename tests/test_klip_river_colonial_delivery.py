"""Regression fixture: British-colony NAL, independent ZUL, no play yet.

Evaluate the actual preflight/invalidation expressions for this limited fixture.
This does not emulate play creation or tooltip execution in the engine.
"""
import re
import unittest

from tests.test_natal_zululand_gameplay_contract import object_block, nested_blocks

TRIGGERS = 'common/scripted_triggers/sb_klip_river_county_triggers.txt'
EFFECTS = 'common/scripted_effects/sb_klip_river_county_effects.txt'


def expression(source):
    tokens = iter(re.findall(r'\?=|>=|<=|!=|[=<>]|[{}]|[^\s{}=<>]+',
                            re.sub(r'#[^\n]*', '', source)))

    def body():
        result = []
        for key in tokens:
            if key == '}':
                return result
            operator = next(tokens)
            assert operator in ('=', '?=', '>', '<', '>=', '<=', '!=')
            if operator not in ('=', '?='):
                key += ' ' + operator
            value = next(tokens)
            result.append((key, body() if value == '{' else value))
        return result

    return body()[0][1]


def evaluate(nodes, country='NAL', busy=False):
    def check(key, value):
        if key == 'NOT':
            return not any(evaluate([node], country, busy) for node in value)
        if key == 'OR':
            return any(evaluate([node], country, busy) for node in value)
        if key.startswith('c:'):
            return evaluate(value, key[2:], busy)
        if key == 'any_diplomatic_play':
            return False
        if key == 'country_definition':
            return value == 'cd:' + country
        if key == 'exists':
            assert value in ('s:STATE_NATAL.region_state:NAL', 's:STATE_NATAL.region_state:ZUL')
            return True
        if key.endswith('.state.owner'):
            owner = 'NAL' if key == 'p:x279045.state.owner' else 'KLR'
            return owner == (country if value == 'this' else value[2:])
        if key == 'has_variable':
            assert value.endswith('_play_scope') or value == 'sb_klip_river_ora_appeal_pending_var'
            return False
        if key == 'has_war_with':
            return False
        facts = {
            'is_country_alive': True,
            'is_at_war': busy,
            'is_active_in_diplomatic_play': False,
            'is_subject': country == 'NAL',
            'aggressive_diplomatic_plays_permitted': country != 'NAL',
        }
        return facts[key] == (value == 'yes')

    return all(check(key, value) for key, value in nodes)


class KlipRiverColonialDeliveryTests(unittest.TestCase):
    def test_colonial_natal_can_reach_both_scripted_launches(self):
        for route in ('secession', 'punitive'):
            with self.subTest(route=route):
                preflight = expression(object_block(TRIGGERS, f'sb_klip_river_{route}_preflight'))
                invalid = expression(object_block(TRIGGERS, f'sb_klip_river_{route}_delivery_currently_permanently_invalid'))
                self.assertTrue(evaluate(preflight))
                self.assertFalse(evaluate(invalid))
                # A busy participant delays the launch; it is not a settlement.
                self.assertFalse(evaluate(preflight, busy=True))
                self.assertFalse(evaluate(invalid, busy=True))
                play = object_block('common/diplomatic_plays/sb_diplomatic_plays.txt',
                                    'dp_sb_klip_river_' + ('secession' if route == 'secession' else 'punitive_expedition'))
                self.assertIn('blocked_by_diplomatic_status = no', play)

    def test_prewar_cancellation_does_not_fabricate_a_war_result(self):
        cancel = object_block(EFFECTS, 'sb_klip_river_cancel_punitive_delivery')
        self.assertNotIn('finalize_punitive_', cancel)
        self.assertNotIn('record_punitive_final_evidence', cancel)
        self.assertNotIn('outcome_delivery', cancel)
        self.assertIn('sb_klip_river_clear_punitive_runtime = yes', cancel)

    def test_terminal_cleanup_stops_pending_launch_retries(self):
        for route in ('secession', 'punitive'):
            with self.subTest(route=route):
                cleanup = object_block(EFFECTS, f'sb_klip_river_clear_{route}_runtime')
                natal = '\n'.join(nested_blocks(cleanup, 'c:NAL ?'))
                self.assertIn(f'remove_variable = sb_klip_river_{route}_delivery_pending_var', natal)

    def test_refugee_quota_preview_waits_for_the_destination_count(self):
        effect = object_block('common/scripted_effects/sb_natalia_colony_effects.txt',
                              'sb_klip_river_distribute_boer_emigrants')
        count = 'scope:sb_natal_refugee_non_ora_count'
        guards = [b for b in nested_blocks(effect, 'if')
                  if ('exists', count) in dict(expression(b))['limit']]
        self.assertEqual(1, len(guards))
        guard = guards[0]
        self.assertIn('divide = ' + count, guard)
        self.assertNotIn(count, effect.replace(guard, ''))


if __name__ == '__main__':
    unittest.main()
