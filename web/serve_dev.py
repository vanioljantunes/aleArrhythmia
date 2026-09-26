"""Serve web/ on the loopback interface, with the rewrites the production site applies.

  /projects/ale/viewer/<file>   web/viewer/<file>, falling back to web/viewer/index.html
  /projects/ale/vendor/<file>   web/vendor/<file>
  /projects/ale/<slug>          the vault note source docs/vault/*/<slug>.md, standing in for the
                                section page feature 002 renders, so links can be checked for 200

Loopback only. Nothing is written.
"""
from __future__ import annotations

import http.server
import os
import socketserver
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VAULT = ROOT.parent / "docs" / "vault"
SECTION = "/projects/ale"
MISSING = str(ROOT / "nonexistent")
# The page links the site's own stylesheets at the root (/site-bar.css, /site.css). With a checkout
# of the site named here, root paths that web/ lacks are served from it, so the page looks as it
# will on the site. Without it, the page is unstyled but works.
SITE = Path(os.environ["ALE_SITE_ROOT"]).resolve() if os.environ.get("ALE_SITE_ROOT") else None


class Handler(http.server.SimpleHTTPRequestHandler):
    # Windows may map .js to text/plain through the registry, which blocks module scripts.
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript; charset=utf-8",
        ".mjs": "text/javascript; charset=utf-8",
        ".json": "application/json",
        ".glb": "model/gltf-binary",
        ".md": "text/markdown; charset=utf-8",
    }

    def translate_path(self, path: str) -> str:
        clean = path.split("?", 1)[0].split("#", 1)[0]
        if clean == SECTION or clean == SECTION + "/":
            return MISSING
        if clean.startswith(SECTION + "/"):
            head, _, tail = clean[len(SECTION) + 1:].partition("/")
            if head in ("viewer", "vendor"):
                if tail:
                    candidate = (ROOT / head / tail).resolve()
                    if candidate.is_file() and str(candidate).startswith(str(ROOT)):
                        return str(candidate)
                return str(ROOT / "viewer" / "index.html") if head == "viewer" else MISSING
            if head and not tail and "." not in head:
                for note in VAULT.rglob(f"{head}.md"):
                    return str(note)
            return MISSING
        candidate = (ROOT / clean.lstrip("/")).resolve()
        if not str(candidate).startswith(str(ROOT)):
            return MISSING
        if not candidate.exists() and SITE is not None:
            fallback = (SITE / clean.lstrip("/")).resolve()
            if fallback.is_file() and str(fallback).startswith(str(SITE)):
                return str(fallback)
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
        print(f"viewer on http://127.0.0.1:{port}{SECTION}/viewer/", flush=True)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
