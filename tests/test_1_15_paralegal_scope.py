"""Source-level AI scope regression; native event delivery still needs DP replay."""
from pathlib import Path
import unittest

from tools.check_naval_network import find_game_root
from tools.check_override_inventory import find_object
from tests.test_usuthu_movement_contest import parse

ROOT = Path(__file__).resolve().parents[1]
GAME = find_game_root(None)
EVENT_PATH = Path('events/paralegal_discrimination_events.txt')
HELPERS = ('ai_avoids_radicals', 'ai_wants_radicals')


@unittest.skipIf(GAME is None, 'installed Vanilla sources unavailable')
class ParalegalScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = (GAME / EVENT_PATH).read_bytes()
        source = (GAME / 'common/scripted_triggers/00_ai_triggers.txt').read_text(encoding='utf-8-sig')
        keys = HELPERS + tuple('divided_monarchists_ai_' + path for path in
                               ('monarchist', 'orleanist', 'legitimist', 'bonapartist', 'republican'))
        cls.helpers = {key: parse(find_object(source, key)) for key in keys}

    def ai_triggers(self, source):
        event = parse(find_object(source, 'paralegal_discrimination.1'))
        self.assertIn(('type', '=', 'state_event'), event)
        result = []
        for key, _, option in event:
            if key != 'option':
                continue
            for field, _, chance in option:
                if field == 'ai_chance':
                    self.assertIn(('base', '=', '1'), chance)
                    modifier = next(value for name, _, value in chance if name == 'modifier')
                    self.assertIn(('add', '=', '10'), modifier)
                    result.append(next(value for name, _, value in modifier if name == 'trigger'))
        self.assertEqual(2, len(result))
        return result

    def evaluate(self, nodes, scope):
        """Execute the actual helper predicates with explicit state/country types."""
        results = []
        for key, op, value in nodes:
            self.assertEqual('?=' if key == 'owner' or key.startswith('var:') else '=', op)
            if key == 'owner':
                result = self.evaluate(value, scope['owner'])
            elif key in ('OR', 'AND'):
                terms = [self.evaluate([term], scope) for term in value]
                result = any(terms) if key == 'OR' else all(terms)
            elif key in self.helpers:
                self.assertEqual('yes', value)
                result = self.evaluate(self.helpers[key], scope)
            else:
                self.assertEqual('country', scope['type'], f'{key} requires country scope')
                if key == 'has_journal_entry':
                    result = value in scope['journals']
                elif key == 'var:divided_monarchists_ai_var':
                    result = value == scope['path']
                else:
                    self.fail(f'Unmodelled predicate: {key}')
            results.append(result)
        return all(results)

    def test_native_optional_owner_guards_both_choices_without_a_mod_shadow(self):
        for mod in (ROOT, ROOT.parent / 'Community Mod Framework'):
            self.assertFalse((mod / EVENT_PATH).exists())
        triggers = self.ai_triggers(self.native.decode('utf-8-sig'))
        for trigger, helper in zip(triggers, HELPERS):
            self.assertEqual([('owner', '?=', [(helper, '=', 'yes')])], trigger)

    def test_native_choices_use_the_owner_and_keep_native_ai_weights(self):
        triggers = self.ai_triggers(self.native.decode('utf-8-sig'))
        for journals, path, expected in (
            (set(), 'flag:orleanist', [1, 1]),
            ({'je_divided_monarchists'}, None, [1, 1]),
            ({'je_divided_monarchists'}, 'flag:orleanist', [11, 1]),
            ({'je_divided_monarchists'}, 'flag:legitimist', [11, 1]),
            ({'je_divided_monarchists'}, 'flag:bonapartist', [11, 1]),
            ({'je_divided_monarchists'}, 'flag:republican', [1, 11]),
        ):
            with self.subTest(journals=journals, path=path):
                owner = {'type': 'country', 'journals': journals, 'path': path}
                state = {'type': 'state', 'owner': owner}
                self.assertEqual(expected, [1 + 10 * self.evaluate(trigger, state) for trigger in triggers])

if __name__ == '__main__':
    unittest.main()
