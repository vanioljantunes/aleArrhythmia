---
title: Reading this vault
type: theory
status: active
created: 2026-09-21
updated: 2026-09-21
---

# Reading this vault

This folder is the theory behind aleArrhythmia: derivations, method notes, literature summaries,
open questions, decision records and work logs. It is written to be read by anyone, with any
text editor or directly on the code host. You do not need Obsidian, or any other application.

**Start at [index.md](index.md).** Every note is reachable from there in two links or fewer.

## What a note looks like

Every note is a plain Markdown file that opens with a short header between two `---` lines:

```yaml
---
title: Universal Ventricular Coordinates
type: literature
status: active
created: 2026-09-20
updated: 2026-09-20
---
```

That header is for machines — the checker and, later, the website. Everything below it is ordinary
prose for people. You can ignore the header entirely and read the note.

| Field | Meaning |
|---|---|
| `title` | What the note is about |
| `type` | One of the five note types below |
| `status` | Where the note is in its life — see below |
| `created` / `updated` | Dates, always written year-month-day |

## The five note types

| Type | Folder | What it holds |
|---|---|---|
| `adr` | `decisions/` | A **decision record**. One decision, the options that were on the table, what each cost, which was chosen and why, why the others lost, and the evidence. Numbered `ADR-0001`, `ADR-0002`, and so on |
| `theory` | `theory/` | Derivations and method notes — how the method works and why |
| `literature` | `literature/` | One note per source surveyed: a paper, an atlas, a file format |
| `question` | `questions/` | An open question the project has not yet answered, what the candidate answers are, and what evidence would settle it |
| `log` | `logs/` | A dated record of a working session — what was asked, what was decided, what was tried |

## Status values

| Type | Possible status |
|---|---|
| `theory`, `literature`, `log` | `draft`, `active`, `archived` |
| `adr` | `proposed`, `accepted`, `superseded` |
| `question` | `open`, `answered` |

A superseded decision record is never deleted. It stays readable, and it names the record that
replaced it. Reversals are part of the history, not erased from it.

## Links

Notes link to each other with double square brackets: `[[canonical-reference-space]]` means "the
note whose file is named `canonical-reference-space.md`", wherever in the vault it lives. On the
code host these appear as literal text; open the named file to follow them. Every such link is
checked automatically — a link to a note that does not exist fails the check.

Decision records are cited by number anywhere in the project — in code, specifications and notes —
as `ADR-0003`. Those citations are checked too.

## Templates

`templates/` holds one starting file per note type. Copy the one you need; its header and section
headings are already in place.

## Licence

The prose in this folder is licensed under CC-BY-4.0: you may quote and reuse it with attribution.
The code elsewhere in the repository is under a different licence. See the root `README.md`.
