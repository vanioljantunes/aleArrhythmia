---
title: aleArrhythmia theory vault
type: theory
status: active
created: 2026-09-21
updated: 2026-09-21
---

# aleArrhythmia theory vault

The theory, decisions and evidence behind aleArrhythmia: Activation Likelihood Estimation adapted
from brain imaging to cardiac electrophysiology, so that arrhythmia origins reported in individual
studies can be pooled into a map.

New here? Read [[README]] first — it explains how notes are laid out and needs no special software.

> **Research use only.** Not a medical device. Nothing in this vault is a clinical recommendation,
> and in the current phase nothing in it is a claim about cardiac results.

## Decision records

Every non-trivial choice the project has made, with the options that were considered, what each
cost, and why one was chosen.

| Record | Decision | Status |
|---|---|---|
| [[ADR-0001-repository-layout]] | The project lives in its own standalone public repository | accepted |
| [[ADR-0002-licensing]] | Apache-2.0 for code, CC-BY-4.0 for vault prose | accepted |
| [[ADR-0003-enforcement-mechanism]] | A local pre-push hook plus a check on every push | accepted |
| [[ADR-0004-citation-scan-scope]] | Scan all tracked text files, minus a reasoned ignore list | accepted |

## Open questions

Choices the project has deliberately not made yet, and what evidence would settle them.

_None yet._

## Theory

How the method works and why.

_None yet._

## Literature

One note per source surveyed.

_None yet._

## Work logs

Dated records of working sessions.

- [[log-2026-09-20-clarification]] — the session that settled repository layout, enforcement, scan
  scope and licensing
- [[log-2026-09-21-enforcement-verification]] — evidence that the pre-push hook and the repository
  workflow each refuse a broken decision record

## Templates

Starting points for each note type live in `templates/`. Copy one, rename it, and fill it in; the
header fields and section headings are already there.

| Template | For |
|---|---|
| `templates/adr.md` | A decision record — options, trade-offs, choice, rejections, references |
| `templates/theory.md` | A derivation or method note |
| `templates/literature.md` | One surveyed source, atlas, file format or system |
| `templates/question.md` | An open question, its candidate answers, and what would settle it |
| `templates/log.md` | A dated working session |

Templates are not notes: they are excluded from the checks, so their placeholder values do not
fail anything.

## Keeping this page complete

Every decision record and every open question must appear on this page. The checker verifies it
and fails when one is missing, so this page cannot silently fall out of date.
