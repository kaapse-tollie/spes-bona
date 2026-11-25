"""Execute the shared contest controller; native timing, wars and GUI remain DP checks."""
from pathlib import Path
import hashlib
import json
import re
import unittest
from tools.check_override_inventory import extract_top_level_blocks, find_object, extract_braced_object
from tests.test_zulu_institutions_laws import statements

ROOT = Path(__file__).resolve().parents[1]

def source(path): return (ROOT/path).read_text(encoding='utf-8-sig')
def defs(path): return {k: statements(v) for k,v in extract_top_level_blocks(source(path)).items()}
E = defs('common/scripted_effects/sb_chiefdoms_contest_effects.txt')
E.update(defs('common/scripted_effects/sb_zululand_settlement_effects.txt'))
E.update(defs('common/scripted_effects/sb_usuthu_politics_effects.txt'))
T = defs('common/scripted_triggers/sb_chiefdoms_contest_triggers.txt')
T.update({k:v for k,v in defs('common/scripted_triggers/sb_zululand_settlement_triggers.txt').items() if k != 'sb_zululand_chiefdoms_situation_active'})
T.update(defs('common/scripted_triggers/sb_hamu_bargain_triggers.txt'))
T.update(defs('common/scripted_triggers/sb_game_rule_triggers.txt'))

def entity(name, **fields): return dict(id=name, vars={}, **fields)

def substitute_parameters(nodes, params):
    if isinstance(nodes, list):
        return [(substitute_parameters(k, params), op, substitute_parameters(v, params)) for k, op, v in nodes]
    return re.sub(r'\$([^$]+)\$', lambda m: params[m[1]], nodes)

