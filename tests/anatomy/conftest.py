from pathlib import Path

import pytest

# The vaultcheck environment has no numpy; these tests belong to the anatomy CI job.
pytest.importorskip("numpy")

EXTERNAL = Path(__file__).resolve().parents[1] / "fixtures" / "external"
ARCHIVE = EXTERNAL / "average.tar.gz"


@pytest.fixture(scope="session")
def mesh():
    if not ARCHIVE.exists():
        pytest.skip("source mesh not fetched; run python tests/fixtures/fetch.py")
    from tools.anatomy.vtk_reader import read_source
    return read_source(ARCHIVE)


@pytest.fixture(scope="session")
def surface(mesh):
    from tools.anatomy.surface import boundary
    return boundary(mesh.points, mesh.tets, mesh.cell_ids)
