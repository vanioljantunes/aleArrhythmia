"""Vertex clustering that respects structure boundaries and thin walls. numpy only, deterministic.

Every input vertex is assigned one cluster. A cluster is a cell of a regular grid, at a level of
refinement chosen per structure, split further by which way the surface faces there. Vertices on the
two sides of a thin wall have opposite normals and so never merge, which is what keeps a 2 mm atrial
wall from collapsing into a sheet. A triangle maps to its corners' clusters; degenerate ones vanish.
Because every vertex maps to exactly one cluster across the whole mesh, structures stay welded.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Decimated:
    positions: np.ndarray      # (V, 3) float64
    normals: np.ndarray        # (V, 3) float64, unit
    triangles: np.ndarray      # (T, 3) int32
    owner: np.ndarray          # (T,) int32, structure id per triangle
    cluster_of_input: np.ndarray  # (N,) int32, output vertex for each input vertex
    cell_size: dict[int, float]   # structure id -> cell size used, mm


def vertex_normals(points: np.ndarray, tri: np.ndarray) -> np.ndarray:
    n = np.zeros_like(points)
    fn = np.cross(points[tri[:, 1]] - points[tri[:, 0]], points[tri[:, 2]] - points[tri[:, 0]])
    for k in range(3):
        np.add.at(n, tri[:, k], fn)
    length = np.linalg.norm(n, axis=1)
    length[length == 0] = 1.0
    return n / length[:, None]


def _facing_bucket(normals: np.ndarray) -> np.ndarray:
    """Six buckets: the dominant axis of the normal and its sign."""
    axis = np.argmax(np.abs(normals), axis=1)
    sign = normals[np.arange(len(normals)), axis] >= 0
    return (axis * 2 + sign).astype(np.int64)


def decimate(points: np.ndarray, tri: np.ndarray, owner: np.ndarray,
             base_cell: float, level: dict[int, int]) -> Decimated:
    """level[id] = 0 means base_cell, 1 means base_cell / 2, and so on."""
    n_in = len(points)
    used = np.zeros(n_in, dtype=bool)
    used[tri.ravel()] = True

    # Each vertex takes the finest level of any structure whose triangle touches it.
    vlevel = np.zeros(n_in, dtype=np.int64)
    tlevel = np.array([level.get(int(o), 0) for o in owner], dtype=np.int64)
    for k in range(3):
        np.maximum.at(vlevel, tri[:, k], tlevel)

    normals_in = vertex_normals(points, tri)
    bucket = _facing_bucket(normals_in)

    origin = points.min(axis=0)
    cell = base_cell / (2.0 ** vlevel)
    ijk = np.floor((points - origin) / cell[:, None]).astype(np.int64)
    key = np.column_stack([vlevel, bucket, ijk])
    key[~used] = -1  # unused vertices share one dummy cluster that no triangle references

    uniq, inverse = np.unique(key, axis=0, return_inverse=True)
    inverse = inverse.ravel()
    n_out = len(uniq)
    positions = np.zeros((n_out, 3))
    counts = np.zeros(n_out)
    np.add.at(positions, inverse, points)
    np.add.at(counts, inverse, 1.0)
    positions /= counts[:, None]

    t = inverse[tri]
    keep = (t[:, 0] != t[:, 1]) & (t[:, 1] != t[:, 2]) & (t[:, 0] != t[:, 2])
    t, own = t[keep], owner[keep]
    # Deterministic dedupe: sort by (owner, sorted corners), keep the first of each.
    sk = np.sort(t, axis=1)
    order = np.lexsort((sk[:, 2], sk[:, 1], sk[:, 0], own))
    t, own, sk = t[order], own[order], sk[order]
    first = np.ones(len(t), dtype=bool)
    first[1:] = np.any(sk[1:] != sk[:-1], axis=1) | (own[1:] != own[:-1])
    t, own = t[first], own[first]

    # Drop output vertices no triangle references, renumbering densely.
    ref = np.zeros(n_out, dtype=bool)
    ref[t.ravel()] = True
    new_index = np.cumsum(ref) - 1
    positions = positions[ref]
    t = new_index[t]
    cluster_of_input = np.where(used, new_index[inverse], -1).astype(np.int32)

    normals = vertex_normals(positions, t)
    cell_size = {sid: base_cell / (2.0 ** level.get(sid, 0)) for sid in np.unique(owner).tolist()}
    return Decimated(positions, normals, t.astype(np.int32), own.astype(np.int32),
                     cluster_of_input, cell_size)
