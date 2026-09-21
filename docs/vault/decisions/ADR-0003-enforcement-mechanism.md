---
title: Enforcement mechanism for the traceability check
type: adr
status: accepted
id: ADR-0003
created: 2026-09-21
updated: 2026-09-21
---

# ADR-0003: Enforcement mechanism for the traceability check

Principle VIII says a check must refuse untraceable work, but a check nobody runs refuses nothing.
This decides where the check runs, and so what actually stops a defective decision record from
becoming part of the public history. Chosen during the 2026-09-20 clarification session.

**Consequence for the constitution.** Rejecting pull requests left the constitution's Governance
section binding its citation duty to "every pull request description" — a surface that would never
exist here. The constitution was amended to v1.2.0 so the duty binds the commit message instead.

**A limitation this record does not hide.** Git deliberately does not run hooks from a freshly
cloned repository until the person who cloned it opts in — a security property, so that cloning
cannot execute code. A clone where `git config core.hooksPath .githooks` has not been run will push
without the local check. Such a push is never *unchecked*: the repository-side check still runs on
it and records a failure publicly. But it is not refused locally. The spec's edge case asking that
this situation "fail loudly" locally cannot be met by any hook-based design, and needs restating as
"never passes unchecked". To narrow the gap, the checker warns whenever it runs in a clone where
the hook is not installed.

## Options considered

- **Local pre-push hook plus a check on every push to the public repository** — a tracked hook
  script refuses a defective push before it leaves the machine, and a workflow on the code host
  runs the same check on every push that arrives.
- **Pull requests with a required status check** — all work goes through pull requests, and the
  check must pass before a pull request can merge.
- **The `pre-commit` framework** — the check is registered with the widely used `pre-commit` tool,
  which installs and manages the hook.
- **Repository-side check only** — no local hook; the workflow alone runs the check after each push.

## Trade-offs

**Local pre-push hook plus a check on every push**: costs a one-line install step per clone, and
the limitation above — an uninstalled clone is caught publicly rather than locally. Buys failure in
well under a second before anything is public, a public pass/fail record an outside reader can
inspect, and a deliberate, visible override (git's standard flag for skipping hooks on push) rather
than either no override or a silent one.

**Pull requests with a required status check**: costs a pull request for every change, including a
one-line fix to a note — a solo author reviewing their own pull requests produces ceremony, not
review. Buys the strongest and most conventional signal, and a merge that is genuinely blocked.

**The `pre-commit` framework**: costs a dependency and a configuration file to do what four lines of
shell already do, and it still needs a per-clone install step, so it does not close the fresh-clone
gap either. Buys a familiar tool and easy addition of other checks later.

**Repository-side check only**: costs the local feedback loop — a broken record is public before
anyone learns it is broken. Buys zero setup and no per-clone step at all.

## Chosen

**Local pre-push hook plus a check on every push to the public repository.** Neither point is
enough alone. The hook gives fast, private failure; the repository-side check guarantees that
every push is checked whether or not the hook was installed, and shows the result publicly. The
combination matches how this project is actually worked on — by one author pushing directly —
without pretending there is a review process that does not exist.

## Rejected

**Pull requests with a required status check** — rejected because it imposes a review ritual with
nobody to review, on every change, for a signal the chosen option already provides. The author
declined it explicitly. It remains the right choice if the project gains regular contributors; this
record would then be superseded, not edited.

**The `pre-commit` framework** — rejected under Principle VII: it adds a dependency to replace a
few lines of shell, and it does not solve the fresh-clone gap that is the hard part.

**Repository-side check only** — rejected because it makes broken records public before they are
caught, which is exactly the outcome the check exists to prevent.

## References

- Constitution, Principle VIII, Traceable by Construction — `.specify/memory/constitution.md:166`
- Constitution, Governance, Compliance review (as amended in v1.2.0) — `.specify/memory/constitution.md:266`
- Spec 001, FR-023 — `specs/001-theory-vault-traceability/spec.md:256`
- Spec 001, FR-023a — `specs/001-theory-vault-traceability/spec.md:260`
- Research note R-008 — `specs/001-theory-vault-traceability/research.md:149`
- Clarification session, 2026-09-20 — [[log-2026-09-20-clarification]]
- Git documentation, hooks and `core.hooksPath` — https://git-scm.com/docs/githooks
