# Specification Quality Checklist: The first 3D anatomy viewer

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-09-25
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Validation notes

### Iteration 1, 2026-09-25

| Item | Finding |
|---|---|
| No implementation details | Passes. No requirement names a language, library or file format. FR-032 forbids a heavy framework, which is a constraint from Principle VII rather than a technology choice. The source dataset is named because it is the subject of the feature and a licence obligation, not because it is an implementation route |
| Requirements testable | Passes. The one that needed care is FR-025, segment labelling. It is written as a conditional with both branches specified, so it is testable whichever way the empirical question falls |
| Success criteria measurable | Passes, with a caveat recorded below |
| Success criteria technology-agnostic | Passes. The build-step property in FR-030 belongs to the existing site and is inherited from feature 002 |
| Scope bounded | Passes. The Out of scope table names six exclusions, each with a reason |

### Judgement calls worth recording

| Call | Reasoning |
|---|---|
| No clarification markers were raised | Three candidates were considered and all three had defensible answers that did not need the author. Whether segments ship is empirical, so FR-025 specifies both branches. Whether the vendor switch appears was already settled by ADR-0007. Whether to commit the 58 MB source follows from Principle VII and is recorded as an assumption under FR-022 |
| SC-002 says "smooth enough to feel continuous" rather than naming a frame rate | A frame rate is an implementation measure. The user-facing property is whether rotation feels continuous. The plan should turn this into a measurable threshold on named hardware |
| SC-001 and SC-003 say "a normal laptop" and "a normal connection" | Deliberately loose at specification level. The plan must fix what these mean before they can be tested |

### Iteration 2, 2026-09-25, after clarification

Three questions asked and answered. All 16 checkbox items still pass, 16/16 before and after, with
no regressions. What improved was the quality of items that already passed:

| Item | Change |
|---|---|
| Success criteria are measurable | Strengthened. SC-001 to SC-003 previously said "a normal laptop" and "smooth enough". They now state 2 MB, 60,000 triangles, 30 frames per second on integrated graphics, and 2 seconds on a 20 Mbps connection. The caveat recorded in iteration 1 is resolved |
| Requirements are testable, FR-005 | Strengthened. It previously said the viewer must name "whichever" structures it makes separately visible, which dodged the question. It now requires each structure to be independently toggleable |
| Requirements are testable, FR-020 | Strengthened. It previously deferred to "a criterion the documentation states". It now names byte-identical checksum comparison with pinned tool versions |

Two answers introduce a cost the specification now carries openly rather than hiding:

| Cost | Where it is recorded |
|---|---|
| Byte-identical matching fails on any dependency change, and an outside reader years from now is likely to hit that | Clarifications, the assumptions table, FR-020b, and an edge case. FR-020b requires geometry counts beside the hash so the failure is diagnosable |
| The triangle budget and the full structure list may not both be satisfiable | SC-003a and an edge case require the conflict to be recorded rather than resolved silently |

### Iteration 3, 2026-09-25, second clarification session

Four more questions asked and answered. The feature grew: 40 functional requirements to 58, 12
success criteria to 17, four user stories to five. All 16 checkbox items still pass, 16/16 before
and after, no regressions.

The scope changed materially, so two statements that had been true became false and were replaced
rather than left standing:

| Obsolete text | Replaced with |
|---|---|
| Title and input line saying "anatomy only, no statistics" | A description naming both modes |
| "This feature draws that heart and nothing else" | A statement that it adds a second mode and computes nothing |
| FR-013, which forbade any coordinate readout | A rule that every coordinate is stated as belonging to the displayed geometry's own frame |

FR-013 is worth noting as a genuine conflict rather than a tidy-up. The earlier version forbade
showing coordinates at all, on the grounds that doing so would imply a settled reference space. The
author then asked for coordinate entry. Both concerns are satisfied by scoping every coordinate to
the frame of whatever is on screen, which is why the requirement was rewritten instead of deleted.

### Safety requirements added this session

The feature now touches clinical data, which it did not before. These were not requested and are not
negotiable:

| Requirement | Why |
|---|---|
| FR-013j, nothing transmitted | A personal static site must not become a processor of clinical data |
| FR-013k, nothing persisted | Clinical data at rest on a possibly shared machine |
| FR-013m, no study file in the repository | The obvious failure mode for a public project |
| FR-013n, de-identification verified by inspection | Mapping exports routinely carry identifiers in metadata. Being told a file is anonymised is a claim, not a guarantee |

### Open risk carried into planning

The feature depends on a 58 MB research-grade volume mesh that nobody on this project has yet
opened. Three things are unknown and cannot be settled by specification:

| Unknown | Effect if it goes badly |
|---|---|
| Whether the outer surface extracts cleanly | The preprocessing route in US3 becomes harder than assumed |
| How far the surface decimates before anatomy distorts | SC-002 and SC-003 may conflict with FR-005 |
| Whether landmarks for AHA-17 are derivable | FR-025 falls to its disabled branch, which the specification already allows |

These are correctly left to planning, where the mesh can actually be inspected. The specification is
written so that the honest answer to each is acceptable.

Added 2026-09-25, from the second clarification session:

| Unknown | Effect if it goes badly |
|---|---|
| Whether a study export actually contains chamber geometry as well as points | Patient mode depends on it. If an export carries only points, there is nothing to draw them on, and patient mode has no self-consistent frame after all |
| When an anonymised verified export will exist | The importer cannot be written or tested until then. FR-013p keeps the control disabled meanwhile, so the feature still ships without it |
| Whether a real export's point count fits the performance budget | A study with thousands of points may exceed what the viewer can draw smoothly |

The first of these is the one that would hurt. Patient mode is coherent only because geometry and
points are assumed to travel together in the same file. That assumption is recorded and unverified,
and inspecting a real export is what settles it.

Settled 2026-09-25. A real CARTO 3 export was downloaded and read: four mesh files sit beside the
point lists in the same directory. The assumption holds. The second unknown is also answered: two
exports were found the same day, one inspected and clear of identifiers, the other documented as
anonymised by its publisher and awaiting inspection. The third stays open until ARGO is opened.

## Notes

- Items marked incomplete require spec updates before `/speckit-clarify` or `/speckit-plan`
