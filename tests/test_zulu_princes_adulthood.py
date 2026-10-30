"""Source execution for Mpande's sons; native portraits and dates remain DP checks."""
import unittest

from tests.test_zulu_frontier_followup import FrontierRuntime, block, field
from tests.test_zulu_court_politics import character, EFFECTS, TRIGGERS
from tests.test_zulu_recognition_backing import RecognitionRuntime, add


def family(runtime=FrontierRuntime):
    rt = runtime()
    mpande = character('Mpande', 0, 45, -1, 1, age=38)
    mpande['template'] = 'ZUL_mpande_zulu'
    mpande['vars']['sb_court_claimant_scope'] = mpande
    sons = [character('Cetshwayo', 0, 40, 0, 1, age=15),
            character('Mbuyazi', 0, 30, 0, 1, age=14)]
    for son, template in zip(sons, ('ZUL_cetshwayo_heir', 'ZUL_mbuyazi_heir')):
        son['template'] = template
    for actor in [mpande, *sons]:
        actor['owner'] = rt.country
        actor['vars']['sb_court_home_scope'] = rt.country
        rt.country['members'].append(actor)
        rt.country['characters'].append(actor)
    return rt, mpande, sons


def pulse(rt):
    rt.effect(EFFECTS['sb_court_mpande_sons_come_of_age'], rt.country)


