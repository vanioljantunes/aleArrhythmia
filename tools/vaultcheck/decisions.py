"""Decision records: required sections, options, references, identity, supersession.

Contract: specs/001-theory-vault-traceability/contracts/decision-record.md
"""

from __future__ import annotations

import re
from pathlib import Path

from .frontmatter import Note, is_empty, sections, strip_comments
from .report import Violation

REQUIRED_SECTIONS = ("Options considered", "Trade-offs", "Chosen", "Rejected", "References")

ADR_ID = re.compile(r"^ADR-\d{4}$")
_FILENAME = re.compile(r"^(ADR-\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*$")
_ITEM = re.compile(r"^[-*+]\s+(.*)$")
_BOLD_LEAD = re.compile(r"^\*\*[^*]+\*\*")

# Accepted reference forms (contract: decision-record.md, "Reference forms").
_DOI = re.compile(r"\b10\.\d{4,9}/\S+")
_URL = re.compile(r"https?://\S+")
_DATASET = re.compile(r"\b(?:osf|zenodo|figshare|pmid|pmcid|arxiv):[\w./-]+", re.I)
_WIKILINK = re.compile(r"\[\[[^\]]+\]\]")
_CODE_TOKEN = re.compile(r"`([^`\s]+)`")
_REPO_PATH = re.compile(r"^(?P<path>[\w.\-/]+?)(?::(?P<line>\d+))?$")


def _items(content: str) -> list[tuple[int, str]]:
    """Top-level list items as (0-based line offset, text). Indented lines continue an item.

    If the section has no list at all, each non-blank line counts as an item, so prose-only
    references are still examined and rejected rather than silently skipped.
    """
    lines = strip_comments(content).split("\n")
    items: list[tuple[int, str]] = []
    for n, line in enumerate(lines):
        m = _ITEM.match(line)
        if m:
            items.append((n, m.group(1)))
        elif items and line.startswith((" ", "\t")) and line.strip():
            off, text = items[-1]
            items[-1] = (off, f"{text} {line.strip()}")
    if not items:
        items = [(n, line.strip()) for n, line in enumerate(lines) if line.strip()]
    return items


_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
_TABLE_RULE = re.compile(r"^\s*\|[\s:|-]+\|\s*$")


def _count_options(content: str) -> int:
    """Options are named as table rows, top-level list items, or bold-led paragraphs (ADR-0005)."""
    lines = strip_comments(content).split("\n")
    rows = [line for line in lines if _TABLE_ROW.match(line)]
    if rows:
        separators = sum(1 for line in rows if _TABLE_RULE.match(line))
        # every table has one header row and one separator row; the rest are options
        return len(rows) - 2 * separators
    listed = sum(1 for line in lines if _ITEM.match(line))
    if listed:
        return listed
    return sum(1 for para in "\n".join(lines).split("\n\n") if _BOLD_LEAD.match(para.strip()))


def _repo_candidate(token: str) -> re.Match | None:
    """A code-span token is treated as a repository location only if it looks like one."""
    m = _REPO_PATH.match(token)
    if not m:
        return None
    path = m.group("path")
    if m.group("line") or "/" in path or path.startswith("."):
        return m
    return None


def _check_reference(root: Path, note: Note, line: int, text: str) -> tuple[bool, list[Violation]]:
    """Return (counts as a valid reference, violations)."""
    v: list[Violation] = []
    has_form = bool(_DOI.search(text) or _URL.search(text) or _DATASET.search(text) or _WIKILINK.search(text))
    for token in _CODE_TOKEN.findall(text):
        m = _repo_candidate(token)
        if not m:
            continue
        target = root / m.group("path")
        if not target.is_file():
            v.append(Violation(note.path, line, "ADR-UNRESOLVED-REFERENCE",
                               f"'{m.group('path')}' does not exist in the repository"))
            continue
        if m.group("line"):
            want = int(m.group("line"))
            have = len(target.read_text(encoding="utf-8", errors="replace").splitlines())
            if want < 1 or want > have:
                v.append(Violation(note.path, line, "ADR-UNRESOLVED-REFERENCE",
                                   f"'{token}' points past the end of the file ({have} lines)"))
                continue
        has_form = True
    if not has_form and not v:
        v.append(Violation(note.path, line, "ADR-BAD-REFERENCE",
                           "not a reference in an accepted form (DOI, URL, repository path, "
                           f"dataset id, or wikilink): {text[:60]!r}"))
    return has_form and not v, v


def _as_list(value: object) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [str(x) for x in value]
    return [str(value)]


