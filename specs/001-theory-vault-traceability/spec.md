# Feature Specification: Theory Vault and Decision Traceability

**Feature Branch**: `001-theory-vault-traceability`

**Created**: 2026-09-20

**Status**: Draft

**Input**: User description: "Phase 0 foundation: the theory vault, the ADR traceability machinery, and the reference-space survey. Deliverables: (1) an Obsidian vault at docs/vault/ with plain-Markdown notes, wikilinks and machine-readable frontmatter, plus its folder structure and note templates (theory, adr, literature, question, log); (2) an ADR template enforcing Options considered / Trade-offs per option / Chosen and why / Rejected and why / References, with sequential ids and supersedes links; (3) a CI traceability check that fails on empty Options, Trade-offs or References fields, dangling cited ADR ids, duplicate ADR numbers, supersession without the superseding id recorded, and broken wikilinks; (4) a written survey of candidate canonical cardiac reference spaces (Universal Ventricular/Atrial Coordinates on an open statistical heart atlas, AHA 17-segment and atrial-segment models, fixed-atlas vertex space, hybrids), of available open cardiac atlases, and of the exported file formats of EnSite X EP, Rhythmia HDx and KODEX-EPD, each written as vault literature notes and feeding ADRs; (5) ADR-0001 recording the repository layout decision (standalone public repo versus a folder inside a larger repository). Out of scope for this phase: the ALE statistics implementation itself, the 3D viewer, the vault-to-HTML renderer, and any public claim about cardiac results. The audience for the vault is a researcher who has never opened Obsidian."


## Clarifications

### Session 2026-09-20

- Q: Should the project live in its own repository or as a folder inside a larger repository? → A: Its own standalone public repository.
- Q: What actually blocks untraceable work from landing (FR-023)? → A: A local pre-push hook plus the check running on every push to the public repository. Not pull-request branch protection.
- Q: Which files does the check scan for ADR citations (FR-012 / FR-017)? → A: All version-controlled text files, minus an explicit, reviewable ignore list. Citations must use the exact `ADR-NNNN` form.
- Q: Which licence for the public repository? → A: Apache-2.0 for the software, CC-BY-4.0 for the vault prose.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Re-open a past decision and understand it (Priority: P1)

A researcher, the author a year later, or a stranger auditing the project, wants to know why the
project made a particular choice. They open the decision record by its number and find, in one
place: which options were on the table, what each one cost and bought, which was chosen and why it
beat the others, why each rejected option lost, and the references backing all of it. They can
follow every reference to its source. If the decision was later reversed, the record says so and
points to the record that replaced it, and the original text is still readable.

**Why this priority**: This is the whole point of the phase. Without it the project produces
conclusions nobody can check, which defeats both the scientific goal and the portfolio goal. It is
also the smallest slice that is useful on its own, a single well-formed decision record already
delivers value before any vault structure or automation exists.

**Independent Test**: Write one real decision record (the repository layout choice) using the
template, hand it to a reader with no prior context, and confirm they can state the alternatives,
the trade-offs and the reason for the choice without asking a question.

**Acceptance Scenarios**:

1. **Given** a completed decision record, **When** a reader opens it, **Then** they find all five
   required parts present and non-empty: options considered (at least two), trade-offs stated per
   option, the chosen option with its reason, each rejected option with its reason, and at least
   one resolvable reference.
2. **Given** a decision that is later reversed, **When** a reader opens the original record,
   **Then** it is marked superseded and names the record that replaced it, and the replacement
   names what it supersedes.
3. **Given** a decision record, **When** a reader follows any listed reference, **Then** it
   resolves to a real source, a published work, a web page, a specific file and line, a dataset,
   or a recorded conversation.
4. **Given** a piece of work (code, specification, or note) that embodies a decision, **When** a
   reader inspects it, **Then** it names the decision record it follows by identifier.

---

### User Story 2 - Read the project's theory without special tools (Priority: P2)

A researcher who has never opened Obsidian wants to understand the method. They find the theory -
derivations, method notes, literature summaries, open questions, as ordinary text files they can
read in any editor, in a browser on the code host, or printed. Notes are organised so they can
find their way in without a guide: an entry page, clear note types, and links between related
notes that resolve rather than dangle.

**Why this priority**: The vault is where the method actually lives, and it must not be legible
only to its author with a particular application installed. It comes after the decision record
because a decision record is useful even without surrounding structure, but the structure is what
makes the project accumulate understanding rather than files.

**Independent Test**: Hand the vault folder to someone without Obsidian and ask them to find the
project's open questions and one method note; they succeed using only a plain text editor or the
code host's file browser.

**Acceptance Scenarios**:

1. **Given** the vault, **When** a reader opens any note in a plain text editor, **Then** it is
   readable as-is: no note requires an optional or proprietary plugin to be understood or rendered.
