"""Anonymous, loopback-only read fixture for APM 0.31.0. No publication endpoint.

Requires Python 3.10+ and PyYAML 6. Tested with Python 3.12.10 / PyYAML 6.0.3.
The deterministic ZIP bytes correspond to the committed genuine lockfiles.
Use verify.py to opt into registries in a disposable HOME, not your real config.
"""
from __future__ import annotations

import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import threading
from urllib.parse import urlsplit
import zipfile

import yaml


def package_bytes(name: str, version: str, base: str) -> bytes:
    manifest = {"name": name, "version": version, "dependencies": {}}
    if name == "parent":
        manifest["registries"] = {"fixture": {"url": base}, "default": "fixture"}
        manifest["dependencies"] = {
            "apm": [{
                "registry": "fixture",
                "id": "operations/leaf",
                "version": ">=1.0.0" if version == "1.0.0" else ">=1.1.0",
            }]
        }
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for filename, text in [
            ("apm.yml", yaml.safe_dump(manifest, sort_keys=False)),
            (
                f".apm/instructions/{name}.instructions.md",
                f"---\napplyTo: '**'\n---\n# Registry fixture\n\nInert {name} version {version} review guidance.\n",
            ),
        ]:
            info = zipfile.ZipInfo(filename, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, text)
    return stream.getvalue()


class RegistryFixture:
    """Serve only fixed inert fixtures. Unknown routes return 404; no PUT/POST."""

    def __init__(self, port: int = 18431):
        self.requests = []
        self.published = {name: ["1.0.0"] for name in ["exact", "other", "range", "parent", "leaf"]}
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                path = urlsplit(self.path).path
                # Never retain credential values, even accidentally supplied ones.
                outer.requests.append({"path": path, "authorization_present": bool(self.headers.get("Authorization"))})
                if self.headers.get("Authorization"):
                    self.send_error(400, "This fixture accepts anonymous requests only")
                    return
                parts = path.strip("/").split("/")
                body, mime = None, "application/json"
                if len(parts) >= 5 and parts[:3] == ["v1", "packages", "operations"]:
                    name = parts[3]
                    if name in outer.published and parts[4] == "versions":
                        if len(parts) == 5:
                            value = {
                                "package": "operations/" + name,
                                "versions": [
                                    {
                                        "version": version,
                                        "digest": "sha256:" + hashlib.sha256(outer.packages[name, version]).hexdigest(),
                                        "published_at": "2026-09-15T00:00:00Z",
                                        "size_bytes": len(outer.packages[name, version]),
                                    }
                                    for version in outer.published[name]
                                ],
                            }
                            body = json.dumps(value).encode("utf-8")
                        elif len(parts) == 7 and parts[6] == "download":
                            body = outer.packages.get((name, parts[5]))
                            mime = "application/zip"
                if body is None:
                    self.send_error(404, "No such fixture")
                    return
                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
        self.base = f"http://127.0.0.1:{self.server.server_port}"
        self.packages = {
            (name, version): package_bytes(name, version, self.base)
            for name in self.published
            for version in ["1.0.0", "1.1.0", "2.0.0-beta.1"]
        }
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def advance(self):
        for name in self.published:
            self.published[name] = ["1.0.0", "1.1.0"]
            if name not in ["parent", "leaf"]:
                self.published[name].append("2.0.0-beta.1")

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *_):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all-versions", action="store_true")
    args = parser.parse_args()
    with RegistryFixture() as fixture:
        if args.all_versions:
            fixture.advance()
        print(f"Anonymous fixture at {fixture.base}; stop with Ctrl+C. No publication endpoint.", flush=True)
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            pass
