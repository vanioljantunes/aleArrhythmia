# Contract: Note Frontmatter

**Consumers**: the `vaultcheck` checker, the Phase 2 static renderer, Obsidian, any editor.

**Stability**: adding an optional key is backward-compatible. Removing a key, renaming one, or
narrowing a vocabulary is breaking and requires a decision record.

---

## Envelope

A note is a UTF-8 text file ending in `.md`. It opens with a YAML frontmatter block: a line
containing exactly `---`, the YAML body, and a closing line containing exactly `---`. The first line
of the file is the opening delimiter — no blank line, no byte-order mark before it.

```markdown
---
title: Universal Ventricular Coordinates
type: literature
status: active
created: 2026-09-20
updated: 2026-09-20
tags: [reference-space, ventricle]
---

# Universal Ventricular Coordinates

Body text begins here.
```

Parsed with `yaml.safe_load`. Anything `safe_load` refuses is a violation attributed to the file, not
a crash.

---

## Keys

### Required on every note

| Key | Type | Constraint |
|---|---|---|
| `title` | string | Non-empty after stripping whitespace |
| `type` | string | One of `theory`, `adr`, `literature`, `question`, `log` |
| `status` | string | Must belong to the vocabulary for `type` (below) |
| `created` | date | ISO `YYYY-MM-DD`; unquoted, so YAML yields a date |
| `updated` | date | ISO `YYYY-MM-DD`; not earlier than `created` |

### Optional on every note

| Key | Type | Constraint |
|---|---|---|
| `tags` | list of string | Not validated; free-form |

### Required on `type: adr`

| Key | Type | Constraint |
|---|---|---|
| `id` | string | Matches `^ADR-\d{4}$`; equals the filename's `ADR-NNNN` prefix |

### Conditional

| Key | Type | Required when | Constraint |
|---|---|---|---|
| `superseded_by` | string | `type: adr` and `status: superseded` | An existing ADR id; the target must list this record in its `supersedes` |
| `supersedes` | list of string | never | Each entry an existing ADR id; each target must name this record in `superseded_by` |
| `answered_by` | string | `type: question` and `status: answered` | An existing ADR id |

---

## Status vocabularies

| `type` | Allowed `status` |
|---|---|
| `theory`, `literature`, `log` | `draft`, `active`, `archived` |
| `adr` | `proposed`, `accepted`, `superseded` |
| `question` | `open`, `answered` |

Any other value is a violation. The vocabularies are closed deliberately — see R-011.

---

## Filename rules

- Extension `.md`.
- Basename unique across the whole vault, regardless of folder.
- Decision records: `ADR-NNNN-kebab-slug.md`, the numeric part matching frontmatter `id`.
- Other notes: kebab-case recommended, not enforced.

---

## Body conventions

- The body MAY open with a level-one heading. It is not required and is not checked.
- Links between notes use wikilinks: `[[basename]]`, `[[basename|display text]]`,
  `[[basename#heading]]`. Standard Markdown links are permitted for external URLs.
- No note may require a plugin to be understood. Callouts, dataview queries, templater syntax and
  embedded query blocks are not permitted (FR-002).

---

## Violations emitted

| Rule id | Condition |
|---|---|
| `NOTE-MISSING-FIELD` | A required key is absent or empty |
| `NOTE-BAD-TYPE` | `type` outside the enum |
| `NOTE-BAD-STATUS` | `status` outside the vocabulary for its `type` |
| `NOTE-BAD-DATE` | `created` or `updated` not an ISO date, or `updated` earlier than `created` |
| `NOTE-DUPLICATE-BASENAME` | Two notes share a basename; both files named |
| `NOTE-BAD-FRONTMATTER` | Missing or malformed frontmatter block |
| `NOTE-PLUGIN-SYNTAX` | Plugin-dependent syntax found in the body |