2. **Given** the vault, **When** a reader starts at its entry page, **Then** they can reach every
   note type, theory, decision, literature, open question, work log, within two links.
3. **Given** any note, **When** its machine-readable header is inspected, **Then** it declares at
   minimum a title, a note type, a status, a creation date and a last-updated date, and decision
   notes additionally declare an identifier and any supersession links.
4. **Given** a note that links to another note, **When** the link is followed, **Then** it resolves
   to an existing note.
5. **Given** a writer starting a new note, **When** they pick its type, **Then** a template for
   that type exists and already contains the required header fields and section headings.

---

### User Story 3 - Untraceable work is rejected automatically (Priority: P2)

A contributor, including the author in a hurry, proposes a change whose decision record has an
empty options list, no references, a number that already exists, a citation to a record that does
not exist, a supersession with no replacement recorded, or a link to a note that is not there. The
project's automated check refuses the change and says exactly which record and which field is at
fault, so the gap is fixed before it leaves the machine rather than discovered a year later.

**Why this priority**: Convention alone erodes precisely when a session is rushed, which is when
the record matters most. This is what turns the traceability promise from an intention into a
guarantee. It depends on the record format existing first, hence P2.

**Independent Test**: Deliberately introduce each defect kind the checker claims to catch, one at a
time, and confirm the check fails each time with a message naming the offending file and field;
then confirm a clean vault passes.

**Acceptance Scenarios**:

1. **Given** a decision record with an empty options, trade-offs or references field, **When** the
   check runs, **Then** it fails and names the record and the empty field.
2. **Given** two decision records sharing a number, **When** the check runs, **Then** it fails and
   names both files.
3. **Given** a note or source file citing a decision identifier that does not exist, **When** the
   check runs, **Then** it fails and names the citing location and the missing identifier.
4. **Given** a record marked superseded without naming its replacement, or naming a replacement
   that does not name it back, **When** the check runs, **Then** it fails and names the broken
   pair.
5. **Given** a link pointing at a note that does not exist, **When** the check runs, **Then** it
   fails and names the source note and the unresolved target.
6. **Given** a vault with none of these defects, **When** the check runs, **Then** it passes and
   reports how many records and links it verified.
7. **Given** any failure, **When** the contributor reads the output, **Then** every failure line
   identifies a file and, where applicable, a line number.
8. **Given** a defective vault, **When** the contributor attempts to push, **Then** the push is
   refused locally, and if the local enforcement is deliberately overridden, the public repository
   records a failed status for that push.

---

### User Story 4 - Choose the cardiac reference space on the evidence (Priority: P3)

The project must eventually commit to one canonical cardiac coordinate space, and that commitment
decides what every future coordinate means. Before choosing, a reader can consult a written survey
of the candidates, continuous universal coordinate systems on an open statistical heart atlas,
discrete segment models, fixed-atlas vertex indexing, and hybrids, together with what open
cardiac atlases actually exist and what the commercial mapping systems can export. Each surveyed
item is a note stating what it is, what it covers, its licence and availability, and its
consequences for coordinate-based pooling. The open question stays explicitly open and links to
the evidence that will settle it.

**Why this priority**: It is the substantive research output of the phase, but it produces no
decision yet, the choice itself is deliberately deferred. It is last because it is the part that
depends on the record format, the vault structure and the automated check already being in place
to hold it.

**Independent Test**: A reader can list the candidate spaces, say what each would cost the project,
and name what evidence is still missing, using only the survey notes.

**Acceptance Scenarios**:

1. **Given** the survey, **When** a reader looks for candidate reference spaces, **Then** each
   candidate has its own note recording what it is, its anatomical coverage, its licence and
   availability, and its consequences for pooling coordinates across studies.
2. **Given** the survey, **When** a reader looks for source material, **Then** open cardiac atlases
   and the export capabilities of the named commercial mapping systems each have notes with
   resolvable references, and anything that could not be established is recorded as an unknown
   rather than guessed.
3. **Given** the reference-space question, **When** a reader opens it, **Then** it is marked open,
   links to every candidate note, and states what evidence would close it.
4. **Given** the survey notes, **When** a reader looks for conclusions about cardiac results,
   **Then** there are none, the phase makes no scientific claim.

---

### Edge Cases

- Two decision records are written in parallel and claim the same number: the automated check must
  fail rather than silently accept, and the fix must not require renumbering unrelated records.
- A decision is genuinely forced with no alternative: the record must still name the alternative
  that was ruled out, including "do nothing", rather than leave the options field empty.
- A referenced web page disappears: the reference must retain enough identifying detail (title,
  author, date, identifier) to remain traceable without the live link.
- A decision is superseded by a record that is itself later superseded: the chain must remain
  followable in both directions.
- A note is renamed or moved: links pointing at it must either be updated or fail the check, never
  silently resolve to nothing.
