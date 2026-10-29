"""DP's specific .141 approval must not authorize neighboring or later prose."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import validate

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = "localization/english/sb_boer_conventions_l_english.yml"
NAMESPACE = "sb_boer_conventions.141"
APPROVED_SHA256 = "8e6d62ea3e3d6f6afc98f0377b991a68d8a9c833eec7303a70345c840ac2c756"


class ApprovedConventionTests(unittest.TestCase):
    def test_current_text_marker_and_exact_namespace_have_dp_approval(self):
        source = (ROOT / RELATIVE).read_text(encoding="utf-8-sig")
        rows = validate.localization_review_classifications(source, ())
        self.assertEqual([("event", NAMESPACE, "REVIEWED")],
                         [(kind, name, status) for kind, name, status, line in rows if name == NAMESPACE])
        self.assertEqual((APPROVED_SHA256, 708, 5), validate.reviewed_localization_digest(
            ROOT / RELATIVE, "event", NAMESPACE, ()
        ))
        fixture = json.loads((ROOT / "tools/reviewed_localization_baseline.json").read_text())
        entry = next(e for e in fixture["namespaces"] if e["namespace"] == NAMESPACE)
        self.assertEqual(APPROVED_SHA256, entry["sha256"])
        self.assertIn("DP approved", entry["approval"])

    def test_later_unapproved_edit_fails_without_expanding_namespace_boundaries(self):
        fixture = json.loads((ROOT / "tools/reviewed_localization_baseline.json").read_text())
        entry = next(e for e in fixture["namespaces"] if e["namespace"] == NAMESPACE)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / RELATIVE
            path.parent.mkdir(parents=True)
            source = (ROOT / RELATIVE).read_text(encoding="utf-8-sig")
            # Underscore suffixes and adjacent numbered events are outside this approval.
            source += '\n sb_boer_conventions.141_extra:0 "Outside approval"\n sb_boer_conventions.1410.d:0 "Outside approval"\n'
            path.write_text(source, encoding="utf-8-sig")
            baseline = root / "tools/reviewed_localization_baseline.json"
            baseline.parent.mkdir()
            baseline.write_text(json.dumps(dict(fixture, namespaces=[entry])))
            classifications = {("event", NAMESPACE): [("REVIEWED", path, 1)]}
            with patch.object(validate, "ROOT", root):
                self.assertEqual([], validate.reviewed_localization_baseline_errors((), classifications))
                path.write_text(source.replace('sb_boer_conventions.141.t:0 "The Bloemfontein Convention"',
                                               'sb_boer_conventions.141.t:0 "Unapproved replacement"'), encoding="utf-8-sig")
                errors = validate.reviewed_localization_baseline_errors((), classifications)
                self.assertTrue(any("prose drift" in error and NAMESPACE in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
