---
title: Phase 0 survey, and what to do about its gaps
type: log
status: active
created: 2026-09-24
updated: 2026-09-24
---

# Survey and gaps, 2026-09-24

The Phase 0 survey landed and returned two blocking unknowns. The author asked what the licence
finding means in practice, and how the viewer should show a version that cannot work yet. Session
run with an AI coding assistant (Claude).

## Questions and answers

| # | Question | Options offered | Answer | Record |
|---|---|---|---|---|
| 1 | Does the atlas licence finding mean the project may not use it? | Answered from the source, no options offered | Use is fine. Redistribution is not permitted, and commercial use needs permission | [[cardiac-atlas-project-biventricular-modes]] |
| 2 | When a user picks Affera, how much should work? | Display mode live and import blocked (recommended); whole mode a placeholder; control greyed out | Control greyed out until it works | [[ADR-0007-unavailable-capability]] |

## Checked during the session

| Claim | Source | Result |
|---|---|---|
| The atlas download page states terms | https://www.cardiacatlas.org/biventricular-modes/ | Confirmed: no licence, no terms, no registration on the page |
| A project-level policy governs reuse | CAP Policies and Procedures for Data Distribution to Users | Confirmed. Clause 6 forbids transfer of data or derivatives to any other entity. Clause 14 forbids commercial use without permission of the Contributing Studies |
| Those clauses bind an open download | Same document | Not established. They govern data obtained under a signed Data Distribution Agreement, and the modes are a plain public download with no agreement |

## Consequences recorded

| Finding | Effect |
|---|---|
| No stated licence defaults to all rights reserved | Principle I needs a positive open licence, so bundling is blocked |
| Use and citation are unaffected | The project may still depend on the atlas |
| A fetch at setup avoids redistribution | The user downloads the file themselves, so the project never transfers it |
| Asking the publisher to state a licence would settle it | Recorded as a follow-up, not yet done |

## Follow-ups

| Item | Where |
|---|---|
| Ask the Cardiac Atlas Project to state a licence on the download page | Not yet sent |
| Check UK Biobank terms on derived data, which sit underneath the atlas | Not yet done |
| Build the disabled-control pattern | Phase 2, viewer |
