"""Render web/viewer/data/heart-still.png: the loaded viewer at its reset camera, 1200 by 900.

Starts the dev server on a free port, opens the page with ?still=1, which hides everything but the
stage and fixes it at 1200 by 900, waits for the model, and screenshots the stage element.
Needs Playwright with Chromium.
"""
from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "web" / "viewer" / "data" / "heart-still.png"
ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]


def main() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    proc = subprocess.Popen([sys.executable, str(REPO / "web" / "serve_dev.py"), str(port)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        deadline = time.time() + 15
        while time.time() < deadline:
            try:
                socket.create_connection(("127.0.0.1", port), timeout=0.5).close()
                break
            except OSError:
                time.sleep(0.1)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=ARGS)
            page = browser.new_page(viewport={"width": 1400, "height": 1000}, device_scale_factor=1)
            page.goto(f"http://127.0.0.1:{port}/projects/ale/viewer/?still=1")
            page.wait_for_function("window.aleViewer && window.aleViewer.ready === true", timeout=30000)
            page.wait_for_timeout(800)
            page.locator("#stage-box").screenshot(path=str(OUT))
            browser.close()
    finally:
        proc.kill()
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
