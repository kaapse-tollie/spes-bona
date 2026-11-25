"""Native NOR semantics and the compound guards audited on 13 November 2026.

Truth tables execute the source's Boolean grouping. Scope/iterator/helper atoms
are supplied explicitly; this does not emulate native event delivery or USFP.
"""
from itertools import product
from pathlib import Path
import re
import unittest

from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import find_object

ROOT = Path(__file__).resolve().parents[1]


def definition(path, key, directive=None):
    return statements(find_object((ROOT / path).read_text(encoding='utf-8-sig'), key, directive=directive))


def field(nodes, key):
    return next(v for k, _, v in nodes if k == key)


def walk(nodes):
    for node in nodes:
        yield node
        if isinstance(node[2], list):
            yield from walk(node[2])


def evaluate(nodes, atoms):
    def check(node):
        key, _, value = node
        if key in ('NOT', 'NOR'): return not any(check(n) for n in value)
        if key == 'OR': return any(check(n) for n in value)
        if key == 'AND': return all(check(n) for n in value)
        return atoms[repr(node)]
    return all(check(n) for n in nodes)


def atoms_in(nodes):
    for node in nodes:
        if node[0] in ('NOT', 'NOR', 'OR', 'AND'):
            yield from atoms_in(node[2])
        else:
            yield node


class CompoundNegationTests(unittest.TestCase):
    def test_native_not_rejects_any_true_child_but_a_scope_is_one_child(self):
        for a, b in product((False, True), repeat=2):
            simple = [('a', '=', 'yes'), ('b', '=', 'yes')]
            atoms = {repr(n): value for n, value in zip(simple, (a, b))}
            self.assertEqual(not (a or b), evaluate([('NOT', '=', simple)], atoms))
            self.assertEqual(not (a and b), evaluate([('NOT', '=', [('AND', '=', simple)])], atoms))
            owner = ('owner', '=', simple)
            self.assertEqual(not (a and b), evaluate([('NOT', '=', [owner])], {repr(owner): a and b}))

    def test_reactionary_exception_requires_both_usfp_and_american_country(self):
        creation = field(definition('common/political_movements/zzz_sb_chiefdoms_uprising_overrides.txt',
                                    'movement_reactionary', 'REPLACE'), 'creation_trigger')
        leaves = list(atoms_in(creation))
        active = next(n for n in leaves if n[0] == 'is_usfp_active')
        american = next(n for n in leaves if n[0] == 'usfp_country_is_american')
        normal = [n for n in leaves if n not in (active, american)]
        for usfp, culture in product((False, True), repeat=2):
            atoms = {repr(n): n[0] != 'any_political_movement' for n in normal}
            atoms.update({repr(active): usfp, repr(american): culture})
            self.assertEqual(not (usfp and culture), evaluate(creation, atoms), (usfp, culture))
            # Fixing the exception must not bypass any native creation requirement.
            for n in normal:
                invalid = {**atoms, repr(n): not atoms[repr(n)]}
                self.assertFalse(evaluate(creation, invalid), (usfp, culture, n[0]))

    def test_absolutist_character_must_approve_both_royal_laws(self):
        support = field(definition('common/political_movements/zz_sb_absolutist_override.txt',
                                   'movement_royalist_absolutist', 'REPLACE'), 'character_support_trigger')
        gate = next(n for n in walk(support) if n[0] == 'NOT' and
                    [c[0] for c in n[2]] == ['law_stance', 'law_stance'])
        for disapproves_monarchy, disapproves_autocracy in product((False, True), repeat=2):
            atoms = {repr(n): v for n, v in zip(gate[2], (disapproves_monarchy, disapproves_autocracy))}
            self.assertEqual(not disapproves_monarchy and not disapproves_autocracy, evaluate([gate], atoms))

    def test_bechuanaland_popups_cancel_if_either_eligibility_or_route_is_lost(self):
        for number in ('032', '033'):
            event = definition('events/sb_bechuanaland_corridor_events.txt', 'sb_bechuanaland_corridor.' + number)
            valid, cancel = field(event, 'trigger'), field(event, 'cancellation_trigger')
            for eligible, correct_route in product((False, True), repeat=2):
                atoms = {repr(n): v for n, v in zip(valid, (eligible, correct_route))}
                self.assertEqual(not evaluate(valid, atoms), evaluate(cancel, atoms), (number, eligible, correct_route))

    def test_martinus_dismissal_covers_lost_authority_or_lost_pending_stage(self):
        event = definition('events/sb_martinus_confederation_events.txt', 'sb_martinus_confederation.010')
        options = [v for k, _, v in event if k == 'option']
        valid, fallback = field(options[1], 'trigger'), field(options[2], 'trigger')
        for authority, pending in product((False, True), repeat=2):
            atoms = {repr(n): v for n, v in zip(valid, (authority, pending))}
            self.assertEqual(not evaluate(valid, atoms), evaluate(fallback, atoms), (authority, pending))

    def test_port_natal_retry_covers_each_launch_blocker_but_not_invalid_participants(self):
        event = definition('events/sb_natal_crisis_events.txt', 'sb_natal_crisis.085')
        options = [v for k, _, v in event if k == 'option']
        launch, retry = field(options[0], 'trigger'), field(options[2], 'trigger')
        ready = {repr(n): n[0] not in ('has_truce_with', 'has_variable') for n in atoms_in(launch)}
        required = {repr(n): True for n in retry if n[0] != 'NOT'}
        self.assertFalse(evaluate(retry, {**ready, **required}))
        for n in atoms_in(launch):
            atoms = {**ready, **required, repr(n): not ready[repr(n)]}
            participant_valid = all(atoms[k] for k in required)
            self.assertEqual(participant_valid, evaluate(retry, atoms), n[0])
        for key in required:
            self.assertFalse(evaluate(retry, {**ready, **required, key: False}))

    def test_cetshwayo_without_either_backer_shows_the_no_backer_tooltip(self):
        effect = definition('common/scripted_effects/sb_court_cast_effects.txt', 'sb_court_preview_brother_backing')
        branch = next(v for k, _, v in walk(effect) if k == 'else_if')
        gate = field(branch, 'limit')
        leaves = list(atoms_in(gate))
        for cetshwayo, second_backer in product((False, True), repeat=2):
            atoms = {repr(n): v for n, v in zip(leaves, (cetshwayo, second_backer))}
            self.assertEqual(not (cetshwayo and second_backer), evaluate(gate, atoms))


