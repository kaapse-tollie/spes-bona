import json
from pathlib import Path
import tempfile
import unittest

from tools import validate


class RepositoryValidatorTests(unittest.TestCase):
    def test_cmf_compatibility_rejects_an_unreviewed_release(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".metadata").mkdir()
            (root / ".metadata/metadata.json").write_text(json.dumps({
                "id": validate.CMF_ID,
                "version": "1.64.0",
            }))
            check = validate.check_cmf_install(root)
            self.assertEqual("FAIL", check.status)
            self.assertIn("requires a rebase", check.detail)

    def test_cmf_sync_command_uses_exact_inventory_tag_and_digest(self):
        digest = "a" * 64
        with tempfile.TemporaryDirectory() as temporary:
            inventory = Path(temporary) / "override_inventory.json"
            inventory.write_text(json.dumps({
                "dependencies": [{
                    "name": "Community Mod Framework",
                    "version": "1.66.0",
                    "release_tag": "1.66.0",
                    "asset_name": "release-1.66.0.zip",
                    "asset_sha256": digest,
                }],
            }))
            command = validate.cmf_sync_command(Path(temporary) / "cmf", inventory)
            self.assertEqual("1.66.0", command[command.index("--tag") + 1])
            self.assertEqual(digest, command[command.index("--sha256") + 1])
            self.assertNotIn("--latest", command)

            payload = json.loads(inventory.read_text())
            payload["dependencies"][0]["asset_sha256"] = "not-a-digest"
            inventory.write_text(json.dumps(payload))
            with self.assertRaisesRegex(ValueError, "asset_sha256"):
                validate.cmf_sync_command(Path(temporary) / "cmf", inventory)

    def test_nonzero_diagnostic_is_operational_failure(self):
        check = validate.run_advisory_command(
            "fixture diagnostic",
            [validate.sys.executable, "-c", "print('schema lag'); raise SystemExit(7)"],
        )
        self.assertEqual("FAIL", check.status)
        self.assertIn("exit status 7", check.detail)
        self.assertIn("schema lag", check.detail)

    def test_tiger_requires_exact_load_paths_and_terminal_summary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cmf = root / 'CMF with "quote"'
            cmf.mkdir()
            config = (root / "dependencies.conf").resolve()
            escaped = str(cmf.resolve()).replace("\\", "\\\\").replace('"', '\\"')
            config.write_text(f'load_mod = {{ label = "CMF" mod = "{escaped}" }}\n')
            expected = (
                f"Using conf file: {config}\n"
                "Using mod directory: Fixture Mod\n"
                f"Loading secondary mod CMF from: {cmf.resolve()}\n"
                "fatal: 0, error: 8, warning: 1, untidy: 0, tips: 0"
            )

            def invoke(output):
                return validate.run_advisory_command(
                    "vic3-tiger",
                    [validate.sys.executable, "-c", f"print({output!r})", "--config", str(config), "Fixture Mod"],
                    root,
                )

            self.assertEqual("WARN", invoke(expected).status)
            self.assertEqual("FAIL", invoke(expected.replace(str(cmf.resolve()), "WRONG", 1)).status)
            self.assertEqual("FAIL", invoke(expected + "\nnot terminal").status)
            self.assertEqual("FAIL", invoke("prefix " + expected).status)

    def test_tiger_style_exit_zero_diagnostics_are_retained_as_warning(self):
        check = validate.run_advisory_command(
            "fixture diagnostic",
            [validate.sys.executable, "-c", "print('fatal: 0, error: 8')"],
        )
        self.assertEqual("WARN", check.status)
        self.assertIn("fatal: 0, error: 8", check.detail)

        silent = validate.run_advisory_command(
            "silent fixture",
            [validate.sys.executable, "-c", "pass"],
        )
        self.assertEqual("PASS", silent.status)
        self.assertEqual("", silent.detail)

    def test_localization_key_regex_is_horizontal_and_does_not_cross_lines(self):
        fixture = (
            "l_english:\n"
            "column_zero:0 \"value\"\n"
            "  spaced_key:1 \"value\"\n"
            "\ttabbed_key:0 \"value\"\n"
            "broken_without_colon\n"
            "  next_key:0 \"value\"\n"
        )
        self.assertEqual(
            ["column_zero", "spaced_key", "tabbed_key", "next_key"],
            validate.LOC_KEY_RE.findall(fixture),
        )
        self.assertNotIn("l_english", validate.LOC_KEY_RE.findall(fixture))
        self.assertTrue(validate.LOC_LINE_KEY_RE.match("column_zero:0 \"value\""))
        self.assertTrue(validate.LOC_LINE_KEY_RE.match("  spaced_key:0 \"value\""))
        self.assertTrue(validate.LOC_LINE_KEY_RE.match("\ttabbed_key:0 \"value\""))
        self.assertIsNone(validate.LOC_LINE_KEY_RE.match("broken\n key:0 \"value\""))

    def test_source_definition_regexes_accept_space_and_tab_indentation(self):
        events = "fixture.1 = { }\n  fixture.2 = { }\n\tfixture.3 = { }\n"
        journals = (
            "je_fixture = { }\n"
            "  REPLACE:je_spaced = { }\n"
            "\tTRY_REPLACE:je_tabbed = { }\n"
        )
        self.assertEqual(
            ["fixture.1", "fixture.2", "fixture.3"],
            validate.SCRIPT_EVENT_RE.findall(events),
        )
        self.assertEqual(
            ["je_fixture", "je_spaced", "je_tabbed"],
            validate.JOURNAL_ENTRY_RE.findall(journals),
        )

    def test_repository_manifests_are_current(self):
        deferred = validate.check_deferred_release_gates()
        checks = (
            validate.check_local_override_inventory(),
            validate.check_map_data(),
            validate.check_localization(),
            validate.check_on_action_router(),
            validate.check_stale_symbols(),
            validate.check_unused_symbols(),
            validate.check_runtime_script_contracts(),
            validate.check_release_invariants(),
            validate.check_delayed_lifecycle(),
        )
        failures = [f"{check.name}: {check.detail}" for check in checks if check.status != "PASS"]
        self.assertEqual([], failures)
        self.assertEqual("WARN", deferred.status, deferred.detail)

    def test_delayed_inventory_counts_duplicate_dispatches(self):
        first = ("events/a.txt", "example.1", (("days", "3"),), "yes")
        second = ("events/b.txt", "example.1", (("months", "1"),), "default")

        count, digest, destinations = validate.delayed_inventory((first, second))
        reversed_count, reversed_digest, _ = validate.delayed_inventory((second, first))

        self.assertEqual(2, count)
        self.assertEqual({"example.1"}, destinations)
        self.assertEqual(count, reversed_count)
        self.assertEqual(digest, reversed_digest)

    def test_braced_parser_ignores_comment_and_quoted_braces(self):
        source = 'event = { text = "{quoted}" # } ignored\n effect = { value = 1 } }'
        self.assertEqual(source, validate.extract_braced(source, 0))

    def test_runtime_contracts_reject_known_engine_only_failures(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            journals = root / "common/journal_entries"
            history = root / "common/history/countries"
            effects = root / "common/scripted_effects"
            journals.mkdir(parents=True)
            history.mkdir(parents=True)
            effects.mkdir(parents=True)
            (journals / "fixture.txt").write_text(
                "je_global = {\n"
                " group = je_group_global_international_situations\n"
                " is_shown_when_inactive = { always = yes }\n"
                "}\n"
                "je_country = { group = je_group_events }\n"
            )
            (history / "fixture.txt").write_text(
                "FIX = {\n"
                " add_journal_entry = { type = je_global }\n"
                " add_contextless_journal_entry = je_country\n"
                "}\n"
            )
            (effects / "fixture.txt").write_text(
                "bad_effect = {\n"
                " set_variable = { name = zeroable_delta_var value = var:left }\n"
                " change_variable = { name = zeroable_delta_var subtract = var:right }\n"
                " if = { limit = { var:zeroable_delta_var = 0 } }\n"
                " remove_variable = zeroable_delta_var\n"
                " # change_variable = { name = commented_delta_var subtract = 1 }\n"
                " set_variable = { name = leaked_delta_var value = 1 }\n"
                "}\n"
            )

            errors = validate.runtime_script_hazards(root)
            self.assertTrue(any("collapse to an unset zero" in error for error in errors))
            self.assertTrue(any("must use add_contextless" in error for error in errors))
            self.assertTrue(any("created twice at startup" in error for error in errors))
            self.assertTrue(any("country journal" in error for error in errors))
            self.assertTrue(any("temporary delta variable" in error for error in errors))
            self.assertFalse(any("commented" in error for error in errors))

    def test_runtime_contracts_accept_safe_equivalents(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            journals = root / "common/journal_entries"
            history = root / "common/history/countries"
            effects = root / "common/scripted_effects"
            journals.mkdir(parents=True)
            history.mkdir(parents=True)
            effects.mkdir(parents=True)
            (journals / "fixture.txt").write_text(
                "je_global = { group = je_group_global_international_situations }\n"
                "je_country = { group = je_group_events }\n"
            )
            (history / "fixture.txt").write_text(
                "FIX = {\n"
                " add_contextless_journal_entry = je_global\n"
                " add_journal_entry = { type = je_country }\n"
                "}\n"
            )
            (effects / "fixture.txt").write_text(
                "safe_effect = {\n"
                " if = {\n"
                "  limit = { has_variable = left has_variable = right }\n"
                "  if = { limit = { var:left = var:right } }\n"
                " }\n"
                "}\n"
            )

            self.assertEqual([], validate.runtime_script_hazards(root))


class LocalizationReviewNamespaceTests(unittest.TestCase):
    def test_numbered_event_marker_stays_on_its_exact_namespace(self):
        fixture = (
            "l_english:\n"
            "# ### REVIEWED ###\n"
            " sb_griqualand_west.260.t:0 \"Reviewed title\"\n"
            " sb_griqualand_west.260.d:0 \"Reviewed description\"\n"
            " sb_griqualand_west.261.t:0 \"Later event\"\n"
            " sb_griqualand_west_251_independent_tt:0 \"General tooltip\"\n"
            " dp_sb_griqualand_revoke_claim:0 \"Diplomatic play\"\n"
        )

        self.assertEqual(
            [("event", "sb_griqualand_west.260", "REVIEWED", 2)],
            validate.localization_review_classifications(fixture, set()),
        )
        for key in (
            "sb_griqualand_west.260",
            "sb_griqualand_west.260.t",
            "sb_griqualand_west.260.d.variant",
            "sb_griqualand_west.260.a.tt",
        ):
            self.assertEqual(
                ("event", "sb_griqualand_west.260"),
                validate.resolve_localization_namespace(key, set()),
            )
        for key in (
            "sb_griqualand_west.260_tooltip",
            "sb_griqualand_west.260extra.t",
            "sb_griqualand_west.260..t",
            "sb_griqualand_west.260.",
            "sb_griqualand_west_251_independent_tt",
            "dp_sb_griqualand_revoke_claim",
        ):
            self.assertIsNone(validate.resolve_localization_namespace(key, set()))

    def test_unrelated_first_key_blocks_a_later_event(self):
        fixture = (
            "l_english:\n"
            "# ### TO REVIEW ###\n"
            "# A comment may be skipped, but the next key is the boundary.\n"
            " sb_general_tooltip:0 \"General prose\"\n"
            " sb_fixture.10.t:0 \"Later event\"\n"
            "# TO REVIEW (non-event/JE keys)\n"
            " sb_fixture.11.t:0 \"Plain comments never classify\"\n"
        )

        self.assertEqual(
            [],
            validate.localization_review_classifications(fixture, set()),
        )

    def test_longest_source_defined_journal_entry_id_wins(self):
        journal_entries = {
            "je_sb_natal_indenture_program",
            "je_sb_natal_indenture_program_v2",
        }

        self.assertEqual(
            ("journal_entry", "je_sb_natal_indenture_program_v2"),
            validate.resolve_localization_namespace(
                "je_sb_natal_indenture_program_v2_reason",
                journal_entries,
            ),
        )
        self.assertEqual(
            ("journal_entry", "je_sb_natal_indenture_program"),
            validate.resolve_localization_namespace(
                "je_sb_natal_indenture_program_reason",
                journal_entries,
            ),
        )
        self.assertEqual(
            [
                (
                    "journal_entry",
                    "je_sb_natal_indenture_program_v2",
                    "TO REVIEW",
                    2,
                )
            ],
            validate.localization_review_classifications(
                "l_english:\n"
                "# ### TO REVIEW ###\n"
                " je_sb_natal_indenture_program_v2_reason:0 \"V2 reason\"\n",
                journal_entries,
            ),
        )
        self.assertIsNone(
            validate.resolve_localization_namespace(
                "je_sb_natal_indenture_programmatic_reason",
                journal_entries,
            )
        )

    def test_overlapping_base_and_v2_journal_entries_get_distinct_markers(self):
        journal_entries = {
            "je_sb_natal_indenture_program",
            "je_sb_natal_indenture_program_v2",
        }
        fixture = (
            "l_english:\n"
            "# ### TO REVIEW ###\n"
            " je_sb_natal_indenture_program:0 \"Base JE\"\n"
            "# ### TO REVIEW ###\n"
            " je_sb_natal_indenture_program_v2:0 \"V2 JE\"\n"
            " je_sb_natal_indenture_program_v2_reason:0 \"V2 reason\"\n"
            " je_sb_natal_indenture_program_reason:0 \"Base reason\"\n"
        )

        self.assertEqual(
            [
                ("journal_entry", "je_sb_natal_indenture_program", "TO REVIEW", 2),
                ("journal_entry", "je_sb_natal_indenture_program_v2", "TO REVIEW", 4),
            ],
            validate.localization_review_classifications(fixture, journal_entries),
        )

    def test_journal_entry_suffix_marker_does_not_reach_the_next_je(self):
        fixture = (
            "l_english:\n"
            "# ### TO REVIEW ###\n"
            " je_sb_first_reason:0 \"First reason\"\n"
            " je_sb_second:0 \"Second title\"\n"
        )

        self.assertEqual(
            [("journal_entry", "je_sb_first", "TO REVIEW", 2)],
            validate.localization_review_classifications(
                fixture,
                {"je_sb_first", "je_sb_second"},
            ),
        )

    def test_unknown_journal_entry_key_blocks_a_later_source_je(self):
        fixture = (
            "l_english:\n"
            "# ### TO REVIEW ###\n"
            " je_sb_unknown_reason:0 \"Unknown JE-like key\"\n"
            " je_sb_real:0 \"Later source JE\"\n"
        )

        self.assertEqual(
            [],
            validate.localization_review_classifications(
                fixture,
                {"je_sb_real"},
            ),
        )

    def test_consecutive_formal_markers_are_reported_as_duplicates(self):
        fixture = (
            "l_english:\n"
            "# ### REVIEWED ###\n"
            "# ### TO REVIEW ###\n"
            " sb_fixture.20.t:0 \"Conflicting authority\"\n"
        )
        resolved = validate.localization_review_classifications(fixture, set())

        self.assertEqual(
            [
                ("event", "sb_fixture.20", "REVIEWED", 2),
                ("event", "sb_fixture.20", "TO REVIEW", 3),
            ],
            resolved,
        )
        errors = validate.review_classification_errors(
            {
                ("event", "sb_fixture.20"): [
                    (status, Path("fixture.yml"), line_number)
                    for _, _, status, line_number in resolved
                ]
            },
            {"sb_fixture.20"},
            set(),
        )
        self.assertIn(
            "sb_fixture.20: expected one review classification, found 2",
            errors,
        )
        self.assertIn("sb_fixture.20: duplicate review classifications", errors)

    def test_plain_general_review_group_is_contiguous_and_not_a_namespace_marker(self):
        fixture = (
            "l_english:\n"
            " # TO REVIEW (non-event/JE keys)\n"
            " first_key:0 \"First\"\n"
            " second_key:0 \"Second\"\n"
            "\n"
            " unmarked_key:0 \"Not in group\"\n"
            " # ### TO REVIEW ###\n"
            " sb_fixture.30.t:0 \"Event\"\n"
        )
        self.assertEqual(
            {"first_key", "second_key"},
            validate.general_localization_review_keys(fixture),
        )

    def test_plain_general_review_group_rejects_event_and_source_je_namespaces(self):
        fixture = (
            "l_english:\n"
            " # ### TO REVIEW ###\n"
            " # TO REVIEW (non-event/JE keys)\n"
            " sb_fixture.30.t:0 \"Event title\"\n"
            " je_sb_fixture_reason:0 \"JE reason\"\n"
            " ordinary_key:0 \"Ordinary\"\n"
        )
        keys = validate.general_localization_review_keys(fixture)
        self.assertEqual(
            [
                ("je_sb_fixture_reason", "journal_entry", "je_sb_fixture"),
                ("sb_fixture.30.t", "event", "sb_fixture.30"),
            ],
            validate.general_review_namespace_violations(keys, {"je_sb_fixture"}),
        )

    def test_general_review_queue_is_exact_and_non_dangling(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            loc = root / "localization/english/fixture_l_english.yml"
            loc.parent.mkdir(parents=True)
            loc.write_text(
                "l_english:\n"
                " # TO REVIEW (non-event/JE keys)\n"
                " fixture_key:0 \"Fixture\"\n"
            )
            queue = root / "Docs/localisation_review_queue.md"
            queue.parent.mkdir()
            queue.write_text(
                "| Localisation file | Exact key | Review note |\n"
                "|---|---|---|\n"
                "| `localization/english/fixture_l_english.yml` | `fixture_key` | Test. |\n"
            )
            definitions = {"fixture_key": loc}
            pairs = {("localization/english/fixture_l_english.yml", "fixture_key")}
            self.assertEqual(
                [],
                validate.localization_review_queue_errors(definitions, pairs, root),
            )

            queue.write_text(
                "| `localization/english/fixture_l_english.yml` | `wrong_key` | Test. |\n"
            )
            errors = validate.localization_review_queue_errors(definitions, pairs, root)
            self.assertTrue(any("not defined in declared file" in error for error in errors))
            self.assertTrue(any("missing from review queue" in error for error in errors))
            self.assertTrue(any("dangling" in error for error in errors))

    def test_source_journal_entry_ids_include_replacement_directives(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            journals = root / "common/journal_entries"
            journals.mkdir(parents=True)
            (journals / "fixture.txt").write_text(
                "je_sb_plain = { }\n"
                "REPLACE:je_sb_replaced = { }\n"
                "TRY_REPLACE:je_sb_try_replaced = { }\n"
                "REPLACE_OR_CREATE:je_sb_created = { }\n"
                "# je_sb_commented = { }\n"
                " other = { je_sb_nested = { } }\n"
            )

            self.assertEqual(
                {
                    "je_sb_plain",
                    "je_sb_replaced",
                    "je_sb_try_replaced",
                    "je_sb_created",
                },
                validate.source_journal_entry_ids(root),
            )

    def test_localized_journal_entries_require_one_classification(self):
        path = Path("fixture.yml")
        classifications = {
            ("event", "sb_fixture.1"): [("TO REVIEW", path, 2)],
            ("journal_entry", "je_sb_first"): [("REVIEWED", path, 5)],
        }

        self.assertEqual(
            [],
            validate.review_classification_errors(
                classifications,
                {"sb_fixture.1"},
                {"je_sb_first"},
            ),
        )
        self.assertEqual(
            ["je_sb_second: expected one review classification, found 0"],
            validate.review_classification_errors(
                classifications,
                {"sb_fixture.1"},
                {"je_sb_first", "je_sb_second"},
            ),
        )


if __name__ == "__main__":
    unittest.main()
