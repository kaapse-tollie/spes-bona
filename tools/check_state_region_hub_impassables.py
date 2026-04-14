#!/usr/bin/env python3
"""Fail if a Southern Africa state region marks a hub origin province as impassable."""

from __future__ import annotations

import re
from pathlib import Path


STATE_PATTERN = re.compile(r"^\s*(STATE_[A-Z0-9_]+)\s*=\s*\{")
HUB_PATTERN = re.compile(r'^\s*(city|port|farm|mine|wood)\s*=\s*"x([0-9A-Fa-f]{6})"')
PROVINCE_PATTERN = re.compile(r"x([0-9A-Fa-f]{6})")


def iter_conflicts(state_region_dir: Path):
    # This repo only rewrites Southern Africa map ownership. Scan that file directly
    # so vanilla pass-through files elsewhere do not create false positives.
    for path in [state_region_dir / "04_subsaharan_africa.txt"]:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        i = 0
        while i < len(lines):
            match = STATE_PATTERN.match(lines[i])
            if not match:
                i += 1
                continue

            state_name = match.group(1)
            depth = lines[i].count("{") - lines[i].count("}")
            impassable: set[str] = set()
            hubs: dict[str, str] = {}
            i += 1

            while i < len(lines) and depth > 0:
                line = lines[i]
                depth += line.count("{") - line.count("}")

                if "impassable" in line:
                    impassable.update(province.upper() for province in PROVINCE_PATTERN.findall(line))

                hub_match = HUB_PATTERN.match(line)
                if hub_match:
                    hubs[hub_match.group(1)] = hub_match.group(2).upper()

                i += 1

            bad_hubs = {hub_type: province for hub_type, province in hubs.items() if province in impassable}
            if bad_hubs:
                yield path, state_name, bad_hubs


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    state_region_dir = repo_root / "map_data" / "state_regions"

    conflicts = list(iter_conflicts(state_region_dir))
    if not conflicts:
        print("OK: no hub origin provinces are marked impassable in Southern Africa state regions.")
        return 0

    print("ERROR: hub origin provinces listed in impassable blocks:")
    for path, state_name, bad_hubs in conflicts:
        details = ", ".join(f"{hub_type}=x{province}" for hub_type, province in sorted(bad_hubs.items()))
        print(f"- {path.name} :: {state_name} :: {details}")
    print()
    print("Map-data edits should be validated from a cold restart. Do not rely on hot reload for state-region or terrain changes.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
