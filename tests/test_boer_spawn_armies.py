"""Founding order prevents commanders from generating a spare empty army.

These inspect the actual script paths; DP verifies automatic formation behavior.
"""
import unittest

from tests.test_1_14_story_war_routes import (
    object_block, object_block_from_source, nested_blocks,
)

NATAL = 'common/scripted_effects/sb_natalia_effects.txt'
TREK = 'common/scripted_effects/sb_trek_migration.txt'
BOER = 'common/scripted_effects/sb_boer_commandant_effects.txt'


class BoerSpawnArmyTests(unittest.TestCase):
    def test_blood_river_army_precedes_transferred_or_new_pretorius(self):
        source = object_block(NATAL, 'sb_found_natalia_after_blood_river')
        muster = source.index('sb_apply_natalia_blood_river_military_setup = yes')
        for effect in ('sb_receive_boer_founder =', 'set_character_as_ruler = yes',
                       'sb_apply_natalia_boer_republic_setup = yes'):
            self.assertLess(muster, source.index(effect))
        natal = nested_blocks(source, 'c:NAL ?')
        self.assertIn('sb_apply_natalia_blood_river_military_setup = yes', natal[0])
        setup = next(block for block in natal
                     if 'sb_apply_natalia_boer_republic_setup = yes' in block)
        self.assertIn('transfer_to_formation = scope:sb_natalia_commando_scope', setup)
        self.assertGreater(source.index('transfer_to_formation'), source.index('sb_receive_boer_founder'))

    def test_peaceful_and_guns_routes_muster_before_retief_or_generic_ruler(self):
        source = object_block(NATAL, 'sb_found_natalia_peacefully')
        natal = object_block_from_source(source, 'c:NAL ?')
        for muster in ('sb_apply_natalia_blood_river_military_setup = yes',
                       'create_military_formation ='):
            for commission in ('sb_apply_natalia_boer_republic_setup = yes',
                               'transfer_character = c:NAL', 'create_character ='):
                self.assertLess(natal.index(muster), natal.index(commission))
        self.assertEqual(1, natal.count('transfer_to_formation = scope:sb_natalia_commando_scope'))
        self.assertGreater(natal.index('transfer_to_formation'), natal.index('add_character_role = general'))
        guns = object_block(NATAL, 'sb_found_natalia_after_guns_bargain_rejection')
        self.assertIn('sb_found_natalia_peacefully = yes', guns)

    def test_transvaal_package_precedes_commissioning_and_cleanup_stays_last(self):
        spawn = object_block(TREK, 'sb_spawn_transvaal_republic_v2')
        for commission in ('sb_apply_boer_republic_spawn_setup = yes', 'create_character =',
                           'sb_receive_boer_founder ='):
            self.assertLess(spawn.index('sb_seed_trn_v2_start_package = yes'), spawn.index(commission))
        package = object_block(TREK, 'sb_seed_trn_v2_start_package')
        self.assertIn('create_military_formation =', package)
        self.assertNotIn('sb_receive_boer_founder', package)
        self.assertNotIn('add_character_role = general', package)
        self.assertIn('NOT = { has_variable = sb_trn_starting_commando_created_var }', package)
        # Assign the founding commandants only after the historical cast arrives.
        self.assertGreater(spawn.index('transfer_to_formation = scope:trn_pretorius_commando_scope'),
                           spawn.rindex('sb_receive_boer_founder ='))
        assignments = next(block for block in nested_blocks(spawn, 'if')
                           if 'limit = { exists = scope:trn_pretorius_commando_scope }' in block)
        self.assertIn('has_template = TRN_andries_pretorius', assignments)
        self.assertIn('has_template = ORA_hendrik_potgieter', assignments)
        self.assertNotIn('TRN_marthinus_wessel_pretorius', assignments)
        self.assertGreater(spawn.index('sb_cleanup_trn_generated_commanders = yes'),
                           spawn.rindex('sb_receive_boer_founder ='))

    def test_zoutpansberg_and_lydenburg_muster_before_baseline_commissions_ruler(self):
        setup = object_block(BOER, 'sb_apply_boer_republic_spawn_setup')
        self.assertLess(setup.index('sb_ensure_boer_republic_starting_commando = yes'),
                        setup.index('sb_apply_boer_commandant_general_baseline = yes'))
        muster = object_block(BOER, 'sb_ensure_boer_republic_starting_commando')
        self.assertIn('army_size <= 0', muster)
        for tag, name in (('ZPB', 'zoutpansberg_commando'), ('LYD', 'lydenburg_commando')):
            self.assertIn(f'country_definition = cd:{tag}', muster)
            self.assertIn(f'name = {name}', muster)

    def test_natal_military_helper_defers_commander_assignment_and_keeps_units(self):
        muster = object_block(NATAL, 'sb_apply_natalia_blood_river_military_setup')
        self.assertNotIn('transfer_to_formation', muster)
        self.assertLess(muster.index('remove_building = building_conscription_center'),
                        muster.index('create_military_formation ='))
        units = nested_blocks(muster, 'combat_unit')
        self.assertEqual(2, len(units))
        for unit, kind in zip(units, ('irregular_infantry', 'dragoons')):
            self.assertIn(f'type = unit_type:combat_unit_type_{kind}', unit)
            self.assertIn('count = 1', unit)


if __name__ == '__main__':
    unittest.main()
