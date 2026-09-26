---
title: The derived heart geometry, as built
type: literature
status: active
created: 2026-09-25
updated: 2026-09-25
---

# The derived heart geometry, as built

The committed file `web/viewer/data/heart.glb` was built on 2026-09-25 from the Rodero average mesh
by `python -m tools.anatomy build`. This note records what came out, so that a later rebuild that
differs can be diagnosed against numbers rather than memory. The manifest beside the file carries
the same numbers in machine form.

## Build summary

| Item | Value |
|---|---|
| Source | `average.tar.gz`, [[rodero-four-chamber-meshes]], SHA-256 `d787d6470c8a4a6c7bfb808c55e44e35a7bc18f5888847e2b24380beae2703ee` |
| Tool | `tools.anatomy`, Python 3.14.3, numpy 2.4.4 |
| Steps | surface, decimate, segments, gltf |
| Base cell | 2.5194 mm, found by bisection so the total lands under 60,000 triangles |
| Refined structures | 12, 15, 20, 21, 23, 24 at half the base cell; 13, 14 at a quarter |
| Triangles | 57,204 of 334,550 on the extracted surface |
| Vertices | 28,142, under the 65,535 that uint16 indices allow |
| Bytes | 1,137,600 raw, 852,235 gzipped, under the 2 MB target |
| Output SHA-256 | `34d54a5e359a6bc18f14746aca1e6602cdce60cada4e79367d23b99ac733a5e4` |
| Rebuild check | `python -m tools.anatomy verify` exit 0, byte-identical, 2026-09-25 |
| Enclosed volume | 0.9993 of the source tetrahedral volume |

## Per structure

| Id | Structure | Triangles | Vertices | Cell mm |
|---|---|---|---|---|
| 1 | Left ventricle myocardium | 15,089 | 7,794 | 2.5194 |
| 2 | Right ventricle myocardium | 12,491 | 6,595 | 2.5194 |
| 3 | Left atrium myocardium | 8,124 | 4,363 | 2.5194 |
| 4 | Right atrium myocardium | 9,253 | 4,834 | 2.5194 |
| 5 | Aorta wall | 4,445 | 2,322 | 2.5194 |
| 6 | Pulmonary artery wall | 1,318 | 729 | 2.5194 |
| 7 | Mitral valve plane | 674 | 387 | 2.5194 |
| 8 | Tricuspid valve plane | 1,220 | 678 | 2.5194 |
| 9 | Aortic valve plane | 536 | 324 | 2.5194 |
| 10 | Pulmonary valve plane | 528 | 332 | 2.5194 |
| 11 | Left atrial appendage inlet | 182 | 123 | 2.5194 |
| 12 | Left superior pulmonary vein inlet | 174 | 121 | 1.2597 |
| 13 | Left inferior pulmonary vein inlet | 298 | 194 | 0.6299 |
| 14 | Right inferior pulmonary vein inlet | 338 | 216 | 0.6299 |
| 15 | Right superior pulmonary vein inlet | 326 | 207 | 1.2597 |
| 16 | Superior vena cava inlet | 189 | 134 | 2.5194 |
| 17 | Inferior vena cava inlet | 216 | 136 | 2.5194 |
| 18 | Left atrial appendage border | 231 | 146 | 2.5194 |
| 19 | Right inferior pulmonary vein border | 207 | 126 | 2.5194 |
| 20 | Left inferior pulmonary vein border | 235 | 159 | 1.2597 |
| 21 | Left superior pulmonary vein border | 324 | 202 | 1.2597 |
| 22 | Right superior pulmonary vein border | 180 | 121 | 2.5194 |
| 23 | Superior vena cava border | 317 | 204 | 1.2597 |
| 24 | Inferior vena cava border | 309 | 198 | 1.2597 |

Every structure keeps at least 150 triangles, the floor the plan set. No `BudgetConflict` arose.

## Surface quality after clustering

| Edge shared by | Count |
|---|---|
| 1 triangle | 1,337 |
| 2 triangles | 81,887 |
| 3 or more | 2,046 |

The source surface was closed with 64 pinch edges. Clustering opens small slits and pinches where
thin structures meet, mostly at valve planes and vessel borders. Rendering does not need a manifold
surface, and the enclosed volume is preserved to 0.07 percent, so this is accepted for the viewer.
A tool that needs a watertight surface must not take this file as input.

## The segment check

Segments are derived from the coordinates the mesh carries, with the origin found from the data as
research R-004 describes. The check compares the inferior insertion against the AHA 3/4 boundary.

| Measurement | Value |
|---|---|
| Contact points, LV epicardium within 1.5 mm of RV wall | 6,020 in two bands of 4,243 and 1,777 |
| PHI direction seen from the apex | clockwise |
| Anterior insertion, band mean | 70.79 deg of PHI |
| Inferior insertion, band mean | -30.47 deg of PHI |
| Septal arc between them | 101.26 deg |
| AHA 3/4 boundary, 120 deg from the origin | -49.21 deg of PHI |
| Gap between inferior insertion and 3/4 boundary | 18.74 deg |
| Tolerance | 15.0 deg |
| Result | fail |

The check fails. Segments are therefore not shipped, and the viewer shows the segment control
disabled with this reason, as FR-025 and [[ADR-0007-unavailable-capability]] require. The
per-vertex labels are still in the file under `_SEGMENT` for anyone who wants to inspect them, and
the manifest says `shipped: false`.

The measurement depends on what counts as the insertion. The RV wall lies against the LV surface
for some distance, so each contact band is 30 to 50 degrees wide. Three readings of the same data:

| Insertion taken as | Septal arc | Gap to 120 |
|---|---|---|
| Band mean, used above | 101 deg | 19 deg |
| Outer band edges, 3rd and 97th percentile | 146 deg | 26 deg |
| Inner band edges | shorter still | larger still |

None of them passes at 15 degrees. The honest reading is that this anatomy's septum does not
subtend the 120 degrees the equal-sector AHA model assumes, which is a known property of the model
rather than a fault in the mesh. The way out, if segments are wanted, is a decision to anchor both
insertions and divide the septum into two sectors and the free wall into four, the convention some
clinical software uses. That changes the specification and is recorded as an open question in
[[aha-17-segment-model]], not decided here.

## References

- Source and licence: [[rodero-four-chamber-meshes]]
- What the source contains: [[rodero-mesh-contents]]
- Decision that adopted the mesh: [[ADR-0008-reference-anatomy]]
- Disabled control pattern: [[ADR-0007-unavailable-capability]]
- Coordinates used for the segments: [[universal-ventricular-coordinates]]
- Plan and research: `specs/003-anatomy-viewer/plan.md`, `specs/003-anatomy-viewer/research.md`
