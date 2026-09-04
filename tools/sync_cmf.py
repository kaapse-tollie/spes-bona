#!/usr/bin/env python3
"""Synchronize the canonical local CMF install with an exact GitHub release."""

from __future__ import annotations

import argparse
import hashlib
from http.client import RemoteDisconnected
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import tempfile
import time
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
import zipfile


CMF_ID = "com.github.Victoria-3-Modding-Co-op.Community-Mod-Framework"
REPOSITORY = "Victoria-3-Modding-Co-op/Community-Mod-Framework"
RELEASES_URL = f"https://api.github.com/repos/{REPOSITORY}/releases"
LATEST_RELEASE_URL = f"{RELEASES_URL}/latest"
PINNED_TAG = "1.66.0"
PINNED_SHA256 = "79dd0d434e6ffb617147ad1b91b73e6306139adfffcadf6774eeb32db3a09b8b"
DEFAULT_TARGET = Path(__file__).resolve().parents[2] / "Community Mod Framework"
USER_AGENT = "Spes-Bona-CMF-Synchronizer/1"
SAFE_TAG_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]*")
SHA256_RE = re.compile(r"[0-9a-fA-F]{64}")


class SyncError(RuntimeError):
    """A safe CMF synchronization could not be completed."""


def request(url: str, *, binary: bool = False) -> Request:
    headers = {
        "Accept": "application/octet-stream" if binary else "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return Request(url, headers=headers)


def read_url(
    url: str,
    opener: Callable = urlopen,
    *,
    binary: bool = False,
    attempts: int = 3,
) -> bytes:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with opener(request(url, binary=binary), timeout=60) as response:
                return response.read()
        except HTTPError as exc:
            if exc.code < 500 and exc.code != 429:
                raise SyncError(f"GitHub returned HTTP {exc.code} for {url}") from exc
            last_error = exc
        except (URLError, RemoteDisconnected, TimeoutError, OSError) as exc:
            last_error = exc
        if attempt + 1 < attempts:
            time.sleep(2 ** attempt)
    detail = getattr(last_error, "reason", last_error)
    raise SyncError(f"could not download {url} after {attempts} attempts: {detail}") from last_error


def validate_tag(tag: str) -> str:
    if not isinstance(tag, str) or SAFE_TAG_RE.fullmatch(tag) is None:
        raise SyncError(f"invalid CMF release tag {tag!r}")
    return tag


def validate_sha256(digest: str, *, label: str = "expected SHA-256") -> str:
    if not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None:
        raise SyncError(f"{label} must be exactly 64 hexadecimal characters")
    return digest.lower()


def tagged_release_url(tag: str) -> str:
    tag = validate_tag(tag)
    return f"{RELEASES_URL}/tags/{quote(tag, safe='')}"


def read_release_metadata(url: str, opener: Callable = urlopen) -> dict:
    try:
        release = json.loads(read_url(url, opener))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise SyncError("GitHub returned invalid release metadata") from exc
    if not isinstance(release, dict):
        raise SyncError("GitHub returned invalid release metadata")
    return release


def parse_release(
    release: dict,
    *,
    source: str,
    expected_tag: str | None = None,
    expected_sha256: str | None = None,
) -> dict:
    if release.get("draft") is not False or release.get("prerelease") is not False:
        raise SyncError(f"GitHub's {source} endpoint returned a non-stable release")

    version = release.get("tag_name")
    if not isinstance(version, str) or SAFE_TAG_RE.fullmatch(version) is None:
        raise SyncError(f"GitHub's {source} CMF release has no valid tag")
    if expected_tag is not None and version != expected_tag:
        raise SyncError(
            f"GitHub's tag endpoint returned {version!r}, expected exact tag {expected_tag!r}"
        )

    asset_name = f"release-{version}.zip"
    assets_value = release.get("assets")
    assets = assets_value if isinstance(assets_value, list) else []
    matches = [
        asset
        for asset in assets
        if isinstance(asset, dict) and asset.get("name") == asset_name
    ]
    if len(matches) != 1:
        raise SyncError(f"{source} CMF release does not contain exactly one {asset_name}")
    asset = matches[0]

    digest_value = asset.get("digest")
    if not isinstance(digest_value, str) or not digest_value.startswith("sha256:"):
        raise SyncError(f"{asset_name} has no GitHub SHA-256 digest")
    digest = validate_sha256(
        digest_value.removeprefix("sha256:"),
        label=f"GitHub digest for {asset_name}",
    )
    if expected_sha256 is not None and digest != expected_sha256:
        raise SyncError(
            f"GitHub digest for {asset_name} is {digest}, expected {expected_sha256}"
        )

    download_url = asset.get("browser_download_url")
    canonical_url = (
        f"https://github.com/{REPOSITORY}/releases/download/"
        f"{quote(version, safe='')}/{quote(asset_name, safe='')}"
    )
    if download_url != canonical_url:
        raise SyncError(f"{asset_name} has an unexpected download URL")

    return {
        "version": version,
        "asset_name": asset_name,
        "download_url": download_url,
        "sha256": digest,
    }


def tagged_release(
    tag: str,
    expected_sha256: str,
    opener: Callable = urlopen,
) -> dict:
    tag = validate_tag(tag)
    expected_sha256 = validate_sha256(expected_sha256)
    release = read_release_metadata(tagged_release_url(tag), opener)
    return parse_release(
        release,
        source=f"tag {tag}",
        expected_tag=tag,
        expected_sha256=expected_sha256,
    )


def latest_release(opener: Callable = urlopen) -> dict:
    release = read_release_metadata(LATEST_RELEASE_URL, opener)
    return parse_release(release, source="latest")


def download_release(url: str, opener: Callable = urlopen) -> bytes:
    try:
        return read_url(url, opener, binary=True)
    except SyncError:
        if opener is not urlopen:
            raise
    curl = shutil.which("curl")
    if curl is None:
        raise SyncError("Python download failed and curl is not installed")
    with tempfile.NamedTemporaryFile() as download:
        result = subprocess.run(
            [
                curl,
                "--fail",
                "--location",
                "--silent",
                "--show-error",
                "--retry",
                "3",
                "--output",
                download.name,
                url,
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            detail = result.stderr.strip() or f"curl exited {result.returncode}"
            raise SyncError(f"curl could not download {url}: {detail}")
        return Path(download.name).read_bytes()


def load_installed_metadata(target: Path) -> dict:
    path = target / ".metadata/metadata.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


def validate_member(member: zipfile.ZipInfo) -> None:
    path = PurePosixPath(member.filename)
    if path.is_absolute() or ".." in path.parts or "\\" in member.filename:
        raise SyncError(f"release archive contains an unsafe path: {member.filename}")
    mode = member.external_attr >> 16
    if stat.S_ISLNK(mode):
        raise SyncError(f"release archive contains a symbolic link: {member.filename}")


def extract_release(archive: bytes, destination: Path, version: str) -> None:
    archive_path = destination / "release.zip"
    archive_path.write_bytes(archive)
    payload = destination / "payload"
    payload.mkdir()
    try:
        with zipfile.ZipFile(archive_path) as bundle:
            for member in bundle.infolist():
                validate_member(member)
            bundle.extractall(payload)
    except zipfile.BadZipFile as exc:
        raise SyncError("GitHub's CMF release asset is not a valid ZIP archive") from exc

    metadata = load_installed_metadata(payload)
    if metadata.get("id") != CMF_ID:
        raise SyncError("release archive does not contain canonical CMF metadata")
    if metadata.get("version") != version:
        raise SyncError(
            f"release archive metadata version {metadata.get('version')} does not match tag {version}"
        )
    if not (payload / "common").is_dir() or not (payload / "gui").is_dir():
        raise SyncError("release archive is missing required CMF content")


def path_exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def install_release(target: Path, release: dict, archive: bytes) -> None:
    if "steamapps/workshop" in target.as_posix().lower():
        raise SyncError("refusing to overwrite a Steam Workshop installation")
    target.parent.mkdir(parents=True, exist_ok=True)
    actual_digest = hashlib.sha256(archive).hexdigest()
    if actual_digest != release["sha256"]:
        raise SyncError(
            f"downloaded {release['asset_name']} digest {actual_digest} "
            f"does not match required {release['sha256']}"
        )

    # Extract and validate the complete candidate before moving the live target. Both
    # directory renames are on the target filesystem. If the second rename fails, the
    # first is reversed before the staging directory is removed.
    staging = Path(tempfile.mkdtemp(prefix=".cmf-update-", dir=target.parent))
    preserve_staging = False
    try:
        extract_release(archive, staging, release["version"])
        payload = staging / "payload"
        backup = staging / "previous"
        had_target = path_exists(target)
        try:
            if had_target:
                target.rename(backup)
            payload.rename(target)
        except BaseException as exc:
            rollback_error: BaseException | None = None
            if path_exists(backup):
                if path_exists(target):
                    rollback_error = RuntimeError("replacement path unexpectedly exists")
                else:
                    try:
                        backup.rename(target)
                    except BaseException as caught:
                        rollback_error = caught
            if rollback_error is not None:
                preserve_staging = True
                raise SyncError(
                    "CMF installation failed and automatic rollback failed; "
                    f"the previous installation remains at {backup}: {rollback_error}"
                ) from exc
            if isinstance(exc, Exception):
                state = "previous installation was restored" if had_target else "target was unchanged"
                raise SyncError(f"atomic CMF installation failed; {state}: {exc}") from exc
            raise
    finally:
        if not preserve_staging:
            shutil.rmtree(staging, ignore_errors=True)


def synchronize(
    target: Path,
    *,
    tag: str | None = None,
    expected_sha256: str | None = None,
    latest: bool = False,
    check_only: bool = False,
    force: bool = False,
    opener: Callable = urlopen,
) -> tuple[str, str]:
    target = target.expanduser().absolute()
    if latest:
        if tag is not None or expected_sha256 is not None:
            raise SyncError("latest maintenance mode cannot be combined with an exact tag or digest")
        release = latest_release(opener)
        expectation = f"latest release {release['version']}"
    else:
        exact_tag = PINNED_TAG if tag is None else tag
        if expected_sha256 is None:
            if exact_tag != PINNED_TAG:
                raise SyncError("an exact non-pinned tag requires an expected SHA-256")
            expected_sha256 = PINNED_SHA256
        release = tagged_release(exact_tag, expected_sha256, opener)
        expectation = f"exact release {exact_tag}"

    installed = load_installed_metadata(target)
    current = (
        installed.get("id") == CMF_ID
        and installed.get("version") == release["version"]
        and (target / "common").is_dir()
        and (target / "gui").is_dir()
    )
    if current and not force:
        return "current", release["version"]
    if check_only:
        installed_version = installed.get("version", "not installed")
        raise SyncError(f"CMF {installed_version} is not {expectation}")
    archive = download_release(release["download_url"], opener)
    install_release(target, release, archive)
    return "updated", release["version"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--tag",
        help=f"Synchronize an exact release tag (default: {PINNED_TAG})",
    )
    mode.add_argument(
        "--latest",
        action="store_true",
        help="Maintenance only: discover and synchronize GitHub's latest stable release",
    )
    parser.add_argument(
        "--sha256",
        "--expected-sha256",
        dest="expected_sha256",
        help=f"Required archive SHA-256 for exact-tag mode (default for {PINNED_TAG}: pinned)",
    )
    parser.add_argument("--check", action="store_true", help="Check without installing an update")
    parser.add_argument("--force", action="store_true", help="Reinstall even when versions match")
    args = parser.parse_args()
    if args.latest and args.expected_sha256 is not None:
        parser.error("--sha256 cannot be combined with --latest")
    try:
        status, version = synchronize(
            args.target,
            tag=args.tag,
            expected_sha256=args.expected_sha256,
            latest=args.latest,
            check_only=args.check,
            force=args.force,
        )
    except SyncError as exc:
        print(f"CMF synchronization FAILED: {exc}")
        return 1
    verb = "is current at" if status == "current" else "updated to"
    print(f"Community Mod Framework {verb} {version}: {args.target.expanduser().absolute()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
