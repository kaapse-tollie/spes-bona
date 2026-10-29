"""Exercise grant, snapshot and restore scripts; no native recruitment simulation."""
from copy import deepcopy
from decimal import Decimal
import unittest

from tests.test_zulu_annexation_movement import (
    annexation, native_disband, deliver, run_effect, movement, CHOICE, INITIAL,
    INITIAL_EXPIRY, ANNEXATION, OLD_GRANT, PENDING, EVENTS, RECEIPT, ROOT,
)
from tests.test_klip_punitive_protectorate import (
    game_day, variables, effect_nodes, ENTHUSIASM_EFFECT, expression,
)
from tests.test_natal_zululand_gameplay_contract import object_block
from tools.check_override_inventory import find_object

REFUSAL = 'sb_shepstone_refusal_zulu_movement_attraction'
REPEAL = 'sb_shepstone_repeal_zulu_movement_attraction'
EXPIRIES = {
    INITIAL: INITIAL_EXPIRY,
    REFUSAL: 'sb_natal_zulu_shepstone_refusal_until_var',
    REPEAL: 'sb_natal_zulu_shepstone_repeal_until_var',
}
DURATIONS = {INITIAL: 7300, REFUSAL: 9000, REPEAL: 3600}
BASE_STRENGTH = {INITIAL: Decimal(1), REFUSAL: Decimal(1), REPEAL: Decimal('.5')}
APPLIED = {'sb_natal_shepstone_rejection_attraction_applied_var',
           'sb_natal_shepstone_repeal_attraction_applied_var'}


def grant(state, modifier, date):
    state['date'] = date
    if modifier == INITIAL:
        run_effect('add_movement_enthusiasm_modifier', state, actor=state['movements'][0])
    else:
        action = 'declined' if modifier == REFUSAL else 'repealed'
        state['flags'].add('sb_natal_shepstone_' + action + '_var')
        run_effect('sb_natal_sync_' + action + '_shepstone_zulu_movement_attraction', state)


def granted_state():
    state = annexation()
    state['movements'] = [movement(enthusiasm=False)]
    grant(state, INITIAL, '1840.1.1')
    grant(state, REFUSAL, '1845.2.1')
    grant(state, REPEAL, '1848.3.1')
    state['date'] = '1850.6.6'
    return state


def strength(record, day, base=Decimal(1)):
    return base * record['multiplier'] * max(0, record['end'] - day) / (record['end'] - record['start'])


