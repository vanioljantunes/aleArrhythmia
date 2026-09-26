"""The boundary of a tetrahedral mesh: every face that belongs to exactly one tetrahedron."""
from __future__ import annotations

import numpy as np

# The four faces of a tet (a, b, c, d), each with its opposite vertex.
_FACES = ((0, 1, 2, 3), (0, 1, 3, 2), (0, 2, 3, 1), (1, 2, 3, 0))


def boundary(points: np.ndarray, tets: np.ndarray, cell_ids: np.ndarray):
    """Return (triangles (K,3) int32, owner ids (K,) int32) with outward-consistent winding."""
    faces, opposite, owner = [], [], []
    for a, b, c, d in _FACES:
        faces.append(tets[:, [a, b, c]])
        opposite.append(tets[:, d])
        owner.append(cell_ids)
    F = np.vstack(faces)
    O = np.concatenate(opposite)
    W = np.concatenate(owner)

    key = np.sort(F, axis=1)
    order = np.lexsort((key[:, 2], key[:, 1], key[:, 0]))
    key, F, O, W = key[order], F[order], O[order], W[order]
    same = np.all(key[1:] == key[:-1], axis=1)
    paired = np.zeros(len(key), dtype=bool)
    paired[:-1] |= same
    paired[1:] |= same
    tri, opp, own = F[~paired].copy(), O[~paired], W[~paired]

    # Wind each face so its normal points away from the tet's opposite vertex, that is outward.
    p0, p1, p2 = points[tri[:, 0]], points[tri[:, 1]], points[tri[:, 2]]
    normal = np.cross(p1 - p0, p2 - p0)
    inward = np.einsum("ij,ij->i", normal, points[opp] - p0) > 0
    tri[inward, 1], tri[inward, 2] = tri[inward, 2], tri[inward, 1]
    return tri.astype(np.int32), own.astype(np.int32)


def edge_share_counts(tri: np.ndarray) -> dict[int, int]:
    """How many edges are shared by 1, 2, 3, 4 ... triangles. A closed surface has only even counts."""
    e = np.sort(np.vstack([tri[:, [0, 1]], tri[:, [1, 2]], tri[:, [2, 0]]]), axis=1)
    _, counts = np.unique(e, axis=0, return_counts=True)
    vals, freq = np.unique(counts, return_counts=True)
    return dict(zip(vals.tolist(), freq.tolist()))


def signed_volume(points: np.ndarray, tri: np.ndarray) -> float:
    """Volume enclosed by an outward-wound closed surface, in the points' units cubed."""
    a, b, c = points[tri[:, 0]], points[tri[:, 1]], points[tri[:, 2]]
    return float(np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6.0)


def tet_volume(points: np.ndarray, tets: np.ndarray) -> float:
    p = points
    va, vb, vc = p[tets[:, 1]] - p[tets[:, 0]], p[tets[:, 2]] - p[tets[:, 0]], p[tets[:, 3]] - p[tets[:, 0]]
    return float(np.abs(np.einsum("ij,ij->i", va, np.cross(vb, vc))).sum() / 6.0)
