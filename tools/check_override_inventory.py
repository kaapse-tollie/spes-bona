#!/usr/bin/env python3
"""Validate Spes Bona's exact-path and keyed override inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HARD_REPLACE_RE = re.compile(
    r"^(REPLACE|TRY_REPLACE|REPLACE_OR_CREATE):([^\s=]+)\s*=\s*\{", re.MULTILINE
)
TOP_LEVEL_RE = re.compile(r"^([A-Za-z0-9_]+)\s*=\s*\{", re.MULTILINE)
SKIP_TOP_LEVEL = {".git", ".claude", ".prime"}
SUPPORTED_TARGETS = {"1.13.10": "24689003"}
CMF_NAME = "Community Mod Framework"
CMF_VERSION = "1.63.0"
CMF_COMMIT = "bd92022"
CMF_DEPENDENCY_RANGE = "1.63.*"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def listed_repo_files(root: Path) -> list[Path]:
    """Use Git's tracked/untracked set so ignored editor/game artifacts are excluded."""
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        capture_output=True,
    )
    if result.returncode == 0:
        return [Path(item.decode()) for item in result.stdout.split(b"\0") if item and (root / item.decode()).is_file()]
    return [
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file() and path.relative_to(root).parts[0] not in SKIP_TOP_LEVEL
    ]


def extract_braced_object(text: str, start: int) -> str:
    brace = text.find("{", start)
    if brace < 0:
        raise ValueError("object has no opening brace")
    depth = 0
    in_quote = False
    escaped = False
    in_comment = False
    for index in range(brace, len(text)):
        char = text[index]
        if in_comment:
            if char == "\n":
                in_comment = False
            continue
        if in_quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_quote = False
            continue
        if char == "#":
            in_comment = True
        elif char == '"':
            in_quote = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("unclosed object")


def find_object(text: str, key: str, *, directive: str | None = None) -> str:
    if directive is None:
        pattern = re.compile(rf"^{re.escape(key)}\s*=\s*\{{", re.MULTILINE)
    else:
        pattern = re.compile(rf"^{re.escape(directive)}:{re.escape(key)}\s*=\s*\{{", re.MULTILINE)
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise ValueError(f"expected one {directive + ':' if directive else ''}{key}, found {len(matches)}")
    return extract_braced_object(text, matches[0].start())


