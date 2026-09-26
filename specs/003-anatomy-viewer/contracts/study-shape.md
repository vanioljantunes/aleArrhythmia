# Contract: The shape every reader produces

A reader turns files the user picked into one Study. The viewer knows only this shape. It does not
know which reader ran.

## Study

```json
{
  "source": "carto",
  "label": "1-Map",
  "frame": "study",
  "geometry": {
    "positions": "Float32Array, xyz triples, mm",
    "indices": "Uint32Array, triangles"
  },
  "points": [
    {"label": "P1", "position": [12.4, -30.1, 55.8], "origin": "mapped", "values": {"bipolar_mV": 0.5, "unipolar_mV": 2.1}},
    {"label": "A3", "position": [10.0, -28.0, 50.0], "origin": "ablation"}
  ]
}
```

| Rule | Reason |
|---|---|
| `frame` is always `study` | FR-013d. The page prints it. No reader may emit `canonical` |
| Positions are passed through untransformed | FR-013e. No registration, no unit change beyond what the source declares |
| A point carries no value of this project's making. It MAY carry the export's own measured values under FR-006a, shown only when asked | FR-013i, ADR-0010 |
| A reader opens only the files it names | FR-013j. Least exposure |
| A reader throws a `ReadError` naming what it expected and what it found | FR-013r. The viewer shows the message and stays in its previous mode |

## CARTO reader

| Reads | For |
|---|---|
| `<map>.mesh` | `[VerticesSection]` X Y Z, `[TrianglesSection]` vertex indices; rows with a negative group id are dropped |
| `<map>_car.txt` | One line per mapped point, starting with `P`: id in the third field, X Y Z in the fifth to seventh |
| `VisiTagExport/Sites.txt` | Ablation sites, columns X Y Z and SiteIndex, `origin: ablation`; absent in a study without ablation |
| `<map>_car.txt`, fields 11 and 12 | Unipolar and bipolar voltage per mapped point, in mV, read into `point.values` at the same time as the position (they are on the same line). Verified against the per-point XML: 1.902 and 0.024 for P1 |
| Nothing else | `<map>_Points_Export.xml`, per-point XML, ECG, electrode positions and contact force files are never opened |

Corrected 2026-09-25 on reading the porcine export: `<map>_Points_Export.xml` in this export
carries no positions, only the names of per-point files. The positions are in `<map>_car.txt`, and
the sensor position in the per-point files matches them exactly.

When a folder holds several maps, the reader lists them by name and the user picks one. A map with
zero points is valid and shows its shell alone.

## ARGO reader

| Reads | For |
|---|---|
| `XYZmesh.txt` | Vertex positions |
| `ConnectivityList.txt` | Triangles, 1-based in the source, converted |
| `POS_POINTS.txt` | Mapped points with their ids |
| `AblationPoints.txt` | Ablation points, `origin: ablation` |
| `MESHcoloring.txt`, on demand only | Header `Voltage,LAT`, one row per vertex, `NaN` where unmapped. Opened only when the value control is turned on (ADR-0010), by `readArgoValues`, never by `readArgo` |

## Fixtures

| Fixture | Source | Fetched by | Committed |
|---|---|---|---|
| Porcine CARTO export | Zenodo 10.5281/zenodo.6651600, CC BY 4.0 | `tests/fixtures/fetch.py` | Never |
| ARGO | PhysioNet 10.13026/8gh2-e660, CC BY-NC-SA 4.0 | Same, after the FR-013n inspection is recorded | Never |

A test asserts that no file under `tests/fixtures/external/` is tracked by git.
