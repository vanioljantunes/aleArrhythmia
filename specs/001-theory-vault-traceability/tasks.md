---

description: "Task list for Theory Vault and Decision Traceability"
---

# Tasks: Theory Vault and Decision Traceability

**Input**: Design documents from `/specs/001-theory-vault-traceability/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/](./contracts/)

**Tests**: Included. Not a style preference — SC-004 requires a deliberately broken example per
defect kind, and User Story 3's independent test is exactly that. Fixtures come before the code they
exercise.

**Organization**: Grouped by user story so each is independently implementable and testable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on incomplete work)
- **[Story]**: US1–US4, mapping to the user stories in spec.md
- Exact file paths in every description

## Path Conventions

Single project, repository root. Vault at `docs/vault/`, checker at `tools/vaultcheck/`, tests at
`tests/`. Per [plan.md](./plan.md) Structure Decision.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Skeleton and packaging, so every later task has somewhere to land.

- [X] T001 Create the directory skeleton with `.gitkeep` placeholders: `docs/vault/decisions/`, `docs/vault/theory/`, `docs/vault/literature/`, `docs/vault/questions/`, `docs/vault/logs/`, `docs/vault/templates/`, `tools/vaultcheck/`, `tests/fixtures/`
- [X] T002 Create `pyproject.toml` declaring the `vaultcheck` package: `requires-python = ">=3.11"`, runtime dependency PyYAML, `dev` extra with pytest, console script `vaultcheck = "tools.vaultcheck.__main__:main"` per [research.md](./research.md) R-012
- [X] T003 [P] Create `.vaultcheckignore` with the initial reasoned exclusions (`specs/**` — spec prose cites example identifiers; `docs/vault/templates/**` — templates carry placeholder ids by design), format per [contracts/vaultcheck-cli.md](./contracts/vaultcheck-cli.md)
- [X] T004 [P] Create root `README.md`: what the project is, the research-use and not-a-medical-device disclaimer required by Constitution Principle VI, how to run the checker, and a licence section left as a stub until T011

**Checkpoint**: `pip install -e ".[dev]"` succeeds; directories exist; nothing checks anything yet.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The vault has to be navigable before notes are worth writing into it.

**CRITICAL**: No user story work begins until this phase is complete.

- [X] T005 Write `docs/vault/README.md` — how to read the vault without Obsidian: what the note types are, what frontmatter means, how `[[wikilinks]]` work, where to start (FR-002)
- [X] T006 Create `docs/vault/index.md` as a valid note (frontmatter `type: theory`, `status: active`) with an empty section per note type, ready to be filled by T019 (FR-005)

**Checkpoint**: A stranger opening `docs/vault/` finds an entry page and an explanation, even though it is nearly empty.

---

## Phase 3: User Story 1 — Re-open a past decision and understand it (Priority: P1) 🎯 MVP

**Goal**: One well-formed decision record that a reader with no context can audit: options,
trade-offs, choice, rejections, references.

**Independent test**: Hand `ADR-0001` to a reader who has never seen the project. They can state the
alternatives, the trade-offs and the reason for the choice without asking a question.

**Sequencing note**: the ADR template (T007) comes first because Principle VIII binds decisions to
the ADR form, and the form must exist before it can be filled. T011 follows T010 for the same
reason — the licence files are the *action*, ADR-0002 is the *record that precedes it*.

- [X] T007 [US1] Write `docs/vault/templates/adr.md` implementing [contracts/decision-record.md](./contracts/decision-record.md): frontmatter stub plus the five fixed headings `## Options considered`, `## Trade-offs`, `## Chosen`, `## Rejected`, `## References`, each with a placeholder comment the checker will treat as empty
- [X] T008 [P] [US1] Write `docs/vault/logs/log-2026-09-20-clarification.md` recording the clarification session: the four questions asked, the options presented, and the answers given. This is the conversation reference that ADR-0001 through ADR-0004 cite, so it must exist before them
- [X] T009 [US1] Write `docs/vault/decisions/ADR-0001-repository-layout.md` from [research.md](./research.md) R-001. Must state plainly that the repository was created before this record existed, rather than back-dating the sequence
- [X] T010 [US1] Write `docs/vault/decisions/ADR-0002-licensing.md` from R-002: Apache-2.0 for code, CC-BY-4.0 for vault prose, with the patent-grant reasoning and the rejected single-licence options. Record that this decision forced the Principle I amendment in constitution v1.2.0, since CC-BY-4.0 is not OSI-approved
- [X] T011 [US1] Add `LICENSE` (Apache-2.0 full text) and `LICENSE-docs` (CC-BY-4.0 full text), and replace the README licence stub with a statement of which licence covers which path, citing ADR-0002 (FR-013a)
- [X] T012 [US1] Write `docs/vault/decisions/ADR-0003-enforcement-mechanism.md` from R-008: pre-push hook plus push workflow, with pull-request branch protection and the `pre-commit` framework as rejected options. Record that rejecting pull requests forced the Governance amendment in constitution v1.2.0, moving the ADR-citation duty onto the commit message
- [X] T013 [US1] Write `docs/vault/decisions/ADR-0004-citation-scan-scope.md` from R-009 and R-010: all tracked text files minus a reasoned ignore list, exact `ADR-NNNN` citation form, with vault-only and filesystem-walk as rejected options
- [ ] T014 [US1] Run the reader test from the Independent Test above and record the outcome — including anything the reader could not follow — in `docs/vault/logs/`

**Checkpoint**: Four decision records exist, each with two or more options, per-option trade-offs, a
stated reason for the choice, a reason per rejection, and at least one resolvable reference. The
repository is licensed. Nothing enforces any of this yet — that is US3.

---

## Phase 4: User Story 2 — Read the project's theory without special tools (Priority: P2)

**Goal**: The vault is navigable and writable: a template per note type, an index that reaches
everything within two links.

**Independent test**: Someone without Obsidian is asked to find the project's open questions and one
method note. They succeed using only a plain text editor or the code host's file browser.

- [X] T015 [P] [US2] Write `docs/vault/templates/theory.md` — frontmatter stub plus the conventional headings for a derivation or method note
- [X] T016 [P] [US2] Write `docs/vault/templates/literature.md` — frontmatter stub plus `## What it is`, `## Coverage`, `## Licence and availability`, `## Consequences for pooling` (the fields FR-024 requires of every surveyed item)
- [X] T017 [P] [US2] Write `docs/vault/templates/question.md` — frontmatter stub plus `## The question`, `## Candidates`, `## What would settle it` per [data-model.md](./data-model.md) OpenQuestion
- [X] T018 [P] [US2] Write `docs/vault/templates/log.md` — frontmatter stub for a dated work log
- [X] T019 [US2] Fill `docs/vault/index.md`: a section per note type, the list of decision records with their status, and the list of open questions, so every note is two links from the entry page (FR-005)
- [ ] T020 [US2] Run the non-Obsidian reader trial from the Independent Test and record the result in `docs/vault/logs/`; fix whatever the reader could not find rather than explaining it to them

**Checkpoint**: Five templates, a populated index, and evidence that a stranger can navigate it.

---

## Phase 5: User Story 3 — Untraceable work is rejected automatically (Priority: P2)

**Goal**: The checker exists, catches every defect kind, and is wired in at both enforcement points.

**Independent test**: Introduce each defect kind one at a time; the check fails each time naming the
file and field. A clean vault passes.

**Fixtures precede implementation** — each fixture is the executable statement of what a rule means.

- [X] T021 [P] [US3] Build `tests/fixtures/clean/` — a minimal valid vault (one note of each type, one complete ADR, resolving links) that MUST pass
- [X] T022 [P] [US3] Build the fixture generator `tests/fixtures/build.py`: a clean base vault plus one mutation per rule id, each fixture directory named after its rule id in lowercase (e.g. `tests/fixtures/adr-empty-section/`). Per amended SC-004, every rule id gets exactly one fixture
- [X] T023 [P] [US3] Generate and commit the fixture trees under `tests/fixtures/` from `tests/fixtures/build.py`, so each broken vault is readable by a person and runnable by hand with `--root`
- [X] T024 [P] [US3] Include a `tests/fixtures/note-plugin-syntax/` fixture for the `NOTE-PLUGIN-SYNTAX` rule (closes analyze finding G1) and a meta-test in `tests/test_rules.py` that fails if any registered rule id lacks a fixture
- [X] T025 [P] [US3] Build the negative-control fixtures that MUST pass: `tests/fixtures/prose-mentions-adr/` (prose containing an identifier-like string, excluded or non-matching) and `tests/fixtures/empty-vault/` (zero notes, exits 0 reporting zero)
- [X] T026 [US3] Implement `tools/vaultcheck/report.py` — the `Violation` record, `path:line: RULE-ID: message` formatting on stderr, the stdout summary, stable sort order, and the 0/1/2 exit codes per [contracts/vaultcheck-cli.md](./contracts/vaultcheck-cli.md)
- [X] T027 [US3] Implement `tools/vaultcheck/discovery.py` — enumerate via `git ls-files -z`, drop binaries by null-byte sniff of the first 8 KiB, apply `.vaultcheckignore` with `fnmatch`, and emit `IGNORE-NO-REASON` (error) and `IGNORE-STALE` (warning)
- [X] T028 [US3] Implement `tools/vaultcheck/frontmatter.py` — parse with `yaml.safe_load`, enforce required fields, per-type status vocabularies, ISO dates with `updated >= created`, and vault-wide basename uniqueness; emits the `NOTE-*` rules in [contracts/note-frontmatter.md](./contracts/note-frontmatter.md)
- [X] T029 [US3] Implement `tools/vaultcheck/decisions.py` — locate the five fixed headings, detect empty sections (ignoring unmodified template placeholders), count named options, validate reference forms including local file-and-line resolution, check id uniqueness and id/filename agreement, and verify reciprocal supersession; emits the `ADR-*` rules
- [X] T030 [US3] Implement `tools/vaultcheck/links.py` — resolve `[[target]]`, `[[target|alias]]` and `[[target#heading]]` against unique basenames, match `ADR-NNNN` citations on a word boundary against existing records, and validate open-question structure; emits `LINK-*`, `CITE-DANGLING` and `Q-*`. Wikilinks inside inline code spans and fenced code blocks are examples, not links, and MUST be skipped (the vault README shows `[[...]]` syntax inside backticks)
- [X] T031 [US3] Implement the index completeness rule `INDEX-INCOMPLETE` in `tools/vaultcheck/links.py` — every decision record and open question found on disk appears in `docs/vault/index.md` (FR-005, V-X2)
- [X] T032 [US3] Implement `tools/vaultcheck/__main__.py` and `tools/vaultcheck/__init__.py` — argument parsing (`--root`, `--vault`, `--ignore-file`, `--quiet`, `--version`), orchestration of the rule modules, and the summary line; both `vaultcheck` and `python -m tools.vaultcheck` must work. Per ADR-0003, print a warning (not a failure) when run in a clone whose `core.hooksPath` is not `.githooks`, so an uninstalled local hook is visible
- [X] T033 [P] [US3] Write `tests/test_rules.py` (one parametrised test per fixture asserting the specific rule id and exit code, a meta-test that every registered rule has a fixture, and a drift test that committed trees match the generator) and `tests/test_cli.py` (output format, exit codes 0/1/2, `--quiet`, hook warning). Consolidated from four per-module files: the fixture table is the single source of truth, so splitting it by module would duplicate it
- [X] T034 [P] [US3] Write `tests/test_performance.py` asserting a full run on a generated 1000-note vault completes within the 60-second budget (SC-008)
- [ ] T035 [US3] Add `.githooks/pre-push` running the checker and refusing the push on non-zero exit, with a message naming the override; document `git config core.hooksPath .githooks` as the single install step in the README (FR-023a)
- [ ] T036 [US3] Add `.github/workflows/traceability.yml` running the checker on every push. Push this file in its own commit: if the credential lacks the `workflow` scope the push is rejected, and that error must be surfaced and fixed, never worked around by dropping the file (see plan.md Risks)
- [ ] T037 [US3] Verify both enforcement points by hand per quickstart Scenarios 3 and 4: a broken record is refused locally, and a `--no-verify` override still fails on the repository

**Checkpoint**: Every defect kind is caught with a named rule, a clean vault passes, and neither
enforcement point can be skipped by accident.

---

## Phase 6: User Story 4 — Choose the cardiac reference space on the evidence (Priority: P3)

**Goal**: The survey exists as linked literature notes feeding one explicitly open question. No
decision is made, and no claim about cardiac results appears anywhere.

**Independent test**: A reader can list the candidate spaces, say what each would cost the project,
and name what evidence is still missing, using only the survey notes.

- [ ] T038 [P] [US4] Write one literature note per candidate reference space in `docs/vault/literature/`: Universal Ventricular Coordinates, Universal Atrial Coordinates, the AHA 17-segment model, atrial segment models, fixed-atlas vertex indexing, and hybrid schemes — each stating coverage, licence, availability and consequences for pooling (FR-024)
- [ ] T039 [P] [US4] Write one literature note per open cardiac atlas found, with licence and anatomical coverage (FR-025)
- [ ] T040 [P] [US4] Write one literature note per commercial system — EnSite X EP, Rhythmia HDx, KODEX-EPD — recording what each can export and under what licence terms that export may be read, from published documentation only (FR-026)
- [ ] T041 [US4] Write an explicit unknown note in `docs/vault/literature/` for every item the survey could not establish, stating what was tried. Absence is not an acceptable answer (FR-027)
- [ ] T042 [US4] Write `docs/vault/questions/canonical-reference-space.md` with `status: open`, linking every candidate note under `## Candidates` and stating under `## What would settle it` what evidence would close it (FR-028)
- [ ] T043 [US4] Write `docs/vault/theory/ale-method.md` — what Activation Likelihood Estimation is and what changes when it moves from brain to heart, citing Turkeltaub 2002 and Eickhoff 2009/2012 by DOI
- [ ] T044 [US4] Update `docs/vault/index.md` with the new notes, and confirm no scientific claim about cardiac results appears anywhere in the vault (FR-029, quickstart Scenario 6)

**Checkpoint**: The survey is complete and honest, the question is open and linked, and the phase
has claimed nothing.

---

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T045 Walk every quickstart scenario on a fresh clone in a clean directory, exactly as written in [quickstart.md](./quickstart.md); fix the guide wherever reality and text disagree
- [ ] T046 Update `.specify/memory/constitution.md`: mark `TODO(VENDOR_INTEROP)` resolved or restate it with what the survey established, and bump the constitution version with a Sync Impact Report
- [ ] T047 [P] Add `CONTRIBUTING.md` — how to add a note, when a decision needs a record, how to run the checker before pushing
- [ ] T048 Final clean run of `vaultcheck`, full `pytest` pass, then commit and push

---

## Dependencies

**Phase order**: Setup → Foundational → US1 → US2 → US3 → US4 → Polish

**Story dependencies**:

- **US1** depends on Foundational only. It is the MVP and ships alone.
- **US2** depends on Foundational. Independent of US1 in principle; sequenced after it because
  T019's index must list the records US1 creates.
- **US3** depends on US1 (the ADR format must exist before a checker can check it) and on US2
  (the index rule T031 needs an index).
- **US4** depends on US2 (templates) and is verified by US3 (the checker proves the survey notes are
  well formed). It could be written before US3 exists, at the cost of fixing violations later.

**Hard ordering inside US1**: T007 → T008 → T009 → T010 → T011 → T012 → T013. The template precedes
the records; ADR-0002 precedes the licence files it justifies.

**Hard ordering inside US3**: fixtures (T021–T025) → `report.py` (T026) → `discovery.py` (T027) →
rule modules (T028–T031) → CLI (T032) → tests (T033–T034) → wiring (T035–T037). Every rule module
imports `report`, so T026 blocks them all.

---

## Parallel Execution Examples

**Setup**: T003 and T004 together — different files, no shared state.

**US1**: T008 runs alongside T007; the remaining ADR tasks are strictly sequential because each is a
numbered record and the numbers must not collide.

**US2**: T015, T016, T017 and T018 all together — four independent template files. T019 waits for
all four.

**US3**: T021 through T025 all together — five independent fixture trees. Then T028, T029 and T030
can proceed in parallel once T026 and T027 land, since each owns its own module. T033 and T034
parallel once the CLI exists.

**US4**: T038, T039 and T040 together — three disjoint groups of literature notes. T041 and T042
wait for all three, since they summarise what the others found.

---

## Implementation Strategy

**MVP is US1 alone.** Four decision records and a template, in a licensed public repository. At that
point the project can already demonstrate the thing it claims: a decision anyone can audit. No
checker, no survey, no automation.

**Increment 2 (US2)** makes the vault navigable, which is what turns a folder of records into
something that accumulates understanding.

**Increment 3 (US3)** converts the promise into a guarantee. It is the largest slice and the one
with real code; it is also the one that can be deferred longest without losing the earlier value.

**Increment 4 (US4)** is the research output. It is last not because it matters least — it is the
substance of the phase — but because it is the part that benefits most from the machinery being
ready to hold it.

Each increment ends at a checkpoint that is demonstrable on its own.