def check_decisions(root: Path, notes: list[Note]) -> tuple[list[Violation], set[str]]:
    """Validate every decision record. Returns the violations and the set of existing ADR ids."""
    adrs = [n for n in notes if n.meta is not None and n.type == "adr"]
    v: list[Violation] = []

    for note in adrs:
        meta = note.meta or {}
        rid = str(meta.get("id", ""))
        fname = _FILENAME.match(note.basename)
        if meta.get("id") not in (None, "") and (not ADR_ID.match(rid) or not fname or fname.group(1) != rid):
            expected = fname.group(1) if fname else "a filename of the form ADR-NNNN-slug.md"
            v.append(Violation(note.path, note.key_lines.get("id", 1), "ADR-ID-FILENAME-MISMATCH",
                               f"id '{rid}' does not match {expected}"))

        secs = sections(note)
        for heading in REQUIRED_SECTIONS:
            if heading not in secs:
                v.append(Violation(note.path, note.body_line, "ADR-MISSING-SECTION",
                                   f"required section '## {heading}' is absent"))
                continue
            line, content = secs[heading]
            if is_empty(content):
                rule = "ADR-NO-REFERENCE" if heading == "References" else "ADR-EMPTY-SECTION"
                v.append(Violation(note.path, line, rule, f"'## {heading}' has no content"))

        if "Options considered" in secs and not is_empty(secs["Options considered"][1]):
            line, content = secs["Options considered"]
            count = _count_options(content)
            if count < 2:
                v.append(Violation(note.path, line, "ADR-TOO-FEW-OPTIONS",
                                   f"{count} named option{'s' if count != 1 else ''}; at least two are required"))

        if "References" in secs and not is_empty(secs["References"][1]):
            line, content = secs["References"]
            valid = 0
            for off, text in _items(content):
                ok, found = _check_reference(root, note, line + 1 + off, text)
                valid += ok
                v.extend(found)
            if valid == 0:
                v.append(Violation(note.path, line, "ADR-NO-REFERENCE", "no reference in an accepted form"))

    # identity
    by_id: dict[str, list[Note]] = {}
    for note in adrs:
        rid = str((note.meta or {}).get("id", ""))
        if ADR_ID.match(rid):
            by_id.setdefault(rid, []).append(note)
    for rid, group in by_id.items():
        if len(group) > 1:
            for n in group:
                others = ", ".join(o.path for o in group if o is not n)
                v.append(Violation(n.path, n.key_lines.get("id", 1), "ADR-DUPLICATE-ID",
                                   f"{rid} is also claimed by {others}"))

    # supersession
    first = {rid: group[0] for rid, group in by_id.items()}
    for note in adrs:
        meta = note.meta or {}
        rid = str(meta.get("id", ""))
        sb = meta.get("superseded_by")
        if meta.get("status") == "superseded" and sb in (None, ""):
            v.append(Violation(note.path, note.key_lines.get("status", 1), "ADR-SUPERSEDED-NO-TARGET",
                               "status is 'superseded' but 'superseded_by' names no record"))
        if sb not in (None, ""):
            target = first.get(str(sb))
            if target is None:
                v.append(Violation(note.path, note.key_lines.get("superseded_by", 1),
                                   "ADR-SUPERSESSION-DANGLING", f"superseded_by names {sb}, which does not exist"))
            elif rid not in _as_list((target.meta or {}).get("supersedes")):
                _one_sided(v, note, "superseded_by", target, "supersedes",
                           f"{rid} says it is superseded by {sb}, but {sb} does not list {rid} in 'supersedes'")
        for s in _as_list(meta.get("supersedes")):
            target = first.get(s)
            if target is None:
                v.append(Violation(note.path, note.key_lines.get("supersedes", 1),
                                   "ADR-SUPERSESSION-DANGLING", f"supersedes names {s}, which does not exist"))
            elif str((target.meta or {}).get("superseded_by", "")) != rid:
                _one_sided(v, note, "supersedes", target, "superseded_by",
                           f"{rid} says it supersedes {s}, but {s} does not name {rid} in 'superseded_by'")

    return v, set(by_id)


def _one_sided(v: list[Violation], a: Note, a_key: str, b: Note, b_key: str, message: str) -> None:
    v.append(Violation(a.path, a.key_lines.get(a_key, 1), "ADR-SUPERSESSION-ONE-SIDED", message))
    v.append(Violation(b.path, b.key_lines.get(b_key, 1), "ADR-SUPERSESSION-ONE-SIDED", message))
