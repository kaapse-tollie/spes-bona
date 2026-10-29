"""Execute live-entry boundaries and named/introduced heirs without simulating an engine war."""
import re
import unittest

from tests.test_zulu_frontier_followup import FrontierRuntime, ROOT, field
from tests.test_zulu_court_politics import EFFECTS, TRIGGERS, character
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import find_object


class HeirRuntime(FrontierRuntime):
    def __init__(self, date=18360101):
        super().__init__()
        self.country['game_date'] = date
        self.country['vars']['sb_prerogative_var'] = 75
        self.used_templates = set()

    def ref(self, key, scope, prev=None):
        if re.fullmatch(r'\d{4}\.\d{1,2}\.\d{1,2}', key):
            y,m,d = map(int,key.split('.'));return y*10000+m*100+d
        return super().ref(key,scope,prev)

    def condition(self, nodes, scope, prev=None):
        for node in nodes:
            k,_,v = node
            if k == 'is_template_used': result = v in self.used_templates
            else: result = super().condition([node],scope,prev)
            if not result:return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes,scope,prev):
            k,_,v = node
            if k == 'create_character':
                template = field(v,'template')
                src = (ROOT/'common/character_templates/sb_zulu_dynasty_characters.txt').read_text(encoding='utf-8-sig')
                body = statements(re.sub(r'\btraits\s*=\s*\{[^}]*\}', '', find_object(src,template)))
                data = dict((n,x) for n,_,x in body)
                age = int(data['age']) if 'age' in data else (scope['game_date']-self.ref(data['birth_date'],scope))//10000
                actor = character(f'child-{self.created}',0,0,alignment=1,age=age)
                actor.update(vars={},template=template,owner=scope,historical=data['historical'],female=data.get('female'))
                scope['characters'].append(actor);self.created+=1;self.used_templates.add(template)
                # Native on_created is local; save_scope_as on creation is the exported handle.
                outer = self.scopes;self.scopes = dict(outer,root=actor)
                try:self.effect(data.get('on_created',[]),actor,scope)
                finally:self.scopes = outer
                self.scopes[field(v,'save_scope_as')] = actor
            elif k == 'set_career_length':scope['career_years'] = int(field(v,'years'))
            elif k == 'sb_institutions_recalculate':self.backing()
            else:super().effect([node],scope,prev)

    def run(self, name):self.effect(EFFECTS[name],self.country)

    def father(self, template, age=42):
        actor = character(template,0,50,alignment=1,age=age)
        actor.update(template=template,owner=self.country)
        actor['vars']['sb_court_home_scope']=self.country
        self.country['members'].append(actor);self.country['characters'].append(actor)
        self.used_templates.add(template)
        return actor


