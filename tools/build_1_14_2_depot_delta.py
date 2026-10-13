"""Reproduce the pinned opening-beta to 1.14.2 core-depot comparison."""

from pathlib import Path
import argparse
import json

try:
    from . import build_steam_depot_delta as depot
except ImportError:
    import build_steam_depot_delta as depot

OLD = depot.NEW_IDENTITY
NEW = depot.ManifestIdentity(
    label="Victoria 3 1.14.2 Open Beta Update 1 + Hotfix 1",
    game_version="1.14.2", steam_build="25207758", depot_id=529341,
    manifest_id=2887980275526736263, created_utc="2026-09-09T10:39:15Z",
    source_name="529341_2887980275526736263.manifest", source_size=4733886,
    source_sha256="6c684bd6b7b6abdc67e310feb39ceedfd1622d856ea0d1f1a3d3bcff105d86bf",
    entry_count=26654,
)
OUTPUT = Path(__file__).resolve().parents[1] / "Docs/compatibility/1_14_0_to_1_14_2_depot_delta.json"


def build_delta(old_path=None, new_path=None):
    old = depot.decode_manifest(old_path or depot.default_manifest_path(OLD), OLD).records
    new = depot.decode_manifest(new_path or depot.default_manifest_path(NEW), NEW).records
    entries = []
    for path in sorted(old.keys() | new.keys()):
        before, after = old.get(path), new.get(path)
        if before == after:
            continue
        change = "added" if before is None else "removed" if after is None else "changed"
        entries.append({"path": path, "change": change,
                        "old": before.evidence() if before else depot._empty_evidence(),
                        "new": after.evidence() if after else depot._empty_evidence()})
    counts = {kind: sum(e["change"] == kind for e in entries) for kind in ("added", "changed", "removed")}
    counts["total"] = len(entries)
    if counts != {"added": 1, "changed": 69, "removed": 0, "total": 70}:
        raise ValueError(f"unexpected 1.14.2 depot delta: {counts}")
    return {"schema_version": 1, "depot_id": "529341", "target_branch": "1.14-openbeta",
            "generated_by": "tools/build_1_14_2_depot_delta.py",
            "old_manifest": depot._manifest_summary(OLD), "new_manifest": depot._manifest_summary(NEW),
            "counts": counts, "entries": entries}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--game-root", type=Path)
    args = parser.parse_args()
    delta = build_delta()
    if args.game_root:
        depot.verify_current_payload(delta, args.game_root)
    args.output.write_text(depot.normalized_json(delta), encoding="utf-8")
    print(json.dumps(delta["counts"]))
