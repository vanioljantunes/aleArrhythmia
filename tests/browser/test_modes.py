"""User story 5: the two modes never mix (SC-014, SC-015, FR-013a to FR-013e)."""
from __future__ import annotations

from pathlib import Path

import pytest

from .support import EXPORT, VIEWER, load_carto, wait_ready

ROOT = Path(__file__).resolve().parents[2]
ATTACHED = "aleViewer.scene.children.filter(c => c.name === 'mean' || c.name === 'patient').map(c => c.name)"


@pytest.fixture(scope="module")
def export():
    d = ROOT / EXPORT
    if not d.exists():
        pytest.skip("porcine export not fetched; run python tests/fixtures/fetch.py")
    return d


def add_point(page, x, y, z):
    page.fill("#cx", str(x))
    page.fill("#cy", str(y))
    page.fill("#cz", str(z))
    page.click("#add-point")


def test_study_loads_and_the_mean_is_detached(server, page, export):
    page.goto(server + VIEWER)
    wait_ready(page)
    add_point(page, 1, 2, 3)
    assert page.locator("#points li").count() == 1

    load_carto(page, export, "2-Map")
    assert page.locator("#mode").inner_text() == "Patient: 2-Map, this study's own frame"
    assert page.evaluate("aleViewer.modes.active.kind") == "patient"
    assert page.evaluate("aleViewer.modes.inactive().group.children.length") == 0
    assert page.evaluate("aleViewer.modes.active.group.children.length") > 0
    assert page.evaluate(ATTACHED) == ["patient"]
    assert page.evaluate("aleViewer.modes.active.study") == {"source": "carto", "label": "2-Map", "mapped": 2, "ablation": 22}
    assert page.locator("#points li").count() == 0
    assert "study's own frame" in page.locator("#frame-label").inner_text()
    assert page.locator("#segments").is_disabled()

    # Close: back to the mean with its typed point intact, and the study gone.
    page.click("#close-study button")
    page.wait_for_function("document.getElementById('mode').dataset.mode === 'mean'")
    assert page.locator("#mode").inner_text() == "Population mean"
    assert page.locator("#points li").count() == 1
    assert page.evaluate("aleViewer.modes.patient") is None
    assert page.evaluate(ATTACHED) == ["mean"]
    assert page.locator("#structures input[type=checkbox]").count() == 24

    # Reload: the mean, with no points.
    page.reload()
    wait_ready(page)
    assert page.locator("#mode").get_attribute("data-mode") == "mean"
    assert page.locator("#points li").count() == 0


def test_folder_without_a_mesh_leaves_the_mode_unchanged(server, page, tmp_path):
    (tmp_path / "notes.txt").write_text("nothing here", encoding="utf-8")
    page.goto(server + VIEWER)
    wait_ready(page)
    page.set_input_files("#pick-carto", str(tmp_path))
    page.wait_for_selector("#error:not([hidden])")
    text = page.locator("#error").inner_text()
    assert ".mesh" in text and "unchanged" in text
    assert page.locator("#mode").get_attribute("data-mode") == "mean"
    assert page.evaluate("aleViewer.modes.patient") is None
