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
| Download | Public page, open link, no login and no click-through agreement |
| Licence | Not stated on the download page, nor anywhere the page links to |
| Citation requested | The page points to Mauger 2019 and acknowledges Petersen 2017 |
| Project policy | A separate document governs data distribution. Read 2026-09-24 |

What the policy says, for data obtained under a Data Distribution Agreement:

| Clause | Text |
|---|---|
| 6, Security and Restricted Transfer | The user retains control of data and of unmodified or modified derivatives, and does not transfer them, with or without charge, to any other entity or individual, in a manner not previously approved |
| 14, Commercial Use | The user cannot use data for commercial use without the permission of the Contributing Studies |
| 4, Acknowledgements | The user acknowledges the Contributing Studies, their funding sources, the project and its funder |

Whether those clauses reach this download is unresolved. They govern data released under a signed
agreement, and these two files are a plain public download with no agreement attached. The absence
of a stated licence is decisive on its own: nothing grants redistribution, and silence is not
permission.

## What the project may do

| Action | Status |
|---|---|
| Download and use the files | Permitted. The page offers them openly |
| Cite the atlas and the papers | Permitted, and expected |
| Ship the files inside this repository | Not permitted. No licence grants it, and clause 6 points the other way |
| Ship a mesh derived from them | Same answer. Clause 6 names modified derivatives explicitly |
| Any commercial use | Needs permission of the Contributing Studies |

Way around it, without asking anyone: the project fetches the file at setup from the publisher, so
the user obtains it directly and the project never transfers it. This is how the dependency will be
carried until a licence is stated.

Underneath this sits another layer. The modes derive from UK Biobank, which imposes its own terms
on derived data. Not checked, recorded below.

## Consequences for pooling

| Point | Effect |
|---|---|
| A mean shape exists | Gives the project a concrete reference anatomy without building one |
| Population based | The atlas represents a UK Biobank population, which may not match an arrhythmia population. Any map inherits that mismatch |
| No atria | An atrial reference anatomy is still missing |
| No stated licence | Blocks redistribution inside this repository, since Principle I requires a positive open licence for data. Does not block use, so the dependency could be carried by fetching at setup |
| Superseded in practice, 2026-09-25 | The project no longer needs this file. [[ADR-0008-reference-anatomy]] adopts an Attribution-licensed four-chamber mesh instead, and [[nagel-biatrial-shape-model]] covers the atria. This note stays because the reasoning that led here is worth keeping |

## Unknowns

| Unknown | What was tried |
|---|---|
| Whether the publisher would state an open licence if asked | Not asked. A single request would settle bundling permanently |
| Whether the distribution policy binds this open download at all | Read the policy in full 2026-09-24. It is written for data released under a signed agreement, and does not say whether it reaches unsigned public downloads |
| What UK Biobank terms apply to a model derived from its images | Not checked |
| Whether an equivalent open atrial atlas exists | Not searched yet |

## References

- Cardiac Atlas Project, Biventricular PCA modes: https://www.cardiacatlas.org/biventricular-modes/
- CAP Policies and Procedures for Data Distribution to Users, read 2026-09-24: https://www.cardiacatlas.org/wp-content/uploads/2022/10/CAPPolicyStatementUsers.pdf
- Mauger and others, Journal of Cardiovascular Magnetic Resonance 2019: 10.1186/s12968-019-0551-6
- Petersen and others, 2017: 10.1186/s12968-017-0327-9