class PrincesAdulthoodTests(unittest.TestCase):
    def test_candidature_and_regency_use_the_same_native_adulthood(self):
        rt, father, (son, _) = family()
        rt.scopes['sb_court_country'] = rt.country
        rt.country['vars']['sb_court_minor_sovereign_scope'] = son
        regency = field(field(EFFECTS['sb_court_reconcile_regency'], 'if'), 'limit')
        for age, adult in ((15, False), (16, True)):
            son['age'] = age
            self.assertEqual(adult, rt.condition([('sb_court_adult_member','=','yes')], son))
            self.assertEqual(adult, rt.condition(regency, rt.country))

    def test_princes_careers_survive_birthdays_and_the_succession_crisis(self):
        from datetime import date
        from tests.test_zulu_court_politics import GAME, ROOT
        from tests.test_zulu_institutions_laws import statements
        from tools.check_override_inventory import find_object
        import re
        defines = (GAME/'common/defines/00_defines.txt').read_text(encoding='utf-8-sig')
        native_age = int(re.search(r"\bADULT_AGE = (\d+)", defines).group(1))
        self.assertEqual(16, native_age)
        for template, birth in [('REPLACE:ZUL_mpande_zulu', date(1797,7,9)),
                                ('ZUL_gqugqu_claimant', date(1808,1,1)),
                                ('ZUL_cetshwayo_heir', date(1826,4,27)),
                                ('ZUL_mbuyazi_heir', date(1828,1,1))]:
            source = (ROOT/'common/character_templates/sb_zulu_dynasty_characters.txt').read_text(encoding='utf-8-sig')
            data = statements(re.sub(r'traits\s*=\s*\{[^}]*\}', 'traits = { }', find_object(source, template)))
            years = int(field(field(field(data, 'on_created'), 'set_career_length'), 'years'))
            expiry = date(1836 + years, 1, 1)
            self.assertGreater(expiry, date(birth.year + native_age, birth.month, birth.day))
            self.assertGreater(expiry, date(1856,12,1))
            self.assertEqual('yes', field(data, 'historical'))
            # Retain native lifespan: the fix extends the role, not the character's health.
            self.assertNotIn('death_date', [k for k, _, _ in data])
            self.assertNotIn('immortal', str(data))

    def test_each_son_declares_once_at_adulthood_without_surrendering_his_claim(self):
        rt, father, (elder, younger) = family()
        pulse(rt)
        self.assertNotIn('events', rt.country)
        elder['age'] = 16
        pulse(rt)
        self.assertEqual(['sb_court_succession.003'], rt.country['events'])
        self.assertIs(father, elder['vars']['sb_court_claimant_scope'])
        self.assertEqual(-1, elder['vars']['sb_court_endorsement_var'])
        self.assertIn('sb_court_endorsement_claimant_trait', elder['traits'])
        self.assertEqual(0, younger['vars']['sb_court_endorsement_var'])
        self.assertEqual(1, elder['vars']['sb_court_alignment_var'])
        self.assertIn('charismatic', elder['traits'])
        self.assertIn('sb_court_claimant_trait', elder['traits'])
        self.assertNotIn('charismatic', younger.get('traits', set()))
        self.assertNotIn('sb_court_claim_renounced_var', elder['vars'])
        self.assertNotIn('sb_court_successor_pledge_scope', elder['vars'])
        own = elder['vars']['sb_court_represented_weight_var']
        self.assertEqual(own, elder['vars']['sb_court_coalition_weight_var'])
        self.assertEqual(own + father['vars']['sb_court_represented_weight_var'],
                         father['vars']['sb_court_current_weight_var'])
        self.assertEqual(0, elder['vars']['sb_court_current_weight_var'])
        elder['vars']['sb_court_endorsement_var'] = 0
        elder['vars'].pop('sb_court_claimant_scope')
        pulse(rt)
        self.assertEqual(0, elder['vars']['sb_court_endorsement_var'])
        younger['age'] = 16
        pulse(rt)
        self.assertIs(father, younger['vars']['sb_court_claimant_scope'])
        self.assertEqual(2, len(rt.country['events']))
        self.assertEqual(0, rt.country['vars']['sb_prerogative_var'])
        self.assertEqual('GBR', rt.scopes['root']['id'])
        self.assertNotIn('events', rt.scopes['root'])
        rt.backing()
        self.assertAlmostEqual(rt.country['vars']['sb_court_weight_var'],
            rt.country['vars']['sb_court_current_unpledged_weight_var'] +
            sum(m['vars']['sb_court_current_weight_var'] for m in rt.country['members']))

    def test_father_dead_absent_or_ruling_at_adulthood_does_not_defer_declaration(self):
        for state in ('dead', 'absent', 'ruler'):
            with self.subTest(state=state):
                rt, father, (son, _) = family()
                king = rt.country['ruler']
                son['age'] = 16
                if state == 'dead': father['alive'] = False
                elif state == 'absent': rt.country['members'].remove(father)
                else: rt.country['ruler'] = father
                pulse(rt)
                self.assertNotIn('events', rt.country)
                self.assertIn('sb_court_adulthood_checked_var', son['vars'])
                self.assertEqual(1 if state == 'ruler' else 0, son['vars']['sb_court_endorsement_var'])
                # Losing the throne later is not another coming of age.
                rt.country['ruler'] = king
                father['alive'] = True
                if state == 'absent': rt.country['members'].append(father)
                pulse(rt)
                self.assertNotIn('events', rt.country)

    def test_dead_son_minor_son_and_son_on_throne_never_pledge(self):
        for state in ('dead', 'minor', 'ruler'):
            rt, father, (son, _) = family()
            if state != 'minor': son['age'] = 16
            if state == 'dead': son['alive'] = False
            if state == 'ruler': rt.country['ruler'] = son
            pulse(rt)
            self.assertNotIn('events', rt.country, state)
            self.assertNotIn('sb_court_claimant_scope', son['vars'])

    def test_other_country_and_inactive_court_are_untouched(self):
        for inactive, tag in ((False, 'ORA'), (True, 'ZUL')):
            rt, _, (son, _) = family()
            son['age'] = 16
            rt.country['id'] = tag
            if inactive: rt.country['vars'].pop('sb_institutions_active_var')
            pulse(rt)
            self.assertNotIn('events', rt.country)
            self.assertNotIn('sb_court_adulthood_checked_var', son['vars'])
        rt, father, (son, _) = family()
        rt.country['id'] = 'NGN'
        rt.country['vars']['sb_ngu_inherited_zul_content_var'] = 1
        son['age'] = 16
        pulse(rt)
        self.assertIs(father, son['vars']['sb_court_claimant_scope'])

    def test_notification_cannot_apply_the_pledge_twice_or_use_dead_portraits(self):
        rt, father, (son, _) = family()
        son['age'] = 16
        pulse(rt)
        event = block('events/sb_court_succession_events.txt', 'sb_court_succession.003')
        self.assertTrue(rt.condition(field(event, 'trigger'), rt.country))
        father['alive'] = False
        self.assertFalse(rt.condition(field(event, 'trigger'), rt.country))
        self.assertEqual({'name', 'default_option', 'custom_tooltip'}, {k for k, _, _ in field(event, 'option')})

    def test_january_declaration_follows_the_annual_roll(self):
        rt, father, (son, _) = family()
        son['age'] = 16
        monthly = block('common/scripted_effects/sb_institutions_effects.txt', 'sb_institutions_monthly_update')
        active = next(v for k, _, v in monthly if k == 'if' and any(n[0] == 'sb_court_annual_allegiances' for n in v))
        calls = [k for k, _, _ in active]
        self.assertLess(calls.index('sb_court_annual_allegiances'), calls.index('sb_court_mpande_sons_come_of_age'))
        # An ordinary annual result is superseded by this one authored declaration.
        son['vars']['sb_court_endorsement_var'] = 1
        pulse(rt)
        self.assertIs(father, son['vars']['sb_court_claimant_scope'])
        pulse(rt)
        self.assertEqual(1, len(rt.country['events']))


