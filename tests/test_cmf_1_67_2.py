"""Exact CMF 1.67.2 deltas and scripted-wrapper argument regression checks."""

import json
from pathlib import Path
import re
import unittest

from tools import cmf_patch
from tools.check_override_inventory import extract_braced_object, find_object
from tests.test_zulu_institutions_laws import statements


ROOT = Path(__file__).resolve().parents[1]
CMF = ROOT.parent / "Community Mod Framework"
DEMO = "common/journal_entries/com_progress_in_style.txt"
TRIGGERS = "common/scripted_triggers/com_progress_bar_triggers.txt"
EMPTY_CALL = (
    b"\t\trun_in_com_progress_bar_scope = {\n"
    b"\t\t\tprogress_bar = spb_com_progress_in_style\n"
    b'\t\t#\t"<effects>" #just add your effect here in quotes\n'
    b"\t\t}\n"
)
DEBUG_LINE = b"            debug_log_details = true\n"


def missing_wrapper_arguments(source, required):
    errors = []
    # Match calls, excluding REPLACE_OR_CREATE definitions and comments.
    for key, parameters in required.items():
        for match in re.finditer(r"(?m)^\s*" + re.escape(key) + r"\s*=\s*\{", source):
            call = extract_braced_object(source, match.start())
            supplied = {name for name, _, _ in statements(call)}
            if missing := parameters - supplied:
                errors.append((key, missing))
    return errors


class Cmf1672PatchTests(unittest.TestCase):
    def payload(self, relative):
        revision = ROOT / "patches/cmf/sb-1.15.0-r2"
        patch = json.loads((revision / "manifest.json").read_text())
        entry = next(e for e in patch["files"] if e["path"] == relative)
        return entry, (revision / entry["payload"]).read_bytes()

    def test_historical_r2_kept_r1_payloads_and_native_contracts(self):
        previous = ROOT / "patches/cmf/sb-1.15.0-r1"
        old = json.loads((previous / "manifest.json").read_text())
        revision = ROOT / "patches/cmf/sb-1.15.0-r2"
        current = json.loads((revision / "manifest.json").read_text())
        self.assertEqual(old["upstream_contracts"], current["upstream_contracts"])
        for entry in old["files"]:
            actual = next(e for e in current["files"] if e["path"] == entry["path"])
            payload = (revision / actual["payload"]).read_bytes()
            self.assertEqual(entry, actual)
            self.assertEqual((previous / entry["payload"]).read_bytes(), payload)

    def test_demo_preserves_every_byte_except_the_invalid_empty_call(self):
        entry, payload = self.payload(DEMO)
        anchor = b"\t}\n\n\ton_weekly_pulse = {"
        self.assertEqual(1, payload.count(anchor))
        original = payload.replace(anchor, EMPTY_CALL + anchor, 1)
        expected = "6c29627de593aa2ddfdf3ba568ac549d73f5d052a528329e7b34e172b213eb86"
        self.assertEqual(expected, entry["original_sha256"])
        self.assertEqual(expected, cmf_patch.digest(original))
        required = {"run_in_com_progress_bar_scope": {"progress_bar", "effect"}}
        self.assertEqual(
            [("run_in_com_progress_bar_scope", {"effect"})],
            missing_wrapper_arguments(original.decode("utf-8-sig"), required),
        )
        self.assertEqual([], missing_wrapper_arguments(payload.decode("utf-8-sig"), required))

    def test_trigger_preserves_every_byte_except_the_debug_directive(self):
        entry, payload = self.payload(TRIGGERS)
        anchor = b"\t\t}\n    }\n\tscope:com_$progress_bar$ ?= {"
        self.assertEqual(1, payload.count(anchor))
        original = payload.replace(anchor, DEBUG_LINE + anchor, 1)
        expected = "62a484a1253021acfa4c7a677c8408d82bc9458a35cec23c57172aee616003e7"
        self.assertEqual(expected, entry["original_sha256"])
        self.assertEqual(expected, cmf_patch.digest(original))
        self.assertNotIn(b"debug_log_details", payload)

    def test_effective_wrapper_calls_supply_their_required_arguments(self):
        effects = "common/scripted_effects/com_progressbar_effects.txt"
        required = {}
        for path, key in (
            (effects, "run_in_com_progress_bar_scope"),
            (TRIGGERS, "test_in_com_progress_bar_scope"),
        ):
            source = (CMF / path).read_text(encoding="utf-8-sig")
            body = find_object(source, key, directive="REPLACE_OR_CREATE")
            required[key] = set(re.findall(r"\$([a-z_]+)\$", body))
        self.assertEqual({"progress_bar", "effect"}, required["run_in_com_progress_bar_scope"])
        self.assertEqual({"progress_bar", "trigger"}, required["test_in_com_progress_bar_scope"])
        for path in (DEMO, TRIGGERS, effects, "common/scripted_buttons/com_progress_in_style_buttons.txt"):
            with self.subTest(path=path):
                source = (CMF / path).read_text(encoding="utf-8-sig")
                self.assertEqual([], missing_wrapper_arguments(source, required))


if __name__ == "__main__":
    unittest.main()
