"""Fetch the source mesh and the study fixtures into tests/fixtures/external/.

Nothing fetched here is ever committed (FR-013m). Each file is checked against the SHA-256 recorded
below; a mismatch stops the run. The ARGO archive is human study data and is fetched only when
asked for with --argo, and only once its hash has been recorded after the FR-013n inspection.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "external"

FILES = {
    "average.tar.gz": {
        "url": "https://zenodo.org/records/4593739/files/average.tar.gz?download=1",
        "sha256": "d787d6470c8a4a6c7bfb808c55e44e35a7bc18f5888847e2b24380beae2703ee",
        "source": "Rodero and others, 10.5281/zenodo.4593739, CC BY 4.0",
        "extract": "tar",
    },
    "carto.zip": {
        "url": "https://zenodo.org/records/6651600/files/carto.zip?download=1",
        "sha256": "4d6b52db2227de91ad0ef2d0d0fe9843c14f3e5e4a07bff7ba711ded6be5dab8",
        "source": "Williams, openep-testingdata, 10.5281/zenodo.6651600, CC BY 4.0, porcine",
        "extract": "zip",
    },
}

ARGO = {
    "url": "https://physionet.org/static/published-projects/argo/argo-1.0.0.zip",
    # Recorded 2026-09-26 by the FR-013n inspection; see the vault note. None would mean the
    # inspection has not been run and the archive must not be fetched by a test.
    "sha256": "2f25614704d62ebf30d80adec25f8b09e962ddf68fcd094c770704f0fa7f132e",
    "source": "ARGO, PhysioNet 10.13026/8gh2-e660, CC BY-NC-SA 4.0, anonymised human",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(name: str, url: str, expected: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    if dest.exists() and sha256(dest) == expected:
        print(f"{name}: present, hash ok")
        return dest
    print(f"{name}: downloading")
    urllib.request.urlretrieve(url, dest)
    got = sha256(dest)
    if got != expected:
        dest.unlink()
        sys.exit(f"{name}: hash mismatch, expected {expected}, got {got}. File removed.")
    print(f"{name}: {dest.stat().st_size:,} bytes, hash ok")
    return dest


def extract(dest: Path, kind: str) -> None:
    if kind == "tar":
        with tarfile.open(dest) as t:
            t.extractall(OUT, filter="data")
    elif kind == "zip":
        with zipfile.ZipFile(dest) as z:
            z.extractall(OUT / dest.stem)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--argo", action="store_true", help="also fetch the ARGO archive")
    args = ap.parse_args()

    for name, spec in FILES.items():
        dest = fetch(name, spec["url"], spec["sha256"])
        extract(dest, spec["extract"])
        print(f"  source: {spec['source']}")

    if args.argo:
        if ARGO["sha256"] is None:
            sys.exit("ARGO: no hash recorded. Run the FR-013n inspection first and record the "
                     "hash in this file. Fetching human study data without that step is refused.")
        dest = fetch("argo.zip", ARGO["url"], ARGO["sha256"])
        extract(dest, "zip")
        print(f"  source: {ARGO['source']}")


if __name__ == "__main__":
    main()