class BrothersRuntime(RecognitionRuntime):
    def condition(self, nodes, scope, prev=None):
        for key, op, value in nodes:
            if key in TRIGGERS and isinstance(value, list):
                params = {k:v for k, _, v in value}
                def subst(node):
                    if isinstance(node, list): return [(subst(k), op, subst(v)) for k, op, v in node]
                    for param, val in params.items(): node = node.replace('$'+param+'$', val)
                    return node
                result = self.condition(subst(TRIGGERS[key]), scope, prev)
            elif key == 'any_in_list' and any(k == 'count' for k, _, _ in value):
                collection = 'members' if field(value, 'variable') == 'sb_court_members' else field(value, 'variable')
                count = sum(self.condition([n for n in value if n[0] not in ('variable', 'count')], item, scope)
                            for item in scope.get(collection, []))
                comparator, threshold = next((op, v) for k, op, v in value if k == 'count')
                assert comparator == '>='
                result = count >= int(threshold)
            else:
                result = super().condition([(key, op, value)], scope, prev)
            if not result: return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            if node[:2] == ('add_trait', '=') and node[2] == 'ambitious':
                scope.setdefault('traits', set()).add('ambitious')
            elif node[0] == 'custom_tooltip':
                self.tooltips.append(node[2])
            else:
                super().effect([node], scope, prev)


