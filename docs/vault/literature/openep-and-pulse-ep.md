---
title: OpenEP and pulse-ep, open parsers for mapping exports
type: literature
status: active
created: 2026-09-24
updated: 2026-09-24
---


# OpenEP and pulse-ep, open parsers for mapping exports

Two open projects that already read exports from commercial mapping systems. They set the precedent
for the importers in [[ADR-0006-viewer-versions]] and they bound how much this project must build.

## What it is

| Project | Detail |
|---|---|
| OpenEP | A cross-platform data format and analysis platform for electrophysiology research. Converts proprietary exports into one standard format |
| OpenEP paper | Williams and others, Frontiers in Physiology 2021. States implementations for three systems: Carto3, Velocity and Precision |
| OpenEP code | https://github.com/openep/openep-core, Apache-2.0, contains a CARTO importer |
| Later OpenEP coverage | A conference report describes parsers added for KODEX (EPD, Philips), and export in openCARP format |
| pulse-ep | Parses EnSite X export archives into a relational database and exposes the data through several surfaces |

## Coverage

| Covered | Not covered |
|---|---|
| CARTO 3, EnSite Precision, Velocity, KODEX, EnSite X through pulse-ep | Affera, Rhythmia HDx |
| Geometry and electrogram derived scalar fields | The vendor display conventions this project also needs |

## Licence and availability

| Item | Detail |
|---|---|
| OpenEP core | Apache-2.0, compatible with this project's code licence |
| OpenEP language | MATLAB in the core repository. A Python effort is reported elsewhere and not verified here |
| pulse-ep | Public GitHub mirror. Licence not read in this pass |

## Consequences for pooling

| Point | Effect |
|---|---|
| Format work already done | For CARTO the project can follow an existing open parser rather than reverse engineering |
| Licence compatible | Apache-2.0 matches the code licence in [[ADR-0002-licensing]], so reuse or porting is possible |
| Gap remains | Nothing open was found for Affera, the second first-class version in [[ADR-0006-viewer-versions]] |

## Unknowns

| Unknown | What was tried |
|---|---|
| Whether a maintained Python implementation of OpenEP exists | Search only, not confirmed |
| The licence of pulse-ep | Not read |
| Whether the KODEX and EnSite parsers sit in the core repository or elsewhere | Not established |

## References

- Williams and others, OpenEP, Frontiers in Physiology 2021: 10.3389/fphys.2021.646023
- https://github.com/openep/openep-core
- https://openep.io/
- https://github.com/swillert/pulse-ep
- https://touchcardio.com/electrophysiology/journal-articles/102-electroanatomic-mapping-data-analysis-using-openep/
