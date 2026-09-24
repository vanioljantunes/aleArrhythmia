# Contributing

This project records why it does things, as well as what it does. A change to the code and a change
to the reasoning behind it arrive together.

Two rules cover most of it:

1. Anything you assert has a source you can point to.
2. Run the checker before you push. The hook runs it anyway.

## Set up

```
git clone https://github.com/vanioljantunes/aleArrhythmia.git
cd aleArrhythmia
git config core.hooksPath .githooks
python -m tools.vaultcheck
python -m pytest -q
```

The `git config` line is not optional. Without it the pre-push hook never runs, and a broken record
reaches the remote and fails in CI instead.

Python 3.11 or newer. No dependencies for the checker itself.

## The one thing that surprises people

**Stage a new note before running the checker.** Discovery uses `git ls-files`, so an unstaged file
does not exist as far as the checker is concerned. Links pointing at it report as unresolved and
the note itself is never checked.

```
git add docs/vault/theory/my-new-note.md
python -m tools.vaultcheck
```

If you see `LINK-UNRESOLVED` for a note you just wrote, this is why.

## Adding a note

| Step | Do |
|---|---|
| 1 | Copy the right template from `docs/vault/templates/` |
| 2 | Put it in the folder matching its type: `theory/`, `literature/`, `questions/`, `decisions/`, `logs/` |
| 3 | Fill the frontmatter. `title`, `type`, `status`, `created`, `updated`. Dates are ISO, `2026-09-24` |
| 4 | Link related notes with `[[note-basename]]`, no path and no extension |
| 5 | `git add` it, then run the checker |

Filenames are kebab-case and unique across the whole vault, because wikilinks resolve by basename.

A title containing a colon must be quoted, or the YAML parser rejects the header:

```yaml
title: "Hybrid: continuous coordinates with segment labels"
```

## When a decision needs a record

Write an ADR when all three are true:

| Test | Meaning |
|---|---|
| Hard to reverse | Changing your mind later costs something real |
| Surprising without context | A future reader will ask why it was done this way |
| A genuine trade-off | Real alternatives existed and one was picked for stated reasons |

Two of three is not enough. A decision with one obvious answer does not need a record; the code is
the record.

Some changes require one regardless. Principles II, III, V and VI of the constitution cannot be
amended without an ADR. See `.specify/memory/constitution.md`.

An ADR has five sections, in this order, none empty:

```
## Options considered      at least two, usually a table
## Trade-offs              what each option costs and gains
## Chosen                  which one, and why
## Rejected                each loser, and why it lost
## References              at least one resolvable source
```

A reference is a DOI, a URL, a repository-relative path or a `[[wikilink]]`. "Common knowledge" is
not a reference. If you cannot cite it, you have not finished thinking about it.

Numbering is sequential and permanent: `ADR-NNNN-short-slug.md`, with the same id in the
frontmatter. Superseding an ADR is a two-way link, never a deletion. Records are appended to, not
rewritten.

Every ADR and every open question must be listed in `docs/vault/index.md`. The checker fails if one
is missing.

## Writing style

Rules live in ADR-0005. The checker enforces the mechanical half.

| Rule | Why |
|---|---|
| No em dashes. Use a comma, a colon or a full stop | Author preference, enforced as an error |
| No curly quotes. Straight quotes only | Same |
| Prefer tables and flowcharts over paragraphs | Faster to scan, harder to hide vagueness in |
| Say the thing, then stop | |

Some words raise a warning rather than an error: the vocabulary that signals machine-written prose.
A warning does not block a push. Read it, decide, move on.

## Commits

Conventional prefixes: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `ci:`.

A commit that embodies a decision cites the record: `Decision cited: ADR-0007.` This is a governance
requirement, not a convention.

## Before you push

```
git add -A
python -m tools.vaultcheck
python -m pytest -q
```

Exit codes: `0` clean, `1` violations found, `2` the checker itself failed.

Never use `--no-verify`. If the hook blocks you, the hook is right. Fix the record.

## Scope, for now

This phase builds the traceability machinery, not the science. No claim about cardiac anatomy,
arrhythmia mechanism or statistical result belongs in the vault yet. Surveyed sources and recorded
unknowns, yes. Conclusions, no.

An unknown is a finding. Write it down, say what you tried, and leave it visible rather than
guessing. `docs/vault/literature/survey-unknowns-2026-09-24.md` is the pattern.

## Research use only

This is a research tool. It is not a medical device, it is not validated for clinical use, and no
output of it should guide a procedure. Keep that true in anything you add.
