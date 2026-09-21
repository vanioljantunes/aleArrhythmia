"""Command-line entry point: python -m tools.vaultcheck, or vaultcheck once installed.

Contract: specs/001-theory-vault-traceability/contracts/vaultcheck-cli.md
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from . import __version__
from .decisions import check_decisions
from .discovery import discover, git_toplevel
from .frontmatter import check_basenames, check_note, parse
from .links import check_citations, check_index, check_links, check_questions
from .style import check_style
from .report import EXIT_CHECKER_ERROR, CheckerError, Counts, Violation, emit

HOOKS_DIR = ".githooks"


def hook_warning(root: Path) -> list[Violation]:
    """Warn when the tracked pre-push hook is not active in this clone (ADR-0003).

    Git will not run hooks from a fresh clone until its owner opts in, so this is the only
    place an uninstalled hook can be made visible locally. Skipped in CI, where no hook runs.
    """
    if os.environ.get("CI"):
        return []
    try:
        out = subprocess.run(["git", "-C", str(root), "config", "--get", "core.hooksPath"],
                             capture_output=True, text=True)
    except OSError:
        return []
    if out.stdout.strip() == HOOKS_DIR:
        return []
    return [Violation(f"{HOOKS_DIR}/pre-push", 1, "HOOK-NOT-INSTALLED",
                      f"the local pre-push check is not active; run: git config core.hooksPath {HOOKS_DIR}")]


def check(root: Path, vault: Path, ignore_file: Path, check_hook: bool = True) -> tuple[list[Violation], Counts]:
    found = discover(root, ignore_file)
    violations = list(found.violations)
    try:
        vault_rel = vault.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise CheckerError(f"vault {vault} is not inside the repository {root}") from exc
    vault_rel = "" if vault_rel == "." else vault_rel

    def in_vault(rel: str) -> bool:
        return rel.endswith(".md") and (not vault_rel or rel.startswith(vault_rel + "/"))

    notes = []
    for rel in (f for f in found.files if in_vault(f)):
        note, problems = parse(root, rel)
        notes.append(note)
        violations += problems
        violations += check_note(note)
    violations += check_basenames(notes)

    decision_violations, ids = check_decisions(root, notes)
    violations += decision_violations
    link_violations, link_count = check_links(notes, found.files)
    violations += link_violations
    cite_violations, cite_count = check_citations(root, found.files, ids)
    violations += cite_violations
    violations += check_questions(notes, ids)
    violations += check_index(vault_rel, notes)
    violations += check_style(root, found.files)
    if check_hook:
        violations += hook_warning(root)

    decisions = sum(1 for n in notes if n.type == "adr")
    return violations, Counts(len(notes), decisions, link_count, cite_count)


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(prog="vaultcheck", description="Refuse untraceable work in the theory vault.")
    parser.add_argument("--root", type=Path, help="repository to check (default: the enclosing Git repository)")
    parser.add_argument("--vault", type=Path, help="vault directory (default: docs/vault under the root)")
    parser.add_argument("--ignore-file", type=Path, help="exclusion list (default: .vaultcheckignore under the root)")
    parser.add_argument("--quiet", action="store_true", help="suppress the summary line")
    parser.add_argument("--version", action="version", version=f"vaultcheck {__version__}")
    args = parser.parse_args(argv)

    try:
        root = args.root.resolve() if args.root else git_toplevel(Path.cwd())
        vault = (root / args.vault) if args.vault and not args.vault.is_absolute() else (args.vault or root / "docs" / "vault")
        ignore = (root / args.ignore_file) if args.ignore_file and not args.ignore_file.is_absolute() else (args.ignore_file or root / ".vaultcheckignore")
        violations, counts = check(root, vault, ignore)
    except CheckerError as exc:
        print(f"vaultcheck: error: {exc}", file=sys.stderr)
        return EXIT_CHECKER_ERROR
    return emit(violations, counts, quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())