- A reference is a conversation rather than a document: it must be recorded in a form that can be
  re-read, not cited as an unrecoverable memory.
- A note links to a candidate reference space that the project later rejects: the note stays, the
  rejection is recorded, and neither is deleted.
- The check runs on a vault with no decision records yet: it passes and reports zero, rather than
  erroring.
- Prose happens to mention a decision identifier that does not exist, quoting an external project's
  record, or illustrating the format in documentation: the citation form must be exact enough, or
  the ignore list explicit enough, that this does not produce a false failure.
- The local enforcement is not installed on a fresh clone: Git does not run hooks from a clone
  until its owner opts in, so the push cannot be refused locally. It must never pass unchecked -
  the repository-side check still runs and records the failure publicly, and the checker warns
  whenever it runs in a clone without the hook installed (ADR-0003).
- A contributor deliberately overrides the local enforcement: the override must be visible after the
  fact, and the public repository must still record the failure.

## Requirements *(mandatory)*

### Functional Requirements

**Vault structure and notes**

- **FR-001**: The project MUST hold all theory, derivations, method notes, literature summaries,
  open questions, decision records and work logs, as plain text notes inside a single vault folder
  versioned alongside the code.
- **FR-002**: Every note MUST be readable and understandable without any optional or proprietary
  plugin, application or paid service.
- **FR-003**: Every note MUST carry a machine-readable header declaring at minimum: title, note
  type (theory, decision, literature, open question, work log), status, creation date and
  last-updated date. Dates MUST use an unambiguous year-month-day form.
- **FR-004**: The vault MUST provide a template per note type, each pre-filled with the required
  header fields and the required section headings for that type.
- **FR-005**: The vault MUST have an entry page from which every note type is reachable within two
  links, and which lists the open questions and the decision records.
- **FR-006**: Notes MUST be able to link to one another, and every such link MUST resolve to an
  existing note.

**Decision records**

- **FR-007**: Every non-trivial decision MUST be recorded as a numbered decision record before the
  decision is acted upon.
- **FR-008**: A decision record MUST contain all five of: options considered (at least two, each
  named and described), trade-offs stated separately for each option, the chosen option with the
  reason it was preferred, each rejected option with the reason it lost, and at least one reference.
- **FR-009**: A reference MUST be resolvable: a published work with a persistent identifier, a web
  address, a specific file and line in the repository, a dataset identifier, or a recorded
  conversation stored in the vault.
- **FR-010**: Decision record numbers MUST be sequential and unique across the project.
- **FR-011**: A decision record MUST NOT be deleted or rewritten once merged. A reversal MUST be a
  new record that names the record it supersedes, and the superseded record MUST name its
  replacement.
- **FR-012**: Any artifact that embodies a decision, source file, specification, plan, or note -
  MUST cite that decision by its identifier.
- **FR-013**: The project MUST live in its own standalone public repository, not as a folder inside
  a larger repository, and MUST record that choice as its first decision record together with the
  trade-offs of both options.
- **FR-013a**: The repository MUST carry two licences: a permissive software licence granting
  patent rights (Apache-2.0) covering the code, and an attribution licence (CC-BY-4.0) covering the
  vault prose, each with its scope stated unambiguously at the repository root.

**Automated traceability check**

- **FR-014**: The project MUST provide an automated check, runnable both locally and on every
  proposed change, that verifies the vault's traceability rules.
- **FR-015**: The check MUST fail when a decision record has an empty options, trade-offs or
  references field.
- **FR-016**: The check MUST fail when two decision records share a number.
- **FR-017**: The check MUST fail when any artifact cites a decision identifier that does not exist.
  Citations are recognised by an exact identifier form (`ADR-NNNN`) so that ordinary prose cannot
  trigger a false match.
- **FR-017a**: The check MUST scan every version-controlled text file for citations, vault notes,
  specifications, plans, source and configuration alike, excluding only paths named in an explicit
  ignore list kept in the repository, so that the exclusions are themselves reviewable.
- **FR-018**: The check MUST fail when a record is marked superseded without a recorded replacement,
  or when a supersession is not recorded reciprocally by both records.
- **FR-019**: The check MUST fail when a link points at a note that does not exist.
- **FR-020**: The check MUST fail when a note is missing a required header field.
- **FR-021**: Every failure MUST name the offending file and, where the defect is line-bound, its
  line number, and state which rule was broken.
- **FR-022**: The check MUST exit successfully on a clean vault and report the number of records,
  citations and links it verified.
- **FR-023**: The check MUST run automatically at two points: locally before a push, blocking the
  push when it fails, and on the public repository for every push, recording a visible pass or fail
  status. Neither point may be the only one: the local run gives fast feedback, the repository run
  proves the discipline to an outside reader.
