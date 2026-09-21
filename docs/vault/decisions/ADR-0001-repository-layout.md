---
title: Repository layout
type: adr
status: accepted
id: ADR-0001
created: 2026-09-21
updated: 2026-09-21
---

# ADR-0001: Repository layout

Where the project's code and notes live.

| Date | Event |
|---|---|
| 2026-09-20 | Planning files committed inside the private monorepo, on an unrelated branch |
| 2026-09-20 | Author: every monorepo project gets its own repository |
| 2026-09-20 | Public repository created, files moved |
| 2026-09-21 | This record written |

The action came one day before the record, because the record format did not exist yet.
Principle VIII asks for the record first. The dates above are the real ones.

Reformatted on 2026-09-21 per [[ADR-0005-writing-style]]. Options, trade-offs, choice and reasons
are unchanged. The original wording is in commit 0e80c20.

## Options considered

| Option | What it means |
|---|---|
| A. Standalone public repository | Own history, licences, issues and checks. The monorepo keeps at most a pointer. |
| B. Monorepo folder plus public snapshot | Files stay in the private monorepo. A copy is pushed to a public place from time to time. |
| C. Git submodule | A standalone repository that the monorepo embeds by reference. |

## Trade-offs

| Option | Cost | Gain |
|---|---|---|
| A | One more repository, one more local clone | Public, continuous history. Independent licensing. Checks visible to outside readers. |
| B | A snapshot copies files, not commits, so the public copy has no history. Copies drift when an export is forgotten. | One fewer repository. Atomic commits across sibling projects. |
| C | A moving part that goes stale easily. Confusing workflow. | Both views at once. |

## Chosen

A. Principle I requires public work, and the monorepo must stay private. A public copy with no
history would contradict Principle VIII in the one project built to show traceability.

## Rejected

| Option | Why it lost |
|---|---|
| B | Loses history, which contradicts Principle VIII, and drifts. Its gain, cross-project commits, is unused: no other project shares code with this one. |
| C | No present benefit. It can be added later without changing this repository. |

## References

- Constitution, Principles I and VIII: `.specify/memory/constitution.md`
- Spec 001, FR-013: `specs/001-theory-vault-traceability/spec.md`
- Research note R-001: `specs/001-theory-vault-traceability/research.md`
- Clarification session, 2026-09-20: [[log-2026-09-20-clarification]]
- The repository: https://github.com/vanioljantunes/aleArrhythmia
