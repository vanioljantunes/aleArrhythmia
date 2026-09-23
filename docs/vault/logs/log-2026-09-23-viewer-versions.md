---
title: Viewer versions for CARTO and Affera
type: log
status: active
created: 2026-09-23
updated: 2026-09-23
---

# Viewer versions, 2026-09-23

Author asked for the map to have a CARTO version and an Affera version, switchable. Session run
with an AI coding assistant (Claude).

## Questions and answers

| # | Question | Options offered | Answer | Record |
|---|---|---|---|---|
| 1 | What changes when the user switches version? | Adapter plus display mode (recommended); display mode only; adapter only | Adapter plus display mode | [[ADR-0006-viewer-versions]] |
| 2 | Do CARTO and Affera replace the three systems already named, or join them? | Two first-class, others surveyed (recommended); all five first-class; only these two | Two first-class, others stay in the survey | [[ADR-0006-viewer-versions]] |

## Checked during the session

| Claim | Source | Result |
|---|---|---|
| An open parser for CARTO 3 exports exists | https://github.com/openep/openep-core | Confirmed, Apache-2.0, CARTO importer present |
| OpenEP names its supported systems | 10.3389/fphys.2021.646023 | Confirmed: Carto3, Velocity, Precision |
| An open parser for Affera exports exists | Not found | Recorded as an unknown in ADR-0006 |

## Follow-ups

| Item | Where |
|---|---|
| Survey notes for CARTO 3 and Affera, with export formats and display conventions | US4 of spec 001 |
| Build the two versions | Phase 2, viewer, not this phase |
