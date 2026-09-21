---
title: Citation scan scope
type: adr
status: accepted
id: ADR-0004
created: 2026-09-21
updated: 2026-09-21
---

# ADR-0004: Citation scan scope

The checker verifies that every citation of a decision record points at a record that exists. That
raises two questions this record settles together, because each constrains the other: which files
are searched for citations, and what text counts as a citation. Chosen during the 2026-09-20
clarification session; the ignore-list format was settled during planning.

## Options considered

- **All version-controlled text files, minus a reasoned ignore list** — enumerate every file Git
  tracks, drop binaries, drop paths named in a tracked `.vaultcheckignore` whose every entry carries
  a written reason, and scan the rest for the exact form `ADR-` followed by four digits.
- **Vault notes plus specifications and plans only** — scan the documentation layer, and leave
  source code unscanned.
- **The vault only** — scan notes under `docs/vault/` and nothing else.
- **Walk the filesystem directly** — scan every text file on disk under the repository root,
  tracked or not, with ignore rules of the checker's own.

## Trade-offs

**All version-controlled text files, minus a reasoned ignore list**: costs a small ignore file to
maintain, and some care over false positives — this project's own specifications quote example
identifiers on purpose. Buys the property that a citation cannot hide anywhere, and an exclusion
list that is itself tracked and reviewable, so every exclusion is a visible choice. Using Git's own
file list honours `.gitignore` for free and never touches build output or scratch files.

**Vault notes plus specifications and plans only**: costs coverage exactly where it matters most —
source code is where a decision silently drifts from what was recorded. Buys zero false positives
from code, and a simpler scan.

**The vault only**: costs almost all enforcement of the rule that artifacts cite their decisions
(FR-012). Buys the simplest possible scan.

**Walk the filesystem directly**: costs picking up untracked scratch files, editor backups and build
output, and requires reimplementing ignore logic that Git already provides. Buys independence from
Git, which this project does not need.

## Chosen

**All version-controlled text files, minus a reasoned ignore list.** The rule being enforced is that
work cites the decision it embodies, and work lives in code as much as in prose — a scope that
skipped code would skip the most likely place for drift. The exact four-digit form keeps false
positives rare; the ignore list catches the deliberate cases; and requiring a reason on every
ignore entry stops the list from quietly becoming the place where inconvenient files go.

Two details follow from this choice:

- **Citation form**: exactly `ADR-` plus four digits, on a word boundary. A looser pattern such as
  one-or-more digits would match prose like "ADR-1" and version strings.
- **Ignore format**: one `fnmatch` glob per line over repository-relative paths, each with a trailing
  `#` reason. An entry without a reason fails the check; an entry matching nothing is warned about,
  so stale exclusions are visible without blocking work.

## Rejected

**Vault notes plus specifications and plans only** — rejected because it leaves code, the place where
drift does the most damage, entirely unchecked.

**The vault only** — rejected because it would reduce FR-012 to a rule nothing enforces outside the
vault.

**Walk the filesystem directly** — rejected because it scans files that are not part of the project
and duplicates logic Git already has. Principle VII favours reusing the tool that already defines
what the repository contains.

**Full gitignore semantics for the ignore file** — considered during planning as a variant of the
chosen option, and rejected: it would need either an extra dependency or a reimplementation of
negation and anchoring rules, for a file expected to hold a handful of entries.

## References

- Constitution, Principle VIII, Traceable by Construction — `.specify/memory/constitution.md:166`
- Spec 001, FR-017a — `specs/001-theory-vault-traceability/spec.md:245`
- Research note R-009 — `specs/001-theory-vault-traceability/research.md:169`
- Research note R-010 — `specs/001-theory-vault-traceability/research.md:188`
- The ignore list this record governs — `.vaultcheckignore`
- Clarification session, 2026-09-20 — [[log-2026-09-20-clarification]]
