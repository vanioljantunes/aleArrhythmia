"""AHA 17 segments from the universal ventricular coordinates already on the mesh.

The coordinates give apicobasal position (Z), rotation about the long axis (PHI) and which ventricle
(V). PHI zero is not the AHA origin, so the origin is found from the data:

  1. The right ventricular wall (V = 1) meets the left ventricle (V = -1, which owns the septum)
     only along the two insertions. Left ventricular epicardial points within a small distance of
     any right ventricular point therefore form two bands in PHI. Each band's circular mean is an
     insertion.
  2. The septum is the shorter arc between the two insertions.
  3. AHA numbering runs counter-clockwise when the heart is viewed from the apex, and moving that
     way from the anterior insertion enters the septum. Whether PHI increases clockwise or
     counter-clockwise in that view is measured from the point positions, which decides which
     insertion is anterior.

The anterior insertion is the boundary between segments 1 and 2. The other insertion should sit at
the 3/4 boundary, 120 degrees on, and the report records how far it actually is. If the gap exceeds
the tolerance the check fails and the segments are not shipped (FR-025, FR-026).
"""
from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np

LV, RV = -1.0, 1.0
UNDEFINED = -10.0
CONTACT_MM = 1.5
EPI_RHO = 0.9
APEX_Z = 0.08
TOLERANCE_DEG = 15.0


@dataclass
class SegmentReport:
    contact_points: int
    band_sizes: list[int]
    insertion_anterior_deg: float
    insertion_inferior_deg: float
    septal_arc_deg: float
    phi_increases_ccw_from_apex: bool
    origin_deg: float
    boundary_1_2_deg: float
    boundary_3_4_deg: float
    boundary_3_4_offset_deg: float
    tolerance_deg: float
    check: str
    reason: str

    def as_dict(self) -> dict:
        return asdict(self)


def _wrap(deg):
    return (np.asarray(deg) + 180.0) % 360.0 - 180.0


def _pack(k: np.ndarray) -> np.ndarray:
    return (k[:, 0] + 2**20) * 2**42 + (k[:, 1] + 2**20) * 2**21 + (k[:, 2] + 2**20)


def _contact_mask(points: np.ndarray, rho: np.ndarray, v: np.ndarray) -> np.ndarray:
    """LV epicardial points within about CONTACT_MM of any RV point, by grid lookup."""
    lv_epi = (v == LV) & (rho > EPI_RHO)
    rv_keys = np.unique(np.floor(points[v == RV] / CONTACT_MM).astype(np.int64), axis=0)
    rv_packed = np.sort(_pack(rv_keys))
    idx = np.flatnonzero(lv_epi)
    keys = np.floor(points[idx] / CONTACT_MM).astype(np.int64)
    near = np.zeros(len(idx), dtype=bool)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                q = _pack(keys + np.array([dx, dy, dz]))
                pos = np.searchsorted(rv_packed, q)
                pos[pos == len(rv_packed)] = 0
                near |= rv_packed[pos] == q
    mask = np.zeros(len(points), dtype=bool)
    mask[idx[near]] = True
    return mask


def _circular_mean(deg: np.ndarray) -> float:
    rad = np.radians(deg)
    return float(np.degrees(np.arctan2(np.sin(rad).mean(), np.cos(rad).mean())))


