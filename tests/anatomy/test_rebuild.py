"""Scenario 1: the committed geometry rebuilds byte for byte (FR-020, FR-020b)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "web" / "viewer" / "data"
ARCHIVE = ROOT / "tests" / "fixtures" / "external" / "average.tar.gz"


def test_verify_exits_zero():
    if not ARCHIVE.exists():
        pytest.skip("source mesh not fetched; run python tests/fixtures/fetch.py")
    r = subprocess.run([sys.executable, "-m", "tools.anatomy", "verify"], cwd=ROOT,
                       capture_output=True, text=True, timeout=900)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "identical" in r.stdout


def test_verify_reports_a_difference_with_counts(tmp_path, monkeypatch, capsys):
    # A rebuild that differs must exit 1 and print the per-structure table. The rebuild itself is
    # replaced by a stand-in so this does not cost a second real build.
    from tools.anatomy import __main__ as cli

    committed = json.loads((DATA / "heart.manifest.json").read_text(encoding="utf-8"))
    (tmp_path / "heart.glb").write_bytes((DATA / "heart.glb").read_bytes())
    (tmp_path / "heart.manifest.json").write_text(json.dumps(committed), encoding="utf-8")

    def stand_in(source, out, quiet=False):
        fresh = json.loads(json.dumps(committed))
        fresh["output"]["per_structure"]["12"]["triangles"] += 7
        fresh["output"]["sha256"] = "0" * 64
        fresh["pipeline"]["numpy"] = "0.0.0"
        (Path(out) / "heart.glb").write_bytes(b"not the same bytes")
        return fresh

    monkeypatch.setattr(cli, "build", stand_in)
    assert cli.verify(ARCHIVE, tmp_path) == 1
    out = capsys.readouterr().out
    assert "DIFFERENT" in out
    assert "numpy committed" in out and "0.0.0" in out
    assert "<-" in out
    flagged = [line for line in out.splitlines() if line.strip().startswith("12 ") and "<-" in line]
    assert flagged, out
