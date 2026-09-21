---
title: Clarification session for spec 001
type: log
status: active
created: 2026-09-20
updated: 2026-09-21
---

# Clarification session, 2026-09-20

Spec 001 clarification, run by the author with an AI coding assistant (Claude) through
`/speckit-clarify`. ADR-0001 to ADR-0004 cite this log as evidence. Each question was offered as
named options with one marked recommended.

## Questions and answers

| # | Question | Options offered | Answer | Record |
|---|---|---|---|---|
| 1 | Where does the project live? | Raised by the author, not offered: "this should have an repository of its own, not nested in a local folder (all prjects under a local folder should follow this rule actually)" | Own public repository; standing rule for every monorepo project | [[ADR-0001-repository-layout]] |
| 2 | What blocks untraceable work? | Hook plus workflow (recommended); pull requests with branch protection; workflow only | Hook plus workflow | [[ADR-0003-enforcement-mechanism]] |
| 3 | Which files are scanned for citations? | All tracked text minus an ignore list (recommended); vault plus specs; vault only | All tracked text minus an ignore list | [[ADR-0004-citation-scan-scope]] |
| 4 | Which licence? | Apache-2.0 code plus CC-BY-4.0 prose (recommended); MIT for all; Apache-2.0 for all | Apache-2.0 code plus CC-BY-4.0 prose | [[ADR-0002-licensing]] |

## Mistake during the session

| Step | Detail |
|---|---|
| What happened | The assistant committed the planning files into the monorepo on an unrelated feature branch, because that branch was checked out |
| Author asked | Why that branch |
| Remedies offered | Extract to a new repository and drop from the monorepo (recommended); extract and also rewrite the other branch (needs force-push); leave old commits, move future work |
| Chosen | Extract and drop. Repository created the same day, before any decision record existed. |

## Found later

On 2026-09-21 `/speckit-analyze` found that answers 2 and 4 conflicted with the constitution as
then written. The constitution was amended to v1.2.0; the answers stood.

Reformatted on 2026-09-21 per [[ADR-0005-writing-style]]; content unchanged.
