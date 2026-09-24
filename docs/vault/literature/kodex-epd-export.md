---
title: KODEX-EPD export (Philips)
type: literature
status: active
created: 2026-09-24
updated: 2026-09-24
---


# KODEX-EPD export (Philips)

Surveyed, with no build commitment under [[ADR-0006-viewer-versions]].

## What it is

| Item | Detail |
|---|---|
| System | KODEX-EPD, Philips, originally EPD Solutions. A dielectric imaging and mapping system |
| Export | A report on OpenEP states that parsers were added for KODEX, which implies a readable export |
| Evidence | [[openep-and-pulse-ep]] |

## Coverage

| Covered | Not covered |
|---|---|
| That open parsing has been done | The format itself, not read in this pass |

## Licence and availability

| Item | Detail |
|---|---|
| Vendor specification | None found publicly |
| Open parser | Reported within the OpenEP project. Exact repository and licence not confirmed |

## Consequences for pooling

| Point | Effect |
|---|---|
| Plausible later addition | Prior open work reduces the cost if this system is promoted to a version |
| Not scheduled | ADR-0006 keeps it in the survey only |

## Unknowns

| Unknown | What was tried |
|---|---|
| Where the KODEX parser lives and under what licence | Search found a conference report describing it, not the code |
| Format contents | Not established |

## References

- Report describing OpenEP parsers including KODEX: https://touchcardio.com/electrophysiology/journal-articles/102-electroanatomic-mapping-data-analysis-using-openep/
- Philips announcement of KODEX-EPD enhancements: https://www.philips.com/a-w/about/news/archive/standard/news/press/2020/20200826-philips-announces-new-imaging-and-workflow-enhancements-for-kodex-epd-cardiac-imaging-and-mapping-system-to-treat-heart-rhythm-disorders.html
