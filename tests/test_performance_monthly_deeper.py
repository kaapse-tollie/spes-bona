"""Equivalent global traversal and monthly involvement maintenance.

These run the affected script bodies, including current-country versus ROOT
scope, and count traversals. They do not claim measured game tick improvements.
"""
from copy import deepcopy
from hashlib import sha256
from itertools import product
import unittest

from tests.test_zulu_institutions_laws import ROOT, read, statements
from tools.check_override_inventory import find_object


OLD_INVOLVEMENT = """old = {
 every_country = {
  limit = { OR = {
   is_involved_in_journal_entry = je_sb_imperial_confederation_scheme
   sb_should_be_involved_in_imperial_confederation = yes
  } }
  if = {
   limit = {
    is_involved_in_journal_entry = je_sb_imperial_confederation_scheme
    NOT = { sb_should_be_involved_in_imperial_confederation = yes }
   }
   save_temporary_scope_as = sb_imperial_confederation_involvement_candidate
   c:GBR ?= { je:je_sb_imperial_confederation_scheme ?= {
    remove_involved_country = scope:sb_imperial_confederation_involvement_candidate
   } }
  }
  if = {
   limit = {
    NOT = { is_involved_in_journal_entry = je_sb_imperial_confederation_scheme }
    sb_should_be_involved_in_imperial_confederation = yes
   }
   save_temporary_scope_as = sb_imperial_confederation_involvement_candidate
   c:GBR ?= { je:je_sb_imperial_confederation_scheme ?= {
    add_involved_country = scope:sb_imperial_confederation_involvement_candidate
   } }
  }
 }
}"""


class Runtime:
    def __init__(self, countries, britain=True, journal=True):
        self.countries = deepcopy(countries)
        self.britain, self.journal = britain, journal
        self.scopes = {}
        self.visits = self.state_visits = self.eligibility_checks = 0
        self.operations = []
        self.globals, self.containers = set(), set()

    def condition(self, nodes, scope):
        for key, _, value in nodes:
            if key == 'OR': result = any(self.condition([node], scope) for node in value)
            elif key == 'NOT': result = not any(self.condition([node], scope) for node in value)
            elif key == 'any_country':
                result = False
                for country in self.countries:
                    self.visits += 1
                    if self.condition(value, country):
                        result = True
                        break
            elif key == 'any_scope_state':
                result = False
                for state in scope.get('states', []):
                    self.state_visits += 1
                    if self.condition(value, state):
                        result = True
                        break
            elif key == 'is_involved_in_journal_entry': result = scope['involved']
            elif key == 'sb_should_be_involved_in_imperial_confederation':
                self.eligibility_checks += 1
                result = scope['eligible']
            elif key == 'container_exists': result = value in self.containers
            elif key == 'has_global_variable': result = value in self.globals
            elif key == 'has_variable': result = value in scope.get('vars', set())
            else: raise AssertionError(key)
            if not result: return False
        return True

    def execute(self, nodes, scope):
        matched = False
        for key, _, value in nodes:
            if key == 'limit': continue
            if key in ('if', 'else_if'):
                if key == 'if': matched = False
                limit = next((v for k, _, v in value if k == 'limit'), [])
                if not matched and self.condition(limit, scope):
                    self.execute(value, scope)
                    matched = True
            elif key == 'every_country':
                limit = next((v for k, _, v in value if k == 'limit'), [])
                for country in self.countries:
                    if self.condition(limit, country): self.execute(value, country)
            elif key == 'save_temporary_scope_as': self.scopes[value] = scope
            elif key == 'c:GBR':
                if self.britain: self.execute(value, {'id': 'GBR'})
            elif key == 'je:je_sb_imperial_confederation_scheme':
                if self.journal: self.execute(value, {'id': 'journal'})
            elif key in ('add_involved_country', 'remove_involved_country'):
                country = self.scopes[value.removeprefix('scope:')]
                country['involved'] = key == 'add_involved_country'
                self.operations.append((key, country['id']))
            else: raise AssertionError(key)


def atoms(nodes, path=()):
    """This OR-only predicate is a union of atoms with unchanged scope paths."""
    for key, op, value in nodes:
        if isinstance(value, list):
            assert key in ('OR', 'any_country', 'any_scope_state'), key
            yield from atoms(value, path if key == 'OR' else path + (key,))
        else:
            yield path, key, op, value


