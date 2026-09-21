---
title: Clarification session for spec 001
type: log
status: active
created: 2026-09-20
updated: 2026-09-21
---

# Clarification session — 2026-09-20

Working session between the project author and an AI coding assistant (Claude), run through the
spec-kit `/speckit-clarify` command on spec 001, theory vault and decision traceability. This log
is the recorded conversation that decision records ADR-0001 through ADR-0004 cite as evidence.

Each question was put as a choice between named options, with one marked as recommended. The
answers below are the author's, recorded as given.

## Q1 — Where does the project live?

Raised by the author directly, not offered as a question: *"this should have an repository of its
own, not nested in a local folder (all projects under a local folder should follow this rule actually)."*

**Answer**: its own standalone public repository. The author stated this as a standing rule for
every project in the personal monorepo, not a one-off.

**What happened next**: the planning files had already been committed into the monorepo, on an
unrelated feature branch — an error by the assistant, which had committed to whatever branch was
checked out. The author asked why. Three remedies were offered: extract to a new repository and
drop from the monorepo (recommended); extract and also rewrite the unrelated branch's history
(requires a force-push); or leave the existing commits and move only future work. The author chose
the first. The repository `github.com/vanioljantunes/aleArrhythmia` was created the same day,
before any decision record existed. Recorded as [[ADR-0001-repository-layout]].

## Q2 — What blocks untraceable work from landing?

Options offered:

- **Pre-push hook plus a check on every push to the public repository** (recommended) — fast local
  failure, and a public pass/fail record that works without pull requests.
- **Pull requests with branch protection** — strongest conventional signal, but forces a solo
  author to open a pull request against themselves for every note.
- **A check on push only, no local hook** — no friction, but broken records are public before
  anyone learns of them.

**Answer**: pre-push hook plus a check on every push. Recorded as
[[ADR-0003-enforcement-mechanism]].

## Q3 — Which files are scanned for decision citations?

Options offered:

- **All version-controlled text files, minus an explicit ignore list** (recommended) — a citation
  cannot hide anywhere, and the exclusions are themselves reviewable.
- **Vault notes plus specifications and plans only** — no false positives, but code is where a
  silently drifted decision does the most damage.
- **The vault only** — narrowest, and leaves citation outside the vault unenforced.

**Answer**: all version-controlled text files, minus an ignore list. Recorded as
[[ADR-0004-citation-scan-scope]].

## Q4 — Which licence?

Options offered:

- **Apache-2.0 for code, CC-BY-4.0 for vault prose** (recommended) — a patent grant on the code,
  which matters in a field where device vendors hold patents, and attribution-based reuse of the
  theory.
- **MIT for everything** — shortest and most familiar, no patent grant, and an awkward fit for
  prose.
- **Apache-2.0 for everything** — one licence with the patent grant, but no citation-style
  attribution requirement on the theory.

**Answer**: Apache-2.0 for code, CC-BY-4.0 for prose. Recorded as [[ADR-0002-licensing]].

## Consequence discovered later

On 2026-09-21, `/speckit-analyze` found that two of these answers contradicted the constitution as
then written: CC-BY-4.0 is not an OSI-approved licence, which Principle I required of every
artifact; and rejecting pull requests left a Governance rule binding pull request descriptions with
nothing to bind. The constitution was amended to v1.2.0 rather than the answers being reversed.
