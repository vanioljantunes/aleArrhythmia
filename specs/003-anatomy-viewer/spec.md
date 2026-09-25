# Feature Specification: The first 3D anatomy viewer

**Feature Branch**: `main`

**Created**: 2026-09-25

**Status**: Draft

**Input**: User description: build the first 3D anatomy viewer as a page inside the project's web section. Anatomy only, no statistics. The anatomy is the Rodero average four-chamber mesh adopted in ADR-0008.

## Context

The project's name promises a likelihood map on a heart. It has neither a statistical core nor a
reference space, and until now it had no anatomy it was allowed to ship either. ADR-0008 settled the
last of those: the Rodero average four-chamber mesh is licensed CC-BY-4.0 and may be bundled with
attribution.

This feature draws that heart and nothing else.

| In | Out |
|---|---|
| A reference heart a reader can rotate, zoom and inspect | Any likelihood map |
| Provenance, licence and attribution visible to the reader | Any focus, coordinate or study data |
| A reproducible route from the published source file to web geometry | Any ALE computation |
| Honest statements about what is not yet decided | Any claim about arrhythmia |

The restraint is the point. A viewer that showed a coloured overlay would be read as a result, and
there is no result. Feature 001 built machinery specifically to stop that happening.

## Clarifications

### Session 2026-09-25

- Q: SC-001 to SC-003 used vague adjectives. What is the budget for the shipped geometry? -> A: At
  most 2 MB compressed and 60,000 triangles, holding at least 30 frames per second while rotating on
  integrated graphics, with the model first visible within 2 seconds on a 20 Mbps connection.
- Q: What can the reader do with the structures the source labels separately? -> A: Toggle each one
  on and off. Hiding a structure reveals what sits behind it. Rejected: fixed colours with a legend
  only, which is barely more than a picture; and per-structure opacity, which adds interface this
  feature does not need yet.
- Q: How does someone rebuilding the geometry prove their result matches what ships? -> A: A
  byte-identical checksum of the output, with the preprocessing tool versions pinned. Accepted with
  the known cost that a dependency change makes it fail. To keep such a failure diagnosable rather
  than mysterious, the geometry counts are recorded alongside the hash, so a mismatch can be told
  apart from a shape change. Rejected: geometric tolerance, which survives version drift but was not
  chosen; and a manifest with no automated check, which is not a check.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A visitor sees the heart (Priority: P1)

Someone reading the project's section opens the viewer and turns a three-dimensional heart around.
They install nothing.

**Why this priority**: This is the feature. Everything else supports it.

**Independent Test**: Open the viewer page, drag to rotate, scroll to zoom, and confirm the geometry
responds smoothly and reads as a heart.

**Acceptance Scenarios**:

1. **Given** the project's section page, **When** the visitor opens the viewer, **Then** a
   three-dimensional heart appears without further action
2. **Given** the heart is displayed, **When** the visitor drags, **Then** it rotates about its centre
3. **Given** the heart is displayed, **When** the visitor zooms, **Then** the view scales and stays
   centred, with limits that prevent the model being lost off screen
4. **Given** the visitor has moved the view, **When** they ask to reset it, **Then** the original
   orientation returns

---

### User Story 2 - The reader knows what they are looking at (Priority: P1)

The reader can tell, without leaving the page, that this is a population average rather than a
patient, who made it, under what licence, and that the project claims nothing from it yet.

**Why this priority**: Equal to US1. An unlabelled heart on a page named after arrhythmia invites
exactly the wrong conclusion. Principles IV and VI both bind here, and the licence requires credit.

**Independent Test**: Show the page to someone who has never seen the project and ask what the heart
is. They should say it is an average, not a patient, and should be able to find its source.

**Acceptance Scenarios**:

1. **Given** the viewer, **When** the visitor reads the page, **Then** it states the mesh is a
   population mean and not any individual's anatomy
