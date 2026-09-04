#!/usr/bin/env python3
"""Build the reviewed Victoria 3 1.13.11 -> 1.14.0 OB1 depot delta.

The script decodes Steam's protobuf depot-manifest envelope with only the Python
standard library.  It is intentionally pinned to the two retained core-depot
manifests.  A missing or different input fails closed instead of comparing against
whatever Steam currently calls "latest".
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import struct
import sys
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


PAYLOAD_MAGIC = 0x71F617D0
METADATA_MAGIC = 0x1F4812BE
SIGNATURE_MAGIC = 0x1B81B817
END_MAGIC = 0x32C415AB
DIRECTORY_FLAG = 0x40
SYMLINK_FLAG = 0x200
ZERO_SHA1 = "0" * 40


@dataclass(frozen=True)
class ManifestIdentity:
    label: str
    game_version: str
    steam_build: str
    depot_id: int
    manifest_id: int
    created_utc: str
    source_name: str
    source_size: int
    source_sha256: str
    entry_count: int


OLD_IDENTITY = ManifestIdentity(
    label="Victoria 3 1.13.11",
    game_version="1.13.11",
    steam_build="24799966",
    depot_id=529341,
    manifest_id=4498977168532327663,
    created_utc="2026-08-18T13:02:33Z",
    source_name="529341_4498977168532327663.manifest",
    source_size=4_732_224,
    source_sha256="5ffcff6dab4ad7d8008618c50413bb3dcaeb12608cbe9d3e93872fa287fc4ddc",
    entry_count=26_642,
)
NEW_IDENTITY = ManifestIdentity(
    label="Victoria 3 1.14.0 Open Beta 1",
    game_version="1.14.0",
    steam_build="25081502",
    depot_id=529341,
    manifest_id=3868129321396195520,
    created_utc="2026-09-01T09:43:27Z",
    source_name="529341_3868129321396195520.manifest",
    source_size=4_733_748,
    source_sha256="1c76bc89eebffc465999a90cfc8ded5c1e771c089bbecb05c86b0d4f6bde4977",
    entry_count=26_653,
)
EXPECTED_COUNTS = {"changed": 182, "added": 13, "removed": 2, "total": 197}
TARGET_BRANCH = "1.14-openbeta"

# These are the changed depot paths that intersect the pre-rebase SB override
# inventory: one exact-path shadow and six upstream sources for keyed overrides.
# SB-dependent APIs without a direct override are deliberately not called
# collisions; their dispositions still require adaptation where applicable.
SB_COLLISION_PATHS = frozenset(
    {
        "game/common/coat_of_arms/coat_of_arms/02_countries.txt",
        "game/common/dynamic_country_names/00_dynamic_country_names.txt",
        "game/common/interest_groups/00_armed_forces.txt",
        "game/common/scripted_triggers/00_ai_triggers.txt",
        "game/common/subject_types/00_subject_types.txt",
        "game/common/technology/technologies/30_society.txt",
        "game/gfx/map/spline_network/spline_network.splnet",
    }
)

MERGE_REQUIRED = frozenset(
    {
        "game/common/dynamic_country_names/00_dynamic_country_names.txt",
    }
)
MERGE_REQUIRED_RUNTIME_PENDING = frozenset(
    {
        "game/common/scripted_triggers/00_ai_triggers.txt",
        "game/common/subject_types/00_subject_types.txt",
        "game/gfx/map/spline_network/spline_network.splnet",
    }
)
REPIN_REVIEWED = SB_COLLISION_PATHS - MERGE_REQUIRED - MERGE_REQUIRED_RUNTIME_PENDING

DISPOSITION_DEFINITIONS = {
    "adapt-sb-contract-runtime-pending": (
        "No direct path collision, but the changed upstream contract requires SB-owned "
        "adaptation and remains Engine pending until the runtime matrix is run."
    ),
    "merge-required": (
        "A reviewed semantic collision must be merged into the SB-owned override; no "
        "separate runtime-only claim is attached to this row."
    ),
    "merge-required-runtime-pending": (
        "A reviewed semantic collision must be merged, and the resulting engine behavior "
        "remains Engine pending."
    ),
    "removed-unused-by-sb": (
        "The upstream path was removed and the SB source audit found no reference to it."
    ),
    "repin-reviewed-sb-surface": (
        "The SB surface was reviewed as semantically retained; refresh its upstream pin "
        "without importing unrelated source-file or formatting drift."
    ),
    "upstream-owned-no-sb-action": (
        "The changed path is upstream-owned, has no SB collision, and needs no SB code port."
    ),
    "upstream-owned-runtime-pending": (
        "No SB code port is required, but the affected engine or UI behavior remains "
        "Engine pending in the OB1 runtime matrix."
    ),
}

SUBSYSTEM_DEFINITIONS = {
    "ai-and-economy": "AI strategy, state value, construction, hiring, or wage behavior.",
    "audio": "Sound GUID inventory.",
    "core-script": "Shared script definitions that do not fit a narrower reviewed group.",
    "diplomacy-and-subjects": "Diplomacy, power blocs, acceptance, or subject relations.",
    "events-and-content": "Events, history, scripted effects, or content modifiers.",
    "interface-and-graphics": "GUI, shaders, icons, and other presentation assets.",
    "localization": "Localized user-facing text.",
    "map-and-pathfinding": "Adjacency, line, or spline pathfinding data.",
    "naval-and-military": "Naval, ship, invasion, repair, or military behavior.",
    "politics-and-society": "Interest groups, ideology, law, journal, or society content.",
    "scripted-tests": "Paradox-authored scripted test data.",
    "war-support-and-war-goals": "War support, war-goal, and enforcement contracts.",
}


@dataclass(frozen=True)
class FileRecord:
    path: str
    size: int
    sha1: str
    flags: int

    @property
    def kind(self) -> str:
        if self.flags & DIRECTORY_FLAG:
            return "directory"
        if self.flags & SYMLINK_FLAG:
            return "symlink"
        return "file"

    def evidence(self) -> dict:
        return {"kind": self.kind, "sha1": self.sha1, "size": self.size}


@dataclass(frozen=True)
class DecodedManifest:
    identity: ManifestIdentity
    records: Mapping[str, FileRecord]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_varint(data: bytes, offset: int) -> Tuple[int, int]:
    value = 0
    shift = 0
    while True:
        if offset >= len(data):
            raise ValueError("truncated protobuf varint")
        byte = data[offset]
        offset += 1
        value |= (byte & 0x7F) << shift
        if byte < 0x80:
            return value, offset
        shift += 7
        if shift >= 70:
            raise ValueError("protobuf varint is too long")


def _protobuf_fields(data: bytes) -> List[Tuple[int, int, object]]:
    """Decode the protobuf wire types used by Steam manifests."""
    fields: List[Tuple[int, int, object]] = []
    offset = 0
    while offset < len(data):
        tag, offset = _read_varint(data, offset)
        number = tag >> 3
        wire_type = tag & 0x07
        if number == 0:
            raise ValueError("protobuf field number 0 is invalid")
        if wire_type == 0:
            value, offset = _read_varint(data, offset)
        elif wire_type == 1:
            end = offset + 8
            if end > len(data):
                raise ValueError("truncated protobuf fixed64 field")
            value = data[offset:end]
            offset = end
        elif wire_type == 2:
            length, offset = _read_varint(data, offset)
            end = offset + length
            if end > len(data):
                raise ValueError("truncated protobuf length-delimited field")
            value = data[offset:end]
            offset = end
        elif wire_type == 5:
            end = offset + 4
            if end > len(data):
                raise ValueError("truncated protobuf fixed32 field")
            value = data[offset:end]
            offset = end
        else:
            raise ValueError("unsupported protobuf wire type {}".format(wire_type))
        fields.append((number, wire_type, value))
    return fields


def _single_field(
    fields: Iterable[Tuple[int, int, object]],
    number: int,
    wire_type: int,
    label: str,
) -> object:
    values = [value for field, wire, value in fields if field == number and wire == wire_type]
    if len(values) != 1:
        raise ValueError("{} must contain exactly one field {}".format(label, number))
    return values[0]


def _decode_file_record(message: bytes) -> FileRecord:
    fields = _protobuf_fields(message)
    raw_path = _single_field(fields, 1, 2, "file mapping")
    size = _single_field(fields, 2, 0, "file mapping")
    flags = _single_field(fields, 3, 0, "file mapping")
    raw_sha1 = _single_field(fields, 5, 2, "file mapping")
    assert isinstance(raw_path, bytes)
    assert isinstance(size, int)
    assert isinstance(flags, int)
    assert isinstance(raw_sha1, bytes)
    try:
        path = raw_path.decode("utf-8").replace("\\", "/")
    except UnicodeDecodeError as exc:
        raise ValueError("manifest path is not UTF-8: {}".format(exc))
    pure_path = PurePosixPath(path)
    if not path or path.startswith("/") or ".." in pure_path.parts or path != pure_path.as_posix():
        raise ValueError("non-canonical manifest path: {!r}".format(path))
    if len(raw_sha1) != 20:
        raise ValueError("{} has a non-SHA-1 content digest".format(path))
    record = FileRecord(path=path, size=size, sha1=raw_sha1.hex(), flags=flags)
    if record.kind == "directory" and (record.size != 0 or record.sha1 != ZERO_SHA1):
        raise ValueError("{} has invalid directory evidence".format(path))
    return record


def _read_section(data: bytes, offset: int, expected_magic: int) -> Tuple[bytes, int]:
    if offset + 8 > len(data):
        raise ValueError("truncated Steam manifest section header")
    magic, length = struct.unpack_from("<II", data, offset)
    if magic != expected_magic:
        raise ValueError(
            "unexpected Steam manifest section magic 0x{:08x}; expected 0x{:08x}".format(
                magic, expected_magic
            )
        )
    start = offset + 8
    end = start + length
    if end > len(data):
        raise ValueError("truncated Steam manifest section payload")
    return data[start:end], end


def _manifest_created_utc(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def decode_manifest(path: Path, expected: ManifestIdentity) -> DecodedManifest:
    path = Path(path).expanduser()
    data = path.read_bytes()
    actual_sha256 = sha256_bytes(data)
    if len(data) != expected.source_size:
        raise ValueError(
            "{} has {} bytes; expected {}".format(path, len(data), expected.source_size)
        )
    if actual_sha256 != expected.source_sha256:
        raise ValueError(
            "{} SHA-256 is {}; expected {}".format(
                path, actual_sha256, expected.source_sha256
            )
        )

    payload, offset = _read_section(data, 0, PAYLOAD_MAGIC)
    metadata, offset = _read_section(data, offset, METADATA_MAGIC)
    signature, offset = _read_section(data, offset, SIGNATURE_MAGIC)
    if signature:
        raise ValueError("the pinned Steam manifests unexpectedly contain a signature payload")
    if offset + 4 != len(data):
        raise ValueError("Steam manifest has trailing or missing envelope bytes")
    (end_magic,) = struct.unpack_from("<I", data, offset)
    if end_magic != END_MAGIC:
        raise ValueError("Steam manifest end marker is invalid")

    metadata_fields = _protobuf_fields(metadata)
    depot_id = _single_field(metadata_fields, 1, 0, "manifest metadata")
    manifest_id = _single_field(metadata_fields, 2, 0, "manifest metadata")
    created_timestamp = _single_field(metadata_fields, 3, 0, "manifest metadata")
    assert isinstance(depot_id, int)
    assert isinstance(manifest_id, int)
    assert isinstance(created_timestamp, int)
    actual_created_utc = _manifest_created_utc(created_timestamp)
    if depot_id != expected.depot_id:
        raise ValueError("manifest depot ID {} != {}".format(depot_id, expected.depot_id))
    if manifest_id != expected.manifest_id:
        raise ValueError("manifest ID {} != {}".format(manifest_id, expected.manifest_id))
    if actual_created_utc != expected.created_utc:
        raise ValueError(
            "manifest creation time {} != {}".format(actual_created_utc, expected.created_utc)
        )

    records: Dict[str, FileRecord] = {}
    for number, wire_type, value in _protobuf_fields(payload):
        if number != 1 or wire_type != 2 or not isinstance(value, bytes):
            raise ValueError("unexpected field in Steam manifest payload")
        record = _decode_file_record(value)
        if record.path in records:
            raise ValueError("duplicate manifest path: {}".format(record.path))
        records[record.path] = record
    if len(records) != expected.entry_count:
        raise ValueError(
            "{} contains {} paths; expected {}".format(path, len(records), expected.entry_count)
        )
    return DecodedManifest(identity=expected, records=records)


def subsystem_for(path: str) -> str:
    rel = path[5:] if path.startswith("game/") else path

    if (
        rel.startswith("common/war_goal_types/")
        or rel.startswith("common/script_values/war_")
        or rel == "common/on_actions/00_code_on_actions.txt"
        or rel == "common/effect_localization/00_diplomatic_play_effects_loc.txt"
        or rel in {
            "gfx/FX/gui_war_arrow.shader",
            "gui/add_wargoal_panel.gui",
            "gui/war_panel.gui",
        }
    ):
        return "war-support-and-war-goals"
    if (
        rel.startswith("common/ai_strategies/")
        or rel == "common/defines/00_ai.txt"
        or rel == "common/scripted_triggers/00_ai_triggers.txt"
        or "employment_" in rel
        or "state_value" in rel
        or rel.endswith("ai_strategies_l_english.yml")
    ):
        return "ai-and-economy"
    if (
        rel.startswith("common/travel_network")
        or rel == "common/messages/06_naval_messages.txt"
        or rel == "common/treaty_articles/31_ship_transfer.txt"
        or rel == "common/technology/technologies/20_military.txt"
        or any(token in rel for token in ("naval", "ship_panel", "invasion_planner", "repairing"))
    ):
        return "naval-and-military"
    if rel in {
        "gfx/lines/lines.lines",
        "gfx/map/spline_network/spline_network.splnet",
        "map_data/adjacencies.csv",
    }:
        return "map-and-pathfinding"
    if (
        rel.startswith("common/acceptance_statuses/")
        or rel.startswith("common/diplomatic_catalysts/")
        or rel.startswith("common/political_lobbies/")
        or rel.startswith("common/power_bloc_principles/")
        or rel.startswith("common/subject_types/")
        or rel == "common/ai_strategies/02_diplomatic_strategies.txt"
    ):
        return "diplomacy-and-subjects"
    if (
        rel.startswith("common/ideologies/")
        or rel.startswith("common/interest_groups/")
        or rel.startswith("common/journal_entries/")
        or rel.startswith("common/laws/")
        or rel == "common/history/global/00_global.txt"
        or rel == "common/technology/technologies/30_society.txt"
    ):
        return "politics-and-society"
    if (
        rel.startswith("events/")
        or rel.startswith("common/history/")
        or rel.startswith("common/scripted_effects/")
        or rel.startswith("common/scripted_rules/")
        or rel.startswith("common/static_modifiers/")
    ):
        return "events-and-content"
    if rel.startswith("localization/"):
        return "localization"
    if rel.startswith("gfx/") or rel.startswith("gui/"):
        return "interface-and-graphics"
    if rel.startswith("sound/"):
        return "audio"
    if rel.startswith("tools/scripted_tests/"):
        return "scripted-tests"
    return "core-script"


def disposition_for(path: str, change: str) -> str:
    if path in MERGE_REQUIRED:
        return "merge-required"
    if path in MERGE_REQUIRED_RUNTIME_PENDING:
        return "merge-required-runtime-pending"
    if path in REPIN_REVIEWED:
        return "repin-reviewed-sb-surface"
    if path == "game/common/script_values/war_exhaustion_values.txt":
        return "removed-unused-by-sb"
    if (
        path.startswith("game/common/war_goal_types/")
        or path == "game/common/script_values/war_support_values.txt"
        or path == "game/common/on_actions/00_code_on_actions.txt"
    ):
        return "adapt-sb-contract-runtime-pending"
    subsystem = subsystem_for(path)
    if (
        subsystem in {"ai-and-economy", "map-and-pathfinding", "naval-and-military"}
        or path == "game/common/history/global/00_global.txt"
        or path.startswith("game/gui/")
    ):
        return "upstream-owned-runtime-pending"
    return "upstream-owned-no-sb-action"


def _empty_evidence() -> dict:
    return {"kind": None, "sha1": None, "size": None}


def _manifest_summary(identity: ManifestIdentity) -> dict:
    return {
        "created_utc": identity.created_utc,
        "depot_entry_count": identity.entry_count,
        "game_version": identity.game_version,
        "manifest_id": str(identity.manifest_id),
        "source_file": identity.source_name,
        "source_sha256": identity.source_sha256,
        "source_size": identity.source_size,
        "steam_build": identity.steam_build,
    }


def build_delta(old_path: Path, new_path: Path) -> dict:
    old_manifest = decode_manifest(old_path, OLD_IDENTITY)
    new_manifest = decode_manifest(new_path, NEW_IDENTITY)
    old_paths = set(old_manifest.records)
    new_paths = set(new_manifest.records)
    added = new_paths - old_paths
    removed = old_paths - new_paths
    changed = {
        path
        for path in old_paths & new_paths
        if (
            old_manifest.records[path].size,
            old_manifest.records[path].sha1,
            old_manifest.records[path].flags,
        )
        != (
            new_manifest.records[path].size,
            new_manifest.records[path].sha1,
            new_manifest.records[path].flags,
        )
    }

    counts = {
        "added": len(added),
        "changed": len(changed),
        "removed": len(removed),
        "total": len(added) + len(changed) + len(removed),
    }
    if counts != EXPECTED_COUNTS:
        raise ValueError("depot delta counts {} != {}".format(counts, EXPECTED_COUNTS))

    all_paths = sorted(added | removed | changed)
    if not SB_COLLISION_PATHS <= set(all_paths):
        missing = sorted(SB_COLLISION_PATHS - set(all_paths))
        raise ValueError("reviewed SB collision paths are absent from delta: {}".format(missing))

    entries = []
    for path in all_paths:
        if path in added:
            change = "added"
        elif path in removed:
            change = "removed"
        else:
            change = "changed"
        old_record = old_manifest.records.get(path)
        new_record = new_manifest.records.get(path)
        entries.append(
            {
                "change": change,
                "disposition": disposition_for(path, change),
                "new": new_record.evidence() if new_record else _empty_evidence(),
                "old": old_record.evidence() if old_record else _empty_evidence(),
                "path": path,
                "sb_collision": path in SB_COLLISION_PATHS,
                "subsystem": subsystem_for(path),
            }
        )

    return {
        "classification": {
            "collision_basis": (
                "True only when this changed depot path intersects SB's pre-rebase "
                "exact-path shadow or an upstream source for a keyed override."
            ),
            "dispositions": DISPOSITION_DEFINITIONS,
            "subsystems": SUBSYSTEM_DEFINITIONS,
        },
        "counts": counts,
        "depot_id": str(OLD_IDENTITY.depot_id),
        "entries": entries,
        "generated_by": "tools/build_steam_depot_delta.py",
        "new_manifest": _manifest_summary(NEW_IDENTITY),
        "old_manifest": _manifest_summary(OLD_IDENTITY),
        "schema_version": 1,
        "target_branch": TARGET_BRANCH,
    }


def normalized_json(delta: Mapping[str, object]) -> str:
    return json.dumps(delta, indent=2, sort_keys=True) + "\n"


def verify_current_payload(delta: Mapping[str, object], game_root: Path) -> None:
    game_root = Path(game_root).expanduser()
    errors = []
    entries = delta.get("entries")
    if not isinstance(entries, list):
        raise ValueError("delta entries are not a list")
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("delta entry is not an object")
        new = entry.get("new")
        path = entry.get("path")
        if not isinstance(new, dict) or not isinstance(path, str) or new.get("size") is None:
            continue
        if not path.startswith("game/"):
            errors.append("{} is not rooted at game/".format(path))
            continue
        disk_path = game_root / path[len("game/") :]
        kind = new.get("kind")
        if kind == "directory":
            if not disk_path.is_dir():
                errors.append("{} is not an installed directory".format(path))
        elif kind == "file":
            if not disk_path.is_file():
                errors.append("{} is not an installed file".format(path))
            else:
                actual_size = disk_path.stat().st_size
                actual_sha1 = hashlib.sha1(disk_path.read_bytes()).hexdigest()
                if actual_size != new.get("size") or actual_sha1 != new.get("sha1"):
                    errors.append(
                        "{} installed evidence is {}/{}; expected {}/{}".format(
                            path,
                            actual_size,
                            actual_sha1,
                            new.get("size"),
                            new.get("sha1"),
                        )
                    )
        elif kind == "symlink":
            if not disk_path.is_symlink():
                errors.append("{} is not an installed symlink".format(path))
        else:
            errors.append("{} has unsupported installed kind {!r}".format(path, kind))
    if errors:
        raise ValueError("installed OB1 payload does not match:\n- " + "\n- ".join(errors))


def default_manifest_path(identity: ManifestIdentity) -> Path:
    return Path.home() / "Library/Application Support/Steam/depotcache" / identity.source_name


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the pinned Victoria 3 1.13.11 to 1.14.0 OB1 core-depot delta."
    )
    parser.add_argument(
        "--old-manifest",
        type=Path,
        default=default_manifest_path(OLD_IDENTITY),
        help="Exact retained 1.13.11 core manifest (hash is enforced).",
    )
    parser.add_argument(
        "--new-manifest",
        type=Path,
        default=default_manifest_path(NEW_IDENTITY),
        help="Exact retained 1.14.0 OB1 core manifest (hash is enforced).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("Docs/compatibility/1_13_11_to_1_14_0_ob1_depot_delta.json"),
        help="Normalized JSON output path.",
    )
    parser.add_argument(
        "--game-root",
        type=Path,
        help="Optionally verify every present new-side path against this installed game root.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        delta = build_delta(args.old_manifest, args.new_manifest)
        if args.game_root is not None:
            verify_current_payload(delta, args.game_root)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(normalized_json(delta), encoding="utf-8")
    except (OSError, ValueError) as exc:
        print("depot-delta generation failed: {}".format(exc), file=sys.stderr)
        return 1
    print(
        "wrote {} ({} changed, {} added, {} removed)".format(
            args.output,
            delta["counts"]["changed"],
            delta["counts"]["added"],
            delta["counts"]["removed"],
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
