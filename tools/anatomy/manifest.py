"""The manifest that ships beside heart.glb; shape in contracts/geometry-manifest.md."""
from __future__ import annotations

import hashlib
import json
import platform
from datetime import date
from pathlib import Path

import numpy as np

from .decimate import Decimated
from .segments import SegmentReport

SOURCE = {
    "title": "Virtual cohort of extreme and average four-chamber heart meshes from statistical shape model",
    "doi": "10.5281/zenodo.4593739",
    "file": "average.tar.gz",
    "licence": "CC-BY-4.0",
    "attribution": "Rodero C, Strocchi M, Marciniak M, Longobardi S, Whitaker J, O'Neill MD, "
                   "Gillette K, Augustin C, Plank G, Vigmond EJ, Lamata P, Niederer SA, 2021",
}


def sha256_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def per_structure(d: Decimated) -> dict[str, dict[str, int]]:
    out = {}
    for sid in sorted(set(d.owner.tolist())):
        tri = d.triangles[d.owner == sid]
        out[str(sid)] = {"triangles": int(len(tri)), "vertices": int(len(np.unique(tri)))}
    return out


def build(source_sha256: str, d: Decimated, report: SegmentReport, glb: bytes,
          view: dict[str, list[float]], built: date | None = None) -> dict:
    return {
        "source": {**SOURCE, "sha256": source_sha256},
        "pipeline": {
            "tool": "tools.anatomy",
            "python": platform.python_version(),
            "numpy": np.__version__,
            "steps": ["surface", "decimate", "segments", "gltf"],
            "cell_size_mm": {str(k): round(v, 4) for k, v in sorted(d.cell_size.items())},
        },
        "output": {
            "file": "heart.glb",
            "sha256": sha256_of(glb),
            "bytes": len(glb),
            "triangles": int(len(d.triangles)),
            "vertices": int(len(d.positions)),
            "per_structure": per_structure(d),
            "view": view,
            "segments": {
                "shipped": report.check == "pass",
                "origin_phi_deg": report.origin_deg,
                "check": report.check,
                "reason": report.reason,
                "report": report.as_dict(),
            },
        },
        "built": (built or date.today()).isoformat(),
    }


def dumps(manifest: dict) -> str:
    return json.dumps(manifest, indent=2, sort_keys=False) + "\n"
