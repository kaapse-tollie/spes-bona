"""Execute the Crown appointment, law and garrison scripts in the recipient's scope."""
from copy import deepcopy
import unittest

from tests.test_colonial_government_and_bst_raids import GAME, ROOT, PatchRuntime, block
from tests.test_zulu_court_politics import definitions
from tests.test_zulu_frontier_followup import field

EFFECTS = definitions('common/scripted_effects/sb_crown_administration.txt')
IDENTITIES = definitions('common/scripted_effects/sb_interest_group_identity_effects.txt')
EFFECTS['sb_apply_british_garrison_identity'] = IDENTITIES['sb_apply_british_garrison_identity']
TRIGGERS = definitions('common/scripted_triggers/sb_crown_administration.txt')
ACTIONS = definitions('common/on_actions/sb_crown_administration.txt')
START = 'sb_establish_crown_administration'
CHECK = 'sb_check_crown_administration'
END = 'sb_end_crown_appointments'
LOCK = 'sb_can_reform_crown_bureaucracy'
NATAL = 'sb_natalia_british_colony_resolved_var'
MILITARY = 'law_military_bureaucrats'
APPOINTED = 'law_appointed_bureaucrats'
LEGACY = 'law_sb_imperial_administration'
AMENDMENT = 'amendment_sb_imperial_administration'
GENERIC = {'ideology_jingoist', 'ideology_loyalist', 'ideology_militarist'}
ANGLO = 'ideology_sb_anglo_colonialism'
LAW_GUARD = 'common/laws/sb_crown_administration_guard.txt'
DEACTIVATE = field(block(ROOT, LAW_GUARD, MILITARY, 'INJECT'), 'on_deactivate')


class CrownRuntime(PatchRuntime):
    def __init__(self, tag, law=APPOINTED, subject='subject_type_colony', overlord='GBR', british_natal=True):
        super().__init__([])
        self.country = {'id': tag, 'alive': True, 'vars': {}, 'law': 'law_type:' + law, 'overlord': overlord,
                        'is_subject_type': subject, 'is_country_type': 'colonial'}
        if tag == 'NAL' and british_natal:
            self.country['vars'][NATAL] = 1
        self.forces = {'owner': self.country, 'ideologies': GENERIC | {'earned'}, 'leader': 17,
                       'members': [17, 28], 'name': 'ig_armed_forces'}
        self.laws = {}
        self.queued = None

    def law_object(self, key):
        return self.laws.setdefault(key, {'type': key, 'amendments': []})

    def ref(self, key, scope, prev=None):
        if key.startswith('c:'):
            return self.country if key[2:] == self.country['id'] else None
        if key == 'ig:ig_armed_forces':
            return self.forces if scope is self.country else None
        if key == 'active_law:lawgroup_bureaucracy':
            return self.law_object(scope['law'])
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        for node in nodes:
            key, _, value = node
            if key in TRIGGERS:
                passed = self.condition(TRIGGERS[key], scope, prev) == (value == 'yes')
            elif key == 'NAND':
                passed = not self.condition(value, scope, prev)
            elif key == 'is_direct_subject_of':
                passed = scope['overlord'] == value.removeprefix('c:')
            elif key == 'has_ideology':
                passed = value.removeprefix('ideology:') in scope['ideologies']
            elif key == 'type':
                passed = scope['type'] == value
            elif key == 'has_amendment':
                passed = any(a['type'] == value for a in scope['amendments'])
            elif key == 'can_impose_law_default':
                passed = self.scopes['target_country']['overlord'] == scope['id']
            else:
                passed = super().condition([node], scope, prev)
            if not passed:
                return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, _, value = node
            if key in EFFECTS:
                self.effect(EFFECTS[key], scope, prev)
            elif key.startswith(('ig:', 'active_law:')):
                self.effect(value, self.ref(key, scope, prev), scope)
            elif key == 'set_interest_group_name':
                scope['name'] = value
            elif key == 'add_ideology':
                scope['ideologies'].add(value)
            elif key == 'remove_ideology':
                scope['ideologies'].remove(value)
            elif key == 'add_amendment':
                sponsor = self.ref(field(value, 'sponsor'), scope, prev)
                assert sponsor is self.forces
                scope['amendments'].append({'type': 'amendment_type:' + field(value, 'type')})
            elif key in ('every_law', 'every_scope_amendment'):
                items = self.laws.values() if key == 'every_law' else scope['amendments']
                for item in list(items):
                    if self.condition(field(value, 'limit'), item, scope):
                        self.effect([n for n in value if n[0] != 'limit'], item, scope)
            elif key == 'remove_amendment':
                prev['amendments'].remove(scope)
            else:
                super().effect([node], scope, prev)

    def run(self, name):
        if name in ACTIONS:
            action = ACTIONS[name]
            if self.condition(field(action, 'trigger'), self.country):
                self.effect(field(action, 'effect'), self.country)
        else:
            self.effect(EFFECTS[name], self.country)

    def amendments(self):
        return [a['type'] for a in self.law_object('law_type:' + MILITARY)['amendments']]


