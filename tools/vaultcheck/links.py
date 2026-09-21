"""Wikilinks, citations of decision records, open questions, and index completeness.

Contract: specs/001-theory-vault-traceability/contracts/vaultcheck-cli.md
Decision: ADR-0004 (citation form and scan scope).
"""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

from .frontmatter import Note, headings, is_empty, sections, strip_code
from .report import Violation

WIKILINK = re.compile(r"!?\[\[([^\]\n]+)\]\]")
CITATION = re.compile(r"\bADR-\d{4}\b")
_COMMENT = re.compile(r"<!--.*?-->", re.S)


def _masked(text: str) -> list[str]:
    """Text with code and HTML comments blanked, line numbers preserved.

    Links inside code are examples, not links; links inside comments are template guidance.
    """
    no_comments = _COMMENT.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return strip_code(no_comments).split("\n")


def _split_target(raw: str) -> tuple[str, str]:
    target = raw.split("|", 1)[0]
    name, _, anchor = target.partition("#")
    name = PurePosixPath(name.strip()).name
    if name.endswith(".md"):
        name = name[:-3]
    return name, anchor.strip()


def link_targets(note: Note) -> set[str]:
    found = set()
    for line in _masked(note.body):
        for m in WIKILINK.finditer(line):
            name, _ = _split_target(m.group(1))
            if name:
                found.add(name)
    return found


def check_links(notes: list[Note], tracked: list[str]) -> tuple[list[Violation], int]:
    by_name = {n.basename: n for n in notes}
    asset_names = {PurePosixPath(p).name for p in tracked}
    v: list[Violation] = []
    count = 0
    for note in notes:
        for n, line in enumerate(_masked(note.body)):
            for m in WIKILINK.finditer(line):
                count += 1
                name, anchor = _split_target(m.group(1))
                where = note.body_line + n
                if not name:
                    target = note
                elif name in by_name:
                    target = by_name[name]
                elif "." in name and name in asset_names:
                    continue
                else:
                    v.append(Violation(note.path, where, "LINK-UNRESOLVED",
                                       f"[[{m.group(1)}]] points at no note named '{name}'"))
                    continue
                if anchor and anchor.lower() not in headings(target):
                    v.append(Violation(note.path, where, "LINK-BAD-ANCHOR",
                                       f"'{target.basename}' has no heading '{anchor}'"))
    return v, count


def check_citations(root: Path, files: list[str], ids: set[str]) -> tuple[list[Violation], int]:
    v: list[Violation] = []
    count = 0
    for rel in files:
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for n, line in enumerate(text.splitlines(), start=1):
            for m in CITATION.finditer(line):
                count += 1
                if m.group(0) not in ids:
                    v.append(Violation(rel, n, "CITE-DANGLING", f"cites {m.group(0)}, which does not exist"))
    return v, count


def check_questions(notes: list[Note], ids: set[str]) -> list[Violation]:
    v: list[Violation] = []
    for q in notes:
        if q.meta is None or q.type != "question":
            continue
        secs = sections(q)
        status = q.meta.get("status")
        if status == "open":
            cand = secs.get("Candidates")
            if cand is None or not any(WIKILINK.search(line) for line in _masked(cand[1])):
                v.append(Violation(q.path, cand[0] if cand else q.body_line, "Q-NO-CANDIDATES",
                                   "an open question must link at least one candidate under '## Candidates'"))
        crit = secs.get("What would settle it")
        if crit is None or is_empty(crit[1]):
            v.append(Violation(q.path, crit[0] if crit else q.body_line, "Q-NO-CRITERIA",
                               "'## What would settle it' is missing or empty"))
        if status == "answered":
            ab = q.meta.get("answered_by")
            if ab in (None, "") or str(ab) not in ids:
                v.append(Violation(q.path, q.key_lines.get("answered_by", q.key_lines.get("status", 1)),
                                   "Q-ANSWERED-NO-TARGET",
                                   "status is 'answered' but 'answered_by' names no existing decision record"))
    return v


def check_index(vault_rel: str, notes: list[Note]) -> list[Violation]:
    """Every decision record and open question must be listed on the vault index."""
    required = [n for n in notes if n.meta is not None and n.type in ("adr", "question")]
    if not required:
        return []
    index_path = f"{vault_rel}/index.md" if vault_rel else "index.md"
    index = next((n for n in notes if n.path == index_path), None)
    if index is None:
        return [Violation(index_path, 1, "INDEX-INCOMPLETE",
                          "the vault has decision records or questions but no index.md")]
    listed = link_targets(index)
    return [
        Violation(index.path, 1, "INDEX-INCOMPLETE", f"index does not list {n.basename} ({n.type})")
        for n in required if n.basename not in listed
    ]
