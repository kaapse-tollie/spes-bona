"""Execute the controller with injected native support; do not simulate recruitment."""
import unittest

from tests.test_zulu_contested_crown import (
    ROOT, GAME, TRIGGERS, court, reserve, answer, organising_war, split,
    definitions, statements, find_object, child,
)


def pending(incumbent=248, rival=185, back_rival=True, states=1):
    rt, king, prince, third, neutral = court(incumbent, rival)
    rt.country['states'] = [
        {'id':str(i), 'owner':rt.country, 'state_region':'s:STATE_ZULULAND',
         'buildings':[], 'pops':[], 'vars':{}} for i in range(states)
    ]
    reserve(rt, king, prince)
    # Exercise the actual event option without the manual .990 diagnostic.
    source=(ROOT/'events/sb_court_succession_events.txt').read_text(encoding='utf-8-sig')
    event=statements(find_object(source,'sb_court_succession.004'))
    option_name='sb_court_succession.004.'+('b' if back_rival else 'a')
    option=next(v for k,_,v in event if k=='option' and ('name','=',option_name) in v)
    rt.effect(next(v for k,_,v in option if k=='hidden_effect'),rt.country)
    movement = rt.country['vars']['sb_court_dynastic_movement_scope']
    support(movement, 0)
    return rt, king, prince, movement


def support(movement, value):
    movement.update({key:value for key in (
        'political_movement_support', 'political_movement_popular_support',
        'political_movement_military_support', 'political_movement_wealth_support')})


def weekly_poll(rt):
    source=(ROOT/'events/sb_court_succession_events.txt').read_text(encoding='utf-8-sig')
    poll=dict((k,v) for k,_,v in statements(find_object(source,'sb_court_succession.991')))
    if rt.condition(poll['trigger'],rt.country):
        rt.effect(poll['immediate'],rt.country)


