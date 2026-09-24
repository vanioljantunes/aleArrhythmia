---
title: Cobiveco, consistent biventricular coordinates
type: literature
status: active
created: 2026-09-24
updated: 2026-09-24
---


# Cobiveco, consistent biventricular coordinates

A later biventricular coordinate system with open code, presented as an improvement on earlier
universal coordinates. Candidate for the canonical space in [[canonical-reference-space]].

## What it is

| Item | Detail |
|---|---|
| Source | Schuler and others, Medical Image Analysis 2021, volume 74, article 102247 |
| Idea | Consistent coordinates on tetrahedral biventricular meshes, with tools to transfer data, visualise it in a standard way and align the heart to global axes |
| Reported gain | More than fourfold reduction in transfer and linearity errors against a state of the art method, on 36 patient geometries |
| Code | MATLAB, https://github.com/KIT-IBT/Cobiveco |

## Coverage

| Covered | Not covered |
|---|---|
| Biventricular myocardium, tetrahedral meshes | Atria |
| Data transfer between geometries, standardised visualisation | Surface only meshes, to be confirmed |

## Licence and availability

| Item | Detail |
|---|---|
| Code | Public on GitHub. Described in search results as a permissive open-source licence, not read directly in this pass |
| Language | MATLAB, which matters for a Python project |

## Consequences for pooling

| Point | Effect |
|---|---|
| Open implementation | The project could reuse or port it rather than implementing coordinates from the paper |
| MATLAB | A port or a reimplementation would be needed, since the core here is Python (Principle VII) |
| Lower transfer error | Less distortion when a focus from one heart lands on the atlas |

## Unknowns

| Unknown | What was tried |
|---|---|
| The exact licence text in the repository | Search only. The repository page was not read in this pass |
| Whether a Python port exists | Not searched yet |

## References

- Schuler and others, Cobiveco, Medical Image Analysis 2021: 10.1016/j.media.2021.102247
- https://github.com/KIT-IBT/Cobiveco
- https://pubmed.ncbi.nlm.nih.gov/34592711/
