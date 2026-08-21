from pathlib import Path
import re
import unittest

from tools import validate


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = validate.find_game_root(None)

UNCOVERED_NAMESPACES = (
    "sb_boer_compacts",
    "sb_frontier_ai_wars",
    "sb_gaza",
    "sb_griqualand_east",
    "sb_griqualand_west",
    "sb_swazi_border",
    "sb_swazi_frontier",
    "sb_zulu_court",
)

# Domains whose SB-authored files only need structural smoke coverage: every file
# parses, top-level object names stay unique across the domain, and no file is empty.
DATA_DOMAINS = (
    "buildings",
    "building_groups",
    "character_traits",
    "cultures",
    "customizable_localization",
    "diplomatic_catalysts",
    "diplomatic_plays",
    "discrimination_traits",
    "dynamic_country_map_colors",
    "dynamic_country_names",
    "effect_localization",
    "game_rules",
    "government_types",
    "interest_group_traits",
    "named_colors",
    "script_values",
    "scripted_buttons",
    "subject_types",
    "technology",
    "war_goal_types",
)


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def localization_keys() -> set[str]:
    keys: set[str] = set()
    for path in sorted((ROOT / "localization").rglob("*.yml")):
        for match in re.finditer(r"^\s*([A-Za-z0-9_.]+):\d+", path.read_text(encoding="utf-8-sig"), re.MULTILINE):
            keys.add(match.group(1))
    return keys


def defined_event_ids() -> set[str]:
    ids: set[str] = set()
    for path in sorted((ROOT / "events").rglob("*.txt")):
        source = path.read_text(encoding="utf-8-sig")
        for match in re.finditer(r"^\s*([a-z_0-9]+\.\d+)\s*=\s*\{", source, re.MULTILINE):
            ids.add(match.group(1))
    return ids


def vanilla_event_ids() -> set[str]:
    if GAME_ROOT is None:
        return set()
    ids: set[str] = set()
    for path in sorted((GAME_ROOT / "events").rglob("*.txt")):
        try:
            source = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        for match in re.finditer(r"^\s*([a-z_0-9]+\.\d+)\s*=\s*\{", source, re.MULTILINE):
            ids.add(match.group(1))
    return ids


def repo_source_without(path_prefixes: tuple[str, ...]) -> str:
    chunks = []
    for prefix in path_prefixes:
        base = ROOT / prefix
        if base.is_dir():
            for path in sorted(base.rglob("*.txt")):
                chunks.append(path.read_text(encoding="utf-8-sig"))
    return "\n".join(chunks)


class EventNamespaceSmokeTests(unittest.TestCase):
    """Smoke contracts for the eight event chains that had no direct test coverage.

    Per namespace: every event parses, carries title/desc localisation that resolves,
    every namespaced localisation reference resolves, every trigger_event target is
    defined (mod or vanilla), and every event is dispatched from somewhere.
    """

    def setUp(self):
        self.loc = localization_keys()
        self.mod_ids = defined_event_ids()
        self.vanilla_ids = vanilla_event_ids()

    def namespace_events(self, ns: str) -> dict[str, str]:
        source = text(f"events/{ns}_events.txt")
        events = {}
        for match in re.finditer(rf"^\s*({ns}\.\d+)\s*=\s*\{{", source, re.MULTILINE):
            events[match.group(1)] = validate.extract_braced(source, match.start())
        return events

    def test_namespaces_define_events(self):
        for ns in UNCOVERED_NAMESPACES:
            events = self.namespace_events(ns)
            self.assertGreater(len(events), 0, f"{ns} defines no events")

    def test_event_blocks_parse_and_carry_localisation(self):
        problems = []
        for ns in UNCOVERED_NAMESPACES:
            for eid, block in self.namespace_events(ns).items():
                if "\ttitle = " not in block and "hidden = yes" not in block:
                    problems.append(f"{eid}: no title and not hidden")
                for field in ("title", "desc"):
                    m = re.search(rf"\{field} = ([A-Za-z0-9_.]+)", block)
                    if m and m.group(1) not in self.loc:
                        problems.append(f"{eid}: {field} key missing from localisation: {m.group(1)}")
        self.assertEqual([], problems)

    def test_namespaced_localisation_references_resolve(self):
        problems = []
        for ns in UNCOVERED_NAMESPACES:
            for eid, block in self.namespace_events(ns).items():
                for key in set(re.findall(rf"\b{ns}\.\d+\.[A-Za-z0-9_]+\b", block)):
                    if key not in self.loc:
                        problems.append(f"{eid}: localisation key missing: {key}")
        self.assertEqual([], problems)

    def test_trigger_event_targets_are_defined(self):
        problems = []
        known = self.mod_ids | self.vanilla_ids
        for ns in UNCOVERED_NAMESPACES:
            for eid, block in self.namespace_events(ns).items():
                for target in re.findall(r"trigger_event = \{[^}]*id\s*=\s*([a-z_0-9]+\.\d+)", block):
                    if target not in known:
                        problems.append(f"{eid}: trigger_event target undefined: {target}")
        self.assertEqual([], problems)

    def test_every_event_is_dispatched_somewhere(self):
        haystack = repo_source_without(("common",))
        all_sources = [p.read_text(encoding="utf-8-sig") for p in sorted((ROOT / "events").rglob("*.txt"))]
        problems = []
        for ns in UNCOVERED_NAMESPACES:
            for eid in self.namespace_events(ns):
                pattern = re.compile(rf"\bid\s*=\s*{re.escape(eid)}\b")
                dispatched = any(pattern.search(src) for src in all_sources)
                dispatched = dispatched or re.search(rf"\bid\s*=\s*{re.escape(eid)}\b", haystack) is not None
                if not dispatched:
                    problems.append(f"{eid}: never dispatched (no id = {eid} reference)")
        self.assertEqual([], problems)