2. **Given** the viewer, **When** the visitor looks for the source, **Then** the dataset, its authors,
   its identifier and its licence are named, and the identifier resolves
3. **Given** the viewer, **When** the visitor reads the page, **Then** the research-use statement is
   present
4. **Given** the viewer, **When** the visitor looks for a result, **Then** the page states plainly
   that no statistical result is shown and that no reference space has been chosen yet

---

### User Story 3 - Anyone can reproduce the geometry (Priority: P2)

A reader who doubts the shape can start from the published dataset, run the documented steps, and
obtain the same geometry the viewer uses.

**Why this priority**: Principle VIII, traceable by construction. A mesh that appeared with no route
back to its source is exactly the unsourced assertion the project forbids in prose. Below the first
two only because the viewer has value the moment it is honest.

**Independent Test**: On a clean machine, follow the documented steps from the published source file
and confirm the output matches what ships, by a stated comparison.

**Acceptance Scenarios**:

1. **Given** the repository, **When** a reader looks for how the geometry was made, **Then** the steps
   are documented and runnable
2. **Given** those steps, **When** they are run on the published source, **Then** the result matches
   the shipped geometry by a stated and checkable criterion
3. **Given** the shipped geometry, **When** anyone inspects the repository, **Then** it records which
   source file and which settings produced it

---

### User Story 4 - The page is honest about what it cannot do (Priority: P2)

The reader can see that vendor versions and segment labelling are intended, are not available, and
why.

**Why this priority**: ADR-0007 already decided how the project presents a committed but unavailable
capability. This is the first feature with controls to apply it to.

**Independent Test**: Look for the vendor switch and the segment control, and confirm each is visibly
present, not operable, and states why and as of when.

**Acceptance Scenarios**:

1. **Given** the viewer, **When** the visitor looks at the vendor controls, **Then** both are present
   and disabled, each naming the reason and the date it was last checked
2. **Given** a disabled control, **When** the visitor wants the detail, **Then** it links to the note
   holding the evidence

---

### Edge Cases

| Case | Expected |
|---|---|
| The device cannot render 3D at all | A stated message and a still image of the heart, never a blank area |
| Scripting is unavailable | The page still explains what the viewer is, what the mesh is, and its licence |
| The geometry fails to load | A stated error within a bounded wait, and a route back, never an endless wait |
| A slow connection | The page is readable before the geometry arrives, and shows that it is still loading |
| A low-powered laptop | Interaction stays smooth enough to use, or the viewer reduces detail and says so |
| A phone | The heart is usable with touch, and the page does not scroll sideways |
| The visitor rotates the model into an unreadable position | A reset control returns the original view |
| The visitor hides every structure | The viewer says so and offers a way to restore them, rather than showing an empty area that reads as a failure |
| Decimation to the triangle budget would lose a structure | The conflict is recorded as a finding, not resolved silently by dropping the structure or quietly exceeding the budget |
| A rebuild produces a different checksum | The recorded geometry counts show whether the shape changed or only a dependency version did |
| Someone assumes the colours mean something | No colour on the model encodes any measurement, and the page says so |

## Requirements *(mandatory)*

### Functional requirements, the viewer

- **FR-001**: The viewer MUST display the reference heart in three dimensions on a page inside the
  project's existing web section.
- **FR-002**: The visitor MUST be able to rotate the model continuously about its centre.
- **FR-003**: The visitor MUST be able to zoom, within limits that keep the model on screen.
- **FR-004**: The viewer MUST offer a control that restores the initial view.
- **FR-005**: The viewer MUST show the anatomical structures the source distinguishes, MUST name each
  one, and MUST let the reader turn each one on and off independently.
- **FR-005a**: Hiding a structure MUST reveal whatever lies behind it, so that inner chambers can be
  inspected.
- **FR-005b**: When every structure is hidden, the viewer MUST say so and MUST offer a way to restore
  them, rather than presenting an empty area that reads as a failure.
- **FR-006**: No colour, shade or marking on the model may encode a measurement, a probability or any
  other result. Colour MAY distinguish anatomical structures only.
