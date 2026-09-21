"""The full check must stay fast enough to run on every push (SC-008: under 60 s at 1000 notes)."""

from __future__ import annotations

import time
from pathlib import Path

from tests.helpers import make_repo, run_check

HEADER = "---\ntitle: Note {i}\ntype: literature\nstatus: active\ncreated: 2026-01-01\nupdated: 2026-01-01\n---\n"


def test_thousand_notes_under_budget(tmp_path: Path) -> None:
    files = {
        f"docs/vault/literature/note-{i:04d}.md":
            HEADER.format(i=i) + f"\n# Note {i}\n\n## Coverage\n\nSee [[note-{(i + 1) % 1000:04d}#Coverage]].\n"
        for i in range(1000)
    }
    files["docs/vault/index.md"] = HEADER.format(i="index").replace("literature", "theory") + "\n# Index\n"
    root = make_repo(tmp_path, files)
    start = time.perf_counter()
    violations, counts = run_check(root)
    elapsed = time.perf_counter() - start
    assert violations == [], [v.format() for v in violations][:5]
    assert counts.notes == 1001 and counts.links == 1000
    assert elapsed < 60, f"{elapsed:.1f}s exceeds the 60-second budget"
