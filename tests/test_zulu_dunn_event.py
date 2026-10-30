"""Execute Dunn's dated visit, identity reuse and button-only succession pledge."""
import re
import unittest

from tests.test_zulu_frontier_followup import FrontierRuntime, ROOT, field
from tests.test_zulu_court_politics import character, definitions
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import find_object


DUNN_EFFECTS = definitions('common/scripted_effects/sb_court_dunn_effects.txt')
DUNN_TRIGGERS = definitions('common/scripted_triggers/sb_court_dunn_triggers.txt')


class DunnRuntime(FrontierRuntime):
    def __init__(self, date=18550101):
        super().__init__()
        self.country['game_date'] = date
        self.country['ruler']['template'] = 'ZUL_mpande_zulu'
        self.countries['c:NAL'] = {'id':'NAL','alive':True,'vars':{'sb_natalia_british_colony_resolved_var':1,'sb_klip_river_county_resolved_var':1}}
        self.countries['c:GBR'] = {'id':'GBR','alive':True,'vars':{},'subjects':[self.countries['c:NAL']]}

        self.used_templates = set()
        self.cetshwayo = self.actor('ZUL_cetshwayo_heir', 0, 30, 1)
        self.mbuyazi = self.actor('ZUL_mbuyazi_heir', 0, 28, 1)

    def actor(self, template, house=7, age=30, alignment=0):
        actor = character(template, house, 20, alignment=alignment, age=age)
        actor.update(template=template, owner=self.country)
        actor['vars']['sb_court_home_scope'] = self.country
        self.country['members'].append(actor)
        self.country['characters'].append(actor)
        self.used_templates.add(template)
        return actor

    def ref(self, key, scope, prev=None):
        if re.fullmatch(r'\d{4}\.\d{1,2}\.\d{1,2}', key):
            y, m, d = map(int, key.split('.'))
            return y*10000+m*100+d
        return super().ref(key, scope, prev)

    def condition(self, nodes, scope, prev=None):
        for node in nodes:
            key, _, value = node
            if key in DUNN_TRIGGERS:
                result = self.condition(DUNN_TRIGGERS[key], scope, prev) == (value == 'yes')
            elif key == 'any_subject_or_below': result = any(self.condition(value,c,scope) for c in scope.get('subjects',[]))
            elif key == 'is_template_used': result = value in self.used_templates
            else: result = super().condition([node], scope, prev)
            if not result: return False
        return True

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, _, value = node
            if key == 'create_character':
                actor = self.actor(field(value, 'template'))
                # Registration runs from the actual callback; duplicate list entries are guarded.
                actor['vars'] = {}
                self.created += 1
                self.effect(field(value, 'on_created'), actor, scope)
                for k,_,v in value:
                    if k == 'save_scope_as': self.scopes[v] = actor
            elif key == 'transfer_character': scope['owner'] = self.ref(value,scope,prev)
            elif key == 'change_relations': scope.setdefault('relations',{})[field(value,'country')] = float(field(value,'value'))
            elif key == 'add_character_role': scope.setdefault('roles', set()).add(value)
            elif key == 'trigger_event':
                fields = dict((k,v) for k,_,v in value)
                scope.setdefault('event_schedule', []).append((fields['id'], int(fields.get('days',0))))
                super().effect([node], scope, prev)
            elif key == 'sb_institutions_recalculate': self.backing()
            else: super().effect([node], scope, prev)

    def run(self, name, scope=None): self.effect(DUNN_EFFECTS[name], scope if scope is not None else self.country)


