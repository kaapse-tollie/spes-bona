"""Execute muster scripts; native recruitment/AI/merging still require DP's engine checks."""
import math
import re
import unittest
from pathlib import Path

from tests.test_zulu_contested_crown import (
    ROOT, GAME, court, reserve, answer, split, definitions, VALUES,
)

import tests.test_zulu_contested_crown as claimant


class MusterBehaviour(unittest.TestCase):
    recruitment_states = claimant.ClaimantBehaviour.recruitment_states
    add_staff = claimant.ClaimantBehaviour.add_staff

    def case(self, weights=(300, 200), back_prince=False, regular=4, levies=16):
        rt,king,prince,*_=court(*weights)
        mainland,natal=self.recruitment_states(rt,[(regular,levies),(0,0)])
        self.add_staff(mainland,'soldiers',regular*950,regular*2850)
        self.add_staff(mainland,'officers',regular*50,regular*150)
        self.add_staff(mainland,'peasants',50000,150000)
        self.add_staff(natal,'peasants',200,600)
        reserve(rt,king,prince);answer(rt,back_prince)
        return rt,king,prince,mainland,natal

    def test_one_state_origin_retains_every_native_allocation_for_either_choice(self):
        for back_prince in (False,True):
            rt,king,prince,*_=court(300,200)
            origin,=self.recruitment_states(rt,[(4,16)])
            self.add_staff(origin,'soldiers',2000,6000)
            reserve(rt,king,prince);answer(rt,back_prince)
            self.assertNotIn('sb_court_dynastic_scripted_muster_var',rt.country['vars'])
            self.assertFalse(hasattr(rt,'demolitions'))
            # Native split inputs: two state objects in the same region; their resources
            # are intentionally not the scripted quotas. The script must leave them alone.
            left,right=self.recruitment_states(rt,[(3,9),(1,7)])
            for st in (left,right): st['state_region']='s:STATE_ZULULAND'
            self.add_staff(left,'soldiers',2300,6900)
            self.add_staff(right,'soldiers',1700,5100)
            rt.country['states']=[left]
            _,rebels=split(rt,native_rebel_states=[right])
            for side,st,wanted in ((rt.country,left,(3,9)),(rebels,right,(1,7))):
                self.assertEqual(wanted,tuple(sum(b['level'] for b in st['buildings'] if b['type']==kind)
                    for kind in ('building_barrack','building_conscription_center')))
                self.assertNotIn('sb_court_muster_active_var',side['vars'])
                self.assertNotIn('sb_court_muster_conscription_suspended',side.get('modifiers',{}))
                self.assertIn('sb_court_wartime_provisions',side.get('modifiers',{}))
            self.assertFalse(hasattr(rt,'demolitions'))
            self.assertFalse(hasattr(rt,'pop_moves'))
            rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win')
            self.assertFalse(hasattr(rt,'demolitions'))
            for side in (rt.country,rebels):
                self.assertNotIn('sb_court_wartime_provisions',side.get('modifiers',{}))

    def test_multi_state_levy_snapshot_survives_native_capacity_loss(self):
        for back_prince in (False,True):
            rt,_,_,mainland,natal=self.case(back_prince=back_prince)
            # A native cap truncates the centre during the split; the pre-split budget survives.
            for b in mainland['buildings']:
                if b['type']=='building_conscription_center': b['level']=1
            rt.country['states']=[mainland]
            _,rebels=split(rt,native_rebel_states=[natal])
            self.assertEqual(16,sum(b['level'] for st in (mainland,natal) for b in st['buildings'] if b['type']=='building_sb_court_muster'))
            self.assertFalse(any(b['type']=='building_conscription_center' for st in (mainland,natal) for b in st['buildings']))
            for side in (rt.country,rebels):
                self.assertIn('sb_court_dynastic_scripted_muster_var',side['vars'])
                self.assertIn('sb_court_muster_active_var',side['vars'])
                self.assertIn('sb_court_muster_conscription_suspended',side['modifiers'])
                self.assertIn('sb_court_wartime_provisions',side['modifiers'])
            self.assertFalse(rt.scopes['root'].get('modifiers'))

    def test_civilian_moves_cover_only_deficit_and_keep_the_donors_reserve(self):
        rt,_,_,mainland,natal=self.case()
        before=sum(p['workforce']+p['dependants'] for st in (mainland,natal) for p in st['pops'])
        rt.country['states']=[mainland];_,rebels=split(rt,native_rebel_states=[natal])
        for side in (rt.country,rebels):
            jobs=1200*(side['vars']['sb_court_regular_quota_var']+side['vars']['sb_court_conscript_quota_var'])
            available=sum(p['workforce'] for st in side['states'] for p in st['pops'])
            self.assertGreaterEqual(available,jobs-4)  # Native per-Pop integer rounding.
        self.assertEqual(before,sum(p['workforce']+p['dependants'] for st in (mainland,natal) for p in st['pops']))
        moved=sum(row[3] for row in rt.pop_moves if row[0]=='peasants')
        self.assertGreater(moved,0)
        self.assertLess(moved,9600)
        first=list(rt.pop_moves)
        rt.run('sb_court_rebuild_dynastic_forces');rt.run('sb_court_track_dynastic_war')
        self.assertEqual(first,rt.pop_moves)

    def test_balanced_recruitment_does_not_move_civilians(self):
        rt,king,prince,*_=court(200,200)
        left,right=self.recruitment_states(rt,[(2,8),(2,8)])
        for st in (left,right):
            self.add_staff(st,'peasants',12000,36000)
            self.add_staff(st,'officers',180,540)
        reserve(rt,king,prince);answer(rt)
        rt.country['states']=[left];split(rt,native_rebel_states=[right])
        self.assertFalse(hasattr(rt,'pop_moves'))

    def test_muster_scales_to_workforce_without_consuming_slaves_or_employed_civilians(self):
        rt,king,prince,*_=court()
        left,right=self.recruitment_states(rt,[(4,17),(0,0)])
        self.add_staff(left,'peasants',6000,18000)
        self.add_staff(left,'slaves',100000,300000)
        self.add_staff(left,'laborers',100000,300000)
        reserve(rt,king,prince);answer(rt)
        rt.country['states']=[left];split(rt,native_rebel_states=[right])
        self.assertEqual(1,sum(b['level'] for st in (left,right) for b in st['buildings'] if b['type']=='building_sb_court_muster'))
        self.assertEqual(4,sum(b['level'] for st in (left,right) for b in st['buildings'] if b['type']=='building_barrack'))
        self.assertFalse(any(row[0] in ('slaves','laborers') for row in rt.pop_moves))

    def test_cleanup_after_native_merge_preserves_regulars_construction_and_casualties(self):
        for rebel_wins in (False,True):
            rt,_,_,left,right=self.case()
            rt.country['states']=[left];_,rebels=split(rt,native_rebel_states=[right])
            winner,loser=(rebels,rt.country) if rebel_wins else (rt.country,rebels)
            # Native transfer/merge is supplied explicitly. New regular construction and
            # manpower records must not be overwritten when the temporary type is removed.
            merged={'id':'merged','owner':winner,'vars':{},'buildings':[
                {'type':'building_barrack','level':6,'vars':{},'manpower':1731},
                {'type':'building_sb_court_muster','level':16,'vars':{}},
                {'type':'building_logging_camp','level':4,'vars':{}}]}
            winner['states']=[merged];loser['states']=[]
            rt.run('sb_court_record_dynastic_end');rt.run('sb_court_resolve_dynastic_win',winner)
            self.assertEqual(['building_barrack','building_logging_camp'],[b['type'] for b in merged['buildings']])
            self.assertEqual((6,1731),(merged['buildings'][0]['level'],merged['buildings'][0]['manpower']))
            for side in (winner,loser):
                self.assertNotIn('sb_court_muster_active_var',side['vars'])
                self.assertNotIn('sb_court_dynastic_scripted_muster_var',side['vars'])
                self.assertNotIn('sb_court_muster_conscription_suspended',side['modifiers'])
                self.assertNotIn('sb_court_wartime_provisions',side['modifiers'])
            before=list(rt.demolitions);rt.run('sb_court_demobilise_dynastic_muster',winner)
            self.assertEqual(before,rt.demolitions)

    def test_cancel_before_split_creates_no_muster_and_next_episode_reclassifies(self):
        rt,king,prince,left,right=self.case()
        moves=list(getattr(rt,'pop_moves',[]));rt.run('sb_court_cancel_dynastic_crisis')
        self.assertEqual(moves,getattr(rt,'pop_moves',[]))
        self.assertNotIn('sb_court_dynastic_levies_var',rt.country['vars'])
        rt.run('sb_court_dismiss_dynastic_choice')
        rt.country['states']=[left]
        reserve(rt,king,prince);answer(rt)
        self.assertNotIn('sb_court_dynastic_scripted_muster_var',rt.country['vars'])

    def test_provisioning_is_scoped_to_both_actual_sides_and_cleans_up_an_abandoned_war(self):
        for back_prince in (False,True):
            rt,_,_,left,right=self.case(back_prince=back_prince)
            self.assertNotIn('sb_court_wartime_provisions',rt.country.get('modifiers',{}))
            rt.country['states']=[left];_,rebels=split(rt,native_rebel_states=[right])
            for side in (rt.country,rebels):
                self.assertIn('sb_court_wartime_provisions',side['modifiers'])
            self.assertNotIn('sb_court_wartime_provisions',rt.scopes['root'].get('modifiers',{}))
            # Explicit native disappearance, before a winner callback: the common
            # reconciliation path must remove relief from both stored participants.
            rt.country['wars']=[]
            rt.run('sb_court_reconcile_dynastic_record')
            for side in (rt.country,rebels):
                self.assertNotIn('sb_court_wartime_provisions',side['modifiers'])
            rt.run('sb_court_reconcile_dynastic_record')
            for side in (rt.country,rebels):
                self.assertNotIn('sb_court_wartime_provisions',side['modifiers'])

    def test_largest_recruitment_state_receives_its_own_countrys_available_workers_first(self):
        rt,king,prince,*_=court()
        small,large,rebel=self.recruitment_states(rt,[(1,4),(1,4),(2,8)])
        small['state_population']=10000;large['state_population']=20000;rebel['state_population']=20000
        self.add_staff(small,'peasants',12000,36000)
        self.add_staff(rebel,'peasants',12000,36000)
        reserve(rt,king,prince);answer(rt)
        rt.country['states']=[small,large];_,rebels=split(rt,native_rebel_states=[rebel])
        self.assertTrue(rt.pop_moves)
        self.assertTrue(all(row[1:3]==(small['id'],large['id']) for row in rt.pop_moves))
        self.assertEqual(12000,sum(p['workforce'] for p in large.get('pops',[])))
        self.assertNotIn('pops',rt.scopes['root'])


    def test_multi_state_donor_refills_its_recruitment_state_after_exporting_surplus(self):
        rt,king,prince,*_=court()
        main,hinterland,rebel=self.recruitment_states(rt,[(2,8),(0,0),(2,8)])
        main['state_population']=100000;hinterland['state_population']=90000
        self.add_staff(main,'peasants',12000,36000)
        self.add_staff(hinterland,'peasants',50000,150000)
        reserve(rt,king,prince);answer(rt)
        rt.country['states']=[main,hinterland];_,rebels=split(rt,native_rebel_states=[rebel])
        for side in (rt.country,rebels):
            destination=side['vars']['sb_court_muster_state_scope']
            required=1200*(side['vars']['sb_court_regular_quota_var']+side['vars']['sb_court_conscript_quota_var'])
            self.assertGreaterEqual(sum(p['workforce'] for p in destination.get('pops',[])),required-4)
        self.assertEqual(62000,sum(p['workforce'] for st in (main,hinterland,rebel) for p in st.get('pops',[])))


