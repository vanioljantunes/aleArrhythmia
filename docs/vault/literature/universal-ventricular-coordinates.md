---
title: Universal ventricular coordinates (UVC)
type: literature
status: active
created: 2026-09-24
updated: 2026-09-24
---


# Universal ventricular coordinates (UVC)

A continuous coordinate system for the ventricles, proposed so that data can be transferred between
different hearts. Candidate for the canonical space in [[canonical-reference-space]].

## What it is

| Item | Detail |
|---|---|
| Source | Bayer and others, Medical Image Analysis 2018 |
| Idea | Every point in the ventricular wall gets four coordinates: apex to base, rotational around the axis, transmural from endocardium to epicardium, and a ventricle label |
| Computed by | Solving Laplace problems on a mesh of the individual heart |
| Purpose stated by the authors | Describing position within the heart and transferring data between hearts |

## Coverage

| Covered | Not covered |
|---|---|
| Left and right ventricular myocardium | Atria |
| Continuous position, so smoothing and kernels work | Valve annuli in the original formulation, addressed by later work |

## Licence and availability

| Item | Detail |
|---|---|
| Paper | Published, not open access at the publisher |
| Reference implementation | Not established in this pass. A related system with code exists, see [[cobiveco-biventricular-coordinates]] |

## Consequences for pooling

| Point | Effect |
|---|---|
| Continuous coordinates | An uncertainty kernel can be placed around a focus, which is what ALE needs |
| Anatomy independent | A focus reported on one patient's heart maps onto the atlas without needing that patient's mesh |
| Ventricles only | An atrial arrhythmia needs a second system, see [[universal-atrial-coordinates]] |

## Unknowns

| Unknown | What was tried |
|---|---|
| Whether a maintained open implementation of the 2018 formulation exists | Web search for the paper and for code. Found the paper and a later, related system with code |
| Transfer error when mapping between very different geometries | Not established in this pass |

## References

- Bayer and others, Universal ventricular coordinates, Medical Image Analysis 2018: 10.1016/j.media.2018.01.005
- https://pubmed.ncbi.nlm.nih.gov/29414438/
