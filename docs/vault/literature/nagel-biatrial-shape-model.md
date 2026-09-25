---
title: Nagel and Loewe bi-atrial statistical shape model
type: literature
status: active
created: 2026-09-25
updated: 2026-09-25
---


# Nagel and Loewe bi-atrial statistical shape model

An openly licensed statistical shape model of both atria. This closes the gap the first survey
recorded as unfilled: no open atrial atlas could be found at all.

## What it is

| Item | Detail |
|---|---|
| Record | A bi-atrial statistical shape model and 100 volumetric anatomical models of the atria |
| Authors | Nagel, Sanchez, Azzolin, Zheng, Schuler, Doessel, Loewe, Karlsruhe Institute of Technology |
| DOI | 10.5281/zenodo.5095379 |
| Shape model | `biatrial_model_completeFit_newReference.h5`, 19.1 MB, HDF5 |
| Also included | 100 volumetric models as VTK, 43.5 to 53.5 MB each, and 95 further geometries spanning left atrial volumes |
| Augmented with | Wall thickness, fibre orientation, material tags |

## Coverage

| Covered | Not covered |
|---|---|
| Left and right atrium together | Ventricles |
| Shape variation across a population | Any electrophysiological measurement |

## Licence

Stated on the Zenodo record as Creative Commons Attribution 4.0 International. Read directly on
2026-09-25. Redistribution is permitted with credit.

## Why this matters

| Point | Effect |
|---|---|
| The atrial gap is closed | The first survey searched and found nothing. This is a direct answer, openly licensed |
| Functional replacement | It does for the atria what the unlicensed ventricular atlas would have done, and its terms are stated |
| Atrial arrhythmia becomes reachable | Most ablation work is atrial, so an atrial reference anatomy is not optional for long |
| Not needed for the first viewer | [[ADR-0008-reference-anatomy]] takes a four-chamber mesh, which already includes atrial geometry |

## Unknowns

| Unknown | What was tried |
|---|---|
| Vertex counts of the mean atrial shape | Not published on the record |
| Whether the model pairs cleanly with universal atrial coordinates | Not established. See [[universal-atrial-coordinates]] |

## References

- Zenodo record, licence read 2026-09-25: https://zenodo.org/records/5095379
- DOI: 10.5281/zenodo.5095379
- The gap this closes: [[survey-unknowns-2026-09-24]]
