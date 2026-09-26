"""The insertion check from research R-004, on the real mesh (FR-025, FR-026)."""
import numpy as np
import pytest

from tools.anatomy.segments import TOLERANCE_DEG, derive


@pytest.fixture(scope="session")
def derived(mesh):
    return derive(mesh.points, mesh.scalars)


def test_all_seventeen_segments_present(derived):
    seg, _ = derived
    assert set(np.unique(seg).tolist()) == set(range(0, 18))


def test_only_left_ventricle_is_segmented(mesh, derived):
    seg, _ = derived
    v = mesh.scalars["V"]
    assert np.all(seg[v != -1.0] == 0)
    assert np.all(seg[(v == -1.0) & (mesh.scalars["Z"] != -10)] > 0)


def test_two_bands_of_similar_size(derived):
    _, r = derived
    small, big = sorted(r.band_sizes)
    assert small > 500
    assert small / big > 0.3, r.band_sizes


def test_origin_is_the_anterior_insertion(derived):
    _, r = derived
    assert r.boundary_1_2_deg == r.insertion_anterior_deg == r.origin_deg


def test_septal_arc_is_the_shorter_one(derived):
    _, r = derived
    assert r.septal_arc_deg < 180


def test_insertion_check_is_reported_honestly(derived):
    # The 3/4 boundary must sit within tolerance of the inferior insertion. When it does not, the
    # report must say fail with the measured gap, not pass quietly (FR-026).
    _, r = derived
    if r.boundary_3_4_offset_deg <= TOLERANCE_DEG:
        assert r.check == "pass"
    else:
        assert r.check == "fail"
        assert f"{r.boundary_3_4_offset_deg:.1f}" in r.reason


def test_measured_angles_match_the_vault(derived):
    # Recorded 2026-09-25 in docs/vault/literature/rodero-mesh-contents.md: insertion peaks near
    # -45 and +90 degrees of PHI.
    _, r = derived
    lo, hi = sorted([r.insertion_anterior_deg, r.insertion_inferior_deg])
    assert -70 < lo < -20
    assert 65 < hi < 115
