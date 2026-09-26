# Feature Specification: The first 3D viewer

**Feature Branch**: `main`

**Created**: 2026-09-25

**Status**: Draft

**Input**: User description: build the first 3D viewer as a page inside the project's web section. Opens on the reference anatomy adopted in ADR-0008. A second mode shows one study's own geometry with its own points, at patient level only, read entirely in the browser. No statistics, no pooling, no registration between the two.

## Context

The project's name promises a likelihood map on a heart. It has neither a statistical core nor a
reference space, and until now it had no anatomy it was allowed to ship either. ADR-0008 settled the
last of those: the Rodero average four-chamber mesh is licensed CC-BY-4.0 and may be bundled with
attribution.

This feature draws that heart, and adds a second mode for looking at a single study on its own
terms. It computes nothing.

| In | Out |
|---|---|
| A reference heart a reader can rotate, zoom and inspect | Any likelihood map |
| A patient mode showing one study's own geometry and its own points | Any pooling across studies |
| Provenance, licence and attribution visible to the reader | Any ALE computation |
| A reproducible route from the published source file to web geometry | Any claim about arrhythmia |
| Honest statements about what is not yet decided | Any registration between patient and mean |

The restraint is the point. A viewer that showed a coloured overlay would be read as a result, and
there is no result. Feature 001 built machinery specifically to stop that happening.

### Two modes, never mixed

A coordinate from a mapping system lives in that patient's own frame, built by the catheter during
that procedure. The reference mesh is a population mean. The two share no frame, so a patient point
drawn on the mean heart would be placed wrongly while looking authoritative.

| Mode | Geometry | Points | Frame |
|---|---|---|---|
| Population mean | The mesh adopted in ADR-0008 | None from any study | The mesh's own |
| Patient | That study's own reconstructed shell | That study's own points | That patient's own |

Each mode is internally consistent because geometry and points come from the same source. The modes
are mutually exclusive, and nothing crosses between them. Registering a patient onto the mean is the
job of a later feature, and it needs the canonical reference space that Principle II still leaves
open.

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
- Q: Should the viewer accept coordinates and vendor exports, given that patient coordinates and the
  mean mesh share no frame? -> A: Yes, but patient level only for this first release. The viewer
  shows a study's own geometry together with that study's own points, so no registration is needed
  and nothing is misplaced. Both patient level and population level are wanted eventually.
- Q: A vendor export is real patient data. Where is it processed? -> A: Never leaves the browser. No
  upload, no server, no storage, nothing in logs. The site keeps no data-processing role. Rejected:
  server-side processing, which would make a personal site a processor of clinical data; and
  optional local persistence, which leaves clinical data at rest on possibly shared machines.
- Q: What does the public page show before any file is loaded? -> A: The population mean heart, with
  patient import as a separate mode. Rejected: a bundled synthetic study, because an invented
  arrhythmia focus is fiction this project has been careful never to display; and an empty state,
  which shows nothing to any visitor without proprietary clinical software.
- Q: Nobody has a CARTO export, so the importer cannot be written or tested. How do we proceed? ->
  A: Obtain an anonymised real export first. Rejected: building against the open parser's documented
  format with a synthetic test file, which would start sooner but leave the importer unverified.
- Q: Which datasets does the importer get built and verified against? -> A: Two. A porcine CARTO 3
  export published under CC BY 4.0 (Zenodo 10.5281/zenodo.6651600), downloaded and inspected for
  identifiers the same day, proves the parser reads a genuine export directory. ARGO, nine
  anonymised human ventricular tachycardia maps on PhysioNet (10.13026/8gh2-e660, CC BY-NC-SA 4.0)
  with a documented anonymisation statement and ethics approval, proves patient mode on a real map.
  Neither is committed; both are fetched at test time. Rejected: the porcine export alone, which
  has two points and cannot show a map; and the OpenEP example MATLAB files, which carry no data
  licence and no de-identification statement.

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

### User Story 5 - Someone looks at one study's own map (Priority: P2)

An electrophysiologist opens a study from their own system and sees that patient's chamber geometry
with that patient's recorded points on it, in the patient's own frame. Nothing is compared to anyone
else, and nothing leaves their machine.

**Why this priority**: This is what the project is ultimately for, and it is the first step toward
it. Below the first two because the population mean must render correctly before a second mode is
worth having, and because the importer is blocked on obtaining a real export.

**Independent Test**: Load a study file, confirm the geometry and its points appear together, and
confirm by inspecting network activity that nothing was transmitted.

**Acceptance Scenarios**:

1. **Given** the viewer in population mode, **When** the user loads a study file, **Then** the view
   switches to patient mode and shows that study's geometry, not the mean
2. **Given** patient mode, **When** the study's points are displayed, **Then** they sit on that
   study's own geometry, in its own frame, with no registration applied
3. **Given** a loaded study, **When** network activity is inspected, **Then** no request carrying the
   file or its contents was made
4. **Given** a loaded study, **When** the page is reloaded, **Then** the data is gone and the viewer
   returns to population mode
5. **Given** patient mode, **When** the user looks at the page, **Then** it states that the view is
   one patient's own frame and is not comparable to any other study
