---
title: Reader trial of ADR-0001 (author)
type: log
status: active
created: 2026-09-21
updated: 2026-09-21
---

# Reader trial of ADR-0001, 2026-09-21

Task T014 of spec 001 asks for a reader who has never seen the project. This trial used the author,
so it is weaker evidence, and T014 stays open for a stranger.

| Item | Result |
|---|---|
| Reader | The author |
| Record read | [[ADR-0001-repository-layout]], on GitHub |
| Content | "a good track": options, trade-offs and reasons were followed |
| Form | Too much prose. Asked for tables and flowcharts, step by step, as concise as possible |
| Hard rule added | No em dash, and none of the signs listed at https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing |

## Actions taken

| Action | Where |
|---|---|
| Writing rules recorded, with enforcement levels | [[ADR-0005-writing-style]] |
| Checker rules added: em dash, curly quotes, AI tool artifacts (errors); AI vocabulary (warning) | `tools/vaultcheck/style.py` |
| All vault notes reformatted into tables and flowcharts, decision content unchanged | this vault |
| Em dashes removed from specs, constitution, README and code | whole repository |