class Contest:
    """A strict bounded interpreter, not a substitute for the game's revolution engine."""
    def __init__(self):
        self.journal=entity('JE',journal_entry_age=0)
        self.nal=entity('NAL',alive=True,journal=self.journal)
        self.trn=entity('TRN',alive=True,states=[entity('east',state_region='s:STATE_EAST_TRANSVAAL')])
        self.britain=entity('GBR',alive=True)
        self.zul=entity('ZUL',alive=True,territory=True,overlord=self.nal,laws={'law_type:law_sb_federated_chiefdoms','law_type:law_sb_chiefly_council'},movements=[])
        self.claimant=entity('claimant',eligible=True)
        self.zul['vars'].update(sb_zululand_usuthu_contest_var=1,sb_court_restoration_claimant_scope=self.claimant)
        self.container=entity('container')
        self.globals={'sb_zululand_live_zul_scope':self.zul}
        self.scopes={}
        self.active=True
        self.results=[]
        self.interrupted=False
        self.run('sb_chiefs_start_clock',self.nal)
    def ref(self,key,ctx,prev=None):
        if key in ('yes','no'): return key=='yes'
        if key.startswith('cu:'): return key
        if key=='game_date': return 18800101
        try: return float(key)
        except ValueError: pass
        first,sep,rest=key.partition('.')
        if first=='this': val=ctx
        elif first=='prev': val=prev
        elif first=='c:NAL': val=self.nal
        elif first=='c:TRN': val=self.trn
        elif first=='c:GBR': val=self.britain
        elif first=='je:je_sb_zululand_chiefdoms': val=ctx.get('journal') if ctx else None
        elif first.startswith('global_var:'): val=self.globals.get(first[11:])
        elif first.startswith('container:'): val=self.container if self.active else None
        elif first.startswith('scope:'): val=self.scopes.get(first[6:])
        elif first.startswith('var:'): val=ctx.get('vars',{}).get(first[4:]) if ctx else None
        else: val=ctx.get(first) if ctx else None
        return self.ref(rest,val,ctx) if sep and val is not None else val
    def condition(self,nodes,ctx,prev=None):
        result=[]
        for k,op,v in nodes:
            if k in ('OR','AND','NOT','NOR'):
                r=[self.condition([n],ctx,prev) for n in v]
                b={'OR':any(r),'AND':all(r),'NOT':not any(r),'NOR':not any(r)}[k]
            elif k=='trigger_if':
                fields=dict((a,c) for a,b,c in v)
                matched=self.condition(fields['limit'],ctx,prev)
                b=not matched or self.condition([n for n in v if n[0]!='limit'],ctx,prev)
            elif k=='trigger_else': b=matched or self.condition(v,ctx,prev)
            elif k in T: b=self.condition(T[k],ctx,prev)==(v=='yes')
            elif k=='sb_zululand_chiefdoms_situation_active': b=self.active==(v=='yes')
            elif k=='sb_court_royal_candidate': b=ctx.get('eligible',False)==(v=='yes')
            elif k=='has_variable': b=v in ctx.get('vars',{})
            elif k=='has_global_variable': b=v in self.globals
            elif k=='exists': b=self.ref(v,ctx,prev) is not None
            elif k=='is_country_alive': b=ctx.get('alive',False)==(v=='yes')
            elif k=='has_game_rule': b=v==getattr(self, 'mode', 'sb_frontier_ai_behavior_off')
            elif k=='any_scope_pop': b=any(self.condition(v,pop,ctx) for pop in ctx.get('pops',[]))
            elif k=='is_pop_type': b=ctx.get('pop_type')==v
            elif k=='is_subject': b=(ctx.get('overlord') is not None)==(v=='yes')
            elif k=='is_direct_subject_of': b=ctx.get('overlord') is self.ref(v,ctx,prev)
            elif k=='is_subject_of':
                actor=ctx.get('overlord'); target=self.ref(v,ctx,prev); b=False
                while actor is not None:
                    if actor is target:b=True;break
                    actor=actor.get('overlord')
            elif k=='country_definition': b=ctx['id']==v[3:]
            elif k=='state_region': b=ctx.get('state_region')==v
            elif k=='any_scope_state': b=any(self.condition(v,s,ctx) for s in ctx.get('states',[]))
            elif k=='has_modifier': b=v in ctx.get('modifiers',set())
            elif k=='owns_entire_state_region': b=ctx.get('territory',False)
            elif k=='has_law': b=v in ctx.get('laws',set())
            elif k=='is_civil_war_type': b=ctx.get('war_type')==v
            elif k=='is_political_movement_type': b=ctx.get('movement_type')==v
            elif k=='any_political_movement': b=any(self.condition(v,m,ctx) for m in ctx.get('movements',[]))
            elif isinstance(v,list):
                target=self.ref(k,ctx,prev)
                b=target is not None and self.condition(v,target,ctx)
            else:
                a,bvalue=self.ref(k,ctx,prev),self.ref(v,ctx,prev)
                if a is None or bvalue is None:b=False
                elif op in ('=','?='):b=a is bvalue if isinstance(a,dict) else a==bvalue
                elif op=='>=':b=a>=bvalue
                elif op=='>':b=a>bvalue
                elif op=='<':b=a<bvalue
                elif op=='<=':b=a<=bvalue
                else:raise AssertionError((k,op,v))
            result.append(b)
        return all(result)
    def run(self,key,ctx=None): self.effect(E[key],ctx or self.zul)
    def effect(self,nodes,ctx,prev=None):
        matched=False
        for k,op,v in nodes:
            if k in ('if','else_if','else'):
                if k=='if': matched=False
                if matched:continue
                limits=next((c for a,b,c in v if a=='limit'),[])
                if k=='else' or self.condition(limits,ctx,prev):
                    matched=True;self.effect([n for n in v if n[0]!='limit'],ctx,prev)
            elif k in ('save_scope_as','save_temporary_scope_as'): self.scopes[v]=ctx
            elif k=='set_variable':
                if isinstance(v,str):ctx['vars'][v]=1
                else:
                    d={a:c for a,b,c in v}
                    ctx['vars'][d['name']]=self.ref(d['value'],ctx,prev) if 'value' in d else ('timed',d.get('years'),d.get('days'))
            elif k=='remove_variable':ctx['vars'].pop(v,None)
            elif k=='change_variable':
                args={a:c for a,_,c in v}
                ctx['vars'][args['name']]+=self.ref(args['add'],ctx,prev)
            elif k=='clamp_variable':
                args={a:c for a,_,c in v}
                ctx['vars'][args['name']]=max(float(args['min']),min(float(args['max']),ctx['vars'][args['name']]))
            elif k=='set_global_variable':
                d={'name':v,'value':'1'} if isinstance(v,str) else {a:c for a,b,c in v}
                self.globals[d['name']]=self.ref(d['value'],ctx,prev)
            elif k=='remove_global_variable':self.globals.pop(v,None)
            elif k=='add_to_variable_list':
                d={a:c for a,b,c in v};ctx.setdefault(d['name'],[]).append(self.ref(d['target'],ctx,prev))
            elif k in ('every_political_movement','every_scope_state','random_scope_state','every_scope_pop'):
                collection = {'every_political_movement':'movements','every_scope_pop':'pops'}.get(k,'states')
                for m in ctx.get(collection,[]):
                    limit=next((c for a,b,c in v if a=='limit'),[])
                    if self.condition(limit,m,ctx):
                        self.effect([n for n in v if n[0]!='limit'],m,ctx)
                        if k=='random_scope_state': break
            elif k=='add_modifier':ctx.setdefault('modifiers',set()).add(dict((a,c) for a,_,c in v)['name'])
            elif k=='remove_modifier':ctx['modifiers'].remove(v)
            elif k=='ordered_scope_pop':
                args={a:c for a,_,c in v}
                pops=sorted((p for p in ctx['pops'] if self.condition(args['limit'],p,ctx)),
                            key=lambda p:self.ref(args['order_by'],p,ctx), reverse=True)
                if pops:
                    self.effect([n for n in v if n[0] not in ('limit','order_by','position','check_range_bounds')],
                                pops[int(args['position'])],ctx)
            elif k=='move_partial_pop':
                args={a:c for a,_,c in v}
                size=int(args['population']) if 'population' in args else int(ctx['total_size']*float(args['population_ratio']))
                ctx['total_size']-=size
                state=self.ref(args['state'],ctx,prev)
                state['arrivals']=state.get('arrivals',0)+size
            elif k=='hidden_effect':self.effect(v,ctx,prev)
            elif k=='sb_zululand_finalize_political_contest':
                self.results.append((ctx['id'],ctx['vars']['sb_zululand_contest_result_var']));self.active=False
            elif k=='sb_zululand_cleanup_situation':self.active=False;self.interrupted=True
            elif k in E:
                body = substitute_parameters(E[k], {a:c for a,_,c in v}) if isinstance(v,list) else E[k]
                self.effect(body,ctx,prev)
            elif isinstance(v,list):
                target=self.ref(k,ctx,prev)
                if target is not None:self.effect(v,target,ctx)
            else:raise AssertionError((k,op,v))
    def expire(self):self.journal['journal_entry_age']=3650
    def royal(self,activism):
        m=entity('usuthu',movement_type='movement_sb_zulu_royal',political_movement_radicalism=activism,owner=self.zul)
        self.zul['movements'].append(m);return m
    def tick(self): self.run('sb_chiefs_evaluate_contest',self.nal)

