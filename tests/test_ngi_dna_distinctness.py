"""PLAN-zul-ngi-playtest-fixes step 6: Fodo kaNombewu must not share a face.

In 0.18.1 `dna_fodo_kanombewu` shipped as a verbatim copy of vanilla
`dna_mpande` (all 116 gene keys identical), which is why Fodo looked like
Mpande in game. This test pins real divergence against BOTH Zulu royal
genomes so that regression cannot recur silently.
"""
from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = validate.find_game_root(None)
FODO = ROOT / "common/dna_data/sb_ngi_leaders.txt"
MIN_DIFFERING = 30

GENE_PAT = re.compile(
    r"(gene_\w+|hairstyles|beards|mustaches|props|eye_accessory|eye_lashes_accessory|"
    r"teeth_accessory|outfits|coats|civilian_coats|medals|waistcoats|top_layer|"
    r"necklaces|legwear|headgear|hair_color|skin_color|eye_color)\s*=\s*\{([^{}]*)\}"
)


def parse_dna(text: str) -> dict:
    return {m.group(1): tuple(m.group(2).split()) for m in GENE_PAT.finditer(text)}


@unittest.skipIf(GAME_ROOT is None, "vanilla game root unavailable")
class TestFodoDnaDistinctness(unittest.TestCase):
    def test_fodo_differs_substantially_from_both_royals(self):
        fodo = parse_dna(FODO.read_text(encoding="utf-8-sig"))
        for label, rel in (
            ("dna_mpande", "common/dna_data/00_mpande.txt"),
            ("dna_dingane", "common/dna_data/00_dingane.txt"),
        ):
            other = parse_dna((GAME_ROOT / rel).read_text(encoding="utf-8-sig"))
            differing = sorted(k for k in fodo if fodo.get(k) != other.get(k))
            self.assertGreaterEqual(
                len(differing),
                MIN_DIFFERING,
                f"Fodo shares too many gene keys with {label}: "
                f"only {len(differing)} of {len(fodo)} keys differ",
            )


if __name__ == "__main__":
    unittest.main()