- **FR-023a**: The local enforcement MUST be installable in one documented step and MUST be
  bypassable only by an explicit, deliberate override, so that a bypass is a visible act rather
  than an accident.

**Reference-space survey**

- **FR-024**: The project MUST record, as literature notes, each candidate canonical cardiac
  reference space, stating what it is, its anatomical coverage, its licence and availability, and
  its consequences for pooling coordinates across studies.
- **FR-025**: The project MUST record, as literature notes, the open cardiac atlases available as
  reference anatomy, with their licences and coverage.
- **FR-026**: The project MUST record, as literature notes, what each named commercial mapping
  system can export, and under what licence terms that export may be read.
- **FR-027**: Anything that could not be established MUST be recorded explicitly as an unknown,
  with what was tried; it MUST NOT be guessed or silently omitted.
- **FR-028**: The reference-space choice MUST remain an open question in this phase, linked to
  every candidate note and stating what evidence would close it.
- **FR-029**: This phase MUST make no scientific claim about cardiac results and MUST NOT publish
  one.

### Key Entities

- **Note**: A single plain-text unit of theory. Has a title, a type, a status, a creation date, a
  last-updated date, body text, and links to other notes.
- **Decision record**: A note of type decision. Additionally has a unique sequential identifier, an
  options list, per-option trade-offs, a chosen option with rationale, rejected options with
  rationale, references, and optional supersedes / superseded-by links to other decision records.
- **Reference**: A resolvable pointer from a note to a source, published work, web address,
  repository file and line, dataset, or recorded conversation.
- **Open question**: A note of type open question. Names an unresolved choice, links to the
  candidate evidence, and states what would settle it. Closes by being linked from the decision
  record that resolves it.
- **Candidate reference space**: A literature note describing one possible canonical cardiac
  coordinate system, its coverage, licence and pooling consequences.
- **Citation**: A reference from an artifact outside the vault (source file, specification, plan,
  configuration) to a decision record identifier, written in an exact recognisable form. Every
  version-controlled text file is scanned for citations except paths named in the repository's
  explicit ignore list.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A reader who has never seen the project can, for any recorded decision, state the
  alternatives, the trade-offs and the reason for the choice within two minutes of opening the
  record, without asking anyone.
- **SC-002**: 100% of decision records have at least two named options, per-option trade-offs, a
  stated reason for the choice, a stated reason for each rejection, and at least one resolvable
  reference, verified automatically on every proposed change.
- **SC-003**: 100% of links between notes resolve; there are zero dangling links and zero citations
  to non-existent decision identifiers.
- **SC-004**: Every rule the checker defines is caught by the check and demonstrated by a
  deliberately broken example, one fixture per rule id, with no rule id lacking a fixture. The
  rule list is the contract's, not a frozen count.
- **SC-005**: A reader without the note-taking application installed can locate the project's open
  questions and any named method note using only a plain text editor or the code host's file
  browser, on the first attempt.
- **SC-006**: Every candidate cardiac reference space identified in the survey has a note recording
  its coverage, licence and pooling consequences, and the reference-space question links to all of
  them.
- **SC-007**: No unknown is left implicit: every item the survey could not establish appears as an
  explicitly recorded unknown.
- **SC-008**: The check completes fast enough to run on every proposed change without contributors
  working around it, under one minute on the full vault.
- **SC-009**: Zero scientific claims about cardiac results are published in this phase.
- **SC-010**: Every file in the public repository is covered by exactly one stated licence, the
  software licence or the prose licence, with zero files whose licence a reader would have to
  guess.
- **SC-011**: On a fresh clone, a contributor can install the local enforcement in one documented
  step, and an attempt to push a defective vault is refused without them needing to read anything
  further.

## Assumptions

- The project lives in its own standalone public repository, and the vault lives inside it rather
  than in a separate one, so that a method change and the note describing it land in the same
  commit.
- The audience is researchers and engineers, not the general public. Notes may assume familiarity
  with meta-analysis and cardiac electrophysiology, but not with the note-taking application.
- "Non-trivial decision" means any choice that a future reader could reasonably question and that
  would cost real work to reverse. Mechanical choices, formatting, naming a local variable, do
  not require a record. The boundary is judged by the author and enforced at review, not
  automatically.
- Decision numbers are assigned sequentially at the time of writing; collisions from parallel work
  are expected to be rare and are resolved by renumbering the later record before merge.
- English is the working language of the vault.
- Rendering the vault as web pages, publishing it, and the appearance of the public site are
  explicitly out of scope here and are specified separately; this phase only requires that the
  notes be structured well enough to be rendered later.
- The statistical implementation, the reference-space decision itself, and the 3D viewer are out of
  scope for this phase.
- Access to the commercial mapping systems' own software is not assumed; the export-format survey
  is built from published documentation and openly available sample data, and gaps are recorded as
  unknowns.
