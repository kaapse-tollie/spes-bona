"""Script-derived appointment scope/lifetime checks; DP verifies engine timing."""
import re
import unittest

from tools import validate
from tests.test_natal_zululand_gameplay_contract import (
    object_block, object_block_from_source, named_option, without_comments,
)

BOER = 'common/scripted_effects/sb_boer_commandant_effects.txt'
NATAL = 'common/scripted_effects/sb_natalia_effects.txt'
TREK = 'common/scripted_effects/sb_trek_migration.txt'
NAMIBIA = 'common/scripted_effects/sb_namibia_effects.txt'
GUARD = 'keep_current_ruler_var'


def guard_writes(source, current, event_root):
    """Resolve the actual enclosing country references, retaining foreign ROOT."""
    source = without_comments(source)
    writes = []
    for match in re.finditer(r'\bset_variable\s*=\s*\{', source):
        assignment = validate.extract_braced(source, match.start())
        if not re.search(rf'\bname\s*=\s*{GUARD}\b', assignment):
            continue
        holder = current
        for scope in re.finditer(
            r'\b(root|this|c:\w+|ruler|heir|random_scope_character|every_scope_character)'
            r'\s*\??=\s*\{', source[:match.start()]
        ):
            enclosing = validate.extract_braced(source, scope.start())
            if scope.start() + len(enclosing) <= match.start():
                continue
            reference = scope.group(1)
            if reference == 'root':
                holder = event_root
            elif reference.startswith('c:'):
                holder = reference[2:]
            elif reference != 'this':
                holder = 'character'
        days = re.search(r'\bdays\s*=\s*(\d+)\b', assignment)
        writes.append((holder, int(days[1]) if days else None))
    return writes


class ScriptedRulerRetentionTests(unittest.TestCase):
    def assert_protected(self, source, current, target):
        for event_root in ('GBR', 'ZUL', 'diplomatic_play_123'):
            self.assertEqual([(target, 7)], guard_writes(source, current, event_root),
                             f'foreign ROOT = {event_root}')
        self.assertNotIn(f'remove_variable = {GUARD}', source)

    def test_boer_refresh_keeps_protection_after_both_law_changes(self):
        refresh = object_block(BOER, 'sb_refresh_boer_commandant_general_government')
        self.assert_protected(refresh, 'NAL', 'NAL')
        self.assertLess(refresh.index(GUARD), refresh.index('activate_law ='))
        self.assertIn('NOT = { has_government_type = gov_boer_commandant_general_republic }', refresh)

    def test_named_boer_founders_protect_the_recipient_before_setup(self):
        cases = (
            (NATAL, 'sb_found_natalia_peacefully', 'NAL', 'sb_apply_natalia_boer_republic_setup'),
            (NATAL, 'sb_found_natalia_after_blood_river', 'NAL', 'sb_apply_natalia_blood_river_military_setup'),
            (TREK, 'sb_spawn_transvaal_republic_v2', 'TRN', 'effect_starting_politics_conservative'),
            (TREK, 'sb_found_zoutpansberg_republic', 'ZPB', 'sb_apply_boer_republic_spawn_setup'),
            (TREK, 'sb_found_lydenburg_republic', 'LYD', 'sb_apply_boer_republic_spawn_setup'),
            ('common/scripted_effects/sb_bechuanaland_corridor_effects.txt',
             'sb_bechuanaland_setup_sgo_frontier_drive', 'SGO', 'sb_apply_boer_republic_spawn_setup'),
        )
        for path, name, recipient, setup in cases:
            with self.subTest(founder=name):
                source = object_block(path, name)
                self.assert_protected(source, 'ORA', recipient)
                self.assertLess(source.index(GUARD), source.index(setup + ' = yes'))
        guns = object_block(NATAL, 'sb_found_natalia_after_guns_bargain_rejection')
        self.assertIn('sb_found_natalia_peacefully = yes', guns)

    def test_vryheid_protects_the_founder_before_it_commissions_its_ruler(self):
        path = 'common/scripted_effects/sb_zululand_settlement_effects.txt'
        appointment = object_block(path, 'sb_nrp_install_founding_commandant')
        self.assert_protected(appointment, 'NRP', 'NRP')
        self.assertLess(appointment.index(GUARD), appointment.index('create_character ='))
        setup = object_block(path, 'sb_nrp_apply_boer_republic_setup')
        self.assertLess(setup.index('sb_nrp_install_founding_commandant'), setup.index('sb_apply_boer_republic_spawn_setup'))

    def test_albany_guards_the_colony_for_transferred_and_created_godlonton(self):
        option = named_option(object_block('events/sb_cape_events.txt', 'sb_cape.200'),
                              'sb_cape.200.a')
        self.assert_protected(option, 'GBR', 'ABY')
        for operation in ('create_diplomatic_pact =', 'set_character_as_ruler =',
                          'template = ABY_robert_godlonton'):
            self.assertLess(option.index(GUARD), option.index(operation))

    def test_swa_protection_is_inside_german_appointment_before_final_laws(self):
        install = object_block(NAMIBIA, 'sb_nam_assign_german_swa_ruler')
        self.assert_protected(install, 'GER', 'SWA')
        self.assertIn('country_definition = cd:GER', object_block_from_source(install, 'limit'))
        self.assertLess(install.index(GUARD), install.index('game_date < 1891.1.1'))
        finalizer = object_block(NAMIBIA, 'sb_nam_finalize_swa_administration')
        self.assertLess(finalizer.index('sb_nam_assign_german_swa_ruler = yes'),
                        finalizer.index('sb_nam_apply_swa_administration_package = yes'))
        self.assertNotIn(GUARD, finalizer)  # Generic, non-German colonies stay native.

    def test_klip_protection_belongs_to_klr_even_from_zulu_event_root(self):
        create = object_block('common/scripted_effects/sb_klip_river_county_effects.txt',
                              'sb_klip_river_create_county')
        self.assert_protected(create, 'NAL', 'KLR')
        self.assertLess(create.index(GUARD), create.index('effect_starting_politics_conservative'))

    def test_guard_scope_checks_reject_foreign_root_and_character_holder(self):
        assignment = f'set_variable = {{ name = {GUARD} days = 7 }}'
        self.assertEqual([('GBR', 7)], guard_writes(f'root = {{ {assignment} }}', 'NAL', 'GBR'))
        self.assertEqual([('character', 7)], guard_writes(f'ruler = {{ {assignment} }}', 'NAL', 'GBR'))

    def test_unrelated_governance_and_zulu_paths_get_no_blanket_guard(self):
        for path, name in (
            (BOER, 'sb_apply_boer_commandant_general_baseline'),
            (BOER, 'sb_apply_boer_republic_spawn_setup'),
            (NATAL, 'sb_restore_natalia_after_boer_corridor_victory'),
            ('common/scripted_effects/sb_subject_autonomy_effects.txt',
             'sb_apply_responsible_colony_governance_from_overlord'),
            ('common/scripted_effects/sb_zululand_settlement_effects.txt', 'sb_zululand_mark_and_exile_royal_house'),
            ('common/scripted_effects/sb_zululand_settlement_effects.txt', 'sb_zululand_finalize_political_contest'),
            ('events/sb_boer_republics_events.txt', 'sb_boer_republics.130'),
        ):
            with self.subTest(effect=name):
                self.assertNotIn(GUARD, object_block(path, name))


if __name__ == '__main__':
    unittest.main()
