---
title: aleArrhythmia theory vault
type: theory
status: active
created: 2026-09-21
updated: 2026-09-21
---

# aleArrhythmia theory vault

Activation Likelihood Estimation adapted from brain imaging to cardiac electrophysiology, so that
arrhythmia origins reported in separate studies can be pooled into one map.

New here: read [[README]] first.

> Research use only. Not a medical device. Nothing here is a clinical recommendation, and in the
> current phase nothing here is a claim about cardiac results.

## Decision records

| Record | Decision | Status |
|---|---|---|
| [[ADR-0001-repository-layout]] | Own standalone public repository | accepted |
| [[ADR-0002-licensing]] | Apache-2.0 for code, CC-BY-4.0 for prose | accepted |
| [[ADR-0003-enforcement-mechanism]] | Pre-push hook plus a check on every push | accepted |
| [[ADR-0004-citation-scan-scope]] | Scan all tracked text files, minus a reasoned ignore list | accepted |
| [[ADR-0005-writing-style]] | Writing rules; mechanical tells blocked, AI vocabulary warned | accepted |
| [[ADR-0006-viewer-versions]] | CARTO and Affera viewer versions, switchable, adapter plus display mode | accepted |
| [[ADR-0007-unavailable-capability]] | A committed but blocked capability shows as a disabled control naming the gap | accepted |

## Open questions

| Question | Status |
|---|---|
| [[canonical-reference-space]] | open |

## Theory

| Note | Content |
|---|---|
| [[ale-method]] | What ALE does, and which steps change for the heart |

## Literature

Candidate reference spaces:

| Note | What it is |
|---|---|
| [[universal-ventricular-coordinates]] | Continuous ventricular coordinates |
| [[cobiveco-biventricular-coordinates]] | Later biventricular coordinates, open code |
| [[universal-atrial-coordinates]] | Atrial coordinates, open access |
| [[aha-17-segment-model]] | Discrete clinical segments |
| [[fixed-atlas-vertex-space]] | Vertex indices on one template |
| [[hybrid-coordinate-and-segment]] | Continuous storage, segment labels |

Reference anatomy and tooling:

| Note | What it is |
|---|---|
| [[cardiac-atlas-project-biventricular-modes]] | Open statistical shape model of the ventricles |
| [[openep-and-pulse-ep]] | Open parsers for commercial mapping exports |

Mapping system exports:

| Note | Status |
|---|---|
| [[carto3-export]] | First-class version, open parser exists |
| [[affera-export]] | First-class version, no public format found |
| [[ensite-x-export]] | Surveyed, open parser exists |
| [[rhythmia-hdx-export]] | Surveyed, export exists, format unknown |
| [[kodex-epd-export]] | Surveyed, parser reported |

Gaps:

| Note | What it is |
|---|---|
| [[survey-unknowns-2026-09-24]] | Everything the first survey pass could not establish |

## Work logs

| Log | Content |
|---|---|
| [[log-2026-09-20-clarification]] | Session that settled layout, enforcement, scan scope and licence |
| [[log-2026-09-21-enforcement-verification]] | Proof that hook and workflow each refuse a broken record |
| [[log-2026-09-21-reader-trial-adr-0001]] | Author reading of ADR-0001; led to ADR-0005 |
| [[log-2026-09-23-viewer-versions]] | Session that asked for CARTO and Affera versions of the map |
| [[log-2026-09-24-survey-and-gaps]] | Survey landed; atlas licence read, Affera control settled |

## Templates

| Template | For |
|---|---|
| templates/adr.md | A decision record |
| templates/theory.md | A derivation or method note |
| templates/literature.md | One surveyed source, atlas, file format or system |
| templates/question.md | An open question |
| templates/log.md | A dated working session |

Templates are excluded from the checks, so their placeholders fail nothing.

Every decision record and open question must appear on this page. The checker fails when one is
missing.
