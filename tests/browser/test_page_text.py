"""User story 2: the reader knows what they are looking at, with and without scripting."""
from __future__ import annotations

import pytest

from .support import VIEWER, wait_ready

STATEMENTS = [
    "research tool, not a medical device",
    "No canonical reference space has been chosen",
    "population mean",
    "Nothing shown encodes a measurement or a statistical result",
    "read in this browser and never uploaded or stored",
    "10.5281/zenodo.4593739",
    "CC BY 4.0",
    "Rodero C, Strocchi M",
]


def test_readable_without_scripting(server, browser):
    ctx = browser.new_context(java_script_enabled=False, viewport={"width": 1200, "height": 900})
    page = ctx.new_page()
    page.goto(server + VIEWER)
    text = page.locator("main").inner_text()
    for s in STATEMENTS:
        assert s in text, s
    # With scripting off the noscript block is parsed as markup, so its image is the visible one.
    still = page.locator("noscript img[src$='heart-still.png']")
    assert still.is_visible()
    assert page.request.get(server + VIEWER + "data/heart-still.png").status == 200
    href = page.locator("a[href^='https://doi.org/']").first.get_attribute("href")
    try:
        status = page.request.get(href, max_redirects=10).status
    except Exception as e:  # no network in this environment
        pytest.skip(f"DOI link not checked, no network: {e}")
    assert status == 200, href
    ctx.close()


def test_still_present_with_scripting(server, page):
    page.goto(server + VIEWER)
    wait_ready(page)
    text = page.locator("main").inner_text()
    for s in STATEMENTS:
        assert s in text, s
    assert page.locator("#mode").inner_text() == "Population mean"
