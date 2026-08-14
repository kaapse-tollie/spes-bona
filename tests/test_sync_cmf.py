import hashlib
from http.client import RemoteDisconnected
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from tools import sync_cmf


class Response:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.payload


def release_archive(version="1.63.0", extra=None):
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


def fake_opener(version="1.63.0", archive=None, digest=None):
    archive = archive if archive is not None else release_archive(version)
    digest = digest or hashlib.sha256(archive).hexdigest()
    metadata = json.dumps({
        "tag_name": version,
        "draft": False,
        "prerelease": False,
        "assets": [{
            "name": f"release-{version}.zip",
            "digest": f"sha256:{digest}",
            "browser_download_url": (
                "https://github.com/Victoria-3-Modding-Co-op/"
                f"Community-Mod-Framework/releases/download/{version}/release-{version}.zip"
            ),
        }],
    }).encode()
    calls = []

    def open_request(request, timeout=60):
        calls.append((request.full_url, timeout))
        if request.full_url == sync_cmf.LATEST_RELEASE_URL:
            return Response(metadata)
        return Response(archive)

    return open_request, calls


class CmfSynchronizationTests(unittest.TestCase):
    def test_latest_release_is_installed_even_across_minor_lines(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "Community Mod Framework"
            opener, calls = fake_opener("1.63.0")
            status, version = sync_cmf.synchronize(target, opener=opener)

            self.assertEqual(("updated", "1.63.0"), (status, version))
            metadata = json.loads((target / ".metadata/metadata.json").read_text())
            self.assertEqual("1.63.0", metadata["version"])
            self.assertEqual(2, len(calls))

    def test_current_release_queries_github_without_redownloading(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "Community Mod Framework"
            (target / ".metadata").mkdir(parents=True)
            (target / ".metadata/metadata.json").write_text(
                json.dumps({"id": sync_cmf.CMF_ID, "version": "1.63.0"})
            )
            opener, calls = fake_opener("1.63.0")

            self.assertEqual(("current", "1.63.0"), sync_cmf.synchronize(target, opener=opener))
            self.assertEqual(1, len(calls))

    def test_digest_failure_preserves_existing_install(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "Community Mod Framework"
            (target / ".metadata").mkdir(parents=True)
            marker = target / "marker.txt"
            marker.write_text("keep")
            (target / ".metadata/metadata.json").write_text(
                json.dumps({"id": sync_cmf.CMF_ID, "version": "1.61.0"})
            )
            opener, _calls = fake_opener("1.63.0", digest="0" * 64)

            with self.assertRaises(sync_cmf.SyncError):
                sync_cmf.synchronize(target, opener=opener)
            self.assertEqual("keep", marker.read_text())

    def test_unsafe_archive_is_rejected(self):
        archive = release_archive(extra=("../outside.txt", "unsafe"))
        opener, _calls = fake_opener(archive=archive)
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(sync_cmf.SyncError):
                sync_cmf.synchronize(Path(temporary) / "Community Mod Framework", opener=opener)

    def test_transient_download_disconnect_is_retried(self):
        archive = release_archive()
        opener, calls = fake_opener(archive=archive)
        disconnected = False

        def flaky_open(request, timeout=60):
            nonlocal disconnected
            if request.full_url != sync_cmf.LATEST_RELEASE_URL and not disconnected:
                disconnected = True
                raise RemoteDisconnected("retry")
            return opener(request, timeout)

        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "Community Mod Framework"
            self.assertEqual(
                ("updated", "1.63.0"),
                sync_cmf.synchronize(target, opener=flaky_open),
            )
            self.assertTrue((target / "common/example.txt").is_file())
            self.assertEqual(2, len(calls))


if __name__ == "__main__":
    unittest.main()