def multi_child_nots(text):
    """Lexical census: comments/strings are opaque; scoped blocks stay one child."""
    tokens = [m.group() for m in re.finditer(
        r'#[^\n]*|"(?:\\.|[^"\\])*"|[{}]|[!<>?]?=|[<>]|[^{}\s=<>!?#"]+', text)
        if not m.group().startswith('#')]
    pairs, stack = {}, []
    for i, token in enumerate(tokens):
        if token == '{': stack.append(i)
        elif token == '}': pairs[stack.pop()] = i
    assert not stack
    found = []
    for i in range(len(tokens) - 2):
        if tokens[i:i+3] != ['NOT', '=', '{']: continue
        children, pos, end = [], i + 3, pairs[i + 2]
        while pos < end:
            key, op, value = tokens[pos:pos+3]
            assert op in ('=', '?=', '!=', '<', '>', '<=', '>='), (key, op)
            children.append(key)
            pos = pairs[pos+2] + 1 if value == '{' else pos + 3
        if len(children) > 1: found.append(tuple(children))
    return found


class NegationInventoryTests(unittest.TestCase):
    def test_new_flat_compound_negations_require_an_intent_review(self):
        found = []
        for directory in ('common', 'events'):
            for path in sorted((ROOT / directory).rglob('*.txt')):
                found.extend((str(path.relative_to(ROOT)), children)
                             for children in multi_child_nots(path.read_text(encoding='utf-8-sig')))
        self.assertEqual([
            # Vanilla 1.15.2's Peru-Bolivia exception, retained verbatim in the autonomy action.
            ('common/diplomatic_actions/zz_sb_colonial_autonomy.txt', ('AND', 'scope:target_country')),
            ('common/political_movements/zz_sb_absolutist_override.txt', ('law_stance', 'law_stance')),
        ], found)


if __name__ == '__main__':
    unittest.main()
