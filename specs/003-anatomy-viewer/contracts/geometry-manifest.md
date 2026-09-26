# Contract: Derived geometry and its manifest

What `heart.glb` and `heart.manifest.json` promise to the page, to the tests, and to anyone
rebuilding them.

## Files

| File | Promise |
|---|---|
| `web/viewer/data/heart.glb` | glTF 2.0 binary. One mesh, 24 primitives named `structure-1` to `structure-24`. Per-vertex attributes `POSITION`, `NORMAL`, and `_SEGMENT` (uint8). Indices uint16 |
| `web/viewer/data/heart.manifest.json` | The record below |
| `web/viewer/data/LICENSE` | The CC-BY-4.0 text and the attribution line the licence requires |

## Manifest shape, with synthetic values

```json
{
  "source": {
    "title": "Virtual cohort of extreme and average four-chamber heart meshes",
    "doi": "10.5281/zenodo.4593739",
    "file": "average.tar.gz",
    "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
    "licence": "CC-BY-4.0",
    "attribution": "Rodero C, Strocchi M, and others, 2021"
  },
  "pipeline": {
    "tool": "tools.anatomy",
    "python": "3.13.0",
    "numpy": "2.0.0",
    "steps": ["surface", "decimate", "segments", "gltf"],
    "cell_size_mm": {"1": 2.4, "2": 2.4, "24": 0.8}
  },
  "output": {
    "file": "heart.glb",
    "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
    "bytes": 1234567,
    "triangles": 59000,
    "vertices": 31000,
    "per_structure": {"1": {"triangles": 15000, "vertices": 7800}},
    "view": {"up": [0.0, 0.0, 1.0], "anterior": [0.0, -1.0, 0.0]},
    "segments": {"shipped": true, "origin_phi_deg": -45.0, "check": "pass"}
  },
  "built": "2026-09-25"
}
```

| Rule | Reason |
|---|---|
| `output.sha256` equals the SHA-256 of `heart.glb` on disk | FR-020 |
| `python` and `numpy` are exact versions | FR-020a |
| Counts are present even when the hash matches | FR-020b, so a future mismatch is diagnosable |
| `segments.shipped` false means the page shows the segment control disabled with `segments.check` as the reason | FR-025, ADR-0007 |
| `view.up` and `view.anterior` are unit vectors in the file's own frame, measured from the source coordinates: apex to base, and left ventricle towards right ventricle made perpendicular to up. The page starts its camera from them | FR-013, so the starting view is derived, not hand-tuned |
| No field names a person, a machine, or a path outside the repository | FR-035 |

## Commands

| Command | Does | Exit |
|---|---|---|
| `python -m tools.anatomy build --source <path to average.tar.gz>` | Writes the three files | 0 on success |
| `python -m tools.anatomy verify` | Rebuilds to a temporary path from the same source and compares bytes with the committed file | 0 identical, 1 differs, with the count diff printed |