class MonthlyTraversalParityTests(unittest.TestCase):
    def involvement(self):
        return statements(find_object(read(ROOT, 'common/scripted_effects/sb_eastern_sphere_effects.txt'),
                                      'sb_imperial_confederation_validate_involvement'))

    def formation(self):
        return statements(find_object(read(ROOT, 'common/scripted_triggers/sb_saf_formation_triggers.txt'),
                                      'sb_southern_formation_has_blocking_story_transaction'))

    def old_formation(self, nodes):
        # Reconstruct the previous independent state scan from the same pinned
        # atoms, without depending on an external historical checkout.
        result = deepcopy(nodes)
        outer = result[0][2]
        country = next(v for k, _, v in outer if k == 'any_country')
        country_or = country[0][2]
        state = next(node for node in country_or if node[0] == 'any_scope_state')
        country_or.remove(state)
        outer.insert(len(outer)-1, ('any_country', '=', [state]))
        return result

    def test_involvement_once_per_country_without_changing_effects_or_scope(self):
        for britain, journal in product((False, True), repeat=2):
            countries = [dict(id=str(i), involved=inv, eligible=elig)
                         for i, (inv, elig) in enumerate(product((False, True), repeat=2))]
            old, new = Runtime(countries, britain, journal), Runtime(countries, britain, journal)
            # Neither implementation should use the unrelated event ROOT.
            old.execute(statements(OLD_INVOLVEMENT), {'id': 'FOREIGN_ROOT'})
            new.execute(self.involvement(), {'id': 'FOREIGN_ROOT'})
            self.assertEqual(old.countries, new.countries)
            self.assertEqual(old.operations, new.operations)
            self.assertEqual(4, new.eligibility_checks)
            self.assertLess(new.eligibility_checks, old.eligibility_checks)
            # A second pulse repairs nothing and keeps every country unchanged.
            old.execute(statements(OLD_INVOLVEMENT), {'id': 'FOREIGN_ROOT'})
            new.execute(self.involvement(), {'id': 'FOREIGN_ROOT'})
            self.assertEqual(old.countries, new.countries)
            self.assertEqual(old.operations, new.operations)

    def test_formation_retains_every_original_guard_and_scope(self):
        pinned = sorted(atoms(self.formation()))
        self.assertEqual(227, len(pinned))
        self.assertEqual('0ba1230db7e945703e61c5bf91af02dee9c9a23364184ef29a204322796a5573',
                         sha256(repr(pinned).encode()).hexdigest())

    def test_every_story_guard_still_blocks_even_on_retagged_holders(self):
        new = self.formation()
        old = self.old_formation(new)
        for path, key, _, value in atoms(new):
            countries = [dict(id='RETAGGED', vars=set(), states=[{'vars': set()}])]
            a, b = Runtime(countries), Runtime(countries)
            for runtime in (a, b):
                if key == 'container_exists': runtime.containers.add(value)
                elif key == 'has_global_variable': runtime.globals.add(value)
                elif len(path) == 2: runtime.countries[0]['states'][0]['vars'].add(value)
                else: runtime.countries[0]['vars'].add(value)
            self.assertTrue(a.condition(old, {'id': 'FOREIGN_ROOT'}), value)
            self.assertTrue(b.condition(new, {'id': 'FOREIGN_ROOT'}), value)

    def test_one_world_scan_when_clear_and_state_scan_skipped_on_route_holder(self):
        new = self.formation()
        old = self.old_formation(new)
        countries = [dict(id=str(i), vars=set(), states=[{'vars': set()}] * 4) for i in range(300)]
        a, b = Runtime(countries), Runtime(countries)
        self.assertFalse(a.condition(old, {})); self.assertFalse(b.condition(new, {}))
        self.assertEqual((600, 300), (a.visits, b.visits))
        self.assertEqual((1200, 1200), (a.state_visits, b.state_visits))
        countries[0]['vars'].add('sb_natal_terminal_outcome_pending_var')
        a, b = Runtime(countries), Runtime(countries)
        self.assertTrue(a.condition(old, {})); self.assertTrue(b.condition(new, {}))
        self.assertEqual((1200, 0), (a.state_visits, b.state_visits))


if __name__ == '__main__':
    unittest.main()
