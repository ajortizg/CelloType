"""Exercise downloads against a local HTTP server; no Zenodo traffic or ML deps."""

import hashlib
import importlib.util
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("resource_download", Path(__file__).parents[1] / "download.py")
downloader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(downloader)

PAYLOAD = b"cellotype-download-test\n" * 10000


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        self.server.requests.append(self.headers.get("Range"))
        mode = self.server.mode
        if mode == "unavailable_once" and len(self.server.requests) == 1:
            self.send_error(503)
            return
        payload = b"x" * len(PAYLOAD) if mode == "corrupt" else PAYLOAD
        start = 0
        if self.headers.get("Range") and mode != "ignore_range":
            start = int(self.headers["Range"].split("=")[1].split("-")[0])
            self.send_response(206)
            self.send_header("Content-Range", "bytes {}-{}/{}".format(start, len(payload) - 1, len(payload)))
        else:
            self.send_response(200)
        self.send_header("Content-Length", str(len(payload) - start))
        self.end_headers()
        if mode == "truncate_once" and len(self.server.requests) == 1:
            self.wfile.write(payload[:10000])
            self.close_connection = True
        else:
            self.wfile.write(payload[start:])


class DownloadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.mode = "normal"
        self.server.requests = []
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = "http://127.0.0.1:{}".format(self.server.server_port)
        self.assets = patch.dict(downloader.ASSETS, {"sample.pth": {
            "path": "models/sample.pth", "bytes": len(PAYLOAD),
            "sha256": hashlib.sha256(PAYLOAD).hexdigest(),
        }}, clear=True)
        self.assets.start()
        self.sleep = patch.object(downloader.time, "sleep", return_value=None)
        self.sleep.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.assets.stop()
        self.sleep.stop()
        self.temp.cleanup()

    def download(self, attempts=3):
        return downloader.download_asset("sample.pth", self.root, self.base_url, attempts)

    def partial(self, content):
        path = self.root / "models/sample.pth.part"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def test_download_and_reuse_verified_file(self):
        path = self.download()
        self.assertEqual(path.read_bytes(), PAYLOAD)
        self.assertEqual(self.download(), path)
        self.assertEqual(len(self.server.requests), 1)

    def test_resume_partial_file(self):
        partial = self.partial(PAYLOAD[:10000])
        self.assertEqual(self.download().read_bytes(), PAYLOAD)
        self.assertEqual(self.server.requests, ["bytes=10000-"])
        self.assertFalse(partial.exists())

    def test_server_ignoring_range_restarts_without_duplicate_bytes(self):
        self.server.mode = "ignore_range"
        self.partial(PAYLOAD[:10000])
        self.assertEqual(self.download().read_bytes(), PAYLOAD)

    def test_interrupted_response_resumes_on_retry(self):
        self.server.mode = "truncate_once"
        self.assertEqual(self.download().read_bytes(), PAYLOAD)
        self.assertEqual(self.server.requests, [None, "bytes=10000-"])

    def test_temporary_server_error_retries(self):
        self.server.mode = "unavailable_once"
        self.assertEqual(self.download().read_bytes(), PAYLOAD)
        self.assertEqual(len(self.server.requests), 2)

    def test_bad_checksum_does_not_replace_existing_file(self):
        self.server.mode = "corrupt"
        path = self.root / "models/sample.pth"
        path.parent.mkdir()
        path.write_bytes(b"existing file")
        with self.assertRaises(RuntimeError):
            self.download(attempts=2)
        self.assertEqual(path.read_bytes(), b"existing file")
        self.assertFalse(path.with_suffix(".pth.part").exists())

    def test_complete_partial_file_is_verified_without_network(self):
        self.partial(PAYLOAD)
        self.assertEqual(self.download().read_bytes(), PAYLOAD)
        self.assertEqual(self.server.requests, [])


if __name__ == "__main__":
    unittest.main()
