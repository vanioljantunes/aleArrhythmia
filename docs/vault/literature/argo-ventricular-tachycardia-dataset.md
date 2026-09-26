---
title: ARGO, an anonymised human ventricular tachycardia mapping dataset
type: literature
status: active
created: 2026-09-25
updated: 2026-09-26
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

FR-013n requires the files themselves to be inspected before use, because a publisher's statement
is a claim. The inspection was run on 2026-09-26 on the archive as downloaded from PhysioNet,
SHA-256 `2f25614704d62ebf30d80adec25f8b09e962ddf68fcd094c770704f0fa7f132e`, 191,810,852 bytes, 11,827 entries.

| Check | Method | Finding |
|---|---|---|
| Layout | Listed every entry | One root folder; `ARGODataset_Folder/Pt1` to `Pt9`; a MATLAB folder; `README.txt`, `LICENSE.txt`, `RECORDS`, `ANNOTATORS`, `SHA256SUMS.txt`, `Additional_subject_data.csv` |
| Dates | Regular expressions for day/month/year and year-month-day over every text file | None |
| Names, birth, record numbers, institutions | Word list in English and Italian over every text file | Hits only in `README.txt` and the MATLAB read-me, where "patient" is used generically |
| File paths | Drive letters, home directories, backslashes | None |
| Email addresses | Pattern over every text file | One, the dataset author's contact in the MATLAB read-me. Binary `.dat` files produced noise, not addresses |
| WFDB headers | Read `.hea` files | Record name, sampling rate, signal descriptors and lead names only. No age, sex or comment lines |
| Subject-level CSV | Read in full | Nine rows: sex, age in years, ejection fraction, point count. No date of birth, no names |
| Geometry files | Letter search in the five named files per patient | Header rows only (`X,Y,Z`, `node1,node2,node3`, `Point,X,Y,Z`, `Voltage,LAT`) and `NaN` |

Inspection result: clear. Nothing in the archive identifies a person. The reader opens only the
four geometry and point files; the subject CSV, the read-mes and the electrograms are never read.

## Formats, as found

| File | Format | Per patient |
|---|---|---|
| `XYZmesh.txt` | CSV, header `X,Y,Z`, millimetres | 3,795 to 7,193 vertices |
| `ConnectivityList.txt` | CSV, header `node1,node2,node3`, 1-based | 7,586 to 14,382 triangles |
| `POS_POINTS.txt` | CSV, header `Point,X,Y,Z` | 46 to 839 points, 1,962 in total |
| `AblationPoints.txt` | CSV, header `X,Y,Z` | 32 to 233 points |
| `MESHcoloring.txt` | CSV, header `Voltage,LAT`, one row per vertex, `NaN` where unmapped | Read only when the value control is on, since [[ADR-0010-study-values-on-the-study-shell]] |

## Coordinate frame

Searched 2026-09-26: the PhysioNet page, the paper and its S1 file describe the files as X, Y, Z
coordinates and say nothing about which patient direction each axis points to. The geometry came
out of CARTO 3, so the CARTO frame recorded in [[carto3-export]] is the likely one, but that is an
inference. The viewer therefore keeps the standard views disabled on an ARGO study, with that reason.

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
