"""Starts the dev server once and hands out Playwright pages. Skips cleanly without Playwright."""
from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

pytest.importorskip("playwright")
from playwright.sync_api import sync_playwright  # noqa: E402

from .support import CHROMIUM_ARGS  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture(scope="session")
def server():
    port = _free_port()
    proc = subprocess.Popen([sys.executable, str(ROOT / "web" / "serve_dev.py"), str(port)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.time() + 15
    while time.time() < deadline:
        try:
            socket.create_connection(("127.0.0.1", port), timeout=0.5).close()
            break
        except OSError:
            time.sleep(0.1)
    else:
        proc.kill()
        raise RuntimeError("dev server did not start")
    yield f"http://127.0.0.1:{port}"
    proc.kill()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=CHROMIUM_ARGS)
        yield b
        b.close()


@pytest.fixture
def context(browser):
    c = browser.new_context(viewport={"width": 1200, "height": 900})
    yield c
    c.close()


@pytest.fixture
def page(context):
    return context.new_page()
