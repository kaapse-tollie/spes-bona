"""New cast availability and registry integration; native appointments remain DP checks."""
import re
import unittest

from tests.test_zulu_frontier_followup import FrontierRuntime, ROOT, block, field
from tests.test_zulu_court_politics import EFFECTS, character
from tests.test_zulu_institutions_laws import statements
from tools.check_override_inventory import find_object


TEMPLATES = 'common/character_templates/sb_court_characters.txt'
SIGANANDA = 'SB_ZUL_sigananda_kazokufa'
LANGAZANA = 'SB_ZUL_langazana'


def template_data(path, name, directive=None):
    body = find_object((ROOT/path).read_text(encoding='utf-8-sig'), name, directive=directive)
    # The gate interpreter deliberately excludes bare-list clauses.
    return statements(re.sub(r'\btraits\s*=\s*\{[^}]*\}', '', body))


class LeadershipRuntime(FrontierRuntime):
    def __init__(self, year=1865):
        super().__init__()
        self.country.update(year=year, states=[{'state_region': 's:STATE_ZULULAND'}])
        # Other dated cast have already appeared in this fixture.
        self.global_vars = {f'sb_court_{name}_created_var' for name in (
            'mnyamana', 'hamu', 'john_dunn', 'godide', 'sekethwayo', 'masiphula', 'maphitha')}

    def condition(self, nodes, scope, prev=None):
        for node in nodes:
            key, _, value = node
            if key == 'has_global_variable': result = value in self.global_vars
            elif key == 'is_revolutionary': result = scope.get(key, False) == (value == 'yes')
            else: result = super().condition([node], scope, prev)
            if not result: return False
        return True

    def new_actor(self, template):
        data = dict((k, v) for k, _, v in template_data(TEMPLATES, template))
        age = self.country['year'] - int(data['birth_date'].split('.')[0]) if 'birth_date' in data else int(data['age'])
        actor = character(template, 0, 60, age=age)
        actor.update(template=template, owner=self.country, interest_group=data['interest_group'],
                     ideology=data['ideology'], vars={})
        self.country['characters'].append(actor)
        return actor

    def effect(self, nodes, scope, prev=None):
        for node in self.branches(nodes, scope, prev):
            key, _, value = node
            if key == 'set_global_variable': self.global_vars.add(value)
            elif key == 'add_character_role': scope[value] = True
            elif key == 'create_character':
                actor = self.new_actor(field(value, 'template'))
                self.created += 1
                outer = self.scopes
                self.scopes = dict(outer, root=actor)
                try: self.effect(field(value, 'on_created'), actor, scope)
                finally: self.scopes = outer
            else: super().effect([node], scope, prev)

    def pulse(self):
        self.effect(EFFECTS['sb_court_spawn_dated_cast'], self.country)


