#!/usr/bin/env python3
"""Synchronize the canonical local CMF install with GitHub's latest release."""

from __future__ import annotations

import argparse
import hashlib
from http.client import RemoteDisconnected
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import tempfile
import time
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import zipfile


CMF_ID = "com.github.Victoria-3-Modding-Co-op.Community-Mod-Framework"
REPOSITORY = "Victoria-3-Modding-Co-op/Community-Mod-Framework"
LATEST_RELEASE_URL = f"https://api.github.com/repos/{REPOSITORY}/releases/latest"
DEFAULT_TARGET = Path(__file__).resolve().parents[2] / "Community Mod Framework"
USER_AGENT = "Spes-Bona-CMF-Synchronizer/1"


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


def latest_release(opener: Callable = urlopen) -> dict:
    try:
        release = json.loads(read_url(LATEST_RELEASE_URL, opener))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise SyncError("GitHub returned invalid release metadata") from exc
    if release.get("draft") or release.get("prerelease"):
        raise SyncError("GitHub's latest release endpoint returned a non-stable release")
    version = str(release.get("tag_name", "")).strip()
    if not version:
        raise SyncError("GitHub's latest CMF release has no tag")
    expected_name = f"release-{version}.zip"
    assets = [asset for asset in release.get("assets", []) if asset.get("name") == expected_name]
    if len(assets) != 1:
        raise SyncError(f"latest CMF release does not contain exactly one {expected_name}")
    asset = assets[0]
    digest = str(asset.get("digest", ""))
    if not digest.startswith("sha256:"):
        raise SyncError(f"{expected_name} has no GitHub SHA-256 digest")
    download_url = str(asset.get("browser_download_url", ""))
    if not download_url.startswith("https://github.com/"):
        raise SyncError(f"{expected_name} has an unexpected download URL")
    return {
        "version": version,
        "asset_name": expected_name,
        "download_url": download_url,
        "sha256": digest.removeprefix("sha256:"),
    }


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


def install_release(target: Path, release: dict, archive: bytes) -> None:
    if "steamapps/workshop" in target.as_posix():
        raise SyncError("refusing to overwrite a Steam Workshop installation")
    target.parent.mkdir(parents=True, exist_ok=True)
    actual_digest = hashlib.sha256(archive).hexdigest()
    if actual_digest != release["sha256"]:
        raise SyncError(
            f"downloaded {release['asset_name']} digest {actual_digest} does not match GitHub"
        )

    with tempfile.TemporaryDirectory(prefix=".cmf-update-", dir=target.parent) as temporary:
        staging = Path(temporary)
        extract_release(archive, staging, release["version"])
        payload = staging / "payload"
        backup = staging / "previous"
        if target.exists():
            target.rename(backup)
        try:
            payload.rename(target)
        except Exception:
            if backup.exists() and not target.exists():
                backup.rename(target)
            raise
        if backup.exists():
            shutil.rmtree(backup)


def synchronize(
    target: Path,
    *,
    check_only: bool = False,
    force: bool = False,
    opener: Callable = urlopen,
) -> tuple[str, str]:
    target = target.expanduser().absolute()
    release = latest_release(opener)
    installed = load_installed_metadata(target)
    current = installed.get("id") == CMF_ID and installed.get("version") == release["version"]
    if current and not force:
        return "current", release["version"]
    if check_only:
        installed_version = installed.get("version", "not installed")
        raise SyncError(f"CMF {installed_version} is not latest release {release['version']}")
    archive = download_release(release["download_url"], opener)
    install_release(target, release, archive)
    return "updated", release["version"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--check", action="store_true", help="Check without installing an update")
    parser.add_argument("--force", action="store_true", help="Reinstall even when versions match")
    args = parser.parse_args()
    try:
        status, version = synchronize(
            args.target,
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
