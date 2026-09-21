---
title: Licensing
type: adr
status: accepted
id: ADR-0002
created: 2026-09-21
updated: 2026-09-21
---

# ADR-0002: Licensing

Licences for the two kinds of work in the repository: software and prose.

| Consequence | Detail |
|---|---|
| Constitution amended | Principle I first required an OSI-approved licence for every artifact. OSI approves software licences only, and CC-BY-4.0 is not one of them. `/speckit-analyze` caught this on 2026-09-21. Constitution v1.2.0 now asks for an OSI licence for software and an open content licence for prose. The decision stood. |

Reformatted on 2026-09-21 per [[ADR-0005-writing-style]]. Options, trade-offs, choice and reasons
are unchanged. The original wording is in commit 0501fa2.

## Options considered

| Option | What it means |
|---|---|
| A. Apache-2.0 for code, CC-BY-4.0 for prose | Two licences, one per kind of work, scopes stated at the repository root |
| B. MIT for everything | One short permissive licence |
| C. Apache-2.0 for everything | One permissive licence with a patent grant, applied to code and prose |
| D. Apache-2.0 for code, CC-BY-SA-4.0 for prose | As A, with share-alike terms on the prose |

## Trade-offs

| Option | Cost | Gain |
|---|---|---|
| A | A second licence file, one sentence on which covers what | Patent grant on code. Attribution required when the theory is quoted. |
| B | No patent grant. Its text speaks of "the Software", which fits prose badly. | Shortest, most familiar licence |
| C | No attribution requirement suited to citation. Software terms on prose. | One licence, with the patent grant |
| D | Share-alike terms make quoting in journals under other licences harder | Derived notes stay open |

## Chosen

A. Mapping and ablation vendors hold patents, so a licence without a patent grant leaves people who
build on the code less protected. For the prose, attribution is how academic credit reaches the
author, and CC-BY-4.0 makes it a condition of reuse without limiting reuse.

## Rejected

| Option | Why it lost |
|---|---|
| B | No patent grant, in a patent-dense field. Poor fit for prose. |
| C | No citation-style attribution for the theory. Workable, not the best fit. |
| D | Makes the theory harder to quote in other publications, against the aim of being cited |

## References

- Constitution, Principle I as amended in v1.2.0: `.specify/memory/constitution.md`
- Spec 001, FR-013a: `specs/001-theory-vault-traceability/spec.md`
- Research note R-002: `specs/001-theory-vault-traceability/research.md`
- Clarification session, 2026-09-20: [[log-2026-09-20-clarification]]
- Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0
- CC-BY-4.0: https://creativecommons.org/licenses/by/4.0/
- OSI approved licences: https://opensource.org/licenses
