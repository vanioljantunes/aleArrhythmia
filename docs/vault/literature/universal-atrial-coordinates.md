---
title: Universal atrial coordinates (UAC)
type: literature
status: active
created: 2026-09-24
updated: 2026-09-24
---


# Universal atrial coordinates (UAC)

The atrial counterpart to ventricular coordinate systems. Candidate for the canonical space in
[[canonical-reference-space]], and the only candidate found so far that covers the atria.

## What it is

| Item | Detail |
|---|---|
| Source | Roney and others, Medical Image Analysis 2019, volume 55, pages 65 to 75 |
| Idea | Two coordinates over the atrial surface, used to map scalar fields between atrial meshes |
| Demonstrated uses | Visualisation, registration, construction of patient specific meshes, transfer of fibre directions and anatomic structures from a reference geometry |

## Coverage

| Covered | Not covered |
|---|---|
| Atrial surfaces, including transfer of fibre fields | Ventricles |
| Scalar fields measured with different mapping modalities | Wall thickness, since the atrial wall is treated as a surface |

## Licence and availability

| Item | Detail |
|---|---|
| Paper | Open access, CC BY |
| Data and code | Reported to come with patient specific meshes, atrial structures and fibre directions, and open code for the extended system |

## Consequences for pooling

| Point | Effect |
|---|---|
| Surface coordinates | Fits atrial arrhythmia, where the substrate is treated as a surface |
| Open access with data | Lowers the cost of adopting it and of checking any result computed in it |
| Pairs with a ventricular system | A project covering both chambers would carry two coordinate systems, which the canonical space decision must address |

## Unknowns

| Unknown | What was tried |
|---|---|
| Exact location and licence of the released code and meshes | Search only. The repository was not opened in this pass |
| How the two coordinates behave near the pulmonary veins and the appendage | Not established |

## References

- Roney and others, Universal atrial coordinates, Medical Image Analysis 2019: 10.1016/j.media.2019.04.004
- Preprint: https://arxiv.org/abs/1810.06630
- https://pubmed.ncbi.nlm.nih.gov/31026761/
