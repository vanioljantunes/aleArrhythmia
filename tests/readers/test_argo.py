"""The ARGO reader against the nine patient folders (FR-013q, quickstart scenario 7)."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from tests.browser.support import VIEWER, wait_ready

ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "docs/vault/literature/argo-ventricular-tachycardia-dataset.md"
BASE = ROOT / "tests/fixtures/external/argo/annotated-dataset-of-post-ischemic-ventricular-tachycardia-electrograms-argo-1.0.0/ARGODataset_Folder"
TOTAL_MAPPED = 1962

READ = """async () => {
  const m = await import('./readers/argo.js');
  const files = document.getElementById('test-pick').files;
  const opened = [];
  const original = File.prototype.text;
  File.prototype.text = function () { opened.push(this.name); return original.call(this); };
  try {
    const s = await m.readArgo(files);
    return { label: s.label, frame: s.frame, source: s.source,
      vertices: s.geometry.positions.length / 3, triangles: s.geometry.indices.length / 3,
      maxIndex: Math.max(...s.geometry.indices), minIndex: Math.min(...s.geometry.indices),
      mapped: s.points.filter(p => p.origin === 'mapped').length,
      ablation: s.points.filter(p => p.origin === 'ablation').length,
      firstMapped: s.points[0], opened };
  } finally { File.prototype.text = original; }
}"""


@pytest.fixture(scope="module")
def patients():
    text = NOTE.read_text(encoding="utf-8")
    if "Inspection result: clear" not in text:
        pytest.skip("the FR-013n inspection result is not recorded as clear in the vault note")
    if not BASE.exists():
        pytest.skip("ARGO not fetched; run python tests/fixtures/fetch.py --argo")
    dirs = sorted(BASE.glob("Pt*"), key=lambda p: int(p.name[2:]))
    assert len(dirs) == 9
    return dirs


def attach_picker(page, directory: Path) -> None:
    page.evaluate("""() => {
      const old = document.getElementById('test-pick');
      if (old) old.remove();
      const i = document.createElement('input');
      i.type = 'file'; i.id = 'test-pick'; i.multiple = true; i.setAttribute('webkitdirectory', '');
      document.body.append(i);
    }""")
    page.set_input_files("#test-pick", str(directory))


def csv_rows(path: Path) -> int:
    return sum(1 for l in path.read_text(encoding="utf-8-sig").splitlines() if l.strip()) - 1


def test_reads_all_nine_patients(server, page, patients):
    page.goto(server + VIEWER)
    wait_ready(page)
    total = 0
    for d in patients:
        attach_picker(page, d)
        r = page.evaluate(READ)
        assert r["frame"] == "study" and r["source"] == "argo" and r["label"] == d.name
        assert r["vertices"] == csv_rows(d / "XYZmesh.txt")
        assert r["triangles"] == csv_rows(d / "ConnectivityList.txt")
        assert r["minIndex"] == 0 and r["maxIndex"] == r["vertices"] - 1, d.name
        assert r["mapped"] == csv_rows(d / "POS_POINTS.txt")
        assert r["ablation"] == csv_rows(d / "AblationPoints.txt")
        assert r["firstMapped"]["origin"] == "mapped" and re.fullmatch(r"P\d+", r["firstMapped"]["label"])
        assert "MESHcoloring.txt" not in r["opened"], r["opened"]
        assert set(r["opened"]) == {"XYZmesh.txt", "ConnectivityList.txt", "POS_POINTS.txt", "AblationPoints.txt"}
        total += r["mapped"]
    assert total == TOTAL_MAPPED


def test_loads_through_the_page_control(server, page, patients):
    page.goto(server + VIEWER)
    wait_ready(page)
    page.set_input_files("#pick-argo", str(patients[0]))
    page.wait_for_function("document.getElementById('mode').dataset.mode === 'patient'", timeout=20000)
    assert page.locator("#mode").inner_text() == "Patient: Pt1, this study's own frame"
    study = page.evaluate("aleViewer.modes.active.study")
    assert study["source"] == "argo" and study["mapped"] == csv_rows(patients[0] / "POS_POINTS.txt")
    page.click("#close-study button")
    page.wait_for_function("document.getElementById('mode').dataset.mode === 'mean'")
