import numpy as np

from tools.anatomy.gltf import read_glb_json, write_glb


def _sample():
    pos = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [2, 0, 0]], dtype=np.float32)
    nrm = np.tile([0, 0, 1], (5, 1)).astype(np.float32)
    seg = np.array([1, 2, 3, 0, 17], dtype=np.uint8)
    prims = {3: np.array([[0, 1, 2]]), 1: np.array([[1, 3, 2], [1, 4, 3]])}
    return pos, nrm, seg, prims


def test_structure_and_alignment():
    pos, nrm, seg, prims = _sample()
    data = write_glb(pos, nrm, seg, prims, "test")
    doc = read_glb_json(data)
    names = [p["name"] for p in doc["meshes"][0]["primitives"]]
    assert names == ["structure-1", "structure-3"]
    assert all(v["byteOffset"] % 4 == 0 for v in doc["bufferViews"])
    assert doc["bufferViews"][2]["byteStride"] == 4
    assert doc["accessors"][0]["count"] == 5 and doc["accessors"][0]["type"] == "VEC3"
    assert doc["accessors"][0]["max"] == [2.0, 1.0, 0.0]
    idx = [doc["accessors"][p["indices"]]["count"] for p in doc["meshes"][0]["primitives"]]
    assert idx == [6, 3]
    assert len(data) % 4 == 0


def test_deterministic_bytes():
    a = write_glb(*_sample(), "test")
    b = write_glb(*_sample(), "test")
    assert a == b
