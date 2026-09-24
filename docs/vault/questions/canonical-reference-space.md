---
title: Which canonical cardiac reference space
type: question
status: open
created: 2026-09-24
updated: 2026-09-24
---


# Which canonical cardiac reference space

## The question

Every coordinate this project stores or pools must be expressed in one space, named and versioned
(Principle II). Which space, and does one space cover both ventricles and atria, or does the
project carry one per chamber group?

## Candidates

- [[universal-ventricular-coordinates]]: continuous ventricular coordinates, the original
  formulation
- [[cobiveco-biventricular-coordinates]]: later biventricular coordinates with open MATLAB code and
  lower reported transfer error
- [[universal-atrial-coordinates]]: the atrial counterpart, open access with data
- [[aha-17-segment-model]]: discrete segments, universally understood, not continuous
- [[fixed-atlas-vertex-space]]: vertex indices on one template mesh
- [[hybrid-coordinate-and-segment]]: continuous storage, segment names for reporting

## What would settle it

| Evidence needed | Why it decides |
|---|---|
| A reference anatomy the project may redistribute under an open licence | Principle I. Without it, no candidate can ship. See the licence unknown in [[survey-unknowns-2026-09-24]] |
| Whether the arrhythmias in scope are atrial, ventricular or both | Decides whether one system suffices or two are needed |
| Transfer error of each candidate between unlike geometries | Sets how much spatial precision survives pooling, which bounds the whole method |
| A documented rule for segment-only reports | Decides whether the many studies reporting only a region can contribute at all |
| An implementation the Python core can use or port | Principle VII. Cobiveco is MATLAB today |

## Current leaning

None recorded. The hybrid option looks attractive because it keeps kernels working while staying
readable, but no candidate can be chosen before the licence and chamber-scope questions above are
answered.
