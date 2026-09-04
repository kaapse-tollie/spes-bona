import hashlib
from http.client import RemoteDisconnected
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import zipfile

from tools import sync_cmf


VERSION = "1.66.0"
EXPECTED_RELEASE_SHA256 = "79dd0d434e6ffb617147ad1b91b73e6306139adfffcadf6774eeb32db3a09b8b"


class Response:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.payload


def release_archive(version=VERSION, extra=None):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w") as bundle:
        bundle.writestr(
            ".metadata/metadata.json",
            json.dumps({"id": sync_cmf.CMF_ID, "version": version}),
        )
        bundle.writestr("common/example.txt", "example")
        bundle.writestr("gui/example.gui", "example")
        if extra:
            bundle.writestr(*extra)
    return output.getvalue()


def release_json(
    version,
    digest,
    *,
    asset_name=None,
    download_url=None,
):
    asset_name = asset_name if asset_name is not None else f"release-{version}.zip"
    download_url = download_url if download_url is not None else (
        "https://github.com/Victoria-3-Modding-Co-op/"
        f"Community-Mod-Framework/releases/download/{version}/release-{version}.zip"
    )
    return json.dumps({
        "tag_name": version,
        "draft": False,
        "prerelease": False,
        "assets": [{
            "name": asset_name,
            "digest": f"sha256:{digest}",
            "browser_download_url": download_url,
        }],
    }).encode()


def fake_opener(
    *,
    requested_tag=VERSION,
    release_tag=None,
    archive=None,
    digest=None,
    asset_name=None,
    download_url=None,
):
    release_tag = release_tag if release_tag is not None else requested_tag
    archive = archive if archive is not None else release_archive(release_tag)
    digest = digest if digest is not None else hashlib.sha256(archive).hexdigest()
    metadata = release_json(
        release_tag,
        digest,
        asset_name=asset_name,
        download_url=download_url,
    )
    canonical_download_url = (
        "https://github.com/Victoria-3-Modding-Co-op/"
        f"Community-Mod-Framework/releases/download/{release_tag}/release-{release_tag}.zip"
    )
    response_download_url = download_url if download_url is not None else canonical_download_url
    calls = []

    def open_request(request, timeout=60):
        calls.append((request.full_url, timeout))
        if request.full_url in {
            sync_cmf.tagged_release_url(requested_tag),
            sync_cmf.LATEST_RELEASE_URL,
        }:
            return Response(metadata)
        if request.full_url == response_download_url:
            return Response(archive)
        raise AssertionError(f"unexpected URL {request.full_url}")

    return open_request, calls


def make_installed(target, version, *, marker=None):
    (target / ".metadata").mkdir(parents=True)
    (target / ".metadata/metadata.json").write_text(
        json.dumps({"id": sync_cmf.CMF_ID, "version": version})
    )
    (target / "common").mkdir()
    (target / "gui").mkdir()
    if marker is not None:
        (target / "marker.txt").write_text(marker)


