"""Reproduce the retained 1.14.4 to 1.14.5 Open Beta core-depot comparison."""

from pathlib import Path
import argparse
import json

try:
    from . import build_steam_depot_delta as depot
except ImportError:
    import build_steam_depot_delta as depot

OLD = depot.ManifestIdentity(
    label="Victoria 3 1.14.4 Open Beta Update 3",
    game_version="1.14.4", steam_build="25483263", depot_id=529341,
    manifest_id=2774789085913801937, created_utc="2026-09-21T19:06:15Z",
    source_name="529341_2774789085913801937.manifest", source_size=4735254,
    source_sha256="80d85b1973e27fd6be49905e0b6e3df772ec3c17d2eee94332d0831b38c30109",
    entry_count=26664,
)
NEW = depot.ManifestIdentity(
    label="Victoria 3 1.14.5 Open Beta Update 4",
    game_version="1.14.5", steam_build="25629520", depot_id=529341,
    manifest_id=5521822647051867164, created_utc="2026-09-29T08:14:14Z",
    source_name="529341_5521822647051867164.manifest", source_size=4735534,
    source_sha256="e1f023a750df92e051928005400d2e1c902b35a5c40a571965e2f032f0632072",
    entry_count=26666,
)
OUTPUT = Path(__file__).resolve().parents[1] / "Docs/compatibility/1_14_4_to_1_14_5_depot_delta.json"


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
    if counts != {"added": 2, "changed": 147, "removed": 0, "total": 149}:
        raise ValueError(f"unexpected 1.14.5 depot delta: {counts}")
    return {"schema_version": 1, "depot_id": "529341", "target_branch": "1.14-openbeta",
            "generated_by": "tools/build_1_14_5_depot_delta.py",
            "old_manifest": depot._manifest_summary(OLD), "new_manifest": depot._manifest_summary(NEW),
            "counts": counts, "entries": entries}


def verify_current_target(game_root, *, report_path=OUTPUT, manifest_path=None):
    """Require current evidence independently of the historical manifest's retention."""
    current = depot.decode_manifest(manifest_path or depot.default_manifest_path(NEW), NEW)
    data = json.loads(Path(report_path).read_text(encoding="utf-8"))
    if data.get("new_manifest") != depot._manifest_summary(NEW):
        raise ValueError("current depot report identity mismatch")
    if data.get("counts") != {"added": 2, "changed": 147, "removed": 0, "total": 149}:
        raise ValueError("current depot report counts mismatch")
    entries = data.get("entries", [])
    if len(entries) != 149 or len({e["path"] for e in entries}) != 149:
        raise ValueError("current depot report entries mismatch")
    for entry in entries:
        record = current.records.get(entry["path"])
        if record is None or entry["new"] != record.evidence():
            raise ValueError(f"current manifest evidence mismatch: {entry['path']}")
    depot.verify_current_payload(data, game_root)


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
