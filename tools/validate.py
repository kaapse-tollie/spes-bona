#!/usr/bin/env python3
"""Run Spes Bona's portable, non-writing repository validation suite."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
TEXT_ROOTS = ("common", "events", "localization", "map_data")
TRIGGER_EVENT_RE = re.compile(r"\btrigger_event\s*=\s*\{")
EVENT_ID_RE = re.compile(r"\bid\s*=\s*([A-Za-z0-9_.:-]+)")
TIMING_RE = re.compile(r"\b(days|months|years)\s*=\s*([^\s}]+)")
LOC_KEY_RE = re.compile(r"^\s*([^#\s][^:]*):\d*\s", re.MULTILINE)
LOC_REFERENCE_RE = re.compile(
    r"\b(?:title|desc|text)\s*=\s*((?:sb_|je_sb_|decision_sb_|concept_sb_|dp_sb_|state_trait_sb_|law_sb_)[A-Za-z0-9_.-]+)"
)
STATE_RE = re.compile(r"^(STATE_[A-Z0-9_]+)\s*=\s*\{", re.MULTILINE)
PROVINCE_RE = re.compile(r"x[0-9A-Fa-f]{6}")
HUB_RE = re.compile(r'^\s*(city|port|farm|mine|wood)\s*=\s*"(x[0-9A-Fa-f]{6})"', re.MULTILINE)
HARD_REPLACE_RE = re.compile(
    r"^(REPLACE|TRY_REPLACE|REPLACE_OR_CREATE):([^\s=]+)\s*=\s*\{", re.MULTILINE
)


@dataclass
class Check:
    name: str
    status: str
    detail: str = ""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract_braced(text: str, start: int) -> str:
    opening = text.find("{", start)
    if opening < 0:
        raise ValueError("missing opening brace")
    depth = 0
    quoted = False
    escaped = False
    commented = False
    for index in range(opening, len(text)):
        char = text[index]
        if commented:
            if char == "\n":
                commented = False
            continue
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == "#":
            commented = True
        elif char == '"':
            quoted = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("unclosed braced object")


def normalize_event_block(block: str) -> str:
    return " ".join(block.split())


def iter_delayed_dispatches(root: Path = ROOT) -> Iterable[tuple[str, str, tuple[tuple[str, str], ...], str]]:
    for base in ("common", "events"):
        for path in sorted((root / base).rglob("*.txt")):
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
            for match in TRIGGER_EVENT_RE.finditer(text):
                block = extract_braced(text, match.start())
                timings = tuple(TIMING_RE.findall(block))
                if not timings:
                    continue
                event_match = EVENT_ID_RE.search(block)
                if event_match is None:
                    continue
                popup_match = re.search(r"\bpopup\s*=\s*(yes|no)", block)
                yield (
                    path.relative_to(root).as_posix(),
                    event_match.group(1),
                    timings,
                    popup_match.group(1) if popup_match else "default",
                )


def delayed_inventory(dispatches: Iterable[tuple[str, str, tuple[tuple[str, str], ...], str]]) -> tuple[int, str, set[str]]:
    rows = list(dispatches)
    fingerprints = [
        "|".join((path, event_id, ",".join(f"{kind}={value}" for kind, value in timing), popup))
        for path, event_id, timing, popup in rows
    ]
    digest = hashlib.sha256("\n".join(sorted(fingerprints)).encode("utf-8")).hexdigest()
    return len(rows), digest, {event_id for _, event_id, _, _ in rows}


def check_delayed_lifecycle() -> Check:
    manifest_path = ROOT / "tools/delayed_event_lifecycle_manifest.json"
    if not manifest_path.is_file():
        return Check("delayed-event lifecycle", "FAIL", "manifest is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    count, digest, destinations = delayed_inventory(iter_delayed_dispatches())
    expected = manifest.get("inventory", {})
    errors: list[str] = []
    if expected.get("dispatch_count") != count:
        errors.append(f"dispatch count {count}, expected {expected.get('dispatch_count')}")
    if expected.get("sha256") != digest:
        errors.append(f"inventory hash {digest}, expected {expected.get('sha256')}")

    registered: set[str] = set()
    for route in manifest.get("routes", []):
        classification = route.get("classification")
        if classification not in {"interactive", "pending-state", "mechanical-finalizer", "narrative"}:
            errors.append(f"{route.get('name', '<unnamed>')}: invalid classification")
        event_ids = set(route.get("event_ids", []))
        overlap = registered & event_ids
        if overlap:
            errors.append(f"duplicate route registration: {', '.join(sorted(overlap))}")
        registered.update(event_ids)
        if not str(route.get("rationale", "")).strip():
            errors.append(f"{route.get('name', '<unnamed>')}: missing rationale")
        if classification in {"interactive", "pending-state"}:
            for field in (
                "lease_marker",
                "destination_revalidation",
                "cancellation_handling",
                "idempotent_outcome",
                "centralized_cleanup",
            ):
                if not str(route.get(field, "")).strip():
                    errors.append(f"{route.get('name', '<unnamed>')}: missing {field}")
    if destinations - registered:
        errors.append("unclassified destinations: " + ", ".join(sorted(destinations - registered)))
    if registered - destinations:
        errors.append("stale destinations: " + ", ".join(sorted(registered - destinations)))
    return Check("delayed-event lifecycle", "FAIL" if errors else "PASS", "; ".join(errors))


def parse_state_blocks(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8-sig")
    return {match.group(1): extract_braced(text, match.start()) for match in STATE_RE.finditer(text)}


def object_values(block: str, key: str) -> set[str]:
    match = re.search(rf"\b{re.escape(key)}\s*=\s*\{{", block)
    if match is None:
        return set()
    return {province.upper().replace("X", "x", 1) for province in PROVINCE_RE.findall(extract_braced(block, match.start()))}


def connected_components(nodes: set[str], adjacency: dict[str, list[str]]) -> list[set[str]]:
    remaining = set(nodes)
    components: list[set[str]] = []
    while remaining:
        start = min(remaining)
        component = {start}
        stack = [start]
        remaining.remove(start)
        while stack:
            current = stack.pop()
            for neighbor in adjacency.get(current, []):
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    component.add(neighbor)
                    stack.append(neighbor)
        components.append(component)
    return components


def check_map_data() -> Check:
    manifest_path = ROOT / "tools/map_connectivity_manifest.json"
    if not manifest_path.is_file():
        return Check("map data", "FAIL", "connectivity manifest is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    state_path = ROOT / manifest["state_region_file"]
    blocks = parse_state_blocks(state_path)
    errors: list[str] = []
    if sha256(ROOT / manifest["province_map"]) != manifest["province_map_sha256"]:
        errors.append("province raster hash changed; regenerate and review adjacency")

    province_owner: dict[str, str] = {}
    for state, block in blocks.items():
        provinces = object_values(block, "provinces")
        impassable = object_values(block, "impassable")
        for province in provinces:
            if province in province_owner:
                errors.append(f"{province} belongs to both {province_owner[province]} and {state}")
            province_owner[province] = state
        for hub_type, hub in HUB_RE.findall(block):
            hub = hub.upper().replace("X", "x", 1)
            if hub not in provinces:
                errors.append(f"{state} {hub_type} {hub} is outside its province list")
            if hub in impassable:
                errors.append(f"{state} {hub_type} {hub} is impassable")

    for state, contract in manifest.get("states", {}).items():
        block = blocks.get(state)
        if block is None:
            errors.append(f"missing state block {state}")
            continue
        provinces = object_values(block, "provinces")
        impassable = object_values(block, "impassable")
        adjacency = contract.get("adjacency", {})
        if set(adjacency) != provinces:
            errors.append(f"{state} adjacency keys do not match current province membership")
            continue
        passable = provinces - impassable
        components = connected_components(passable, adjacency)
        hubs = {hub.upper().replace("X", "x", 1) for _, hub in HUB_RE.findall(block)}
        main = next((component for component in components if component & hubs), max(components, key=len))
        isolated = sorted((sorted(component) for component in components if component is not main))
        allowed = sorted(sorted(component) for component in contract.get("allowed_isolated_components", []))
        if isolated != allowed:
            errors.append(f"{state} isolated components {isolated}, expected {allowed}")
    return Check("map data", "FAIL" if errors else "PASS", "; ".join(errors))


def check_localization() -> Check:
    errors: list[str] = []
    definitions: dict[str, Path] = {}
    folded: dict[str, str] = {}
    for path in sorted((ROOT / "localization/english").rglob("*.yml")):
        data = path.read_bytes()
        if not data.startswith(b"\xef\xbb\xbf"):
            errors.append(f"{path.name}: missing UTF-8 BOM")
        text = data.decode("utf-8-sig")
        if not text.startswith("l_english:"):
            errors.append(f"{path.name}: invalid language header")
        for key in LOC_KEY_RE.findall(text):
            key = key.strip()
            if key == "l_english":
                continue
            if key in definitions:
                errors.append(f"duplicate key {key}: {definitions[key].name}, {path.name}")
            definitions[key] = path
            lowered = key.casefold()
            if lowered in folded and folded[lowered] != key:
                errors.append(f"case-insensitive duplicate {folded[lowered]} / {key}")
            folded[lowered] = key

    allowlist_path = ROOT / "tools/localization_reference_allowlist.json"
    allowlist = set()
    if allowlist_path.is_file():
        allowlist = set(json.loads(allowlist_path.read_text(encoding="utf-8")).get("missing_keys", []))
    references: set[str] = set()
    for base in ("common", "events"):
        for path in (ROOT / base).rglob("*.txt"):
            references.update(LOC_REFERENCE_RE.findall(path.read_text(encoding="utf-8-sig", errors="ignore")))
    missing = references - set(definitions) - allowlist
    stale_allowlist = allowlist - (references - set(definitions))
    if missing:
        errors.append("missing referenced keys: " + ", ".join(sorted(missing)))
    if stale_allowlist:
        errors.append("stale localization allowlist: " + ", ".join(sorted(stale_allowlist)))
    return Check("localization", "FAIL" if errors else "PASS", "; ".join(errors))


def check_stale_symbols() -> Check:
    forbidden = {
        "sb_bechuanaland_transfer_dual_corridor_to_cap",
        "je_sb_cape_responsible_government_button",
        "sb_bst_cap_transfer_pending_var",
        "sb_bst_cap_transfer_resolved_var",
        "sb_bst_frontier.200",
        "sb_bst_frontier.205",
    }
    hits: list[str] = []
    for base in TEXT_ROOTS:
        for path in (ROOT / base).rglob("*"):
            if not path.is_file() or path.suffix not in {".txt", ".yml", ".gui"}:
                continue
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
            for symbol in forbidden:
                if symbol in text:
                    hits.append(f"{symbol} in {path.relative_to(ROOT)}")
    return Check("stale symbols", "FAIL" if hits else "PASS", "; ".join(hits))


def check_local_override_inventory() -> Check:
    path = ROOT / "Docs/compatibility/override_inventory.json"
    inventory = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    descriptor = (ROOT / "descriptor.mod").read_text(encoding="utf-8-sig")
    versions = re.findall(r'^\s*supported_version\s*=\s*"([^"]+)"', descriptor, re.MULTILINE)
    if versions != [inventory.get("target_game_version")]:
        errors.append("descriptor and override inventory target versions differ")
    for entry in inventory.get("same_path_files", []):
        mod_path = ROOT / entry["path"]
        if not mod_path.is_file():
            errors.append(f"missing override {entry['path']}")
        elif entry.get("mod_sha256") != sha256(mod_path):
            errors.append(f"mod hash drift: {entry['path']}")

    keyed: dict[tuple[str, str, str], str] = {}
    for base in ("common", "events", "gui"):
        base_path = ROOT / base
        if not base_path.exists():
            continue
        for mod_path in base_path.rglob("*"):
            if not mod_path.is_file() or mod_path.suffix not in {".txt", ".gui"}:
                continue
            text = mod_path.read_text(encoding="utf-8-sig", errors="ignore")
            for match in HARD_REPLACE_RE.finditer(text):
                identity = (mod_path.relative_to(ROOT).as_posix(), match.group(1), match.group(2))
                keyed[identity] = extract_braced(text, match.start())
    declared = {
        (entry["mod_path"], entry["directive"], entry["key"]): entry
        for entry in inventory.get("keyed_overrides", [])
    }
    for identity in sorted(set(keyed) - set(declared)):
        errors.append(f"unmanifested keyed override: {identity}")
    for identity in sorted(set(declared) - set(keyed)):
        errors.append(f"stale keyed override: {identity}")
    for identity in sorted(set(keyed) & set(declared)):
        digest = hashlib.sha256(keyed[identity].encode("utf-8")).hexdigest()
        if declared[identity].get("mod_object_sha256") != digest:
            errors.append(f"keyed override hash drift: {identity}")
    return Check("local override inventory", "FAIL" if errors else "PASS", "; ".join(errors))


def run_command(name: str, command: list[str], cwd: Path = ROOT) -> Check:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, env=env)
    output = (result.stdout + result.stderr).strip()
    if result.returncode == 0:
        return Check(name, "PASS")
    tail = "\n".join(output.splitlines()[-12:])
    return Check(name, "FAIL", tail)


def check_resources() -> Check:
    command = [sys.executable, "-B", "resource-rework/resources/scripts/resources.py", "test", "--no-write"]
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, env=env)
    failures = set(re.findall(r"^- \*\*FAIL\*\* `([^`]+)`", result.stdout, re.MULTILINE))
    baseline_path = ROOT / "tools/resource_validation_baseline.json"
    baseline = set(json.loads(baseline_path.read_text(encoding="utf-8")).get("allowed_failures", []))
    unexpected = failures - baseline
    stale = baseline - failures
    if unexpected or stale:
        details = []
        if unexpected:
            details.append("unexpected failures: " + ", ".join(sorted(unexpected)))
        if stale:
            details.append("stale baseline: " + ", ".join(sorted(stale)))
        return Check("resource audit", "FAIL", "; ".join(details))
    if failures:
        return Check("resource audit", "WARN", "known Medium-Low baseline: " + ", ".join(sorted(failures)))
    if result.returncode != 0:
        return Check("resource audit", "FAIL", "runner failed without a classified check")
    return Check("resource audit", "PASS")


def find_game_root(explicit: str | None) -> Path | None:
    candidates = [
        Path(explicit).expanduser() if explicit else None,
        Path(os.environ["VIC3_GAME_ROOT"]).expanduser() if os.environ.get("VIC3_GAME_ROOT") else None,
        Path.home() / "Library/Application Support/Steam/steamapps/common/Victoria 3/game",
        Path.home() / ".local/share/Steam/steamapps/common/Victoria 3/game",
    ]
    return next((path.resolve() for path in candidates if path and (path / "common").is_dir()), None)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-root", help="Optional Victoria 3 game directory for upstream comparison")
    parser.add_argument("--cmf-root", help="Optional Community Mod Framework directory")
    parser.add_argument("--tiger", action="store_true", help="Run vic3-tiger when its binary and game root are available")
    args = parser.parse_args()

    checks = [
        run_command("unit tests", [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests"]),
        check_resources(),
        check_local_override_inventory(),
        check_map_data(),
        check_localization(),
        check_stale_symbols(),
        check_delayed_lifecycle(),
    ]

    game_root = find_game_root(args.game_root)
    if game_root is None:
        checks.append(Check("Vanilla/CMF override comparison", "SKIP", "game root not available"))
    else:
        command = [sys.executable, "-B", "tools/check_override_inventory.py", "--game-root", str(game_root)]
        if args.cmf_root:
            command.extend(("--cmf-root", args.cmf_root))
        checks.append(run_command("Vanilla/CMF override comparison", command))

    if args.tiger:
        tiger = shutil.which("vic3-tiger")
        if tiger is None or game_root is None:
            checks.append(Check("vic3-tiger", "SKIP", "binary or game root not available"))
        else:
            command = [
                tiger,
                "-c",
                "--no-color",
                "--game",
                str(game_root.parent),
                ROOT.name,
            ]
            checks.append(run_command("vic3-tiger", command, ROOT.parent))

    for check in checks:
        suffix = f": {check.detail}" if check.detail else ""
        print(f"[{check.status}] {check.name}{suffix}")
    failures = [check for check in checks if check.status == "FAIL"]
    print(f"\n{len(checks) - len(failures)}/{len(checks)} checks passed, warned, or skipped; {len(failures)} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
