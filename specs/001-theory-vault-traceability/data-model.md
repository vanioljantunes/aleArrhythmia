# Phase 1 Data Model: Theory Vault and Decision Traceability

**Feature**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Research**: [research.md](./research.md)

The "data" here is files. Nothing is stored in a database; every entity below is a Markdown file or
a construct parsed out of one. Field names are frontmatter keys unless stated otherwise.

---

## Note

The base entity. Every file under `docs/vault/` is a Note.

| Field | Type | Required | Notes |
|---|---|---|---|
| `title` | string | yes | Human-readable; need not match the filename |
| `type` | enum | yes | `theory`, `adr`, `literature`, `question`, `log` |
| `status` | enum | yes | Vocabulary depends on `type` — see below |
| `created` | date | yes | ISO `YYYY-MM-DD` |
| `updated` | date | yes | ISO `YYYY-MM-DD`; must be >= `created` |
| `tags` | list of string | no | Free-form; not validated |

Non-frontmatter attributes, derived by the checker:

- **basename** — filename without `.md`. Unique across the entire vault (R-004).
- **body** — everything after the closing `---`.
- **outbound links** — every `[[...]]` occurrence in the body.

**Status vocabulary by type**

| `type` | allowed `status` |
|---|---|
| `theory` | `draft`, `active`, `archived` |
| `literature` | `draft`, `active`, `archived` |
| `log` | `draft`, `active`, `archived` |
| `adr` | `proposed`, `accepted`, `superseded` |
| `question` | `open`, `answered` |

**Validation rules**

- V-N1 (FR-003, FR-020): all required fields present, non-empty, correctly typed.
- V-N2 (FR-003): `created` and `updated` parse as ISO dates; `updated` is not earlier than `created`.
- V-N3 (R-011): `status` belongs to the vocabulary for its `type`.
- V-N4 (R-004): basename is unique vault-wide.
- V-N5 (FR-002): the file parses as UTF-8 text with a well-formed frontmatter block.

---

## DecisionRecord

A Note with `type: adr`, living in `docs/vault/decisions/`. Carries extra fields and a required body
structure.

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | Exactly `ADR-` plus four digits, e.g. `ADR-0007` |
| `supersedes` | list of ADR id | no | Records this one replaces |
| `superseded_by` | ADR id | conditional | Required when `status: superseded` |

**Required body sections** — level-two headings, exact wording (R-005):

| Heading | Content requirement |
|---|---|
| `## Options considered` | At least two named options |
| `## Trade-offs` | Non-empty; states cost and benefit per option |
| `## Chosen` | Non-empty; names the option and the reason it won |
| `## Rejected` | Non-empty; a reason per rejected option |
| `## References` | At least one Reference |

**Validation rules**

- V-D1 (FR-008, FR-015): all five sections present and non-empty. Placeholder comments carried over
  from the template do not count as content.
- V-D2 (FR-008): `## Options considered` contains at least two distinct named options.
- V-D3 (FR-010, FR-016): `id` is unique across all decision records.
- V-D4 (R-006): the `ADR-NNNN` prefix of the filename equals `id`.
- V-D5 (FR-018): `status: superseded` requires `superseded_by`, pointing at an existing record.
- V-D6 (FR-018): supersession is reciprocal — if A declares `superseded_by: B`, then B must declare
  A in its `supersedes`. A one-sided declaration is a violation, named on both files.
- V-D7 (FR-008, FR-015): `## References` yields at least one Reference passing V-R1.
- V-D8 (FR-011): a record's `id` never disappears between commits. Enforced by review, not by the
  checker, which sees only the working tree.

**State transitions**

```text
proposed ──accepted──> accepted ──superseded by a new record──> superseded
    │
    └──abandoned before acceptance──> (record stays, status proposed)
```

A record is never deleted or rewritten (FR-011). `superseded` is terminal: a record that is
superseded and later revived is a new record superseding the superseding one.

---

## Reference

Not a file — a line or inline item inside a decision record's `## References` section.

| Kind | Accepted form | Local check |
|---|---|---|
| Published work | DOI matching `10.\d{4,9}/\S+` | Shape only |
| Web page | `http://` or `https://` URL | Shape only; no network request |
| Repository location | `path/to/file.py:123` or `path/to/file.py` | File exists; line number within range |
| Dataset | `scheme:identifier` with a declared scheme | Shape only |
| Conversation | `[[note-basename]]` pointing at a note holding the transcript | Target note exists |

