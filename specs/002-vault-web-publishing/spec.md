# Feature Specification: Publish the theory vault on the web

**Feature Branch**: `main`

**Created**: 2026-09-24

**Status**: Draft

**Input**: User description: publish the aleArrhythmia theory vault as a browsable section of the author's personal website, as a fourth home-page tile named "My projects in 3D reconstruction", rendered in the browser from Markdown.

## Context

Feature 001 built a vault of 31 notes and the machinery that keeps it honest. None of it is visible
to anyone who does not clone the repository. This feature makes the reasoning public.

The vault is the only part of the project that exists today. There is no statistical core and no map
viewer, so this feature publishes reasoning, not results.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A visitor reads the project's reasoning (Priority: P1)

Someone lands on the author's home page, sees a fourth tile about 3D reconstruction projects, opens
it, and reads why the project chose what it chose. They never clone anything and never install
anything.

**Why this priority**: This is the whole point. The project's value today is its recorded reasoning,
and that reasoning currently reaches nobody. Everything else in this feature serves this journey.

**Independent Test**: Open the home page in a browser, reach a decision record in two clicks, and
read it in full. Delivers the project's reasoning to a stranger with no tooling.

**Acceptance Scenarios**:

1. **Given** the home page, **When** the visitor looks at the tiles, **Then** a fourth tile named
   "My projects in 3D reconstruction" is present alongside the existing three
2. **Given** that tile, **When** the visitor follows it, **Then** they reach a page listing the
   project's decision records, open questions, theory notes, literature notes and work logs
3. **Given** that listing, **When** the visitor opens any note, **Then** the note renders as readable
   prose with its tables and diagrams, and no raw frontmatter is shown
4. **Given** an open note, **When** the visitor follows a link to another note, **Then** the linked
   note opens

---

### User Story 2 - A note can be sent to someone (Priority: P1)

The author sends a colleague a link to one specific decision record. The colleague opens it and lands
on that record, not on a front page they have to navigate from.

**Why this priority**: Equal to US1. A public record nobody can cite is barely public. The author's
stated purpose is that people can see specific work, which requires specific links.

**Independent Test**: Copy the address of an open note, open it in a fresh browser with no history,
and confirm it lands on that same note.

**Acceptance Scenarios**:

1. **Given** any note, **When** the visitor reads its address, **Then** the address names that note
   and contains no fragment marker
2. **Given** a note address, **When** it is opened in a new browser session, **Then** that note
   renders directly
3. **Given** a note address that names no existing note, **When** it is opened, **Then** the visitor
   sees a clear message and a way back to the listing, not a blank page

---

### User Story 3 - The project is findable (Priority: P2)

Someone searches for the author, or for a term the project writes about, and finds the project.

**Why this priority**: The author's purpose is that people know the work exists. Below US1 and US2
because those must work first, but this is why the feature exists at all rather than a private page.

**Independent Test**: Disable scripting in the browser, open the section, and confirm the visitor can
still learn what the project contains and what every note is called.

**Acceptance Scenarios**:

1. **Given** scripting is unavailable, **When** the section is opened, **Then** the visitor sees the
   project description and a list of every note title with a one-line summary
2. **Given** the listing, **When** a note is added to the project, **Then** the listing includes it
   without anyone writing markup by hand

---

### User Story 4 - Publishing a note costs nothing extra (Priority: P2)

The author writes a note, commits it, and it appears on the site. No second copy is edited, no markup
is written, no manual step is remembered.

**Why this priority**: A publication route with a manual step decays. The vault is expected to grow
for the life of the project, so the cost per note has to be near zero or the site goes stale and
misrepresents the work.

**Independent Test**: Add a note to the vault, complete the publication route as documented, and
confirm the note is readable on the site with its links resolving, without editing any other file by
hand.

**Acceptance Scenarios**:

1. **Given** a new note in the vault, **When** the publication route runs, **Then** the note is
   readable on the site and appears in the listing
2. **Given** a note that is renamed or removed, **When** the route runs, **Then** the site reflects it
   and no link points at something that is gone
3. **Given** the route has not run, **When** anyone inspects the site, **Then** it is possible to tell
   which version of the vault is published

---

### Edge Cases

