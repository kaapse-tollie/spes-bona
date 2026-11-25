"""Exercise the replacement handoff; native deletion/recruitment remain DP-tested."""
from copy import deepcopy
import unittest
from decimal import Decimal

from tests.test_klip_punitive_protectorate import (
    evaluate, expression, run_effect, subjugate, world, ZUL_EFFECTS, game_day,
)
from tests.test_natal_zululand_gameplay_contract import object_block, object_block_from_source, text, ROOT
from tests.test_1_14_3_compatibility import tokens
from tools.check_override_inventory import find_object
from tests.test_performance_pass import canonical_trigger
from tests.test_zulu_institutions_laws import child, statements

CHOICE = 'sb_zululand_choose_direct_natal_administration'
INITIAL = 'initial_movement_enthusiasm'
INITIAL_EXPIRY = 'sb_natal_zulu_initial_enthusiasm_until_var'
ANNEXATION = 'sb_zululand_annexation_movement_attraction'
OLD_GRANT = 'sb_zulu_national_movement_initial_enthusiasm_var'
DISBAND = 'sb_natal_zulu_movement_replace_var'
PENDING = 'sb_natal_zulu_movement_replacement_pending_var'
RECEIPT = 'sb_natal_interwar.031'
OVERRIDE = 'common/political_movements/zz_sb_cultural_minority_movement_override.txt'
EVENTS = 'events/sb_natal_interwar_events.txt'


def movement(owner='NAL', culture='cu:zulu', kind='movement_cultural_minority', enthusiasm=True):
    start = game_day('1839.10.27')
    tracked = enthusiasm and (owner, culture, kind) == ('NAL', 'cu:zulu', 'movement_cultural_minority')
    return {'owner': owner, 'culture': culture, 'type': kind,
            'flags': {INITIAL_EXPIRY} if tracked else set(),
            'variables': {INITIAL_EXPIRY: Decimal(start + 7300)} if tracked else {},
            'modifiers': {INITIAL: {'start': start, 'end': start + 7300,
                                    'multiplier': Decimal(1), 'decaying': True}} if enthusiasm else {},
            'identity': 'existing', 'supporters': [11, 23], 'activism': 0.3}


def annexation(existing=True, old_grant=True):
    state = world()
    state['flags'] = {OLD_GRANT} if old_grant else set()
    subjugate(state)
    state['date'] = '1850.6.6'
    state['movements'] = [movement()] if existing else []
    return state


def disband_rule():
    rule = object_block(OVERRIDE, 'disband_trigger')
    return 'AND', expression(object_block_from_source(rule, 'AND'))


def native_disband(state, old):
    """Supply native ordering explicitly: on_disbanded runs before deletion."""
    run_effect(None, state, actor=old, root=old,
               nodes=expression(object_block(OVERRIDE, 'on_disbanded')))
    state['movements'].remove(old)


def deliver(state, actor='NAL'):
    event = dict(expression(object_block(EVENTS, RECEIPT)))
    if evaluate(event['trigger'], state, actor=actor):
        run_effect(None, state, actor=actor, root=actor, nodes=event['immediate'])


