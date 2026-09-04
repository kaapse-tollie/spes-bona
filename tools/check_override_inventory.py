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
STEAM_APP_ID = "529340"
CORE_DEPOT_ID = "529341"
SUPPORTED_TARGETS = {
    "1.14.0": {
        "build": "25081502",
        "branch": "1.14-openbeta",
        "core_depot": CORE_DEPOT_ID,
        "core_manifest": "3868129321396195520",
    }
}
CMF_NAME = "Community Mod Framework"
CMF_VERSION = "1.66.0"
CMF_COMMIT = "807c32ff42b75714a3a0e090c0db3357b5e46ed7"
CMF_DEPENDENCY_RANGE = "1.66.*"
CMF_RELEASE_TAG = "1.66.0"
CMF_ASSET_NAME = "release-1.66.0.zip"
CMF_ASSET_SHA256 = "79dd0d434e6ffb617147ad1b91b73e6306139adfffcadf6774eeb32db3a09b8b"


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


VDF_TOKEN_RE = re.compile(r'"((?:\\.|[^"\\])*)"|([{}])')


def parse_vdf(text: str) -> dict:
    """Parse the quoted KeyValues subset used by Steam app manifests."""
    tokens = [
        match.group(1).replace(r'\"', '"').replace(r"\\", "\\")
        if match.group(1) is not None
        else match.group(2)
        for match in VDF_TOKEN_RE.finditer(text)
    ]

    def parse_object(index: int, *, nested: bool) -> tuple[dict, int]:
        result: dict[str, object] = {}
        while index < len(tokens):
            token = tokens[index]
            if token == "}":
                if not nested:
                    raise ValueError("unexpected closing brace")
                return result, index + 1
            if token == "{":
                raise ValueError("object key is missing")
            key = token
            index += 1
            if index >= len(tokens):
                raise ValueError(f"missing value for {key}")
            value = tokens[index]
            index += 1
            if value == "{":
                value, index = parse_object(index, nested=True)
            elif value == "}":
                raise ValueError(f"missing value for {key}")
            result[key] = value
        if nested:
            raise ValueError("unclosed object")
        return result, index

    parsed, index = parse_object(0, nested=False)
    if index != len(tokens):
        raise ValueError("unexpected trailing tokens")
    return parsed


def find_steam_app_manifest(game_root: Path) -> Path | None:
    filename = f"appmanifest_{STEAM_APP_ID}.acf"
    for directory in (game_root, *game_root.parents):
        candidate = directory / filename
        if candidate.is_file():
            return candidate
    return None