def _two_bands(phi_deg: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Split angles on the circle into two clusters at the two largest gaps."""
    order = np.sort(phi_deg)
    gaps = np.diff(np.concatenate([order, [order[0] + 360.0]]))
    cut = np.sort(np.argsort(gaps)[-2:])
    first = order[cut[0] + 1:cut[1] + 1]
    second = np.concatenate([order[cut[1] + 1:], order[:cut[0] + 1]])
    return first, second


def _phi_sense(points: np.ndarray, phi: np.ndarray, z: np.ndarray, v: np.ndarray) -> bool:
    """True if PHI increases counter-clockwise when the heart is viewed from the apex."""
    lv = (v == LV) & (z != UNDEFINED)
    p, zz, ph = points[lv], z[lv], phi[lv]
    q = p - p.mean(axis=0)
    # Long axis, apex to base: the direction in which Z grows, by least squares.
    coef, *_ = np.linalg.lstsq(np.column_stack([q, np.ones(len(q))]), zz, rcond=None)
    u = coef[:3] / np.linalg.norm(coef[:3])
    # An observer at the apex looks along +u. Counter-clockwise in that view is a positive rotation
    # about -u, so the frame's third axis is -u.
    e1 = np.cross(u, [1.0, 0.0, 0.0])
    if np.linalg.norm(e1) < 1e-6:
        e1 = np.cross(u, [0.0, 1.0, 0.0])
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(-u, e1)
    az = np.arctan2(q @ e2, q @ e1)
    same = np.abs(np.mean(np.exp(1j * (ph - az))))
    opposite = np.abs(np.mean(np.exp(1j * (ph + az))))
    return bool(same > opposite)


def derive(points: np.ndarray, scalars: dict[str, np.ndarray]) -> tuple[np.ndarray, SegmentReport]:
    rho, phi, z, v = scalars["RHO"], scalars["PHI"], scalars["Z"], scalars["V"]
    phi_deg = np.degrees(phi)

    contact = _contact_mask(points, rho, v)
    band_a, band_b = _two_bands(phi_deg[contact])
    a, b = _circular_mean(band_a), _circular_mean(band_b)

    # The septum is the shorter arc. Orient it so it runs from sept_start to sept_end in +PHI.
    if (b - a) % 360.0 <= 180.0:
        sept_start, sept_end = a, b
    else:
        sept_start, sept_end = b, a
    arc = (sept_end - sept_start) % 360.0

    ccw = _phi_sense(points, phi, z, v)
    s = 1.0 if ccw else -1.0
    # Counter-clockwise from the anterior insertion enters the septum. If PHI runs counter-clockwise
    # that is +PHI from sept_start; otherwise it is -PHI from sept_end.
    anterior = sept_start if ccw else sept_end
    inferior = sept_end if ccw else sept_start
    origin = anterior

    seg = np.zeros(len(points), dtype=np.uint8)
    lv = (v == LV) & (z != UNDEFINED)
    # Counter-clockwise angle from the 1/2 boundary. The sectors run 2, 3, 4, 5, 6, 1. The apical
    # septal segment 14 is centred on the septum (theta 60), so the apical sectors start 15 degrees
    # in and run 14, 15, 16, 13.
    theta = (s * (phi_deg[lv] - origin)) % 360.0
    basal = np.array([2, 3, 4, 5, 6, 1])[(theta / 60.0).astype(int) % 6]
    apical = np.array([14, 15, 16, 13])[(((theta - 15.0) % 360.0) / 90.0).astype(int) % 4]
    zz = z[lv]
    out = np.where(zz >= 2 / 3, basal, np.where(zz >= 1 / 3, basal + 6, apical))
    out = np.where(zz < APEX_Z, 17, out)
    seg[lv] = out

    b34 = float(_wrap(origin + s * 120.0))
    off34 = float(abs(_wrap(inferior - b34)))
    ok = off34 <= TOLERANCE_DEG
    report = SegmentReport(
        contact_points=int(contact.sum()),
        band_sizes=[int(len(band_a)), int(len(band_b))],
        insertion_anterior_deg=round(float(anterior), 2),
        insertion_inferior_deg=round(float(inferior), 2),
        septal_arc_deg=round(float(arc), 2),
        phi_increases_ccw_from_apex=ccw,
        origin_deg=round(float(origin), 2),
        boundary_1_2_deg=round(float(origin), 2),
        boundary_3_4_deg=round(b34, 2),
        boundary_3_4_offset_deg=round(off34, 2),
        tolerance_deg=TOLERANCE_DEG,
        check="pass" if ok else "fail",
        reason=(f"the inferior insertion sits {off34:.1f} degrees from the 3/4 boundary, within the "
                f"{TOLERANCE_DEG:.0f} degree tolerance") if ok else
               (f"the inferior insertion sits {off34:.1f} degrees from the 3/4 boundary, beyond the "
                f"{TOLERANCE_DEG:.0f} degree tolerance; this anatomy's septal arc is {arc:.1f} degrees "
                f"where the AHA model assumes 120"),
    )
    return seg, report


def propagate(seg_in: np.ndarray, cluster_of_input: np.ndarray, n_out: int) -> np.ndarray:
    """Output vertex segment = the most common segment among the input points in its cluster."""
    counts = np.zeros((n_out, 18), dtype=np.int64)
    ok = cluster_of_input >= 0
    np.add.at(counts, (cluster_of_input[ok], seg_in[ok]), 1)
    return counts.argmax(axis=1).astype(np.uint8)
