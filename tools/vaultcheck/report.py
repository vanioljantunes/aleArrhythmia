"""Violations, the rule registry, output formatting and exit codes.

Contract: specs/001-theory-vault-traceability/contracts/vaultcheck-cli.md
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field

ERROR = "error"
WARNING = "warning"

# Every rule the checker can emit. A rule missing from this table cannot be emitted, and
# tests/test_rules.py fails if any rule here lacks a fixture (SC-004).
RULES: dict[str, str] = {
    # note headers : contracts/note-frontmatter.md
    "NOTE-MISSING-FIELD": ERROR,
    "NOTE-BAD-TYPE": ERROR,
    "NOTE-BAD-STATUS": ERROR,
    "NOTE-BAD-DATE": ERROR,
    "NOTE-DUPLICATE-BASENAME": ERROR,
    "NOTE-BAD-FRONTMATTER": ERROR,
    "NOTE-PLUGIN-SYNTAX": ERROR,
    # decision records : contracts/decision-record.md
    "ADR-MISSING-SECTION": ERROR,
    "ADR-EMPTY-SECTION": ERROR,
    "ADR-TOO-FEW-OPTIONS": ERROR,
    "ADR-NO-REFERENCE": ERROR,
    "ADR-BAD-REFERENCE": ERROR,
    "ADR-UNRESOLVED-REFERENCE": ERROR,
    "ADR-DUPLICATE-ID": ERROR,
    "ADR-ID-FILENAME-MISMATCH": ERROR,
    "ADR-SUPERSEDED-NO-TARGET": ERROR,
    "ADR-SUPERSESSION-ONE-SIDED": ERROR,
    "ADR-SUPERSESSION-DANGLING": ERROR,
    # citations, links, questions, index
    "CITE-DANGLING": ERROR,
    "LINK-UNRESOLVED": ERROR,
    "LINK-BAD-ANCHOR": ERROR,
    "Q-NO-CANDIDATES": ERROR,
    "Q-NO-CRITERIA": ERROR,
    "Q-ANSWERED-NO-TARGET": ERROR,
    "INDEX-INCOMPLETE": ERROR,
    # ignore file : ADR-0004
    "IGNORE-NO-REASON": ERROR,
    "IGNORE-STALE": WARNING,
    # local enforcement: ADR-0003
    "HOOK-NOT-INSTALLED": WARNING,
    # writing style: ADR-0005
    "STYLE-EM-DASH": ERROR,
    "STYLE-CURLY-QUOTE": ERROR,
    "STYLE-AI-ARTIFACT": ERROR,
    "STYLE-AI-VOCABULARY": WARNING,
}

EXIT_CLEAN = 0
EXIT_VIOLATIONS = 1
EXIT_CHECKER_ERROR = 2


class CheckerError(Exception):
    """The checker itself could not run. Maps to exit code 2, never to a clean result."""


@dataclass(frozen=True, order=True)
class Violation:
    path: str
    line: int
    rule: str
    message: str = field(compare=False)

    def __post_init__(self) -> None:
        if self.rule not in RULES:
            raise ValueError(f"unregistered rule id: {self.rule}")

    @property
    def severity(self) -> str:
        return RULES[self.rule]

    def format(self) -> str:
        tag = "" if self.severity == ERROR else "warning: "
        return f"{self.path}:{self.line}: {self.rule}: {tag}{self.message}"


@dataclass
class Counts:
    notes: int = 0
    decisions: int = 0
    links: int = 0
    citations: int = 0


def exit_code(violations: list[Violation]) -> int:
    return EXIT_VIOLATIONS if any(v.severity == ERROR for v in violations) else EXIT_CLEAN


def emit(violations: list[Violation], counts: Counts, quiet: bool = False) -> int:
    """Print violations to stderr, the summary to stdout, and return the exit code."""
    ordered = sorted(set(violations))
    for v in ordered:
        print(v.format(), file=sys.stderr)
    errors = sum(1 for v in ordered if v.severity == ERROR)
    if not quiet:
        verdict = "clean" if errors == 0 else f"{errors} violation{'s' if errors != 1 else ''}"
        print(
            f"vaultcheck: {counts.notes} notes, {counts.decisions} decision records, "
            f"{counts.links} links, {counts.citations} citations verified: {verdict}"
        )
    return exit_code(ordered)
