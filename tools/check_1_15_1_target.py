"""Verify the pinned 1.15.1 core manifest and every changed/added depot path."""
import json
from pathlib import Path

try:
    from . import build_steam_depot_delta as depot
except ImportError:
    import build_steam_depot_delta as depot

NEW = depot.ManifestIdentity(
    label="Victoria 3 1.15.1", game_version="1.15.1", steam_build="26591675",
    depot_id=529341, manifest_id=5537848810174326853,
    created_utc="2026-11-10T12:35:56Z",
    source_name="529341_5537848810174326853.manifest", source_size=4908334,
    source_sha256="a9af542820b6e56753ffcc95683d7b1c7fc78e8398d36d7132f154c09cfea459",
    entry_count=27664,
)
OUTPUT = Path(__file__).resolve().parents[1] / "Docs/compatibility/evidence/1_15_1_implementation/current_target.json"


def verify_current_target(game_root, *, report_path=OUTPUT, manifest_path=None):
    current = depot.decode_manifest(manifest_path or depot.default_manifest_path(NEW), NEW)
    data = json.loads(Path(report_path).read_text())
    if data.get("new_manifest") != depot._manifest_summary(NEW):
        raise ValueError("current depot report identity mismatch")
    entries = data.get("entries", [])
    if (data.get("counts") != {"changed": 417, "added": 7}
            or len(entries) != 424 or len({e["path"] for e in entries}) != 424):
        raise ValueError("current audited payload entries mismatch")
    for entry in entries:
        record = current.records.get(entry["path"])
        if record is None or entry["new"] != record.evidence():
            raise ValueError(f"current manifest evidence mismatch: {entry['path']}")
    depot.verify_current_payload(data, game_root)
