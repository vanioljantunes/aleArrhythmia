"""The command-line contract: invocation, output format, exit codes, and the hook warning."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

from tests.fixtures.build import build
from tests.helpers import make_repo

REPO = Path(__file__).resolve().parent.parent
LINE = re.compile(r"^[^:\n]+:\d+: [A-Z]+(?:-[A-Z]+)+: ")


def cli(*args: str, ci: bool = True) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.pop("CI", None)
    if ci:
        env["CI"] = "1"
    return subprocess.run([sys.executable, "-m", "tools.vaultcheck", *args],
                          cwd=REPO, env=env, capture_output=True, text=True, encoding="utf-8")


def test_clean_vault_exits_zero_and_states_what_it_verified(tmp_path: Path) -> None:
    root = make_repo(tmp_path, build("clean"))
    out = cli("--root", str(root))
    assert out.returncode == 0, out.stderr
    assert out.stderr == ""
    assert re.search(r"\d+ notes, \d+ decision records, \d+ links, \d+ citations verified: clean", out.stdout)


def test_violations_go_to_stderr_as_path_line_rule(tmp_path: Path) -> None:
    root = make_repo(tmp_path, build("cite-dangling"))
    out = cli("--root", str(root))
    assert out.returncode == 1
    lines = out.stderr.strip().splitlines()
    assert lines and all(LINE.match(line) for line in lines), out.stderr
    assert any(line.startswith("docs/vault/theory/theory-example.md:") and "CITE-DANGLING" in line for line in lines)


def test_quiet_suppresses_only_the_summary(tmp_path: Path) -> None:
    root = make_repo(tmp_path, build("cite-dangling"))
    out = cli("--root", str(root), "--quiet")
    assert out.returncode == 1 and out.stdout == "" and "CITE-DANGLING" in out.stderr


def test_not_a_repository_is_a_checker_error_not_a_clean_result(tmp_path: Path) -> None:
    out = cli("--root", str(tmp_path))
    assert out.returncode == 2, "a checker failure must never read as clean"
    assert "error" in out.stderr


def test_warns_when_the_local_hook_is_not_installed(tmp_path: Path) -> None:
    root = make_repo(tmp_path, build("clean"))
    out = cli("--root", str(root), ci=False)
    assert out.returncode == 0, "the hook warning must not fail the run"
    assert "HOOK-NOT-INSTALLED" in out.stderr
    subprocess.run(["git", "config", "core.hooksPath", ".githooks"], cwd=root, check=True)
    assert "HOOK-NOT-INSTALLED" not in cli("--root", str(root), ci=False).stderr


def test_version() -> None:
    out = cli("--version")
    assert out.returncode == 0 and out.stdout.startswith("vaultcheck ")
