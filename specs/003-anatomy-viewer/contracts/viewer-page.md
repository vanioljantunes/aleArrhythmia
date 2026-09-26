# Contract: What the viewer page promises

The page at `/projects/ale/viewer/` inside the section from feature 002.

## Always present, in the page's own HTML, readable without scripting

| Element | Text or content |
|---|---|
| Title | The viewer's name |
| Research-use statement | This is a research tool, not a medical device, and nothing here should guide a procedure |
| Exploratory label | No canonical reference space has been chosen. Every coordinate shown belongs to the frame of the geometry on screen |
| Provenance | Dataset title, authors, DOI as a link, licence, and the attribution line |
| Mean statement | The default heart is a population mean and is not any individual's anatomy |
| No-result statement | Nothing shown encodes a measurement or a statistical result |
| Local-only statement, beside the import control | Study files are read in this browser and never uploaded or stored |
| Still image | Shown when WebGL is unavailable, with a stated reason |

## Controls

| Control | State in stage A | State in stage B |
|---|---|---|
| Rotate, zoom, reset | Live | Live |
| Structure toggles, 24 | Live | Live |
| Segment overlay | Live if `manifest.output.segments.shipped`; else disabled with the recorded reason | Same |
| Manual coordinate entry | Live | Live |
| Load CARTO export | Disabled: "importer not yet verified against a real export, checked 2026-09-25", linking to the vault note | Live once both fixture tests pass |
| Load ARGO study | Disabled, same reason | Live |
| Affera | Disabled: "no public export format found, checked 2026-09-24", linking to the vault note | Disabled |
| Mode indicator | Reads "Population mean" | Reads "Population mean" or "Patient: <label>, this study's own frame" |
| Close study | Hidden | Shown in patient mode; returns to mean |

Every disabled control carries `aria-disabled`, its reason, its date and a link. ADR-0007.

## Behaviour the tests hold the page to

| Test | Asserts |
|---|---|
| `test_viewer.py` | Model visible within 2 s on a throttled 20 Mbps connection; drag changes camera; wheel changes distance within limits; reset restores; each toggle hides its primitive; segment overlay colours only LV vertices |
| `test_modes.py` | Loading a study attaches the patient document and detaches the mean; the inactive group has zero children; close returns to mean; reload returns to mean with no points |
| `test_privacy.py` | After loading a study: zero requests other than same-origin assets already loaded, none with a body; `localStorage`, `sessionStorage`, IndexedDB empty |
| `test_disabled.py` | Each disabled control's text contains its reason and a date; its link resolves |
| `test_rebuild.py` | `python -m tools.anatomy verify` exits 0 |
