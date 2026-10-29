"""Evaluate the shipped creation gate; native recruitment remains a runtime check."""
import unittest

from tests.test_zulu_court_politics import CourtRuntime, ROOT
from tests.test_zulu_institutions_laws import child, statements
from tools.check_override_inventory import find_object


SOURCE = (ROOT/'common/political_movements/sb_political_movements.txt').read_text(encoding='utf-8-sig')
CREATION = statements(child(find_object(SOURCE, 'movement_sb_cape_liberal'), 'creation_trigger'))


class CapeLiberalCreation(unittest.TestCase):
    def test_open_contest_admits_starting_subjecthood_and_racial_segregation(self):
        rt = CourtRuntime([])
        rt.country.update(id='CAP', journal_entries={'je_sb_cape_politics'})
        for law in ('law_subjecthood', 'law_racial_segregation'):
            rt.country['laws'] = {'law_type:'+law}
            self.assertTrue(rt.condition(CREATION, rt.country), law)
            rt.country['vars']['sb_cape_liberal_resolved_var'] = 1
            self.assertFalse(rt.condition(CREATION, rt.country), law)
            rt.country['vars'].clear()
            rt.country['journal_entries'].clear()
            self.assertFalse(rt.condition(CREATION, rt.country), law)
            rt.country['journal_entries'].add('je_sb_cape_politics')

    def test_other_countries_and_citizenship_laws_stay_ineligible(self):
        rt = CourtRuntime([])
        rt.country.update(id='NAL', laws={'law_type:law_subjecthood'}, journal_entries={'je_sb_cape_politics'})
        self.assertFalse(rt.condition(CREATION, rt.country))
        rt.country['id'] = 'CAP'
        for law in ('law_cultural_exclusion', 'law_multicultural', 'law_ethnostate'):
            rt.country['laws'] = {'law_type:'+law}
            self.assertFalse(rt.condition(CREATION, rt.country), law)


if __name__ == '__main__':
    unittest.main()
