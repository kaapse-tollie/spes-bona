#!/usr/bin/env python3
"""Decode and three-way merge Victoria 3 spline_network.splnet (format version 4).

This script is deliberately strict and target-specific. It recognizes the exact tokenized
record layout used by Victoria 3 1.13.11, 1.14 Open Beta 1, and Spes Bona. It performs an
object/record three-way merge in memory, never edits an input, and writes only paths passed
explicitly with --output / --report-json.

Merge base    : vanilla 1.13.11 build 24799966
Variant delta : current Spes Bona relative to that base
Target        : vanilla 1.14 OB1 build 25081502

The script also performs the reverse operation (upstream delta onto SB) and requires both
directions to produce byte-identical output. That is a strong check that the deltas are
disjoint and their ordering is unambiguous for these inputs.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import struct
from typing import Iterable

# Jomini binary token IDs used by this file.
EQUAL = 0x0001
OPEN = 0x0003
CLOSE = 0x0004
I32 = 0x000C
F32 = 0x000D
U32 = 0x0014
U64 = 0x029C

# Semantic field IDs used by spline_network.splnet v4.
FIELD_VERSION = 238
FIELD_COUNTS = 1114
SECTION_POINTS = 1524
SECTION_STRIPS = 1525
SECTION_LINKS = 1526
FIELD_ID = 11
FIELD_POSITION = 76
FIELD_POINT_LIST = 1527
FIELD_STRIP_LIST = 1525

KNOWN_SHA256 = {
    "old": "91c0957b4898ca4db6b66584d0ab1db1a6039825e9fd635b7a5c1e69068cf2b1",
    "new": "ac58f5fb4cd408cf8dba8ad41c5f3a322a12c5372f055694eb85f528e650c28c",
    "sb": "74cebc60ca7155f598f03924b725de0b3f0e060ca37af8dc356a4b120cb36274",
    "merged": "9fd9d83f0b651284d5ef22066d19239fd9e1127d25c14c0763eca3bbade5ef8c",
}
KNOWN_SIZE = {"old": 1646344, "new": 1646224, "sb": 1650254, "merged": 1650134}
KNOWN_PRE_REINDEX_MERGED_SHA256 = "e9fdab54f3267538ae35f7990818166ae9581af9eac535f4e8bf4753356a5673"
KNOWN_COUNTS = {
    "old": (33780, 4273, 4271),
    "new": (33777, 4273, 4271),
    "sb": (33860, 4283, 4281),
    "merged": (33857, 4283, 4281),
}


class FormatError(ValueError):
    pass


class MergeConflict(ValueError):
    pass


@dataclass(frozen=True)
class Record:
    key: int
    raw: bytes
    payload: tuple[int | float, ...]


@dataclass(frozen=True)
class Model:
    version: int
    counts: tuple[int, int, int]
    points: tuple[Record, ...]
    strips: tuple[Record, ...]
    links: tuple[Record, ...]


class Cursor:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def _need(self, size: int) -> None:
        if self.pos + size > len(self.data):
            raise FormatError(f"unexpected EOF at 0x{self.pos:x}; need {size} bytes")

    def u16(self, expected: int | None = None) -> int:
        self._need(2)
        start = self.pos
        value = struct.unpack_from("<H", self.data, self.pos)[0]
        self.pos += 2
        if expected is not None and value != expected:
            raise FormatError(
                f"token mismatch at 0x{start:x}: expected 0x{expected:04x}, got 0x{value:04x}"
            )
        return value

    def peek_u16(self) -> int:
        self._need(2)
        return struct.unpack_from("<H", self.data, self.pos)[0]

    def i32_token(self) -> int:
        self.u16(I32)
        self._need(4)
        value = struct.unpack_from("<i", self.data, self.pos)[0]
        self.pos += 4
        return value

    def u32_token(self) -> int:
        self.u16(U32)
        self._need(4)
        value = struct.unpack_from("<I", self.data, self.pos)[0]
        self.pos += 4
        return value

    def u64_token(self) -> int:
        self.u16(U64)
        self._need(8)
        value = struct.unpack_from("<Q", self.data, self.pos)[0]
        self.pos += 8
        return value

    def f32_token(self) -> float:
        self.u16(F32)
        self._need(4)
        value = struct.unpack_from("<f", self.data, self.pos)[0]
        self.pos += 4
        return value


def read_section(cursor: Cursor, section_id: int, kind: str) -> tuple[Record, ...]:
    """Read one top-level collection and retain each record's exact raw bytes.

    points record:
      { FIELD_ID = U32(id) FIELD_POSITION = { F32(x) F32(y) } }
    strips record:
      { FIELD_ID = U64(id) FIELD_POINT_LIST = { U32(point_id)... } }
    links record:
      { FIELD_ID = U64(id) FIELD_STRIP_LIST = { U64(strip_id)... } }
    """
    cursor.u16(section_id)
    cursor.u16(EQUAL)
    cursor.u16(OPEN)
    records: list[Record] = []

    while cursor.peek_u16() != CLOSE:
        start = cursor.pos
        cursor.u16(OPEN)
        cursor.u16(FIELD_ID)
        cursor.u16(EQUAL)

        if kind == "point":
            key = cursor.u32_token()
            cursor.u16(FIELD_POSITION)
            cursor.u16(EQUAL)
            cursor.u16(OPEN)
            payload: tuple[int | float, ...] = (
                cursor.f32_token(),
                cursor.f32_token(),
            )
            cursor.u16(CLOSE)
        elif kind == "strip":
            key = cursor.u64_token()
            cursor.u16(FIELD_POINT_LIST)
            cursor.u16(EQUAL)
            cursor.u16(OPEN)
            values: list[int] = []
            while cursor.peek_u16() != CLOSE:
                values.append(cursor.u32_token())
            cursor.u16(CLOSE)
            payload = tuple(values)
        elif kind == "link":
            key = cursor.u64_token()
            cursor.u16(FIELD_STRIP_LIST)
            cursor.u16(EQUAL)
            cursor.u16(OPEN)
            values = []
            while cursor.peek_u16() != CLOSE:
                values.append(cursor.u64_token())
            cursor.u16(CLOSE)
            payload = tuple(values)
        else:
            raise AssertionError(kind)

        cursor.u16(CLOSE)
        records.append(Record(key, cursor.data[start : cursor.pos], payload))

    cursor.u16(CLOSE)
    keys = [record.key for record in records]
    if len(keys) != len(set(keys)):
        raise FormatError(f"duplicate primary key in section {section_id}")
    return tuple(records)


def parse(data: bytes) -> Model:
    cursor = Cursor(data)
    cursor.u16(FIELD_VERSION)
    cursor.u16(EQUAL)
    version = cursor.i32_token()
    if version != 4:
        raise FormatError(f"only spline format version 4 is supported; got {version}")

    cursor.u16(FIELD_COUNTS)
    cursor.u16(EQUAL)
    cursor.u16(OPEN)
    counts = tuple(cursor.i32_token() for _ in range(3))
    cursor.u16(CLOSE)

    points = read_section(cursor, SECTION_POINTS, "point")
    strips = read_section(cursor, SECTION_STRIPS, "strip")
    links = read_section(cursor, SECTION_LINKS, "link")
    if cursor.pos != len(data):
        raise FormatError(f"unparsed trailing data at 0x{cursor.pos:x}")

    actual = (len(points), len(strips), len(links))
    if counts != actual:
        raise FormatError(f"header counts {counts} do not match decoded collections {actual}")
    model = Model(version, counts, points, strips, links)
    if serialize(model) != data:
        raise FormatError("lossless parse/serialize round trip failed")
    validate_references(model)
    return model


def serialize(model: Model) -> bytes:
    """Serialize exact record bytes, rebuilding only wrappers and header counts."""
    output = bytearray()
    output += struct.pack("<HHHi", FIELD_VERSION, EQUAL, I32, model.version)
    output += struct.pack("<HHH", FIELD_COUNTS, EQUAL, OPEN)
    for count in (len(model.points), len(model.strips), len(model.links)):
        output += struct.pack("<Hi", I32, count)
    output += struct.pack("<H", CLOSE)

    for section_id, records in (
        (SECTION_POINTS, model.points),
        (SECTION_STRIPS, model.strips),
        (SECTION_LINKS, model.links),
    ):
        output += struct.pack("<HHH", section_id, EQUAL, OPEN)
        for record in records:
            output += record.raw
        output += struct.pack("<H", CLOSE)
    return bytes(output)


def validate_references(model: Model) -> None:
    point_ids = {record.key for record in model.points}
    strip_ids = {record.key for record in model.strips}
    missing_points = sorted(
        {int(value) for record in model.strips for value in record.payload if value not in point_ids}
    )
    missing_strips = sorted(
        {int(value) for record in model.links for value in record.payload if value not in strip_ids}
    )
    if missing_points:
        raise FormatError(f"strip references missing points: {missing_points[:20]}")
    if missing_strips:
        raise FormatError(f"link references missing strips: {missing_strips[:20]}")


def record_map(records: Iterable[Record]) -> dict[int, Record]:
    return {record.key: record for record in records}


def delta(base: tuple[Record, ...], variant: tuple[Record, ...]) -> dict[str, list[int]]:
    base_map = record_map(base)
    variant_map = record_map(variant)
    return {
        "removed": sorted(base_map.keys() - variant_map.keys()),
        "added": sorted(variant_map.keys() - base_map.keys()),
        "modified": sorted(
            key
            for key in base_map.keys() & variant_map.keys()
            if base_map[key].raw != variant_map[key].raw
        ),
    }


def apply_delta(
    base: tuple[Record, ...],
    variant: tuple[Record, ...],
    target: tuple[Record, ...],
    label: str,
) -> tuple[Record, ...]:
    """Apply base->variant records to target, retaining target-only changes.

    Content merge is by the FIELD_ID primary key and exact raw record bytes. Insertions retain
    variant order by locating each added record between its nearest surviving variant neighbors.
    Concurrent edits to one key fail closed. No last-writer policy is silently assumed.
    """
    base_map = record_map(base)
    variant_map = record_map(variant)
    target_map = record_map(target)

    removed = base_map.keys() - variant_map.keys()
    added = variant_map.keys() - base_map.keys()
    modified = {
        key
        for key in base_map.keys() & variant_map.keys()
        if base_map[key].raw != variant_map[key].raw
    }
    conflicts: list[tuple[int, str]] = []

    for key in removed:
        if key in target_map and target_map[key].raw != base_map[key].raw:
            conflicts.append((key, "variant deletes a record modified by target"))
    for key in modified:
        if key not in target_map:
            conflicts.append((key, "variant modifies a record deleted by target"))
        elif target_map[key].raw not in (base_map[key].raw, variant_map[key].raw):
            conflicts.append((key, "variant and target modify the record differently"))
    for key in added:
        if key in target_map and target_map[key].raw != variant_map[key].raw:
            conflicts.append((key, "variant and target add different records at the same key"))
    if conflicts:
        raise MergeConflict(f"{label}: {conflicts}")

    result: list[Record] = []
    for record in target:
        if record.key in removed:
            continue
        result.append(variant_map[record.key] if record.key in modified else record)

    # Insert variant-only records in variant sequence order. This is required because SB keeps
    # reindexed point records at their old semantic position rather than globally sorting them.
    for variant_index, record in enumerate(variant):
        if record.key not in added or any(item.key == record.key for item in result):
            continue
        positions = {item.key: index for index, item in enumerate(result)}
        left = next(
            (variant[index].key for index in range(variant_index - 1, -1, -1)
             if variant[index].key in positions),
            None,
        )
        right = next(
            (variant[index].key for index in range(variant_index + 1, len(variant))
             if variant[index].key in positions),
            None,
        )
        if left is not None and right is not None and positions[left] >= positions[right]:
            raise MergeConflict(
                f"{label}: ordering anchors cross for added key {record.key}: {left}, {right}"
            )
        if right is not None:
            insertion_index = positions[right]
        elif left is not None:
            insertion_index = positions[left] + 1
        else:
            insertion_index = len(result)
        result.insert(insertion_index, record)

    keys = [record.key for record in result]
    if len(keys) != len(set(keys)):
        raise MergeConflict(f"{label}: duplicate key after merge")
    return tuple(result)


def merge(base: Model, variant: Model, target: Model, label: str) -> Model:
    if not (base.version == variant.version == target.version == 4):
        raise MergeConflict("input format versions differ")
    result = Model(
        version=target.version,
        counts=(0, 0, 0),
        points=apply_delta(base.points, variant.points, target.points, label + "/points"),
        strips=apply_delta(base.strips, variant.strips, target.strips, label + "/strips"),
        links=apply_delta(base.links, variant.links, target.links, label + "/links"),
    )
    result = Model(
        result.version,
        (len(result.points), len(result.strips), len(result.links)),
        result.points,
        result.strips,
        result.links,
    )
    validate_references(result)
    return result


def u32_occurrence_payload_offsets(data: bytes, value: int) -> list[int]:
    marker = struct.pack("<HI", U32, value)
    result: list[int] = []
    start = 0
    while True:
        found = data.find(marker, start)
        if found < 0:
            return result
        result.append(found + 2)  # payload offset, matching the existing SB regression constants
        start = found + 1


def section_lookup(model: Model, name: str) -> dict[int, Record]:
    return record_map(getattr(model, name))


def validate_known_inputs(blobs: dict[str, bytes], models: dict[str, Model]) -> None:
    for label in ("old", "new", "sb"):
        digest = hashlib.sha256(blobs[label]).hexdigest()
        if digest != KNOWN_SHA256[label]:
            raise ValueError(f"{label} SHA-256 mismatch: expected {KNOWN_SHA256[label]}, got {digest}")
        if len(blobs[label]) != KNOWN_SIZE[label]:
            raise ValueError(f"{label} size mismatch")
        if models[label].counts != KNOWN_COUNTS[label]:
            raise ValueError(f"{label} count mismatch")


def validate_known_merge(model: Model, data: bytes) -> None:
    if model.counts != KNOWN_COUNTS["merged"]:
        raise ValueError(f"merged counts mismatch: {model.counts}")
    if len(data) != KNOWN_SIZE["merged"]:
        raise ValueError(f"merged size mismatch: {len(data)}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != KNOWN_SHA256["merged"]:
        raise ValueError(f"merged SHA-256 mismatch: {digest}")

    points = section_lookup(model, "points")
    strips = section_lookup(model, "strips")
    expected_points = {
        8388908: (4389.43798828125, 2924.208740234375),
        8391908: (4149.6474609375, 2788.444580078125),
        8392008: (4136.5185546875, 2764.40869140625),
        277150838: (4377.90234375, 2949.68798828125),
        121303: (4797.912109375, 804.8287963867188),
        121304: (4785.4609375, 816.4765625),
    }
    for key, expected in expected_points.items():
        if points.get(key) is None or points[key].payload != expected:
            raise ValueError(f"merged point {key} mismatch")
    for removed in (277145160, 277150307, 277150308, 277150309, 25703, 25704):
        if removed in points:
            raise ValueError(f"removed point {removed} remains")

    expected_strips = {
        1661955: (8388908, 277150838, 8690508),
        1658883: (8391908, 277150349, 277150350, 277150352, 8699108),
        1661187: (8392008, 277150355, 277150356, 277150357, 8691408),
    }
    for key, expected in expected_strips.items():
        if strips.get(key) is None or strips[key].payload != expected:
            raise ValueError(f"merged strip {key} mismatch")
    for removed in (299267, 443907, 448003):
        if removed in strips:
            raise ValueError(f"superseded strip {removed} remains")

    expected_offsets = {
        121303: [0x0097DE, 0x128DCA, 0x16760E],
        121304: [0x009800, 0x165DDC, 0x167620, 0x167E2C],
        25703: [],
        25704: [],
    }
    for value, expected in expected_offsets.items():
        actual = u32_occurrence_payload_offsets(data, value)
        if actual != expected:
            raise ValueError(f"merged U32 offsets for {value}: expected {expected}, got {actual}")
    pre_reindex = bytearray(data)
    for new_id, old_id in ((121303, 25703), (121304, 25704)):
        for offset in expected_offsets[new_id]:
            pre_reindex[offset : offset + 4] = struct.pack("<I", old_id)
    pre_reindex_digest = hashlib.sha256(pre_reindex).hexdigest()
    if pre_reindex_digest != KNOWN_PRE_REINDEX_MERGED_SHA256:
        raise ValueError(f"merged pre-reindex SHA-256 mismatch: {pre_reindex_digest}")
    if sum(a != b for a, b in zip(data, pre_reindex)) != 21:
        raise ValueError("Natal reindex must alter exactly 21 payload bytes")

    expected_natal = [
        (121303, 26003, 16),
        (121304, 25804, 12),
        (121303, 121304, 4),
        (25700, 121304, 9),
    ]
    actual_natal = sorted(
        (int(record.payload[0]), int(record.payload[-1]), len(record.payload))
        for record in model.strips
        if record.payload and (
            record.payload[0] in (121303, 121304)
            or record.payload[-1] in (121303, 121304)
        )
    )
    if actual_natal != sorted(expected_natal):
        raise ValueError(f"Natal connectivity mismatch: {actual_natal}")


def build_report(
    paths: dict[str, Path],
    blobs: dict[str, bytes],
    models: dict[str, Model],
    merged: Model,
    merged_data: bytes,
) -> dict:
    sections = ("points", "strips", "links")
    return {
        "inputs": {
            label: {
                "path": str(paths[label]),
                "bytes": len(blobs[label]),
                "sha256": hashlib.sha256(blobs[label]).hexdigest(),
                "counts": list(models[label].counts),
                "round_trip_exact": serialize(models[label]) == blobs[label],
            }
            for label in ("old", "new", "sb")
        },
        "upstream_delta_old_to_new": {
            section: delta(getattr(models["old"], section), getattr(models["new"], section))
            for section in sections
        },
        "sb_delta_old_to_sb": {
            section: delta(getattr(models["old"], section), getattr(models["sb"], section))
            for section in sections
        },
        "merge": {
            "algorithm": "record-keyed three-way; fail on same-key conflict; preserve variant insertion order",
            "conflicts": [],
            "reverse_direction_byte_identical": True,
            "bytes": len(merged_data),
            "sha256": hashlib.sha256(merged_data).hexdigest(),
            "counts": list(merged.counts),
            "references_valid": True,
        },
        "merged_ob1_checks": {
            "point_positions": {
                str(key): list(section_lookup(merged, "points")[key].payload)
                for key in (8388908, 8391908, 8392008, 277150838)
            },
            "strip_paths": {
                str(key): list(section_lookup(merged, "strips")[key].payload)
                for key in (1658883, 1661187, 1661955)
            },
            "removed_point_ids_absent": [277145160, 277150307, 277150308, 277150309],
            "superseded_strip_ids_absent": [299267, 443907, 448003],
        },
        "merged_sb_checks": {
            "natal_positions": {
                str(key): list(section_lookup(merged, "points")[key].payload)
                for key in (121303, 121304)
            },
            "old_natal_ids_absent": [25703, 25704],
            "u32_payload_occurrences": {
                str(key): [f"0x{offset:06X}" for offset in u32_occurrence_payload_offsets(merged_data, key)]
                for key in (121303, 121304, 25703, 25704)
            },
            "pre_natal_reindex_sha256": KNOWN_PRE_REINDEX_MERGED_SHA256,
            "reindex_changed_byte_count": 21,
            "natal_strips": [
                [record.key, int(record.payload[0]), int(record.payload[-1]), len(record.payload)]
                for record in merged.strips
                if record.payload and (
                    record.payload[0] in (121303, 121304)
                    or record.payload[-1] in (121303, 121304)
                )
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old", required=True, type=Path, help="exact vanilla 1.13.11 splnet")
    parser.add_argument("--new", required=True, type=Path, help="exact vanilla 1.14 OB1 splnet")
    parser.add_argument("--sb", required=True, type=Path, help="current Spes Bona splnet")
    parser.add_argument("--output", type=Path, help="optional merged binary output (never an input path)")
    parser.add_argument("--report-json", type=Path, help="optional JSON validation report")
    args = parser.parse_args()

    paths = {"old": args.old.resolve(), "new": args.new.resolve(), "sb": args.sb.resolve()}
    if args.output and args.output.resolve() in paths.values():
        raise ValueError("refusing to overwrite an input")
    blobs = {label: path.read_bytes() for label, path in paths.items()}
    models = {label: parse(data) for label, data in blobs.items()}
    validate_known_inputs(blobs, models)

    # Requested direction: transplant the old-vanilla -> SB delta onto 1.14.
    merged = merge(models["old"], models["sb"], models["new"], "SB onto 1.14")
    merged_data = serialize(merged)

    # Independent reverse-direction check: put old-vanilla -> 1.14 onto SB. Exact equality
    # proves the two record deltas are disjoint and ordering has no ambiguity for this triplet.
    reverse = merge(models["old"], models["new"], models["sb"], "1.14 onto SB")
    reverse_data = serialize(reverse)
    if merged_data != reverse_data:
        raise MergeConflict("merge directions are semantically compatible but byte order differs")
    validate_known_merge(merged, merged_data)

    report = build_report(paths, blobs, models, merged, merged_data)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(merged_data)
    if args.report_json:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