class RecruitmentTrialTests(unittest.TestCase):
    def ready(self, rt, movement):
        return rt.condition(TRIGGERS['sb_court_recruitment_ready'], movement)

    def test_actual_rebel_identity_and_frozen_share_follow_both_choices(self):
        for back_rival in (False, True):
            rt, king, prince, movement = pending(back_rival=back_rival)
            self.assertIn('sb_court_recruitment_trial_var',rt.country['vars'])
            self.assertEqual(1,len(rt.country['debug_logs']))
            self.assertIn('SB recruitment trial started:',rt.country['debug_logs'][0])
            expected = 248/433 if back_rival else 185/433
            self.assertAlmostEqual(expected, rt.country['vars']['sb_court_dynastic_target_var'])
            self.assertIs(king if back_rival else prince,
                          rt.country['vars']['sb_court_recruitment_rebel_scope'])
            self.assertTrue(prince['agitator'])  # Legal agitator and eventual rebel ruler differ.
            self.assertFalse(king['agitator'])
            king['popularity'], prince['popularity'] = -80, 80
            self.assertAlmostEqual(.2 if back_rival else 1.8,
                                   rt.ref('sb_court_claimant_popularity_attraction', rt.country))
            self.assertAlmostEqual(16*expected-2, movement['modifiers']['sb_court_coalition_recruitment'])

    def test_readiness_uses_actual_support_and_above_target_band(self):
        for inc, rival in ((300,100),(200,200),(100,300),(248,185)):
            rt, _, _, movement = pending(inc,rival,back_rival=False)
            target = rt.country['vars']['sb_court_dynastic_target_var']
            for actual, expected in ((target-.00001,False),(target,True),
                                     (target+.04999,True),(target+.05001,False)):
                support(movement,actual)
                self.assertEqual(expected,self.ready(rt,movement),(target,actual))
            support(movement,target)
            movement['political_movement_military_support'] = 0
            self.assertTrue(self.ready(rt,movement))
            self.assertEqual(0,rt.ref('sb_court_recruitment_military',rt.country))

    def test_native_gate_rejects_weak_wrong_and_invalid_movements(self):
        rt, king, _, movement = pending()
        source=(ROOT/'common/political_movements/sb_court_dynastic_test.txt').read_text(encoding='utf-8-sig')
        gate=statements(child(child(source,'revolution'),'possible'))
        self.assertFalse(rt.condition(gate,movement))
        support(movement,.58)
        self.assertTrue(rt.condition(gate,movement))
        self.assertFalse(rt.condition(gate,dict(movement,id='unrelated')))
        king['alive']=False
        self.assertFalse(rt.condition(gate,movement))

    def test_advance_rechecks_readiness_and_advances_exact_war_once(self):
        rt, _, _, movement = pending()
        war=organising_war(rt)
        unrelated={'id':'other-war','type':'revolution','political_movement':{'id':'other'},'progress':0,'vars':{}}
        rt.country['wars'].insert(0,unrelated)
        support(movement,.52)  # Four of nine provinces; below this episode's target.
        rt.run('sb_court_progress_dynastic_crisis')
        self.assertEqual(0,war['progress'])
        support(movement,.58)
        rt.run('sb_court_progress_dynastic_crisis')
        rt.run('sb_court_progress_dynastic_crisis')
        self.assertEqual(1,war['progress'])
        self.assertEqual(0,unrelated['progress'])

    def test_feedback_increases_decreases_and_holds_without_stacking(self):
        rt, _, _, movement = pending()
        for actual, direction in ((.05,1),(.95,-1),(.58,0)):
            support(movement,actual)
            old=rt.country['vars']['sb_court_recruitment_factor_var']
            rt.run('sb_court_tick_recruitment_trial')
            self.assertEqual(old,rt.country['vars']['sb_court_recruitment_factor_var'])
            rt.run('sb_court_refresh_recruitment_trial')
            new=rt.country['vars']['sb_court_recruitment_factor_var']
            self.assertEqual(direction,(new>old)-(new<old))
            self.assertAlmostEqual(new-2,movement['modifiers']['sb_court_coalition_recruitment'])
            self.assertEqual(1,movement['modifiers']['sb_court_claimant_mobilisation'])
        for actual, bound in ((0,32),(1,.25)):
            support(movement,actual)
            for _ in range(20):
                rt.country['vars']['sb_court_recruitment_weeks_var']=0
                rt.run('sb_court_tick_recruitment_trial')
                rt.run('sb_court_refresh_recruitment_trial')
            self.assertEqual(bound,rt.country['vars']['sb_court_recruitment_factor_var'])

    def test_budget_stops_polling_without_fabricating_outcomes(self):
        rt, _, _, movement = pending()
        for _ in range(26):
            weekly_poll(rt)
        self.assertEqual(list(range(1,26)),[r['week'] for r in rt.pop_support_refreshes])
        self.assertIn('sb_court_recruitment_failed_var',rt.country['vars'])
        self.assertFalse(self.ready(rt,movement))
        before=list(rt.country['events'])
        rt.country['vars'].pop('sb_court_dynastic_poll_queued_var',None)
        rt.run('sb_court_queue_dynastic_poll')
        rt.run('sb_court_tick_recruitment_trial')
        rt.run('sb_court_refresh_recruitment_trial')
        self.assertEqual(25,len(rt.pop_support_refreshes))
        self.assertEqual(before,rt.country['events'])
        self.assertEqual(26,rt.country['vars']['sb_court_recruitment_weeks_var'])
        self.assertNotIn('sb_court_dynastic_resolved_var',rt.country['vars'])
        self.assertIn('sb_court_dynastic_crisis_var',rt.country['vars'])

    def test_final_sample_success_precedes_expiry_and_stalled_war_does_not_bypass_it(self):
        for actual, advanced in ((.58,True),(.4,False)):
            rt, _, _, movement = pending()
            war=organising_war(rt)
            rt.country['vars']['sb_court_recruitment_weeks_var']=25
            support(movement,actual)
            weekly_poll(rt)
            self.assertEqual(int(advanced),war['progress'])
            self.assertEqual(not advanced,'sb_court_recruitment_failed_var' in rt.country['vars'])
            self.assertFalse(getattr(rt,'pop_support_refreshes',[]))

    def test_refresh_uses_last_weeks_modifier_and_does_not_assign_support(self):
        rt, _, _, movement = pending()
        old=movement['modifiers']['sb_court_coalition_recruitment']
        weekly_poll(rt)
        refresh=rt.pop_support_refreshes[0]
        self.assertEqual(old,refresh['applied_modifier'])
        self.assertAlmostEqual((old+2)*1.5,refresh['next_factor'])
        self.assertEqual(refresh['next_factor']-2,movement['modifiers']['sb_court_coalition_recruitment'])
        self.assertEqual(0,movement['political_movement_support'])
        self.assertNotIn('sb_court_dynastic_advanced_var',rt.country['vars'])
        # Supply a later native sample. Readiness stops refreshing even if the
        # native organising object has not appeared yet.
        support(movement,.58)
        weekly_poll(rt)
        self.assertEqual(1,len(rt.pop_support_refreshes))
        war=organising_war(rt)
        weekly_poll(rt)
        self.assertEqual(1,war['progress'])
        self.assertEqual(1,len(rt.pop_support_refreshes))

    def test_refresh_is_confined_to_valid_pending_one_state_episodes(self):
        for invalid in ('unrelated','multi_state','no_trial','no_pending','failed','advanced',
                        'active_war','dead','no_movement','foreign_movement','other_movement',
                        'before_first_sample','at_budget'):
            with self.subTest(invalid=invalid):
                rt, king, _, movement = pending()
                v=rt.country['vars']
                v['sb_court_recruitment_weeks_var']=1
                if invalid=='unrelated': v.pop('sb_institutions_active_var')
                elif invalid=='multi_state': rt.country['states'].append({'vars':{}})
                elif invalid=='no_trial': v.pop('sb_court_recruitment_trial_var')
                elif invalid=='no_pending': v.pop('sb_court_dynastic_test_pending_var')
                elif invalid=='failed': v['sb_court_recruitment_failed_var']=1
                elif invalid=='advanced': v['sb_court_dynastic_advanced_var']=1
                elif invalid=='active_war': v['sb_court_dynastic_war_scope']={'id':'war'}
                elif invalid=='dead': king['alive']=False
                elif invalid=='no_movement': v.pop('sb_court_dynastic_movement_scope')
                elif invalid=='foreign_movement': movement['owner']={'id':'other','vars':{}}
                elif invalid=='other_movement': movement['type']='movement_other'
                elif invalid=='before_first_sample': v['sb_court_recruitment_weeks_var']=0
                elif invalid=='at_budget': v['sb_court_recruitment_weeks_var']=26
                before=movement['modifiers']['sb_court_coalition_recruitment']
                rt.run('sb_court_refresh_recruitment_trial')
                self.assertFalse(getattr(rt,'pop_support_refreshes',[]))
                self.assertEqual(before,movement['modifiers']['sb_court_coalition_recruitment'])

    def test_weekly_refresh_uses_current_country_with_a_foreign_event_root(self):
        rt, _, _, movement = pending()
        foreign={'id':'foreign','vars':{},'movements':[]}
        rt.scopes['root']=foreign
        weekly_poll(rt)
        self.assertEqual([rt.country['id']],[r['country'] for r in rt.pop_support_refreshes])
        self.assertEqual({},foreign['vars'])

    def test_native_refresh_order_and_installed_effect_contract(self):
        source=(ROOT/'events/sb_court_succession_events.txt').read_text(encoding='utf-8-sig')
        poll=find_object(source,'sb_court_succession.991')
        order=['sb_court_tick_recruitment_trial','sb_court_progress_dynastic_crisis',
               'sb_court_finish_recruitment_trial_tick','sb_court_refresh_recruitment_trial',
               'sb_court_queue_dynastic_poll']
        self.assertEqual(sorted(poll.index(name) for name in order),[poll.index(name) for name in order])
        native=(GAME/'common/laws/00_church_and_state.txt').read_text(encoding='utf-8-sig')
        self.assertIn('recalculate_pop_ig_support = yes',native)

    def test_diagnostic_cannot_arm_future_crises_or_retrofit_existing_movements(self):
        rt, king, prince, *_ = court()
        rt.country['states']=[{'id':'state','owner':rt.country,'vars':{},'buildings':[],'pops':[]}]
        rt.run('sb_court_enable_recruitment_trial')
        self.assertNotIn('sb_court_recruitment_trial_var',rt.country['vars'])
        # A movement created without a one-state trial remains untouched even if
        # the state count later falls to one, or the choice is delivered again.
        rt, _, _, movement = pending(states=2)
        rt.country['states'].pop()
        rt.run('sb_court_enable_recruitment_trial')
        answer(rt)
        self.assertNotIn('sb_court_recruitment_trial_var',rt.country['vars'])
        self.assertNotIn('sb_court_coalition_recruitment',movement['modifiers'])
        self.assertTrue(self.ready(rt,movement))
        self.assertEqual(1,len(rt.country['movements']))

    def test_multi_state_path_unchanged(self):
        rt, _, _, movement = pending(states=2)
        self.assertNotIn('sb_court_recruitment_trial_var',rt.country['vars'])
        self.assertNotIn('sb_court_coalition_recruitment',movement['modifiers'])
        self.assertTrue(self.ready(rt,movement))
        war=organising_war(rt)
        rt.run('sb_court_progress_dynastic_crisis')
        self.assertEqual(1,war['progress'])

    def test_repeated_choice_does_not_reset_recruitment_or_duplicate_start_log(self):
        rt, _, _, movement = pending()
        rt.run('sb_court_tick_recruitment_trial')
        factor=rt.country['vars']['sb_court_recruitment_factor_var']
        answer(rt,False)
        self.assertEqual(1,rt.country['vars']['sb_court_recruitment_weeks_var'])
        self.assertEqual(factor,rt.country['vars']['sb_court_recruitment_factor_var'])
        self.assertIs(movement,rt.country['vars']['sb_court_dynastic_movement_scope'])
        self.assertEqual(1,sum('SB recruitment trial started:' in line
                               for line in rt.country['debug_logs']))

    def test_state_count_change_cannot_start_one_state_trial(self):
        rt, _, _, movement = pending()
        support(movement,.58)
        rt.country['states'].append({'vars':{}})
        self.assertFalse(self.ready(rt,movement))
        rt.run('sb_court_tick_recruitment_trial')
        self.assertIn('sb_court_recruitment_failed_var',rt.country['vars'])

    def test_cancel_death_and_both_winners_clean_only_trial_additions(self):
        for outcome in ('cancel','death','main','rebels'):
            rt, king, _, movement = pending()
            movement['modifiers']['unrelated_bonus']=.3
            if outcome in ('main','rebels'):
                support(movement,.58)
                _, rebels=split(rt)
                winner=rt.country if outcome=='main' else rebels
                rt.run('sb_court_record_dynastic_end')
                rt.run('sb_court_resolve_dynastic_win',winner)
            elif outcome=='death':
                king['alive']=False
                rt.run('sb_court_progress_dynastic_crisis')
            else: rt.run('sb_court_cancel_dynastic_crisis')
            self.assertNotIn('sb_court_coalition_recruitment',movement['modifiers'])
            self.assertEqual(.3,movement['modifiers']['unrelated_bonus'])
            self.assertFalse(any(k.startswith('sb_court_recruitment_') for k in rt.country['vars']))

    def test_only_weekly_delivery_updates_controller(self):
        rt, _, _, movement = pending()
        for _ in range(3): rt.run('sb_court_progress_dynastic_crisis')
        self.assertEqual(0,rt.country['vars']['sb_court_recruitment_weeks_var'])
        self.assertFalse(getattr(rt,'pop_support_refreshes',[]))
        weekly_poll(rt)
        self.assertEqual(1,rt.country['vars']['sb_court_recruitment_weeks_var'])
        self.assertEqual(1,len(rt.pop_support_refreshes))
        self.assertEqual(3,len(rt.country['debug_logs']))

    def test_trial_modifier_cannot_scale_activism_and_reads_exist(self):
        mods=definitions('common/static_modifiers/sb_court_dynastic_modifiers.txt')
        attraction=dict((k,v) for k,_,v in mods['sb_court_coalition_recruitment'])
        self.assertEqual({'icon','political_movement_pop_attraction_mult'},set(attraction))
        mobilisation=dict((k,v) for k,_,v in mods['sb_court_claimant_mobilisation'])
        self.assertEqual('4',mobilisation['political_movement_activism_growth_mult'])
        native=(GAME/'common/trigger_localization/00_trigger_localization.txt').read_text(encoding='utf-8-sig')
        for key in ('political_movement_support','political_movement_popular_support',
                    'political_movement_military_support','political_movement_wealth_support'):
            self.assertIn(key+' = {',native)


if __name__ == '__main__': unittest.main()
