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

## Notes

- Items marked incomplete require spec updates before `/speckit-clarify` or `/speckit-plan`
