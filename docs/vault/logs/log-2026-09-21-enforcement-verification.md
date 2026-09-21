---
title: Verification of both enforcement points
type: log
status: active
created: 2026-09-21
updated: 2026-09-21
---

# Verification of both enforcement points — 2026-09-21

Evidence that the two halves of the enforcement mechanism in [[ADR-0003-enforcement-mechanism]]
each refuse a broken decision record. Task T037 of spec 001.

## Local half: the pre-push hook

With the hook installed (`git config core.hooksPath .githooks`), the hook script was run three
times against the working tree:

| Run | State of ADR-0001 | Hook exit | Output |
|---|---|---|---|
| 1 | Unchanged | 0 | clean |
| 2 | `## References` emptied on disk | 1 | `ADR-0001-repository-layout.md:64: ADR-NO-REFERENCE`, push refused |
| 3 | Restored | 0 | clean |

The hook then ran on every real push that followed; its summary line appears before Git transmits
anything.

## Repository half: the workflow

This half exists for the case the hook cannot cover: a clone where the hook was never installed.
That case was reproduced exactly, on a throwaway branch so that `main` was never touched:

1. Branch `verify/server-check` created from `main` at 99d6bb3.
2. ADR-0001's `## References` emptied and committed as 32410a7.
3. `core.hooksPath` unset, simulating a fresh clone. The push produced no hook output — the hook
   did not run, as expected.
4. `core.hooksPath` restored immediately after the single push.

The workflow ran on the push and failed with the same violation the hook reports:

```text
docs/vault/decisions/ADR-0001-repository-layout.md:64: ADR-NO-REFERENCE: '## References' has no content
vaultcheck: 7 notes, 4 decision records, 13 links, 36 citations verified — 1 violation
Process completed with exit code 1.
```

- Failing run: https://github.com/vanioljantunes/aleArrhythmia/actions/runs/35625031339
- Passing run on `main` at 99d6bb3: https://github.com/vanioljantunes/aleArrhythmia/actions/runs/35624850054

The branch was then deleted. The failed run stays in the repository's Actions history on purpose:
it is the public record that the backstop works.

## What was not done

The documented override flag was not used to push a broken commit. The author's standing rules
forbid bypassing hooks, and a local guard blocks it. The uninstalled-clone path exercises the same
server-side check, which is what the override would ultimately rely on.
