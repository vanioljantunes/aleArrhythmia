---
title: CARTO 3 export (Biosense Webster)
type: literature
status: active
created: 2026-09-24
updated: 2026-09-26
---


# CARTO 3 export (Biosense Webster)

One of the two systems that get a viewer version in [[ADR-0006-viewer-versions]].

## What it is

| Item | Detail |
|---|---|
| System | CARTO 3, Biosense Webster |
| Export | Studies can be exported for offline analysis. An open parser reads them |
| Evidence | [[openep-and-pulse-ep]]: OpenEP names Carto3 among its supported systems and ships a CARTO importer |

## Coverage

| Covered | Not covered |
|---|---|
| Chamber geometry and mapping points, as consumed by existing open parsers | Exact field list, not read in this pass |

## Licence and availability

| Item | Detail |
|---|---|
| Format documentation | No public vendor specification found in this pass. The knowledge sits in open parsers |
| Reading an export | Precedent exists under Apache-2.0, which suggests no practical barrier to reading files a site already holds |

## Consequences for pooling

| Point | Effect |
|---|---|
| Importer is tractable | An existing open implementation can be followed or ported |
| Display conventions still needed | ADR-0006 requires the display mode, and no source for the default colour scales and views has been gathered yet |

## Unknowns

| Unknown | What was tried |
|---|---|
| Field level structure of an export | Partly read 2026-09-25 from a real export: [[openep-testingdata-carto-export]]. Mesh files hold vertices, normals and triangles; point lists are XML; per-point positions, ECG and contact force are text. Full field semantics still to be documented while the importer is written |
| Default colour scales, standard views and orientation labels | Not searched yet |
| Whether reading exports carries any vendor licence restriction | Not established |

## Coordinate frame, found 2026-09-26

No vendor document or the OpenEP paper states the patient direction of each axis. Two independent
open-source readers encode the same convention, found empirically by their authors:

| Source | What it says |
|---|---|
| SlicerEAMapReader, `EAMapReader.py`, `transformCarto` | Comment: "CARTO mesh is in LPS and seems to be additionally rotated 90 deg around the LR axis", with the matrix to Slicer's RAS: R = -X, A = Z, S = Y. Applied alike to the mesh, the car points and the VisiTag sites |
| OpenEP core, `drawMap.m` | The AP view puts the camera on +Z with +Y up, so +Z anterior, +Y superior, and in a right-handed frame +X is the patient's left |

So: +X left, +Y superior, +Z anterior. The viewer uses this for the standard views on a CARTO study.
It is a finding of other people's code, not a vendor statement, and the two sources agree.
Standard views follow the fluoroscopic convention: AP and PA along the anterior axis, LAO and RAO
swung 45 degrees towards the patient's left or right, LL and RL from the sides, SUP and INF along the
long axis of the body, RPO and LPO posterior obliques. CARTO's own default angles were not found.

- https://github.com/stephan1312/SlicerEAMapReader
- https://github.com/openep/openep-core/blob/master/drawMap.m

## References

- Williams and others, OpenEP, Frontiers in Physiology 2021: 10.3389/fphys.2021.646023
- https://github.com/openep/openep-core
- Decision that makes this a first-class version: [[ADR-0006-viewer-versions]]