6. **Given** any mode, **When** the user inspects the view, **Then** points from one mode are never
   drawn on the geometry of the other

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
| A study file will not parse | A stated error naming what was expected, and the viewer stays in its previous mode |
| A study contains thousands of points | They render within the performance budget, or the viewer says how many it is showing and why |
| An entered coordinate falls outside the geometry | Shown as outside, never silently clamped or hidden |
| A user tries to compare a patient view with the mean | The modes are exclusive, so the comparison cannot be made by accident. The page says why |
| A file turns out to carry identifiers | It is not used. FR-013n requires the file to be inspected before use, not trusted |
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
- **FR-013**: Any coordinate the viewer shows or accepts MUST be stated as belonging to the frame of
  the geometry currently displayed, and MUST NOT be presented as a canonical or cross-study
  coordinate. No axis label, grid or readout may imply that a reference space has been chosen.

### Functional requirements, the two modes

- **FR-013a**: The viewer MUST have exactly two modes, population mean and patient, and MUST make the
  active one obvious at all times.
- **FR-013b**: The viewer MUST open in population mean mode.
- **FR-013c**: The modes MUST be mutually exclusive. Points belonging to one mode MUST NEVER be drawn
  on the geometry of the other.
- **FR-013d**: Patient mode MUST state that the view is one patient's own frame and is not comparable
  to any other study or to the population mean.
- **FR-013e**: The viewer MUST NOT offer, imply or perform any registration between a patient frame
  and the mean, since no canonical reference space has been chosen.

### Functional requirements, coordinates

- **FR-013f**: The user MUST be able to enter coordinates manually and see them marked on the
  geometry currently displayed.
- **FR-013g**: An entered coordinate that falls outside the displayed geometry MUST be shown as such
  rather than silently clamped, hidden or moved.
- **FR-013h**: Every displayed point MUST be removable, and the user MUST be able to clear all points
  at once.
- **FR-013i**: A point MUST carry no meaning beyond its position. Nothing about a marker may encode a
  probability, a likelihood or any other result.

### Functional requirements, patient data

- **FR-013j**: A study file MUST be read entirely within the browser. The viewer MUST NOT transmit
  the file, any part of it, or anything derived from it, to any server.
- **FR-013k**: The viewer MUST NOT persist study data. Reloading the page MUST leave nothing behind.
- **FR-013l**: The page MUST tell the user, before they choose a file, that it is read locally and
  never uploaded.
- **FR-013m**: No patient study file, anonymised or otherwise, may be committed to the repository or
  served from the site.
- **FR-013n**: Any export used to develop or test the importer MUST be verified as de-identified
  before use, by inspecting the file itself rather than accepting an assurance. Mapping exports
  routinely carry identifiers in metadata, so being told a file is anonymised is a claim to check.
- **FR-013o**: The check performed under FR-013n, and what it examined, MUST be recorded in the
  vault.

### Functional requirements, the importer

- **FR-013p**: The file import control for a given system MUST appear disabled under ADR-0007,
  stating the reason and the date last checked, until the importer for that system has passed
  against a verified real export. For CARTO 3 the fixtures exist and are named in the Clarifications;
  for Affera no export format is public and the control stays disabled.
- **FR-013q**: The importer MUST NOT be described as supporting any system until it has been run
  against a real export from that system.
- **FR-013r**: A file that cannot be parsed MUST produce a stated error naming what was expected, and
  MUST leave the viewer in its previous mode rather than in a broken state.

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
- **SC-012**: Loading a study file produces zero network requests carrying the file or anything
  derived from it, confirmed by inspecting network activity.
- **SC-013**: Reloading the page after a study is loaded leaves no trace of it, confirmed by
  inspecting browser storage.
- **SC-014**: Zero points from one mode are ever drawn on the geometry of the other.
- **SC-015**: A reader in patient mode can state that the view is one patient's own frame and is not
  comparable to another study.
- **SC-016**: Zero patient study files exist anywhere in the repository or on the site.

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
| A study export contains both the chamber geometry and the recorded points | Verified 2026-09-25 on a real CARTO 3 export: four mesh files beside the point lists. Patient mode's frame is self-consistent as assumed |
| The porcine export needs no patient-data handling, and ARGO's anonymisation is the publisher's claim until inspected | FR-013n. The porcine files were inspected the same day and carry no identifiers. ARGO has not been downloaded yet and must be inspected before use |
| ARGO's NonCommercial and ShareAlike terms are compatible with test-time use | The project is non-commercial research and derives nothing from the files. They are fetched when tests run and never committed |

## Dependencies

| Dependency | Why |
|---|---|
| ADR-0008 and the published dataset | It is the anatomy this feature draws |
| Feature 002, the web section | FR-001. The viewer is a page inside it |
| ADR-0007, the disabled-control pattern | FR-023 and FR-025 apply it |
| The existing traceability checks | FR-033 |
| Two study exports, fetched at test time | FR-013p and FR-013q. The porcine export (Zenodo 6651600) for the parser, ARGO (PhysioNet) for patient mode. Neither committed |

## Out of scope

| Excluded | Reason |
|---|---|
| Any likelihood map, heatmap or overlay | No statistical core exists. This is the whole point of the restraint |
| Pooling anything across studies | That needs one shared space, which Principle II leaves open |
| Registering a patient frame onto the mean | Same reason. Attempting it now would misplace points while looking authoritative |
| Any server-side handling of study data | FR-013j. The site keeps no data-processing role |
| Importing vendor export files | No importer exists. ADR-0007 says show the gap instead |
| The separate atrial shape model | The four-chamber mesh already includes atrial geometry. The atrial model waits for a feature that needs it |
| Cutting, slicing or measuring the model | A measurement tool on an unvalidated mesh invites exactly the misuse Principle VI forbids |
| Patient data of any kind | Never in scope for this project |
