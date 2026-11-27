"""Smoke test the deployed edition without accepting a stale successful HTTP response."""
from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


def check_site(url: str, tag: str, *, attempts: int = 6, delay: float = 10) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        raise ValueError("Expected an absolute HTTP(S) site URL.")
    if not re.fullmatch(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", tag):
        raise ValueError("Expected a released vX.Y tag.")
    for attempt in range(attempts):
        try:
            for path in ("", "llms.txt", "sitemap.xml", "robots.txt"):
                request = urllib.request.Request(
                    url.rstrip("/") + "/" + path,
                    headers={"Cache-Control": "no-cache", "User-Agent": "APM-book-smoke"},
                )
                with urllib.request.urlopen(request, timeout=20) as response:
                    text = response.read().decode("utf-8")
                    if response.status != 200 or not text.strip():
                        raise ValueError(f"{path or '/'} is empty or not HTTP 200.")
                    if not path and not re.search(rf"Edition {re.escape(tag)}(?![0-9.])", text):
                        raise ValueError(f"Homepage does not show Edition {tag}.")
            return
        except (urllib.error.URLError, TimeoutError, UnicodeError, ValueError) as error:
            if attempt == attempts - 1:
                raise ValueError(f"Deployed edition smoke test failed: {error}") from error
            print(f"Waiting for deployment ({attempt + 1}/{attempts}): {error}", file=sys.stderr)
            time.sleep(delay)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--tag", required=True)
    args = parser.parse_args(argv)
    try:
        check_site(args.url, args.tag)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1
    print(f"Deployed edition {args.tag} passed the smoke test.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
