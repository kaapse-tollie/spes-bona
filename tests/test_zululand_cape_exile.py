"""Exercise the host fallback with a foreign event root and an actual minor."""
import unittest
from tests.test_zululand_claimant_return import RoyalHandoffRuntime


class ZululandCapeExileTests(unittest.TestCase):
    def test_whole_house_follows_the_available_host_without_child_agitators(self):
        for cape_alive in (True, False):
            with self.subTest(cape_alive=cape_alive):
                rt = RoyalHandoffRuntime()
                rt.countries['c:CAP']['alive'] = cape_alive
                rt.run('sb_zululand_mark_and_exile_royal_house', rt.natal)
                host = rt.countries['c:CAP'] if cape_alive else rt.natal
                for person in (rt.king, rt.heir):
                    self.assertIs(person['owner'], host)
                self.assertFalse(rt.heir['agitator'])
                self.assertEqual({}, rt.scopes['root']['vars'])
