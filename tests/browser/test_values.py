"""A study's own values on the study's own geometry (FR-006a, ADR-0010)."""
from __future__ import annotations

from pathlib import Path

import pytest

from .support import EXPORT, VIEWER, load_carto, wait_ready

ROOT = Path(__file__).resolve().parents[2]
ARGO_PT1 = ROOT / "tests/fixtures/external/argo/annotated-dataset-of-post-ischemic-ventricular-tachycardia-electrograms-argo-1.0.0/ARGODataset_Folder/Pt1"


def test_control_absent_on_the_mean_and_file_opened_only_on_demand(server, page):
    if not ARGO_PT1.exists():
        pytest.skip("ARGO not fetched")
    requests = []
    page.on("request", lambda r: requests.append(r.url))
    page.goto(server + VIEWER)
    wait_ready(page)
    assert page.locator("#values-box").is_hidden()
    page.evaluate("""() => { window.__opened = []; const o = File.prototype.text;
      File.prototype.text = function () { window.__opened.push(this.name); return o.call(this); }; }""")
    page.set_input_files("#pick-argo", str(ARGO_PT1))
    page.wait_for_function("document.getElementById('mode').dataset.mode === 'patient'", timeout=20000)
    assert page.locator("#values-box").is_visible()
    assert "MESHcoloring.txt" not in page.evaluate("window.__opened")
    assert page.evaluate("aleViewer.modes.active.model.children[0].material.vertexColors") is False
    mark = len(requests)
    page.check("#value-on")
    page.wait_for_function("!document.getElementById('value-bar').hidden", timeout=10000)
    assert "MESHcoloring.txt" in page.evaluate("window.__opened")
    assert page.evaluate("aleViewer.modes.active.model.children[0].material.vertexColors") is True
    label = page.locator("#value-bar-label").inner_text()
    assert "mV" in label and "MESHcoloring.txt" in label and "Pt1" in label and "Not a result of this project" in label
    assert requests[mark:] == []
    page.uncheck("#value-on")
    assert page.evaluate("aleViewer.modes.active.model.children[0].material.vertexColors") is False
    page.click("#close-study button")
    page.wait_for_function("document.getElementById('mode').dataset.mode === 'mean'")
    assert page.locator("#values-box").is_hidden()
    assert page.evaluate("aleViewer.modes.active.model.children.every(m => m.material.vertexColors === false)")


def test_carto_values_colour_points_not_shell(server, page):
    export = ROOT / EXPORT
    if not export.exists():
        pytest.skip("porcine export not fetched")
    page.goto(server + VIEWER)
    wait_ready(page)
    load_carto(page, export, "2-Map")
    assert "per mapped point" in page.locator("#value-note").inner_text()
    page.check("#value-on")
    page.wait_for_function("!document.getElementById('value-bar').hidden", timeout=10000)
    assert page.evaluate("aleViewer.modes.active.model.children[0].material.vertexColors") is False
    colours = page.evaluate("aleViewer.modes.active.studyPoints.filter(s => s.userData.origin === 'mapped').map(s => s.material.color.getHex())")
    assert len(colours) == 2 and colours[0] != colours[1]
    label = page.locator("#value-bar-label").inner_text()
    assert "0.02" in label and "0.03" in label and "2-Map_car.txt" in label


def test_standard_views_live_on_carto_disabled_on_argo(server, page):
    export = ROOT / EXPORT
    if not export.exists() or not ARGO_PT1.exists():
        pytest.skip("fixtures not fetched")
    page.goto(server + VIEWER)
    wait_ready(page)
    page.check("#maplook")
    assert page.locator("#orient button[data-view=AP]").is_enabled()
    load_carto(page, export, "2-Map")
    assert page.locator("#orient button[data-view=LAO]").is_enabled()
    p0 = page.evaluate("aleViewer.camera.position.toArray()")
    page.click("#orient button[data-view=LAO]")
    page.wait_for_timeout(200)
    assert page.evaluate("aleViewer.camera.position.toArray()") != p0
    page.click("#close-study button")
    page.wait_for_function("document.getElementById('mode').dataset.mode === 'mean'")
    page.set_input_files("#pick-argo", str(ARGO_PT1))
    page.wait_for_function("document.getElementById('mode').dataset.mode === 'patient'", timeout=20000)
    assert page.locator("#orient button[data-view=AP]").get_attribute("aria-disabled") == "true"
    assert "states no patient frame" in page.locator("#orient-reason").inner_text()
