---
title: Rodero four-chamber heart meshes
type: literature
status: active
created: 2026-09-25
updated: 2026-09-25
---


# Rodero four-chamber heart meshes

An openly licensed cohort of whole-heart meshes derived from a statistical shape model. Chosen as
the project's reference anatomy in [[ADR-0008-reference-anatomy]].

## What it is

| Item | Detail |
|---|---|
| Record | Virtual cohort of extreme and average four-chamber heart meshes from a statistical shape model |
| Authors | Rodero, Strocchi, Marciniak, Longobardi, Whitaker, O'Neill, Gillette, Augustin, Plank, Vigmond, Lamata, Niederer |
| Published | 2021-03-15 |
| DOI | 10.5281/zenodo.4593739 |
| Contents | 39 heart models: one average, plus nine shape modes at plus and minus two and three standard deviations |
| The file that matters here | `average.tar.gz`, 58.2 MB, the mean heart |

## Coverage

| Covered | Not covered |
|---|---|
| All four chambers | Electrophysiology of any kind |
| Ventricular and atrial myocardium | Conduction system |
| Valve planes, aorta, pulmonary artery, pulmonary vein inlets, vena cava | Wall properties beyond geometry |

## Licence

Stated on the Zenodo record as Creative Commons Attribution 4.0 International. Read directly on
2026-09-25, not inferred. The licence permits redistribution and reuse on condition that the creator
is credited.

This is the property the project needed and could not find before: an explicit grant, not an absent
refusal. See [[cardiac-atlas-project-biventricular-modes]] for the candidate it replaces.

## Consequences for the project

| Point | Effect |
|---|---|
| Redistribution permitted | The mesh can be bundled in this repository with attribution, satisfying Principle I |
| Four chambers in one mesh | Ventricles and atria arrive together, so the project does not need two anatomies to start |
| Research-grade volume mesh | Not web-ready. The surface has to be extracted and decimated before a browser can draw it |
| Mean shape, not a patient | Honest as a reference anatomy, and it must never be presented as any individual's heart |

## Unknowns

| Unknown | What was tried |
|---|---|
| Vertex and element counts | Not published on the record. The paper defers to supplementary text. Only an average edge length near 1 mm is stated |
| How much decimation the surface tolerates before anatomy is distorted | Not tested. To be measured when the pipeline is built |
| Whether the average mesh carries universal ventricular coordinates | Not established. A sibling record (10.5281/zenodo.4590294) states UVC, this one does not say |

## References

- Zenodo record, licence read 2026-09-25: https://zenodo.org/records/4593739
- DOI: 10.5281/zenodo.4593739
- Decision that adopts it: [[ADR-0008-reference-anatomy]]
