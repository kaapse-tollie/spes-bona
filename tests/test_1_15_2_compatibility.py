"""Source and byte-level regressions for the 1.15.2 port."""
import hashlib
import json
import re
from pathlib import Path
import tempfile
import unittest

from tools import check_1_15_2_target as target, cmf_patch
from tools.check_override_inventory import extract_braced_object, find_object
from tools.validate import find_game_root
from tests.test_zulu_institutions_laws import child, statements

ROOT = Path(__file__).resolve().parents[1]
GAME = find_game_root(None)
CMF = ROOT.parent / "Community Mod Framework"


def read(root, path):
    return (root / path).read_text(encoding="utf-8-sig")


class DepotTests(unittest.TestCase):
    def test_previous_and_current_manifests_reproduce_reviewed_report(self):
        if not target.depot.default_manifest_path(target.OLD).is_file():
            self.skipTest("Historical 1.15.1 manifest unavailable")
        self.assertEqual(target.OUTPUT.read_text(), target.depot.normalized_json(target.build_delta()))

    def test_replacing_a_reviewed_path_with_another_valid_depot_file_fails(self):
        data = json.loads(target.OUTPUT.read_text())
        current = target.depot.decode_manifest(target.depot.default_manifest_path(target.NEW), target.NEW)
        replacement = current.records["game/common/laws/01_health_system.txt"]
        data["entries"][0].update(path=replacement.path, new=replacement.evidence())
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "altered.json"
            report.write_text(target.depot.normalized_json(data))
            with self.assertRaisesRegex(ValueError, "report SHA-256 mismatch"):
                target.verify_current_target(GAME, report_path=report)