class ChiefdomsRefinement(unittest.TestCase):
    def test_ten_year_review_mixed_constitution_and_no_prerogative_gate(self):
        c=Contest();c.tick();self.assertEqual([],c.results)
        c.expire();c.zul['laws']={'law_type:law_monarchy','law_type:law_sb_chiefly_council'}
        c.tick();self.assertTrue(c.active);self.assertEqual([],c.results)
        c.zul['laws']={'law_type:law_sb_federated_chiefdoms','law_type:law_sb_chiefly_council'}
        c.zul['vars']['sb_prerogative_var']=-100;c.tick();self.assertEqual([('ZUL',2)],c.results)
        c.tick();self.assertEqual(1,len(c.results))
    def test_clock_does_not_reset_on_exit_reentry_or_repeated_setup(self):
        c=Contest();c.expire();c.run('sb_chiefs_start_clock');self.assertEqual(3650,c.journal['journal_entry_age'])
        self.assertEqual([c.zul],c.container['sb_chiefs_countries'])
    def test_actual_activism_boundary_requires_a_valid_claimant(self):
        for level,wins in ((.99,False),(.9999,False),(1,True)):
            c=Contest();c.royal(level);c.tick();self.assertEqual(wins,bool(c.results))
        c=Contest();c.claimant['eligible']=False;c.royal(1);c.tick();self.assertEqual([],c.results)
    def test_completed_restoration_early_but_partial_pair_does_not_win(self):
        c=Contest();c.zul['ruler']=c.claimant;c.zul['laws']={'law_type:law_monarchy','law_type:law_sb_chiefly_council'}
        c.tick();self.assertEqual([],c.results)
        c.zul['laws']={'law_type:law_monarchy','law_type:law_autocracy'};c.tick();self.assertEqual([('ZUL',1)],c.results)
    def test_loss_of_pact_or_territory_interrupts_without_rewards(self):
        for field,value in [('overlord',None),('territory',False),('alive',False)]:
            c=Contest();c.zul[field]=value;c.expire();c.tick()
            self.assertTrue(c.interrupted);self.assertEqual([],c.results)
    def test_native_organising_waits_and_cancelled_object_does_not_stick(self):
        c=Contest();c.container['vars']['sb_chiefs_native_test_var']=1;c.expire();m=c.royal(1)
        m['civil_war']=entity('war',war_type='revolution',civil_war_progress=.5)
        c.tick();self.assertEqual([],c.results)
        m.pop('civil_war');c.tick();self.assertEqual([('ZUL',2)],c.results)
    def test_native_winner_is_exact_waits_for_reunion_and_receipt_is_once(self):
        for alignment in (1,2):
            c=Contest();rebel=entity('REBELS',alive=True,territory=False,laws=set())
            rebel['vars'].update(sb_court_war_alignment_var=alignment,sb_zululand_usuthu_contest_var=1,sb_court_restoration_claimant_scope=c.claimant)
            c.container['vars'].update(sb_chiefs_rebels_scope=rebel,sb_chiefs_native_test_var=1)
            rebel['vars']['sb_court_civil_war_var']=c.zul
            c.zul['vars']['sb_court_civil_war_var']=rebel
            c.run('sb_chiefs_reserve_war_result',rebel);c.tick();self.assertEqual([],c.results)
            c.zul['vars']['sb_court_war_alignment_var']=3-alignment
            c.run('sb_chiefs_reserve_war_result',c.zul);self.assertIs(rebel,c.globals['sb_zululand_live_zul_scope'])
            rebel['territory']=True;c.tick();self.assertEqual([('REBELS',alignment)],c.results)
    def test_original_winner_without_pact_and_third_party_subject_are_interrupted(self):
        for rebel in (False,True):
            c=Contest();actor=c.zul
            if rebel:
                actor=entity('REBELS',alive=True,territory=True,overlord=entity('foreign'))
                c.container['vars']['sb_chiefs_rebels_scope']=actor
            else:actor.pop('overlord')
            c.container['vars']['sb_chiefs_native_test_var']=1
            if not rebel:c.container['vars']['sb_chiefs_rebels_scope']=entity('defeated')
            actor['vars'].update(sb_court_war_alignment_var=2,sb_zululand_usuthu_contest_var=1,sb_court_civil_war_var=c.zul if rebel else c.container['vars']['sb_chiefs_rebels_scope'])
            c.run('sb_chiefs_reserve_war_result',actor);c.tick();self.assertTrue(c.interrupted);self.assertEqual([],c.results)
    def test_unrelated_or_preexisting_winner_cannot_reserve_partition(self):
        c=Contest();c.zul['vars'].update(sb_court_war_alignment_var=1,sb_court_civil_war_var=entity('unrelated'))
        c.run('sb_chiefs_reserve_war_result',c.zul)
        self.assertNotIn('sb_chiefs_winner_scope',c.container['vars'])
        c.container['vars']['sb_chiefs_native_test_var']=1
        c.run('sb_chiefs_reserve_war_result',c.zul)
        self.assertNotIn('sb_chiefs_winner_scope',c.container['vars'])
    def test_scoped_uprising_gates_leave_unrelated_owners_and_secession_causes(self):
        c=Contest();m=c.royal(.5)
        self.assertFalse(c.condition(T['sb_chiefs_other_uprising_allowed'],m))
        self.assertFalse(c.condition(T['sb_chiefs_constitutional_uprising_allowed'],m))
        c.container['vars']['sb_chiefs_native_test_var']=1
        self.assertTrue(c.condition(T['sb_chiefs_constitutional_uprising_allowed'],m))
        self.assertFalse(c.condition(T['sb_chiefs_other_uprising_allowed'],m))
        m['owner']=c.nal;self.assertTrue(c.condition(T['sb_chiefs_other_uprising_allowed'],m))
        for path in ['zz_sb_cultural_majority_movement_override.txt','zz_sb_cultural_minority_movement_override.txt']:
            self.assertNotIn('sb_chiefs_other_uprising_allowed',source('common/political_movements/'+path))
    def test_new_movement_overrides_only_add_documented_gate_and_usfp_grouping_fix(self):
        report=json.loads(source('Docs/compatibility/chiefdoms_uprising_contracts_1_15_2.json'))
        out=source('common/political_movements/zzz_sb_chiefdoms_uprising_overrides.txt')
        for row in report['contracts']:
            upstream=(ROOT.parent/'Community Mod Framework'/row['dependency_path']).read_text(encoding='utf-8-sig')
            original=find_object(upstream,row['key'],directive='REPLACE')
            self.assertEqual(row['dependency_object_sha256'],hashlib.sha256(original.encode()).hexdigest())
            actual=find_object(out,row['key'],directive='REPLACE')
            actual=re.sub(r'\s*possible = \{ sb_chiefs_other_uprising_allowed = yes \}', '', actual)
            actual=re.sub(r'\s*sb_chiefs_other_uprising_allowed = yes','',actual)
            if row['key']=='movement_reactionary':
                # Keep the installed CMF hash; permit only the documented NAND correction.
                actual,count=re.subn(r'NOT\s*=\s*\{\s*AND\s*=\s*\{\s*(is_usfp_active = yes\s*usfp_country_is_american = yes #[^\n]*\n\s*)\}\s*\}',
                                     r'NOT = { \1 }',actual)
                self.assertEqual(1,count)
            self.assertEqual(re.sub(r'\s+','',original),re.sub(r'\s+','',actual),row['key'])
    def test_ir_exit_preserves_contest_and_shared_country_ui(self):
        core=source('common/scripted_effects/sb_institutions_effects.txt')
        self.assertNotIn('sb_zululand_suspend_contest_interventions',core)
        self.assertIn('NOT = { sb_chiefs_contest_country = yes }',core)
        shared=source('gui/sb_court_house_roster.gui')
        self.assertRegex(shared, r'^types sb_court_house_types \{')
        self.assertNotIn('JournalEntry.GetCountry',shared);self.assertNotIn('GetPlayer',shared)
        self.assertIn("Country.MakeScope.GetList('sb_court_members')",shared)
        self.assertIn("Character.GetIDString",shared)
        for path in ['gui/sb_prerogative_progress_bars.gui','gui/sb_zululand_chiefdoms_progress_bars.gui']:
            self.assertIn('sb_court_house_roster = {',source(path))
    def test_native_test_is_opt_in_and_no_dependency_payload_changed(self):
        decision=source('common/decisions/sb_chiefdoms_test_decisions.txt')
        self.assertIn('has_global_variable = sb_chiefdoms_test_tools_enabled_var',decision)
        self.assertIn('is_subject_type = subject_type_sb_zulu_chiefdoms',decision)
        self.assertIn('ai_chance = { value = 0 }',decision)

if __name__=='__main__':unittest.main()