- **FR-007**: The viewer MUST work with touch input as well as pointer input.
- **FR-008**: The page MUST remain readable at phone width and MUST NOT scroll sideways.

### Functional requirements, honesty

- **FR-009**: The page MUST state that the mesh is a population mean and is not any individual's
  anatomy.
- **FR-010**: The page MUST state that no statistical result is displayed.
- **FR-011**: The page MUST state that no canonical reference space has been chosen, and MUST mark
  the viewer exploratory, as Principle II requires until that choice is recorded.
- **FR-012**: The page MUST carry the research-use statement: a research tool, not a medical device,
  and nothing here should guide a procedure.
- **FR-013**: The viewer MUST NOT display any coordinate readout, axis label or grid that would imply
  a coordinate system has been settled.

### Functional requirements, provenance and licence

- **FR-014**: The page MUST name the dataset, its authors, its persistent identifier and its licence.
- **FR-015**: The persistent identifier MUST resolve to the published record.
- **FR-016**: The repository MUST record the licence of the bundled geometry separately from the
  licence of the software, so that the boundary between them is legible.
- **FR-017**: The attribution the licence requires MUST be present both in the repository and on the
  page the reader sees.
- **FR-018**: The repository MUST record which source file and which preprocessing settings produced
  the shipped geometry.

### Functional requirements, reproducibility

- **FR-019**: The route from the published source file to the shipped geometry MUST be documented and
  runnable by someone who has only the repository and the public dataset.
- **FR-020**: Running that route on the published source MUST produce a file byte-identical to the
  shipped geometry, verified against a published checksum.
- **FR-020a**: The exact versions of every tool the preprocessing depends on MUST be pinned and
  recorded, since byte-identical output requires them.
- **FR-020b**: The geometry counts MUST be recorded alongside the checksum, so that a failed match
  can be told apart from a changed shape. A checksum alone cannot distinguish a dependency update
  from a different heart.
- **FR-021**: The preprocessing MUST record what it did, including how much detail it removed.
- **FR-022**: The source dataset MUST NOT be committed to the repository in full. Only the derived,
  web-sized geometry ships.

### Functional requirements, unavailable capabilities

- **FR-023**: The vendor controls for CARTO and Affera MUST appear, MUST be disabled, and MUST each
  state the reason and the date last checked, as ADR-0007 requires.
- **FR-024**: Each disabled control MUST link to the note holding the evidence for its gap.
- **FR-025**: AHA 17-segment labelling MUST ship only if the segments can be placed from landmarks
  actually derivable from the mesh. If they cannot, the control MUST appear disabled under ADR-0007,
  stating that the landmarks are not available, and the attempt MUST be recorded as a finding.
- **FR-026**: The viewer MUST NOT display approximate or guessed segment boundaries. Segments are
  either derived and correct, or absent and stated as absent.

### Functional requirements, robustness and weight

- **FR-027**: A device that cannot render three dimensions MUST receive a stated message and a still
  image, never an empty area.
- **FR-028**: A failure to load the geometry MUST produce a stated error within a bounded wait.
- **FR-029**: The page MUST be readable before the geometry finishes loading, and MUST show that
  loading is in progress.
- **FR-030**: The website MUST continue to work without a build step, as feature 002 requires.
- **FR-031**: Geometry MUST be served next to the site, not requested from a third party when the
  reader opens the page.
- **FR-032**: The viewer MUST NOT introduce a heavy application framework, per Principle VII.

### Functional requirements, traceability

- **FR-033**: The existing traceability checks MUST continue to pass.
- **FR-034**: Any prose added by this feature MUST satisfy the project's writing rules.
- **FR-035**: No output of this feature may reference the author's personal folder organisation.
- **FR-036**: Whatever this feature establishes about the mesh, including anything it fails to
  establish, MUST be recorded in the vault rather than left in code comments.

### Key entities

