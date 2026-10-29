"""Constitution/ideology contracts and narrow parity for institutional reform gates.

These execute gate predicates and inspect effective definitions. Native movement
recruitment, decree invalidation and government selection remain DP engine checks.
"""
from pathlib import Path
import re
import unittest

from tools.check_override_inventory import extract_braced_object, find_object
from tools.validate import find_game_root

ROOT = Path(__file__).resolve().parents[1]
GAME = find_game_root(None)
CMF = ROOT.parent / 'Community Mod Framework'


def read(root, path):
    return (root / path).read_text(encoding='utf-8-sig')


def child(text, key):
    match = re.search(r'(?m)^\s*' + re.escape(key) + r'\s*=\s*\{', text)
    if not match:
        raise AssertionError(f'missing {key}')
    return extract_braced_object(text, text.index(key, match.start()))


def tokens(text):
    return re.findall(r'"[^"\n]*"|[^\s]+', re.sub(r'#[^\n]*', '', text))


def statements(text):
    """The small gate vocabulary has no bare-list clauses."""
    ts = re.findall(r'\?=|>=|<=|[=<>]|[{}]|[^\s{}=<>]+', re.sub(r'#[^\n]*', '', text))
    pos = 0
    def parse():
        nonlocal pos
        out = []
        while pos < len(ts) and ts[pos] != '}':
            key, op, value = ts[pos:pos+3]
            pos += 3
            if value == '{':
                value = parse()
                assert ts[pos] == '}'
                pos += 1
            out.append((key, op, value))
        return out
    return parse()[0][2]


def gate(nodes, state):
    results = []
    for key, op, value in nodes:
        if key == 'OR': result = any(gate([n], state) for n in value)
        elif key == 'AND': result = gate(value, state)
        elif key == 'NOR': result = not any(gate([n], state) for n in value)
        elif key == 'NOT': result = not gate(value, state)
        elif key == 'has_variable': result = value in state.get('flags', set())
        elif key == 'has_law': result = value.removeprefix('law_type:') in state.get('laws', set())
        elif key == 'sb_institutions_profile_country': result = state.get('profile', False) == (value == 'yes')
        elif key == 'any_political_movement':
            result = any(gate(value, {'movement': m}) for m in state.get('movements', []))
        elif key == 'is_political_movement_type': result = value == state['movement']
        else: raise AssertionError(key)
        results.append(result)
    return all(results)


class ReformGateTests(unittest.TestCase):
    def test_firearms_completion_unlocks_only_the_authored_levies(self):
        predicate = statements(find_object(read(ROOT, 'common/scripted_triggers/sb_institutions_reform_triggers.txt'), 'sb_can_reform_customary_army'))
        for law in ('law_sb_amabutho_system', 'law_sb_chiefly_levy'):
            self.assertFalse(gate(predicate, {'laws': {law}}))
            self.assertTrue(gate(predicate, {'laws': {law}, 'flags': {'sb_firearms_modernized_var'}}))
        for law in ('law_peasant_levies', 'law_warrior_caste', 'law_professional_army'):
            self.assertTrue(gate(predicate, {'laws': {law}}))

    def test_all_five_native_army_laws_retain_every_other_rule(self):
        self.assertIsNotNone(GAME)
        native = read(GAME, 'common/laws/00_army_model.txt')
        override = read(ROOT, 'common/laws/zz_sb_customary_army_reform.txt')
        for law in ('peasant_levies', 'warrior_caste', 'professional_army', 'national_militia', 'mass_conscription'):
            key = 'law_' + law
            old = find_object(native, key)
            new = find_object(override, key, directive='REPLACE').removeprefix('REPLACE:')
            enacted = child(new, 'can_enact')
            tooltip = child(enacted, 'custom_tooltip')
            self.assertIn('sb_can_reform_customary_army = yes', tooltip)
            if '\tcan_enact = {' in old:
                new = new.replace(tooltip, '')
            else:
                new = new.replace(enacted, '')
            self.assertEqual(tokens(old), tokens(new), key)

    def test_decree_has_only_owner_active_gate_and_keeps_native_weekly_invalidation_contract(self):
        source = read(GAME, 'common/decrees/00_decree.txt')
        old = find_object(source, 'decree_promote_social_mobility')
        new = find_object(read(ROOT, 'common/decrees/zz_sb_institutions_social_mobility.txt'), 'decree_promote_social_mobility', directive='REPLACE').removeprefix('REPLACE:')
        extra = 'owner ?= { NOT = { has_variable = sb_institutions_active_var } }'
        tooltip = child(child(new, 'state_trigger'), 'custom_tooltip')
        self.assertIn(extra, tooltip)
        self.assertIn('text = sb_institutions_social_mobility_available_tt', tooltip)
        self.assertIn('sb_institutions_social_mobility_available_tt:', read(ROOT, 'localization/english/sb_institutions_l_english.yml'))
        self.assertEqual(tokens(old), tokens(new.replace(tooltip, '', 1)))
        self.assertIn('invalidate the Decree on a weekly basis', source)
        self.assertNotIn('sb_firearms_modernized_var', new)

    def test_generic_absolutist_exclusion_tracks_active_profile_or_surviving_constituency(self):
        predicate = statements(find_object(read(ROOT, 'common/scripted_triggers/sb_institutions_reform_triggers.txt'), 'sb_uses_authored_zulu_movements'))
        self.assertTrue(gate(predicate, {'profile': True, 'flags': {'sb_institutions_active_var'}}))
        self.assertTrue(gate(predicate, {'movements': ['movement_sb_zulu_traditionalist']}))
        self.assertFalse(gate(predicate, {'profile': False, 'flags': {'sb_institutions_active_var'}}))
        self.assertFalse(gate(predicate, {'profile': True}))


