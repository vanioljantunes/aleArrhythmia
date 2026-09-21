"""Note parsing, header validation, and the Markdown helpers other rule modules share.

Contract: specs/001-theory-vault-traceability/contracts/note-frontmatter.md
"""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .report import Violation

REQUIRED = ("title", "type", "status", "created", "updated")
STATUSES: dict[str, tuple[str, ...]] = {
    "theory": ("draft", "active", "archived"),
    "literature": ("draft", "active", "archived"),
    "log": ("draft", "active", "archived"),
    "adr": ("proposed", "accepted", "superseded"),
    "question": ("open", "answered"),
}
PLUGIN_FENCES = {"dataview", "dataviewjs", "query", "tasks"}

_FENCE = re.compile(r"^\s*(`{3,}|~{3,})\s*([\w-]*)")
_INLINE_CODE = re.compile(r"`[^`\n]*`")
_COMMENT = re.compile(r"<!--.*?-->", re.S)
_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
_CALLOUT = re.compile(r"^\s*>\s*\[![\w-]+\]")


@dataclass
class Note:
    path: str                      # repository-relative, POSIX
    basename: str
    meta: dict | None
    body: str
    body_line: int                 # 1-based line where the body starts
    key_lines: dict[str, int] = field(default_factory=dict)

    @property
    def type(self) -> str | None:
        return (self.meta or {}).get("type")


# ---------- Markdown helpers ----------

def strip_code(text: str) -> str:
    """Blank out fenced blocks and inline code spans, keeping every line in place."""
    out: list[str] = []
    fence: str | None = None
    for line in text.split("\n"):
        m = _FENCE.match(line)
        if fence is None and m:
            fence = m.group(1)
            out.append("")
        elif fence is not None:
            if line.strip().startswith(fence):
                fence = None
            out.append("")
        else:
            out.append(_INLINE_CODE.sub(lambda s: " " * len(s.group(0)), line))
    return "\n".join(out)


def strip_comments(text: str) -> str:
    return _COMMENT.sub("", text)


def fence_languages(text: str) -> list[tuple[int, str]]:
    """(0-based line, language) for every opening code fence that names a language."""
    found: list[tuple[int, str]] = []
    fence: str | None = None
    for n, line in enumerate(text.split("\n")):
        m = _FENCE.match(line)
        if fence is None and m:
            fence = m.group(1)
            if m.group(2):
                found.append((n, m.group(2).lower()))
        elif fence is not None and line.strip().startswith(fence):
            fence = None
    return found


def sections(note: Note, level: int = 2) -> dict[str, tuple[int, str]]:
    """Map heading text to (1-based line, raw content until the next heading of level <= level)."""
    lines = note.body.split("\n")
    masked = strip_code(note.body).split("\n")
    result: dict[str, tuple[int, str]] = {}
    current: str | None = None
    start = 0
    for i, line in enumerate(masked):
        m = _HEADING.match(line)
        if m and len(m.group(1)) <= level:
            if current is not None:
                result[current] = (note.body_line + start, "\n".join(lines[start + 1:i]))
            current = m.group(2).strip() if len(m.group(1)) == level else None
            start = i
    if current is not None:
        result[current] = (note.body_line + start, "\n".join(lines[start + 1:]))
    return result


def headings(note: Note) -> set[str]:
    found = set()
    for line in strip_code(note.body).split("\n"):
        m = _HEADING.match(line)
        if m:
            found.add(m.group(2).strip().lower())
    return found


def is_empty(content: str) -> bool:
    return not strip_comments(content).strip()


# ---------- parsing ----------

