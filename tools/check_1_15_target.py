"""Verify the exact 1.15.0 core manifest and the audited installed payload.

This is a current-target check, not a reconstructed historical depot diff.
"""
import json
from pathlib import Path

from tools import build_steam_depot_delta as depot

NEW = depot.ManifestIdentity(
    label="Victoria 3 1.15.0", game_version="1.15.0", steam_build="26453692",
    depot_id=529341, manifest_id=7727600027425614094,
    created_utc="2026-11-03T17:10:02Z",
    source_name="529341_7727600027425614094.manifest", source_size=4907427,
    source_sha256="11c40742e46590c5d0018003f2ee4febee43216fe2b05e0ae5b0b3b7f5ca4298",
    entry_count=27657,
)
OUTPUT = Path(__file__).resolve().parents[1] / "Docs/compatibility/evidence/1_15_0_implementation/current_target.json"


def verify_current_target(game_root, *, report_path=OUTPUT, manifest_path=None):
    current = depot.decode_manifest(manifest_path or depot.default_manifest_path(NEW), NEW)
    data = json.loads(Path(report_path).read_text())
    if data.get("new_manifest") != depot._manifest_summary(NEW):
        raise ValueError("current depot report identity mismatch")
    entries = data.get("entries", [])
    if len(entries) != 146 or len({e["path"] for e in entries}) != 146:
        raise ValueError("current audited payload entries mismatch")
    for entry in entries:
        record = current.records.get(entry["path"])
        if record is None or entry["new"] != record.evidence():
            raise ValueError(f"current manifest evidence mismatch: {entry['path']}")
    depot.verify_current_payload(data, game_root)
