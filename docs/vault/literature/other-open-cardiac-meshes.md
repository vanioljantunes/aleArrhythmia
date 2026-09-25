---
title: Other openly licensed cardiac meshes
type: literature
status: active
created: 2026-09-25
updated: 2026-09-25
---


# Other openly licensed cardiac meshes

Surveyed alongside the two the project adopted, and recorded so the choice can be revisited without
repeating the search. None of these record pages was read directly; the licences below come from a
search pass and are marked accordingly.

## Candidates

| Source | Covers | Licence as reported | Read directly |
|---|---|---|---|
| Strocchi 24 four-chamber meshes, 10.5281/zenodo.3890034 | Whole heart, fibres, universal ventricular coordinates, 22.5 GB | CC-BY-4.0 | No |
| Rodero 1000 synthetic hearts, 10.5281/zenodo.4506930 | Whole heart, 24 labelled structures, plus the shape model as eigenvector tables | CC-BY-4.0 | No |
| Rodero 20 computed-tomography hearts, 10.5281/zenodo.4590294 | Whole heart, fibres, universal ventricular coordinates | CC-BY-4.0 | No |
| CobivecoX, 10.5281/zenodo.7922601 | Biventricular, 481 instances and a mean atlas, single 25.5 GB archive | CC-BY-4.0 | No |
| Roney atrial modelling toolkit, 10.5281/zenodo.10139306 | Example atrial models | CC-BY-4.0 | No |
| BodyParts3D | Whole heart anatomy, browser-native OBJ, about 266 thousand triangles | CC BY-SA 2.1 Japan | No |

## The share-alike case

BodyParts3D and its derivatives carry a share-alike condition. Bundling them would oblige the
project to license the mesh directory, and any mesh it modifies, under the same terms, with changes
indicated. The Attribution-only records above carry no such condition, which is why they were
preferred. See [[ADR-0008-reference-anatomy]].

## Confirmed unusable

| Source | Reason |
|---|---|
| Zygote Solid 3D Heart | Commercial terms. Modifications and additions may not be distributed without written permission |
| Multi-Modality Whole Heart Segmentation challenge data | Recipients commit not to pass the data to any third party |
| Living Heart Project | Commercial product, no public licence |
| IT'IS Virtual Population | Click-through terms at download, no open licence |
| Cardiac Atlas Project biventricular modes | No licence stated. See [[cardiac-atlas-project-biventricular-modes]] |

## Unknowns

| Unknown | What was tried |
|---|---|
| Whether the licences in the first table are as reported | Search pass only. Each record page must be read before any of these is adopted |
| The licence covering example meshes inside the Cobiveco repository | The repository licence names source code. Whether it reaches the data is ambiguous |
| Whether openCARP bundled meshes carry any data licence | Nothing found. The project licence covers the simulator and its example experiments |

## References

- Strocchi and others: https://zenodo.org/records/3890034
- Rodero synthetic cohort: https://zenodo.org/records/4506930
- BodyParts3D licence page: https://lifesciencedb.jp/bp3d/info/license/index.html
- Decision that selected among these: [[ADR-0008-reference-anatomy]]
