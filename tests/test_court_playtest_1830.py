"""25 October hover regressions: execute previews without applying their mutations."""
from pathlib import Path
import re
import unittest

from tests.test_zulu_court_politics import CourtRuntime, character
from tests.test_zulu_court_event_package import EventRuntime, EVENTS, fields
from tests.test_zulu_court_rework import court
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import find_object

ROOT = Path(__file__).resolve().parents[1]


class StrictCourt(CourtRuntime):
    def condition(self, nodes, scope, prev=None):
        for key, op, value in nodes:
            if isinstance(value, str) and value.startswith('var:') and key.startswith('var:'):
                if self.ref(key, scope, prev) is not None and self.ref(value, scope, prev) is None:
                    raise AssertionError('Invalid right side during comparison: ' + value)
        return super().condition(nodes, scope, prev)


class ReportPreview(EventRuntime):
    def __init__(self, members):
        super().__init__(members)
        self.lines = []

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, _, value = node
            if key == 'save_scope_as':
                continue  # Tooltip construction does not execute this write.
            if key == 'show_as_tooltip':
                self.effect(value, scope, prev)
            elif key == 'custom_tooltip':
                self.lines.append((value, scope))
            else:
                super().effect([node], scope, prev)


class RefusalRuntime(CourtRuntime):
    def __init__(self, preview=False):
        super().__init__([])
        self.zul = self.country
        self.ora = {'id': 'ORA', 'vars': {}}
        self.scopes['root'] = self.zul
        self.containers = {}
        self.preview = preview
        self.scheduled = []

    def ref(self, key, scope, prev=None):
        if key == 'c:ZUL': return self.zul
        if key == 'c:ORA': return self.ora
        if key.startswith('container:'):
            name = key.split(':', 1)[1]
            if name not in self.containers: raise AssertionError('Missing container: ' + name)
            return self.containers[name]
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        results = []
        for node in nodes:
            key, _, value = node
            if key == 'container_exists': result = value in self.containers
            elif key == 'country_definition': result = value == 'cd:' + scope['id']
            elif key == 'is_country_alive': result = value == 'yes'
            elif key == 'is_subject': result = value == 'no'
            else: result = super().condition([node], scope, prev)
            results.append(result)
        return all(results)

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, _, value = node
            if self.preview and key in ('create_container', 'set_variable', 'save_scope_as'): continue
            if key == 'create_container':
                f = fields(value)
                obj = {'id': f['name'], 'vars': {}, 'parent': self.ref(f['parent'], scope, prev)}
                self.containers[f['name']] = obj
                self.effect(f['on_created'], obj, scope)
            elif key == 'random_scope_character':
                limit = fields(value).get('limit', [])
                eligible = [actor for actor in scope.get('characters', []) if self.condition(limit, actor, scope)]
                if eligible:
                    self.effect([n for n in value if n[0] != 'limit'], eligible[0], scope)
            elif key.startswith(('c:', 'container:')):
                self.effect(value, self.ref(key, scope, prev), scope)
            elif key == 'trigger_event':
                self.scheduled.append((scope['id'], fields(value)))
            else: super().effect([node], scope, prev)