class DunnVisitTests(unittest.TestCase):
    def test_dated_intro_does_not_pledge_until_acknowledged(self):
        rt = DunnRuntime(18541231)
        rt.run('sb_court_prepare_dunn_offer')
        self.assertEqual(0, rt.created)
        rt.country['game_date'] = 18550101
        rt.run('sb_court_prepare_dunn_offer')
        dunn = rt.country['vars']['sb_court_dunn_visitor_scope']
        self.assertEqual(1, rt.created)
        self.assertEqual(7, dunn['vars']['sb_court_following_var'])
        self.assertNotIn('sb_court_successor_pledge_scope', dunn['vars'])
        self.assertEqual(['sb_court_dunn.001'], rt.country['events'])
        rt.run('sb_court_prepare_dunn_offer')
        self.assertEqual(1, len(rt.country['events']))
        rt.run('sb_court_accept_dunn_offer')
        self.assertIs(rt.mbuyazi, dunn['vars']['sb_court_successor_pledge_scope'])
        self.assertEqual(0, dunn['vars']['sb_court_endorsement_var'])
        self.assertNotIn('sb_court_dunn_offer_var', rt.country['vars'])
        rt.run('sb_court_accept_dunn_offer')
        rt.run('sb_court_prepare_dunn_offer')
        self.assertEqual(1, rt.created)
        self.assertEqual(2, len(rt.country['events']))
        self.assertEqual({}, rt.scopes['root']['vars'])

    def test_existing_identity_reused_without_changing_present_allegiance(self):
        rt = DunnRuntime()
        dunn = rt.actor('SB_ZUL_john_dunn')
        dunn['vars']['sb_court_endorsement_var'] = 1
        rt.run('sb_court_prepare_dunn_offer')
        rt.run('sb_court_accept_dunn_offer')
        self.assertEqual(0, rt.created)
        self.assertIs(rt.mbuyazi, dunn['vars']['sb_court_successor_pledge_scope'])
        self.assertEqual(1, dunn['vars']['sb_court_endorsement_var'])
        self.assertIn('sb_court_john_dunn_created_var', rt.global_vars)

    def test_dead_or_foreign_dunn_is_not_recreated_or_transferred(self):
        for invalid in ('dead', 'foreign', 'created_receipt'):
            rt = DunnRuntime()
            if invalid == 'created_receipt': rt.global_vars['sb_court_john_dunn_created_var'] = 1
            else:
                dunn = rt.actor('SB_ZUL_john_dunn')
                if invalid == 'dead': dunn['alive'] = False
                else:
                    rt.country['characters'].remove(dunn)
                    dunn['owner'] = rt.scopes['root']
            rt.run('sb_court_prepare_dunn_offer')
            self.assertEqual(0, rt.created, invalid)
            self.assertNotIn('events', rt.country, invalid)
            self.assertNotIn('sb_court_dunn_offer_var', rt.country['vars'], invalid)

    def test_ineligible_courts_and_absent_rival_have_no_visit(self):
        for invalid in ('country', 'inactive', 'ruler', 'minor', 'renounced', 'crisis', 'accession'):
            rt = DunnRuntime()
            if invalid == 'country': rt.country['id'] = 'FRA'
            elif invalid == 'inactive': rt.country['vars'].pop('sb_institutions_active_var')
            elif invalid == 'ruler': rt.country['ruler']['template'] = 'ZUL_dingane'
            elif invalid == 'minor': rt.mbuyazi['age'] = 15
            elif invalid == 'renounced': rt.cetshwayo['vars']['sb_court_claim_renounced_var'] = 1
            elif invalid == 'crisis': rt.country['vars']['sb_court_dynastic_crisis_var'] = 1
            else: rt.country['vars']['sb_court_accession_open_var'] = 1
            rt.run('sb_court_prepare_dunn_offer')
            self.assertEqual(0, rt.created, invalid)
            self.assertNotIn('events', rt.country, invalid)

    def test_invalidated_popup_releases_retirement_reservation_without_pledge(self):
        for invalid in ('dead_prince', 'dead_dunn', 'new_ruler', 'other_pledge'):
            rt = DunnRuntime()
            rt.run('sb_court_prepare_dunn_offer')
            dunn = rt.country['vars']['sb_court_dunn_visitor_scope']
            if invalid == 'dead_prince': rt.mbuyazi['alive'] = False
            elif invalid == 'dead_dunn': dunn['alive'] = False
            elif invalid == 'new_ruler': rt.country['ruler'] = rt.cetshwayo
            else: dunn['vars']['sb_court_successor_pledge_scope'] = rt.cetshwayo
            rt.run('sb_court_prepare_dunn_offer')
            rt.run('sb_court_accept_dunn_offer')
            self.assertNotIn('sb_court_dunn_offer_var', rt.country['vars'], invalid)
            self.assertIsNot(rt.mbuyazi, dunn['vars'].get('sb_court_successor_pledge_scope'), invalid)

    def test_every_visible_dunn_event_uses_an_installed_window(self):
        import re
        from tests.test_zulu_court_politics import GAME
        native = (GAME/'gui/eventwindow.gui').read_text(encoding='utf-8-sig')
        source = (ROOT/'events/sb_court_dunn_events.txt').read_text(encoding='utf-8-sig')
        hamu = (ROOT/'events/sb_hamu_bargain_events.txt').read_text(encoding='utf-8-sig')
        for window in re.findall(r'gui_window\s*=\s*(\w+)', source+'\n'+hamu):
            self.assertRegex(native, r'name\s*=\s*"?'+window+r'"?\s')
        body = statements(find_object(source,'sb_court_dunn.002'))
        self.assertEqual('event_window_1char_tabloid',field(body,'gui_window'))
        self.assertEqual('scope:sb_court_dunn_trader',field(body,'left_icon'))
        self.assertIn('sb_court_dunn_trader',str(field(body,'immediate')))
        options = [v for k, _, v in body if k == 'option']
        self.assertEqual(1, len(options))
        self.assertEqual('yes', field(options[0], 'default_option'))

    def test_event_uses_native_paired_portraits_and_button_effect(self):
        text = (ROOT/'events/sb_court_dunn_events.txt').read_text(encoding='utf-8-sig')
        body = statements(find_object(text, 'sb_court_dunn.001'))
        self.assertEqual('event_window_2char', field(body, 'gui_window'))
        self.assertNotIn('sb_court_accept_dunn_offer', str(field(body, 'immediate')))
        self.assertIn('sb_court_accept_dunn_offer', str(field(body, 'option')))
        self.assertIn('sb_court_dunn_offer_valid', str(field(body, 'cancellation_trigger')))


if __name__ == '__main__': unittest.main()
