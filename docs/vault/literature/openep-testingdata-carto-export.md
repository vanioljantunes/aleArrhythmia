---
title: OpenEP testing data, a porcine CARTO 3 export
type: literature
status: active
created: 2026-09-25
updated: 2026-09-25
---


# OpenEP testing data, a porcine CARTO 3 export

A genuine, unmodified CARTO 3 export directory, published to test the OpenEP parsers. The first
fixture the importer is built against.

## What it is

| Item | Detail |
|---|---|
| Record | openep-testingdata |
| Author | Steven Williams, The University of Edinburgh |
| DOI | 10.5281/zenodo.6651600 |
| Published | 2022-06-16 |
| File | `carto.zip`, 10,536,737 bytes |
| Subject | Porcine. The record states: "Pig data obtained using Carto" |
| Contents | One export directory, `Export_Study-1-11_25_2021-15-01-32`, with 4 mesh files, 8 XML files and 99 text files |

## Licence

Stated on the Zenodo record as Creative Commons Attribution 4.0 International. Read directly on
2026-09-25. A GitHub mirror of the same content declares GPL-3.0; the Zenodo deposit is the one the
project cites, and its terms are the ones relied on.

## What the export contains

| File kind | Count | Holds |
|---|---|---|
| `*.mesh` | 4 | Chamber geometry. Biosense Webster triangulated mesh format, 2008, with vertices, normals and triangles |
| `*_Points_Export.xml` | 4 | Point lists per map. Three maps hold zero points, one holds two |
| `*_Point_Export.xml`, positions, ECG, contact force | per point | Full per-point detail for the two points |
| `VisiTagExport/` | many | Ablation lesion positions and settings |
| `Study 1 11_25_2021 15-01-32.xml` | 1 | Study manifest, units in millimetres and radians |

Largest mesh: 3,513 vertices, 7,022 triangles.

## Why it was chosen

| Point | Effect |
|---|---|
| A real export, not a parsed copy | Proves the importer reads what CARTO actually writes, which no reformatted dataset can |
| Geometry and points travel together | Confirms the assumption patient mode rests on |
| Porcine | Patient-data obligations do not arise. The de-identification check was still run, see below |
| Two points only | Enough to prove the format. Not enough to show a map, which is why [[argo-ventricular-tachycardia-dataset]] is paired with it |

## De-identification check, required by FR-013n

Run on 2026-09-25 by reading the extracted files, not by trusting the record.

| Looked for | Method | Found |
|---|---|---|
| Names, surnames, birth dates, record numbers, hospital names, file paths | Case-insensitive search across every file | None. Every hit was a `Map_Name` or `Short_Name` attribute naming an anatomical structure or a map |
| The study name | Read the manifest | `Study 1 11_25_2021 15-01-32`, a sequence number and acquisition timestamp |
| Mesh identity | Read the mesh headers | `MeshName` empty, `MeshID` -1 |

Nothing identifying a person or an institution was found. The acquisition timestamp remains in the
study name, which for a porcine study identifies nobody.

## References

- Zenodo record, licence read 2026-09-25: https://zenodo.org/records/6651600
- DOI: 10.5281/zenodo.6651600
- The parser it was published to test: [[openep-and-pulse-ep]]
- The format it exercises: [[carto3-export]]
- Session: [[log-2026-09-25-eam-datasets]]