| Case | Expected |
|---|---|
| A note fails to load over the network | The reader sees a stated error and a way back, never a blank page or a wait that never ends |
| Scripting is unavailable | Titles, summaries and the project description remain readable (US3) |
| A link points at a note that does not exist | The reader is told, and the link is visibly distinguished from a working one |
| A note name collides with a site route | The vault route is namespaced so no vault note can shadow an existing page |
| The vault has a note the listing does not | The listing is generated, so this cannot happen silently; the traceability check already fails on an incomplete index |
| A very long note | Renders in full; long tables scroll horizontally rather than forcing the page to |
| The reader is on a phone | The section is readable at phone width, including tables |
| A note contains a diagram | The diagram renders, or degrades to its source text with an explanation, never to an empty box |

## Requirements *(mandatory)*

### Functional requirements, reading

- **FR-001**: The home page MUST carry a fourth tile named "My projects in 3D reconstruction",
  consistent in appearance and behaviour with the three tiles already there.
- **FR-002**: The tile MUST lead to a section page describing the project in plain language and
  listing every published note, grouped by kind.
- **FR-003**: Every note in the vault MUST be reachable from the section page within two steps.
- **FR-004**: A note MUST render its Markdown as formatted prose, including headings, tables, lists,
  code blocks and links.
- **FR-005**: A note MUST NOT display its frontmatter as raw text. The frontmatter MUST instead supply
  a note header showing at least the title, the kind of note, its status and its dates.
- **FR-006**: Links between notes MUST resolve to the corresponding published note.
- **FR-007**: A link to a note that does not exist MUST be visibly distinguished and MUST NOT navigate
  to a broken page.
- **FR-008**: Diagrams written in the vault MUST render, or MUST degrade to legible source text with a
  stated reason, never to an empty area.
- **FR-009**: The section MUST be readable at phone width. Tables and diagrams MAY scroll horizontally
  within their own area; the page body MUST NOT.

### Functional requirements, addressing

- **FR-010**: Every note MUST have its own address, distinct from every other note.
- **FR-011**: A note address MUST identify the note in its path, not in a fragment.
- **FR-012**: Opening a note address in a new session MUST render that note directly, with no
  intermediate navigation.
- **FR-013**: Vault addresses MUST be namespaced under a single path belonging to this project, so
  that no note can collide with an existing page of the site.
- **FR-014**: An address naming no existing note MUST produce a stated message and a route back to the
  listing.
- **FR-015**: Moving between notes MUST update the address, and the browser's back control MUST return
  to the previous note.

### Functional requirements, findability

- **FR-016**: The section page MUST list every note's title and a one-line summary as ordinary page
  content, readable without scripting.
- **FR-017**: That listing MUST be generated from the vault, never written by hand.
- **FR-018**: The section MUST state what the project is in its own page content, so that a reader who
  reaches it with no scripting learns what they have found.

### Functional requirements, robustness

- **FR-019**: Note content MUST be served from the same place as the site, and MUST NOT depend on a
  third-party interface at read time.
- **FR-020**: A failure to load a note MUST produce a stated error and a route back, within a bounded
  wait.
- **FR-021**: The site MUST continue to work without any build step, preserving the property it has
  today.

### Functional requirements, publication

- **FR-022**: Adding, renaming or removing a note MUST require no hand-written markup anywhere.
- **FR-023**: The published site MUST record which version of the vault it reflects.
- **FR-024**: The publication route MUST be documented in the repository well enough for the author to
  follow it after a long gap.
- **FR-025**: Publishing MUST NOT be possible from a vault that fails the existing traceability checks.
- **FR-025a**: The copy of the notes that the site serves MUST be produced by an automated job in this
  repository, not by a person, and MUST run only after those checks pass.
- **FR-025b**: The automated job MUST be the only writer of the published copy, so that the site
  cannot drift from the vault through a forgotten manual step.
- **FR-025c**: A note removed or renamed in the vault MUST disappear or move in the published copy on
  the next run, leaving nothing orphaned behind.

### Functional requirements, obligations carried from the constitution

- **FR-026**: Every page of the section MUST carry the research-use statement: this is a research tool,
  not a medical device, and nothing in it should guide a procedure.
- **FR-027**: The section MUST state the licence covering the notes and the licence covering the
  software.