class ZuluIGLeadershipTests(unittest.TestCase):
    def test_opening_appointments_and_later_candidate_roles(self):
        opening = 'common/character_templates/sb_court_opening_templates.txt'
        for path, name, ig in ((opening, 'ZUL_mkabayi', 'ig_landowners'),
                               (opening, 'ZUL_ndlela_kasompisi', 'ig_armed_forces'),
                               (TEMPLATES, LANGAZANA, 'ig_devout')):
            data = template_data(path, name, 'REPLACE' if path == opening else None)
            self.assertEqual(ig, field(data, 'interest_group'))
            self.assertEqual('yes', field(data, 'ig_leader'))
        history = (ROOT/'common/history/characters/zul - zulu.txt').read_text(encoding='utf-8-sig')
        self.assertEqual(1, history.count('template = ' + LANGAZANA))
        self.assertNotIn(SIGANANDA, history)
        later = dict((k, v) for k, _, v in template_data(TEMPLATES, SIGANANDA))
        self.assertEqual('ig_rural_folk', later['interest_group'])
        self.assertNotIn('ig_leader', later)
        self.assertEqual('1811.1.1', later['birth_date'])
        for name in (LANGAZANA, SIGANANDA):
            data = template_data(TEMPLATES, name)
            self.assertEqual('yes', field(data, 'historical'))
            self.assertEqual('yes', field(data, 'noble'))
            self.assertEqual('yes', field(field(data, 'trait_generation'), 'sb_court_authored_initial_traits'))

    def test_langazana_registration_counts_one_house_and_preserves_later_pledges(self):
        rt = LeadershipRuntime(1836)
        actor = rt.new_actor(LANGAZANA)
        rt.effect(EFFECTS['sb_court_register_expanded_cast'], rt.country)
        self.assertEqual((13, 1, 0), tuple(actor['vars'][f'sb_court_{key}_var'] for key in ('following', 'alignment', 'endorsement')))
        self.assertNotIn('sb_court_successor_pledge_scope', actor['vars'])
        rt.backing()
        self.assertEqual(60, actor['vars']['sb_court_represented_weight_var'])
        self.assertEqual(110, rt.country['vars']['sb_court_weight_var'])
        actor['vars'].update(sb_court_alignment_var=2, sb_court_endorsement_var=1,
                             sb_court_successor_pledge_scope=rt.country['ruler'])
        for _ in range(3): rt.effect(EFFECTS['sb_court_register_expanded_cast'], rt.country)
        self.assertEqual(2, actor['vars']['sb_court_alignment_var'])
        self.assertEqual(1, actor['vars']['sb_court_endorsement_var'])
        self.assertIs(rt.country['ruler'], actor['vars']['sb_court_successor_pledge_scope'])
        self.assertEqual(1, sum(m is actor for m in rt.country['members']))
        self.assertEqual({}, rt.scopes['root']['vars'])

    def test_later_creation_boundaries_and_country_controls(self):
        cases = ((1836, 'ZUL', False, False), (1864, 'ZUL', False, False),
                 (1865, 'ZUL', False, True), (1905, 'ZUL', False, True),
                 (1906, 'ZUL', False, False), (1865, 'NAL', False, False),
                 (1865, 'NGN', False, False), (1865, 'NGN', True, True))
        for year, tag, inherited, expected in cases:
            with self.subTest(year=year, tag=tag, inherited=inherited):
                rt = LeadershipRuntime(year); rt.country['id'] = tag
                if inherited: rt.country['vars']['sb_ngu_inherited_zul_content_var'] = 1
                rt.country['is_at_war'] = True  # No unrelated-war peace requirement.
                rt.pulse()
                self.assertEqual(int(expected), rt.created)
                if expected:
                    actor = rt.country['characters'][-1]
                    self.assertEqual(year - 1811, actor['age'])
                    self.assertEqual((14, 0, 0), tuple(actor['vars'][f'sb_court_{key}_var'] for key in ('following', 'alignment', 'endorsement')))
                    self.assertIs(rt.country, actor['vars']['sb_court_home_scope'])
                    self.assertTrue(actor['politician'])
                    self.assertEqual({}, rt.scopes['root']['vars'])

    def test_local_availability_defers_instead_of_consuming_creation(self):
        for reason in ('territory', 'revolution', 'crisis'):
            with self.subTest(reason=reason):
                rt = LeadershipRuntime()
                if reason == 'territory': rt.country['states'] = [{'state_region': 's:STATE_NATAL'}]
                if reason == 'revolution': rt.country['is_revolutionary'] = True
                if reason == 'crisis': rt.country['vars']['sb_court_dynastic_crisis_var'] = 1
                rt.pulse(); self.assertEqual(0, rt.created)
                rt.country['states'] = [{'state_region': 's:STATE_ZULULAND'}]
                rt.country['is_revolutionary'] = False
                rt.country['vars'].pop('sb_court_dynastic_crisis_var', None)
                rt.pulse(); self.assertEqual(1, rt.created)

    def test_death_and_inherited_reentry_do_not_recreate_historical_identity(self):
        rt = LeadershipRuntime(); rt.pulse()
        actor = rt.country['characters'][-1]
        actor['alive'] = False
        rt.country.update(id='NGN', characters=[rt.country['ruler']])
        rt.country['vars']['sb_ngu_inherited_zul_content_var'] = 1
        for _ in range(3): rt.pulse()
        self.assertEqual(1, rt.created)
        self.assertEqual('kaZokufa', field(template_data(TEMPLATES, SIGANANDA), 'last_name').strip('"'))
        fictional = template_data('common/character_templates/sb_zulu_dynasty_characters.txt', 'ZUL_mbuyazi_successor')
        self.assertEqual('no', field(fictional, 'historical'))


if __name__ == '__main__':
    unittest.main()