class ConstitutionalDefinitionTests(unittest.TestCase):
    def test_law_packages_are_weaker_without_adding_pb_or_elder_council_perks(self):
        source = read(ROOT, 'common/laws/05_sb_chiefly_constitution.txt')
        federation = child(find_object(source, 'law_sb_federated_chiefdoms'), 'modifier')
        council = child(find_object(source, 'law_sb_chiefly_council'), 'modifier')
        self.assertEqual(dict((k, v) for k, _, v in statements(federation)), {
            'country_legitimacy_headofstate_add': '10',
            'country_legitimacy_ideological_incoherence_mult': '0.1',
            'country_aristocrats_pol_str_mult': '0.25',
            'country_authority_add': '100',
        })
        self.assertEqual(dict((k, v) for k, _, v in statements(council)), {
            'country_legitimacy_headofstate_add': '10',
            'country_legitimacy_govt_total_clout_add': '100',
            'country_legitimacy_ideological_incoherence_mult': '0.5',
            'country_aristocrats_pol_str_mult': '0.5',
            'country_officers_pol_str_mult': '0.5',
            'country_authority_add': '150',
        })
        self.assertFalse((ROOT/'common/laws/zz_sb_law_chiefdom_override.txt').exists())
        self.assertFalse((ROOT/'common/laws/zz_sb_law_elder_council_override.txt').exists())

    def test_council_uses_selected_head_without_government_reshuffle_replacement(self):
        source = read(ROOT, 'common/government_types/00_sb_chiefly_constitution.txt')
        government = find_object(source, 'gov_sb_federated_chiefdoms')
        self.assertIn('transfer_of_power = dictatorial', government)
        self.assertIn('new_leader_on_reform_government = no', government)
        self.assertIn('has_law = law_type:law_sb_federated_chiefdoms', child(government, 'possible'))
        post = child(government, 'on_post_government_type_change')
        self.assertLess(post.index('post_change_to_dictatorial'), post.index('sb_court_select_chiefly_head'))
        old = find_object(read(GAME, 'common/government_types/00_chiefdoms.txt'), 'gov_chiefdom')
        self.assertIn('has_law_or_variant = law_type:law_chiefdom', child(old, 'possible'))
        self.assertNotIn('REPLACE:gov_chiefdom', source)

    def test_constitutional_movements_are_narrow_without_replacing_character_ideology(self):
        royals = find_object(read(ROOT, 'common/ideologies/sb_usuthu_ideology.txt'), 'ideology_sb_usuthu')
        source = read(ROOT, 'common/ideologies/sb_zulu_constitutional_ideologies.txt')
        chiefs = find_object(source, 'ideology_sb_zulu_chiefly')
        for body in (royals, chiefs):
            groups = re.findall(r'\b(lawgroup_\w+)\s*=', body)
            self.assertEqual(['lawgroup_governance_principles', 'lawgroup_distribution_of_power'], groups)
        movements = read(ROOT, 'common/political_movements/sb_zulu_constitutional_movements.txt')
        for key, alignment in [('movement_sb_zulu_royal', 1), ('movement_sb_zulu_chiefly', 2)]:
            movement = find_object(movements, key)
            self.assertEqual(['character_ideologies', '=', '{', '}'], tokens(child(movement, 'character_ideologies')))
            support = child(movement, 'character_support_trigger')
            self.assertNotIn('has_ideology', support)
            self.assertIn(f'var:sb_court_alignment_var = {alignment}', support)
        self.assertNotIn('character_ideology = yes', source)
        self.assertIn('law_sb_federated_chiefdoms = strongly_disapprove', royals)
        self.assertIn('law_sb_chiefly_council = strongly_approve', chiefs)

    def test_startup_history_excludes_only_eligible_authored_absolutists(self):
        from tests.test_zulu_institutions_core import Runtime, country
        path = 'common/history/political_movements/00_movements.txt'
        native = read(GAME, path)
        changed = read(ROOT, path)
        guard = '\t\t\t\tNOT = { sb_institutions_eligible = yes } # Authored constitutional movements replace Absolutists.\n'
        self.assertEqual(1, changed.count(guard))
        self.assertEqual(native, changed.replace(guard, ''))
        first_branch = child(child(find_object(changed, 'POLITICAL_MOVEMENTS'), 'every_country'), 'if')
        self.assertIn(guard.strip(), child(first_branch, 'limit'))
        self.assertIn('create_political_movement = { type = movement_royalist_absolutist }', first_branch)
        runtime = Runtime()
        predicate = statements('gate = { NOT = { sb_institutions_eligible = yes } }')
        # No post-lobby/active flag is required to suppress the explicit history creation.
        self.assertFalse(runtime.condition(predicate, country()))
        inherited = country('NGN')
        inherited['vars']['sb_ngu_inherited_zul_content_var'] = 1
        self.assertFalse(runtime.condition(predicate, inherited))
        for other in (country('GBR'), country('BST'), country('NGN'), country(laws={'law_parliamentary_republic'})):
            self.assertTrue(runtime.condition(predicate, other))

    def test_chiefly_laws_allow_their_own_ideological_stances(self):
        source = read(ROOT, 'common/laws/05_sb_chiefly_constitution.txt')
        for law in ('law_sb_federated_chiefdoms', 'law_sb_chiefly_council'):
            fields = dict((k, v) for k, _, v in statements(find_object(source, law)))
            # A variant silently inherits its parent's stances and rejects explicit ones.
            self.assertNotIn('parent', fields, law)

    def test_traditionalist_stances_match_approved_customary_package(self):
        source = find_object(read(ROOT, 'common/ideologies/sb_zulu_constitutional_ideologies.txt'), 'ideology_sb_zulu_traditionalist')
        expected = {
            'law_oligarchy': 'approve', 'law_landed_voting': 'disapprove', 'law_wealth_voting': 'disapprove',
            'law_census_voting': 'strongly_disapprove', 'law_universal_suffrage': 'strongly_disapprove',
            'law_technocracy': 'strongly_disapprove', 'law_single_party_state': 'strongly_disapprove', 'law_anarchy': 'strongly_disapprove',
            'law_hereditary_bureaucrats': 'strongly_approve', 'law_appointed_bureaucrats': 'disapprove', 'law_elected_bureaucrats': 'strongly_disapprove',
            'law_traditionalism': 'strongly_approve', 'law_agrarianism': 'approve', 'law_interventionism': 'disapprove',
            'law_laissez_faire': 'disapprove', 'law_command_economy': 'disapprove',
            'law_cooperative_ownership': 'strongly_disapprove', 'law_extraction_economy': 'strongly_disapprove',
            'law_local_police': 'strongly_approve', 'law_dedicated_police': 'approve',
            'law_peasant_levies': 'strongly_approve', 'law_professional_army': 'disapprove',
            'law_national_militia': 'disapprove', 'law_mass_conscription': 'strongly_disapprove',
        }
        actual = dict(re.findall(r'\b(law_\w+)\s*=\s*(\w+)', source))
        self.assertEqual(expected, actual)  # N/A laws must remain absent, including Militarized Police.
        amabutho = find_object(read(ROOT, 'common/laws/03_sb_amabutho_system.txt'), 'law_sb_amabutho_system')
        parent = dict((k, v) for k, _, v in statements(amabutho))['parent']
        self.assertEqual('law_peasant_levies', parent)
        self.assertEqual('strongly_approve', actual[parent])

    def test_generic_absolutist_preserves_complete_cmf_body_except_scoped_exclusion(self):
        old = find_object(read(CMF, 'common/political_movements/ycom_00_ideological_movements.txt'), 'movement_royalist_absolutist', directive='REPLACE')
        new = find_object(read(ROOT, 'common/political_movements/zz_sb_absolutist_override.txt'), 'movement_royalist_absolutist', directive='REPLACE')
        new = re.sub(r'\s*sb_uses_authored_zulu_movements = (?:yes|no)', '', new)
        self.assertEqual(tokens(old), tokens(new))

    def test_three_movements_use_native_revolution_without_old_contest_suppression(self):
        source = read(ROOT, 'common/political_movements/sb_zulu_constitutional_movements.txt')
        for suffix in ('royal', 'chiefly', 'traditionalist'):
            body = find_object(source, 'movement_sb_zulu_'+suffix)
            self.assertIn('always = no', child(body, 'creation_trigger'))
            self.assertEqual(1, body.count('add_movement_enthusiasm_modifier = yes'))
            self.assertIn('revolution = {', body)
            self.assertNotIn('secession = {', body)
            self.assertNotIn('sb_zululand_usuthu_contest_var', body)
            self.assertNotIn('num_states', body)
            self.assertNotIn('is_at_war', body)
            self.assertIn('mog_plp_movement_all_general_state_weight_mult', body)
            self.assertIn('mog_plp_movement_mainland_general_pop_support_trigger', body)
            self.assertIn('days_since_movement_defeated', body)


if __name__ == '__main__':
    unittest.main()
