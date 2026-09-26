"""No study file, and nothing but the three committed geometry files, may be tracked (FR-013m)."""
import subprocess

ALLOWED_DATA = {
    "web/viewer/data/heart.glb",
    "web/viewer/data/heart.manifest.json",
    "web/viewer/data/heart-still.png",
    "web/viewer/data/LICENSE",
}


def tracked(prefix: str) -> list[str]:
    out = subprocess.run(["git", "ls-files", prefix], capture_output=True, text=True, check=True)
    return [line for line in out.stdout.splitlines() if line]


def test_nothing_under_external_is_tracked():
    files = [f for f in tracked("tests/fixtures/external") if not f.endswith(".gitkeep")]
    assert files == [], f"study or source files are tracked: {files}"


def test_only_the_derived_geometry_is_tracked_under_data():
    extra = set(tracked("web/viewer/data")) - ALLOWED_DATA
    assert not extra, f"unexpected files tracked under web/viewer/data: {sorted(extra)}"
