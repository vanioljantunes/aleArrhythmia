---
title: Rhythmia HDx export (Boston Scientific)
type: literature
status: active
created: 2026-09-24
updated: 2026-09-24
---


# Rhythmia HDx export (Boston Scientific)

Surveyed, with no build commitment under [[ADR-0006-viewer-versions]].

## What it is

| Item | Detail |
|---|---|
| System | Rhythmia HDx, Boston Scientific |
| Export | An Advanced Study Export exists. It appears in a clinical trial protocol as the route by which study data leaves the system onto external media |
| Related | LabSystem Pro is described as giving access to electrophysiology study data outside the laboratory |

## Coverage

| Covered | Not covered |
|---|---|
| That an export path exists | What the export contains, and in what format |

## Licence and availability

| Item | Detail |
|---|---|
| Vendor specification | None found publicly |
| Open parser | None found |

## Consequences for pooling

| Point | Effect |
|---|---|
| Cannot be scheduled yet | With no format knowledge and no open parser, an importer would start from nothing |
| Export exists | The path is not closed, which is the useful part of this finding |

## Unknowns

| Unknown | What was tried |
|---|---|
| Contents and format of an Advanced Study Export | Web search across the vendor site, instructions for use documents and trial protocols. Only the existence of the export was established |
| Whether any research group has parsed it openly | Search found nothing |

## References

- Boston Scientific, Rhythmia HDx system pages: https://www.bostonscientific.com/en-US/medical-specialties/electrophysiology/cardiac-mapping-system/.html
- Instructions for use, Rhythmia HDx software 6.0: https://www.bostonscientific.com/content/dam/elabeling/ep/rhythmia-mapping-system/rhythmia_6-0_mappingsystem/51660906-01A_RHY_HDX_SW_6.0_IFU_OUS_ML_s.pdf
