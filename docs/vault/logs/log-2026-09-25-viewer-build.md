---
title: Building the viewer, what the work found
type: log
status: active
created: 2026-09-25
updated: 2026-09-26
---

# Building the viewer, 2026-09-25 to 2026-09-26

Feature 003 was implemented in one long session. This records what building it found that no
earlier note holds, per FR-036. Numbers live in [[derived-heart-geometry]]; this is the narrative.

## Findings, in order

| Found | Where recorded |
|---|---|
| Uniform decimation loses the small structures; eight needed a finer cell, none conflicted with the budget | [[derived-heart-geometry]] |
| Clustering opens small slits and pinches; volume preserved to 0.07 percent; accepted for rendering | [[derived-heart-geometry]] |
| The RV wall touches the LV only along the two insertion bands, so the contact zone is two bands, not the septum | [[derived-heart-geometry]] |
| The insertion check fails: septal arc 101 degrees between band means, 19 degrees from the AHA 3/4 boundary, beyond the 15 degree tolerance. Segments ship disabled | [[derived-heart-geometry]], [[aha-17-segment-model]] |
| The 24 structure ids are named in the Zenodo record itself; the Strocchi 2020 cohort numbers them differently | [[rodero-mesh-contents]] |
| The porcine CARTO export keeps point positions in `<map>_car.txt`, not in `Points_Export.xml`; ablation sites in `VisiTagExport/Sites.txt` | `specs/003-anatomy-viewer/contracts/study-shape.md` |
| ARGO inspected for identifiers: clear. CSV with header rows, 1-based connectivity | [[argo-ventricular-tachycardia-dataset]] |
| The rebuild is byte-identical on Ubuntu in CI as well as on the Windows machine that built it | `.github/workflows/traceability.yml`, run for commit baac91d |
| On Windows a clone under a deep directory breaks at the 260 character path limit; a short path walks the quickstart cleanly, 92 tests passing | `specs/003-anatomy-viewer/quickstart.md` |

## The mapping-system look, 2026-09-26

The author asked for the viewer to look like CARTO 3, from a screenshot of a voltage map. The look
(dark stage, green lesion tags, counter, standard views) needed no decision. The voltage colouring
contradicted FR-006, so [[ADR-0010-study-values-on-the-study-shell]] was drafted and the author
accepted it the same day: a study's own values may colour that study's shell, labelled as the
study's, never on the mean. ARGO carries voltage and activation time per vertex; the CARTO export
carries bipolar and unipolar voltage per mapped point only, on the same line as the position, so
there the points are coloured and the shell is not. The CARTO axis convention was found in two
open-source readers and recorded in [[carto3-export]]; ARGO's publisher states none, so the
standard views stay disabled on an ARGO study.

## The starting view

The first still image looked down the long axis from the base. Rather than hand-tune a camera,
the build now measures two vectors on the source coordinates, the long axis from the apicobasal
coordinate and the anterior direction from the right ventricle's position, and records them in the
manifest. The page starts from them. The still image is anterior with the base up.

## What is not done

| Item | State |
|---|---|
| Public route | Waits on feature 002's publication job. The viewer is proven on the local server only |
| Link from the section page | Lands with that job; the local preview builder carries it |
| Segments | Disabled by evidence. The open question in [[aha-17-segment-model]] is the way forward |
| Affera import | Disabled, no public format |

## AI assistance

The session used an AI coding assistant for drafting code, notes and tests under the author's
direction; every measurement above was produced by running the code on the real files, and every
decision was the author's.

## References

- Tasks and their state: `specs/003-anatomy-viewer/tasks.md`
- Decisions embodied: [[ADR-0007-unavailable-capability]], [[ADR-0008-reference-anatomy]], [[ADR-0009-study-data-in-the-browser]]
- Previous session: [[log-2026-09-25-eam-datasets]]
