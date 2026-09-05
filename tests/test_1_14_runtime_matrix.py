import hashlib
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "Docs/compatibility/1_14_0_open_beta_1_runtime_matrix.md"
HISTORICAL = ROOT / "Docs/compatibility/1_13_11_runtime_matrix.md"
HISTORICAL_SHA256 = "a32e9c62909386aa5e92f2bd7fa71de947b6f12121df736b739d0996658c0e2e"
ROW_RE = re.compile(r"^\| `(?P<id>OB1-[^`]+)` \|(?P<body>.*)\|$", re.MULTILINE)


class OpenBetaRuntimeMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = MATRIX.read_text(encoding="utf-8")
        cls.rows = [(match.group("id"), match.group("body")) for match in ROW_RE.finditer(cls.text)]

    def test_historical_1_13_runtime_evidence_is_byte_identical(self):
        self.assertEqual(HISTORICAL_SHA256, hashlib.sha256(HISTORICAL.read_bytes()).hexdigest())

    def test_matrix_has_exact_target_identity_and_no_runtime_certification(self):
        for token in (
            "25081502",
            "1.14-openbeta",
            "3868129321396195520",
            "0.20.0",
            "1.66.0",
            "807c32ff42b75714a3a0e090c0db3357b5e46ed7",
            "79dd0d434e6ffb617147ad1b91b73e6306139adfffcadf6774eeb32db3a09b8b",
            "not runtime-certified",
        ):
            self.assertIn(token, self.text)
        self.assertNotRegex(self.text, r"\|\s*(?:Pass|PASS)\s*\|")

    def test_all_52_runtime_rows_are_unique_and_engine_pending(self):
        identifiers = [identifier for identifier, _ in self.rows]
        self.assertEqual(52, len(identifiers))
        self.assertEqual(52, len(set(identifiers)))
        for identifier, body in self.rows:
            with self.subTest(identifier=identifier):
                self.assertEqual("Engine pending", body.rsplit("|", 1)[-1].strip())

    def test_carried_cases_and_griqualand_sequence_rows_are_complete(self):
        carried = {
            match.group(1): match.group(2)
            for match in re.finditer(r"^\| `(OB1-CF-\d{2})` \| `(RV-\d{2})` \|", self.text, re.MULTILINE)
        }
        self.assertEqual(
            {f"OB1-CF-{index:02d}": f"RV-{index:02d}" for index in range(1, 14)},
            carried,
        )
        identifiers = {identifier for identifier, _ in self.rows}
        self.assertTrue({f"OB1-GQ-{index:02d}" for index in range(0, 9)} <= identifiers)
        self.assertIn("Fail — blocker", self.text)
        self.assertIn("must not be relabelled pending", self.text)


if __name__ == "__main__":
    unittest.main()
