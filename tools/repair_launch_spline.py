#!/usr/bin/env python3
"""Repair the state-split identities exposed by the 2026-09-05 OB1 launch.

Input is the audited 0.20.0 three-way merge. Preserve that historical merge;
apply this separate, reproducible correction to the deployed spline.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from pathlib import Path
import struct

try:
    from . import spline_structured_merge as spline
except ImportError:
    import spline_structured_merge as spline

INPUT_SHA256 = "9fd9d83f0b651284d5ef22066d19239fd9e1127d25c14c0763eca3bbade5ef8c"
# Port and wood moved to Natal; old Cape farm is now Northern Cape's port,
# and old Northern Cape wood lies in the new Bechuanaland wood province.
REINDEX = {25703: 121303, 25704: 121304, 8414308: 8509908,
           26101: 26203, 26204: 122104}
ANCHOR_MASK = (1 << 29) - 1


def link_endpoints(key: int) -> tuple[int, int]:
    return key >> 35, (key >> 6) & ANCHOR_MASK


def link_key(a: int, b: int, style: int) -> int:
    return (max(a, b) << 35) | (min(a, b) << 6) | style


def point(key: int, x: float, y: float) -> spline.Record:
    raw = struct.pack('<HHHHIHHHHfHfHH', spline.OPEN, spline.FIELD_ID,
                      spline.EQUAL, spline.U32, key, spline.FIELD_POSITION,
                      spline.EQUAL, spline.OPEN, spline.F32, x, spline.F32, y,
                      spline.CLOSE, spline.CLOSE)
    return spline.Record(key, raw, (x, y))


def sequence(key: int, values: tuple[int, ...], kind: str) -> spline.Record:
    token, fmt, field = ((spline.U64, 'Q', spline.FIELD_STRIP_LIST) if kind == 'link'
                         else (spline.U32, 'I', spline.FIELD_POINT_LIST))
    raw = struct.pack('<HHHHQHHH', spline.OPEN, spline.FIELD_ID, spline.EQUAL,
                      spline.U64, key, field, spline.EQUAL, spline.OPEN)
    raw += b''.join(struct.pack('<H' + fmt, token, value) for value in values)
    raw += struct.pack('<HH', spline.CLOSE, spline.CLOSE)
    return spline.Record(key, raw, values)


def validate_link_endpoints(model: spline.Model) -> None:
    strips = spline.record_map(model.strips)
    for link in model.links:
        degrees = Counter(p for key in link.payload
                          for p in (strips[key].payload[0], strips[key].payload[-1]))
        ends = {p for p, degree in degrees.items() if degree % 2}
        if ends != set(link_endpoints(link.key)):
            raise ValueError(f'link {link.key} encodes {link_endpoints(link.key)}, '
                             f'but its strips end at {sorted(ends)}')


def repair(data: bytes) -> bytes:
    if hashlib.sha256(data).hexdigest() != INPUT_SHA256:
        raise ValueError('input must be the audited 0.20.0 OB1 merge')
    model = spline.parse(data)
    points = [point(REINDEX[r.key], *r.payload) if r.key in REINDEX else r
              for r in model.points]
    strips = [sequence(r.key, tuple(REINDEX.get(p, p) for p in r.payload), 'strip')
              if any(p in REINDEX for p in r.payload) else r for r in model.strips]
    links = []
    for r in model.links:
        a, b = link_endpoints(r.key)
        key = link_key(REINDEX.get(a, a), REINDEX.get(b, b), r.key & 63)
        links.append(sequence(key, r.payload, 'link') if key != r.key else r)

    # Restore the two land hubs whose old anchors now belong to different states.
    # Coordinates are the current authored map-object locators.
    points.extend([point(26101, 4535.0, 710.0), point(26204, 4624.0, 768.0)])
    # New coastal state ports have generated harbor nodes but no spline port.
    # Sample the nearest coastal-land pixels to OB1's harbor nodes; reuse offshore routes.
    points.extend([point(8414308, 4834.0, 850.0), point(8414808, 4482.0, 821.0)])
    # Namaqualand's authored port moved north; retain the offshore half of its route.
    points = [point(r.key, 4426.0, 975.0) if r.key in (25503, 8414108) else r
              for r in points]
    strips = [sequence(r.key, (8414108, *r.payload[4:]), 'strip')
              if r.key == 896771 else r for r in strips]
    routes = [
        (0, (26101, 26104)),
        (0, (26204, 26202)),
        (3, (8414308, 277145773, 277145770, 277150497, 277145764,
             277150496, 277145760, 8699208)),
        (3, (8414808, 277145802, 277145808, 277145809, 8699208)),
    ]
    next_id = (max(r.key for r in strips) >> 8) + 1
    for offset, (style, route) in enumerate(routes):
        key = ((next_id + offset) << 8) | style
        strips.append(sequence(key, route, 'strip'))
        links.append(sequence(link_key(route[0], route[-1], style), (key,), 'link'))
    result = spline.Model(model.version, (len(points), len(strips), len(links)),
                          tuple(points), tuple(strips), tuple(links))
    output = spline.serialize(result)
    checked = spline.parse(output)
    validate_link_endpoints(checked)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = repair(args.input.read_bytes())
    args.output.write_bytes(output)
    print(f'{len(output)} bytes; SHA-256 {hashlib.sha256(output).hexdigest()}')


if __name__ == '__main__':
    main()
