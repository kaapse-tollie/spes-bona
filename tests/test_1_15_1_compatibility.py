"""1.15.1 ports, exact CMF payload boundaries and mandatory verification."""
import copy
import hashlib
from itertools import product
import json
from pathlib import Path
import unittest
from unittest import mock

from tools import check_1_15_target as previous_target
from tools import check_1_15_1_target as target
from tools import check_1_15_2_target as current_target
from tools import check_override_inventory as inventory, cmf_patch, validate
from tests.test_performance_pass import Runtime
from tests.test_zulu_institutions_laws import child, statements, tokens

ROOT = Path(__file__).resolve().parents[1]
GAME = validate.find_game_root(None)
CMF = ROOT.parent / 'Community Mod Framework'
HOTFIX_PATCH = ROOT / 'patches/cmf/sb-1.15.1-r1'
MOVEMENTS = {
    '01_religious_movements.txt': ('movement_religious_majority', 'movement_religious_minority'),
    '02_cultural_movement.txt': ('movement_cultural_minority',),
    '04_national_movements.txt': ('movement_hindu_nationalist', 'movement_muslim_nationalist'),
    '05_slave_revolt_movements.txt': ('movement_slave_revolt',),
}
FLAG = b'\t\tcan_secede_during_revolution = yes\n\n'


