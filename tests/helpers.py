"""Shared helpers: build a fixture into a throwaway Git repository and run the checker on it."""

from __future__ import annotations

import subprocess
from pathlib import Path

from tests.fixtures.build import write
from tools.vaultcheck.__main__ import check


def make_repo(dest: Path, files: dict[str, str]) -> Path:
    write(dest, files)
    subprocess.run(["git", "init", "-q"], cwd=dest, check=True)
    subprocess.run(["git", "add", "-A"], cwd=dest, check=True)
    return dest


def run_check(root: Path):
    return check(root, root / "docs" / "vault", root / ".vaultcheckignore", check_hook=False)