class MusterContracts(unittest.TestCase):
    def test_provisions_give_partial_relief_without_guaranteeing_an_end_to_starvation(self):
        from tools.check_override_inventory import extract_top_level_blocks
        from tests.test_zulu_institutions_laws import statements,child
        modifiers=definitions('common/static_modifiers/sb_court_dynastic_modifiers.txt')
        fields={k:v for k,_,v in modifiers['sb_court_wartime_provisions']}
        relief=float(fields['state_food_security_add'])
        self.assertEqual(.75,relief)
        self.assertTrue((GAME/fields['icon'].strip('"')).is_file())
        source=(GAME/'common/defines/00_defines.txt').read_text(encoding='utf-8-sig')
        price_range=float(re.search(r'^\s*PRICE_RANGE\s*=\s*([\d.]+)',source,re.M)[1])
        starvation=float(re.search(r'^\s*@starvation_threshold\s*=\s*([\d.]+)',source,re.M)[1])
        packages=extract_top_level_blocks((GAME/'common/buy_packages/00_buy_packages.txt').read_text(encoding='utf-8-sig'))
        food_shares=[]
        for name,body in packages.items():
            if not name.startswith('wealth_'): continue
            goods={k:float(v) for k,_,v in statements(child(body,'goods'))}
            food_shares.append(goods.get('popneed_basic_food',0)/sum(goods.values()))
        # Installed native formula: clamp(1 + modifier - basic-food cost share
        # - shortage severity, 0, 1). This is arithmetic coverage, not engine replay.
        improves = remains_hungry = False
        for food_share in food_shares:
            for price_multiplier in (1-price_range,1,1+price_range):
                for shortage in (0,.5,1):
                    security=max(0,min(1,1+relief-food_share*price_multiplier-shortage))
                    unassisted=max(0,min(1,1-food_share*price_multiplier-shortage))
                    self.assertGreaterEqual(security,unassisted)
                    improves |= security > unassisted
                    remains_hungry |= security < starvation
        self.assertTrue(improves)
        self.assertTrue(remains_hungry)

    def test_temporary_muster_uses_installed_training_without_native_centre_identity(self):
        building=definitions('common/buildings/sb_court_muster.txt')['building_sb_court_muster']
        fields={k:v for k,_,v in building}
        self.assertEqual('yes',fields['recruits_combat_units'])
        self.assertEqual('bg_army',fields['building_group'])
        for key in ('buildable','expandable','downsizeable'): self.assertEqual('no',fields[key])
        self.assertNotIn('has_max_level',fields)
        self.assertIn('pmg_training_conscription',str(fields['production_method_groups']))
        self.assertNotIn('INJECT:building_conscription_center', (ROOT/'common/buildings/sb_court_muster.txt').read_text())

    def test_multiplier_gate_clamps_instead_of_making_negative_capacity(self):
        modifiers=definitions('common/static_modifiers/sb_court_dynastic_modifiers.txt')
        fields={k:v for k,_,v in modifiers['sb_court_muster_conscription_suspended']}
        reduction=float(fields['state_conscription_rate_mult'])
        self.assertNotIn('state_conscription_rate_add',fields)
        # Native CValueCalculator floors multiplicative factors at zero. Positive
        # additions and native uprising rates therefore cannot re-enable conscription.
        for additive in (.01,.04,.4,1.1):
            for bonus in (-.75,0,.25,1,2,5):
                self.assertEqual(0,additive*max(0,1+bonus+reduction))

    def test_training_job_mapping_matches_installed_ratios(self):
        if not GAME.exists(): self.fail('Current-target game is required for muster training contracts')
        from tools.check_override_inventory import extract_top_level_blocks
        from tests.test_zulu_institutions_laws import statements,child
        pms=extract_top_level_blocks((GAME/'common/production_methods/05_military.txt').read_text(encoding='utf-8-sig'))
        pms.update(extract_top_level_blocks((ROOT/'common/production_methods/sb_customary_muster.txt').read_text(encoding='utf-8-sig')))
        mappings={'regular':['pm_no_organization','pm_samurai_training','pm_general_training','pm_advanced_tactics_training','pm_training_streamlining','pm_nco_incorporation','pm_mobile_warfare_tactics'],
                  'levy':['pm_no_organization_conscription','pm_general_training_conscription','pm_advanced_tactics_training_conscription','pm_training_streamlining_conscription','pm_nco_incorporation_conscription','pm_mobile_warfare_tactics_conscription','pm_sb_customary_muster_conscription']}
        rt,*_=court();rt.scopes['sb_court_force_origin']=rt.country
        for service,methods in mappings.items():
            for number,method in enumerate(methods,1):
                rt.country['vars']['sb_court_'+('regular' if service=='regular' else 'conscript')+'_training_var']=number
                ratio={k:float(v) for k,_,v in statements(child(pms[method],'profession_ratio'))}
                self.assertEqual(100,ratio['soldiers']+ratio['officers'])
                self.assertEqual(10*ratio['officers'],rt.calc(VALUES['sb_court_muster_'+service+'_officers'],rt.country))
