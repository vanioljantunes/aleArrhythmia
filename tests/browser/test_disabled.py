"""User story 4: every unavailable capability is a visible, disabled control (ADR-0007, SC-008)."""
from __future__ import annotations

import re

from .support import VIEWER, wait_ready

DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
# Stage B, CARTO verified 2026-09-25. ARGO waits for its FR-013n inspection; Affera has no format.
EXPECTED_DISABLED = {"argo", "affera"}


def test_disabled_import_controls(server, page):
    page.goto(server + VIEWER)
    wait_ready(page)
    items = page.locator("#imports .ctl-disabled")
    assert items.count() == len(EXPECTED_DISABLED)
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
    assert seen == EXPECTED_DISABLED
    assert "never uploaded or stored" in page.locator("#local-only").inner_text()


def test_live_carto_control_states_what_it_reads(server, page):
    page.goto(server + VIEWER)
    wait_ready(page)
    control = page.locator("#imports [data-control=carto]")
    assert control.locator("button#load-carto").is_enabled()
    text = control.inner_text()
    assert "Only the map shell" in text
    assert DATE.search(text)
    href = control.locator("a").get_attribute("href")
    assert page.request.get(server + href).status == 200
