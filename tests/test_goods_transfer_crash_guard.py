"""Native-call boundary and upstream parity; not an engine crash reproduction."""
from pathlib import Path
import unittest

from tools import check_override_inventory as inventory, validate
from tests.test_natal_zululand_gameplay_contract import object_block_from_source
from tests.test_usuthu_movement_contest import parse

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = 'common/treaty_articles/13_goods_transfer.txt'


class GoodsTransferGuardTests(unittest.TestCase):
    def setUp(self):
        game = validate.find_game_root(None)
        self.assertIsNotNone(game, 'Current Vanilla is required for this contract')
        self.vanilla = (game / RELATIVE).read_text(encoding='utf-8-sig')
        self.sb = (ROOT / RELATIVE).read_text(encoding='utf-8-sig')
        self.original = object_block_from_source(self.vanilla, 'possible')
        self.possible = object_block_from_source(self.sb, 'possible')
        self.nodes = parse(self.possible)

    def test_only_possible_wrapper_changes_and_valid_branch_is_vanilla(self):
        self.assertEqual(self.vanilla, self.sb.replace(self.possible, self.original, 1))
        self.assertEqual(['trigger_if', 'trigger_else'], [n[0] for n in self.nodes])
        branch = self.nodes[0][2]
        self.assertEqual('limit', branch[0][0])
        self.assertEqual(parse(self.original), branch[1:])
        self.assertEqual([('always', '=', 'no')], self.nodes[1][2])
        cmf = ROOT.parent / 'Community Mod Framework'
        self.assertFalse((cmf / RELATIVE).exists())
        for path in (cmf / 'common/treaty_articles').glob('*.txt'):
            self.assertNotRegex(path.read_text(encoding='utf-8-sig'), r'(?m)^\s*(?:REPLACE:)?goods_transfer\s*=')

    def test_invalid_scopes_skip_native_call_and_valid_results_are_preserved(self):
        # Evaluate the actual wrapper only. The native body is opaque: reaching
        # it is counted, or fails the test if a prerequisite has been removed.
        references = {
            'market_capital', 'market.owner.market_capital',
            'scope:other_country.market_capital',
            'scope:other_country.market.owner.market_capital',
        }
        limit = self.nodes[0][2][0][2]
        self.assertEqual(references, {v for k, _, v in limit if k == 'exists'})

        def admitted(existing, alive, other_alive):
            def evaluate(nodes, current_alive):
                results = []
                for key, op, value in nodes:
                    if key == 'exists':
                        results.append(value in existing)
                    elif key == 'is_country_alive':
                        self.assertEqual('yes', value)
                        results.append(current_alive)
                    elif key == 'scope:other_country':
                        self.assertEqual('?=', op)
                        results.append(evaluate(value, other_alive))
                    else:
                        self.fail(f'Unexpected guard node: {key}')
                return all(results)
            return evaluate(limit, alive)

        cases = [(references - {r}, True, True) for r in references]
        cases += [(references, False, True), (references, True, False), (set(), False, False)]
        for existing, alive, other_alive in cases:
            with self.subTest(existing=existing, alive=alive, other_alive=other_alive):
                calls = []
                if admitted(existing, alive, other_alive):
                    calls.append('native reachability')
                self.assertEqual([], calls)
        for native_result in (False, True):
            calls = []
            if admitted(references, True, True):
                calls.append('native reachability')
                result = native_result
            else:
                result = False
            self.assertEqual(['native reachability'], calls)
            self.assertEqual(native_result, result)

    def test_upstream_and_result_hashes_are_pinned(self):
        import json
        data = json.loads((ROOT / 'Docs/compatibility/override_inventory.json').read_text())
        entry = next(e for e in data['same_path_files'] if e['path'] == RELATIVE)
        self.assertEqual(inventory.sha256_bytes(self.vanilla.encode('utf-8-sig')), entry['upstream_sha256'])
        self.assertEqual(inventory.sha256(ROOT / RELATIVE), entry['mod_sha256'])


if __name__ == '__main__':
    unittest.main()
