from __future__ import annotations

import functools
import http.server
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_site import check_site


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class DeploySmokeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for path in ("index.html", "llms.txt", "sitemap.xml", "robots.txt"):
            (self.root / path).write_text("Edition v1.2", encoding="utf-8")
        self.server = http.server.ThreadingHTTPServer(
            ("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(self.root))
        )
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        self.addCleanup(self.stop)
        self.url = f"http://127.0.0.1:{self.server.server_port}"

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def test_cli_checks_the_released_edition_and_public_files(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_site.py"),
             "--url", self.url, "--tag", "v1.2"],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Deployed edition v1.2 passed", result.stdout)

    def test_stale_edition_missing_and_empty_assets_fail(self):
        for path, content in [("index.html", "Edition v1.20"), ("robots.txt", ""), ("llms.txt", None)]:
            with self.subTest(path=path):
                file = self.root / path
                if content is None:
                    file.unlink()
                else:
                    file.write_text(content, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "smoke test failed"):
                    check_site(self.url, "v1.2", attempts=1, delay=0)
                file.write_text("Edition v1.2", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
