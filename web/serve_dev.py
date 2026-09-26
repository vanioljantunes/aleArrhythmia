"""Serve web/ on the loopback interface, with the rewrite the production site applies.

/projects/ale/viewer/<anything> falls back to web/viewer/index.html. Nothing is written.
"""
from __future__ import annotations

import http.server
import socketserver
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIEWER = "/projects/ale/viewer"


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        clean = path.split("?", 1)[0].split("#", 1)[0]
        if clean.startswith(VIEWER):
            rest = clean[len(VIEWER):].lstrip("/")
            candidate = (ROOT / "viewer" / rest).resolve()
            if rest and candidate.is_file() and str(candidate).startswith(str(ROOT)):
                return str(candidate)
            return str(ROOT / "viewer" / "index.html")
        candidate = (ROOT / clean.lstrip("/")).resolve()
        if not str(candidate).startswith(str(ROOT)):
            return str(ROOT / "nonexistent")
        return str(candidate)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt: str, *args) -> None:
        pass


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8788
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
        print(f"viewer on http://127.0.0.1:{port}{VIEWER}/", flush=True)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
