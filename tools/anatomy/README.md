# tools.anatomy

Turns the Rodero average four-chamber mesh into the one geometry file the viewer draws, and proves
that the committed file is exactly what the source produces.

## From the DOI to the committed file

| Step | What happens | Where |
|---|---|---|
| 1 | `average.tar.gz` is fetched from Zenodo record 10.5281/zenodo.4593739 and checked against its SHA-256 | `tests/fixtures/fetch.py` |
| 2 | The VTK ASCII file inside is read into arrays: points, tetrahedra, structure id per cell, and the four universal ventricular coordinates per point | `vtk_reader.py` |
| 3 | Boundary faces of the tetrahedral mesh are kept, with the owning structure per face and outward winding | `surface.py` |
| 4 | A base cell size is found by bisection so the total stays under 60,000 triangles; structures that would fall under 150 triangles get a finer cell, by halving, up to three times. If both limits cannot hold, `BudgetConflict` names the structure and the build stops | `budget.py` |
| 5 | Vertices are clustered on a grid per structure, keyed also by which way they face so thin walls do not collapse, and the pieces are welded at shared vertices | `decimate.py` |
| 6 | AHA 17 segments are derived from the coordinates for the left ventricle, with the origin found from the data. The insertion check decides whether they ship | `segments.py` |
| 7 | One glTF binary is written by hand: one mesh, one primitive per structure, shared vertex buffer, `_SEGMENT` per vertex | `gltf.py` |
| 8 | The manifest records the source hash, tool versions, cell sizes, counts, the segment report, the starting view and the output hash | `manifest.py` |

## Commands

```bash
python tests/fixtures/fetch.py                  # once; downloads into an ignored directory
python -m tools.anatomy build                   # writes web/viewer/data/heart.glb and its manifest
python -m tools.anatomy verify                  # rebuilds to a temporary directory and compares bytes
python tools/anatomy/still.py                   # renders the still image with Playwright
```

`verify` exits 0 when the rebuilt file is byte-identical to the committed one. It exits 1 with a
table of per-structure triangle and vertex counts, committed against rebuilt, when it is not.

## What the manifest fields mean

| Field | Meaning |
|---|---|
| `source.sha256` | Hash of the archive the build read. A different archive is a different build |
| `pipeline.python`, `pipeline.numpy` | The exact versions. Byte identity is promised only for these |
| `pipeline.cell_size_mm` | The grid cell used per structure, in millimetres |
| `output.sha256`, `output.bytes` | The committed file's hash and size |
| `output.per_structure` | Triangles and vertices per structure, so a mismatch can be located |
| `output.view` | Two unit vectors in the file's frame: up, apex to base; anterior, left ventricle towards right ventricle. The page starts its camera from them |
| `output.segments` | Whether segments ship, the check result, the reason, and the full report of measured angles |
| `built` | The date of the build |

## What a mismatch means

| Symptom | Likely cause | What to do |
|---|---|---|
| `verify` exits 1, versions differ | numpy or Python changed | Install the pinned versions from `requirements-anatomy.txt` and rerun |
| `verify` exits 1, same versions, counts differ in a few structures | Floating point differs on this platform | Record it in the vault. The counts table names the structures. The committed file stays the reference |
| `verify` exits 1, source hash differs | The archive on disk is not the one recorded | Delete it and fetch again |
| `BudgetConflict` | A structure cannot keep 150 triangles under the 60,000 total | Record the conflict, per SC-003a. Do not lower the floor quietly |

## Files

| File | Purpose |
|---|---|
| `structures.json` | Names of the 24 structure ids, from the Zenodo record. A copy ships beside the page |
| `still.py` | Renders `heart-still.png`, shown when scripting or WebGL is unavailable |