class CompatibilityTests(unittest.TestCase):
    def test_dominion_differs_from_native_only_in_ordinary_war_participation(self):
        native = find_object(read(GAME, "common/subject_types/00_subject_types.txt"), "subject_type_dominion")
        mod = find_object(read(ROOT, "common/subject_types/zz_sb_dominion_override.txt"),
                          "subject_type_dominion", directive="REPLACE")
        self.assertEqual(1, native.count("join_overlord_wars = yes"))
        self.assertEqual(statements(native.replace("join_overlord_wars = yes", "join_overlord_wars = no")),
                         statements(mod))

    def test_removed_subject_and_naval_interfaces_have_no_active_callers(self):
        removed = (
            b"breaks_if_subject_not_protected", b"on_diplo_play_subject_released", b"on_diplo_play_subject_released_overlord",
            b"MapListNavalMissionOption", b"MapListNavalMissionPanel", b"CanEditSeaRegionsForSelectedFleets",
            b"GetCanEditMissionSeaRegionsForSelectedFleetsDesc", b"OnEditSelectedFleetsSeaRegionsClicked",
        )
        pattern = re.compile(rb"\b(?:" + b"|".join(removed) + rb")\b")
        hits = []
        for root in (ROOT, CMF):
            for folder in ("common", "events", "gui", "data_binding", "input_profile"):
                for path in (root / folder).rglob("*"):
                    if path.suffix in {".txt", ".gui", ".profile"}:
                        raw = path.read_bytes()
                        if pattern.search(raw):
                            code = re.sub(rb"(?m)#.*$", b"", raw)
                            hits.extend((str(path.relative_to(root)), token.decode()) for token in pattern.findall(code))
        self.assertEqual([], hits)

    def test_raster_pins_bind_the_reviewed_merge_to_the_installed_map(self):
        evidence = json.loads(read(ROOT, "Docs/compatibility/evidence/1_15_2_implementation/raster_merge.json"))
        self.assertEqual((2225, 17, 0), (evidence["authored_pixels"], evidence["native_changed_pixels"],
                         evidence["overlap_pixels"]))
        self.assertEqual(17, len({tuple(p) for p in evidence["native_pixel_change"]["coordinates"]}))
        current = json.loads(read(ROOT, "tools/map_connectivity_manifest.json"))
        self.assertEqual(evidence["result_sha256"], current["zululand_boundary_edit"]["base_sha256"])
        for root, expected in ((ROOT, current["province_map_sha256"]), (GAME, evidence["native_1_15_2_sha256"])):
            self.assertEqual(expected, hashlib.sha256((root / "map_data/provinces.png").read_bytes()).hexdigest())

    def test_party_exception_and_weight_reverse_to_the_pristine_cmf_bytes(self):
        patch = cmf_patch.load_patch()
        parties = {e["path"]: e for e in patch["files"] if e["path"].startswith("common/parties/")}
        self.assertEqual({p.relative_to(GAME).as_posix() for p in (GAME / "common/parties").glob("*_party.txt")
                          if (CMF / p.relative_to(GAME)).is_file()}, set(parties))
        self.assertEqual(11, len(parties))
        for path, entry in parties.items():
            with self.subTest(path=path):
                # Keep BOMs, tabs, trailing spaces and line endings for the archive hash.
                patched = (CMF / path).read_bytes().decode()
                native = (GAME / path).read_bytes().decode()
                name = Path(path).stem.removesuffix("_party")
                outer = child(patched, "available_for_interest_group")
                self.assertEqual(child(child(native, "available_for_interest_group"), "trigger_if"),
                                 child(outer, "trigger_if"))
                self.assertEqual(["trigger_if", "trigger_else"], [key for key, _, _ in statements(outer)])
                conditional = child(outer, "trigger_if")
                self.assertEqual([("limit", "=", [("ig_is_member_of_dominant_party", "=", [("PARTY", "=", name)])]),
                                  ("always", "=", "yes")], statements(conditional))
                ordinary = child(outer, "trigger_else").splitlines()[1:-1]
                old_gate = "available_for_interest_group = {\n" + "\n".join(
                    line.removeprefix("\t") for line in ordinary) + "\n\t}"

                join = child(native, "join_weight")
                pos = join.index("ig_is_member_of_dominant_party")
                start = join.rindex("\n\t\tif = {", 0, pos) + 1
                weight = extract_braced_object(join, start)
                self.assertIn('desc = "amendment_' + name + '_party_dominance"', weight)
                self.assertIn("value = 1000", weight)
                self.assertEqual(1, child(patched, "join_weight").count(weight))
                following = join[start + len(weight):].splitlines()[1:4]
                self.assertIn(weight + "\n" + "\n".join(following), patched)
                restored = patched.replace(outer, old_gate, 1).replace(weight + "\n", "", 1)
                self.assertEqual(entry["original_sha256"], hashlib.sha256(restored.encode()).hexdigest())

    def test_party_dominance_requires_membership_and_an_active_or_enacting_amendment(self):
        triggers = read(GAME, "common/scripted_triggers/00_victoria_scripted_triggers.txt")
        helper = find_object(triggers, "ig_is_member_of_dominant_party")
        amendment = [("has_amendment", "=", "amendment_type:amendment_$PARTY$_party_dominance")]
        self.assertEqual([
            ("party", "?=", [("is_party_type", "=", "$PARTY$_party")]),
            ("owner", "?=", [("OR", "=", [
                ("any_active_law", "=", amendment), ("currently_enacting_law", "?=", amendment),
            ])]),
        ], statements(helper))

    def test_single_party_selection_cleanup_fallback_and_native_checkpoint(self):
        sb = find_object(read(ROOT, "common/laws/zz_sb_law_journal_readiness.txt"),
                         "law_single_party_state", directive="REPLACE")
        self.assertIn("party_has_insurrectionary_member = no", child(sb, "can_enact"))
        activate = child(sb, "on_activate")
        choice = child(activate, "custom_tooltip")
        self.assertIn("has_party = yes", child(choice, "if"))
        self.assertIn("set_only_legal_party_from_ig = var:sps_dominant_party_ig_var", child(choice, "if"))
        self.assertIn("set_only_legal_party_from_ig = ruler.interest_group", child(choice, "else"))
        self.assertIn("remove_variable = sps_dominant_party_ig_var", activate)
        self.assertEqual([("name", "=", "modifier_single_party_consolidation"), ("days", "=", "90")],
                         statements(child(activate, "add_modifier")))
        actions = read(GAME, "common/on_actions/00_code_on_actions.txt")
        self.assertIn("single_party_state.8", find_object(actions, "on_law_checkpoint_success"))
        for stage in ("success", "advance", "debate", "stall"):
            self.assertIn("sps_law_checkpoint_cancellation", find_object(actions, "on_law_checkpoint_" + stage))
        self.assertIn("remove_variable = sps_dominant_party_ig_var", find_object(actions, "on_law_enactment_started"))
        cancellation = find_object(actions, "sps_law_checkpoint_cancellation")
        self.assertIn("party_has_insurrectionary_member = yes", cancellation)
        self.assertIn("id = single_party_state.9", cancellation)
        events = read(GAME, "events/law_events/single_party_state_laws.txt")
        self.assertIn("cancel_enactment = yes", find_object(events, "single_party_state.9"))
        self.assertIn("set_sps_dominant_party_effect", find_object(events, "single_party_state.8"))

    def test_customary_levies_enable_protected_recruitment_and_preserve_authored_caps(self):
        for file, name, rate, barracks, peasant_only in (
            ("03_sb_amabutho_system.txt", "law_sb_amabutho_system", "0.30", "25", False),
            ("04_sb_chiefly_levy.txt", "law_sb_chiefly_levy", "0.60", "5", True),
        ):
            with self.subTest(law=name):
                law = find_object(read(ROOT, "common/laws/" + file), name)
                fields = {key: value for key, _, value in statements(child(law, "modifier"))}
                self.assertIn("parent = law_peasant_levies", law)
                self.assertEqual("yes", fields["country_can_conscript_protected_subsistence_employment_bool"])
                self.assertEqual(peasant_only, fields.get("country_can_only_conscript_peasants_bool") == "yes")
                self.assertEqual((rate, barracks, "25"), (fields["state_conscription_rate_add"],
                                 fields["state_building_barrack_max_level_add"],
                                 fields["state_building_conscription_center_max_level_add"]))

    def test_inherited_gui_overlaps_keep_the_framework_layouts(self):
        for root, path, align, width in (
            (GAME, "gui/panel_military.gui", "hcenter", 520),
            (CMF, "gui/00_com_gui_panel_military.gui", "vcenter", 180),
        ):
            button = child(read(root, path), "military_formation_mobilize_button")
            self.assertIn("parentanchor = " + align, button)
            self.assertIn("size = { %d 50 }" % width, button)
        key = "type construction_interaction_item_full ="
        native = read(GAME, "gui/map_list_panel.gui")
        body = extract_braced_object(native, native.index(key))
        self.assertEqual("154f2d0d6c0808347c897a8fe3e27c2461098993ca26d1c2a2c71b65709f93e4",
                         hashlib.sha256(body.encode()).hexdigest())
        overlay = read(CMF, "gui/00_MPM_map_list_panel.gui")
        self.assertIn('name = "horizontal_scrollbar"', extract_braced_object(overlay, overlay.index(key)))

    def test_company_ai_targets_and_scripted_charter(self):
        for path, industries in (
            ("zz_sb_de_beers_override.txt", {"building_diamond_mine"}),
            ("zz_sb_mozambique_company_override.txt", {"building_cotton_plantation", "building_tea_plantation"}),
        ):
            body = read(ROOT, "common/company_types/" + path)
            targets = statements(child(body, "ai_construction_targets"))
            self.assertEqual(industries, {key for key, _, _ in targets})
            for _, _, fields in targets:
                self.assertTrue(next(value for key, _, value in fields if key == "state_trigger"))
        charter = read(ROOT, "common/company_types/sb_british_south_africa_company.txt")
        for gate in ("possible", "ai_will_do"):
            self.assertEqual([("always", "=", "no")], statements(child(charter, gate)))


if __name__ == "__main__":
    unittest.main()