class ZuluAnnexationMovementTests(unittest.TestCase):
    def test_existing_movement_is_marked_for_replacement_after_annexation(self):
        state = annexation()
        old = state['movements'][0]
        run_effect(CHOICE, state)
        self.assertIn(DISBAND, old['flags'])
        self.assertEqual('NAL', state['zululand_owner'])
        self.assertEqual([old], state['movements'])
        self.assertEqual([], state['events'])  # Wait for native deletion, not a guessed delay.

    def test_early_and_late_existing_movement_get_one_fresh_instance(self):
        for enthusiasm in (True, False):
            for old_grant in (True, False):
                with self.subTest(enthusiasm=enthusiasm, old_grant=old_grant):
                    state = annexation(old_grant=old_grant)
                    old = state['movements'][0] = movement(enthusiasm=enthusiasm)
                    run_effect(CHOICE, state)
                    self.assertTrue(evaluate([disband_rule()], state, actor=old))
                    native_disband(state, old)
                    self.assertEqual([], state['movements'])
                    self.assertEqual([(RECEIPT, 'NAL')], [e[:2] for e in state['events']])
                    state = deepcopy(state)  # Pending receipt survives save/reload.
                    state['date'] = '1850.6.17'
                    deliver(state)
                    self.assertEqual(1, len(state['movements']))
                    new = state['movements'][0]
                    self.assertIsNot(old, new)
                    self.assertEqual(('NAL', 'movement_cultural_minority', 'cu:zulu'),
                                     tuple(new[k] for k in ('owner', 'type', 'culture')))
                    self.assertEqual({ANNEXATION, INITIAL} if enthusiasm else {ANNEXATION},
                                     set(new['modifiers']))
                    self.assertEqual(game_day('1850.6.17') + 7300, new['modifiers'][ANNEXATION]['end'])
                    if enthusiasm:
                        self.assertEqual(old['modifiers'][INITIAL]['end'], new['modifiers'][INITIAL]['end'])
                    self.assertFalse(evaluate([disband_rule()], state, actor=new))
                    self.assertNotIn(PENDING, state['flags'])
                    self.assertIn(OLD_GRANT, state['flags'])

    def test_absent_movement_is_created_immediately_despite_old_country_marker(self):
        for old_grant in (True, False):
            state = annexation(existing=False, old_grant=old_grant)
            run_effect(CHOICE, state)
            self.assertEqual(1, len(state['movements']))
            self.assertEqual({ANNEXATION}, set(state['movements'][0]['modifiers']))
            self.assertEqual([], state['events'])
            self.assertNotIn(PENDING, state['flags'])

    def test_foreign_root_and_unrelated_movements_do_not_receive_the_package(self):
        for root in ('NAL', 'ZUL', 'GBR', 'diplomatic_play_123'):
            for existing in (True, False):
                with self.subTest(root=root, existing=existing):
                    state = annexation(existing=existing)
                    others = [movement(owner='GBR'), movement(culture='cu:xhosa'),
                              movement(kind='movement_royalist_absolutist')]
                    before = deepcopy(others)
                    old = state['movements'][0] if existing else None
                    state['movements'].extend(others)
                    run_effect(CHOICE, state, actor='NAL', root=root)
                    if old:
                        native_disband(state, old)
                        deliver(state)
                    self.assertEqual(before, others)
                    self.assertEqual(4, len(state['movements']))
                    self.assertFalse(state['zulu_alive'])

    def test_disband_hook_ignores_other_countries_cultures_and_unmarked_deaths(self):
        for owner, culture, marked in (('GBR', 'cu:zulu', True),
                                       ('NAL', 'cu:xhosa', True), ('NAL', 'cu:zulu', False)):
            state = annexation(existing=False)
            old = movement(owner=owner, culture=culture)
            if marked:
                old['flags'].add(DISBAND)
            state['movements'] = [old]
            self.assertFalse(evaluate([disband_rule()], state, actor=old))
            native_disband(state, old)
            self.assertEqual([], state['events'])
            self.assertNotIn(PENDING, state['flags'])

    def test_duplicate_delivery_and_later_death_never_refresh_or_revive(self):
        state = annexation()
        old = state['movements'][0]
        run_effect(CHOICE, state)
        native_disband(state, old)
        deliver(state)
        before = deepcopy(state['movements'])
        state['date'] = '1851.6.6'
        deliver(state)
        run_effect(CHOICE, state)
        run_effect('sb_natal_create_zulu_national_movement', state)
        self.assertEqual(before, state['movements'])
        state['events'].clear()
        native_disband(state, state['movements'][0])
        deliver(state)
        run_effect(CHOICE, state)
        self.assertEqual([], state['movements'])
        self.assertEqual([], state['events'])

    def test_native_recreation_between_deletion_and_receipt_is_not_duplicated(self):
        state = annexation()
        old = state['movements'][0]
        run_effect(CHOICE, state)
        native_disband(state, old)
        new = movement(enthusiasm=False)
        state['movements'].append(new)
        deliver(state)
        self.assertEqual([new], state['movements'])
        self.assertEqual({INITIAL, ANNEXATION}, set(new['modifiers']))
        self.assertNotIn(DISBAND, new['flags'])

    def test_override_preserves_cmf_outside_natal_hooks_and_garrison_exclusion(self):
        cmf = ROOT.parent / 'Community Mod Framework/common/political_movements/ycom_02_cultural_movement.txt'
        source = cmf.read_text(encoding='utf-8-sig')  # Current dependency is mandatory.
        native = find_object(source, 'movement_cultural_minority', directive='REPLACE')
        sb = find_object(text(OVERRIDE), 'movement_cultural_minority', directive='REPLACE')
        self.assertNotIn('on_disbanded', native)
        added = object_block_from_source(object_block(OVERRIDE, 'disband_trigger'), 'AND')
        self.assertEqual(1, sb.count(added))
        sb = sb.replace(added, '').replace(object_block(OVERRIDE, 'on_disbanded'), '')
        sb = sb.replace('NOT = { has_ideology = ideology:ideology_sb_anglo_colonialism }', '', 1)
        # Same neighbour predicate, cheap insurrection check before culture lookup.
        old_filter = child(child(native, 'additional_radicalism_factors'), 'any_political_movement')
        new_filter = child(child(sb, 'additional_radicalism_factors'), 'any_political_movement')
        self.assertEqual(canonical_trigger(statements(old_filter)), canonical_trigger(statements(new_filter)))
        self.assertEqual(tokens(native.replace(old_filter, new_filter)), tokens(sb))

    def test_receipt_is_hidden_delayed_and_has_no_recurring_dispatch(self):
        callback = object_block(OVERRIDE, 'on_disbanded')
        self.assertIn('trigger_event = { id = ' + RECEIPT + ' days = 1 }', callback)
        event = dict(expression(object_block(EVENTS, RECEIPT)))
        self.assertEqual('yes', event['hidden'])
        self.assertNotIn('option', event)
        self.assertEqual(('remove_variable', PENDING), event['immediate'][0])
        choice = object_block(ZUL_EFFECTS, CHOICE)
        self.assertLess(choice.index('annex = c:ZUL'), choice.index(DISBAND))
        callers = [p for folder in ('common', 'events') for p in (ROOT / folder).rglob('*.txt')
                   if 'id = ' + RECEIPT in p.read_text(encoding='utf-8-sig')]
        self.assertEqual([ROOT / OVERRIDE], callers)


if __name__ == '__main__':
    unittest.main()
