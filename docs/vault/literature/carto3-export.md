---
title: CARTO 3 export (Biosense Webster)
type: literature
status: active
created: 2026-09-24
updated: 2026-09-24
---


# CARTO 3 export (Biosense Webster)

One of the two systems that get a viewer version in [[ADR-0006-viewer-versions]].

## What it is

| Item | Detail |
|---|---|
| System | CARTO 3, Biosense Webster |
| Export | Studies can be exported for offline analysis. An open parser reads them |
| Evidence | [[openep-and-pulse-ep]]: OpenEP names Carto3 among its supported systems and ships a CARTO importer |

## Coverage

| Covered | Not covered |
|---|---|
| Chamber geometry and mapping points, as consumed by existing open parsers | Exact field list, not read in this pass |

## Licence and availability

| Item | Detail |
|---|---|
| Format documentation | No public vendor specification found in this pass. The knowledge sits in open parsers |
| Reading an export | Precedent exists under Apache-2.0, which suggests no practical barrier to reading files a site already holds |

## Consequences for pooling

| Point | Effect |
|---|---|
| Importer is tractable | An existing open implementation can be followed or ported |
| Display conventions still needed | ADR-0006 requires the display mode, and no source for the default colour scales and views has been gathered yet |

## Unknowns

| Unknown | What was tried |
|---|---|
| Field level structure of an export | Not read. Next step is the OpenEP importer source |
| Default colour scales, standard views and orientation labels | Not searched yet |
| Whether reading exports carries any vendor licence restriction | Not established |

## References

- Williams and others, OpenEP, Frontiers in Physiology 2021: 10.3389/fphys.2021.646023
- https://github.com/openep/openep-core
- Decision that makes this a first-class version: [[ADR-0006-viewer-versions]]