class CurrentPatchTests(unittest.TestCase):
    def test_historical_hotfix_retained_the_four_previous_payloads(self):
        previous = ROOT / 'patches/cmf/sb-1.15.0-r2'
        old = json.loads((previous / 'manifest.json').read_text())
        current = json.loads((HOTFIX_PATCH / 'manifest.json').read_text())
        self.assertEqual(8, len(current['files']))
        self.assertEqual(14, len(current['upstream_contracts']))
        for entry in old['files']:
            self.assertIn(entry, current['files'])
            self.assertEqual((previous / entry['payload']).read_bytes(),
                             (HOTFIX_PATCH / entry['payload']).read_bytes())
        for old_contract, new_contract in zip(old['upstream_contracts'], current['upstream_contracts']):
            self.assertEqual({k: v for k, v in old_contract.items() if k != 'file_sha256'},
                             {k: v for k, v in new_contract.items() if k != 'file_sha256'})

    def test_movement_payloads_and_native_hotfix_change_only_the_six_flags(self):
        patch = json.loads((HOTFIX_PATCH / 'manifest.json').read_text())
        delta = {e['path']: e for e in json.loads(target.OUTPUT.read_text())['entries']}
        for filename, keys in MOVEMENTS.items():
            path = 'common/political_movements/ycom_' + filename
            entry = next(e for e in patch['files'] if e['path'] == path)
            payload = (HOTFIX_PATCH / entry['payload']).read_bytes()
            self.assertEqual(len(keys), payload.count(FLAG), path)
            self.assertEqual(entry['original_sha256'], cmf_patch.digest(payload.replace(FLAG, b'')))
            native_path = 'common/political_movements/' + filename
            native = (GAME / native_path).read_bytes()
            self.assertEqual(delta['game/' + native_path]['old']['sha1'],
                             hashlib.sha1(native.replace(FLAG, b'')).hexdigest())
            effective = (CMF / path).read_text(encoding='utf-8-sig')
            self.assertEqual(tokens(payload.decode('utf-8-sig')), tokens(effective), path)
            for key in keys:
                block = inventory.find_object(effective, key, directive='REPLACE')
                self.assertIn(('can_secede_during_revolution', '=', 'yes'),
                              statements(child(block, 'secession')))
        minority = ROOT / 'common/political_movements/zz_sb_cultural_minority_movement_override.txt'
        block = inventory.find_object(minority.read_text(encoding='utf-8-sig'), 'movement_cultural_minority', directive='REPLACE')
        self.assertIn(('can_secede_during_revolution', '=', 'yes'), statements(child(block, 'secession')))
        for path in (CMF / 'common/political_movements/ycom_00_ideological_movements.txt',
                     ROOT / 'common/political_movements/zzz_sb_chiefdoms_uprising_overrides.txt',
                     ROOT / 'common/political_movements/zzz_sb_cape_political_movement_overrides.txt'):
            self.assertNotRegex(path.read_text(encoding='utf-8-sig'), r'(?m)^\s*can_secede_during_revolution\s*=\s*yes\b')

    def test_labor_character_weight_and_anti_slavery_helper_follow_cmf(self):
        native = inventory.find_object((CMF / 'common/political_movements/ycom_00_ideological_movements.txt').read_text(encoding='utf-8-sig'), 'movement_labor', directive='REPLACE')
        sb = inventory.find_object((ROOT / 'common/political_movements/zzz_sb_chiefdoms_uprising_overrides.txt').read_text(encoding='utf-8-sig'), 'movement_labor', directive='REPLACE')
        self.assertEqual(tokens(child(native, 'character_support_weight')), tokens(child(sb, 'character_support_weight')))
        self.assertIn('has_ideology = ideology:ideology_communist_leader', sb)
        helper = inventory.find_object((CMF / 'common/scripted_triggers/com_political_movement_triggers.txt').read_text(encoding='utf-8-sig'), 'character_is_anti_slavery', directive='REPLACE_OR_CREATE')
        self.assertIn('has_ideology = ideology:ideology_humanitarian_royalist', helper)
        self.assertNotIn('ideology:ideology_utopian', helper)
        anti_slavery = inventory.find_object((ROOT / 'common/political_movements/zzz_sb_chiefdoms_uprising_overrides.txt').read_text(encoding='utf-8-sig'), 'movement_anti_slavery', directive='REPLACE')
        self.assertIn('character_is_anti_slavery = yes', anti_slavery)

    def test_depot_delta_reproduces_from_both_pinned_manifests(self):
        old_path = target.depot.default_manifest_path(previous_target.NEW)
        if not old_path.is_file() or not target.depot.default_manifest_path(target.NEW).is_file():
            self.skipTest('Historical 1.15.0/1.15.1 manifest pair unavailable')
        old = target.depot.decode_manifest(old_path, previous_target.NEW)
        new = target.depot.decode_manifest(target.depot.default_manifest_path(target.NEW), target.NEW)
        changed = {p for p in old.records.keys() | new.records.keys()
                   if p not in old.records or p not in new.records
                   or old.records[p].evidence() != new.records[p].evidence()}
        data = json.loads(target.OUTPUT.read_text())
        self.assertEqual(changed, {e['path'] for e in data['entries']})
        for entry in data['entries']:
            self.assertEqual(old.records[entry['path']].evidence() if entry['path'] in old.records else None, entry['old'])
            self.assertEqual(new.records[entry['path']].evidence(), entry['new'])
            self.assertTrue(entry['disposition'])

    def test_inventory_requires_depot_manifest_native_contracts_and_installed_tree(self):
        data = json.loads((ROOT / 'Docs/compatibility/override_inventory.json').read_text())
        with mock.patch.object(current_target, 'verify_current_target', side_effect=ValueError('depot sentinel')) as depot_check, \
             mock.patch.object(cmf_patch, 'verify_upstream', side_effect=ValueError('native sentinel')) as native_check:
            errors = inventory.validate(ROOT, GAME, data, CMF)
        depot_check.assert_called_once_with(GAME)
        native_check.assert_called_once()
        self.assertTrue(any('depot sentinel' in e for e in errors))
        self.assertTrue(any('native sentinel' in e for e in errors))
        with mock.patch.object(cmf_patch, 'verify_install', side_effect=ValueError('tree sentinel')) as tree_check:
            errors = inventory.validate(ROOT, GAME, data, CMF)
        tree_check.assert_called_once()
        self.assertTrue(any('tree sentinel' in e for e in errors))
        altered = copy.deepcopy(data)
        altered['dependencies'][0]['patch_manifest_sha256'] = '0' * 64
        errors = inventory.validate(ROOT, GAME, altered, CMF)
        self.assertTrue(any('CMF patch manifest hash mismatch' in e for e in errors))

    def test_colonial_infamy_uses_native_claim_independent_value_and_target_discount(self):
        class InfamyRuntime(Runtime):
            def ref(self, key, scope, prev=None):
                if key == 'state_infamy_value':
                    # Model the native value as an input; require its scope marker
                    # before evaluation. The engine owns population/recognition maths.
                    assert self.scopes.get('infamy_ignores_claim') is scope
                    return scope['native_infamy']
                return super().ref(key, scope, prev)

            def condition(self, nodes, scope, prev=None):
                if len(nodes) == 1 and nodes[0][0] == 'is_country_type':
                    return scope['country_type'] == nodes[0][2]
                return super().condition(nodes, scope, prev)

            def calc(self, nodes, scope, prev=None):
                rewritten = []
                for key, op, value in nodes:
                    if key == 'scope:second_state':
                        rewritten.append(('add', '=', str(self.calc(value, self.scopes['second_state'], scope))))
                    elif key == 'save_temporary_scope_as':
                        self.scopes[value] = scope
                    else:
                        rewritten.append((key, op, value))
                return super().calc(rewritten, scope, prev)

        native = (GAME / 'common/diplomatic_actions/56_stake_colonial_claim.txt').read_text(encoding='utf-8-sig')
        sb = (ROOT / 'common/diplomatic_actions/zz_sb_stake_colonial_claim_override.txt').read_text(encoding='utf-8-sig')
        def value(source):
            start = source.rfind('set_local_variable', 0, source.index('name = infamy_value'))
            return statements(child(inventory.extract_braced_object(source, start), 'value'))
        for kind, claimed, amount in product(('recognized', 'unrecognized', 'decentralized'), (False, True), (0, 4, 100)):
            outputs = []
            for source in (native, sb):
                rt = InfamyRuntime()
                rt.scopes['second_state'] = {'owner': {'country_type': kind}, 'claimed': claimed, 'native_infamy': amount}
                outputs.append(rt.calc(value(source), {}))
            self.assertEqual([amount * (.25 if kind == 'decentralized' else .5)] * 2, outputs)


if __name__ == '__main__':
    unittest.main()