def validate_steam_app_manifest(path: Path, inventory: dict, errors: list[str]) -> None:
    try:
        parsed = parse_vdf(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        errors.append(f"Steam app manifest is invalid: {exc}")
        return
    app = parsed.get("AppState")
    if not isinstance(app, dict):
        errors.append("Steam app manifest has no AppState object")
        return
    if str(app.get("appid", "")) != STEAM_APP_ID:
        errors.append(
            f"Steam app manifest appid {app.get('appid', 'missing')} does not match {STEAM_APP_ID}"
        )

    expected_build = str(inventory.get("target_steam_build", ""))
    actual_build = str(app.get("buildid", ""))
    if actual_build != expected_build:
        errors.append(
            f"installed Steam build {actual_build or 'missing'} does not match "
            f"target_steam_build {expected_build}"
        )

    expected_branch = str(inventory.get("target_steam_branch", ""))
    branches = {
        str(section.get("BetaKey"))
        for name in ("UserConfig", "MountedConfig")
        if isinstance((section := app.get(name)), dict) and section.get("BetaKey") is not None
    }
    if branches != {expected_branch}:
        actual = ", ".join(sorted(branches)) if branches else "missing"
        errors.append(
            f"installed Steam branch {actual} does not match target_steam_branch "
            f"{expected_branch}"
        )

    depots = app.get("InstalledDepots")
    depot_id = str(inventory.get("target_core_depot", ""))
    expected_manifest = str(inventory.get("target_core_depot_manifest", ""))
    depot = depots.get(depot_id) if isinstance(depots, dict) else None
    actual_manifest = str(depot.get("manifest", "")) if isinstance(depot, dict) else ""
    if actual_manifest != expected_manifest:
        errors.append(
            f"installed core depot {depot_id or 'missing'} manifest "
            f"{actual_manifest or 'missing'} does not match target_core_depot_manifest "
            f"{expected_manifest}"
        )


def validate_release_metadata(
    root: Path,
    inventory: dict,
    errors: list[str],
    steam_app_manifest: Path | None = None,
) -> None:
    if inventory.get("schema_version") != 2:
        errors.append("override inventory schema_version must be 2")

    target = inventory.get("target_game_version")
    expected = SUPPORTED_TARGETS.get(target)
    if expected is None:
        errors.append(f"unsupported target_game_version: {target}")
    else:
        fields = {
            "target_steam_build": expected["build"],
            "target_steam_branch": expected["branch"],
            "target_core_depot": expected["core_depot"],
            "target_core_depot_manifest": expected["core_manifest"],
        }
        for field, value in fields.items():
            if inventory.get(field) != value:
                errors.append(
                    f"{field} {inventory.get(field)} does not match {target} target {value}"
                )

    if steam_app_manifest is not None:
        validate_steam_app_manifest(steam_app_manifest, inventory, errors)

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
        expected_fields = {
            "version": CMF_VERSION,
            "version_range": CMF_DEPENDENCY_RANGE,
            "commit": CMF_COMMIT,
            "release_tag": CMF_RELEASE_TAG,
            "asset_name": CMF_ASSET_NAME,
            "asset_sha256": CMF_ASSET_SHA256,
        }
        for field, value in expected_fields.items():
            if dependency.get(field) != value:
                errors.append(f"inventory CMF {field} must be {value}")

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
        if result.returncode != 0 or result.stdout.strip() != CMF_COMMIT:
            actual = result.stdout.strip() or "unavailable"
            errors.append(f"CMF checkout commit {actual} does not match {CMF_COMMIT}")


def validate_upstream_api_surface(
    game_root: Path, cmf_root: Path | None, errors: list[str]
) -> None:
    vanilla_on_actions = game_root / "common/on_actions/00_code_on_actions.txt"
    if not vanilla_on_actions.is_file():
        errors.append("Vanilla 1.14.0 code on-actions file is missing")
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
                errors.append(f"Vanilla 1.14.0 API {key}: {exc}")
                continue
            for token in tokens:
                if token not in block:
                    errors.append(f"Vanilla 1.14.0 API {key} is missing: {token}")

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



ZZ_OVERRIDE_FILE_RE = re.compile(r"^(zz|zzz)_sb_.+\.txt$")


def validate_additive_overrides(root: Path, inventory: dict, errors: list[str]) -> None:
    """Additive zz_/zzz_ files that create new objects instead of replacing upstream keys.

    They must be registered in `additive_overrides` (path, intent, owner, mod_sha256).
    Any unregistered override-style file under common/ or events/ is an error, so a new
    zz_ file cannot silently bypass the inventory contract.
    """
    registered: set[str] = set()
    for entry in inventory.get("additive_overrides", []):
        rel = entry.get("path")
        if not rel:
            errors.append("additive override entry has no path")
            continue
        registered.add(rel)
        path = root / rel
        if not path.is_file():
            errors.append(f"additive override path missing: {rel}")
            continue
        if entry.get("mod_sha256") != sha256(path):
            errors.append(f"{rel}: additive override mod hash drift")
        for field in ("intent", "owner"):
            if not str(entry.get(field, "")).strip():
                errors.append(f"{rel}: additive override missing {field}")
    keyed_paths = {k.get("mod_path") for k in inventory.get("keyed_overrides", [])}
    for base in ("common", "events"):
        base_path = root / base
        if not base_path.is_dir():
            continue
        for path in sorted(base_path.rglob("*.txt")):
            rel = path.relative_to(root).as_posix()
            if ZZ_OVERRIDE_FILE_RE.match(path.name) and rel not in registered and rel not in keyed_paths:
                errors.append(
                    f"unregistered zz_ override-style file: {rel} "
                    "(register in additive_overrides or keyed_overrides)"
                )


def validate_localization_replace(root: Path, game_root: Path, inventory: dict, errors: list[str]) -> None:
    """Files under localization/english/replace/ shadow upstream localisation by name and
    must be registered in `localization_replace_files` with an explicit upstream reference
    (or null for SB-authored names) and the mod file hash."""
    registered: set[str] = set()
    for entry in inventory.get("localization_replace_files", []):
        rel = entry.get("path")
        if not rel:
            errors.append("localization replace entry has no path")
            continue
        registered.add(rel)
        path = root / rel
        if not path.is_file():
            errors.append(f"localization replace path missing: {rel}")
            continue
        if entry.get("mod_sha256") != sha256(path):
            errors.append(f"{rel}: localization replace mod hash drift")
        if not str(entry.get("intent", "")).strip():
            errors.append(f"{rel}: localization replace entry missing intent")
        upstream = entry.get("upstream_file")
        if upstream:
            upstream_path = game_root / "localization/english" / upstream
            if not upstream_path.is_file():
                errors.append(f"{rel}: declared upstream localisation missing: {upstream}")
            elif entry.get("upstream_sha256") != sha256(upstream_path):
                errors.append(f"{rel}: upstream localisation hash drift for {upstream}")
        elif "upstream_file" not in entry:
            errors.append(f"{rel}: localization replace entry missing upstream_file (use null for SB-authored)")
    base = root / "localization/english/replace"
    if base.is_dir():
        for path in sorted(base.rglob("*.yml")):
            rel = path.relative_to(root).as_posix()
            if rel not in registered:
                errors.append(f"unregistered localization replace file: {rel}")


def validate(
    root: Path,
    game_root: Path,
    inventory: dict,
    cmf_root: Path | None = None,
    steam_app_manifest: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    target = inventory.get("target_game_version")
    validate_release_metadata(root, inventory, errors, steam_app_manifest)
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

    validate_additive_overrides(root, inventory, errors)
    validate_localization_replace(root, game_root, inventory, errors)
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
    parser.add_argument(
        "--steam-app-manifest",
        help="Optional Steam appmanifest_529340.acf path; inferred from --game-root when available",
    )
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
    steam_app_manifest = (
        Path(args.steam_app_manifest).expanduser().resolve()
        if args.steam_app_manifest
        else find_steam_app_manifest(game_root)
    )
    errors = validate(root, game_root, inventory, cmf_root, steam_app_manifest)
    if errors:
        print("Override inventory validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Override inventory OK: {len(inventory['same_path_files'])} same-path files, "
        f"{len(inventory['keyed_overrides'])} keyed overrides, "
        f"{len(inventory['state_region_blocks'])} changed state-region blocks, "
        f"{len(inventory['approved_replace_paths'])} replace_path directives, "
        f"{len(inventory.get('additive_overrides', []))} additive overrides, "
        f"{len(inventory.get('localization_replace_files', []))} localization replace files."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
