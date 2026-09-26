---
title: What the Rodero average mesh actually contains
type: literature
status: active
created: 2026-09-25
updated: 2026-09-25
---

# What the Rodero average mesh actually contains

The file was downloaded and read on 2026-09-25, to answer three questions that could not be settled from
the record page. All three are now answered, and two of them turned out better than assumed.

## What was measured

| Property | Value |
|---|---|
| Archive | `average.tar.gz`, 58,167,648 bytes, containing one file |
| File | `average.vtk`, 187,320,446 bytes, VTK 3.0 ASCII, unstructured grid |
| Points | 379,158 |
| Tetrahedra | 1,766,006 |
| Labelled structures | 24 |
| Bounding box | 129.4 by 108.1 by 124.9 mm |

The bounding box is the size of a real adult heart, which is a useful check that the units are
millimetres and the geometry is not scaled.

## The three questions

| Question | Answer |
|---|---|
| Does the outer surface extract cleanly? | Yes. 334,550 boundary triangles. 95.3 percent of faces are shared by exactly two tetrahedra, and the remainder form a closed boundary |
| How far must it decimate? | 5.6 times, keeping 17.9 percent, to reach a 60,000 triangle budget |
| Are landmarks for AHA-17 derivable? | Not needed. The mesh already carries universal ventricular coordinates |

## The coordinates already in the file

Four scalar fields sit on the points. Their ranges identify them:

| Field | Range | What it is |
|---|---|---|
| `RHO.dat` | 0 to 1 | Transmural, endocardium to epicardium |
| `PHI.dat` | -pi to pi | Rotational about the long axis |
| `Z.dat` | 0 to 1 | Apicobasal, apex to base |
| `V.dat` | -1 or 1 | Which ventricle |

Every field also takes the value -10, a sentinel marking points where the coordinate is undefined,
that is outside the ventricles.

This matters more than the size numbers. The specification wrote AHA-17 segmentation as a
conditional, shipping only if landmarks could be derived, because finding apex, base and the right
ventricular insertions on a raw mesh is real work. It does not have to be done. Segments follow
directly from the apicobasal and rotational coordinates already present, which is the same
construction that makes an idealised ventricle segment exactly.

## Consequences

| Point | Effect |
|---|---|
| The surface is closed | Extraction is a boundary-face count, not a repair job |
| 17.9 percent retention | Comfortable. A 60,000 triangle mesh with normals is roughly 1.1 to 1.5 MB before compression, inside the 2 MB budget |
| 24 structures survive to the surface | All 24 appear on the boundary, so each one can be shown and hidden |
| Universal ventricular coordinates present | AHA-17 is derivable, and the file already carries a coordinate system |

## Unknowns that remain

| Unknown | What was tried |
|---|---|
| Whether uniform decimation preserves the smallest structures | Answered 2026-09-25. It does not: eight structures needed a finer cell than the rest. No conflict arose. The sizes chosen are in [[derived-heart-geometry]] |
| Whether these fields match the published universal ventricular coordinates definition exactly | The ranges and the sentinel are consistent with it, but the record page does not state it and no definition was compared field by field |
| What the 24 structure identifiers mean | Answered 2026-09-25. The legend is in the Zenodo record description, missed on the first reading. See the section below |

## The 24 structure identifiers, resolved

Found 2026-09-25. The Zenodo record description, section "Cardiac meshes", lists the labels in
order. Rodero 2021 S1 Text, Fig B, shows the same 24 among 31 segmentation labels, the other seven
being blood pools, trabeculae and vessel cavities that are not meshed. The two sources agree.

| Id | Structure |
|---|---|
| 1 | Left ventricle myocardium |
| 2 | Right ventricle myocardium |
| 3 | Left atrium myocardium |
| 4 | Right atrium myocardium |
| 5 | Aorta wall |
| 6 | Pulmonary artery wall |
| 7 | Mitral valve plane |
| 8 | Tricuspid valve plane |
| 9 | Aortic valve plane |
| 10 | Pulmonary valve plane |
| 11 | Left atrial appendage inlet |
| 12 | Left superior pulmonary vein inlet |
| 13 | Left inferior pulmonary vein inlet |
| 14 | Right inferior pulmonary vein inlet |
| 15 | Right superior pulmonary vein inlet |
| 16 | Superior vena cava inlet |
| 17 | Inferior vena cava inlet |
| 18 | Left atrial appendage border |
| 19 | Right inferior pulmonary vein border |
| 20 | Left inferior pulmonary vein border |
| 21 | Left superior pulmonary vein border |
| 22 | Right superior pulmonary vein border |
| 23 | Superior vena cava border |
| 24 | Inferior vena cava border |

| Term | Meaning |
|---|---|
| Inlet | The closing plane at a vessel or appendage ostium |
| Border | The short ring of vessel wall kept beyond the inlet, for mechanics boundary conditions |

One trap. The earlier Strocchi 2020 cohort (Zenodo 3890034) uses the same first six ids and then a
different order for 7 to 24: valves at 14 to 17, vein rings at 7 to 13. Its lookup must not be used
for these meshes. The table above is committed as `tools/anatomy/structures.json`.

## References

- The dataset: [[rodero-four-chamber-meshes]]
- Zenodo record: https://zenodo.org/records/4593739
- The coordinate system these fields resemble: [[universal-ventricular-coordinates]]
- Decision that adopted this mesh: [[ADR-0008-reference-anatomy]]
- Specification this informs: `specs/003-anatomy-viewer/spec.md`
