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


if __name__ == "__main__":
    unittest.main()
