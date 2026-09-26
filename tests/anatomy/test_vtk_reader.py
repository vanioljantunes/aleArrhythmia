"""Values recorded in docs/vault/literature/rodero-mesh-contents.md, measured 2026-09-25."""
import numpy as np


def test_counts(mesh):
    assert mesh.points.shape == (379158, 3)
    assert mesh.tets.shape == (1766006, 4)
    assert len(np.unique(mesh.cell_ids)) == 24


def test_bounding_box_is_an_adult_heart_in_mm(mesh):
    extent = np.ptp(mesh.points, axis=0)
    assert np.allclose(extent, [129.4, 108.1, 124.9], atol=0.1)


def test_universal_ventricular_coordinates_present(mesh):
    s = mesh.scalars
    assert set(s) == {"RHO", "PHI", "Z", "V"}
    for name in ("RHO", "Z"):
        v = s[name][s[name] != -10]
        assert v.min() >= 0.0 and abs(v.max() - 1.0) < 1e-6
    phi = s["PHI"][s["PHI"] != -10]
    assert abs(phi.min() + np.pi) < 1e-3 and abs(phi.max() - np.pi) < 1e-3
    assert set(np.unique(s["V"]).tolist()) == {-10.0, -1.0, 1.0}