class BrothersChoiceTests(unittest.TestCase):
    def setup_court(self, heir=None):
        rt, father, (elder, younger) = family(BrothersRuntime)
        rt.tooltips = []
        rt.country['ruler'] = father
        elder['age'], younger['age'] = 18, 16
        rt.country['vars']['sb_prerogative_var'] = 5
        if heir is not None:
            rt.country['vars']['sb_court_recognized_heir_scope'] = (elder, younger)[heir]
            rt.country['heir'] = (elder, younger)[heir]
        highest = add(rt, 'High chief', 100, 1)
        lesser = add(rt, 'Lesser chief', 60, 1)
        return rt, father, (elder, younger), (highest, lesser)

    def open_event(self, rt):
        pulse(rt)
        event = block('events/sb_court_succession_events.txt', rt.country['events'][-1])
        self.assertTrue(rt.condition(field(event, 'trigger'), rt.country))
        rt.effect(field(event, 'immediate'), rt.country)
        return event

    def answer(self, rt, event, index=0):
        options = [v for k, _, v in event if k == 'option']
        rt.effect(field(options[index], 'hidden_effect'), rt.country)

    def test_both_unsettled_choices_recognise_and_reserve_the_rivals_house_once(self):
        for choice in (0, 1):
            rt, _, sons, (highest, lesser) = self.setup_court()
            event = self.open_event(rt)
            self.assertEqual(['sb_court_succession.006'], rt.country['events'])
            self.assertNotIn('ambitious', sons[1-choice].get('traits', set()))
            self.assertNotIn('sb_court_successor_pledge_scope', highest['vars'])
            self.assertEqual(5, rt.country['vars']['sb_prerogative_var'])
            self.assertFalse(rt.condition([('sb_court_recognisable_successor','=','yes')], sons[choice]))
            self.assertNotIn('innovative',sons[1].get('traits',set()))
            self.answer(rt, event, choice)
            self.assertIn('innovative',sons[1]['traits'])
            self.assertIs(sons[choice], rt.country['heir'])
            self.assertIs(sons[choice], rt.country['vars']['sb_court_recognized_heir_scope'])
            self.assertEqual(-20, rt.country['vars']['sb_prerogative_var'])
            self.assertIn('ambitious', sons[1-choice]['traits'])
            self.assertIs(sons[1-choice], highest['vars']['sb_court_successor_pledge_scope'])
            self.assertIs(sons[0], lesser['vars']['sb_court_successor_pledge_scope'])
            self.assertEqual(1, highest['vars']['sb_court_endorsement_var'])
            self.assertEqual(1, highest['vars']['sb_court_alignment_var'])
            self.answer(rt, event, choice)
            pulse(rt)
            self.assertEqual(-20, rt.country['vars']['sb_prerogative_var'])
            self.assertEqual(1, len(rt.country['events']))
            self.assertFalse(any(k.startswith('sb_court_brothers_') for k in rt.country['vars']))
            self.assertEqual({}, rt.scopes['root']['vars'])

    def test_each_existing_heir_keeps_his_appointment_without_another_charge(self):
        for heir in (0, 1):
            rt, _, sons, (highest, _) = self.setup_court(heir)
            event = self.open_event(rt)
            self.assertEqual(['sb_court_succession.007'], rt.country['events'])
            self.assertIs(sons[1-heir], rt.scopes['sb_court_brothers_other'])
            self.assertNotIn('innovative',sons[1].get('traits',set()))
            self.answer(rt, event)
            self.assertIn('innovative',sons[1]['traits'])
            self.assertIs(sons[heir], rt.country['heir'])
            self.assertIs(sons[1-heir], highest['vars']['sb_court_successor_pledge_scope'])
            self.assertIn('ambitious', sons[1-heir]['traits'])
            self.assertEqual(5, rt.country['vars']['sb_prerogative_var'])

    def test_sons_support_mpandes_reign_while_retaining_future_claims(self):
        rt, father, sons, houses = self.setup_court(1)
        self.open_event(rt)
        rt.backing()
        for son in sons:
            self.assertEqual(1, son['vars']['sb_court_endorsement_var'])
            self.assertNotIn('sb_court_claimant_scope', son['vars'])
            self.assertIn('sb_court_claimant_trait', son['traits'])
            self.assertIn('sb_court_endorsement_incumbent_trait', son['traits'])
            self.assertEqual(0, son['vars']['sb_court_current_weight_var'])
            self.assertGreater(son['vars']['sb_court_coalition_weight_var'], 0)
            self.assertFalse(rt.condition(TRIGGERS['sb_court_current_opposition_prince'], son))
            self.assertTrue(rt.condition(TRIGGERS['sb_court_episode_prince'], son))
        self.assertIn(sons[0], father['sb_court_current_supporters'])
        self.assertIn(sons[1], father['sb_court_current_supporters'])
        # A different ruler restores their eligibility as current opposition.
        rt.country['ruler'] = rt.country['members'][0]
        self.assertTrue(rt.condition(TRIGGERS['sb_court_current_opposition_prince'], sons[0]))

    def test_frozen_conflict_does_not_rewrite_sons_commitments(self):
        rt, _, sons, _ = self.setup_court(1)
        for flag in ('sb_court_accession_open_var', 'sb_court_dynastic_crisis_var', 'sb_court_civil_war_var'):
            sons[0]['vars'].update(sb_court_endorsement_var=-1, sb_court_claimant_scope=sons[0])
            rt.country['vars'][flag] = 1
            rt.effect(EFFECTS['sb_court_reconcile_mpande_sons'], rt.country)
            self.assertEqual(-1, sons[0]['vars']['sb_court_endorsement_var'])
            rt.country['vars'].pop(flag)

    def test_an_existing_backer_prevents_an_extra_grant_and_an_empty_pool_is_honest(self):
        rt, _, sons, (highest, lesser) = self.setup_court(0)
        lesser['vars']['sb_court_successor_pledge_scope'] = sons[1]
        event = self.open_event(rt)
        self.answer(rt, event)
        self.assertNotIn('sb_court_successor_pledge_scope', highest['vars'])
        self.assertIs(sons[1], lesser['vars']['sb_court_successor_pledge_scope'])
        rt, _, sons, houses = self.setup_court(0)
        for house in houses: house['vars']['sb_court_successor_pledge_scope'] = sons[0]
        event = self.open_event(rt)
        self.assertNotIn('sb_court_brothers_backer_scope', rt.country['vars'])
        preview = [n for n in field(event, 'option') if n[0] == 'sb_court_preview_brother_backing']
        rt.effect(preview, rt.country)
        self.assertEqual(['sb_court_succession.006.no_backer'], rt.tooltips)
        self.answer(rt, event)
        self.assertIn('ambitious', sons[1]['traits'])
        self.assertTrue(all(h['vars']['sb_court_successor_pledge_scope'] is sons[0] for h in houses))

    def test_rival_cetshwayo_receives_two_new_houses_without_stealing_pledges(self):
        for existing in (0, 1, 2):
            rt, _, sons, (highest, lesser) = self.setup_court(1)
            for i in range(existing):
                backer = add(rt, 'Existing '+str(i), 30)
                backer['vars']['sb_court_successor_pledge_scope'] = sons[0]
            pledged_to_heir = add(rt, 'Heir backer', 200)
            pledged_to_heir['vars']['sb_court_successor_pledge_scope'] = sons[1]
            event = self.open_event(rt)
            preview = [n for n in field(event, 'option') if n[0] == 'sb_court_preview_brother_backing']
            rt.effect(preview, rt.country)
            self.assertEqual(2, len(rt.tooltips))
            self.answer(rt, event)
            backers = [m for m in rt.country['members'] if m['vars'].get('sb_court_successor_pledge_scope') is sons[0]]
            self.assertEqual(existing + 2, len(backers))
            self.assertIs(sons[1], pledged_to_heir['vars']['sb_court_successor_pledge_scope'])
            self.assertEqual(1, highest['vars']['sb_court_endorsement_var'])

    def test_house_ranking_uses_combined_prominence_and_counts_shared_house_once(self):
        rt, _, sons, (highest, lesser) = self.setup_court(1)
        lesser['vars']['sb_court_following_var'] = 20
        junior = add(rt, 'Junior member', 55, following=20)
        event = self.open_event(rt)
        self.assertIs(lesser, rt.country['vars']['sb_court_brothers_backer_scope'])
        self.assertIs(highest, rt.country['vars']['sb_court_brothers_second_backer_scope'])
        self.answer(rt, event)
        self.assertIs(sons[0], lesser['vars']['sb_court_successor_pledge_scope'])
        self.assertNotIn('sb_court_successor_pledge_scope', junior['vars'])

    def test_cetshwayo_second_frozen_house_can_fill_a_gap_without_replacing_stale_first(self):
        rt, _, sons, (highest, lesser) = self.setup_court(1)
        event = self.open_event(rt)
        highest['vars']['sb_court_successor_pledge_scope'] = sons[1]
        outsider = add(rt, 'Later house', 300)
        self.answer(rt, event)
        self.assertIs(sons[1], highest['vars']['sb_court_successor_pledge_scope'])
        self.assertIs(sons[0], lesser['vars']['sb_court_successor_pledge_scope'])
        self.assertNotIn('sb_court_successor_pledge_scope', outsider['vars'])

    def test_ineligible_notables_do_not_take_the_unpledged_house_slot(self):
        rt, _, sons, (highest, _) = self.setup_court(0)
        for state in ('agitator', 'dead', 'foreign', 'zero', 'prince', 'pledged'):
            actor = add(rt, state, 400)
            if state == 'agitator': actor['agitator'] = True
            elif state == 'dead': actor['alive'] = False
            elif state == 'foreign': actor['owner'] = rt.scopes['root']
            elif state == 'zero': actor['prominence'] = 0
            elif state == 'prince': actor['template'] = 'ZUL_gqugqu_claimant'
            else: actor['vars']['sb_court_successor_pledge_scope'] = sons[0]
        event = self.open_event(rt)
        self.assertIs(highest, rt.country['vars']['sb_court_brothers_backer_scope'])
        self.answer(rt, event)
        self.assertIs(sons[1], highest['vars']['sb_court_successor_pledge_scope'])

    def test_stale_participants_cancel_without_payment_or_substitution(self):
        for change in ('king', 'dead_son', 'renunciation', 'heir'):
            rt, _, sons, (highest, _) = self.setup_court()
            event = self.open_event(rt)
            if change == 'king': rt.country['ruler'] = rt.country['members'][0]
            elif change == 'dead_son': sons[1]['alive'] = False
            elif change == 'renunciation': sons[1]['vars']['sb_court_claim_renounced_var'] = 1
            else: rt.country['vars']['sb_court_recognized_heir_scope'] = sons[0]
            self.assertTrue(rt.condition(field(event, 'cancellation_trigger'), rt.country), change)
            self.answer(rt, event)
            self.assertEqual(5, rt.country['vars']['sb_prerogative_var'])
            self.assertNotIn('sb_court_successor_pledge_scope', highest['vars'])
            self.assertNotIn('ambitious', sons[1].get('traits', set()))
            self.assertNotIn('sb_court_brothers_choice_var', rt.country['vars'])
        rt, _, sons, (highest, lesser) = self.setup_court(0)
        event = self.open_event(rt)
        highest['vars']['sb_court_successor_pledge_scope'] = sons[0]
        self.answer(rt, event)
        self.assertIs(sons[0], highest['vars']['sb_court_successor_pledge_scope'])
        self.assertNotIn('sb_court_successor_pledge_scope', lesser['vars'])

    def test_no_birthday_replay_after_later_accession_or_with_another_heir(self):
        rt, father, sons, _ = self.setup_court()
        rt.country['ruler'] = rt.country['members'][0]
        pulse(rt)
        rt.country['events'] = []
        rt.country['ruler'] = father
        pulse(rt)
        self.assertEqual([], rt.country['events'])
        rt, _, sons, _ = self.setup_court()
        other = add(rt, 'Other prince', 80, template='ZUL_gqugqu_claimant')
        rt.country['vars']['sb_court_recognized_heir_scope'] = other
        pulse(rt)
        self.assertNotIn('events', rt.country)
        self.assertIs(other, rt.country['vars']['sb_court_recognized_heir_scope'])

    def test_native_portraits_ai_weights_and_post_cancellation_cleanup(self):
        rt, _, sons, _ = self.setup_court()
        event = self.open_event(rt)
        self.assertEqual('event_window_2char', field(event, 'gui_window'))
        options = [v for k, _, v in event if k == 'option']
        self.assertEqual(['33', '66'], [field(field(o, 'ai_chance'), 'base') for o in options])
        sons[0]['alive'] = False
        monthly = block('common/scripted_effects/sb_institutions_effects.txt', 'sb_institutions_monthly_update')
        cleanup = next(n for n in monthly if n[0] == 'if' and ('has_variable', '=', 'sb_court_brothers_choice_var') in field(n[2], 'limit'))
        rt.effect([cleanup], rt.country)
        self.assertFalse(any(k.startswith('sb_court_brothers_') for k in rt.country['vars']))


if __name__ == '__main__':
    unittest.main()
