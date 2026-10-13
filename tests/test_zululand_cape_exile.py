"""Royal exile destinations and later claimant lookup."""
import re
import unittest
from tests.test_klip_river_scope_context import resolve
from tests.test_natal_zululand_gameplay_contract import object_block, object_block_from_source
EFFECTS = 'common/scripted_effects/sb_zululand_settlement_effects.txt'
class ZululandCapeExileTests(unittest.TestCase):
    def test_both_exiles_go_to_cape_and_later_claimant_routes_find_the_host(self):
        exile = object_block(EFFECTS, 'sb_zululand_mark_and_exile_royal_house')
        # Capture both before removing either from office: succession can change heir.
        for role in ('ruler', 'heir'):
            self.assertLess(exile.index(f'save_scope_as = sb_zululand_exile_{role}'),
                            exile.index('exile_character_with_role_cleanup = yes'))
            branch = object_block_from_source(exile, f'scope:sb_zululand_exile_{role} ?')
            ref = re.search(r'transfer_character = (\S+)', branch)[1]
            for event_root in ('NAL', 'ZUL'):
                self.assertEqual('CAP', resolve(ref, role, event_root, {}))
        for name in ('sb_zululand_return_exiled_claimant', 'sb_zululand_restore_dynastic_ruler'):
            route = object_block(EFFECTS, name)
            cape = object_block_from_source(route, 'c:CAP ?')
            self.assertIn('has_variable = sb_zululand_exiled_claimant_var', cape)
            self.assertIn('transfer_character = c:ZUL', cape)
            self.assertLess(route.index('c:CAP ?'), route.index('any_character_in_exile_pool'))


if __name__ == '__main__':
    unittest.main()
