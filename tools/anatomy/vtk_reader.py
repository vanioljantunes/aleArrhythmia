"""Read the source VTK 3.0 ASCII unstructured grid into numpy arrays. numpy only.

The file is large (187 MB) and line oriented. Sections are located by their header keyword and the
numbers under each are parsed with numpy from the joined text, which is far faster than loadtxt.
"""
from __future__ import annotations

import tarfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class Mesh:
    points: np.ndarray        # (N, 3) float64, mm
    tets: np.ndarray          # (M, 4) int32
    cell_ids: np.ndarray      # (M,) int32, the structure of each tetrahedron
    scalars: dict[str, np.ndarray]  # per point, float64; -10 is the source's undefined sentinel


def _numbers(lines: list[str], dtype) -> np.ndarray:
    return np.fromstring(" ".join(lines), sep=" ", dtype=dtype)


def read_vtk(path: Path) -> Mesh:
    text = Path(path).read_text(encoding="ascii")
    lines = text.split("\n")
    n = len(lines)
    i = 0
    points = tets = cell_ids = None
    scalars: dict[str, np.ndarray] = {}
    section, cell_count, point_count = "", 0, 0
    while i < n:
        head = lines[i].split()
        if not head:
            i += 1
            continue
        key = head[0]
        if key == "POINTS":
            count = int(head[1])
            points = _numbers(lines[i + 1:i + 1 + count], np.float64).reshape(count, 3)
            i += 1 + count
        elif key == "CELLS":
            count = int(head[1])
            raw = _numbers(lines[i + 1:i + 1 + count], np.int32).reshape(count, 5)
            if not np.all(raw[:, 0] == 4):
                raise ValueError("expected a purely tetrahedral grid")
            tets = raw[:, 1:].copy()
            i += 1 + count
        elif key == "CELL_TYPES":
            i += 1 + int(head[1])
        elif key == "CELL_DATA":
            section, cell_count = "cell", int(head[1])
            i += 1
        elif key == "POINT_DATA":
            section, point_count = "point", int(head[1])
            i += 1
        elif key == "SCALARS":
            name = head[1]
            i += 2  # the LOOKUP_TABLE line follows the header
            count = cell_count if section == "cell" else point_count
            values = _numbers(lines[i:i + count], np.float64)
            if section == "cell":
                cell_ids = values.astype(np.int32)
            else:
                scalars[name.replace(".dat", "")] = values
            i += count
        else:
            i += 1
    if points is None or tets is None or cell_ids is None:
        raise ValueError("file lacks POINTS, CELLS or a cell scalar")
    return Mesh(points=points, tets=tets, cell_ids=cell_ids, scalars=scalars)


def read_source(archive: Path, workdir: Path | None = None) -> Mesh:
    """Read average.vtk out of average.tar.gz, extracting beside the archive if needed."""
    archive = Path(archive)
    workdir = Path(workdir) if workdir else archive.parent
    vtk = workdir / "average.vtk"
    if not vtk.exists():
        with tarfile.open(archive) as t:
            t.extract("average.vtk", workdir, filter="data")
    return read_vtk(vtk)
