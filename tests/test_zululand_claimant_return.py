"""Execute royal handoffs around a destructive annexation boundary; no engine emulation."""
import unittest
from tests.test_zulu_court_politics import CourtRuntime, character, definitions, ROOT
from tests.test_zulu_institutions_laws import statements, child
from tools.check_override_inventory import find_object

SETTLEMENT = definitions('common/scripted_effects/sb_zululand_settlement_effects.txt')
INSTALLERS = definitions('common/scripted_effects/sb_zulu_dynasty_succession_effects.txt')
RETURN_TRIGGER = definitions('common/scripted_triggers/sb_zululand_settlement_triggers.txt')['sb_zululand_can_return_claimant']
ROYAL = find_object((ROOT/'common/political_movements/sb_zulu_constitutional_movements.txt').read_text(encoding='utf-8-sig'), 'movement_sb_zulu_royal')


class RoyalHandoffRuntime(CourtRuntime):
    def __init__(self, natal=True):
        self.king = character('Cetshwayo', 1, 80, 1, 1)
        self.king['template'] = 'ZUL_cetshwayo_heir'
        self.heir = character('Dinuzulu', 0, 25, 0, 1, age=13)
        self.heir['template'] = 'ZUL_dinuzulu_heir'
        super().__init__([self.king, self.heir])
        self.country.update(alive=True, heir=self.heir, characters=[self.king, self.heir])
        self.countries = {'c:ZUL': self.country}
        for tag in ('GBR', 'CAP', 'NAL'):
            self.countries['c:'+tag] = dict(id=tag, vars={}, alive=tag!='NAL' or natal, characters=[], members=[])
        self.britain = self.countries['c:GBR']
        self.natal = self.countries['c:NAL']
        self.scopes = {'root': dict(id='foreign_diplomatic_play', vars={})}
        self.transfers = []

    def ref(self, key, scope, prev=None):
        if key in ('ROOT', 'PREV'): key = key.lower()
        if key.startswith(('ROOT.', 'PREV.')): key = key[:4].lower()+key[4:]
        if key.startswith('c:'):
            tag, _, tail = key.partition('.')
            found = self.countries.get(tag)
            return self.ref(tail, found) if tail and found else found
        if key == 'game_date': return 18810101
        if key.count('.') == 2 and all(p.isdigit() for p in key.split('.')):
            y,m,d = map(int,key.split('.')); return y*10000+m*100+d
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        results = []
        for key, op, value in nodes:
            if key == 'is_country_alive': result = scope['alive'] == (value == 'yes')
            elif key == 'is_template_used': result = True # Cast admission has separate coverage.
            elif key == 'any_scope_character': result = any(self.condition(value,c,scope) for c in scope.get('characters',[]))
            elif key == 'sb_zululand_can_return_claimant':
                result = self.condition(RETURN_TRIGGER, scope, prev) == (value == 'yes')
            elif key == 'sb_zululand_contest_interventions_available': result = getattr(self, 'interventions_open', True) == (value == 'yes')
            elif key == 'sb_chiefs_contest_country': result = (scope is self.country and getattr(self, 'contest_active', False)) == (value == 'yes')
            elif key == 'sb_zululand_trn_is_eligible_participant': result = False
            else: result = super().condition([(key,op,value)],scope,prev)
            results.append(result)
        return all(results)

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes,scope,prev):
            key,op,value = node
            if key in SETTLEMENT or key in INSTALLERS:
                self.effect(SETTLEMENT.get(key,INSTALLERS.get(key)),scope,prev)
            elif key.startswith('c:') or key == 'heir':
                target = self.ref(key,scope,prev)
                if target is not None: self.effect(value,target,scope)
            elif key == 'save_temporary_scope_as': self.scopes[value] = scope
            elif key == 'random_scope_character':
                limit = next((v for k,_,v in value if k == 'limit'),[])
                eligible = [c for c in scope.get('characters',[]) if self.condition(limit,c,scope)]
                if eligible: self.effect([n for n in value if n[0]!='limit'],eligible[0],scope)
            elif key == 'sb_court_ensure_roster':
                self.scopes['sb_court_country'] = scope
                for person in scope.get('characters',[]):
                    person['vars']['sb_court_home_scope'] = scope
                    if not any(person is m for m in scope['members']): scope['members'].append(person)
            elif key == 'exile_character_with_role_cleanup':
                old = scope['owner']
                for role in ('heir','ruler'):
                    if old.get(role) is scope: old.pop(role)
                scope['agitator'] = True
                scope['is_in_exile_pool'] = True
                scope.setdefault('modifiers',{})['in_exile_modifier'] = 1
            elif key == 'transfer_character':
                target = self.ref(value,scope,prev)
                old = scope['owner']
                old['characters'] = [c for c in old['characters'] if c is not scope]
                target['characters'].append(scope)
                scope['owner'] = target
                scope['is_in_exile_pool'] = False
                self.transfers.append((scope['id'],target['id']))
            elif key == 'free_from_exile_effect': scope.setdefault('modifiers',{}).pop('in_exile_modifier',None)
            elif key == 'free_character_from_void': scope['is_in_void'] = False
            elif key == 'add_character_role': scope[value] = True
            elif key == 'set_career_length':
                career = dict((k,v) for k,_,v in value)
                self.assert_role_exists(scope, career['role'])
                scope.setdefault('careers', {})[career['role']] = int(career['years'])
            elif key == 'set_interest_group': scope['interest_group'] = 'ig_landowners'
            elif key == 'cleanup_ruler_character_roles': scope['agitator'] = False
            elif key in ('sb_court_update_heir_blocker','sb_court_release_heir_blocker', 'sb_court_sync_allegiance_traits',
                         'sb_institutions_recalculate','sb_institutions_reconcile'): pass # Separate court suite.
            elif key == 'sb_court_select_chiefly_head': scope['ruler'] = {'id':'Chief', 'owner':scope}
            elif key == 'add_loyalists': scope['loyalist_grants'] = scope.get('loyalist_grants',0)+1
            else: super().effect([node],scope,prev)

    def run(self,name,country=None): self.effect(SETTLEMENT[name],country or self.britain)

    def assert_role_exists(self, person, role):
        assert person.get(role), 'Career must be set after acquiring the role'

    def annex(self):
        # Native country removal destroys locally hosted people, regardless of archive refs.
        for person in self.country['characters']: person['alive'] = False
        self.country['characters'] = []
        self.country['alive'] = False

    def restore_country(self):
        self.country = dict(id='ZUL',vars={},alive=True,characters=[],members=[])
        self.countries['c:ZUL'] = self.country
        generated = character('Generated monarch',0,20)
        generated['owner'] = self.country
        self.country.update(ruler=generated,characters=[generated])
        self.run('sb_zululand_restore_preannexation_royal_house',self.country)


