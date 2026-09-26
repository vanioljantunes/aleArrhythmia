"""Nothing leaves, nothing persists (SC-012, SC-013, FR-013j, FR-013k)."""
from __future__ import annotations

from pathlib import Path

import pytest

from .support import EXPORT, VIEWER, load_carto, wait_ready

ROOT = Path(__file__).resolve().parents[2]

STORAGE = """async () => ({
  local: localStorage.length,
  session: sessionStorage.length,
  indexed: (await indexedDB.databases()).length,
})"""


@pytest.fixture(scope="module")
def export():
    d = ROOT / EXPORT
    if not d.exists():
        pytest.skip("porcine export not fetched; run python tests/fixtures/fetch.py")
    return d


def test_no_request_leaves_and_no_storage_is_written(server, page, export):
    requests = []
    page.on("request", lambda r: requests.append((r.url, r.method, r.post_data)))
    page.goto(server + VIEWER)
    wait_ready(page)
    seen_before = {u for u, _, _ in requests}
    assert page.evaluate(STORAGE) == {"local": 0, "session": 0, "indexed": 0}

    mark = len(requests)
    load_carto(page, export, "2-Map")
    page.wait_for_timeout(500)
    after = requests[mark:]
    for url, method, body in after:
        assert url.startswith(server), f"request left the origin: {url}"
        assert url in seen_before, f"new request after loading a study: {url}"
        assert method == "GET" and body is None, (url, method)
    assert page.evaluate(STORAGE) == {"local": 0, "session": 0, "indexed": 0}

    page.reload()
    wait_ready(page)
    assert page.evaluate(STORAGE) == {"local": 0, "session": 0, "indexed": 0}
    assert page.locator("#mode").get_attribute("data-mode") == "mean"
    for url, _, _ in requests:
        assert url.startswith(server), url
