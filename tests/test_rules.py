"""One fixture per rule id: each must fire its rule, each control must pass (SC-004)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.fixtures.build import FIXTURES, STATE_RULES, build
from tests.helpers import make_repo, run_check
from tools.vaultcheck.report import ERROR, RULES


@pytest.mark.parametrize("name", sorted(FIXTURES))
def test_fixture_produces_its_rule(tmp_path: Path, name: str) -> None:
    expected_rule, expected_exit, _ = FIXTURES[name]
    violations, _ = run_check(make_repo(tmp_path, build(name)))
    report = "\n".join(v.format() for v in sorted(violations)) or "(none)"
    exit_code = 1 if any(v.severity == ERROR for v in violations) else 0

    if expected_rule is None:
        assert violations == [], f"control '{name}' must be clean, got:\n{report}"
    else:
        assert expected_rule in {v.rule for v in violations}, f"'{name}' did not raise {expected_rule}:\n{report}"
        fired = [v for v in violations if v.rule == expected_rule]
        assert all(v.path and v.line >= 1 for v in fired), "every violation names a file and a line (FR-021)"
    assert exit_code == expected_exit, f"'{name}' exit {exit_code}, expected {expected_exit}:\n{report}"


def test_every_registered_rule_has_a_fixture() -> None:
    covered = {rule for rule, _, _ in FIXTURES.values() if rule} | STATE_RULES
    missing = sorted(set(RULES) - covered)
    assert not missing, f"rules with no fixture (SC-004 requires one per rule): {missing}"


def test_committed_fixture_trees_match_the_generator() -> None:
    here = Path(__file__).parent / "fixtures"
    for name in FIXTURES:
        tree = here / name
        assert tree.is_dir(), f"fixture tree missing: run python tests/fixtures/build.py ({name})"
        on_disk = {
            p.relative_to(tree).as_posix(): p.read_text(encoding="utf-8").replace("\r\n", "\n")
            for p in tree.rglob("*") if p.is_file()
        }
        assert on_disk == build(name), f"tests/fixtures/{name} is stale: run python tests/fixtures/build.py"
