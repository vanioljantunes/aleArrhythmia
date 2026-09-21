"""Which files are in scope: tracked by Git, text not binary, not excluded by the ignore list.

Decision: ADR-0004 (citation scan scope).
"""

from __future__ import annotations

import fnmatch
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from .report import CheckerError, Violation

_SNIFF_BYTES = 8192
_IGNORE_LINE = re.compile(r"^(?P<glob>\S+)\s*(?:#\s*(?P<reason>.*))?$")


@dataclass
class IgnoreRule:
    glob: str
    line: int


@dataclass
class Discovery:
    files: list[str] = field(default_factory=list)
    violations: list[Violation] = field(default_factory=list)


def git_toplevel(start: Path) -> Path:
    try:
        out = subprocess.run(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise CheckerError(f"not inside a Git repository: {start}") from exc
    return Path(out.stdout.strip())


def tracked_files(root: Path) -> list[str]:
    """Repository-relative POSIX paths of every file Git tracks under root."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            capture_output=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise CheckerError(f"git ls-files failed in {root}") from exc
    return sorted(p for p in out.stdout.decode("utf-8").split("\0") if p)


def is_text(path: Path) -> bool:
    try:
        with path.open("rb") as fh:
            return b"\0" not in fh.read(_SNIFF_BYTES)
    except OSError:
        return False


def load_ignore(root: Path, ignore_file: Path) -> tuple[list[IgnoreRule], list[Violation]]:
    """Parse the ignore list. Every entry must carry a trailing '# reason' comment."""
    if not ignore_file.exists():
        return [], []
    rel = ignore_file.relative_to(root).as_posix() if ignore_file.is_relative_to(root) else str(ignore_file)
    rules: list[IgnoreRule] = []
    violations: list[Violation] = []
    for n, raw in enumerate(ignore_file.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = _IGNORE_LINE.match(line)
        if not m:
            violations.append(Violation(rel, n, "IGNORE-NO-REASON", f"malformed entry: {line!r}"))
            continue
        if not (m.group("reason") or "").strip():
            violations.append(Violation(
                rel, n, "IGNORE-NO-REASON",
                f"'{m.group('glob')}' has no reason; add a trailing '# why this is excluded'",
            ))
        rules.append(IgnoreRule(m.group("glob"), n))
    return rules, violations


def discover(root: Path, ignore_file: Path) -> Discovery:
    rules, violations = load_ignore(root, ignore_file)
    matched = {r.glob: False for r in rules}
    kept: list[str] = []
    for rel in tracked_files(root):
        hit = False
        for r in rules:
            if fnmatch.fnmatch(rel, r.glob):
                matched[r.glob] = hit = True
        if not hit and is_text(root / rel):
            kept.append(rel)
    ignore_rel = ignore_file.relative_to(root).as_posix() if ignore_file.is_relative_to(root) else str(ignore_file)
    for r in rules:
        if not matched[r.glob]:
            violations.append(Violation(ignore_rel, r.line, "IGNORE-STALE", f"'{r.glob}' matches no tracked file"))
    return Discovery(kept, violations)