class ClaimantReturnTests(unittest.TestCase):
    def test_partition_successor_is_recognised_without_old_institution_flag(self):
        rt = RoyalHandoffRuntime(); rt.contest_active = True
        rt.king['alive'] = False
        rt.heir['age'] = 21
        rt.country['vars']['sb_court_recognized_heir_scope'] = rt.heir
        rt.effect([('sb_court_refresh_royal_claimant', '=', 'yes')], rt.country)
        self.assertIs(rt.heir, rt.country['vars']['sb_court_restoration_claimant_scope'])
        self.assertNotIn('sb_zululand_usuthu_context_var', rt.country['vars'])

    def test_successor_return_does_not_repeat_reward_and_preserves_foreign_root(self):
        rt = RoyalHandoffRuntime(); rt.contest_active = True
        rt.run('sb_zululand_mark_and_exile_royal_house', rt.natal)
        self.assertEqual([('Dinuzulu', 'CAP'), ('Cetshwayo', 'CAP')], rt.transfers)
        rt.global_vars['sb_zululand_live_zul_scope'] = rt.country
        rt.run('sb_zululand_return_exiled_claimant', rt.natal)
        self.assertEqual(100, rt.king['careers']['agitator'])
        rt.king['alive'] = False
        rt.heir['age'] = 21
        rt.country['vars']['sb_court_recognized_heir_scope'] = rt.heir
        rt.effect([('sb_court_refresh_royal_claimant', '=', 'yes')], rt.country)
        rt.run('sb_zululand_return_exiled_claimant', rt.natal)
        rt.run('sb_zululand_return_exiled_claimant', rt.natal)
        self.assertIs(rt.country, rt.heir['owner'])
        self.assertTrue(rt.heir['agitator'])
        self.assertEqual(100, rt.heir['careers']['agitator'])
        self.assertEqual(1, rt.natal['loyalist_grants'])
        self.assertEqual(1, rt.transfers.count(('Dinuzulu', 'ZUL')))
        self.assertEqual({}, rt.scopes['root']['vars'])

    def test_return_rejects_child_dead_renounced_and_closed_contest(self):
        for invalid in ('child', 'dead', 'renounced', 'closed'):
            with self.subTest(invalid=invalid):
                rt = RoyalHandoffRuntime()
                rt.global_vars['sb_zululand_live_zul_scope'] = rt.country
                rt.country['vars']['sb_court_restoration_claimant_scope'] = rt.heir
                rt.heir['age'] = 21
                if invalid == 'child': rt.heir['age'] = 13
                elif invalid == 'dead': rt.heir['alive'] = False
                elif invalid == 'renounced': rt.heir['vars']['sb_court_claim_renounced_var'] = 1
                else: rt.interventions_open = False
                rt.run('sb_zululand_return_exiled_claimant', rt.natal)
                self.assertEqual([], rt.transfers)
                self.assertNotIn('loyalist_grants', rt.natal)

    def test_exact_pair_survives_annex_partition_and_returns_without_coronation(self):
        for natal_at_start in (False,True):
            with self.subTest(natal=natal_at_start):
                rt = RoyalHandoffRuntime(natal_at_start)
                rt.run('sb_british_shelter_preannex_zulu_royals')
                self.assertEqual([('Dinuzulu','GBR'),('Cetshwayo','GBR')],rt.transfers)
                rt.annex()
                rt.natal['alive'] = True
                rt.run('sb_british_transfer_preannex_zulu_royal_house_to_natal')
                rt.restore_country()
                self.assertIs(rt.king,rt.country['ruler']); self.assertIs(rt.heir,rt.country['heir'])
                self.assertTrue(rt.king['alive']); self.assertTrue(rt.heir['alive'])
                self.assertNotIn('in_exile_modifier',rt.king['modifiers'])
                rt.run('sb_zululand_mark_and_exile_royal_house',rt.natal)
                self.assertIs(rt.king,rt.country['vars']['sb_court_restoration_claimant_scope'])
                self.assertIs(rt.countries['c:CAP'],rt.king['owner'])
                self.assertIs(rt.countries['c:CAP'],rt.heir['owner'])
                rt.global_vars['sb_zululand_live_zul_scope'] = rt.country
                rt.run('sb_zululand_return_exiled_claimant',rt.natal)
                rt.run('sb_zululand_return_exiled_claimant',rt.natal)
                self.assertIs(rt.country,rt.king['owner']); self.assertTrue(rt.king['agitator'])
                self.assertEqual('Chief',rt.country['ruler']['id'])
                self.assertEqual(1,rt.natal['loyalist_grants'])
                self.assertEqual({},rt.scopes['root']['vars'])

    def test_reference_only_archive_does_not_keep_a_person_alive(self):
        rt = RoyalHandoffRuntime()
        rt.run('sb_british_archive_preannex_zulu_royal_house')
        rt.annex()
        self.assertFalse(rt.king['alive']); self.assertFalse(rt.heir['alive'])

    def test_enforcement_refreshes_a_legitimate_wartime_succession_once(self):
        rt = RoyalHandoffRuntime()
        rt.run('sb_british_archive_preannex_zulu_royal_house')
        old = rt.king; old['alive'] = False
        rt.country['ruler'] = rt.heir
        rt.country.pop('heir')
        rt.run('sb_british_shelter_preannex_zulu_royals')
        rt.run('sb_british_shelter_preannex_zulu_royals')
        self.assertEqual([('Dinuzulu','GBR')],rt.transfers)
        self.assertIs(rt.heir,rt.britain['vars']['sb_british_zulu_preannex_ruler_scope_var'])
        self.assertNotIn('sb_british_zulu_preannex_heir_scope_var',rt.britain['vars'])
        self.assertFalse(old['alive'])

    def test_reversed_enforcement_restores_only_a_sheltered_pair_without_natal(self):
        for enforced in (False,True):
            rt = RoyalHandoffRuntime(natal=False)
            rt.run('sb_british_archive_preannex_zulu_royal_house')
            if enforced: rt.run('sb_british_shelter_preannex_zulu_royals')
            replacement = dict(id='legitimate successor',owner=rt.country)
            rt.country['ruler'] = replacement
            rt.run('sb_british_return_sheltered_zulu_royals')
            rt.run('sb_british_return_sheltered_zulu_royals')
            self.assertIs(rt.king if enforced else replacement,rt.country['ruler'])
            if enforced:
                self.assertIs(rt.heir,rt.country['heir'])
                self.assertEqual(4,len(rt.transfers))
            self.assertNotIn('sb_british_zulu_royals_sheltered_var',rt.britain['vars'])

    def test_dead_sheltered_king_is_not_recreated(self):
        rt = RoyalHandoffRuntime()
        rt.run('sb_british_shelter_preannex_zulu_royals')
        rt.king['alive'] = False
        rt.annex()
        rt.run('sb_british_transfer_preannex_zulu_royal_house_to_natal')
        rt.restore_country()
        self.assertEqual('Generated monarch',rt.country['ruler']['id'])
        self.assertIs(rt.heir,rt.country['heir'])
        self.assertFalse(rt.king['alive'])

    def test_only_exact_restoration_claimant_gets_movement_priority(self):
        rt = RoyalHandoffRuntime()
        rt.country['vars'].update(sb_zululand_usuthu_contest_var=1,sb_court_restoration_claimant_scope=rt.king)
        weight = statements(child(ROYAL,'character_support_weight'))
        self.assertEqual(100000,rt.calc(weight,rt.king))
        self.assertEqual(200,rt.calc(weight,rt.heir))
        rt.country['vars']['sb_court_dynastic_crisis_var'] = 1
        self.assertEqual(200,rt.calc(weight,rt.king)) # Dedicated claimant-war movement retains priority.
        rt.country['vars'].pop('sb_court_dynastic_crisis_var')
        rt.king['owner'] = rt.countries['c:CAP']
        self.assertEqual(200,rt.calc(weight,rt.king))
        rt.king['owner'] = rt.country
        rt.country['vars'].pop('sb_zululand_usuthu_contest_var')
        self.assertEqual(200,rt.calc(weight,rt.king))
        returned = SETTLEMENT['sb_zululand_return_exiled_claimant']
        def flatten(nodes):
            for key,_,value in nodes:
                yield key
                if isinstance(value,list): yield from flatten(value)
        operations=list(flatten(returned))
        self.assertLess(operations.index('sb_court_align_royal'),operations.index('transfer_character'))

    def test_archive_copy_reads_britain_even_with_a_conflicting_foreign_root(self):
        rt = RoyalHandoffRuntime()
        rt.run('sb_british_archive_preannex_zulu_royal_house')
        rt.scopes['root']['vars']['sb_british_zulu_preannex_ruler_scope_var'] = rt.heir
        rt.run('sb_british_transfer_preannex_zulu_royal_house_to_natal')
        self.assertIs(rt.king,rt.natal['vars']['sb_zululand_preannexation_ruler_scope_var'])
        self.assertIs(rt.heir,rt.natal['vars']['sb_zululand_preannexation_heir_scope_var'])
        self.assertIs(rt.heir,rt.scopes['root']['vars']['sb_british_zulu_preannex_ruler_scope_var'])

    def test_shelter_and_rollback_are_on_actual_enforcement_and_survivor_paths(self):
        hook = find_object((ROOT/'common/war_goal_types/zz_sb_zululand_annex_handoff.txt').read_text(encoding='utf-8-sig'),'annex_country',directive='REPLACE')
        self.assertIn('sb_british_shelter_preannex_zulu_royals = yes',child(hook,'on_enforced'))
        final = definitions('common/scripted_effects/sb_natal_interwar_effects.txt')['sb_british_zulu_finalize_bound_annex']
        outer = next(v for k,_,v in final if k=='if')
        survivor = next(v for k,_,v in outer if k=='if')
        self.assertIn(('sb_british_return_sheltered_zulu_royals','=','yes'),survivor)
        keys = [k for k,_,_ in survivor]
        self.assertLess(keys.index('sb_british_return_sheltered_zulu_royals'),keys.index('sb_british_clear_preannex_zulu_royal_house'))
