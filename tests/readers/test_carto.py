"""The CARTO reader against the porcine export (FR-013q, quickstart scenario 7)."""
from __future__ import annotations

from pathlib import Path

import pytest

from tests.browser.support import EXPORT, VIEWER, wait_ready

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {"1-Map": (3513, 0), "1-1-ReMap": (3513, 0), "2-Map": (2916, 2), "3-Map": (2083, 0)}
ABLATION_SITES = 22

READ_ALL = """async () => {
  const m = await import('./readers/carto.js');
  const files = document.getElementById('test-pick').files;
  const out = { maps: m.listMaps(files), studies: {} };
  for (const name of out.maps) {
    const s = await m.readCarto(files, name);
    out.studies[name] = {
      frame: s.frame, source: s.source, label: s.label,
      vertices: s.geometry.positions.length / 3, triangles: s.geometry.indices.length / 3,
      first: Array.from(s.geometry.positions.slice(0, 9)),
      mapped: s.points.filter(p => p.origin === 'mapped').map(p => [p.label, p.position]),
      ablation: s.points.filter(p => p.origin === 'ablation').length,
    };
  }
  return out;
}"""


@pytest.fixture(scope="module")
def export():
    d = ROOT / EXPORT
    if not d.exists():
        pytest.skip("porcine export not fetched; run python tests/fixtures/fetch.py")
    return d


def first_vertices(mesh: Path, n: int = 3) -> list[float]:
    out = []
    in_section = False
    for line in mesh.read_text(encoding="latin-1").splitlines():
        if line.startswith("[VerticesSection]"):
            in_section = True
            continue
        if in_section and "=" in line:
            out.extend(float(x) for x in line.split("=")[1].split()[:3])
            if len(out) >= 3 * n:
                break
    return out


def car_points(car: Path) -> list[tuple[str, list[float]]]:
    out = []
    for line in car.read_text(encoding="latin-1").splitlines():
        if line.startswith("P"):
            f = line.split()
            out.append((f"P{f[2]}", [float(f[4]), float(f[5]), float(f[6])]))
    return out


def attach_picker(page, directory: Path) -> None:
    page.evaluate("""() => {
      const i = document.createElement('input');
      i.type = 'file'; i.id = 'test-pick'; i.multiple = true; i.setAttribute('webkitdirectory', '');
      document.body.append(i);
    }""")
    page.set_input_files("#test-pick", str(directory))


def test_reads_every_map_of_the_porcine_export(server, page, export):
    page.goto(server + VIEWER)
    wait_ready(page)
    attach_picker(page, export)
    result = page.evaluate(READ_ALL)
    assert sorted(result["maps"]) == sorted(EXPECTED)
    for name, (n_vertices, n_points) in EXPECTED.items():
        s = result["studies"][name]
        assert s["frame"] == "study" and s["source"] == "carto" and s["label"] == name
        assert s["vertices"] == n_vertices, name
        assert s["triangles"] == 2 * n_vertices - 4, name
        assert len(s["mapped"]) == n_points, name
        assert s["ablation"] == ABLATION_SITES, name
        expected_first = first_vertices(export / f"{name}.mesh")
        assert all(abs(a - b) < 1e-3 for a, b in zip(s["first"], expected_first)), name
    got = [(lbl, [round(v, 4) for v in pos]) for lbl, pos in result["studies"]["2-Map"]["mapped"]]
    want = [(lbl, [round(v, 4) for v in pos]) for lbl, pos in car_points(export / "2-Map_car.txt")]
    assert got == want


def test_names_what_is_missing(server, page, tmp_path):
    (tmp_path / "1-Map.mesh").write_text("#TriangulatedMeshVersion2.0\n[GeneralAttributes]\nNumVertex = 1\n", encoding="utf-8")
    page.goto(server + VIEWER)
    wait_ready(page)
    attach_picker(page, tmp_path)
    message = page.evaluate("""async () => {
      const m = await import('./readers/carto.js');
      const files = document.getElementById('test-pick').files;
      try { await m.readCarto(files, '1-Map'); return 'no error'; }
      catch (e) { return e.name + ': ' + e.message; }
    }""")
    assert message.startswith("ReadError:")
    assert "expected" in message and "1-Map_car.txt" in message
