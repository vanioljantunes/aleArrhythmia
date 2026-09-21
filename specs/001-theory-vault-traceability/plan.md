# Implementation Plan: Theory Vault and Decision Traceability

**Branch**: `001-theory-vault-traceability` | **Date**: 2026-09-20 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-theory-vault-traceability/spec.md`

## Summary

Build the record-keeping foundation the whole project rests on: a plain-Markdown theory vault whose
notes carry machine-readable headers, a decision-record format that cannot be filled in vaguely, and
a checker that refuses to let untraceable work leave the machine. Then use that machinery to write
the phase's actual research output — the survey of candidate cardiac reference spaces, open cardiac
atlases and commercial export formats — as linked literature notes feeding one explicitly open
question.

Technical approach: a small Python package, `vaultcheck`, walks the files Git already tracks, parses
note headers and decision-record structure, and reports rule violations with file and line. It is
wired in twice — a tracked pre-push hook for fast local failure, and a workflow on the public
repository so the discipline is visible to an outside reader. No service, no database, no framework:
the vault is files, and the checker is a function over files.

## Technical Context

**Language/Version**: Python 3.11+ (matches the future statistical core, per Constitution VII)

**Primary Dependencies**: PyYAML for note headers; pytest for tests. Nothing else. Standard library
for file walking, parsing and reporting.

**Storage**: Plain files in Git. No database.

**Testing**: pytest, with a fixture vault per defect kind under `tests/fixtures/`

**Target Platform**: Any OS with Python 3.11+ and Git; developed on Windows, verified on Linux in CI

**Project Type**: Documentation corpus plus a single-purpose CLI tool

**Performance Goals**: Full-vault check under 1 second at present size; must stay under 60 seconds at
1000 notes (SC-008) so nobody routes around it

**Constraints**: Offline; no network calls in the checker. Every note readable without any plugin.
Exit code 0 on clean, non-zero on any violation.

**Scale/Scope**: Tens of notes at the end of this phase, hundreds within a year. One vault, one
checker, one hook, one workflow.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Checked against constitution v1.2.0.

| Principle | Gate | Status |
|---|---|---|
| I. Open by Default | Public repo, open licence appropriate to each artifact kind, no proprietary dependency to build or run | PASS — repo is public; Apache-2.0 (OSI-approved) covers code and CC-BY-4.0 covers vault prose, matching the v1.2.0 wording; PyYAML is MIT |
| II. One Canonical Reference Space | No coordinate work may assume a space before the ADR exists | PASS — this phase writes the survey and keeps the question open; it stores no coordinates |
| III. Statistical Validity | Statistical routines need numerical tests | NOT APPLICABLE — no statistics in this phase; recorded so the gate is seen to have been considered |
| IV. Provenance on Every Number | Emitted results carry provenance | NOT APPLICABLE — this phase emits no results. The checker's own output names every file it verified, which is the same discipline applied to itself |
| V. Add-On, Not Replacement | Nothing intraprocedural, no vendor code | PASS — the export-format survey reads published documentation only; no vendor SDK enters the repo |
| VI. Research Tool, Not a Medical Device | Disclaimer present, no patient data, no telemetry | PASS — disclaimer ships in the README and the vault index this phase; the checker makes no network call |
| VII. Small, Legible, Installable | Smallest thing that works; dependencies must replace code we would otherwise test | PASS — two dependencies. PyYAML replaces a header parser we do not want to own; pytest is test-only |
| VIII. Traceable by Construction | Every non-trivial decision is an ADR before it is acted on | PASS with sequencing note — see below |

**Principle VIII sequencing.** The ADR format must exist before ADRs can be written, so the very
first task creates the template, and the first four decisions are then recorded against it before
the code they justify is written: ADR-0001 repository layout, ADR-0002 licensing, ADR-0003
enforcement mechanism, ADR-0004 citation scan scope. Each corresponds to a clarification already
answered in the spec, so no decision is being made after the fact — only written down in the binding
form. The repository-layout decision was acted on before its ADR existed (the repository was created
during the clarification session); ADR-0001 records that honestly rather than back-dating it.

**Theory Vault and Public Surface section.** Vault at `docs/vault/`, plain Markdown, wikilinks,
machine-readable headers, no plugin dependency: all satisfied by design. Rendering to HTML and the
vanioantunes.com surface are explicitly deferred to Phase 2 and are out of scope here; the note
structure is designed so that renderer can be added without touching note content.

No violations. Complexity Tracking is empty.

## Project Structure

### Documentation (this feature)

```text
specs/001-theory-vault-traceability/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── note-frontmatter.md
│   ├── decision-record.md
│   └── vaultcheck-cli.md
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 output (/speckit-tasks — not created here)
```

### Source Code (repository root)

```text
docs/vault/                     # the vault; every note plain Markdown
├── index.md                    # entry page: every note type within two links
├── README.md                   # how to read this without Obsidian
├── decisions/                  # ADR-NNNN-slug.md
├── theory/                     # derivations and method notes
├── literature/                 # one note per surveyed source
├── questions/                  # open questions
├── logs/                       # dated work logs
└── templates/                  # one template per note type

