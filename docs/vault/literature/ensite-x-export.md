---
title: EnSite X EP export (Abbott)
type: literature
status: active
created: 2026-09-24
updated: 2026-09-24
---


# EnSite X EP export (Abbott)

Surveyed, with no build commitment under [[ADR-0006-viewer-versions]].

## What it is

| Item | Detail |
|---|---|
| System | EnSite X EP, Abbott. Successor to EnSite Precision |
| Export | Export archives exist and are read by open tooling |
| Evidence | pulse-ep parses EnSite X export archives. The OpenEP community discusses which export settings produce the files its tools expect. The OpenEP paper lists Precision, the predecessor |

## Coverage

| Covered | Not covered |
|---|---|
| Geometry and per-map data, in files that open tools consume | Exact contents, not read in this pass |

## Licence and availability

| Item | Detail |
|---|---|
| Vendor specification | None found publicly |
| Open parsers | pulse-ep for EnSite X, OpenEP for Precision |

## Consequences for pooling

| Point | Effect |
|---|---|
| A third importer would be cheap later | Two independent open implementations already read this family |
| Not scheduled | ADR-0006 keeps this system in the survey only |

## Unknowns

| Unknown | What was tried |
|---|---|
| Which export setting produces which files, and their fields | Search found a community thread naming per-map comma separated files. The thread was not read in this pass |
| Licence of pulse-ep | Not read |

## References

- https://github.com/swillert/pulse-ep
- OpenEP community thread on EnSite X export settings: https://openep.discourse.group/t/ensitex-data-export-setting-recommendations/108
- Abbott product page: https://www.cardiovascular.abbott/us/en/hcp/products/electrophysiology/mapping-systems/ensite-x.html