class CrownTransitions(unittest.TestCase):
    def test_new_colonies_and_pre_grant_repair_with_foreign_root(self):
        for tag, name in [('CAP', 'ig_sb_imperial_establishment'), ('NAL', 'ig_sb_colonial_garrison')]:
            rt = CrownRuntime(tag)
            for hook in (START, START, CHECK):
                rt.run(hook)
            self.assertEqual([f'amendment_type:{AMENDMENT}'], rt.amendments())
            self.assertFalse(rt.condition(TRIGGERS[LOCK], rt.country))
            self.assertEqual(name, rt.forces['name'])
            self.assertEqual({'earned', 'ideology_loyalist', 'ideology_militarist', 'ideology_sb_imperialist',
                              'ideology_patriotic', ANGLO}, rt.forces['ideologies'])
            rt.effect(DEACTIVATE, rt.country)
            rt.country['law'] = 'law_type:' + APPOINTED
            rt.law_object('law_type:' + MILITARY)['amendments'].clear()
            rt = deepcopy(rt)  # pending native delivery across a save boundary
            self.assertEqual((CHECK, 1), rt.queued)
            rt.run(rt.queued[0])
            self.assertEqual('law_type:' + MILITARY, rt.country['law'])
            self.assertEqual([f'amendment_type:{AMENDMENT}'], rt.amendments())

    def test_grant_then_independence_or_transfer_before_or_after_civilian_reform(self):
        for grant, reform in [(False, False), (True, False), (True, True)]:
            for overlord in (None, 'TRN'):
                rt = CrownRuntime('NAL')
                rt.run(START)
                rt.effect(DEACTIVATE, rt.country)
                if grant:
                    rt.run(END)
                    rt.country['is_subject_type'] = 'subject_type_sb_responsible_colony'
                    if reform:
                        rt.country['law'] = 'law_type:' + APPOINTED
                    rt.run(CHECK)
                    self.assertIn(ANGLO, rt.forces['ideologies'])
                rt.country['overlord'] = overlord
                rt.queued = None
                rt.run('sb_on_crown_relationship_changed')
                if overlord is None:
                    self.assertEqual((CHECK, 1), rt.queued)
                else:
                    self.assertIsNone(rt.queued)
                    self.assertEqual('ig_armed_forces', rt.forces['name'])
                rt = deepcopy(rt)
                rt.run(CHECK)
                self.assertTrue(rt.condition(TRIGGERS[LOCK], rt.country))
                self.assertEqual([], rt.amendments())
                self.assertEqual('law_type:' + (APPOINTED if reform else MILITARY), rt.country['law'])
                self.assertEqual(GENERIC | {'earned'}, rt.forces['ideologies'])
                self.assertEqual(('ig_armed_forces', 17, [17, 28]),
                                 (rt.forces['name'], rt.forces['leader'], rt.forces['members']))
                rt.country['overlord'] = 'GBR'
                for hook in (CHECK, START, 'sb_migrate_legacy_crown_administration'):
                    rt.run(hook)
                self.assertEqual([], rt.amendments())
                self.assertEqual(GENERIC | {'earned'}, rt.forces['ideologies'])

    def test_settled_overlord_and_reform_while_cleanup_is_pending(self):
        rt = CrownRuntime('CAP')
        rt.run(START)
        rt.country['overlord'] = None
        rt.run('sb_on_crown_relationship_changed')
        rt.country['overlord'] = 'GBR'
        rt.run(CHECK)
        self.assertFalse(rt.condition(TRIGGERS[LOCK], rt.country))
        self.assertIn(ANGLO, rt.forces['ideologies'])
        rt.country['overlord'] = 'TRN'
        rt.country['law'] = 'law_type:' + APPOINTED
        rt.run(CHECK)
        self.assertEqual('law_type:' + APPOINTED, rt.country['law'])
        self.assertEqual([], rt.amendments())

    def test_observed_transfer_and_responsible_pact_restoration(self):
        rt = CrownRuntime('CAP')
        rt.run(START)
        # A subject-type restoration can happen outside the diplomatic actions.
        rt.country['is_subject_type'] = 'subject_type_sb_responsible_colony'
        rt.run(CHECK)
        self.assertEqual([], rt.amendments())
        self.assertIn(ANGLO, rt.forces['ideologies'])
        rt.country['overlord'] = 'TRN'
        rt.run('sb_on_crown_relationship_changed')
        rt.country['overlord'] = 'GBR'
        rt.run('sb_on_crown_relationship_changed')
        rt.run(CHECK)
        self.assertEqual(GENERIC | {'earned'}, rt.forces['ideologies'])
        self.assertEqual([], rt.amendments())

    def test_only_legacy_holders_get_the_law_and_only_direct_ordinary_colonies_get_the_lock(self):
        for law in (LEGACY, APPOINTED):
            for subject in ('subject_type_colony', 'subject_type_sb_responsible_colony'):
                for overlord in ('GBR', None, 'TRN'):
                    rt = CrownRuntime('NAL', law, subject, overlord)
                    rt.forces['ideologies'].update({'ideology_colonialist', 'ideology_sb_boer_commando_republicanism'})
                    rt.run(CHECK)
                    rt.run(CHECK)
                    lock = law == LEGACY and overlord == 'GBR' and subject == 'subject_type_colony'
                    self.assertEqual(int(lock), len(rt.amendments()))
                    self.assertEqual(not lock, rt.condition(TRIGGERS[LOCK], rt.country))
                    self.assertEqual('law_type:' + (MILITARY if law == LEGACY else law), rt.country['law'])
                    self.assertEqual(overlord == 'GBR', ANGLO in rt.forces['ideologies'])
                    self.assertNotIn('ideology_sb_boer_commando_republicanism', rt.forces['ideologies'])

    def test_other_countries_and_company_platform(self):
        dead = CrownRuntime('NAL', LEGACY)
        dead.country['alive'] = False
        dead.run(CHECK)
        self.assertEqual('law_type:' + LEGACY, dead.country['law'])
        self.assertEqual({NATAL: 1}, dead.country['vars'])
        for tag in ('NAL', 'BSA', 'ORA', 'CAN'):
            rt = CrownRuntime(tag, british_natal=False)
            rt.run(CHECK)
            self.assertEqual({}, rt.country['vars'])
            self.assertTrue(rt.condition(TRIGGERS[LOCK], rt.country))
            if tag == 'BSA':
                rt.run('sb_apply_british_garrison_identity')
                self.assertIn('ideology_colonialist', rt.forces['ideologies'])
                self.assertNotIn(ANGLO, rt.forces['ideologies'])

    def test_imposition_uses_recipient_and_preserves_native_eligibility(self):
        cape = CrownRuntime('CAP')
        cape.run(START)
        cape.scopes['target_country'] = cape.country
        group = field(block(ROOT, 'common/law_groups/sb_crown_administration.txt',
                            'lawgroup_bureaucracy', 'INJECT'), 'change_allowed_trigger')
        self.assertFalse(cape.condition(group, cape.country))
        for law in ('law_hereditary_bureaucrats', 'law_crownland_diets', APPOINTED,
                    'law_elected_bureaucrats', 'law_communal_administration'):
            native = block(GAME, 'common/laws/00_bureaucracy.txt', law)
            self.assertNotIn('can_impose', [k for k, _, _ in native])
            gate = field(block(ROOT, LAW_GUARD, law, 'INJECT'), 'can_impose')
            self.assertFalse(cape.condition(gate, cape.scopes['root']))
            other = CrownRuntime('CAN').country
            cape.scopes['target_country'] = other
            self.assertTrue(cape.condition(gate, cape.scopes['root']))
            self.assertFalse(cape.condition(gate, {'id': 'FRA'}))
            cape.scopes['target_country'] = cape.country

    def test_amendment_platforms_and_vanilla_staffing(self):
        amendment = definitions('common/amendments/sb_amendments.txt')[AMENDMENT]
        self.assertEqual(MILITARY, field(amendment, 'parent'))
        self.assertEqual([(MILITARY, 'bare', MILITARY)], field(amendment, 'allowed_laws'))
        self.assertEqual([('country_liberty_desire_add', '=', '-0.10')], field(amendment, 'modifier'))
        rt = CrownRuntime('CAP')
        for key in ('would_sponsor', 'can_repeal', 'ai_will_revoke'):
            self.assertFalse(rt.condition(field(amendment, key), rt.country))
        military_pm = block(GAME, 'common/production_methods/07_government.txt', 'pm_military_bureaucrats')
        self.assertIn((MILITARY, 'bare', MILITARY), field(military_pm, 'unlocking_laws'))
        self.assertIn(('building_employment_officers_add', '=', '250'),
                      field(field(military_pm, 'building_modifiers'), 'level_scaled'))
        ideologies = definitions('common/ideologies/sb_ideologies.txt')
        colonialist = block(GAME, 'common/ideologies/00_ig_ideologies_flavored.txt', 'ideology_colonialist')
        self.assertEqual([n for n in colonialist if n[0] != 'lawgroup_colonization'],
                         [n for n in ideologies[ANGLO] if n[0] != 'lawgroup_colonization'])
        def ratings(ideology, group):
            return {k: v for k, _, v in field(ideologies[ideology], group)}
        self.assertEqual({'law_colonial_exploitation': 'strongly_approve', 'law_frontier_colonization': 'approve',
                          'law_colonial_resettlement': 'approve', 'law_internal_colonization': 'neutral',
                          'law_no_colonial_affairs': 'disapprove'}, ratings(ANGLO, 'lawgroup_colonization'))
        self.assertEqual({MILITARY: 'strongly_approve', 'law_hereditary_bureaucrats': 'neutral',
                          APPOINTED: 'disapprove', 'law_elected_bureaucrats': 'strongly_disapprove',
                          'law_communal_administration': 'strongly_disapprove'},
                         ratings('ideology_sb_imperialist', 'lawgroup_bureaucracy'))
        diets = block(GAME, 'common/laws/00_bureaucracy.txt', 'law_crownland_diets')
        self.assertEqual('law_hereditary_bureaucrats', field(diets, 'parent'))

    def test_both_natal_foundations_and_settlement_acknowledgement(self):
        founding = definitions('common/scripted_effects/sb_natalia_colony_effects.txt')
        common = 'sb_apply_british_natal_colony_setup'
        self.assertIn((common, '=', 'yes'), founding['sb_finalize_british_natal_colony'])
        self.assertIn((common, '=', 'yes'), field(founding['sb_found_natal_colony_after_british_annexation'], 'c:NAL'))
        first_setup = next(v for k, _, v in founding[common]
                           if k == 'if' and (START, '=', 'yes') in v)
        fresh = CrownRuntime('NAL')
        self.assertTrue(fresh.condition(field(first_setup, 'limit'), fresh.country))
        fresh.run(START)
        self.assertFalse(fresh.condition(field(first_setup, 'limit'), fresh.country))
        convert = founding['sb_convert_natalia_to_british_crown_colony']
        pact = next(field(field(v, 'c:GBR'), 'create_diplomatic_pact') for k, _, v in convert
                    if k == 'if' and any(n[0] == 'c:GBR' for n in v))
        self.assertEqual('prev', field(pact, 'country'))
        # Both a new colony and an existing protectorate may be settled from Britain's event.
        for old_overlord in (None, 'GBR', 'CAP'):
            rt = CrownRuntime('NAL', subject='subject_type_protectorate', overlord=old_overlord)
            country = rt.country
            for key, _, value in rt.branches(convert, country):
                if key == 'c:GBR':
                    for operation, _, target in value:
                        if operation == 'create_diplomatic_pact':
                            self.assertIs(country, rt.ref(field(target, 'country'), rt.scopes['root'], country))
                            country['is_subject_type'] = 'subject_type_' + field(target, 'type')
                        else:
                            self.assertEqual('transfer_subject', operation)
                            self.assertIs(country, rt.ref(target, rt.scopes['root'], country))
                        country['overlord'] = 'GBR'
                elif key == 'change_subject_type':
                    country['is_subject_type'] = value
            self.assertEqual(('GBR', 'subject_type_colony'), (country['overlord'], country['is_subject_type']))
        restoration = definitions('common/scripted_effects/sb_natalia_effects.txt')['sb_restore_natalia_after_boer_corridor_victory']
        rt = CrownRuntime('NAL')
        rt.run(START)
        rt.country['overlord'] = 'TRN'
        rt.country['vars'].pop(NATAL)
        rt.run(CHECK)
        def enabled(nodes, key, value):
            return (key, '=', value) in rt.branches(nodes, rt.country)
        self.assertFalse(enabled(restoration, 'activate_law', 'law_type:law_elected_bureaucrats'))
        force_block = next(v for k, _, v in IDENTITIES['sb_apply_boer_republic_interest_group_identity']
                           if k == 'if' and any(n[0] == 'ig:ig_armed_forces' for n in v))
        self.assertFalse(rt.condition(field(force_block, 'limit'), rt.country))
        boer = CrownRuntime('NAL', british_natal=False)
        self.assertTrue(boer.condition(field(force_block, 'limit'), boer.country))

    def test_petition_scores_refusal_and_shared_grant(self):
        actions = definitions('common/diplomatic_actions/sb_subject_autonomy_actions.txt')
        request = actions['sb_ask_responsible_government']
        grant = actions['sb_grant_responsible_government']
        handoff = 'sb_apply_responsible_colony_subject_type_from_overlord'
        self.assertIn((handoff, '=', 'yes'), field(request, 'accept_effect'))
        self.assertNotIn(handoff, str(field(request, 'decline_effect')))
        self.assertIn((handoff, '=', 'yes'), field(field(grant, 'accept_effect'), 'scope:target_country'))
        shared = definitions('common/scripted_effects/sb_subject_autonomy_effects.txt')[handoff]
        self.assertIn((END, '=', 'yes'), field(shared, 'if'))
        self.assertIn(('liberty_desire', '>=', '60'), field(field(field(grant, 'ai'), 'will_propose'), 'scope:target_country'))
        class ProtectiveOverlord(CrownRuntime):
            def condition(self, nodes, scope, prev=None):
                if len(nodes) == 1 and nodes[0][0] == 'has_attitude':
                    return field(nodes[0][2], 'attitude') == 'protective'
                return super().condition(nodes, scope, prev)
        rt = ProtectiveOverlord('CAP')
        recipient = rt.scopes['root']
        recipient.update({'"scope:actor.ai_ideological_opinion(root)"': 0,
                          '"scope:actor.potential_diplomatic_play_power_ratio(root)"': 0.25,
                          '"relations(scope:actor)"': 50, 'relations_threshold:friendly': 80,
                          'relations_threshold:amicable': 50, '"scope:actor.infamy"': 0,
                          'infamy_threshold:infamous': 25, 'infamy_threshold:notorious': 50,
                          'infamy_threshold:pariah': 100})
        for liberty, expected in [(60, 10), (70, 30)]:
            recipient['"scope:actor.liberty_desire"'] = liberty
            self.assertEqual(expected, rt.calc(field(field(request, 'ai'), 'accept_score'), recipient))
