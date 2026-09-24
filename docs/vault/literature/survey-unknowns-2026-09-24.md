---
title: Survey unknowns as of 2026-09-24
type: literature
status: active
created: 2026-09-24
updated: 2026-09-24
---


# Survey unknowns as of 2026-09-24

Everything the first survey pass could not establish, gathered in one place so that absence is
visible. Each row also lives in the note it belongs to. Required by FR-027.

## Blocking a decision

| Unknown | Blocks | What was tried |
|---|---|---|
| No licence stated for the Cardiac Atlas Project biventricular files | Bundling a reference anatomy, which Principle I requires to be openly licensed. Use and citation are unaffected, and a fetch at setup avoids the problem | Read the download page and the project distribution policy on 2026-09-24. The page states no licence. The policy forbids transferring data or derivatives, but is written for data released under a signed agreement and may not reach an open download |
| What UK Biobank terms apply to a model derived from its images | The same bundling question, one layer down | Not checked |
| Whether Affera exports geometry and points at all | The Affera importer and exporter in [[ADR-0006-viewer-versions]], and with them the whole Affera control under [[ADR-0007-unavailable-capability]] | Searched vendor pages, the FDA approval announcement, trial protocols. Nothing found |
| Whether an open atrial reference anatomy exists | Any atrial arrhythmia work, since the surveyed atlas covers ventricles only | Not searched yet |

## Not blocking yet

| Unknown | What was tried |
|---|---|
| Licence text of the Cobiveco repository | Search described it as permissive. Repository not read |
| Whether a maintained Python implementation of OpenEP exists | Search only |
| Licence of pulse-ep | Not read |
| Where the OpenEP KODEX parser lives | Search found a report, not the code |
| Contents of a Rhythmia HDx Advanced Study Export | Searched vendor documents. Only its existence established |
| Default colour scales, standard views and orientation labels for CARTO 3 and Affera | Not searched yet, needed for the display modes in ADR-0006 |
| Whether an agreed atrial segment model of AHA standing exists | Not searched yet |

## References

- Spec 001, FR-027: `specs/001-theory-vault-traceability/spec.md`
- Notes holding these rows: [[cardiac-atlas-project-biventricular-modes]], [[affera-export]], [[carto3-export]], [[cobiveco-biventricular-coordinates]], [[openep-and-pulse-ep]], [[rhythmia-hdx-export]], [[kodex-epd-export]]