class HeirRelease(unittest.TestCase):
    def test_fecund_has_health_and_popularity_without_direct_prominence(self):
        body = find_object((ROOT/'common/character_traits/sb_character_traits.txt').read_text(encoding='utf-8-sig'),'sb_fecund')
        self.assertIn('character_health_add = 0.05',body)
        self.assertIn('character_popularity_add = 25',body)
        self.assertNotIn('character_prominence_add',body)

    def test_live_profile_boundary_includes_inherited_and_actual_rebel_courts(self):
        for tag,flags,want in (('ZUL',{},True),('NGN',{'sb_ngu_inherited_zul_content_var':1},True),
                               ('NGN',{},False),('FRA',{},False),('rebel',{'sb_institutions_zulu_profile_var':1},True)):
            rt=HeirRuntime();rt.country['id']=tag;rt.country['vars'].update(flags)
            self.assertEqual(want,rt.condition(TRIGGERS['sb_court_dynastic_enabled'],rt.country),tag)
            self.assertNotIn('sb_court_dynasty_test_var',rt.country['vars'])

    def test_unknown_line_creates_one_newborn_and_recognises_same_identity(self):
        rt=HeirRuntime();king=rt.country['ruler'];king['template']='ZUL_gqugqu_claimant'
        rt.run('sb_court_introduce_son');child=rt.country['heir']
        self.assertEqual(0,child['age']);self.assertEqual('no',child['historical'])
        self.assertEqual('SB_ZUL_newborn_son',child['template']);self.assertEqual('no',child['female'])
        self.assertIs(child,king['vars']['sb_court_presented_son_scope'])
        self.assertIs(child,rt.country['vars']['sb_court_recognized_heir_scope'])
        self.assertEqual(25,rt.country['vars']['sb_prerogative_var'])
        self.assertTrue(rt.condition(TRIGGERS['sb_court_living_dynast'],child))
        self.assertTrue(rt.condition(TRIGGERS['sb_court_dynastic_candidate'],child))
        self.assertFalse(rt.condition(TRIGGERS['sb_court_royal_candidate'],child))
        self.assertEqual(0,child['vars']['sb_court_represented_weight_var'])
        child['alive']=False;rt.country['vars']['sb_prerogative_var']=100
        rt.run('sb_court_introduce_son');self.assertEqual(1,rt.created)
        self.assertEqual(100,rt.country['vars']['sb_prerogative_var'])
        # The receipt belongs to the father, not every future ruler of this country.
        successor=rt.father('SB_ZUL_newborn_son');rt.country['ruler']=successor
        rt.run('sb_court_introduce_son');self.assertEqual(2,rt.created)
        self.assertIsNot(child,rt.country['heir'])
        self.assertEqual({},rt.scopes['root']['vars'])

    def test_dingane_keeps_uthumbu_and_known_lines_cannot_buy_replacements(self):
        rt=HeirRuntime();rt.run('sb_court_introduce_son')
        self.assertEqual('ZUL_uthumbu_claimed_son',rt.country['heir']['template'])
        for template in ('ZUL_mpande_zulu','ZUL_cetshwayo_heir','ZUL_dinuzulu_heir'):
            rt=HeirRuntime();rt.country['ruler']['template']=template
            rt.run('sb_court_introduce_son');self.assertEqual(0,rt.created,template)
            self.assertEqual(75,rt.country['vars']['sb_prerogative_var'])

    def test_no_payment_for_insufficient_prerogative_or_unavailable_court(self):
        for change in ('cash','inactive','chiefly','pending','minor'):
            rt=HeirRuntime();rt.country['ruler']['template']='ZUL_gqugqu_claimant'
            if change=='cash':rt.country['vars']['sb_prerogative_var']=49.99
            elif change=='inactive':rt.country['vars'].pop('sb_institutions_active_var')
            elif change=='chiefly':rt.country['laws']={'law_type:law_sb_federated_chiefdoms'}
            elif change=='pending':rt.country['vars']['sb_court_action_open_var']=1
            else:rt.country['vars']['sb_court_minor_sovereign_scope']=rt.country['ruler']
            before=rt.country['vars']['sb_prerogative_var'];rt.run('sb_court_introduce_son')
            self.assertEqual(0,rt.created,change);self.assertEqual(before,rt.country['vars']['sb_prerogative_var'])

    def test_known_birth_dates_no_forced_designation_and_no_resurrection(self):
        for father,child,date in (('ZUL_cetshwayo_heir','ZUL_dinuzulu_heir',18680101),
                                  ('ZUL_dinuzulu_heir','ZUL_solomon_heir',18910101)):
            rt=HeirRuntime(date-1);rt.father(father)
            rt.run('sb_court_introduce_known_children');self.assertEqual(0,rt.created)
            rt.country['game_date']=date;rt.run('sb_court_introduce_known_children')
            born=rt.scopes['sb_court_new_child']
            self.assertEqual(child,born['template']);self.assertEqual(0,born['age'])
            self.assertEqual('yes',born['historical']);self.assertEqual(100,born['career_years'])
            self.assertNotIn('sb_court_recognized_heir_scope',rt.country['vars'])
            self.assertFalse(rt.condition(TRIGGERS['sb_court_dynastic_candidate'],born))
            born['alive']=False;rt.run('sb_court_introduce_known_children');self.assertEqual(1,rt.created)

    def test_absent_dead_foreign_fathers_and_used_templates_do_not_create_children(self):
        for invalid in ('absent','dead','foreign','used','inactive'):
            rt=HeirRuntime(18680101)
            if invalid!='absent':father=rt.father('ZUL_cetshwayo_heir')
            if invalid=='dead':father['alive']=False
            elif invalid=='foreign':father['vars']['sb_court_home_scope']=rt.scopes['root']
            elif invalid=='used':rt.used_templates.add('ZUL_dinuzulu_heir')
            elif invalid=='inactive':rt.country['vars'].pop('sb_institutions_active_var')
            rt.run('sb_court_introduce_known_children');self.assertEqual(0,rt.created,invalid)

    def test_minors_can_be_recognised_without_an_adult_following(self):
        rt=HeirRuntime(18680101);rt.father('ZUL_cetshwayo_heir')
        rt.run('sb_court_introduce_known_children');child=rt.scopes['sb_court_new_child']
        rt.scopes['candidate']=child
        rt.effect(statements('effect = { sb_court_recognize_candidate = { CANDIDATE = scope:candidate } }'),rt.country)
        self.assertIs(child,rt.country['heir']);self.assertEqual(50,rt.country['vars']['sb_prerogative_var'])
        self.assertTrue(rt.condition(TRIGGERS['sb_court_dynastic_candidate'],child))
        self.assertEqual(0,child['vars']['sb_court_represented_weight_var'])
        self.assertEqual({},rt.scopes['root']['vars'])


if __name__=='__main__':unittest.main()
