"""Authored-movement handoffs replace the retired native-Absolutist mutation tests.

This executes the small intervention vocabulary with a foreign event ROOT. Core
seed-once behavior and the definition/CMF exclusion are tested separately.
"""
from copy import deepcopy
from pathlib import Path
import unittest

from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import find_object

ROOT = Path(__file__).resolve().parents[1]
EFFECTS = ROOT / 'common/scripted_effects/sb_usuthu_politics_effects.txt'


def block(name):
    return statements(find_object(EFFECTS.read_text(encoding='utf-8-sig'), name))


class InterventionRuntime:
    def __init__(self):
        self.countries = {
            tag: {'tag': tag, 'flags': set(), 'modifiers': set(), 'movements': []}
            for tag in ('NAL', 'ZUL', 'GBR', 'REV')
        }
        for tag in ('ZUL', 'REV'):
            self.countries[tag]['movements'] = [
                {'type': movement, 'modifiers': set(), 'support': .23, 'activism': .64}
                for movement in ('movement_sb_zulu_chiefly', 'movement_sb_zulu_royal', 'movement_modernizer')
            ]
        self.globals = {}
        self.reconciled = []
        self.event_root = 'GBR'

    def check(self, nodes, scope):
        for key, op, value in nodes:
            if key == 'has_variable': valid = value in scope['flags']
            elif key == 'has_modifier': valid = value in scope['modifiers']
            elif key == 'is_political_movement_type': valid = value == scope['type']
            else: raise AssertionError(key)
            if not valid: return False
        return True

    def execute(self, nodes, scope):
        for key, op, value in nodes:
            if key == 'set_global_variable':
                data = {k: v for k, _, v in value}
                self.globals[data['name']] = data['value'].removeprefix('c:')
            elif key.startswith('c:'):
                self.execute(value, self.countries[key[2:]])
            elif key.startswith('global_var:'):
                tag = self.globals.get(key.split(':', 1)[1])
                if tag: self.execute(value, self.countries[tag])
            elif key == 'sb_institutions_reconcile':
                self.reconciled.append(scope['tag'])
            elif key == 'set_variable': scope['flags'].add(value)
            elif key == 'remove_variable': scope['flags'].remove(value)
            elif key == 'add_modifier':
                scope['modifiers'].add(next(v for k, _, v in value if k == 'name'))
            elif key == 'remove_modifier': scope['modifiers'].remove(value)
            elif key == 'if':
                limit = next(v for k, _, v in value if k == 'limit')
                if self.check(limit, scope): self.execute([n for n in value if n[0] != 'limit'], scope)
            elif key == 'every_political_movement':
                limit = next(v for k, _, v in value if k == 'limit')
                for movement in scope['movements']:
                    if self.check(limit, movement): self.execute([n for n in value if n[0] != 'limit'], movement)
            else: raise AssertionError(key)

    def call(self, name, country='NAL'):
        self.execute(block(name), self.countries[country])


class AuthoredMovementHandoffTests(unittest.TestCase):
    def test_partition_handoff_reconciles_actual_zulu_scope_without_touching_existing_movements(self):
        runtime = InterventionRuntime()
        before = deepcopy(runtime.countries)
        runtime.call('sb_zululand_setup_usuthu_politics')
        runtime.call('sb_zululand_setup_usuthu_politics')
        self.assertEqual(['ZUL', 'ZUL'], runtime.reconciled)
        self.assertEqual('ZUL', runtime.globals['sb_zululand_live_zul_scope'])
        self.assertEqual(before, runtime.countries)
        self.assertEqual('GBR', runtime.event_root)

    def test_chief_patronage_uses_tracked_country_and_never_harms_royal_or_unrelated_movements(self):
        runtime = InterventionRuntime()
        runtime.globals['sb_zululand_live_zul_scope'] = 'REV'
        before = deepcopy(runtime.countries)
        runtime.call('sb_zululand_start_chief_patronage')
        self.assertEqual({'sb_zululand_chiefly_patronage'}, runtime.countries['REV']['movements'][0]['modifiers'])
        self.assertEqual(before['REV']['movements'][1:], runtime.countries['REV']['movements'][1:])
        self.assertEqual(before['ZUL'], runtime.countries['ZUL'])
        self.assertEqual(before['GBR'], runtime.countries['GBR'])
        runtime.call('sb_zululand_stop_chief_patronage')
        runtime.call('sb_zululand_stop_chief_patronage')
        self.assertEqual(before, runtime.countries)

    def test_retired_native_mutation_and_fixed_lobbies_are_absent(self):
        source = EFFECTS.read_text(encoding='utf-8-sig')
        for retired in ('set_core_ideology', 'sb_usuthu_royalist_networks', 'every_political_lobby', 'movement_royalist_absolutist'):
            self.assertNotIn(retired, source)
        for removed in ('common/customizable_localization/sb_usuthu_custom_loc.txt', 'localization/english/replace/sb_usuthu_movement_l_english.yml'):
            self.assertFalse((ROOT / removed).exists(), removed)


if __name__ == '__main__':
    unittest.main()