- **FR-028**: This feature MUST NOT add any claim about cardiac anatomy, arrhythmia mechanism or
  statistical result. It publishes existing notes and nothing more.
- **FR-029**: Any prose written for this feature MUST satisfy the project's writing rules, and MUST be
  covered by the existing style checks where those checks apply.
- **FR-030**: The choice of rendering in the reader's browser, and its trade-offs against publishing
  pre-rendered pages, MUST be recorded as a decision record before this feature is considered complete.
- **FR-031**: No output of this feature may reference the author's personal folder organisation.

### Key entities

| Entity | What it is |
|---|---|
| **Note** | One vault document: a title, a kind, a status, dates, a body, and links to other notes |
| **Kind** | What a note is: decision record, theory, literature, open question, work log |
| **Listing** | The generated catalogue of every note, readable without scripting |
| **Address** | The public, sendable location of one note |
| **Published snapshot** | The note contents the site is currently serving, and the vault version they correspond to |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A visitor who has never seen the project reaches a decision record from the home page in
  two clicks and reads it in full, without installing anything.
- **SC-002**: 100 percent of the vault's notes are reachable from the section page, and the count on
  the site equals the count the traceability checker reports.
- **SC-003**: 100 percent of links between notes resolve to the correct note. Zero links lead to a
  broken page.
- **SC-004**: Every note has a distinct address that renders that note when opened in a browser with no
  prior history.
- **SC-005**: With scripting unavailable, a reader can still state what the project is and name every
  note it contains.
- **SC-006**: Adding one note to the vault and publishing it requires no hand-written markup, and the
  published site shows it.
- **SC-007**: A reader on a phone can read any note, including its tables, without the page body
  scrolling sideways.
- **SC-008**: A note that fails to load produces a stated message within five seconds, never an
  indefinite wait or a blank page.
- **SC-009**: The site continues to deploy with no build step.
- **SC-010**: Someone who has never seen the project can say, after reading the section page alone,
  what the project is for and that it is not a medical device.
- **SC-011**: The traceability checks pass on the repository with this feature complete.

## Assumptions

| Assumption | Basis |
|---|---|
| The section lives under one path belonging to this project on the author's existing personal site | FR-013. The exact domain changes no requirement |
| The existing site keeps its current shape: static pages, no build step, existing tile layout | Stated constraint, and FR-021 |
| Note contents are served as files next to the site rather than requested from a third party | FR-019, which the author asked for explicitly |
| Readers use a current browser | Standard for a public personal site |
| The vault stays small enough to list on one page | 31 notes today; a few hundred would still list |
| Rendering happens in the reader's browser | The author chose this over publishing pre-rendered pages. Trade-offs to be recorded under FR-030 |
| The website's files can be written to by an automated job from this repository | Required by FR-025a. Needs a credential with permission to commit to the website, which the author holds |

## Dependencies

| Dependency | Why |
|---|---|
| The vault of feature 001 | This feature publishes it |
| The existing traceability checker | FR-025 gates publication on it, and FR-017 can reuse its parsing rather than adding a second parser |
| The author's existing website and its hosting | FR-001 and FR-021 |
| Write access from this repository to the website's files | FR-025a. Without it the publication route cannot be automatic |

## Out of scope

| Excluded | Reason |
|---|---|
| Any map, mesh or 3D rendering | No reference space is chosen and no statistical core exists. This feature publishes text |
| Editing notes through the website | The vault is edited in the repository, and records are never rewritten |
| Search across notes | 31 notes list on one page. Revisit when the count makes it necessary |
| Comments or any reader account | Nothing in the project's purpose needs them |
| Translations | Not requested |

## Clarifications

### Session 2026-09-24

- Q: Note contents must be served next to the site (FR-019) and the site must gain no build step
  (FR-021), so a copy of the Markdown has to reach the site's own files. What carries it, and how
  does anyone tell whether the copy is current? -> A: An automated job in this repository copies the
  notes and the generated listing into the website's files and commits them, after the traceability
  checks pass and only then. Rejected: carrying this repository as a submodule of the website, and a
  script the author runs by hand. The first ships the whole repository where only notes are wanted;
  the second is a step someone has to remember, and the site goes stale silently when they do not.