class CmfSynchronizationTests(unittest.TestCase):
    def test_pinned_release_identity_is_exact(self):
        self.assertEqual(VERSION, sync_cmf.PINNED_TAG)
        self.assertEqual(EXPECTED_RELEASE_SHA256, sync_cmf.PINNED_SHA256)
        self.assertEqual(
            "https://api.github.com/repos/Victoria-3-Modding-Co-op/"
            "Community-Mod-Framework/releases/tags/1.66.0",
            sync_cmf.tagged_release_url(sync_cmf.PINNED_TAG),
        )

    def test_exact_tag_release_is_installed(self):
        archive = release_archive()
        digest = hashlib.sha256(archive).hexdigest()
        opener, calls = fake_opener(archive=archive, digest=digest)
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "Community Mod Framework"
            status, version = sync_cmf.synchronize(
                target,
                tag=VERSION,
                expected_sha256=digest,
                opener=opener,
            )

            self.assertEqual(("updated", VERSION), (status, version))
            metadata = json.loads((target / ".metadata/metadata.json").read_text())
            self.assertEqual(VERSION, metadata["version"])
            self.assertTrue((target / "common/example.txt").is_file())
            self.assertEqual(sync_cmf.tagged_release_url(VERSION), calls[0][0])
            self.assertNotIn(sync_cmf.LATEST_RELEASE_URL, [url for url, _timeout in calls])
            self.assertEqual(2, len(calls))

    def test_default_mode_checks_the_pinned_tag_not_latest(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "Community Mod Framework"
            make_installed(target, VERSION)
            opener, calls = fake_opener(digest=EXPECTED_RELEASE_SHA256)

            self.assertEqual(("current", VERSION), sync_cmf.synchronize(target, opener=opener))
            self.assertEqual([(sync_cmf.tagged_release_url(VERSION), 60)], calls)

    def test_exact_tag_refuses_later_release_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "Community Mod Framework"
            make_installed(target, "1.65.0", marker="keep")
            opener, calls = fake_opener(requested_tag=VERSION, release_tag="1.67.0")

            with self.assertRaisesRegex(sync_cmf.SyncError, "expected exact tag '1.66.0'"):
                sync_cmf.synchronize(
                    target,
                    tag=VERSION,
                    expected_sha256="0" * 64,
                    opener=opener,
                )

            self.assertEqual("keep", (target / "marker.txt").read_text())
            self.assertEqual([(sync_cmf.tagged_release_url(VERSION), 60)], calls)
            self.assertNotIn(sync_cmf.LATEST_RELEASE_URL, [url for url, _timeout in calls])

    def test_latest_release_requires_explicit_maintenance_mode(self):
        archive = release_archive("1.67.0")
        digest = hashlib.sha256(archive).hexdigest()
        opener, calls = fake_opener(
            requested_tag=VERSION,
            release_tag="1.67.0",
            archive=archive,
            digest=digest,
        )
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "Community Mod Framework"
            self.assertEqual(
                ("updated", "1.67.0"),
                sync_cmf.synchronize(target, latest=True, opener=opener),
            )
            self.assertEqual(sync_cmf.LATEST_RELEASE_URL, calls[0][0])

    def test_github_digest_mismatch_is_rejected_before_download(self):
        archive = release_archive()
        actual_digest = hashlib.sha256(archive).hexdigest()
        opener, calls = fake_opener(archive=archive, digest=actual_digest)
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "Community Mod Framework"
            make_installed(target, "1.65.0", marker="keep")

            with self.assertRaisesRegex(sync_cmf.SyncError, "GitHub digest"):
                sync_cmf.synchronize(
                    target,
                    tag=VERSION,
                    expected_sha256="0" * 64,
                    opener=opener,
                )

            self.assertEqual("keep", (target / "marker.txt").read_text())
            self.assertEqual(1, len(calls))

    def test_download_digest_failure_preserves_existing_install(self):
        expected_archive = release_archive()
        expected_digest = hashlib.sha256(expected_archive).hexdigest()
        opener, calls = fake_opener(
            archive=expected_archive + b"corrupt",
            digest=expected_digest,
        )
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "Community Mod Framework"
            make_installed(target, "1.65.0", marker="keep")

            with self.assertRaisesRegex(sync_cmf.SyncError, "does not match required"):
                sync_cmf.synchronize(
                    target,
                    tag=VERSION,
                    expected_sha256=expected_digest,
                    opener=opener,
                )

            self.assertEqual("keep", (target / "marker.txt").read_text())
            self.assertEqual(2, len(calls))

    def test_archive_metadata_version_mismatch_preserves_existing_install(self):
        archive = release_archive("1.67.0")
        digest = hashlib.sha256(archive).hexdigest()
        opener, _calls = fake_opener(
            requested_tag=VERSION,
            release_tag=VERSION,
            archive=archive,
            digest=digest,
        )
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "Community Mod Framework"
            make_installed(target, "1.65.0", marker="keep")

            with self.assertRaisesRegex(sync_cmf.SyncError, "metadata version 1.67.0"):
                sync_cmf.synchronize(
                    target,
                    tag=VERSION,
                    expected_sha256=digest,
                    opener=opener,
                )

            self.assertEqual("keep", (target / "marker.txt").read_text())

    def test_wrong_asset_name_is_rejected_before_download(self):
        archive = release_archive()
        digest = hashlib.sha256(archive).hexdigest()
        opener, calls = fake_opener(
            archive=archive,
            digest=digest,
            asset_name="release-1.67.0.zip",
        )
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "Community Mod Framework"
            make_installed(target, "1.65.0", marker="keep")

            with self.assertRaisesRegex(sync_cmf.SyncError, "exactly one release-1.66.0.zip"):
                sync_cmf.synchronize(
                    target,
                    tag=VERSION,
                    expected_sha256=digest,
                    opener=opener,
                )

            self.assertEqual("keep", (target / "marker.txt").read_text())
            self.assertEqual(1, len(calls))

    def test_atomic_install_failure_rolls_back_existing_install(self):
        archive = release_archive()
        digest = hashlib.sha256(archive).hexdigest()
        opener, _calls = fake_opener(archive=archive, digest=digest)
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            target = parent / "Community Mod Framework"
            make_installed(target, "1.65.0", marker="keep")
            real_rename = Path.rename

            def fail_candidate_rename(path, destination):
                if path.name == "payload" and Path(destination) == target:
                    raise OSError("simulated replacement failure")
                return real_rename(path, destination)

            with mock.patch.object(Path, "rename", new=fail_candidate_rename):
                with self.assertRaisesRegex(sync_cmf.SyncError, "previous installation was restored"):
                    sync_cmf.synchronize(
                        target,
                        tag=VERSION,
                        expected_sha256=digest,
                        opener=opener,
                    )

            self.assertEqual("keep", (target / "marker.txt").read_text())
            metadata = json.loads((target / ".metadata/metadata.json").read_text())
            self.assertEqual("1.65.0", metadata["version"])
            self.assertFalse((target / "common/example.txt").exists())
            self.assertEqual([], list(parent.glob(".cmf-update-*")))

    def test_unsafe_archive_is_rejected(self):
        archive = release_archive(extra=("../outside.txt", "unsafe"))
        digest = hashlib.sha256(archive).hexdigest()
        opener, _calls = fake_opener(archive=archive, digest=digest)
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(sync_cmf.SyncError):
                sync_cmf.synchronize(
                    Path(temporary) / "Community Mod Framework",
                    tag=VERSION,
                    expected_sha256=digest,
                    opener=opener,
                )

    def test_transient_download_disconnect_is_retried(self):
        archive = release_archive()
        digest = hashlib.sha256(archive).hexdigest()
        opener, calls = fake_opener(archive=archive, digest=digest)
        disconnected = False

        def flaky_open(request, timeout=60):
            nonlocal disconnected
            if request.full_url != sync_cmf.tagged_release_url(VERSION) and not disconnected:
                disconnected = True
                raise RemoteDisconnected("retry")
            return opener(request, timeout)

        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "Community Mod Framework"
            with mock.patch.object(sync_cmf.time, "sleep"):
                self.assertEqual(
                    ("updated", VERSION),
                    sync_cmf.synchronize(
                        target,
                        tag=VERSION,
                        expected_sha256=digest,
                        opener=flaky_open,
                    ),
                )
            self.assertTrue((target / "common/example.txt").is_file())
            self.assertEqual(2, len(calls))


if __name__ == "__main__":
    unittest.main()
