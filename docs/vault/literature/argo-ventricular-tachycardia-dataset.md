---
title: ARGO, an anonymised human ventricular tachycardia mapping dataset
type: literature
status: active
created: 2026-09-25
updated: 2026-09-25
---


# ARGO, an anonymised human ventricular tachycardia mapping dataset

Nine post-ischaemic ventricular tachycardia patients mapped with CARTO 3, published on PhysioNet
with documented ethics approval and a documented anonymisation statement. The second fixture for
the importer, and the one that shows patient mode doing something real.

## What it is

| Item | Detail |
|---|---|
| Host | PhysioNet |
| DOI | 10.13026/8gh2-e660 |
| Version | 1.0.0 |
| Mapping system | Stated on the record: CARTO 3 |
| Patients | 9, post-ischaemic ventricular tachycardia |
| Points | 1,962 across the nine |
| Size | 378.4 MB uncompressed, 182.9 MB compressed |

## Per-patient files, as the record describes them

| File | Record's description |
|---|---|
| `XYZmesh.txt` | 3-D coordinates of the triangulated mesh vertices composing the LV reconstruction |
| `ConnectivityList.txt` | List of connections between triangulated mesh vertices |
| `MESHcoloring.txt` | Voltage and LAT map coloring data |
| `POS_POINTS.txt` | Pn coordinates on the LV reconstruction |
| `AblationPoints.txt` | Coordinates of the ablated points on the LV reconstruction |

Plus electrograms and 12-lead ECG per point in WFDB format, and a MATLAB bundle.

## Licence

Stated on the record, read directly on 2026-09-25: Creative Commons Attribution-NonCommercial-
ShareAlike 4.0 International Public License.

| Term | What it means for this project |
|---|---|
| NonCommercial | The project is non-commercial research. The dataset is used to test the importer, never sold or bundled into anything sold |
| ShareAlike | Applies to derivatives. The project derives nothing from it: the files are read at test time and nothing produced from them is shipped |
| Never committed | FR-013m already forbids committing any study file. This one is fetched when tests run |

## De-identification

Documented by the publisher, quoted from the record:

> All identifying information that could link data to a given participant has been removed by
> anonymization before public release. The dataset contains no protected health information (PHI)
> or direct identifiers.

Ethics: Independent Ethical Committee of the Azienda Tutela Salute, Sardegna, Prot. n. 351/2021/CE,
approved 2021-07-13, with informed consent.

FR-013n still requires the files themselves to be inspected before use, because a publisher's
statement is a claim. That inspection has not been run yet: the archive is 183 MB and has not been
downloaded. It is a task in feature 003, and its result will be recorded here.

## Limits

| Limit | Effect |
|---|---|
| Geometry is plain text, not the native CARTO format | Proves patient mode, not the CARTO parser. The porcine export proves the parser |
| Left ventricle only | Fine for a first fixture. Atrial maps are not represented |
| Point count per patient about 220 | Well inside any performance budget |

## References

- PhysioNet record, licence and anonymisation statement read 2026-09-25: https://physionet.org/content/argo/1.0.0/
- Licence page: https://physionet.org/content/argo/view-license/1.0.0/
- DOI: 10.13026/8gh2-e660
- Paired fixture: [[openep-testingdata-carto-export]]
- Session: [[log-2026-09-25-eam-datasets]]
