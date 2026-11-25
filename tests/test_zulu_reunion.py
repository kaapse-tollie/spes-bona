"""Run the shipped play replacement and reunion against the existing court fixtures.

The fixture supplies native demands, the enforcement callback and the territorial
merge. Only an engine replay can verify native callback order and diplomacy.
"""
from copy import deepcopy
from itertools import product
from unittest import TestCase
from unittest.mock import patch

from tests import test_zulu_contested_crown as dynasty
from tests.test_hamu_constitutional_settlement import ConstitutionalContractRuntime, WAR
from tests.test_zulu_court_politics import EFFECTS, TRIGGERS, definitions
from tests.test_zulu_frontier_followup import field

REUNION = definitions('common/scripted_effects/sb_court_reunion_effects.txt')
BOUND = definitions('common/scripted_triggers/sb_court_reunion_triggers.txt')
GOAL = definitions('common/war_goal_types/sb_zulu_take_power.txt')['sb_zulu_take_power']
HOOKS = definitions('common/on_actions/sb_court_on_actions.txt')


class ReunionNatives:
    def condition(self, nodes, scope, prev=None):
        for node in nodes:
            key, _, value = node
            if key == 'play_participant_has_war_goal_of_type_against':
                target = self.ref(field(value,'target'),scope,prev)
                demand = (scope['id'],target['id'],field(value,'type'))
                result = any(demand in play['goals'] for play in self.plays)
            elif key == 'is_diplomatic_play_type':
                result = scope['type'] == value
            elif key == 'any_civil_war':
                result = any(self.condition(value,w,scope) for w in scope.get('wars',[]))
            elif key == 'is_player':
                result = scope.get('player',False) == (value == 'yes')
            else:
                result = super().condition([node],scope,prev)
            if not result:
                return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes,scope,prev):
            key, _, value = node
            if key == 'every_diplomatic_play':
                for play in self.plays:
                    if self.condition(field(value,'limit'),play,scope):
                        self.effect([n for n in value if n[0]!='limit'],play,scope)
            elif key == 'add_war_goal':
                holder = self.ref(field(value,'holder'),scope,prev)
                target = self.ref(field(value,'target_country'),scope,prev)
                old = self.scopes.copy()
                self.scopes.update(diplomatic_play=scope,target_country=target)
                assert self.condition(field(GOAL,'valid'),holder)
                assert field(value,'primary_demand') == 'yes'
                scope['goals'].add((holder['id'],target['id'],field(value,'type')))
                self.scopes = old
            elif key == 'remove_war_goal':
                holder = scope[field(value,'who')]
                scope['goals'].remove((holder['id'],scope['target']['id'],field(value,'type')))
            elif key == 'annex_as_civil_war':
                absorbed = self.ref(value,scope,prev)
                assert absorbed['alive'] and absorbed is not scope
                absorbed['alive'] = False
                self.reunions.append((scope['id'],absorbed['id']))
            elif key in ('initiator','target','heir'):
                obj = self.ref(key,scope,prev)
                if obj is not None:
                    self.effect(value,obj,scope)
            elif key == 'trigger_event' and isinstance(value,list) and any(k=='on_action' for k,_,_ in value):
                self.delayed = field(value,'on_action')
            elif key == 'play_as':
                scope['player']=False
                self.ref(value,scope,prev)['player']=True
            else:
                super().effect([node],scope,prev)

    def prepare(self, rebels, war, early_play=True):
        self.reunions=[]
        self.delayed=None
        self.plays=[]
        rebels['alive']=True
        rebels['civil_war_origin_country']=self.country
        self.country['wars']=[war]
        self.country['external']={'truce_to_NAL':19221,'truce_from_NAL':19221,
                                  'articles':[(28,2)],'relations':{'NAL':-42},'overlord':'NAL'}
        origin,opposition = self.country['id'],rebels['id']
        goals={(origin,opposition,'annex_country'),(opposition,origin,'annex_country')}
        play={'type':'dp_revolution','id':11,'vars':{},'initiator':rebels,'target':self.country,
              'leader':'GBR','goals':goals}
        if early_play:
            self.plays.append(play)
            self.effect(REUNION['sb_court_bind_reunion_play'],play)
            assert len(goals)==2 and all(goal[2]=='annex_country' for goal in goals)
        self.scopes.update(target=rebels,actual_war=war)
        self.effect([('sb_court_register_reunion','=',[('WAR','=','scope:actual_war')])],self.country)
        if not early_play:
            assert self.delayed=='sb_court_recheck_reunion_play'
            self.plays.append(play)
            self.effect(field(HOOKS[self.delayed],'effect'),rebels)
        self.effect(REUNION['sb_court_bind_reunion_play'],play)
        assert goals=={(origin,opposition,'annex_country'),(opposition,origin,'sb_zulu_take_power')}
        return play

    def enforce(self, play):
        self.scopes={'root':{'id':'foreign','vars':{}},'diplomatic_play':play,'target_country':play['target']}
        self.effect(field(GOAL,'on_enforced'),play['initiator'])


