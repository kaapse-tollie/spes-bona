from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


class NgiReframeTests(unittest.TestCase):
    """FA-23 disposition: NGI reframed as the Nguni Chiefdoms abstraction paying
    tribute to the Zulu kingdom, led by the attested Nhlangwini chief Fodo kaNombewu."""

    def test_display_name_reframed(self):
        loc = text("localization/english/sb_l_english.yml")
        self.assertIn(' NGI:0 "Nguni Chiefdoms"', loc)
        self.assertIn(' NGI_ADJ:0 "Nguni"', loc)
        self.assertNotIn('"Qwabe"', loc)

    def test_tribute_modifier_and_transfer_exist(self):
        mods = text("common/static_modifiers/sb_modifiers.txt")
        self.assertIn("sb_tribute_to_zul = {", mods)
        self.assertIn("sb_tribute_from_nguni = {", mods)
        values = text("common/script_values/sb_ngi_tribute_values.txt")
        for token in ("sb_ngi_tribute_payment", "sb_ngi_tribute_payment_neg"):
            self.assertIn(token, values)
        handlers = text("common/on_actions/sb_ngi_tribute_on_action_handlers.txt")
        for token in ("sb_on_ngi_tribute_monthly_pulse_country",
                      "add_treasury = sb_ngi_tribute_payment_neg",
                      "sb_tribute_from_nguni"):
            self.assertIn(token, handlers)
        wiring = text("common/on_actions/sb_on_actions.txt")
        self.assertIn("sb_on_ngi_tribute_monthly_pulse_country", wiring)

    def test_fodo_kanombewu_leads_the_tag(self):
        tpl = text("common/character_templates/sb_nguni_chiefdoms_characters.txt")
        for token in ("NGI_fodo_kanombewu", 'first_name = "Fodo"',
                      'last_name = "kaNombewu"', "ruler = yes", "historical = yes"):
            self.assertIn(token, tpl)
        hist = text("common/history/characters/ngi - nguni chiefdoms.txt")
        self.assertIn("template = NGI_fodo_kanombewu", hist)
        self.assertIn("c:NGI ?=", hist)
        # Regression guard: without name localisation the engine reverts the leader
        # to a random culture name at launch (shipped once; caught in cold-launch logs).
        loc = text("localization/english/sb_l_english.yml")
        self.assertIn(" Fodo:0 ", loc)
        self.assertIn(" kaNombewu:0 ", loc)


if __name__ == "__main__":
    unittest.main()
