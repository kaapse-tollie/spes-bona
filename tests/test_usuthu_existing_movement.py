"""Execute the setup's movement subset; engine UI/pop calculations remain DP checks."""
from copy import deepcopy
from pathlib import Path
import unittest

from tests.test_usuthu_movement_contest import parse
from tests.test_zululand_postwar_settlement import object_block, text

EFFECTS = 'common/scripted_effects/sb_usuthu_politics_effects.txt'
NATIVE = 'movement_royalist_absolutist'


def configure(countries):
    setup = parse(object_block(EFFECTS, 'sb_zululand_setup_usuthu_politics'))
    zul = next(value for key, _, value in setup if key == 'c:ZUL')
    # Lobby effects follow the movement transition and are independently tested.
    prefix = zul[:next(i for i, node in enumerate(zul) if node[0] == 'every_political_lobby')]
    helper = parse(object_block(EFFECTS, 'sb_zululand_configure_usuthu_movement'))

    def check(nodes, scope):
        results = []
        for key, _, value in nodes:
            if key == 'NOT': result = not check(value, scope)
            elif key == 'owner': result = check(value, countries[scope['owner']])
            elif key == 'country_definition': result = value == 'cd:' + scope['tag']
            elif key == 'has_variable': result = value in scope['flags']
            elif key == 'has_modifier': result = value in scope['modifiers']
            elif key == 'is_political_movement_type': result = value == scope['type']
            elif key == 'any_political_movement': result = any(check(value, m) for m in scope['movements'])
            else: raise AssertionError(key)
            results.append(result)
        return all(results)

    def execute(nodes, scope):
        for key, _, value in nodes:
            if key == 'if':
                limit = next(v for k, _, v in value if k == 'limit')
                if check(limit, scope): execute([n for n in value if n[0] != 'limit'], scope)
            elif key == 'every_political_movement':
                limit = next(v for k, _, v in value if k == 'limit')
                for movement in scope['movements']:
                    if check(limit, movement): execute([n for n in value if n[0] != 'limit'], movement)
            elif key == 'create_political_movement':
                movement = dict(type=next(v for k, _, v in value if k == 'type'), owner=scope['tag'], modifiers={}, support=0, activism=0)
                scope['movements'].append(movement)
                execute(helper, movement)  # Scoped addition to native on_created.
            elif key == 'sb_zululand_configure_usuthu_movement': execute(helper, scope)
            elif key == 'set_core_ideology': scope['ideology'] = value
            elif key == 'add_modifier':
                name = next(v for k, _, v in value if k == 'name')
                scope['modifiers'][name] = scope['modifiers'].get(name, 0) + 1
            else: raise AssertionError(key)

    execute(prefix, countries['ZUL'])  # Explicit c:ZUL, irrespective of event root.


class ExistingMovementTests(unittest.TestCase):
    def test_existing_identity_support_activism_and_other_countries_survive(self):
        flags = {'sb_zululand_usuthu_context_var', 'sb_zululand_usuthu_contest_var'}
        movement = dict(type=NATIVE, owner='ZUL', id=42, support=0.13, activism=0.64, modifiers={'existing_modifier': 1})
        other = dict(type='movement_modernizer', owner='ZUL', id=43, support=0.16, activism=0.65, modifiers={})
        countries = {'ZUL': dict(tag='ZUL', flags=flags, movements=[movement, other]), 'NAL': dict(tag='NAL', flags=set(), movements=[deepcopy(movement)])}
        untouched = deepcopy((other, countries['NAL']))
        configure(countries)
        configure(countries)
        self.assertEqual(2, len(countries['ZUL']['movements']))
        self.assertIs(movement, countries['ZUL']['movements'][0])
        self.assertEqual((42, 0.13, 0.64), (movement['id'], movement['support'], movement['activism']))
        self.assertEqual('ideology_sb_usuthu', movement['ideology'])
        self.assertEqual({'existing_modifier': 1, 'sb_usuthu_royalist_networks': 1}, movement['modifiers'])
        self.assertEqual(untouched, (other, countries['NAL']))

    def test_missing_movement_is_created_once(self):
        countries = {'ZUL': dict(tag='ZUL', flags={'sb_zululand_usuthu_context_var', 'sb_zululand_usuthu_contest_var'}, movements=[])}
        configure(countries)
        configure(countries)
        movements = countries['ZUL']['movements']
        self.assertEqual([NATIVE], [m['type'] for m in movements])
        self.assertEqual('ideology_sb_usuthu', movements[0]['ideology'])
        self.assertEqual({'sb_usuthu_royalist_networks': 1}, movements[0]['modifiers'])

    def test_only_one_runtime_type_and_country_scoped_display_name(self):
        root = Path(__file__).resolve().parents[1]
        self.assertFalse((root / 'common/political_movements/sb_usuthu_movement.txt').exists())
        for folder in ('common/scripted_effects', 'common/scripted_triggers', 'common/script_values'):
            for path in (root / folder).glob('*.txt'):
                self.assertNotIn('movement_sb_usuthu', path.read_text(encoding='utf-8-sig'), str(path))
        name = text('common/customizable_localization/sb_usuthu_custom_loc.txt')
        self.assertIn('country_definition = cd:ZUL has_variable = sb_zululand_usuthu_context_var', name)
        self.assertIn('localization_key = movement_royalist_absolutist', name)
        self.assertIn('localization_key = movement_sb_usuthu', name)
        native = text('common/political_movements/zz_sb_absolutist_override.txt')
        self.assertIn('sb_zululand_configure_usuthu_movement = yes', object_block('common/political_movements/zz_sb_absolutist_override.txt', 'on_created'))
        self.assertNotIn('NOT = { has_variable = sb_zululand_usuthu_context_var }', native)


if __name__ == '__main__':
    unittest.main()
