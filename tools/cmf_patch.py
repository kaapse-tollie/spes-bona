"""Verify and apply SB's exact CMF compatibility payload in staging."""

import hashlib
import json
from pathlib import Path, PurePosixPath
import re


DEFAULT_MANIFEST = Path(__file__).resolve().parents[1] / "patches/cmf/sb-1.15.2-r1/manifest.json"
REVISION = "sb-1.15.2-r1"
GUI_PATCH_TARGETS = {"gui/com_gui_progressbars.gui"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree_digest(root: Path) -> str:
    rows = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if ".git" in relative.parts or path.name == ".DS_Store":
            continue
        if path.is_symlink():
            raise ValueError(f"CMF tree contains a symlink: {relative}")
        if path.is_file():
            rows.append(relative.as_posix() + "\0" + digest(path.read_bytes()) + "\n")
    return digest("".join(rows).encode())


def load_patch(path: Path = DEFAULT_MANIFEST) -> dict:
    patch = json.loads(path.read_text(encoding="utf-8"))
    if patch.get("schema_version") != 1 or patch.get("revision") != REVISION:
        raise ValueError("unsupported CMF patch manifest")
    for key in ("base_asset_sha256", "base_tree_sha256", "tree_sha256"):
        if re.fullmatch(r"[0-9a-f]{64}", str(patch.get(key, ""))) is None:
            raise ValueError(f"invalid CMF patch {key}")
    seen = set()
    if not patch.get("files"):
        raise ValueError("empty CMF patch")
    for entry in patch["files"]:
        for key in ("path", "payload"):
            value = entry[key]
            relative = PurePosixPath(value)
            if relative.is_absolute() or ".." in relative.parts or "\\" in value or relative.as_posix() != value:
                raise ValueError(f"unsafe CMF patch {key}: {value}")
        if entry["path"] in seen:
            raise ValueError("duplicate CMF patch target")
        seen.add(entry["path"])
        if (not entry["path"].startswith("common/") and entry["path"] not in GUI_PATCH_TARGETS) or entry["payload"] != "files/" + entry["path"]:
            raise ValueError("unexpected CMF patch target")
        for key in ("original_sha256", "sha256"):
            if re.fullmatch(r"[0-9a-f]{64}", str(entry.get(key, ""))) is None:
                raise ValueError(f"invalid CMF patch {key}")
        payload = path.parent / entry["payload"]
        if payload.is_symlink() or not payload.resolve().is_relative_to(path.parent.resolve()):
            raise ValueError("unsafe CMF patch payload")
        if digest(payload.read_bytes()) != entry["sha256"]:
            raise ValueError(f"CMF patch payload hash mismatch: {entry['path']}")
    return patch


def verify_install(root: Path, manifest: Path = DEFAULT_MANIFEST) -> None:
    patch = load_patch(manifest)
    if tree_digest(root) != patch["tree_sha256"]:
        raise ValueError(f"CMF installation does not match required patch {patch['revision']}")


def verify_upstream(game: Path, manifest: Path = DEFAULT_MANIFEST) -> None:
    try:
        from .check_override_inventory import find_object, extract_braced_object
    except ImportError:
        from check_override_inventory import find_object, extract_braced_object
    patch = load_patch(manifest)
    for entry in patch.get("upstream_contracts", []):
        path = game / entry["path"]
        data = path.read_bytes()
        if digest(data) != entry["file_sha256"]:
            raise ValueError(f"CMF upstream source drift: {entry['path']}")
        source = data.decode("utf-8-sig")
        if entry["kind"] == "gui_type":
            matches = list(re.finditer(r"\btype\s+" + re.escape(entry["key"]) + r"\s*=", source))
            if len(matches) != 1:
                raise ValueError(f"CMF upstream GUI type missing or ambiguous: {entry['key']}")
            body = extract_braced_object(source, matches[0].start())
        else:
            body = find_object(source, entry["key"])
        if digest(body.encode()) != entry["object_sha256"]:
            raise ValueError(f"CMF upstream object drift: {entry['key']}")


def apply_patch(root: Path, manifest: Path = DEFAULT_MANIFEST) -> None:
    patch = load_patch(manifest)
    if tree_digest(root) != patch["base_tree_sha256"]:
        raise ValueError("CMF pristine release tree hash mismatch")
    # Validate every source before writing any replacement. The caller owns staging.
    for entry in patch["files"]:
        if digest((root / entry["path"]).read_bytes()) != entry["original_sha256"]:
            raise ValueError(f"CMF original file hash mismatch: {entry['path']}")
    for entry in patch["files"]:
        (root / entry["path"]).write_bytes((manifest.parent / entry["payload"]).read_bytes())
    verify_install(root, manifest)
