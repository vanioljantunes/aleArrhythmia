---
title: Fixed atlas vertex space
type: literature
status: draft
created: 2026-09-24
updated: 2026-09-24
---


# Fixed atlas vertex space

Using vertex indices on one fixed template mesh as the coordinate system. Candidate for the
canonical space in [[canonical-reference-space]]. No single publication defines it; it is the
option of doing the simplest possible thing.

## What it is

| Item | Detail |
|---|---|
| Idea | Choose one template mesh, for example from [[cardiac-atlas-project-biventricular-modes]]. A location is the index of a vertex, or a barycentric position on a face |
| How a focus arrives | Register the study's geometry to the template, then take the nearest vertex |

## Coverage

| Covered | Not covered |
|---|---|
| Whatever the chosen template covers | Anything the template omits, permanently |

## Licence and availability

| Item | Detail |
|---|---|
| Depends entirely on the template | See the atlas note for the candidate template and its terms |

## Consequences for pooling

| Point | Effect |
|---|---|
| Simple to implement and to check | Distances are mesh distances, computable once and cached |
| Brittle | Changing or refining the template invalidates every coordinate already reported, which Principle II treats as a new space version |
| Resolution fixed by the mesh | Kernel widths smaller than the vertex spacing cannot be represented |

## Unknowns

| Unknown | What was tried |
|---|---|
| Whether a template of adequate resolution exists with terms that allow redistribution | Partly. See the licence unknown in [[cardiac-atlas-project-biventricular-modes]] |

## References

- Cardiac Atlas Project biventricular modes: [[cardiac-atlas-project-biventricular-modes]]
- Cobiveco, which aligns geometries to standard axes: [[cobiveco-biventricular-coordinates]]
