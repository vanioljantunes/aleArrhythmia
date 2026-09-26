---
title: Finding a mapping export the importer can be built against
type: log
status: active
created: 2026-09-25
updated: 2026-09-25
---


# Mapping datasets, 2026-09-25

The importer was blocked: nobody had a CARTO export, and the author chose to obtain a verified
anonymised one before writing it rather than build against a synthetic file. A search found two
that serve, and one that does not. Session run with an AI coding assistant (Claude).

## Question and answer

| Question | Options offered | Answer |
|---|---|---|
| Which datasets does the importer get built and verified against? | Porcine export plus the ARGO human set (recommended); porcine only; add the OpenEP MATLAB files | Porcine export plus ARGO |

## Checked during the session

| Claim | Source | Result |
|---|---|---|
| The porcine export is CC BY 4.0 | https://zenodo.org/records/6651600 | Confirmed by reading the record |
| It is a real CARTO 3 export with geometry and points | Downloaded and extracted | Confirmed. 4 mesh files, 4 point lists, per-point positions, ECG, contact force |
| It carries no personal identifiers | Every file searched | Confirmed. Hits were map and structure names only |
| ARGO is anonymised and ethically approved | https://physionet.org/content/argo/1.0.0/ | Confirmed by reading the record. Files not yet inspected |
| ARGO licence | Same record | CC BY-NC-SA 4.0, read directly |
| The OpenEP paper's datasets carry a data licence | Paper read in full, repository read | Not established. The article is CC BY; the MATLAB files in the examples repository carry only the repository's GPL-3.0 with no statement covering data, and no anonymisation statement anywhere |

## Rejected

| Dataset | Why |
|---|---|
| OpenEP example MATLAB files | Richest content, 1,366 points with a full map, but no licence names the data and nobody has documented de-identification. FR-013n could inspect them; it cannot supply a licence that was never granted. Kept as a reference for what a complete import should contain, never as a fixture |

## What changed

| Before | After |
|---|---|
| Importer blocked on obtaining an export | Two fixtures identified, one already inspected |
| Assumption that exports carry geometry as well as points, unverified | Verified on the porcine export |
| FR-013p keeps the import control disabled | Can lift for CARTO once the importer passes against both fixtures |

## Follow-ups

| Item | Where |
|---|---|
| Download ARGO and run the FR-013n inspection on the files themselves | Feature 003 task |
| Confirm with the OpenEP author why the same content is CC BY 4.0 on Zenodo and GPL-3.0 on GitHub | Not blocking. The Zenodo deposit is the one relied on |
