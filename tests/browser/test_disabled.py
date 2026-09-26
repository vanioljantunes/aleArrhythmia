"""User story 4: every unavailable capability is a visible, disabled control (ADR-0007, SC-008)."""
from __future__ import annotations

import re

from .support import VIEWER, wait_ready

DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def test_disabled_import_controls(server, page):
    page.goto(server + VIEWER)
    wait_ready(page)
    items = page.locator("#imports .ctl-disabled")
    assert items.count() == 3
    seen = set()
    for i in range(items.count()):
        item = items.nth(i)
        seen.add(item.get_attribute("data-control"))
        button = item.locator("button")
        assert button.get_attribute("aria-disabled") == "true"
        assert button.is_disabled()
        text = item.inner_text()
        assert "Not available:" in text
        assert DATE.search(text), text
        href = item.locator("a").get_attribute("href")
        assert page.request.get(server + href).status == 200, href
        button.dispatch_event("click")
        assert page.locator("#mode").get_attribute("data-mode") == "mean"
    assert seen == {"carto", "argo", "affera"}
    assert "never uploaded or stored" in page.locator("#local-only").inner_text()
