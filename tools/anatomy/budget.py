"""Choose a base cell size and per-structure refinement so that every structure keeps at least
MIN_TRIANGLES and the whole mesh stays under MAX_TRIANGLES. Raises BudgetConflict when both cannot
hold, naming the structure, so the conflict is recorded rather than resolved silently (SC-003a).
"""
from __future__ import annotations

import numpy as np

from .decimate import Decimated, decimate

MAX_TRIANGLES = 60000
MIN_TRIANGLES = 150
MAX_LEVEL = 3
MAX_ROUNDS = 40


class BudgetConflict(Exception):
    pass


def per_structure_counts(d: Decimated) -> dict[int, int]:
    ids, counts = np.unique(d.owner, return_counts=True)
    return dict(zip(ids.tolist(), counts.tolist()))


def fit(points: np.ndarray, tri: np.ndarray, owner: np.ndarray,
        start_cell: float = 2.0) -> tuple[Decimated, float, dict[int, int]]:
    base = start_cell
    level: dict[int, int] = {}
    ids = np.unique(owner).tolist()
    for _ in range(MAX_ROUNDS):
        d = decimate(points, tri, owner, base, level)
        counts = per_structure_counts(d)
        total = len(d.triangles)
        small = [s for s in ids if counts.get(s, 0) < MIN_TRIANGLES]
        if small:
            stuck = [s for s in small if level.get(s, 0) >= MAX_LEVEL]
            if stuck:
                raise BudgetConflict(
                    f"structure {stuck[0]} keeps {counts.get(stuck[0], 0)} triangles at the finest "
                    f"level; cannot reach {MIN_TRIANGLES} inside a {MAX_TRIANGLES} budget")
            for s in small:
                level[s] = level.get(s, 0) + 1
            continue
        if total > MAX_TRIANGLES:
            base *= 1.08
            continue
        return d, base, level
    raise BudgetConflict("no cell size satisfied both limits within the round limit")
