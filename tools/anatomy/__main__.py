"""python -m tools.anatomy build | verify

build   reads the source archive, extracts the surface, decimates to budget, derives segments,
        writes heart.glb, heart.manifest.json into --out.
verify  rebuilds into a temporary directory from the same source and compares heart.glb byte for
        byte with the committed one. Exit 0 identical, 1 different, with the per-structure counts of
        both builds printed so the difference is diagnosable (FR-020, FR-020b).
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

import numpy as np

from . import budget, manifest as mf, segments
from .gltf import write_glb
from .surface import boundary
from .vtk_reader import read_source

REPO = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = REPO / "tests" / "fixtures" / "external" / "average.tar.gz"
DEFAULT_OUT = REPO / "web" / "viewer" / "data"
GENERATOR = "tools.anatomy (aleArrhythmia)"


def build(source: Path, out: Path, quiet: bool = False) -> dict:
    log = (lambda *a: None) if quiet else (lambda *a: print(*a, file=sys.stderr))
    log(f"reading {source.name}")
    mesh = read_source(source)
    log(f"  {len(mesh.points):,} points, {len(mesh.tets):,} tetrahedra")
    tri, own = boundary(mesh.points, mesh.tets, mesh.cell_ids)
    log(f"surface: {len(tri):,} triangles")
    d, base, level = budget.fit(mesh.points, tri, own)
    log(f"decimated: {len(d.triangles):,} triangles, {len(d.positions):,} vertices, "
        f"base cell {base:.3f} mm, levels {level}")
    seg_in, report = segments.derive(mesh.points, mesh.scalars)
    seg_out = segments.propagate(seg_in, d.cluster_of_input, len(d.positions))
    log(f"segments: {report.check}: {report.reason}")
    prims = {int(s): d.triangles[d.owner == s] for s in np.unique(d.owner)}
    glb = write_glb(d.positions, d.normals, seg_out, prims, GENERATOR)
    man = mf.build(mf.sha256_file(source), d, report, glb)
    out.mkdir(parents=True, exist_ok=True)
    (out / "heart.glb").write_bytes(glb)
    (out / "heart.manifest.json").write_text(mf.dumps(man), encoding="utf-8")
    log(f"wrote {out / 'heart.glb'} ({len(glb):,} bytes) sha256 {man['output']['sha256']}")
    return man


def verify(source: Path, data: Path) -> int:
    committed = data / "heart.glb"
    if not committed.exists():
        print(f"no committed geometry at {committed}", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory() as tmp:
        fresh = build(source, Path(tmp), quiet=True)
        fresh_bytes = (Path(tmp) / "heart.glb").read_bytes()
    old_bytes = committed.read_bytes()
    if fresh_bytes == old_bytes:
        print(f"identical: {mf.sha256_of(old_bytes)}")
        return 0
    old = json.loads((data / "heart.manifest.json").read_text(encoding="utf-8"))
    print("DIFFERENT")
    print(f"  committed sha256 {old['output']['sha256']}  bytes {old['output']['bytes']}")
    print(f"  rebuilt   sha256 {fresh['output']['sha256']}  bytes {fresh['output']['bytes']}")
    print(f"  numpy committed {old['pipeline']['numpy']}  rebuilt {fresh['pipeline']['numpy']}")
    print(f"  python committed {old['pipeline']['python']}  rebuilt {fresh['pipeline']['python']}")
    print("  structure  tri(committed)  tri(rebuilt)  vert(committed)  vert(rebuilt)")
    a, b = old["output"]["per_structure"], fresh["output"]["per_structure"]
    for sid in sorted(set(a) | set(b), key=int):
        x, y = a.get(sid, {}), b.get(sid, {})
        flag = "" if x == y else "  <-"
        print(f"  {sid:>9}  {x.get('triangles', '-'):>14}  {y.get('triangles', '-'):>12}  "
              f"{x.get('vertices', '-'):>15}  {y.get('vertices', '-'):>13}{flag}")
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m tools.anatomy")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    b.add_argument("--out", type=Path, default=DEFAULT_OUT)
    v = sub.add_parser("verify")
    v.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    v.add_argument("--data", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args(argv)
    if args.cmd == "build":
        try:
            build(args.source, args.out)
        except budget.BudgetConflict as e:
            print(f"budget conflict: {e}", file=sys.stderr)
            return 1
        return 0
    return verify(args.source, args.data)


if __name__ == "__main__":
    sys.exit(main())
