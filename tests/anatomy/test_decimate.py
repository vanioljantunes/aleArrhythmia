import numpy as np
import pytest

from tools.anatomy.budget import MAX_TRIANGLES, MIN_TRIANGLES, BudgetConflict, fit, per_structure_counts
from tools.anatomy.decimate import decimate
from tools.anatomy.surface import signed_volume, tet_volume


@pytest.fixture(scope="session")
def fitted(mesh, surface):
    tri, own = surface
    return fit(mesh.points, tri, own)


def test_total_within_budget(fitted):
    d, _, _ = fitted
    assert len(d.triangles) <= MAX_TRIANGLES


def test_every_structure_keeps_its_minimum(fitted):
    d, _, _ = fitted
    counts = per_structure_counts(d)
    assert set(counts) == set(range(1, 25))
    assert min(counts.values()) >= MIN_TRIANGLES, counts


def test_fits_uint16_indices(fitted):
    d, _, _ = fitted
    assert len(d.positions) < 65536


def test_volume_is_preserved(mesh, fitted):
    d, _, _ = fitted
    ratio = signed_volume(d.positions, d.triangles) / tet_volume(mesh.points, mesh.tets)
    assert abs(ratio - 1.0) < 0.01


def test_deterministic(mesh, surface, fitted):
    tri, own = surface
    d, base, level = fitted
    again = decimate(mesh.points, tri, own, base, level)
    assert np.array_equal(d.positions, again.positions)
    assert np.array_equal(d.triangles, again.triangles)
    assert np.array_equal(d.owner, again.owner)


def test_budget_conflict_is_raised_not_hidden():
    # Two structures, one of them a single triangle. It can never reach MIN_TRIANGLES.
    pts = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]], dtype=float)
    tri = np.array([[0, 1, 2], [1, 3, 2]], dtype=np.int32)
    own = np.array([1, 2], dtype=np.int32)
    with pytest.raises(BudgetConflict):
        fit(pts, tri, own, start_cell=0.5)
