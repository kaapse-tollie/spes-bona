"""Reproduce and verify the public 1.15.1 to 1.15.2 core-depot delta."""
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from . import build_steam_depot_delta as depot
    from .check_1_15_1_target import NEW as OLD
except ImportError:
    import build_steam_depot_delta as depot
    from check_1_15_1_target import NEW as OLD

NEW = depot.ManifestIdentity(
    label="Victoria 3 1.15.2", game_version="1.15.2", steam_build="26763837",
    depot_id=529341, manifest_id=5942745929618312121,
    created_utc="2026-11-18T17:03:49Z",
    source_name="529341_5942745929618312121.manifest", source_size=4910249,
    source_sha256="80b9772dd115b5d964581143adf47cd3d748429d9f77b1a24cbbdabb741f0d63",
    entry_count=27677,
)
OUTPUT = Path(__file__).resolve().parents[1] / "Docs/compatibility/evidence/1_15_2_implementation/current_target.json"
REPORT_SHA256 = "c946e683cc563aa5fe06b0ea893cfa043d474a29543aae6041ec5bd1e275fa24"


def build_delta(old_path=None, new_path=None):
    old = depot.decode_manifest(old_path or depot.default_manifest_path(OLD), OLD).records
    new = depot.decode_manifest(new_path or depot.default_manifest_path(NEW), NEW).records
    entries = []
    for path in sorted(old.keys() | new.keys()):
        before = old[path].evidence() if path in old else None
        after = new[path].evidence() if path in new else None
        if before != after:
            change = "added" if before is None else "removed" if after is None else "changed"
            entries.append({"path": path, "change": change, "old": before, "new": after})
    return {
        "depot_id": NEW.depot_id, "branch": "public", "old_manifest": depot._manifest_summary(OLD),
        "new_manifest": depot._manifest_summary(NEW), "counts": dict(Counter(e["change"] for e in entries)),
        "entries": entries,
    }


def verify_current_target(game_root, *, report_path=OUTPUT, manifest_path=None):
    current = depot.decode_manifest(manifest_path or depot.default_manifest_path(NEW), NEW)
    raw = Path(report_path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != REPORT_SHA256:
        raise ValueError("reviewed 1.15.2 depot report SHA-256 mismatch")
    data = json.loads(raw)
    for entry in data["entries"]:
        record = current.records.get(entry["path"])
        if record is None or record.evidence() != entry["new"]:
            raise ValueError(f"current manifest evidence mismatch: {entry['path']}")
    depot.verify_current_payload(data, game_root)