class DynasticReunion(ReunionNatives, dynasty.ClaimantRuntime):
    pass


class ConstitutionalReunion(ReunionNatives, ConstitutionalContractRuntime):
    pass


class PreserveZuluKingdom(TestCase):
    def setUp(self):
        for namespace, entries in ((EFFECTS,REUNION),(TRIGGERS,BOUND)):
            mapping=patch.dict(namespace,entries)
            mapping.start()
            self.addCleanup(mapping.stop)

    def dynastic(self, backed=False):
        with patch.object(dynasty,'ClaimantRuntime',DynasticReunion):
            rt,king,prince,*_=dynasty.court()
        dynasty.reserve(rt,king,prince)
        dynasty.answer(rt,backed)
        war,rebels=dynasty.split(rt)
        return rt,war,rebels

    def test_dynastic_contenders_both_victors_and_callback_routes(self):
        for back_claimant, rebel_win, early_play in product((False,True),repeat=3):
            with self.subTest(back_claimant=back_claimant,rebel_win=rebel_win,early_play=early_play):
                rt,war,rebels=self.dynastic(back_claimant)
                play=rt.prepare(rebels,war,early_play)
                # A backdown has no war. Military capitulation supplies the linked war.
                if not early_play:
                    play['war']={'diplomatic_play':play,'defence_leader':'GBR'}
                original=rt.country
                winner=rebels if rebel_win else original
                sovereign=winner['vars']['sb_court_dynastic_candidate_scope']
                winner['vars']['sb_prerogative_var']=17
                # Exercise an ended truce and a still-live truce, plus a treaty changed at war.
                if early_play:
                    del original['external']['truce_to_NAL'], original['external']['truce_from_NAL']
                else:
                    original['external']['truce_from_NAL']+=13
                original['external']['articles'].append((32,7))
                expected=deepcopy(original['external'])
                old_id=original['id']
                if rebel_win:
                    rebels['player']=True
                    if not early_play:  # Persist without any transient callback scopes.
                        rt,play=deepcopy((rt,play))
                        original,rebels=play['target'],play['initiator']
                        sovereign=rebels['vars']['sb_court_dynastic_candidate_scope']
                    rt.enforce(play)
                    rt.enforce(play)
                    self.assertEqual(rt.reunions,[(old_id,rebels['id'])])
                    self.assertTrue(original['player'])
                else:
                    rt.scopes['target']=rebels
                    rt.run('sb_court_record_dynastic_end',original)
                    rt.run('sb_court_resolve_dynastic_win',original)
                    rt.effect([('annex_as_civil_war','=','scope:target')],original)
                rt.run('sb_court_resolve_dynastic_win',original)
                self.assertIs(original['ruler'],sovereign)
                self.assertEqual(original['vars']['sb_prerogative_var'],17)
                self.assertEqual(original['external'],expected)
                self.assertEqual(original['id'],old_id)
                self.assertEqual(sum(str(e).count('sb_court_succession.005') for e in original['events']),1)

    def test_constitutional_win_uses_actual_alignment_including_hamus_settlement(self):
        for royal_rebels, rebel_win in product((False,True),repeat=2):
            with self.subTest(royal_rebels=royal_rebels,rebel_win=rebel_win):
                rt=ConstitutionalReunion(royal_rebels=royal_rebels,contest=False)
                war={'id':'war','vars':{}}
                play=rt.prepare(rt.rebel,war)
                winner=rt.rebel if rebel_win else rt.country
                alignment=winner['vars']['sb_court_war_alignment_var']
                before=deepcopy(rt.country['external'])
                if rebel_win:
                    rt.enforce(play)
                    rt.enforce(play)
                    self.assertEqual(rt.reunions,[(rt.country['id'],rt.rebel['id'])])
                else:
                    rt.scopes['target']=rt.rebel
                    rt.effect(WAR['sb_court_record_war_end'],rt.country)
                    rt.effect(WAR['sb_court_resolve_won_war'],rt.country)
                rt.effect(WAR['sb_court_resolve_won_war'],rt.country)
                self.assertEqual(rt.country['external'],before)
                law='law_type:law_monarchy' if alignment==1 else 'law_type:law_sb_federated_chiefdoms'
                self.assertIn(law,rt.country['laws'])
                self.assertEqual('sb_hamu_earned_var' in rt.sponsor['vars'],alignment==1)
                if alignment==1:
                    self.assertIs(rt.country['ruler'],rt.hamu)
                    self.assertIs(rt.sponsor['vars']['sb_hamu_reunion_scope'],rt.rebel)
                    self.assertIs(rt.sponsor['vars']['sb_hamu_court_scope'],rt.country)

    def test_chiefdoms_reserves_actual_side_on_original_country_and_hamu_keeps_land_receipt(self):
        for royal_rebels in (False, True):
            rt=ConstitutionalReunion(royal_rebels=royal_rebels, contest=True)
            container={'id':'partition','vars':{'sb_chiefs_native_test_var':1,
                       'sb_chiefs_origin_scope':rt.country,'sb_chiefs_rebels_scope':rt.rebel}}
            rt.containers['sb_zululand_chiefdoms_state']=container
            rt.global_vars['sb_zululand_live_zul_scope']=rt.country
            play=rt.prepare(rt.rebel,{'id':'war','vars':{}})
            rt.enforce(play)
            rt.enforce(play)
            self.assertIs(container['vars']['sb_chiefs_winner_scope'],rt.country)
            self.assertEqual(container['vars']['sb_chiefs_winner_alignment_var'],1 if royal_rebels else 2)
            self.assertEqual('sb_hamu_earned_var' in rt.sponsor['vars'],royal_rebels)
            if royal_rebels:
                self.assertIs(rt.sponsor['vars']['sb_hamu_reunion_scope'],rt.rebel)
                self.assertIs(rt.sponsor['vars']['sb_hamu_court_scope'],rt.country)

    def test_foreign_pair_untracked_revolution_and_stale_war_cannot_bind_or_enforce(self):
        rt,war,rebels=self.dynastic()
        play=rt.prepare(rebels,war)
        original=rt.country
        for wrong in ('play','holder','target','war'):
            foreign={'id':'R09','vars':{},'alive':True,'wars':[]}
            other=dict(play,id=22,goals=set(),initiator=foreign)
            if wrong=='war':
                original['wars']=[{'id':'new war','vars':{}}]
                other['initiator']=rebels
                other['goals']={(rebels['id'],original['id'],'annex_country'),(original['id'],rebels['id'],'annex_country')}
            rt.effect(REUNION['sb_court_bind_reunion_play'],other)
            rt.scopes={'diplomatic_play':other if wrong in ('play','war') else play,
                       'target_country':foreign if wrong=='target' else original}
            rt.effect(field(GOAL,'on_enforced'),foreign if wrong=='holder' else rebels)
            self.assertEqual(rt.reunions,[])
            self.assertFalse(any(g[2]=='sb_zulu_take_power' for g in other['goals']))
        start=str(HOOKS['sb_court_on_revolution_start'])
        self.assertIn('sb_court_dynastic_war_scope',start)
        self.assertIn('sb_court_tracked_war',start)
        self.assertIn('cd:ZUL',start)
