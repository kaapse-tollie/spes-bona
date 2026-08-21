#!/usr/bin/env python3
"""Synchronize CMF and run Spes Bona's repository validation suite."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
from typing import Iterable
import zlib


ROOT = Path(__file__).resolve().parents[1]
CMF_ID = "com.github.Victoria-3-Modding-Co-op.Community-Mod-Framework"
CMF_PINNED_VERSION = "1.63.0"
DEFAULT_CMF_ROOT = ROOT.parent / "Community Mod Framework"
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
STATE_ID_RE = re.compile(r"\bid\s*=\s*(\d+)")
TERRAIN_RE = re.compile(r'^\s*(x[0-9A-Fa-f]{6})\s*=\s*"([^"]+)"', re.MULTILINE)
LOCATOR_INSTANCE_RE = re.compile(
    r"\{\s*id=(\d+)\s*position=\{\s*([-0-9.]+)\s+[-0-9.]+\s+([-0-9.]+)\s*\}",
    re.DOTALL,
)
REVIEW_MARKER_RE = re.compile(r"^\s*#\s*###\s+(TO REVIEW|REVIEWED)\s+###\s*$")
EVENT_LOC_KEY_RE = re.compile(r"^\s*([A-Za-z0-9_]+\.\d+)(?:\.[^:]*)?:\d*\s")
SCRIPT_EVENT_RE = re.compile(r"^([A-Za-z0-9_]+\.\d+)\s*=\s*\{", re.MULTILINE)
TOP_LEVEL_OBJECT_RE = re.compile(r"^([A-Za-z0-9_]+)\s*=\s*\{", re.MULTILINE)
HARD_REPLACE_RE = re.compile(
    r"^(REPLACE|TRY_REPLACE|REPLACE_OR_CREATE):([^\s=]+)\s*=\s*\{", re.MULTILINE
)
SB_SYMBOL_RE = re.compile(r"\bsb_[A-Za-z0-9_.]+\b")
SB_DEFINITION_RE = re.compile(
    r"^(?:(?:REPLACE|TRY_REPLACE|REPLACE_OR_CREATE):)?(sb_[A-Za-z0-9_]+)\s*=\s*\{",
    re.MULTILINE,
)
EXPECTED_DEFERRED_GATES = {"BC-20", "BC-22", "CP-07", "SUP-05", "QUAL-09", "CONTENT-01"}


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


def decode_rgb_png(
    path: Path, sample_points: set[tuple[int, int]]
) -> tuple[int, int, set[str], dict[tuple[int, int], str]]:
    payload = path.read_bytes()
    if payload[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")

    offset = 8
    compressed = bytearray()
    width = height = bit_depth = color_type = interlace = None
    while offset < len(payload):
        length = struct.unpack(">I", payload[offset : offset + 4])[0]
        chunk_type = payload[offset + 4 : offset + 8]
        chunk = payload[offset + 8 : offset + 8 + length]
        offset += length + 12
        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type, _, _, interlace = struct.unpack(">IIBBBBB", chunk)
        elif chunk_type == b"IDAT":
            compressed.extend(chunk)
        elif chunk_type == b"IEND":
            break

    if (bit_depth, color_type, interlace) != (8, 2, 0):
        raise ValueError(
            f"unsupported PNG format: depth={bit_depth}, color={color_type}, interlace={interlace}"
        )
    assert width is not None and height is not None

    raw = zlib.decompress(bytes(compressed))
    bytes_per_pixel = 3
    stride = width * bytes_per_pixel
    cursor = 0
    previous = bytearray(stride)
    colors: set[str] = set()
    samples: dict[tuple[int, int], str] = {}
    samples_by_row: dict[int, set[int]] = {}
    for x, y in sample_points:
        samples_by_row.setdefault(y, set()).add(x)

    for y in range(height):
        filter_type = raw[cursor]
        cursor += 1
        current = bytearray(raw[cursor : cursor + stride])
        cursor += stride
        for index in range(stride):
            left = current[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
            above = previous[index]
            upper_left = previous[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
            if filter_type == 1:
                current[index] = (current[index] + left) & 0xFF
            elif filter_type == 2:
                current[index] = (current[index] + above) & 0xFF
            elif filter_type == 3:
                current[index] = (current[index] + ((left + above) // 2)) & 0xFF
            elif filter_type == 4:
                estimate = left + above - upper_left
                left_distance = abs(estimate - left)
                above_distance = abs(estimate - above)
                upper_left_distance = abs(estimate - upper_left)
                predictor = (
                    left
                    if left_distance <= above_distance and left_distance <= upper_left_distance
                    else above
                    if above_distance <= upper_left_distance
                    else upper_left
                )
                current[index] = (current[index] + predictor) & 0xFF
            elif filter_type != 0:
                raise ValueError(f"unsupported PNG filter {filter_type}")

        for index in range(0, stride, bytes_per_pixel):
            colors.add(f"x{current[index]:02X}{current[index + 1]:02X}{current[index + 2]:02X}")
        for x in samples_by_row.get(y, ()):
            index = x * bytes_per_pixel
            samples[(x, y)] = f"x{current[index]:02X}{current[index + 1]:02X}{current[index + 2]:02X}"
        previous = current

    return width, height, colors, samples


def parse_locator_instances(path: Path) -> tuple[dict[int, tuple[float, float]], list[int]]:
    instances: dict[int, tuple[float, float]] = {}
    duplicates: list[int] = []
    text = path.read_text(encoding="utf-8-sig")
    for match in LOCATOR_INSTANCE_RE.finditer(text):
        identifier = int(match.group(1))
        if identifier in instances:
            duplicates.append(identifier)
        instances[identifier] = (float(match.group(2)), float(match.group(3)))
    return instances, duplicates


def check_map_data() -> Check:
    manifest_path = ROOT / "tools/map_connectivity_manifest.json"
    if not manifest_path.is_file():
        return Check("map data", "FAIL", "connectivity manifest is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    state_path = ROOT / manifest["state_region_file"]
    blocks = parse_state_blocks(state_path)
    errors: list[str] = []
    province_map = ROOT / manifest["province_map"]
    if sha256(province_map) != manifest["province_map_sha256"]:
        errors.append("province raster hash changed; regenerate and review adjacency")

    province_owner: dict[str, str] = {}
    state_ids: dict[str, int] = {}
    for state, block in blocks.items():
        identifier = STATE_ID_RE.search(block)
        if identifier is None:
            errors.append(f"{state} has no state id")
        else:
            state_ids[state] = int(identifier.group(1))
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

    duplicate_state_ids = sorted(
        identifier
        for identifier in set(state_ids.values())
        if list(state_ids.values()).count(identifier) > 1
    )
    if duplicate_state_ids:
        errors.append("duplicate state ids: " + ", ".join(map(str, duplicate_state_ids)))

    terrain_path = ROOT / manifest["terrain_file"]
    terrain_records: dict[str, str] = {}
    duplicate_terrain: set[str] = set()
    for province, terrain in TERRAIN_RE.findall(terrain_path.read_text(encoding="utf-8-sig")):
        province = province.upper().replace("X", "x", 1)
        if province in terrain_records:
            duplicate_terrain.add(province)
        terrain_records[province] = terrain
    if duplicate_terrain:
        errors.append("duplicate terrain records: " + ", ".join(sorted(duplicate_terrain)))
    missing_terrain = sorted(set(province_owner) - set(terrain_records))
    if missing_terrain:
        errors.append("state provinces missing terrain: " + ", ".join(missing_terrain))

    locator_instances: dict[str, dict[int, tuple[float, float]]] = {}
    sample_points: set[tuple[int, int]] = set()
    for kind, relative_path in manifest.get("locator_files", {}).items():
        locator_path = ROOT / relative_path
        instances, duplicates = parse_locator_instances(locator_path)
        locator_instances[kind] = instances
        if duplicates:
            errors.append(
                f"{kind} locator has duplicate ids: " + ", ".join(map(str, sorted(set(duplicates))))
            )

    pending_samples: list[tuple[str, str, int, str, tuple[int, int]]] = []
    raster_height = manifest.get("province_map_height", 3616)
    for sample in manifest.get("locator_samples", []):
        state = sample["state"]
        kind = sample["kind"]
        identifier = state_ids.get(state)
        block = blocks.get(state)
        if identifier is None or block is None:
            errors.append(f"locator sample references unknown state {state}")
            continue
        expected_hubs = {key: value.upper().replace("X", "x", 1) for key, value in HUB_RE.findall(block)}
        expected = expected_hubs.get(kind)
        position = locator_instances.get(kind, {}).get(identifier)
        if expected is None or position is None:
            errors.append(f"{state} has no {kind} hub or locator")
            continue
        x = round(position[0])
        y = raster_height - 1 - round(position[1])
        sample_points.add((x, y))
        pending_samples.append((state, kind, identifier, expected, (x, y)))

    try:
        width, height, raster_colors, raster_samples = decode_rgb_png(province_map, sample_points)
    except (OSError, ValueError, zlib.error) as error:
        errors.append(f"cannot validate province raster: {error}")
        width = height = 0
        raster_colors = set()
        raster_samples = {}
    if height and height != raster_height:
        errors.append(f"province raster height {height}, expected {raster_height}")
    missing_raster = sorted(set(province_owner) - raster_colors)
    if missing_raster:
        errors.append("state provinces missing from raster: " + ", ".join(missing_raster))
    for state, kind, identifier, expected, point in pending_samples:
        x, y = point
        if not (0 <= x < width and 0 <= y < height):
            errors.append(f"{state} {kind} locator {identifier} is outside the raster")
            continue
        actual = raster_samples.get(point)
        if actual != expected:
            errors.append(f"{state} {kind} locator samples {actual}, expected {expected}")

    for relative_path, expected_hash in manifest.get("pinned_files", {}).items():
        pinned = ROOT / relative_path
        if not pinned.is_file():
            errors.append(f"missing pinned map file {relative_path}")
        elif sha256(pinned) != expected_hash:
            errors.append(f"pinned map file changed: {relative_path}")

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
    classifications: dict[str, list[tuple[str, Path, int]]] = {}
    reviewed = 0
    to_review = 0
    for path in sorted((ROOT / "localization/english").rglob("*.yml")):
        data = path.read_bytes()
        if not data.startswith(b"\xef\xbb\xbf"):
            errors.append(f"{path.name}: missing UTF-8 BOM")
        text = data.decode("utf-8-sig")
        if not text.startswith("l_english:"):
            errors.append(f"{path.name}: invalid language header")
        if data and not data.endswith(b"\n"):
            errors.append(f"{path.name}: missing final newline")
        for line_number, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                errors.append(f"{path.name}:{line_number}: trailing whitespace")
            if line.startswith("\t"):
                errors.append(f"{path.name}:{line_number}: leading tab")
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

        lines = text.splitlines()
        for index, line in enumerate(lines):
            marker = REVIEW_MARKER_RE.match(line)
            if marker is None:
                continue
            for following in lines[index + 1 :]:
                key_match = EVENT_LOC_KEY_RE.match(following)
                if key_match is not None:
                    event_id = key_match.group(1)
                    classifications.setdefault(event_id, []).append((marker.group(1), path, index + 1))
                    if marker.group(1) == "REVIEWED":
                        reviewed += 1
                    else:
                        to_review += 1
                    break
                if REVIEW_MARKER_RE.match(following):
                    break

    script_events: set[str] = set()
    for path in sorted((ROOT / "events").rglob("*.txt")):
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        script_events.update(SCRIPT_EVENT_RE.findall(text))
        for line_number, line in enumerate(text.splitlines(), 1):
            if "### TO REVIEW ###" in line or "### REVIEWED ###" in line:
                errors.append(f"{path.name}:{line_number}: review marker belongs in localization")

    localized_events = {
        event_id for event_id in script_events if f"{event_id}.t" in definitions
    }
    for event_id in sorted(localized_events):
        entries = classifications.get(event_id, [])
        if len(entries) != 1:
            errors.append(f"{event_id}: expected one review classification, found {len(entries)}")
    for event_id, entries in sorted(classifications.items()):
        if len(entries) != 1:
            errors.append(f"{event_id}: duplicate review classifications")

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

    support_key = "sb_griqualand_west.025.oranje_annexation_d"
    support_event = ROOT / "events/sb_griqualand_west_events.txt"
    if support_key not in definitions:
        errors.append(f"missing support key {support_key}")
    elif support_key not in support_event.read_text(encoding="utf-8-sig"):
        errors.append(f"{support_key} is not referenced by its event")

    coverage = f"event review coverage: {reviewed} reviewed, {to_review} to review"
    return Check(
        "localization",
        "FAIL" if errors else "PASS",
        "; ".join(errors + [coverage]),
    )


def check_on_action_router() -> Check:
    router = ROOT / "common/on_actions/sb_on_actions.txt"
    errors: list[str] = []
    text = router.read_text(encoding="utf-8-sig")
    if len(text.splitlines()) > 150:
        errors.append("central router exceeds 150 lines")
    handler_bodies = [key for key in TOP_LEVEL_OBJECT_RE.findall(text) if key.startswith("sb_")]
    if handler_bodies:
        errors.append("handler bodies remain in central router: " + ", ".join(handler_bodies))

    registered: list[str] = []
    for match in re.finditer(r"\bon_actions\s*=\s*\{", text):
        registered.extend(re.findall(r"\bsb_[A-Za-z0-9_]+\b", extract_braced(text, match.start())))

    definitions: dict[str, list[Path]] = {}
    for path in sorted((ROOT / "common/on_actions").glob("*.txt")):
        if path == router:
            continue
        handler_text = path.read_text(encoding="utf-8-sig", errors="ignore")
        for key in TOP_LEVEL_OBJECT_RE.findall(handler_text):
            if key.startswith("sb_"):
                definitions.setdefault(key, []).append(path)

    for handler in sorted(set(registered)):
        paths = definitions.get(handler, [])
        if len(paths) != 1:
            errors.append(f"{handler}: expected one definition, found {len(paths)}")
    duplicates = sorted(key for key, paths in definitions.items() if len(paths) > 1)
    if duplicates:
        errors.append("duplicate handler definitions: " + ", ".join(duplicates))
    return Check("on-action router", "FAIL" if errors else "PASS", "; ".join(errors))


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


def check_unused_symbols() -> Check:
    manifest_path = ROOT / "tools/unused_symbol_allowlist.json"
    if not manifest_path.is_file():
        return Check("unused symbols", "FAIL", "allowlist is missing")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    allowed_categories = {"engine-entry-point", "public-api", "save-api", "migration-api", "staged-api"}
    errors: list[str] = []
    allowlist: dict[str, dict] = {}
    for entry in manifest.get("symbols", []):
        symbol = entry.get("symbol")
        if not isinstance(symbol, str) or not symbol:
            errors.append("allowlist entry has no symbol")
            continue
        if symbol in allowlist:
            errors.append(f"duplicate unused-symbol allowlist entry: {symbol}")
        allowlist[symbol] = entry
        if entry.get("category") not in allowed_categories:
            errors.append(f"{symbol}: invalid category {entry.get('category')}")
        if not str(entry.get("definition", "")).strip():
            errors.append(f"{symbol}: missing definition path")
        if not str(entry.get("reason", "")).strip():
            errors.append(f"{symbol}: missing rationale")

    texts: dict[Path, str] = {}
    counts: Counter[str] = Counter()
    for base in ("common", "events", "localization"):
        for path in sorted((ROOT / base).rglob("*")):
            if not path.is_file() or path.suffix not in {".txt", ".yml", ".gui"}:
                continue
            source = path.read_text(encoding="utf-8-sig", errors="ignore")
            texts[path] = source
            counts.update(SB_SYMBOL_RE.findall(source))

    definitions: dict[str, list[str]] = {}
    for path, source in texts.items():
        relative = path.relative_to(ROOT).as_posix()
        for symbol in SB_DEFINITION_RE.findall(source):
            definitions.setdefault(symbol, []).append(relative)

    definition_only = {
        symbol: paths
        for symbol, paths in definitions.items()
        if counts[symbol] == 1
    }
    for symbol in sorted(set(definition_only) - set(allowlist)):
        errors.append(f"unclassified definition-only symbol: {symbol} in {definition_only[symbol][0]}")
    for symbol in sorted(set(allowlist) - set(definition_only)):
        errors.append(f"stale unused-symbol allowlist entry: {symbol}")
    for symbol in sorted(set(definition_only) & set(allowlist)):
        expected = allowlist[symbol].get("definition")
        if definition_only[symbol] != [expected]:
            errors.append(
                f"{symbol}: definition path {definition_only[symbol]}, expected {[expected]}"
            )

    detail = f"{len(definition_only)} reviewed definition-only symbols"
    return Check("unused symbols", "FAIL" if errors else "PASS", "; ".join(errors + [detail]))


def check_deferred_release_gates() -> Check:
    manifest_path = ROOT / "tools/deferred_release_gates.json"
    if not manifest_path.is_file():
        return Check("deferred release gates", "FAIL", "manifest is missing")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if manifest.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    gates: dict[str, dict] = {}
    for gate in manifest.get("gates", []):
        identifier = gate.get("id")
        if not isinstance(identifier, str) or not identifier:
            errors.append("gate has no id")
            continue
        if identifier in gates:
            errors.append(f"duplicate gate {identifier}")
        gates[identifier] = gate
        if gate.get("status") not in {"blocked", "deferred-human", "deferred-content"}:
            errors.append(f"{identifier}: invalid status {gate.get('status')}")
        for field in ("owner", "unblock_condition", "artifact", "acceptance_test"):
            if not str(gate.get(field, "")).strip():
                errors.append(f"{identifier}: missing {field}")

    missing = EXPECTED_DEFERRED_GATES - set(gates)
    extra = set(gates) - EXPECTED_DEFERRED_GATES
    if missing:
        errors.append("missing gates: " + ", ".join(sorted(missing)))
    if extra:
        errors.append("unexpected gates: " + ", ".join(sorted(extra)))
    return Check(
        "deferred release gates",
        "FAIL" if errors else "PASS",
        "; ".join(errors or [f"{len(gates)} explicit gates"]),
    )


def check_release_invariants() -> Check:
    errors: list[str] = []
    script_paths = [
        path
        for base in ("common", "events", "localization")
        for path in (ROOT / base).rglob("*")
        if path.is_file() and path.suffix in {".txt", ".yml", ".gui"}
    ]
    script_text = "\n".join(
        path.read_text(encoding="utf-8-sig", errors="ignore") for path in script_paths
    )

    for tag in ("XHG", "XHR", "XHT"):
        if re.search(rf"(?<![A-Za-z0-9_]){tag}(?![A-Za-z0-9_])", script_text):
            errors.append(f"retired country tag remains live: {tag}")
    retained_sgo_flag = ROOT / "gfx/coat_of_arms/textured_emblems/te_sgo_united_flag.tga"
    if not retained_sgo_flag.is_file():
        errors.append("retained SGO united flag is missing")

    router = (ROOT / "common/on_actions/sb_on_actions.txt").read_text(encoding="utf-8-sig")
    handlers = (ROOT / "common/on_actions/sb_regional_on_action_handlers.txt").read_text(
        encoding="utf-8-sig"
    )
    if len(re.findall(r"^on_company_disbanded\s*=", router, re.MULTILINE)) != 1:
        errors.append("SB must register exactly one company-disband on-action")
    if len(re.findall(r"^sb_on_mozambique_company_disbanded\s*=", handlers, re.MULTILINE)) != 1:
        errors.append("SB must define exactly one Mozambique disband handler")
    if "on_treaty_ports_inherited" in script_text or "renege_treaty_ports_with" in script_text:
        errors.append("SB must not shadow or duplicate Vanilla treaty-port inheritance")

    journal = (ROOT / "common/journal_entries/1-11_sb_bechuanaland_corridor.txt").read_text(
        encoding="utf-8-sig"
    )
    for token in (
        "gui/com_journal_injects/situation_widgets.gui",
        "sb_bechuanaland_project_corridor_journal = yes",
    ):
        if token not in journal:
            errors.append(f"Bechuanaland JE is missing its CMF 1.63 journal projection: {token}")
    for token in (
        "com_set_situation_left_title =",
        "com_set_situation_right_title =",
    ):
        if token in journal:
            errors.append(f"Bechuanaland illustration still displays an actor title overlay: {token}")

    corridor_effects = (
        ROOT / "common/scripted_effects/sb_bechuanaland_corridor_effects.txt"
    ).read_text(encoding="utf-8-sig")
    for token in (
        "sb_bechuanaland_project_corridor_journal = {",
        "je:je_sb_bechuanaland_corridor ?= {",
    ):
        if token not in corridor_effects:
            errors.append(f"Bechuanaland singleton JE projection is missing: {token}")
    for token in (
        "com_remove_situation_left_title = yes",
        "com_remove_situation_right_title = yes",
        "com_situation_left_title_var",
        "com_situation_right_title_var",
    ):
        if token in corridor_effects:
            errors.append(f"Bechuanaland singleton JE projection retains obsolete title plumbing: {token}")
    progress_bars = (ROOT / "common/scripted_progress_bars/sb_progress_bars.txt").read_text(
        encoding="utf-8-sig"
    )
    bar = progress_bars.split("sb_bechuanaland_boer_swa_influence_bar = {", 1)[-1]
    bar = bar.split("########################## END ZULU", 1)[0]
    if "container:sb_bechuanaland_corridor_state = {" not in bar:
        errors.append("Bechuanaland influence bar does not read its named container")
    if len(re.findall(r"has_variable\s*=\s*sb_bechuanaland_influence_source_", bar)) != 14:
        errors.append(
            "Bechuanaland influence bar must read all 14 cached source variables"
        )
    if "c:GBR ?= {" not in bar:
        errors.append("Bechuanaland contextless influence bar lacks a stable country scope")
    container_guard = "container_exists = sb_bechuanaland_corridor_state"
    container_scope = "container:sb_bechuanaland_corridor_state = {"
    if container_guard not in bar or (
        container_scope in bar and bar.index(container_guard) > bar.index(container_scope)
    ):
        errors.append("Bechuanaland influence bar reads its container without an existence guard")
    if "owner = {" in bar or "scope:journal_entry = {" in bar:
        errors.append("Bechuanaland contextless influence bar enters an invalid trigger scope")
    for path in (ROOT / "gui").glob("journal*.gui") if (ROOT / "gui").exists() else ():
        errors.append(f"obsolete journal GUI override remains: {path.relative_to(ROOT)}")

    war_goal_count = 0
    for path in [
        path
        for base in ("common", "events")
        for path in (ROOT / base).rglob("*.txt")
    ]:
        source = path.read_text(encoding="utf-8-sig", errors="ignore")
        for match in re.finditer(r"\badd_war_goal\s*=\s*\{", source):
            war_goal_count += 1
            block = extract_braced(source, match.start())
            line = source.count("\n", 0, match.start()) + 1
            missing = [
                key for key in ("holder", "type") if not re.search(rf"\b{key}\s*=", block)
            ]
            if not re.search(r"\btarget_(?:country|state)\s*=", block):
                missing.append("target_country/state")
            if missing:
                errors.append(
                    f"{path.relative_to(ROOT)}:{line}: incomplete add_war_goal ({', '.join(missing)})"
                )

    detail = f"{war_goal_count} complete scripted war-goal blocks"
    return Check("1.13.11 release invariants", "FAIL" if errors else "PASS", "; ".join(errors or [detail]))


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


def check_cmf_install(cmf_root: Path) -> Check:
    metadata_path = cmf_root / ".metadata/metadata.json"
    errors: list[str] = []
    if not metadata_path.is_file():
        return Check("CMF compatibility", "FAIL", f"CMF is not installed at {cmf_root}")
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return Check("CMF compatibility", "FAIL", f"invalid CMF metadata: {exc}")
    if metadata.get("id") != CMF_ID:
        errors.append(f"unexpected metadata id {metadata.get('id')}")
    if metadata.get("version") != CMF_PINNED_VERSION:
        errors.append(
            f"latest CMF is {metadata.get('version')}; SB remains pinned to "
            f"{CMF_PINNED_VERSION} and requires a rebase"
        )
    for relative in (
        "common/scripted_effects/com_general_effects.txt",
        "common/scripted_effects/com_international_situation_effects.txt",
        "common/console_command_macros/com_macros.txt",
        "gui/com_journal_injects/situation_widgets.gui",
    ):
        if not (cmf_root / relative).is_file():
            errors.append(f"missing CMF API file {relative}")
    return Check("CMF compatibility", "FAIL" if errors else "PASS", "; ".join(errors))


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
    parser.add_argument(
        "--skip-cmf-sync",
        action="store_true",
        help="Use the installed CMF without querying or updating from GitHub",
    )
    parser.add_argument("--tiger", action="store_true", help="Run vic3-tiger when its binary and game root are available")
    args = parser.parse_args()

    cmf_root = Path(args.cmf_root).expanduser().absolute() if args.cmf_root else DEFAULT_CMF_ROOT
    checks = []
    if args.skip_cmf_sync:
        checks.append(Check("CMF release sync", "SKIP", "disabled by --skip-cmf-sync"))
    else:
        checks.append(run_command(
            "CMF release sync",
            [sys.executable, "-B", "tools/sync_cmf.py", "--target", str(cmf_root)],
        ))
    checks.extend([
        check_cmf_install(cmf_root),
        run_command("unit tests", [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests"]),
        check_local_override_inventory(),
        check_map_data(),
        check_localization(),
        check_on_action_router(),
        check_stale_symbols(),
        check_unused_symbols(),
        check_deferred_release_gates(),
        check_release_invariants(),
        check_delayed_lifecycle(),
    ])

    game_root = find_game_root(args.game_root)
    if game_root is None:
        checks.append(Check("Vanilla/CMF override comparison", "SKIP", "game root not available"))
    else:
        command = [sys.executable, "-B", "tools/check_override_inventory.py", "--game-root", str(game_root)]
        if cmf_root.is_dir():
            command.extend(("--cmf-root", str(cmf_root)))
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
