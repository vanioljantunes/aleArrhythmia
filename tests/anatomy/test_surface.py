import numpy as np

from tools.anatomy.surface import edge_share_counts, signed_volume, tet_volume


def test_boundary_triangle_count(surface):
    tri, _ = surface
    assert len(tri) == 334550


def test_every_structure_reaches_the_surface(surface):
    _, own = surface
    assert set(np.unique(own).tolist()) == set(range(1, 25))


def test_surface_is_closed(surface):
    # Closed means every edge is shared an even number of times. This mesh has 64 edges where the
    # surface pinches against itself (shared by four triangles); recorded in the vault, not a defect.
    tri, _ = surface
    counts = edge_share_counts(tri)
    assert all(k % 2 == 0 for k in counts), counts
    assert counts.get(2, 0) > 500000


def test_winding_is_outward(mesh, surface):
    # For a consistently outward-wound closed surface the enclosed signed volume equals the tissue
    # volume summed over the tetrahedra. Endocardial faces point into the cavities, which is still
    # out of the tissue, so a centroid test would be wrong here; the volume test is exact.
    tri, _ = surface
    ratio = signed_volume(mesh.points, tri) / tet_volume(mesh.points, mesh.tets)
    assert abs(ratio - 1.0) < 1e-3