class ZuluMovementModifierPreservationTests(unittest.TestCase):
    def test_grants_record_native_durations_and_never_regrant_shepstone(self):
        state = granted_state()
        old = state['movements'][0]
        for modifier, expiry in EXPIRIES.items():
            record = old['modifiers'][modifier]
            self.assertEqual(DURATIONS[modifier], record['end'] - record['start'])
            self.assertEqual(record['end'], variables(state, old)[expiry])
        self.assertTrue(APPLIED <= state['flags'])
        before = deepcopy(old)
        grant(state, REFUSAL, '1851.1.1')
        grant(state, REPEAL, '1851.1.1')
        self.assertEqual(before, old)

    def test_all_three_keep_expiry_and_decay_after_delayed_receipt_and_reload(self):
        for auto_enthusiasm in (False, True):
            with self.subTest(native_enthusiasm=auto_enthusiasm):
                state = granted_state()
                old = deepcopy(state['movements'][0]['modifiers'])
                state['native_enthusiasm_on_create'] = auto_enthusiasm
                run_effect(CHOICE, state, root='foreign_event_root')
                native_disband(state, state['movements'][0])
                self.assertEqual({v: old[k]['end'] for k, v in EXPIRIES.items()}, variables(state, 'NAL'))
                state = deepcopy(state)  # Only persistent variables cross the save boundary.
                state['date'] = '1850.6.19'  # Account for all elapsed time, not just one day.
                deliver(state)
                new = state['movements'][0]
                self.assertEqual({INITIAL, REFUSAL, REPEAL, ANNEXATION}, set(new['modifiers']))
                for modifier in EXPIRIES:
                    record = new['modifiers'][modifier]
                    self.assertEqual(old[modifier]['end'], record['end'])
                    self.assertLess(record['multiplier'], 1)
                    for day in (game_day(state['date']), game_day('1855.1.1'), record['end']):
                        self.assertAlmostEqual(strength(old[modifier], day, BASE_STRENGTH[modifier]),
                                               strength(record, day, BASE_STRENGTH[modifier]), delta=Decimal('.00001'))
                annexed = new['modifiers'][ANNEXATION]
                self.assertEqual((Decimal(1), 7300), (annexed['multiplier'], annexed['end'] - annexed['start']))
                self.assertEqual({}, variables(state, 'NAL'))
                self.assertEqual(set(EXPIRIES.values()), set(variables(state, new)))
                self.assertFalse(set(EXPIRIES.values()) & state['flags'])
                self.assertTrue(APPLIED | {OLD_GRANT} <= state['flags'])
                self.assertNotIn(PENDING, state['flags'])
                before = deepcopy(new)
                state['date'] = '1851.1.1'
                deliver(state)
                run_effect(CHOICE, state)
                run_effect('sb_natal_create_zulu_national_movement', state)
                self.assertEqual(before, new)

    def test_expiry_during_pending_receipt_is_not_renewed(self):
        state = granted_state()
        state['date'] = '1859.12.31'
        old = state['movements'][0]
        old['modifiers'].pop(REPEAL)  # Already expired naturally before disbanding.
        run_effect(CHOICE, state)
        native_disband(state, old)
        state['native_enthusiasm_on_create'] = True
        state['date'] = '1860.1.1'  # Initial Enthusiasm ends today.
        deliver(state)
        new = state['movements'][0]
        self.assertEqual({REFUSAL, ANNEXATION}, set(new['modifiers']))
        self.assertEqual({EXPIRIES[REFUSAL]}, set(variables(state, new)))
        self.assertEqual({}, variables(state, 'NAL'))

    def test_removed_or_untracked_modifiers_are_not_invented(self):
        for mode in ('removed', 'untracked'):
            state = granted_state()
            old = state['movements'][0]
            if mode == 'removed':
                old['modifiers'].clear()  # Stale expiry records are insufficient.
            else:
                old['variables'].clear()
                old['flags'].difference_update(EXPIRIES.values())
            run_effect(CHOICE, state)
            native_disband(state, old)
            deliver(state)
            self.assertEqual({ANNEXATION}, set(state['movements'][0]['modifiers']))
            self.assertEqual({}, variables(state, 'NAL'))
            self.assertTrue(APPLIED <= state['flags'])

    def test_absent_movement_gets_only_annexation_and_unapplied_shepstone_grant(self):
        state = annexation(existing=False)
        state['flags'].add('sb_natal_shepstone_declined_var')
        state['native_enthusiasm_on_create'] = True
        run_effect(CHOICE, state)
        new = state['movements'][0]
        self.assertEqual({REFUSAL, ANNEXATION}, set(new['modifiers']))
        self.assertEqual(Decimal(1), new['modifiers'][REFUSAL]['multiplier'])
        self.assertEqual(9000, new['modifiers'][REFUSAL]['end'] - new['modifiers'][REFUSAL]['start'])
        self.assertEqual({EXPIRIES[REFUSAL]}, set(variables(state, new)))

    def test_native_grant_unchanged_for_other_countries_and_identities(self):
        for owner, culture, kind in (('GBR', 'cu:zulu', 'movement_cultural_minority'),
                                     ('NAL', 'cu:xhosa', 'movement_cultural_minority'),
                                     ('NAL', 'cu:zulu', 'movement_royalist_absolutist')):
            state = annexation()
            other = movement(owner, culture, kind, enthusiasm=False)
            run_effect('add_movement_enthusiasm_modifier', state, actor=other, root='foreign_event_root')
            record = other['modifiers'][INITIAL]
            self.assertEqual((Decimal(1), 7300), (record['multiplier'], record['end'] - record['start']))
            self.assertFalse(other['flags'])
            self.assertFalse(other['variables'])

    def test_enthusiasm_regrant_tracks_new_grant_not_obsolete_expiry(self):
        state = granted_state()
        grant(state, INITIAL, '1849.1.1')
        run_effect(CHOICE, state)
        native_disband(state, state['movements'][0])
        state['date'] = '1850.1.1'
        deliver(state)
        self.assertEqual(game_day('1869.1.1'), state['movements'][0]['modifiers'][INITIAL]['end'])

    def test_override_keeps_native_grant_and_adds_only_hidden_scoped_bookkeeping(self):
        game = ROOT.parents[4] / 'Library/Application Support/Steam/steamapps/common/Victoria 3/game'
        native = find_object((game / 'common/scripted_effects/00_movement_effects.txt').read_text(encoding='utf-8-sig'),
                             'add_movement_enthusiasm_modifier')
        nodes = effect_nodes('add_movement_enthusiasm_modifier')
        self.assertEqual(expression(native), nodes[:1])
        self.assertEqual('sb_natal_record_zulu_movement_modifier', nodes[1][0])
        self.assertEqual(2, len(nodes))
        self.assertEqual(['hidden_effect'], [k for k, _ in effect_nodes('sb_natal_record_zulu_movement_modifier')])
        receipt = object_block(EVENTS, RECEIPT)
        self.assertIn('hidden = yes', receipt)
        self.assertNotIn('option =', receipt)
        self.assertNotIn('custom_tooltip', object_block(ENTHUSIASM_EFFECT, 'REPLACE:add_movement_enthusiasm_modifier'))


if __name__ == '__main__':
    unittest.main()