def parse(root: Path, rel: str) -> tuple[Note, list[Violation]]:
    text = (root / rel).read_text(encoding="utf-8").replace("\r\n", "\n")
    basename = Path(rel).stem
    if text.startswith("﻿") or not text.startswith("---\n"):
        return Note(rel, basename, None, text, 1), [
            Violation(rel, 1, "NOTE-BAD-FRONTMATTER", "note must open with a '---' header block on line 1")
        ]
    lines = text.split("\n")
    close = next((i for i in range(1, len(lines)) if lines[i].rstrip() == "---"), None)
    if close is None:
        return Note(rel, basename, None, text, 1), [
            Violation(rel, 1, "NOTE-BAD-FRONTMATTER", "header block is never closed with '---'")
        ]
    header = "\n".join(lines[1:close])
    body = "\n".join(lines[close + 1:])
    try:
        meta = yaml.safe_load(header) or {}
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        line = mark.line + 2 if mark else 1
        return Note(rel, basename, None, body, close + 2), [
            Violation(rel, line, "NOTE-BAD-FRONTMATTER", f"header is not valid YAML ({exc.__class__.__name__})")
        ]
    if not isinstance(meta, dict):
        return Note(rel, basename, None, body, close + 2), [
            Violation(rel, 2, "NOTE-BAD-FRONTMATTER", "header must be a mapping of keys to values")
        ]
    key_lines: dict[str, int] = {}
    for i in range(1, close):
        m = re.match(r"^([A-Za-z_]\w*)\s*:", lines[i])
        if m:
            key_lines[m.group(1)] = i + 1
    return Note(rel, basename, meta, body, close + 2, key_lines), []


def _as_date(value: object) -> dt.date | None:
    if isinstance(value, dt.datetime):
        return None
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value)
        except ValueError:
            return None
    return None


def check_note(note: Note) -> list[Violation]:
    if note.meta is None:
        return []
    v: list[Violation] = []
    meta = note.meta

    def at(key: str) -> int:
        return note.key_lines.get(key, 1)

    required = REQUIRED + (("id",) if meta.get("type") == "adr" else ())
    for key in required:
        if meta.get(key) in (None, ""):
            v.append(Violation(note.path, at(key), "NOTE-MISSING-FIELD",
                               f"required field '{key}' is missing or empty"))
    kind = meta.get("type")
    if kind not in (None, "") and kind not in STATUSES:
        v.append(Violation(note.path, at("type"), "NOTE-BAD-TYPE",
                           f"'{kind}' is not a note type (expected: {', '.join(STATUSES)})"))
    status = meta.get("status")
    if kind in STATUSES and status not in (None, "") and status not in STATUSES[kind]:
        v.append(Violation(note.path, at("status"), "NOTE-BAD-STATUS",
                           f"'{status}' is not valid for type '{kind}' "
                           f"(expected: {', '.join(STATUSES[kind])})"))
    dates: dict[str, dt.date | None] = {}
    for key in ("created", "updated"):
        if meta.get(key) not in (None, ""):
            d = _as_date(meta[key])
            if d is None:
                v.append(Violation(note.path, at(key), "NOTE-BAD-DATE",
                                   f"'{key}' is not an ISO date (YYYY-MM-DD)"))
            dates[key] = d
    created, updated = dates.get("created"), dates.get("updated")
    if created and updated and updated < created:
        v.append(Violation(note.path, at("updated"), "NOTE-BAD-DATE", "'updated' is earlier than 'created'"))
    v.extend(_plugin_syntax(note))
    return v


def _plugin_syntax(note: Note) -> list[Violation]:
    v: list[Violation] = []
    for n, lang in fence_languages(note.body):
        if lang in PLUGIN_FENCES:
            v.append(Violation(note.path, note.body_line + n, "NOTE-PLUGIN-SYNTAX",
                               f"'{lang}' block needs an Obsidian plugin to be readable"))
    for n, line in enumerate(strip_code(note.body).split("\n")):
        if _CALLOUT.match(line):
            v.append(Violation(note.path, note.body_line + n, "NOTE-PLUGIN-SYNTAX",
                               "callout syntax renders only in Obsidian; use a plain blockquote"))
        if "<%" in line:
            v.append(Violation(note.path, note.body_line + n, "NOTE-PLUGIN-SYNTAX",
                               "templater syntax needs an Obsidian plugin"))
    return v


def check_basenames(notes: list[Note]) -> list[Violation]:
    by_name: dict[str, list[Note]] = {}
    for n in notes:
        by_name.setdefault(n.basename, []).append(n)
    v: list[Violation] = []
    for name, group in by_name.items():
        if len(group) > 1:
            for n in group:
                others = ", ".join(o.path for o in group if o is not n)
                v.append(Violation(n.path, 1, "NOTE-DUPLICATE-BASENAME",
                                   f"basename '{name}' is also used by {others}; links to it are ambiguous"))
    return v