class DataDomainSmokeTests(unittest.TestCase):
    """Structural smoke coverage for SB-authored data domains that had none."""

    def test_domain_files_parse_with_unique_top_level_names(self):
        problems = []
        for domain in DATA_DOMAINS:
            base = ROOT / "common" / domain
            if not base.is_dir():
                continue
            seen: dict[str, str] = {}
            for path in sorted(base.rglob("*.txt")):
                source = path.read_text(encoding="utf-8-sig")
                self.assertGreater(len(source.strip()), 0, f"{path} is empty")
                depth = 0
                for match in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{|[{}]", source):
                    if match.group(1):
                        # top-level "key = {" (the match consumed its opening brace)
                        if depth == 0:
                            name = match.group(1)
                            if name in seen and seen[name] != str(path):
                                problems.append(f"{domain}: duplicate top-level '{name}' in {path} and {seen[name]}")
                            seen.setdefault(name, str(path))
                        depth += 1
                    elif match.group(0) == "{":
                        depth += 1
                    else:
                        depth -= 1
                        self.assertGreaterEqual(depth, 0, f"{path}: unbalanced braces")
                self.assertEqual(0, depth, f"{path}: unbalanced braces")
        self.assertEqual([], problems)

    def test_every_script_file_has_balanced_braces(self):
        """Cold-launch guard: an unbalanced file poisons every definition after it in
        the game database while static checks stay green (FA-19/20 regression class).
        Comment- and string-aware brace scan over all script files."""
        problems = []

        def scan(source: str, label: str):
            depth = 0
            in_string = False
            in_comment = False
            prev = ""
            for ch in source:
                if in_comment:
                    if ch == "\n":
                        in_comment = False
                elif in_string:
                    if ch == '"' and prev != "\\":
                        in_string = False
                elif ch == '"':
                    in_string = True
                elif ch == "#":
                    in_comment = True
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth < 0:
                        problems.append(f"{label}: unbalanced braces (extra closing)")
                        return
                prev = ch
            if depth != 0:
                problems.append(f"{label}: unbalanced braces (depth {depth} at EOF)")

        for base in ("common", "events"):
            for path in sorted((ROOT / base).rglob("*.txt")):
                scan(path.read_text(encoding="utf-8-sig"),
                     path.relative_to(ROOT).as_posix())
        self.assertEqual([], problems)

    def test_buildings_reference_known_building_groups(self):
        group_sources = [p.read_text(encoding="utf-8-sig") for p in sorted((ROOT / "common/building_groups").rglob("*.txt"))]
        if GAME_ROOT is not None:
            group_sources += [p.read_text(encoding="utf-8-sig") for p in sorted((GAME_ROOT / "common/building_groups").rglob("*.txt"))]
        groups = set()
        for source in group_sources:
            groups |= set(re.findall(r"^\s*(bg_[A-Za-z0-9_]+)\s*=\s*\{", source, re.MULTILINE))
        problems = []
        for path in sorted((ROOT / "common/buildings").rglob("*.txt")):
            source = path.read_text(encoding="utf-8-sig")
            for group in re.findall(r"building_group\s*=\s*(bg_[A-Za-z0-9_]+)", source):
                if group not in groups:
                    problems.append(f"{path.name}: unknown building group {group}")
        self.assertEqual([], problems)

    def test_named_colors_stay_in_range(self):
        source = text("common/named_colors/sb_country_colors.txt")
        bad = [v for v in re.findall(r"=\s*x?([0-9.]+)\s+", source)
               if v and float(v) > 1.001]
        self.assertEqual([], bad)

    def test_technologies_reference_known_eras(self):
        eras = set(re.findall(r"^\s*([a-z0-9_]+)\s*=\s*\{",
                              (GAME_ROOT / "common/technology/eras/00_eras.txt").read_text(encoding="utf-8-sig")
                              if GAME_ROOT else "", re.MULTILINE))
        if not eras:
            self.skipTest("vanilla game root unavailable")
        problems = []
        for path in sorted((ROOT / "common/technology").rglob("*.txt")):
            for era in re.findall(r"^\s*era\s*=\s*([a-z0-9_]+)", path.read_text(encoding="utf-8-sig"), re.MULTILINE):
                if era not in eras:
                    problems.append(f"{path.name}: unknown era {era}")
        self.assertEqual([], problems)


if __name__ == "__main__":
    unittest.main()