| Entity | What it is |
|---|---|
| **Source dataset** | The published four-chamber mesh, with its identifier, authors and licence |
| **Derived geometry** | The web-sized surface the viewer draws, with a record of how it was made |
| **Structure** | One named anatomical part the source distinguishes, for example a chamber or a vessel |
| **Provenance record** | What links the derived geometry back to the source file and the settings used |
| **Disabled capability** | A control that is present but not operable, with its reason and date |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The model is first visible within 2 seconds of the page opening, measured on a 20 Mbps
  connection.
- **SC-002**: Rotation holds at least 30 frames per second on a laptop with integrated graphics.
- **SC-003**: The shipped geometry is at most 2 MB compressed and at most 60,000 triangles.
- **SC-003a**: Every structure the source distinguishes remains separately visible and nameable at
  that triangle budget. If decimation to 60,000 triangles loses a structure, the budget is wrong and
  the conflict is recorded rather than resolved silently.
- **SC-004**: A reader who has never seen the project can state, after reading the page alone, that
  the heart is an average rather than a patient, and can name the licence.
- **SC-005**: 100 percent of the provenance claims on the page resolve: the identifier reaches the
  published record, and the named licence matches what that record states.
- **SC-006**: An independent reader can reproduce the shipped geometry from the published dataset by
  following the documented steps, and confirm the match by the stated criterion.
- **SC-007**: Zero elements of the rendered model encode any measurement or result.
- **SC-008**: Every capability the project has committed to but cannot yet provide is visible as a
  disabled control naming its reason and date.
- **SC-009**: The page is usable on a phone: the heart can be rotated by touch and the page body does
  not scroll sideways.
- **SC-010**: A device without 3D support shows a stated message and a still image, never an empty
  area.
- **SC-011**: The traceability checks pass with this feature complete.

## Assumptions

| Assumption | Basis |
|---|---|
| The viewer is a page within the project's existing web section | The section exists from feature 002 and already carries the research-use statement |
| Only the derived geometry is committed, not the 58 MB source | FR-022. Keeps the repository small, per Principle VII, and the source stays available at its identifier |
| The derived geometry is a surface, not a volume mesh | A browser draws surfaces. The interior is not needed to look at anatomy |
| Structures are distinguished by colour, with no colour meaning a measurement | FR-006. The source labels structures, so showing them is description, not inference |
| The triangle budget and the structure list can both be satisfied at once | Assumed, not verified. SC-003a makes the conflict visible if the assumption fails, rather than letting one requirement quietly win |
| Byte-identical rebuilding is achievable with pinned tool versions | The author chose this criterion over geometric tolerance. It holds only while the pinned versions remain installable, which is a known and accepted cost |
| The reader is on a current browser | Standard for a public personal site |
| Segment labelling may not ship in this feature | FR-025. Whether the landmarks are derivable is an empirical question, and the honest answer may be no |
| The mesh is shown in whatever orientation the source uses, described plainly | No reference space is chosen, so the project cannot claim a canonical orientation |

## Dependencies

| Dependency | Why |
|---|---|
| ADR-0008 and the published dataset | It is the anatomy this feature draws |
| Feature 002, the web section | FR-001. The viewer is a page inside it |
| ADR-0007, the disabled-control pattern | FR-023 and FR-025 apply it |
| The existing traceability checks | FR-033 |

## Out of scope

| Excluded | Reason |
|---|---|
| Any likelihood map, heatmap or overlay | No statistical core exists. This is the whole point of the restraint |
| Any focus, coordinate or study data | Nothing to place until a reference space is chosen |
| Importing vendor export files | No importer exists. ADR-0007 says show the gap instead |
| The separate atrial shape model | The four-chamber mesh already includes atrial geometry. The atrial model waits for a feature that needs it |
| Cutting, slicing or measuring the model | A measurement tool on an unvalidated mesh invites exactly the misuse Principle VI forbids |
| Patient data of any kind | Never in scope for this project |
