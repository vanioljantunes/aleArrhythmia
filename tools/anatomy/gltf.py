"""Write a glTF 2.0 binary with one mesh and one primitive per structure. No library.

One vertex buffer is shared by every primitive; each primitive has its own index buffer. That keeps
structures welded at their boundaries and lets the viewer hide one without opening a seam.
"""
from __future__ import annotations

import json
import struct

import numpy as np

FLOAT, UBYTE, USHORT, UINT = 5126, 5121, 5123, 5125
ARRAY_BUFFER, ELEMENT_ARRAY_BUFFER = 34962, 34963


def _pad4(b: bytes, fill: bytes = b"\x00") -> bytes:
    return b + fill * ((4 - len(b) % 4) % 4)


def write_glb(positions: np.ndarray, normals: np.ndarray, segments: np.ndarray,
              primitives: dict[int, np.ndarray], generator: str) -> bytes:
    """primitives: structure id -> (T, 3) triangle indices into the shared vertex arrays."""
    pos = np.ascontiguousarray(positions, dtype=np.float32)
    nrm = np.ascontiguousarray(normals, dtype=np.float32)
    n_vert = len(pos)
    # A vertex attribute must be 4-byte aligned, so each uint8 segment is padded to 4 bytes.
    seg4 = np.zeros((n_vert, 4), dtype=np.uint8)
    seg4[:, 0] = segments.astype(np.uint8)
    index_type = USHORT if n_vert <= 65535 else UINT
    index_dtype = np.uint16 if index_type == USHORT else np.uint32

    blobs: list[bytes] = []
    views: list[dict] = []
    accessors: list[dict] = []
    offset = 0

    def add_view(data: bytes, target: int, stride: int | None = None) -> int:
        nonlocal offset
        v = {"buffer": 0, "byteOffset": offset, "byteLength": len(data), "target": target}
        if stride:
            v["byteStride"] = stride
        views.append(v)
        padded = _pad4(data)
        blobs.append(padded)
        offset += len(padded)
        return len(views) - 1

    vp = add_view(pos.tobytes(), ARRAY_BUFFER)
    accessors.append({"bufferView": vp, "componentType": FLOAT, "count": n_vert, "type": "VEC3",
                      "min": pos.min(axis=0).tolist(), "max": pos.max(axis=0).tolist()})
    vn = add_view(nrm.tobytes(), ARRAY_BUFFER)
    accessors.append({"bufferView": vn, "componentType": FLOAT, "count": n_vert, "type": "VEC3"})
    vs = add_view(seg4.tobytes(), ARRAY_BUFFER, stride=4)
    accessors.append({"bufferView": vs, "componentType": UBYTE, "count": n_vert, "type": "SCALAR"})

    prims = []
    for sid in sorted(primitives):
        tri = np.ascontiguousarray(primitives[sid], dtype=index_dtype)
        vi = add_view(tri.tobytes(), ELEMENT_ARRAY_BUFFER)
        accessors.append({"bufferView": vi, "componentType": index_type,
                          "count": int(tri.size), "type": "SCALAR"})
        prims.append({"name": f"structure-{sid}", "mode": 4,
                      "attributes": {"POSITION": 0, "NORMAL": 1, "_SEGMENT": 2},
                      "indices": len(accessors) - 1})

    doc = {
        "asset": {"version": "2.0", "generator": generator},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "heart"}],
        "meshes": [{"name": "heart", "primitives": prims}],
        "accessors": accessors,
        "bufferViews": views,
        "buffers": [{"byteLength": offset}],
    }
    json_bytes = _pad4(json.dumps(doc, separators=(",", ":"), sort_keys=True).encode("utf-8"), b" ")
    bin_bytes = b"".join(blobs)
    total = 12 + 8 + len(json_bytes) + 8 + len(bin_bytes)
    return (struct.pack("<4sII", b"glTF", 2, total)
            + struct.pack("<I4s", len(json_bytes), b"JSON") + json_bytes
            + struct.pack("<I4s", len(bin_bytes), b"BIN\x00") + bin_bytes)


def read_glb_json(data: bytes) -> dict:
    magic, version, total = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF" or version != 2 or total != len(data):
        raise ValueError("not a glTF 2.0 binary, or length mismatch")
    length, kind = struct.unpack_from("<I4s", data, 12)
    if kind != b"JSON":
        raise ValueError("first chunk is not JSON")
    return json.loads(data[20:20 + length].decode("utf-8"))
