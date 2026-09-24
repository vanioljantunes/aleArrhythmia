---
title: Fresh-clone walk of the quickstart
type: log
status: active
created: 2026-09-24
updated: 2026-09-24
---

# Fresh-clone quickstart walk, 2026-09-24

T045. Cloned the public repository into an empty directory, installed into a fresh virtual
environment, and ran every scenario exactly as written. Six places where the guide and reality
disagreed. The guide was wrong in all six; the tool was right.

## What was run

| Step | Result |
|---|---|
| `git clone`, then `python -m tools.vaultcheck` before installing anything | Clean, exit 0, plus one warning |
| `pip install -e ".[dev]"`, `git config core.hooksPath .githooks` | Installed, hook active |
| Scenario 1, bare `vaultcheck` | Clean, exit 0, as written |
| Scenario 2, `pytest tests/` | 44 passed |
| Scenario 2, single fixture by hand | Failed as written, see defect 2 |
| Scenario 3, break a record and invoke the hook | Passed only after fixing the break script, see defect 4 |
| Scenario 5, vault without Obsidian | 7 decision records and 1 open question listed, readable in a plain editor |
| Scenario 6, survey present and honest | 14 of 14 literature notes record unknowns; no scientific claim found |
| Scenario 7, timing | 0.52 s against a 60 s budget |

## Defects found in the guide

| # | Scenario | Guide said | Reality |
|---|---|---|---|
| 1 | Setup | A summary line and exit 0 | Also one `HOOK-NOT-INSTALLED` warning, unavoidable before the `git config` line |
| 2 | 2 | Fixtures named `empty-section/`, `one-option/`, `no-reference/` and so on | Fixtures are named after their rule: `adr-empty-section/`, `adr-too-few-options/`. The table listed 11 of 35 and named none of them correctly |
| 3 | 2 | `vaultcheck --root tests/fixtures/empty-section` | Exits 2, no such directory. The correct path exits 1 and names the rule |
| 4 | 3 | A break script inserting a comment after `## References` | Breaks nothing. The references below stay intact, the record stays valid, and the push succeeds. The scenario passed vacuously |
| 5 | 3 | A one-line refusal message | The hook prints three lines, with different wording |
| 6 | 6 | `grep -rl "unknown"` | Matches 2 of 14 notes. The heading is `## Unknowns`, so the grep needs `-i` |

Defect 4 is the one that mattered. A reader following the guide would have watched the push succeed
and concluded the enforcement was broken, when in fact the test never broke anything. Re-run with a
script that empties the section, the hook refused the push and named the rule.

## Fixed

All six corrected in `specs/001-theory-vault-traceability/quickstart.md`. No change to the tool was
needed.

## References

- The guide: `specs/001-theory-vault-traceability/quickstart.md`
- Task: T045 in `specs/001-theory-vault-traceability/tasks.md`
- Earlier proof of both enforcement points: [[log-2026-09-21-enforcement-verification]]
