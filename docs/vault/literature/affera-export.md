---
title: Affera export (Medtronic)
type: literature
status: active
created: 2026-09-24
updated: 2026-09-24
---


# Affera export (Medtronic)

The second system that gets a viewer version in [[ADR-0006-viewer-versions]], and the one with the
least public information.

## What it is

| Item | Detail |
|---|---|
| System | Affera Mapping and Ablation System with the Sphere-9 catheter, Medtronic |
| Approval | FDA approval announced 2024-10-24 |
| Function | Stores and displays catheter location, builds a geometric shell of the chamber, collects electrograms and displays voltage on the shell |

## Coverage

| Covered | Not covered |
|---|---|
| Nothing established about exported files | Whether geometry and points can leave the system at all, and in what format |

## Licence and availability

| Item | Detail |
|---|---|
| Public format documentation | None found |
| Open parser | None found |

## Consequences for pooling

| Point | Effect |
|---|---|
| Blocks the Affera importer and exporter | Without a readable export there is no adapter, and the version reduces to a display mode |
| Does not block the display mode | Colour scales and views could still be matched from published figures and manuals |
| Names the next step | Ask Medtronic, or find a site willing to share an anonymised export, before Phase 2 planning |

## Unknowns

| Unknown | What was tried |
|---|---|
| Whether Affera exports geometry and points in any documented form | Web search over Medtronic product pages, the FDA approval announcement, Medtronic Academy, clinical trial protocol documents and research use descriptions. Nothing found |
| Whether research collaborations have obtained exports | Not searched |
| Default colour scales and standard views | Not gathered yet, though published figures exist |

## References

- Medtronic news, FDA approval of the Affera system, 2024-10-24: https://news.medtronic.com/2024-10-24-A-new-paradigm-in-electrophysiology-Medtronic-receives-FDA-approval-of-Affera-TM-Mapping-and-Ablation-System-and-Sphere-9-TM-Catheter
- Medtronic product page: https://www.medtronic.com/en-us/healthcare-professionals/products/surgical-energy/ablation/mapping-ablation-products/affera-mapping-system.html
- Decision that makes this a first-class version: [[ADR-0006-viewer-versions]]
