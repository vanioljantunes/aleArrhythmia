---
title: AHA 17-segment model
type: literature
status: active
created: 2026-09-24
updated: 2026-09-24
---


# AHA 17-segment model

The standard way clinicians name where something is in the left ventricle. Candidate for the
canonical space in [[canonical-reference-space]], and the fallback when a study reports only a
region name.

## What it is

| Item | Detail |
|---|---|
| Source | Cerqueira and others for the American Heart Association, Circulation 2002, volume 105, pages 539 to 542 |
| Idea | The left ventricle divided into 17 named segments, with agreed nomenclature |
| Adoption | Used across nuclear imaging, computed tomography, magnetic resonance, echocardiography and angiography |

## Coverage

| Covered | Not covered |
|---|---|
| Left ventricle | Right ventricle, atria |
| Names every clinician already knows | Position within a segment |

## Licence and availability

| Item | Detail |
|---|---|
| Status | A published consensus standard, readable at the journal site |
| Implementation | None needed. The model is a naming scheme |

## Consequences for pooling

| Point | Effect |
|---|---|
| Discrete segments | Pooling becomes counting per segment. The modelled activation and kernel that define ALE have nothing continuous to act on |
| Universally understood | Any reader can interpret the result without learning a new system |
| Coarse | Two foci a few millimetres apart across a segment boundary count as far apart, and two foci at opposite ends of one segment count as identical |
| Useful as a reporting layer | A continuous space can be labelled with segment names for the reader, keeping both properties |

## Unknowns

| Unknown | What was tried |
|---|---|
| Whether an agreed atrial segmentation of similar standing exists | Not searched yet |

## References

- Cerqueira and others, Standardized myocardial segmentation and nomenclature, Circulation 2002: 10.1161/hc0402.102975
- https://www.ahajournals.org/doi/full/10.1161/hc0402.102975
