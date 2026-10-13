from pathlib import Path
import re
import unittest

from tools.check_override_inventory import find_object


ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


class NatalUltimatumAndTransvaalTests(unittest.TestCase):
    def test_natalia_seizure_requires_no_active_or_previously_sent_ultimatum(self):
        decision = find_object(source("common/decisions/sb_zulu_decisions.txt"), "natalia_raid_port_natal")
        possible = decision[decision.index("\tpossible = {"):decision.index("\twhen_taken = {")]
        self.assertIn("text = sb_natalia_port_natal_before_ultimatum_tt", possible)
        self.assertRegex(possible, r"NOR\s*=\s*\{\s*has_variable = sb_british_natal_ultimatum_var\s*has_variable = sb_natalia_port_natal_raid_closed_var\s*\}")
        self.assertIn("is_at_war = no", possible)
        self.assertIn("p:x279045.state.owner = c:CAP", possible)
        self.assertIn("p:x279045.state.owner = c:GBR", possible)

    def test_closure_is_recorded_on_dispatch_and_never_cleared_by_crisis_cleanup(self):
        events = source("events/sb_natal_crisis_events.txt")
        event = find_object(events, "sb_natal_crisis.100")
        dispatch = event[event.index("name = sb_natal_crisis.100.a"):event.index("\t\tai_chance")]
        self.assertRegex(dispatch, r"scope:natalia\s*\?=\s*\{\s*set_variable = sb_british_natal_ultimatum_var\s*#[^\n]*\n\s*set_variable = sb_natalia_port_natal_raid_closed_var")
        self.assertLess(dispatch.index("set_variable = sb_natalia_port_natal_raid_closed_var"), dispatch.index("id = sb_natal_crisis.109"))
        scripts = "\n".join(p.read_text(encoding="utf-8-sig") for base in (ROOT / "common", ROOT / "events") for p in base.rglob("*.txt"))
        self.assertNotIn("remove_variable = sb_natalia_port_natal_raid_closed_var", scripts)

    def test_transvaal_restores_original_founding_province_priority(self):
        effect = find_object(source("common/scripted_effects/sb_trek_migration.txt"), "sb_spawn_transvaal_republic_v2")
        creation = effect[:effect.index("\t\ts:STATE_TRANSVAAL = {")]
        provinces = re.findall(r"province = p:(x[0-9A-F]+)", creation)
        self.assertEqual(["xD0A010", "x8BDC4D", "xA22DC2", "xD02190", "x6C1786", "x9A137B"], provinces)
        self.assertIn("NOT = { exists = c:TRN }", creation)
        self.assertRegex(creation, r"if = \{\s*limit = \{ p:xD0A010.state.owner = root \}\s*create_country = \{\s*tag = TRN\s*origin = c:ORA\s*province = p:xD0A010")


if __name__ == "__main__":
    unittest.main()
