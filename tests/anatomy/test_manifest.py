"""The committed manifest is true to the file beside it (FR-020a, FR-020b, FR-035)."""
from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "web" / "viewer" / "data"


def manifest() -> dict:
    return json.loads((DATA / "heart.manifest.json").read_text(encoding="utf-8"))


def strings(x):
    if isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)
    elif isinstance(x, str):
        yield x


def test_hash_and_size_match_the_file():
    m = manifest()
    data = (DATA / "heart.glb").read_bytes()
    assert m["output"]["sha256"] == hashlib.sha256(data).hexdigest()
    assert m["output"]["bytes"] == len(data)


def test_numpy_pin_matches_requirements():
    pin = re.search(r"numpy==([\d.]+)", (ROOT / "requirements-anatomy.txt").read_text(encoding="utf-8"))
    assert pin, "requirements-anatomy.txt must pin numpy exactly"
    assert manifest()["pipeline"]["numpy"] == pin.group(1)


def test_every_structure_is_counted():
    m = manifest()
    per = m["output"]["per_structure"]
    assert set(per) == {str(i) for i in range(1, 25)}
    assert sum(v["triangles"] for v in per.values()) == m["output"]["triangles"]
    assert set(m["pipeline"]["cell_size_mm"]) == set(per)


def test_no_personal_paths():
    for s in strings(manifest()):
        assert not re.search(r"[A-Za-z]:\\|/home/|\bUsers\b", s), s


def test_view_vectors_are_unit_and_perpendicular():
    v = manifest()["output"]["view"]
    up, ant = v["up"], v["anterior"]
    assert abs(math.hypot(*up) - 1) < 1e-3
    assert abs(math.hypot(*ant) - 1) < 1e-3
    assert abs(sum(a * b for a, b in zip(up, ant))) < 1e-3


def test_segments_block_is_consistent():
    seg = manifest()["output"]["segments"]
    assert seg["shipped"] == (seg["check"] == "pass")
    assert seg["reason"]
    assert seg["report"]["check"] == seg["check"]


def test_structure_names_copy_matches_the_source():
    a = (ROOT / "tools" / "anatomy" / "structures.json").read_bytes()
    b = (ROOT / "web" / "viewer" / "structures.json").read_bytes()
    assert a == b
