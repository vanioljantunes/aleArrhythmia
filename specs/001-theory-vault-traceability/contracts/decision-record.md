# Contract: Decision Record (ADR)

**Consumers**: the `vaultcheck` checker, every reader auditing a decision, the Phase 2 renderer.

**Stability**: the five section headings are a frozen interface. Renaming one breaks every existing
record and requires a decision record of its own plus a migration of all prior records.

**Location**: `docs/vault/decisions/ADR-NNNN-kebab-slug.md`

---

## Shape

```markdown
---
title: Repository layout
type: adr
status: accepted
id: ADR-0001
created: 2026-09-20
updated: 2026-09-20
---

# ADR-0001: Repository layout

One or two sentences of context: what forced this decision, and when.

## Options considered

- **Standalone public repository**: the project gets its own repository, with its own licences,
  issue tracker and CI.
- **Nested in the private monorepo**: the project stays a folder inside the existing private
  repository, exported periodically to a public snapshot.

## Trade-offs

**Standalone public repository**: costs one more repository to maintain and a clone to keep in
sync locally; buys a public history, independent licensing, and CI that an outside reader can see.

**Nested in the private monorepo**: costs a drifting snapshot and a lost history, since exports
carry no commits; buys one fewer repository and atomic commits across sibling projects.

## Chosen

Standalone public repository. Constitution Principle I requires the work to be public, and the
monorepo is private and must stay so. A snapshot export would break the traceability this project
exists to demonstrate.

## Rejected

**Nested in the private monorepo**: rejected because a public snapshot loses history, which
directly contradicts Principle VIII. The gain, atomic cross-project commits, is not needed: no other
project shares code with this one.

## References

- Constitution Principle I and VIII, `.specify/memory/constitution.md:75`
- Clarification session, 2026-09-20, [[log-2026-09-20-clarification]]
- https://github.com/vanioljantunes/aleArrhythmia
```

---

## Required sections

Exactly these five level-two headings, spelled exactly this way, in any order:

| Heading | Must contain |
|---|---|
| `## Options considered` | At least two named options. An option is named when it appears as a list item or a bolded lead-in |
| `## Trade-offs` | Cost and benefit per option. Non-empty |
| `## Chosen` | The option taken and why it beat the others. Non-empty |
| `## Rejected` | A reason per rejected option. Non-empty. "Not chosen" alone does not satisfy it |
| `## References` | At least one reference in an accepted form |

Content before the first of these headings is free-form context and is not checked. Additional
headings beyond the five are permitted.

**Emptiness**: a section is empty when, after stripping whitespace, HTML comments and unmodified
template placeholder text, nothing remains.

---

## Reference forms

A reference is one list item under `## References`. Accepted forms:

| Form | Example | Local verification |
|---|---|---|
| DOI | `10.1002/hbm.21186` | Pattern `10.\d{4,9}/\S+` |
| URL | `https://example.org/page` | Scheme is `http` or `https` |
| Repository location | `tools/vaultcheck/links.py:42` | File exists; line within range |
| Dataset | `osf:ab12c` | `scheme:identifier`, scheme declared in the checker |
| Conversation | `[[log-2026-09-20-clarification]]` | Target note exists |

Prose alone ("see the paper", "as discussed") is not a reference and fails.

Surrounding prose is allowed on the same line, a DOI followed by author, title and year is
encouraged, so the reference stays traceable if a URL dies.

---

## Identity and supersession

- `id` matches `^ADR-\d{4}$` and equals the filename prefix.
- No two records share an `id`.
- A record is never deleted or rewritten once merged.
- Reversal: write a new record with `supersedes: [ADR-000X]`, and set the old record's `status` to
  `superseded` with `superseded_by: ADR-000Y`. Both sides are required; one-sided supersession is a
  violation naming both files.

---

## Violations emitted

| Rule id | Condition |
|---|---|
| `ADR-MISSING-SECTION` | One of the five headings is absent |
| `ADR-EMPTY-SECTION` | A required section has no content |
| `ADR-TOO-FEW-OPTIONS` | Fewer than two named options |
| `ADR-NO-REFERENCE` | No reference passes any accepted form |
| `ADR-BAD-REFERENCE` | A reference item matches no accepted form |
| `ADR-UNRESOLVED-REFERENCE` | A repository reference names a missing file or an out-of-range line |
| `ADR-DUPLICATE-ID` | Two records share an id; both files named |
| `ADR-ID-FILENAME-MISMATCH` | Frontmatter `id` disagrees with the filename prefix |
| `ADR-SUPERSEDED-NO-TARGET` | `status: superseded` without `superseded_by` |
| `ADR-SUPERSESSION-ONE-SIDED` | Supersession declared by only one of the two records |
| `ADR-SUPERSESSION-DANGLING` | `supersedes` or `superseded_by` names a record that does not exist |
