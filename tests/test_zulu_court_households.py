"""House aggregation and court presentation; actual GUI/native callbacks remain DP checks."""
from pathlib import Path
import unittest
from tests.test_zulu_court_rework import ReworkRuntime, court
from tests.test_zulu_court_politics import character, EFFECTS, ACTIONS, TRIGGERS, GAME
from tools.check_override_inventory import find_object

ROOT=Path(__file__).resolve().parents[1]


class CourtHouseholds(unittest.TestCase):
    def attach(self,rt,actor):
        actor['owner']=rt.country
        actor['vars']['sb_court_home_scope']=rt.country
        rt.country['members'].append(actor)
        return actor

    def test_summed_house_switches_leader_without_penalty_lock_or_double_count(self):
        rt,king,prince,head=court()
        junior=self.attach(rt,character('junior',10,48))
        junior['vars']['sb_court_successor_pledge_scope']=prince
        for _ in range(3):
            rt.backing()
            self.assertEqual(88,head['vars']['sb_court_represented_weight_var'])
            self.assertEqual([junior],head['sb_court_house_members'])
            self.assertEqual([head],prince['sb_court_supporters'])
            self.assertEqual(173,prince['vars']['sb_court_coalition_weight_var'])
        junior['prominence']=51
        for _ in range(3):
            rt.backing()
            self.assertIn('sb_court_house_leader_var',junior['vars'])
            self.assertNotIn('sb_court_house_leader_var',head['vars'])
            self.assertNotIn('sb_court_junior_status',junior['modifiers'])
            self.assertEqual(91,junior['vars']['sb_court_represented_weight_var'])
            self.assertEqual([head],junior['sb_court_house_members'])
            self.assertEqual([junior],prince['sb_court_supporters'])
            self.assertEqual(226,rt.country['vars']['sb_court_weight_var'])

    def test_two_princes_and_unaffiliated_councillor_partition_the_total(self):
        rt,_,mpande,head=court()
        rival=self.attach(rt,character('Gqugqu',0,15,-1,1))  # 15 + 25 claimant = 40
        rival['template']='ZUL_gqugqu_claimant'
        rival['vars']['sb_court_claimant_scope']=rival
        outsider=self.attach(rt,character('councillor',0,40))
        rt.backing()
        self.assertEqual(255,rt.country['vars']['sb_court_weight_var'])
        self.assertEqual(175,rt.country['vars']['sb_court_pledged_weight_var'])
        self.assertEqual(80,rt.country['vars']['sb_court_unpledged_weight_var'])
        self.assertEqual(30,outsider['vars']['sb_court_represented_weight_var'])
        self.assertNotIn('sb_court_house_leader_var',outsider['vars'])
        self.assertEqual(135,mpande['vars']['sb_court_coalition_weight_var'])
        self.assertEqual(40,rival['vars']['sb_court_coalition_weight_var'])
        self.assertAlmostEqual(100,sum(p['vars']['sb_court_pledged_share_var'] for p in [mpande,rival]))
        self.assertEqual({},rt.scopes['root']['vars'])

    def test_house_recruitment_excludes_each_native_agitator_contribution(self):
        rt,king,prince,head=court()
        head['vars']['sb_court_alignment_var']=1
        junior=self.attach(rt,character('junior',10,40,alignment=1,agitator=True))
        rt.backing()
        self.assertEqual(80,head['vars']['sb_court_represented_weight_var'])
        self.assertEqual(50,head['vars']['sb_court_attraction_weight_var'])
        self.assertEqual(185,rt.country['vars']['sb_court_royal_weight_var'])
        head['agitator']=True
        junior['agitator']=False
        rt.backing()
        self.assertEqual(80,head['vars']['sb_court_represented_weight_var'])
        self.assertEqual(30,head['vars']['sb_court_attraction_weight_var'])
        self.assertEqual(165,rt.country['vars']['sb_court_royal_weight_var'])
        self.assertEqual(165,prince['vars']['sb_court_coalition_weight_var'])

    def test_bonus_excludes_minors_is_not_stacked_and_ends_on_accession_or_exit(self):
        rt,king,prince,_=court()
        for _ in range(3):rt.backing()
        self.assertEqual(prince['prominence'] + 25,rt.ref('prominence',prince))
        self.assertIn('sb_court_claimant_trait',prince['traits'])
        self.assertNotIn('sb_court_royal_claim',prince.get('modifiers',{}))
        minor=self.attach(rt,character('child',0,25,0,1,age=12))
        minor['template']='ZUL_uthumbu_claimed_son'
        rt.country['vars']['sb_court_recognized_heir_scope']=minor
        rt.backing()
        self.assertNotIn('sb_court_claimant_trait',minor.get('traits',set()))
        self.assertEqual(minor['prominence'],rt.ref('prominence',minor))
        self.assertEqual(0,minor['vars']['sb_court_represented_weight_var'])
        rt.country['ruler']=prince
        rt.backing()
        self.assertNotIn('sb_court_claimant_trait',prince['traits'])
        self.assertEqual(prince['prominence'],rt.ref('prominence',prince))
        rt.country['ruler']=king
        rt.backing()
        rt.country['vars'].pop('sb_institutions_active_var')
        rt.effect(ACTIONS['sb_court_suspend'],rt.country)
        self.assertNotIn('sb_court_claimant_trait',prince['traits'])
        self.assertEqual(prince['prominence'],rt.ref('prominence',prince))
        rt.country['vars']['sb_institutions_active_var']=1
        rt.backing()
        self.assertEqual(prince['prominence']+25,rt.ref('prominence',prince))

    def test_generated_adults_register_unpledged_once_without_touching_existing_commitments(self):
        rt,king,prince,head=court()
        newcomer=character('generated',0,60);newcomer['vars']={};newcomer.update(owner=rt.country,politician=True)
        child=character('child',0,20,age=12);child['vars']={};child.update(owner=rt.country,politician=True)
        dead=character('dead',0,20,alive=False);dead['vars']={};dead.update(owner=rt.country,general=True)
        foreign=character('foreign',0,20);foreign['vars']={};foreign.update(owner=rt.scopes['root'],magnate=True)
        rt.country['characters']=[king,prince,head,newcomer,child,dead,foreign]
        for _ in range(2):
            rt.effect(EFFECTS['sb_court_register_unpledged_cast'],rt.country)
            rt.backing()
        self.assertEqual(4,len(rt.country['members']))
        self.assertEqual(0,newcomer['vars']['sb_court_endorsement_var'])
        self.assertEqual(0,newcomer['vars']['sb_court_alignment_var'])
        self.assertEqual({'sb_court_alignment_neutral_trait','sb_court_endorsement_uncommitted_trait'},newcomer['traits'])
        self.assertEqual(50,newcomer['vars']['sb_court_represented_weight_var'])
        self.assertIs(prince,head['vars']['sb_court_successor_pledge_scope'])
        for actor in (child,dead,foreign):self.assertNotIn('sb_court_registered_var',actor['vars'])

    def test_house_roster_excludes_princes_juniors_and_unaffiliated_advisers(self):
        rt,_,prince,head=court()
        junior=self.attach(rt,character('junior',10,40))
        outsider=self.attach(rt,character('adviser',0,40))
        rt.backing()
        shown=rt.roster_shown
        self.assertTrue(shown('sb_court_roster_member',head))
        for actor in (prince,junior,outsider):self.assertFalse(shown('sb_court_roster_member',actor))
        self.assertTrue(shown('sb_court_roster_candidate',prince))
        self.assertTrue(shown('sb_court_roster_councillor',outsider))

    def test_new_representatives_do_not_make_princes_purchasable_or_stale_heads_chargeable(self):
        rt,_,prince,head=court()
        junior=self.attach(rt,character('junior',10,40))
        outsider=self.attach(rt,character('adviser',0,40))
        rt.backing()
        for actor in (prince,junior):self.assertFalse(rt.condition(TRIGGERS['sb_court_pledge_target'],actor))
        for actor in (head,outsider):self.assertTrue(rt.condition(TRIGGERS['sb_court_pledge_target'],actor))
        rt.effect(EFFECTS['sb_court_open_pledge_quote'],head)
        before=rt.country['gold_reserves']
        junior['prominence']=60
        rt.effect(EFFECTS['sb_court_confirm_pledge'],rt.country)
        self.assertEqual(before,rt.country['gold_reserves'])
        self.assertNotIn('sb_court_action_open_var',rt.country['vars'])
        self.assertEqual(0,head['vars']['sb_court_endorsement_var'])

    def test_opening_has_no_heir_and_links_have_one_native_navigation_action(self):
        template=(ROOT/'common/character_templates/sb_zulu_dynasty_characters.txt').read_text(encoding='utf-8-sig')
        self.assertNotIn('heir = yes',find_object(template,'REPLACE:ZUL_mpande_zulu'))
        history=(ROOT/'common/history/characters/zul - zulu.txt').read_text(encoding='utf-8-sig')
        self.assertIn('set_variable = no_heirs',history)
        self.assertIn('on_created = { add_character_role = politician }',history)
        gui=(ROOT/'gui/sb_prerogative_progress_bars.gui').read_text(encoding='utf-8-sig')
        import re
        buttons=[find_object(gui[m.start():],'sb_court_character_button') for m in re.finditer(r'sb_court_character_button\s*=\s*\{',gui)]
        self.assertEqual(6,len(buttons))
        for body in buttons:
            self.assertNotIn('onclick',body)
        button=(ROOT/'gui/sb_court_character_buttons.gui').read_text(encoding='utf-8-sig')
        self.assertIn('datacontext = "[Scope.AccessCharacter]"',button)
        self.assertEqual(['"[InformationPanelBar.OpenCharacterPanel(Character.AccessSelf)]"'],re.findall(r'^\s*onclick\s*=\s*([^\n]+)',button,re.M))
        self.assertIn('onrightclick = "[RightClickMenuManager.ShowForCharacter(Character.AccessSelf)]"',button)
        self.assertIn('text = "[Character.GetFullNameNoFormatting]"',button)
        self.assertIn('FancyTooltip_Character',button)
        self.assertIn('alwaystransparent = yes',find_object(button[button.index('buttonText ='):],'buttonText'))
        self.assertNotIn('GetVariableSystem',button)
        self.assertNotIn('sb_court_provenance',gui)
        self.assertIn("GetList('sb_court_house_members')",gui)
        text=(ROOT/'localization/english/sb_institutions_l_english.yml').read_text(encoding='utf-8-sig')
        for line in text.splitlines():
            if line.startswith((' sb_court_movements_readout:',' sb_court_movements_breakdown:')):self.assertNotIn('Traditionalist',line)
        for role in ('IsIGLeader','IsGeneral','IsAdmiral','IsMagnate','IsExecutive'):
            native=(GAME/'localization/english/customized_tooltips_l_english.yml').read_text(encoding='utf-8-sig')+(GAME/'gui/character_panel.gui').read_text(encoding='utf-8-sig')
            self.assertIn('Character.'+role,native)


if __name__=='__main__':unittest.main()