tools/vaultcheck/               # the checker
├── __init__.py
├── __main__.py                 # CLI entry point
├── discovery.py                # which files are in scope (git ls-files minus ignore list)
├── frontmatter.py              # header parsing and required-field validation
├── decisions.py                # ADR structure, numbering, supersession
├── links.py                    # wikilink and citation resolution
└── report.py                   # violation formatting, exit codes

tests/
├── fixtures/                   # one deliberately broken vault per defect kind
└── test_*.py

.githooks/pre-push              # tracked hook; installed via core.hooksPath
.github/workflows/traceability.yml
.vaultcheckignore               # explicit, reviewable exclusions
pyproject.toml
README.md                       # includes the research-use disclaimer
LICENSE                         # Apache-2.0, covers code
LICENSE-docs                    # CC-BY-4.0, covers docs/vault/
```

**Structure Decision**: Single project, two top-level concerns — `docs/vault/` is the content and
`tools/vaultcheck/` is the one tool that guards it. No `src/models/services/` layering: the checker
is a handful of pure functions over file paths, and inventing a service layer for it would violate
Principle VII. Tests sit at the repository root rather than inside the tool so that fixture vaults
can be laid out as real directory trees.

## Risks

| Risk | Consequence | Handling |
|---|---|---|
| Pushing `.github/workflows/` can be rejected when the Git credential lacks the `workflow` scope | The repository-side half of FR-023 silently never lands | Push the workflow file in its own commit and verify it server-side; if rejected, report the exact error and re-authorise rather than dropping the file |
| A tracked hook does nothing until `core.hooksPath` is set | A fresh clone pushes unchecked work while believing it is protected | FR-023a: one documented install step, and the workflow catches what the hook missed |
| Wikilink resolution by basename breaks if two notes share a filename | Ambiguous links resolve arbitrarily | Enforce unique note basenames as a checked rule, not a convention |
| Citation scanning over all tracked text files produces false positives | Contributors learn to ignore the checker | Exact `ADR-NNNN` form plus a reviewable ignore list; a fixture test asserts prose mentioning a format example does not trip it |
| The survey depends on vendor documentation that may not be publicly obtainable | Phase output has holes | FR-027: holes are recorded as explicit unknowns with what was tried, never guessed |

## Constitution Re-Check (post-design)

Re-run after Phase 1, then again after the v1.2.0 amendment.

- **Principle VII (small, legible, installable)** — the design added no dependency beyond the two
  already declared. The checker is six modules of pure functions; no service layer, no plugin
  system, no configuration framework. `--fix` was explicitly rejected in
  [contracts/vaultcheck-cli.md](./contracts/vaultcheck-cli.md) rather than designed in. PASS.
- **Principle VI (research tool, no telemetry)** — R-007 forbids the checker any network path, so
  there is no route by which it could report anything anywhere. PASS.
- **Principle VIII (traceable by construction)** — the design strengthens it: supersession must be
  reciprocal, references must be resolvable rather than merely present, and the ignore list must
  justify every exclusion. PASS.
- **Principles II, III, IV** — unchanged by the design; still not applicable or still satisfied as
  recorded above.

No new violations. Complexity Tracking remains empty.

### Re-check after constitution v1.2.0 (2026-09-21)

`/speckit-analyze` found two MUST statements that no artifact could satisfy as written, and the
constitution was amended rather than the plan:

- **Principle I** previously demanded an OSI-approved licence for *every* artifact. OSI approves
  software licences; the vault prose is CC-BY-4.0, which is not among them. The principle now
  distinguishes software from prose, and the licence decision (FR-013a, ADR-0002) satisfies it
  without change.
- **Governance** previously bound the ADR-citation duty to pull request descriptions, which this
  project does not use (R-008, ADR-0003). The duty now binds the commit message. Consequence for
  this plan: every commit implementing a task that embodies a decision cites that decision's ADR
  id — starting with the commits for T009 through T013.

Neither amendment changed the plan's design, its structure, or any task. Gate still PASS, no
violations, Complexity Tracking still empty.

## Complexity Tracking

No constitution violations. Table intentionally empty.