def current_collisions(root: Path, game_root: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for rel in listed_repo_files(root):
        if (game_root / rel).is_file():
            result[rel.as_posix()] = root / rel
    return result


def current_keyed_overrides(root: Path) -> dict[tuple[str, str, str], str]:
    result: dict[tuple[str, str, str], str] = {}
    for rel in listed_repo_files(root):
        if rel.suffix not in {".txt", ".gui"}:
            continue
        path = root / rel
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        for match in HARD_REPLACE_RE.finditer(text):
            identity = (rel.as_posix(), match.group(1), match.group(2))
            result[identity] = extract_braced_object(text, match.start())
    return result


def extract_top_level_blocks(text: str) -> dict[str, str]:
    return {match.group(1): extract_braced_object(text, match.start()) for match in TOP_LEVEL_RE.finditer(text)}


def state_region_block_comparison(root: Path, game_root: Path) -> tuple[set[str], set[str]]:
    rel = Path("map_data/state_regions/04_subsaharan_africa.txt")
    if not (root / rel).is_file() or not (game_root / rel).is_file():
        return set(), set()
    mod_blocks = extract_top_level_blocks((root / rel).read_text(encoding="utf-8-sig"))
    upstream_blocks = extract_top_level_blocks((game_root / rel).read_text(encoding="utf-8-sig"))
    changed = {name for name, block in mod_blocks.items() if upstream_blocks.get(name) != block}
    missing = set(upstream_blocks) - set(mod_blocks)
    return changed, missing


def load_metadata(path: Path, label: str, errors: list[str]) -> dict:
    if not path.is_file():
        errors.append(f"{label}: metadata file is missing")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        errors.append(f"{label}: invalid metadata JSON: {exc}")
        return {}


def validate_release_metadata(root: Path, inventory: dict, errors: list[str]) -> None:
    target = inventory.get("target_game_version")
    expected_build = SUPPORTED_TARGETS.get(target)
    if expected_build is None:
        errors.append(f"unsupported target_game_version: {target}")
    elif str(inventory.get("target_steam_build")) != expected_build:
        errors.append(
            f"target_steam_build {inventory.get('target_steam_build')} does not match "
            f"{target} build {expected_build}"
        )

    baseline = inventory.get("generated_for_commit_baseline")
    if not isinstance(baseline, str) or re.fullmatch(r"[0-9a-f]{40}", baseline) is None:
        errors.append("generated_for_commit_baseline must be a full 40-character Git commit")

    metadata = load_metadata(root / ".metadata/metadata.json", "SB", errors)
    if metadata:
        if metadata.get("supported_game_version") != target:
            errors.append(
                ".metadata supported_game_version does not match inventory target "
                f"{target}"
            )
        relationships = metadata.get("relationships", [])
        cmf_relationships = [
            relation
            for relation in relationships
            if relation.get("id") == "com.github.Victoria-3-Modding-Co-op.Community-Mod-Framework"
        ]
        if (
            len(cmf_relationships) != 1
            or cmf_relationships[0].get("version") != CMF_DEPENDENCY_RANGE
        ):
            errors.append(
                "SB metadata must declare exactly one CMF dependency at version "
                f"{CMF_DEPENDENCY_RANGE}"
            )

    dependencies = [
        dependency
        for dependency in inventory.get("dependencies", [])
        if dependency.get("name") == CMF_NAME
    ]
    if len(dependencies) != 1:
        errors.append(f"inventory must declare exactly one {CMF_NAME} dependency")
    else:
        dependency = dependencies[0]
        if dependency.get("version") != CMF_VERSION:
            errors.append(f"inventory CMF version must be {CMF_VERSION}")
        if dependency.get("commit") != CMF_COMMIT:
            errors.append(f"inventory CMF commit must be {CMF_COMMIT}")


def validate_cmf_checkout(cmf_root: Path, errors: list[str]) -> None:
    metadata = load_metadata(cmf_root / ".metadata/metadata.json", "CMF", errors)
    if metadata and metadata.get("version") != CMF_VERSION:
        errors.append(
            f"CMF checkout metadata version {metadata.get('version')} does not match {CMF_VERSION}"
        )
    if (cmf_root / ".git").exists():
        result = subprocess.run(
            ["git", "-C", str(cmf_root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0 or not result.stdout.strip().startswith(CMF_COMMIT):
            actual = result.stdout.strip() or "unavailable"
            errors.append(f"CMF checkout commit {actual} does not match {CMF_COMMIT}")


def validate_upstream_api_surface(
    game_root: Path, cmf_root: Path | None, errors: list[str]
) -> None:
    vanilla_on_actions = game_root / "common/on_actions/00_code_on_actions.txt"
    if not vanilla_on_actions.is_file():
        errors.append("Vanilla 1.13.10 code on-actions file is missing")
    else:
        source = vanilla_on_actions.read_text(encoding="utf-8-sig")
        expected = {
            "on_treaty_ports_inherited": (
                "id = treaty_port_inheritance_events.1",
                "popup = yes",
            ),
            "on_company_disbanded": (
                "re_add_disbanded_company_prestige_good_jes = yes",
            ),
        }
        for key, tokens in expected.items():
            try:
                block = find_object(source, key)
            except ValueError as exc:
                errors.append(f"Vanilla 1.13.10 API {key}: {exc}")
                continue
            for token in tokens:
                if token not in block:
                    errors.append(f"Vanilla 1.13.10 API {key} is missing: {token}")

    if cmf_root is None:
        return

    requirements = {
        "common/scripted_effects/com_international_situation_effects.txt": (
            ("com_set_situation_left_title", None),
            ("com_set_situation_right_title", None),
        ),
        "common/console_command_macros/com_macros.txt": (
            ("com_container", None),
        ),
    }
    for rel, objects in requirements.items():
        path = cmf_root / rel
        if not path.is_file():
            errors.append(f"CMF {CMF_VERSION} API source is missing: {rel}")
            continue
        source = path.read_text(encoding="utf-8-sig")
        for key, directive in objects:
            try:
                find_object(source, key, directive=directive)
            except ValueError as exc:
                errors.append(f"CMF {CMF_VERSION} API {key}: {exc}")

    widget = cmf_root / "gui/com_journal_injects/situation_widgets.gui"
    if not widget.is_file():
        errors.append(f"CMF {CMF_VERSION} situation widget is missing")
    else:
        source = widget.read_text(encoding="utf-8-sig")
        for token in ("com_situation_left_title_var", "com_situation_right_title_var"):
            if token not in source:
                errors.append(f"CMF {CMF_VERSION} situation widget is missing: {token}")


def require_metadata(entry: dict, label: str, errors: list[str]) -> None:
    for field in ("scope", "intent", "load_order", "owner", "rebase_date"):
        if not isinstance(entry.get(field), str) or not entry[field].strip():
            errors.append(f"{label}: missing non-empty {field}")


def validate(root: Path, game_root: Path, inventory: dict, cmf_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    target = inventory.get("target_game_version")
    validate_release_metadata(root, inventory, errors)
    if cmf_root is not None:
        validate_cmf_checkout(cmf_root, errors)
    validate_upstream_api_surface(game_root, cmf_root, errors)
    descriptor = (root / "descriptor.mod").read_text(encoding="utf-8-sig")
    supported = re.findall(r'^\s*supported_version\s*=\s*"([^"]+)"', descriptor, re.MULTILINE)
    if supported != [target]:
        errors.append(f"descriptor supported_version {supported} does not match inventory target {target}")

    declared_collisions = {entry["path"]: entry for entry in inventory.get("same_path_files", [])}
    actual_collisions = current_collisions(root, game_root)
    for path in sorted(actual_collisions.keys() - declared_collisions.keys()):
        errors.append(f"unmanifested same-path collision: {path}")
    for path in sorted(declared_collisions.keys() - actual_collisions.keys()):
        errors.append(f"stale same-path inventory entry: {path}")
    for path in sorted(actual_collisions.keys() & declared_collisions.keys()):
        entry = declared_collisions[path]
        require_metadata(entry, path, errors)
        if entry.get("upstream_version") != target:
            errors.append(f"{path}: upstream_version does not match target")
        if entry.get("upstream_sha256") != sha256(game_root / path):
            errors.append(f"{path}: upstream hash drift; rebase/review required")
        if entry.get("mod_sha256") != sha256(root / path):
            errors.append(f"{path}: mod hash drift; intended delta/inventory review required")
        if entry.get("comparison") not in {"text-hash-pair", "binary-hash-pair", "identical-hash"}:
            errors.append(f"{path}: invalid comparison kind")

    declared_keyed = {
        (entry["mod_path"], entry["directive"], entry["key"]): entry
        for entry in inventory.get("keyed_overrides", [])
    }
    actual_keyed = current_keyed_overrides(root)
    for identity in sorted(actual_keyed.keys() - declared_keyed.keys()):
        errors.append(f"unmanifested keyed override: {identity}")
    for identity in sorted(declared_keyed.keys() - actual_keyed.keys()):
        errors.append(f"stale keyed override inventory entry: {identity}")
    text_cache: dict[Path, str] = {}
    for identity in sorted(actual_keyed.keys() & declared_keyed.keys()):
        entry = declared_keyed[identity]
        label = ":".join(identity)
        require_metadata(entry, label, errors)
        if entry.get("mod_object_sha256") != sha256_bytes(actual_keyed[identity].encode("utf-8")):
            errors.append(f"{label}: mod object hash drift")
        upstream = entry.get("upstream")
        if upstream is None:
            if entry["directive"] != "REPLACE_OR_CREATE":
                errors.append(f"{label}: only REPLACE_OR_CREATE may have no upstream object")
        else:
            upstream_path = game_root / upstream["path"]
            if not upstream_path.is_file():
                errors.append(f"{label}: upstream source missing: {upstream['path']}")
            else:
                if upstream.get("file_sha256") != sha256(upstream_path):
                    errors.append(f"{label}: upstream source-file hash drift")
                try:
                    text = text_cache.setdefault(upstream_path, upstream_path.read_text(encoding="utf-8-sig"))
                    block = find_object(text, upstream.get("key", entry["key"]))
                    if upstream.get("object_sha256") != sha256_bytes(block.encode("utf-8")):
                        errors.append(f"{label}: upstream object hash drift")
                except ValueError as exc:
                    errors.append(f"{label}: {exc}")
        baseline = entry.get("dependency_baseline")
        if baseline:
            if cmf_root is None:
                errors.append(f"{label}: CMF baseline declared but CMF root was not found")
            else:
                baseline_path = cmf_root / baseline["path"]
                if not baseline_path.is_file():
                    errors.append(f"{label}: dependency baseline source missing")
                else:
                    if baseline.get("file_sha256") != sha256(baseline_path):
                        errors.append(f"{label}: dependency baseline file hash drift")
                    try:
                        text = text_cache.setdefault(baseline_path, baseline_path.read_text(encoding="utf-8-sig"))
                        block = find_object(text, entry["key"], directive="REPLACE")
                        if baseline.get("object_sha256") != sha256_bytes(block.encode("utf-8")):
                            errors.append(f"{label}: dependency baseline object hash drift")
                    except ValueError as exc:
                        errors.append(f"{label}: dependency baseline {exc}")

    actual_blocks, missing_upstream_blocks = state_region_block_comparison(root, game_root)
    for name in sorted(missing_upstream_blocks):
        errors.append(f"collided state-region file omits upstream block: {name}")
    declared_blocks = set(inventory.get("state_region_blocks", []))
    for name in sorted(actual_blocks - declared_blocks):
        errors.append(f"unmanifested changed state-region block: {name}")
    for name in sorted(declared_blocks - actual_blocks):
        errors.append(f"stale state-region block inventory entry: {name}")

    actual_replace_paths = sorted(re.findall(r'^\s*replace_path\s*=\s*"([^"]+)"', descriptor, re.MULTILINE))
    declared_replace_paths = sorted(inventory.get("approved_replace_paths", []))
    if actual_replace_paths != declared_replace_paths:
        errors.append(f"descriptor replace_path drift: actual={actual_replace_paths}, declared={declared_replace_paths}")
    return errors


def find_root(explicit: str | None, env_name: str, candidates: list[Path], required: tuple[str, ...]) -> Path | None:
    values = [Path(explicit).expanduser() if explicit else None, Path(os.environ[env_name]).expanduser() if os.environ.get(env_name) else None, *candidates]
    for value in values:
        if value is None:
            continue
        value = value.resolve()
        if all((value / part).exists() for part in required):
            return value
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-root", help="Victoria 3 game directory")
    parser.add_argument("--cmf-root", help="Community Mod Framework directory")
    parser.add_argument("--inventory", default="Docs/compatibility/override_inventory.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    game_root = find_root(args.game_root, "VIC3_GAME_ROOT", [
        Path.home() / "Library/Application Support/Steam/steamapps/common/Victoria 3/game",
        Path.home() / ".steam/steam/steamapps/common/Victoria 3/game",
        Path.home() / ".local/share/Steam/steamapps/common/Victoria 3/game",
    ], ("common", "map_data"))
    if game_root is None:
        print("Victoria 3 game root not found; pass --game-root or set VIC3_GAME_ROOT")
        return 2
    cmf_root = find_root(args.cmf_root, "CMF_ROOT", [
        Path.home() / "Documents/Paradox Interactive/Victoria 3/mod/Community Mod Framework",
    ], ("common",))
    inventory = json.loads((root / args.inventory).read_text(encoding="utf-8"))
    errors = validate(root, game_root, inventory, cmf_root)
    if errors:
        print("Override inventory validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Override inventory OK: {len(inventory['same_path_files'])} same-path files, "
        f"{len(inventory['keyed_overrides'])} keyed overrides, "
        f"{len(inventory['state_region_blocks'])} changed state-region blocks, "
        f"{len(inventory['approved_replace_paths'])} replace_path directives."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