**Validation rules**

- V-R1 (FR-009): each reference matches exactly one accepted kind. Bare prose — "see the paper" —
  fails.
- V-R2 (FR-009, R-007): repository references resolve against the working tree; a missing file or an
  out-of-range line is a violation.
- V-R3 (R-007): no reference is checked over the network, ever.

---

## OpenQuestion

A Note with `type: question`, in `docs/vault/questions/`.

| Field | Type | Required | Notes |
|---|---|---|---|
| `answered_by` | ADR id | conditional | Required when `status: answered` |

**Required body sections**: `## The question`, `## Candidates`, `## What would settle it`.

**Validation rules**

- V-Q1 (FR-028): `status: open` requires at least one outbound link under `## Candidates`.
- V-Q2 (FR-028): `## What would settle it` is non-empty.
- V-Q3 (R-011): `status: answered` requires `answered_by` pointing at an existing decision record.

---

## Citation

An occurrence of an `ADR-NNNN` identifier in any scanned file outside the decision record that owns
it. Has a path, a line number and an identifier.

**Validation rules**

- V-C1 (FR-017): the identifier resolves to an existing decision record.
- V-C2 (FR-009, R-009): recognised only in the exact `ADR-` plus four digits form, on a word
  boundary.
- V-C3 (FR-017a): found in any version-controlled text file not excluded by an IgnoreRule.

---

## Link

An occurrence of `[[target]]`, `[[target|alias]]` or `[[target#heading]]` in a note body.

**Validation rules**

- V-L1 (FR-019, FR-006): `target` matches the basename of exactly one note.
- V-L2 (R-004): a `#heading` fragment, when present, matches a heading in the target note.

---

## IgnoreRule

A line in `.vaultcheckignore`.

| Part | Required | Notes |
|---|---|---|
| glob | yes | `fnmatch` pattern over repository-relative POSIX paths |
| reason | yes | Trailing `# ...` comment |

**Validation rules**

- V-I1 (R-010): every non-blank, non-comment line carries a trailing reason comment.
- V-I2 (R-010): a rule matching nothing is reported as a warning, not a failure — stale exclusions
  should be visible without blocking work.

---

## VaultIndex

`docs/vault/index.md` — a Note of type `theory`, status `active`, serving as the entry page.

**Validation rules**

- V-X1 (FR-005): links to every note type's section, so any note is two links away.
- V-X2 (FR-005): lists every open question and every decision record. Generated or hand-maintained;
  if hand-maintained, the checker verifies completeness against what it found on disk.

---

## Relationships

```text
Note ──is-a──> DecisionRecord | OpenQuestion | (theory | literature | log)

DecisionRecord ──supersedes──> DecisionRecord        (reciprocal, V-D6)
DecisionRecord ──contains──>  Reference (1..n)
OpenQuestion   ──candidates──> Note (1..n, via Link)
OpenQuestion   ──answered_by──> DecisionRecord (0..1)
Note           ──links──>     Note (0..n, via Link)
AnyTrackedFile ──cites──>     DecisionRecord (0..n, via Citation)
IgnoreRule     ──excludes──>  AnyTrackedFile
VaultIndex     ──indexes──>   Note (all)
```

---

## Requirement coverage

| Requirement | Enforced by |
|---|---|
| FR-002, FR-003, FR-020 | V-N1, V-N2, V-N5 |
| FR-005 | V-X1, V-X2 |
| FR-006, FR-019 | V-L1, V-L2 |
| FR-008, FR-015 | V-D1, V-D2, V-D7 |
| FR-009 | V-R1, V-R2, V-R3 |
| FR-010, FR-016 | V-D3, V-D4 |
| FR-011 | V-D8 (review), plus the never-delete rule in governance |
| FR-012, FR-017, FR-017a | V-C1, V-C2, V-C3 |
| FR-018 | V-D5, V-D6 |
| FR-028 | V-Q1, V-Q2, V-Q3 |
| R-010 ignore-list hygiene | V-I1, V-I2 |
