"""Generate one fixture vault per rule id, plus the negative controls that must pass.

Each fixture is the executable statement of what one rule means: a clean base vault with exactly
one thing broken. tests/test_rules.py builds every fixture into a temporary Git repository and
asserts the expected rule fires; it also fails if any registered rule has no fixture (SC-004).

Regenerate the committed trees, so they can be read and run by hand with --root:

    python tests/fixtures/build.py
"""

from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path

Files = dict[str, str]

V = "docs/vault"

BASE: Files = {
    f"{V}/index.md": """---
title: Fixture vault
type: theory
status: active
created: 2026-01-01
updated: 2026-01-02
---

# Fixture vault

- [[ADR-0001-example]]
- [[question-example]]
- [[theory-example]]
- [[literature-example]]
- [[log-example]]
""",
    f"{V}/decisions/ADR-0001-example.md": """---
title: Example decision
type: adr
status: accepted
id: ADR-0001
created: 2026-01-01
updated: 2026-01-01
---

# ADR-0001: Example decision

Context for the decision.

## Options considered

- **Option A** — the first option.
- **Option B** — the second option.

## Trade-offs

**Option A**: costs little, buys little.

**Option B**: costs more, buys more.

## Chosen

**Option A**, because it is cheaper.

## Rejected

**Option B** — rejected because it costs more.

## References

- https://example.org/evidence
- [[log-example]]
- `docs/vault/logs/log-example.md:1`
""",
    f"{V}/questions/question-example.md": """---
title: Example question
type: question
status: open
created: 2026-01-01
updated: 2026-01-01
---

# Example question

## The question

Which option is right?

## Candidates

- [[literature-example]] — the only candidate.

## What would settle it

A comparison of costs.
""",
    f"{V}/theory/theory-example.md": """---
title: Example theory
type: theory
status: active
created: 2026-01-01
updated: 2026-01-01
---

# Example theory

## Setting

See [[literature-example#Coverage]] and decision ADR-0001.
""",
    f"{V}/literature/literature-example.md": """---
title: Example literature
type: literature
status: active
created: 2026-01-01
updated: 2026-01-01
---

# Example literature

## Coverage

Everything relevant.
""",
    f"{V}/logs/log-example.md": """---
title: Example log
type: log
status: active
created: 2026-01-01
updated: 2026-01-01
---

# Example log

A session happened.
""",
}

ADR = f"{V}/decisions/ADR-0001-example.md"
THEORY = f"{V}/theory/theory-example.md"
LIT = f"{V}/literature/literature-example.md"
QUESTION = f"{V}/questions/question-example.md"
INDEX = f"{V}/index.md"


def _edit(path: str, old: str, new: str) -> Callable[[Files], Files]:
    def apply(files: Files) -> Files:
        assert old in files[path], f"fixture edit anchor not found in {path}: {old!r}"
        files[path] = files[path].replace(old, new, 1)
        return files
    return apply


def _add(path: str, text: str, list_in_index: str | None = None) -> Callable[[Files], Files]:
    def apply(files: Files) -> Files:
        files[path] = text
        if list_in_index:
            files[INDEX] += f"- [[{list_in_index}]]\n"
        return files
    return apply


def _chain(*steps: Callable[[Files], Files]) -> Callable[[Files], Files]:
    def apply(files: Files) -> Files:
        for step in steps:
            files = step(files)
        return files
    return apply


def _same(files: Files) -> Files:
    return files


def _newer_adr(extra_header: str) -> str:
    return BASE[ADR].replace("id: ADR-0001", f"id: ADR-0002\n{extra_header}").replace(
        "# ADR-0001: Example decision", "# ADR-0002: Newer decision")


