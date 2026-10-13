"""Preserve historical 1.14.2 mirror-patch evidence; current parity is tested separately."""

import hashlib
from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]
CMF_1660_HASHES = {
    "00_annex_country.txt": "ed2d2e14e9fff7ff19f21a1e8dad480afd794598b5056281cae60eb8dd039a5a",
    "03_conquer_state.txt": "04c17110b7c1e7d378dfffa9266a92183eafc599a25f21d00a96c2b9a97502db",
    "21_return_state.txt": "40be5ed4419ddafcad007237f1af2027c7e8b7c5e1c687311dae67469a3600ab",
}
MIRROR = b"\tmirrored_wargoal = {\n\t\tmethod = territorial\n\t}\n\n"


class CmfWarGoalTimerTests(unittest.TestCase):
    def test_historical_1_14_2_goals_added_only_territorial_mirrors(self):
        for filename, digest in CMF_1660_HASHES.items():
            with self.subTest(filename=filename):
                self.assertFalse((ROOT / "common/war_goal_types" / filename).exists())
                payload = (ROOT / "patches/cmf/sb-1.14.2-r1/files/common/war_goal_types" / filename).read_bytes()
                self.assertEqual(1, payload.count(MIRROR))
                self.assertEqual(digest, hashlib.sha256(payload.replace(MIRROR, b"")).hexdigest())
                source = payload.decode("utf-8-sig")
                self.assertNotIn("assent_required", source)
                body = source[source.index("{") + 1:source.rindex("}")]
                top_level = {
                    match.group(1) for match in validate.top_level_matches(
                        re.compile(r"(?m)^\s*(\w+)\s*="), body,
                    )
                }
                self.assertIn("contestion_type", top_level)
                self.assertIn("mirrored_wargoal", top_level)


if __name__ == "__main__":
    unittest.main()
