---
title: Licensing
type: adr
status: accepted
id: ADR-0002
created: 2026-09-21
updated: 2026-09-21
---

# ADR-0002: Licensing

The repository holds two kinds of work: software (the checker now, the statistical core and viewer
later) and prose (the theory vault). The project is public by constitution, and it has two
audiences for reuse — engineers who may build on the code, and researchers who may quote the
theory. The licence was chosen during the 2026-09-20 clarification session.

**Consequence for the constitution.** This decision contradicted Principle I as first written, which
required every artifact to carry an OSI-approved licence. The Open Source Initiative approves
software licences; CC-BY-4.0 is not among them. `/speckit-analyze` caught the conflict on
2026-09-21, and the constitution was amended to v1.2.0 so that Principle I asks for an
OSI-approved licence for software and an open content licence for prose. The decision stood; the
principle's wording moved.

## Options considered

- **Apache-2.0 for code, CC-BY-4.0 for vault prose** — two licences, each chosen for its kind of
  work, with the scope of each stated at the repository root.
- **MIT for everything** — one short, permissive licence across the whole repository.
- **Apache-2.0 for everything** — one permissive licence with a patent grant, applied to code and
  prose alike.
- **Apache-2.0 for code, CC-BY-SA-4.0 for prose** — as the first option, but with share-alike
  (copyleft) terms on the theory.

## Trade-offs

**Apache-2.0 for code, CC-BY-4.0 for vault prose**: costs a second licence file and one sentence of
explanation about which covers what. Buys an explicit patent grant on the code, and a licence on
the prose that requires attribution when the theory is quoted — which is how academic credit
reaches the author.

**MIT for everything**: costs the patent grant, and its text speaks of "the Software", which reads
oddly applied to prose. Buys the shortest, most widely recognised licence text there is.

**Apache-2.0 for everything**: costs any attribution requirement on the theory beyond the notice
file, and applies software terms to prose. Buys a single licence with the patent grant.

**Apache-2.0 for code, CC-BY-SA-4.0 for prose**: costs reuse freedom — share-alike terms can
complicate quoting passages in a journal article published under a different licence. Buys a
guarantee that derivative notes stay open.

## Chosen

**Apache-2.0 for code, CC-BY-4.0 for vault prose.** The patent grant matters in this field
specifically: electroanatomic mapping and ablation are areas where device vendors hold patents, and
a permissive licence without a grant leaves anyone building on the code less protected than they
should be. For the prose, attribution is the point — the project exists partly as a public record
of the author's work, and CC-BY-4.0 makes credit a condition of reuse without restricting how the
theory may be reused.

## Rejected

**MIT for everything** — rejected for the missing patent grant, which is the one property that
matters most in a patent-dense field, and for fitting prose poorly.

**Apache-2.0 for everything** — rejected because it gives the theory no attribution requirement
suited to academic citation. It would have been workable; it was not the best fit for the vault.

**Apache-2.0 for code, CC-BY-SA-4.0 for prose** — rejected because share-alike terms would make it
harder for others to quote the theory in their own publications, which works against the
project's aim of being cited.

## References

- Constitution, Principle I, Open by Default (as amended in v1.2.0) — `.specify/memory/constitution.md:76`
- Spec 001, FR-013a — `specs/001-theory-vault-traceability/spec.md:231`
- Research note R-002 — `specs/001-theory-vault-traceability/research.md:34`
- Clarification session, 2026-09-20 — [[log-2026-09-20-clarification]]
- Apache License, Version 2.0 — https://www.apache.org/licenses/LICENSE-2.0
- Creative Commons Attribution 4.0 International — https://creativecommons.org/licenses/by/4.0/
- OSI list of approved licences — https://opensource.org/licenses
