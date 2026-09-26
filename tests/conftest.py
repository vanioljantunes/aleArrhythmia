"""Make the repository root importable, and hold the browser fixtures once for every test directory.

The browser fixtures need Playwright. They import it lazily, so the vaultcheck and anatomy tests
run without it, and the directories that need it skip themselves in their own conftest.
"""

import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CHROMIUM_ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture(scope="session")
def server():
    """The loopback dev server on a free port, for the whole session."""
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
    playwright = pytest.importorskip("playwright.sync_api")
    with playwright.sync_playwright() as p:
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
