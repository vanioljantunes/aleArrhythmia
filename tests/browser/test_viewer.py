"""User story 1: the heart is on screen and moves (SC-001, SC-002, SC-007)."""
from __future__ import annotations

import re
import statistics
import time

import pytest

from .support import VIEWER, drag, gpu_name, throttle, wait_ready


def test_model_visible_within_two_seconds_at_20_mbps(server, page):
    throttle(page, 20)
    t0 = time.perf_counter()
    page.goto(server + VIEWER)
    wait_ready(page)
    elapsed = time.perf_counter() - t0
    assert page.evaluate("document.getElementById('loading').hidden") is True
    assert elapsed < 2.0, f"{elapsed:.2f} s"


def test_drag_changes_the_camera(server, page):
    page.goto(server + VIEWER)
    wait_ready(page)
    q0 = page.evaluate("aleViewer.camera.quaternion.toArray()")
    drag(page, 160, 50)
    page.wait_for_timeout(300)
    q1 = page.evaluate("aleViewer.camera.quaternion.toArray()")
    assert q0 != q1


def test_wheel_zooms_within_limits(server, page):
    page.goto(server + VIEWER)
    wait_ready(page)
    box = page.locator("#stage").bounding_box()
    page.mouse.move(box["x"] + 100, box["y"] + 100)
    d0 = page.evaluate("aleViewer.controls.getDistance()")
    for _ in range(3):
        page.mouse.wheel(0, -300)
        page.wait_for_timeout(60)
    page.wait_for_timeout(300)
    d1 = page.evaluate("aleViewer.controls.getDistance()")
    assert d1 < d0
    for _ in range(40):
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(15)
    page.wait_for_timeout(400)
    d_far = page.evaluate("aleViewer.controls.getDistance()")
    assert d_far <= page.evaluate("aleViewer.controls.maxDistance") + 1e-6
    for _ in range(80):
        page.mouse.wheel(0, -800)
        page.wait_for_timeout(15)
    page.wait_for_timeout(400)
    d_near = page.evaluate("aleViewer.controls.getDistance()")
    assert d_near >= page.evaluate("aleViewer.controls.minDistance") - 1e-6


def test_reset_restores_the_initial_camera(server, page):
    page.goto(server + VIEWER)
    wait_ready(page)
    p0 = page.evaluate("aleViewer.initial.position.toArray()")
    drag(page, 200, 120)
    page.wait_for_timeout(600)
    assert page.evaluate("aleViewer.camera.position.toArray()") != p0
    page.click("#reset")
    page.wait_for_timeout(400)
    p1 = page.evaluate("aleViewer.camera.position.toArray()")
    assert all(abs(a - b) < 1e-3 for a, b in zip(p0, p1)), (p0, p1)


def test_every_structure_toggles(server, page):
    page.goto(server + VIEWER)
    wait_ready(page)
    boxes = page.locator("#structures input[type=checkbox]")
    assert boxes.count() == 24
    for i in range(24):
        sid = boxes.nth(i).get_attribute("data-structure")
        boxes.nth(i).uncheck()
        assert page.evaluate(f"aleViewer.modes.active.model.getObjectByName('structure-{sid}').visible") is False
        boxes.nth(i).check()
        assert page.evaluate(f"aleViewer.modes.active.model.getObjectByName('structure-{sid}').visible") is True
    names = page.locator("#structures label").all_inner_texts()
    assert any("Left ventricle" in n for n in names)


def test_segment_control_and_legend(server, page):
    page.goto(server + VIEWER)
    wait_ready(page)
    assert page.locator("#legend li").count() == 17
    seg = page.evaluate("aleViewer.manifest.output.segments")
    cb = page.locator("#segments")
    if not seg["shipped"]:
        # ADR-0007: visible, not clickable, reason, date, evidence link.
        assert cb.is_disabled()
        assert cb.get_attribute("aria-disabled") == "true"
        reason = page.locator("#segments-reason").inner_text()
        assert seg["reason"] in reason
        assert re.search(r"\d{4}-\d{2}-\d{2}", reason)
        href = page.locator("#segments-reason a").get_attribute("href")
        assert page.request.get(server + href).status == 200
        return
    cb.check()
    counts = page.evaluate("aleViewer.segmentCounts()")
    assert counts["1"] > 0
    assert all(v == 0 for k, v in counts.items() if k != "1"), counts
    assert page.locator("#legend").is_visible()


def test_frame_time_while_rotating(server, page):
    page.goto(server + VIEWER)
    wait_ready(page)
    page.evaluate("aleViewer.frameTimes.length = 0")
    for _ in range(4):
        drag(page, 120, 30, steps=20)
    times = page.evaluate("aleViewer.frameTimes.slice(-120)")
    median = statistics.median(times)
    name = gpu_name(page)
    print(f"renderer {name}: median frame {median:.1f} ms over {len(times)} frames")
    software = re.search(r"SwiftShader|llvmpipe|Software", name, re.I)
    integrated = re.search(r"Intel|Iris|UHD|Radeon\(TM\) Graphics|Apple M", name)
    if software or not integrated:
        pytest.skip(f"frame time recorded ({median:.1f} ms) but asserted only on integrated graphics; renderer is {name}")
    assert median < 33.4, f"{median:.1f} ms on {name}"
