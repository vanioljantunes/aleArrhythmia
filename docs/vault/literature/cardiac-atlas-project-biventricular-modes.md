---
title: Cardiac Atlas Project biventricular PCA modes
type: literature
status: active
created: 2026-09-24
updated: 2026-09-24
---


# Cardiac Atlas Project biventricular PCA modes

An openly downloadable statistical shape model of the ventricles, a candidate reference anatomy for
the viewer and for [[fixed-atlas-vertex-space]].

## What it is

| Item | Detail |
|---|---|
| Publisher | Cardiac Atlas Project |
| Files | UKBRVLV.h5 from 630 healthy reference subjects, UKBRVLV_ALL.h5 from 4329 subjects |
| Contents | First 200 principal components, eigenvalues, variance explained, and the mean shape |
| Format | HDF5 |
| Derived from | UK Biobank cardiac magnetic resonance, end diastole and end systole |
| Associated paper | Mauger and others, Journal of Cardiovascular Magnetic Resonance 2019 |

## Coverage

| Covered | Not covered |
|---|---|
| Left ventricle, right ventricle, myocardium, with valve contours | Atria |
| Shape variation across a large population | Electrophysiology of any kind |

## Licence and availability

| Item | Detail |
|---|---|
| Download | Public page, files named above |
| Licence | Not stated on the download page. Recorded as an unknown below |
| Citation requested | The page points to Mauger 2019 and acknowledges Petersen 2017 |

## Consequences for pooling

| Point | Effect |
|---|---|
| A mean shape exists | Gives the project a concrete reference anatomy without building one |
| Population based | The atlas represents a UK Biobank population, which may not match an arrhythmia population. Any map inherits that mismatch |
| No atria | An atrial reference anatomy is still missing |
| Licence unknown | Blocks redistribution inside this repository until settled, since Principle I requires an open licence for data |

## Unknowns

| Unknown | What was tried |
|---|---|
| The licence covering the two HDF5 files | Read the download page, which states no licence. Project policy documents not yet read |
| Whether redistribution of a derived mean mesh is allowed | Follows from the licence, so also unknown |
| Whether an equivalent open atrial atlas exists | Not searched yet |

## References

- Cardiac Atlas Project, Biventricular PCA modes: https://www.cardiacatlas.org/biventricular-modes/
- Mauger and others, Journal of Cardiovascular Magnetic Resonance 2019: 10.1186/s12968-019-0551-6
- Petersen and others, 2017: 10.1186/s12968-017-0327-9
