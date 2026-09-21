---
title: Repository layout
type: adr
status: accepted
id: ADR-0001
created: 2026-09-21
updated: 2026-09-21
---

# ADR-0001: Repository layout

aleArrhythmia began as a folder inside the author's private personal monorepo, where its first
planning files were committed. The constitution requires the project to be public, and the author
stated during the 2026-09-20 clarification session that every project in that monorepo should
have a repository of its own.

**Sequencing, stated plainly.** This decision was acted on before this record existed. The public
repository was created on 2026-09-20, during the clarification session, and this record was
written the following day. Principle VIII requires the record to come first; here it did not,
because the decision-record format itself did not yet exist. The record is not back-dated.

## Options considered

- **Standalone public repository** — the project gets its own repository on the code host, with its
  own history, licences, issue tracker and automated checks. The monorepo keeps at most a pointer.
- **Folder in the private monorepo, exported to a public snapshot** — the project stays where it
  started, and a copy is periodically pushed to a public location.
- **Git submodule inside the monorepo** — a standalone repository that the monorepo embeds by
  reference, so both views exist at once.

## Trade-offs

**Standalone public repository**: costs one more repository to maintain, and a separate clone on
the author's machine. Buys a public, continuous history; the freedom to license the project
independently of everything else in the monorepo; and automated checks that an outside reader can
see running.

**Folder in the private monorepo, exported to a public snapshot**: costs history — an export copies
files, not commits, so the public copy has no record of how anything came to be. The copy also
drifts whenever an export is forgotten. Buys one fewer repository and the ability to change this
project and a sibling project in a single commit.

**Git submodule inside the monorepo**: costs a moving part that is easy to leave pointing at a stale
commit, and a workflow most contributors find confusing. Buys both views at once.

## Chosen

**Standalone public repository.** Principle I requires every artifact to be public, and the monorepo
is private and must stay private. An exported snapshot would discard exactly the history that
Principle VIII exists to preserve — a traceability project whose public face has no history would
contradict itself.

## Rejected

**Folder in the private monorepo, exported to a public snapshot** — rejected because the public copy
would carry no history, which directly defeats Principle VIII, and because snapshots drift. Its one
real gain, atomic commits across sibling projects, is not needed: no other project in the monorepo
shares code with this one.

**Git submodule inside the monorepo** — rejected as unnecessary now. It adds a moving part for no
present benefit. If the monorepo ever needs to embed this project, a submodule can be added later
without changing this repository at all, so nothing is lost by declining it today.

## References

- Constitution, Principle I, Open by Default — `.specify/memory/constitution.md:76`
- Constitution, Principle VIII, Traceable by Construction — `.specify/memory/constitution.md:166`
- Spec 001, FR-013 — `specs/001-theory-vault-traceability/spec.md:228`
- Research note R-001 — `specs/001-theory-vault-traceability/research.md:13`
- Clarification session, 2026-09-20 — [[log-2026-09-20-clarification]]
- The repository itself — https://github.com/vanioljantunes/aleArrhythmia