class CourtPlaytest1830(unittest.TestCase):
    def test_personal_rival_without_future_pledge_counts_once_without_invalid_rhs(self):
        king = character('king', 1, 50, 1)
        prince = character('prince', 0, 30, -1, 1)
        prince['template'] = 'ZUL_mpande_zulu'
        prince['vars']['sb_court_claimant_scope'] = prince
        backer = character('house', 2, 40, -1)
        backer['vars']['sb_court_claimant_scope'] = prince
        rt = StrictCourt([king, prince, backer])
        for pledged in (False, True, False):
            if pledged: backer['vars']['sb_court_successor_pledge_scope'] = prince
            else: backer['vars'].pop('sb_court_successor_pledge_scope', None)
            rt.backing()
            self.assertEqual(95, prince['vars']['sb_court_rival_weight_var'])
            self.assertEqual(95, prince['vars']['sb_court_current_weight_var'])
            self.assertEqual(95 if pledged else 55, prince['vars']['sb_court_coalition_weight_var'])

    def test_roster_has_country_root_and_rejects_expired_character_handles(self):
        rt, king, prince, chief = court()
        for section in ('allegiance', 'candidate', 'commander', 'councillor', 'member'):
            self.assertFalse(rt.roster_shown('sb_court_roster_' + section, None))
        self.assertTrue(rt.roster_shown('sb_court_roster_candidate', prince))
        self.assertTrue(rt.roster_shown('sb_court_roster_member', chief))
        gui = (ROOT/'gui/sb_prerogative_progress_bars.gui').read_text(encoding='utf-8-sig') + (ROOT/'gui/sb_court_house_roster.gui').read_text(encoding='utf-8-sig')
        calls = [line for line in gui.splitlines() if "GetScriptedGui('sb_court_roster_" in line]
        self.assertEqual(5, len(calls))
        for call in calls:
            self.assertTrue('SetRoot(JournalEntry.GetCountry.MakeScope)' in call or 'SetRoot(Country.MakeScope)' in call)
            self.assertNotIn('GetPlayer', call)
            self.assertIn('Scope.GetCharacter.IsValid', call)

    def test_annual_report_lists_only_changed_records_in_current_scope(self):
        rt = ReportPreview([character('king', 1, 50, 1), character('chief', 2, 30)])
        actor = rt.country['members'][1]
        for record in ('current', 'future'):
            actor['vars']['sb_court_annual_old_' + record + '_scope'] = rt.country['ruler']
            actor['vars']['sb_court_annual_new_' + record + '_scope'] = actor
        option = next(v for k,_,v in EVENTS['sb_zulu_court.200'] if k == 'option')
        preview = [node for node in option if node[0] == 'show_as_tooltip']
        for current, future in ((False, False), (True, False), (False, True), (True, True)):
            rt.lines = []
            rt.country['sb_court_annual_current_changes'] = [actor] if current else []
            rt.country['sb_court_annual_future_changes'] = [actor] if future else []
            rt.effect(preview, rt.country)
            expected = [('sb_court_annual_' + kind + '_change_tt', actor)
                        for kind,changed in (('current',current),('future',future)) if changed]
            self.assertEqual(expected, rt.lines)
            self.assertNotIn('sb_court_report_actor', rt.scopes)
        loc = (ROOT/'localization/english/sb_zulu_court_l_english.yml').read_text(encoding='utf-8-sig')
        self.assertIn('[THIS.GetCharacter.GetFullName]', loc)
        self.assertNotIn("SCOPE.sCharacter('sb_court_report_actor')", loc)

    def test_annual_report_uses_direct_names_for_join_withdraw_and_switch(self):
        rt = ReportPreview([character('king', 1, 50, 1), character('chief', 2, 30)])
        king, actor = rt.country['members']
        option = next(v for k,_,v in EVENTS['sb_zulu_court.200'] if k == 'option')
        preview = [n for n in option if n[0] == 'show_as_tooltip']
        loc = (ROOT/'localization/english/sb_zulu_court_l_english.yml').read_text(encoding='utf-8-sig')
        for record in ('current', 'future'):
            rt.country['sb_court_annual_current_changes'] = []
            rt.country['sb_court_annual_future_changes'] = []
            rt.country['sb_court_annual_' + record + '_changes'] = [actor]
            for old, new, suffix in ((None, king, 'joined'), (king, None, 'withdrew'),
                                     (king, actor, 'change'), (None, None, None)):
                with self.subTest(record=record, suffix=suffix):
                    actor['vars']['sb_court_annual_old_' + record + '_scope'] = old
                    actor['vars']['sb_court_annual_new_' + record + '_scope'] = new
                    rt.lines = []
                    rt.effect(preview, rt.country)
                    key = 'sb_court_annual_' + record + '_' + str(suffix) + '_tt'
                    self.assertEqual([(key, actor)] if suffix else [], rt.lines)
                    if suffix:
                        row = next(line for line in loc.splitlines() if line.lstrip().startswith(key + ':'))
                        self.assertNotIn('GetCustom', row)
                        for state, target in (('old', old), ('new', new)):
                            self.assertEqual(target is not None, 'sb_court_annual_' + state + '_' + record + '_scope' in row)
        desc = fields(EVENTS['sb_zulu_court.200'])['desc']
        self.assertIn('first_valid', fields(desc))
        for key in ('sb_zulu_court.200.d', 'sb_zulu_court.200.d.chiefs'):
            row = next(line for line in loc.splitlines() if line.lstrip().startswith(key + ':'))
            self.assertNotIn('GetCustom', row)
            if key == 'sb_zulu_court.200.d':
                self.assertIn("SCOPE.sCharacter('sb_court_episode_ruler')", row)

    def test_refusal_preview_does_not_dereference_uncreated_container(self):
        source = (ROOT/'common/scripted_effects/sb_story_war_effects.txt').read_text(encoding='utf-8-sig')
        nodes = statements(re.sub(r'tags\s*=\s*\{[^}]*\}', '', find_object(source, 'sb_natal_story_begin_refusal_generation')))
        preview = RefusalRuntime(preview=True)
        preview.effect(nodes, preview.ora)
        self.assertEqual({}, preview.containers)
        self.assertEqual([], preview.scheduled)
        actual = RefusalRuntime()
        actual.effect(nodes, actual.ora)
        receipt = actual.containers['sb_natal_refusal_generation_state']
        self.assertIs(actual.ora, receipt['parent'])
        self.assertIs(actual.ora, receipt['vars']['sb_natal_refusal_generation_actor_scope'])
        self.assertIs(actual.zul, receipt['vars']['sb_natal_refusal_generation_counterparty_scope'])
        for country in (actual.ora, actual.zul):
            self.assertIs(receipt, country['vars']['sb_natal_refusal_generation_scope'])
        self.assertEqual([30,45,125,731], [int(f['days']) for tag,f in actual.scheduled if tag == 'ORA'])
        self.assertEqual([31,46,126,732], [int(f['days']) for tag,f in actual.scheduled if tag == 'ZUL'])
        event = (ROOT/'events/sb_natal_crisis_events.txt').read_text(encoding='utf-8-sig')
        kill = next(v for k,_,v in statements(find_object(event, 'sb_natal_crisis.020'))
                    if k == 'option' and fields(v)['name'] == 'sb_natal_crisis.020.b')
        boer = fields(kill)['scope:boer_republic']
        self.assertNotIn('trigger_event', fields(boer))
        hidden = fields(boer)['hidden_effect']
        self.assertIn('sb_natal_story_begin_refusal_generation', fields(hidden))
        self.assertIn('sb_natal_crisis.050', str(hidden))

    def test_all_incident_quotes_and_debits_share_doubled_capacity_prices(self):
        from tests.test_zulu_court_event_package import CourtDeckAndChoices
        for card,answer,fraction in ((211,'b',.2),(214,'c',.3),(215,'b',.4)):
            rt,*_ = CourtDeckAndChoices().deliver(card)
            price = rt.country['gold_reserves_limit'] * fraction
            self.assertEqual(price, rt.country['vars']['sb_court_episode_price_var'])
            cash = rt.country['gold_reserves']
            self.assertTrue(rt.answer(card, answer))
            self.assertEqual(cash - price, rt.country['gold_reserves'])

    def test_retief_allegiance_tooltip_requires_the_same_two_eligible_people_as_execution(self):
        from tests.test_zulu_court_event_package import setup, EFFECTS
        source=(ROOT/'events/sb_natal_crisis_events.txt').read_text(encoding='utf-8-sig')
        event=statements(find_object(source,'sb_natal_crisis.020'))
        option=next(v for k,_,v in event if k=='option' and fields(v)['name']=='sb_natal_crisis.020.c')
        for neutral_present,rival_present in ((False,False),(True,False),(False,True),(True,True)):
            base,king,p,r,chiefs=setup()
            rt=ReportPreview([])
            rt.country=base.country;rt.scopes=base.scopes
            c=chiefs[0]
            if neutral_present:rt.scopes['sb_court_frontier_neutral']=c
            if rival_present:rt.scopes['sb_court_frontier_rival']=p
            rt.effect([node for node in option if node[0] in ('if','custom_tooltip')],rt.country)
            keys=[key for key,_ in rt.lines]
            self.assertEqual(neutral_present and rival_present,'sb_court_frontier_allegiance_tt' in keys)
            self.assertNotIn('sb_court_frontier_neutral_named_tt',keys)
            self.assertNotIn('sb_court_frontier_rival_named_tt',keys)
            base.effect(EFFECTS['sb_court_frontier_opposition'],base.country)
            self.assertEqual(-1 if neutral_present and rival_present else 0,c['vars']['sb_court_endorsement_var'])
            if neutral_present and rival_present:self.assertIs(p,c['vars']['sb_court_claimant_scope'])
            self.assertEqual({},rt.scopes['root']['vars'])

    def test_retief_portraits_capture_both_actual_people_and_execute_the_displayed_envoy(self):
        source = (ROOT/'events/sb_natal_crisis_events.txt').read_text(encoding='utf-8-sig')
        event = statements(find_object(source, 'sb_natal_crisis.020'))
        definition = fields(event)
        self.assertEqual('event_window_2char', definition['gui_window'])
        rt = RefusalRuntime()
        king = character('king', 1, 50, 1)
        retief = character('retief', 0, 50)
        retief['template'] = 'ORA_piet_retief'
        other = character('other_envoy', 0, 90)
        dead = character('dead_retief', 0, 50, alive=False)
        dead['template'] = 'ORA_piet_retief'
        rt.zul['ruler'] = king
        rt.ora['characters'] = [other, dead, retief]
        rt.scopes['root'] = rt.ora
        presentation = [n for n in definition['immediate'] if n[0] != 'sb_court_prepare_frontier_choice']
        rt.effect(presentation, rt.zul)
        self.assertIs(king, rt.ref(definition['left_icon'], rt.zul))
        self.assertIs(retief, rt.ref(definition['right_icon'], rt.zul))
        kill = next(v for k,_,v in event if k == 'option' and fields(v)['name'] == 'sb_natal_crisis.020.b')
        rt.effect([n for n in fields(kill)['scope:boer_republic'] if n[0] != 'hidden_effect'], rt.ora)
        self.assertFalse(retief['alive'])
        self.assertTrue(other['alive'])
        self.assertTrue(king['alive'])

    def test_court_choice_labels_disambiguate_people_by_full_name(self):
        loc=(ROOT/'localization/english/sb_zulu_court_l_english.yml').read_text(encoding='utf-8-sig')
        for key in ('sb_zulu_court.210.b','sb_zulu_court.210.c','sb_zulu_court.214.a','sb_zulu_court.214.b'):
            line=next(line for line in loc.splitlines() if line.startswith(key+':'))
            self.assertIn('.GetFullName]',line)
            self.assertNotIn('.GetFirstName]',line)

    def test_nobility_is_authored_for_dynasts_and_chiefs_not_every_court_member(self):
        templates = {}
        for file in (ROOT/'common/character_templates').glob('*.txt'):
            text = file.read_text(encoding='utf-8-sig')
            for name in re.findall(r'(?m)^((?:REPLACE:)?[A-Za-z0-9_]+)\s*=\s*\{', text):
                templates[name] = find_object(text, name)
        nobles = ('REPLACE:ZUL_dingane', 'REPLACE:ZUL_mpande_zulu', 'ZUL_gqugqu_claimant',
                  'ZUL_cetshwayo_heir', 'ZUL_mbuyazi_heir', 'ZUL_dinuzulu_heir', 'ZUL_solomon_heir',
                  'REPLACE:ZUL_mkabayi', 'SB_ZUL_mawa', 'SB_ZUL_hamu',
                  'REPLACE:ZUL_ndlela_kasompisi', 'REPLACE:ZUL_zulu_kanogandaya',
                  'SB_ZUL_godide', 'SB_ZUL_mnyamana', 'SB_ZUL_maphitha',
                  'SB_ZUL_sekethwayo', 'SB_ZUL_masiphula')
        for name in nobles:
            self.assertIn('noble = yes', templates[name], name)
        for name in ('SB_ZUL_dambuza', 'SB_ZUL_sotobe', 'SB_ZUL_nongalaza', 'SB_ZUL_john_dunn'):
            self.assertNotIn('noble = yes', templates[name], name)
        for name in ('ZUL_uthumbu_claimed_son', 'ZUL_mbuyazi_successor', 'ZUL_uthumbu_successor'):
            self.assertIn('historical = no', templates[name])
        effects = (ROOT/'common/scripted_effects/sb_court_politics_effects.txt').read_text(encoding='utf-8-sig')
        blocks = statements(find_object(effects, 'sb_court_ensure_roster'))
        registration = next(body for key, _, body in blocks if key == 'every_scope_character'
                            and any(field == 'limit' and ('has_template', '=', 'ZUL_zibhebhu_kamaphitha') in limits
                                    for field, _, limits in body))
        self.assertIn(('set_is_noble', '=', 'yes'), registration)
        self.assertIn(('NOT', '=', [('has_variable', '=', 'sb_court_registered_var')]),
                      next(limits for key, _, limits in registration if key == 'limit'))
        cast = (ROOT/'common/scripted_effects/sb_court_cast_effects.txt').read_text(encoding='utf-8-sig')
        self.assertNotIn('set_is_noble', find_object(cast, 'sb_court_register_unpledged_cast'))
        for file in (ROOT/'common/character_interactions').glob('*.txt'):
            self.assertNotRegex(file.read_text(encoding='utf-8-sig'), r'(?m)^\s*(?:REPLACE:|INJECT:)?grant_peerage\s*=')