# name -> (expected rule or None for a control that must pass, expected exit code, mutation)
FIXTURES: dict[str, tuple[str | None, int, Callable[[Files], Files]]] = {
    # negative controls
    "clean": (None, 0, _same),
    "empty-vault": (None, 0, lambda files: {f"{V}/.gitkeep": ""}),
    "prose-mentions-adr": (None, 0, _chain(
        _add("notes.txt", "Near misses that must not count: ADR-1, adr-0001, ADR-00NN, ADR-12345.\n"),
        _add("specs/example.md", "An illustrative identifier: ADR-0042.\n"),
        _add(".vaultcheckignore", "specs/**   # example identifiers by design\n"),
    )),
    # note headers
    "note-missing-field": ("NOTE-MISSING-FIELD", 1, _edit(LIT, "title: Example literature\n", "")),
    "note-bad-type": ("NOTE-BAD-TYPE", 1, _edit(THEORY, "type: theory", "type: essay")),
    "note-bad-status": ("NOTE-BAD-STATUS", 1, _edit(THEORY, "status: active", "status: in-progress")),
    "note-bad-date": ("NOTE-BAD-DATE", 1, _edit(f"{V}/logs/log-example.md",
                                                  "updated: 2026-01-01", "updated: 2025-01-01")),
    "note-duplicate-basename": ("NOTE-DUPLICATE-BASENAME", 1,
                                _add(f"{V}/theory/literature-example.md", BASE[LIT])),
    "note-bad-frontmatter": ("NOTE-BAD-FRONTMATTER", 1, _edit(LIT, "---\ntitle", "title")),
    "note-plugin-syntax": ("NOTE-PLUGIN-SYNTAX", 1,
                           _edit(THEORY, "## Setting\n", "## Setting\n\n> [!note]\n> A callout.\n")),
    # decision records
    "adr-missing-section": ("ADR-MISSING-SECTION", 1,
                            _edit(ADR, "## Rejected\n\n**Option B** — rejected because it costs more.\n\n", "")),
    "adr-empty-section": ("ADR-EMPTY-SECTION", 1, _edit(
        ADR, "**Option A**: costs little, buys little.\n\n**Option B**: costs more, buys more.\n",
        "<!-- to be written -->\n")),
    "adr-too-few-options": ("ADR-TOO-FEW-OPTIONS", 1, _edit(ADR, "- **Option B** — the second option.\n", "")),
    "adr-no-reference": ("ADR-NO-REFERENCE", 1, _edit(
        ADR, "- https://example.org/evidence\n- [[log-example]]\n- `docs/vault/logs/log-example.md:1`\n",
        "<!-- emptied on purpose -->\n")),
    "adr-bad-reference": ("ADR-BAD-REFERENCE", 1, _edit(
        ADR, "- https://example.org/evidence\n", "- https://example.org/evidence\n- see the paper\n")),
    "adr-unresolved-reference": ("ADR-UNRESOLVED-REFERENCE", 1,
                                 _edit(ADR, "log-example.md:1`", "log-example.md:999`")),
    "adr-duplicate-id": ("ADR-DUPLICATE-ID", 1,
                         _add(f"{V}/decisions/ADR-0001-copy.md", BASE[ADR], "ADR-0001-copy")),
    "adr-id-filename-mismatch": ("ADR-ID-FILENAME-MISMATCH", 1, _edit(ADR, "id: ADR-0001", "id: ADR-0003")),
    "adr-superseded-no-target": ("ADR-SUPERSEDED-NO-TARGET", 1, _edit(ADR, "status: accepted", "status: superseded")),
    "adr-supersession-one-sided": ("ADR-SUPERSESSION-ONE-SIDED", 1, _add(
        f"{V}/decisions/ADR-0002-newer.md", _newer_adr("supersedes: [ADR-0001]"), "ADR-0002-newer")),
    "adr-supersession-dangling": ("ADR-SUPERSESSION-DANGLING", 1, _edit(
        ADR, "status: accepted", "status: superseded\nsuperseded_by: ADR-0009")),
    # citations and links
    "cite-dangling": ("CITE-DANGLING", 1, _edit(THEORY, "decision ADR-0001.", "decision ADR-0099.")),
    "link-unresolved": ("LINK-UNRESOLVED", 1,
                        _edit(THEORY, "## Setting\n", "## Setting\n\nAlso [[no-such-note]].\n")),
    "link-bad-anchor": ("LINK-BAD-ANCHOR", 1, _edit(THEORY, "#Coverage]]", "#No Such Heading]]")),
    # questions
    "q-no-candidates": ("Q-NO-CANDIDATES", 1,
                        _edit(QUESTION, "- [[literature-example]] — the only candidate.", "None identified yet.")),
    "q-no-criteria": ("Q-NO-CRITERIA", 1, _edit(QUESTION, "A comparison of costs.", "<!-- unknown -->")),
    "q-answered-no-target": ("Q-ANSWERED-NO-TARGET", 1, _edit(QUESTION, "status: open", "status: answered")),
    # index
    "index-incomplete": ("INDEX-INCOMPLETE", 1, _edit(INDEX, "- [[question-example]]\n", "")),
    # ignore file
    "ignore-no-reason": ("IGNORE-NO-REASON", 1, _add(".vaultcheckignore", "notes/**\n")),
    "ignore-stale": ("IGNORE-STALE", 0, _add(".vaultcheckignore", "nothing-here/**   # stale on purpose\n")),
}

# Rules that depend on repository state rather than vault content, tested separately.
STATE_RULES = {"HOOK-NOT-INSTALLED"}


def build(name: str) -> Files:
    _, _, mutate = FIXTURES[name]
    return mutate(dict(BASE))


def write(dest: Path, files: Files) -> None:
    for rel, text in files.items():
        path = dest / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    here = Path(__file__).parent
    for name in FIXTURES:
        dest = here / name
        if dest.exists():
            shutil.rmtree(dest)
        write(dest, build(name))
    print(f"wrote {len(FIXTURES)} fixtures under {here}")


if __name__ == "__main__":
    main()
