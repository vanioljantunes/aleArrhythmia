# Research: The first 3D viewer

Every decision below names the alternatives and why they lost. Measurements are cited from the vault
rather than repeated.

## R-001: Surface extraction

**Decision**: A boundary face is a triangle that belongs to exactly one tetrahedron. Sort all
7,064,024 candidate faces, keep the unpaired ones. numpy only.

**Rationale**: Already done once, by hand, on 2026-09-25, in under a minute. 334,550 boundary
triangles, closed. See [rodero-mesh-contents](../../docs/vault/literature/rodero-mesh-contents.md).

**Alternatives considered**: VTK or pyvista surface filters. Not installed, and installing a
compiled mesh library to do one sort is the wrong trade under Principle VII.

## R-002: Decimation strategy

**Decision**: Vertex clustering on a regular grid, run per structure with its own cell size, then
merged. Cell sizes chosen so every structure keeps at least 150 triangles and the total lands under
60,000. Fully deterministic, numpy only.

**Rationale**: Byte-identical rebuild (FR-020) needs a deterministic algorithm with no floating-point
order dependence beyond numpy's own, and no compiled library whose version drift changes output.
Vertex clustering is order-independent by construction. Running it per structure is what protects the
small ones: a global grid coarse enough for the ventricles would erase a 1,000-triangle vein inlet.
SC-003a stays as the guard: if a structure cannot keep 150 triangles inside the total budget, the
conflict is recorded, not hidden.

**Alternatives considered**:

| Option | Why it lost |
|---|---|
| Quadric edge collapse via a library (pymeshlab, open3d, fast-simplification) | Better shape fidelity per triangle, but a compiled dependency whose output changes across versions, which makes byte-identical rebuild fragile in exactly the way FR-020b anticipates |
| Quadric edge collapse in pure Python | Deterministic and dependency-free, but roughly a thousand lines and slow on 334,550 triangles. Reserved as the fallback if clustering looks visibly faceted at 60,000 |
| No decimation, ship 334,550 triangles | About 8 MB and above the 30 fps target on integrated graphics |

## R-003: Output format

**Decision**: glTF 2.0 binary, one `.glb`, one mesh, 24 primitives named by structure id, float32
positions and normals, uint16 indices per primitive, a per-vertex segment attribute. Written by a
small function of our own, no library.

**Rationale**: glTF is the format every browser 3D library loads natively, so the viewer needs no
custom loader. Named primitives are what makes structure toggling a lookup rather than a lookup
table. Writing it by hand is about 150 lines: a JSON chunk and a binary chunk with byte alignment.
That keeps the pipeline numpy-only and the output deterministic.

**Alternatives considered**:

| Option | Why it lost |
|---|---|
| Draco-compressed glTF | Smaller, but needs a decoder in the browser and an encoder in the pipeline, both compiled. Uncompressed is already under budget: roughly 1.1 to 1.5 MB before the server's own compression |
| Custom JSON or binary | Needs a custom loader and documents nothing anyone else can read |
| OBJ or PLY | Text, larger, and no standard place for named parts or per-vertex attributes |

## R-004: AHA-17 from universal ventricular coordinates

**Decision**: Derive segments from `Z`, `PHI` and `V` for left ventricular points only. Ship them
only if the insertion check passes. Otherwise the segment control is disabled under ADR-0007 and the
finding is recorded.

**What was measured on 2026-09-25**:

| Fact | Value |
|---|---|
| Left ventricle | `V = -1`, 171,367 points, the larger set |
| Points with coordinates defined | 250,416 of 379,158 |
| Where the LV touches the RV, in `PHI` | Two peaks, near -45 degrees and +90 degrees, 135 degrees apart |
| `PHI = 0` | Mid-septal, between the two insertions, not at either |

**Derivation**:

| Step | Rule |
|---|---|
| 1 | Identify the anterior insertion: of the two `PHI` peaks, the one on the side toward the RV centroid projected onto the LV short axis |
| 2 | Set the AHA angular origin at that insertion, so segment 1 (basal anterior) begins there going away from the septum, and segments 2 and 3 cover the septum |
| 3 | Apicobasal thirds from `Z`: basal above 2/3, mid between 1/3 and 2/3, apical below 1/3; apex cap, segment 17, where `Z` is below a small threshold and `RHO` is near the endocardium |
| 4 | Six 60-degree sectors basal and mid, four 90-degree sectors apical |
| 5 | Right ventricular and atrial vertices carry no segment |

**Insertion check, the gate FR-026 needs**: after derivation, the boundary between segments 1 and 2
must coincide with the anterior insertion peak, and the boundary between 3 and 4 with the other,
each within 15 degrees. The test computes both from the same data and fails otherwise. If it fails,
FR-025's disabled branch applies and the mismatch is recorded in the vault as a finding about this
mesh's `PHI` convention.

**Alternatives considered**:

| Option | Why it lost |
|---|---|
| Assume `PHI = 0` is the AHA origin | Measured false. It is mid-septal. Shipping that would rotate every segment by about 45 degrees, which FR-026 forbids |
| Landmark detection on the raw surface | Unnecessary. The coordinates exist. This was the reason FR-025 was conditional, and the reason no longer applies |
| Skip segments | Loses the one clinical vocabulary every reader already has, for no gain now that derivation is cheap |

## R-005: Browser 3D library

**Decision**: three.js, the ES module build, vendored as a single pinned file with its licence and
a recorded hash. Only `Scene`, `PerspectiveCamera`, `WebGLRenderer`, `OrbitControls`, `GLTFLoader`
and `Raycaster` are used.

**Rationale**: Principle VII forbids a heavy framework, not a library. three.js is one file, no
build step, loads glTF natively, and is what Mango-style research viewers on the web already use.
Vendoring rather than loading from a CDN keeps FR-031's spirit for the page's own code and makes the
page reproducible: the exact bytes ship with the site.

**Alternatives considered**:

| Option | Why it lost |
|---|---|
| Raw WebGL | Thousands of lines to reach parity, all of it ours to maintain. Less legible than one pinned file |
| Babylon.js | Larger, and a full engine where a renderer is enough |
| Load three.js from a CDN as feature 002 does with marked and d3 | Works, but the viewer is the thing people will judge the project by; it should not depend on a third party being up. Recorded as a deliberate divergence from 002's choice |

## R-006: Two-mode architecture and enforcement

**Decision**: One scene. Two document objects, `mean` and `patient`, each owning its own geometry
and its own point list. Exactly one is `active`. The renderer draws only the active document's group.
Switching detaches the outgoing document. A patient document is disposed on the way out, so nothing
of the study remains; the mean document keeps its objects detached, so typed coordinates survive a
study visit, which the tests require. There is no shared
point list anywhere in the code.

**Rationale**: FR-013c is enforced structurally, not by discipline. A point cannot be drawn on the
wrong geometry because a point is a field of the document that owns the geometry, and only one
document is ever attached to the scene. `test_modes.py` asserts the inactive document's group has
zero children after every switch.

**Alternatives considered**:

| Option | Why it lost |
|---|---|
| One geometry slot, one global points array, a mode flag | The bug FR-013c forbids becomes one forgotten `if` away |
| Two separate pages | Doubles the shell and controls, and the switch becomes a navigation with reload, which loses the manual points the user typed into the mean view |

## R-007: How a study file reaches the page

**Decision**: A directory picker. The user selects the export folder. The page reads only the files
each reader names, `.mesh` and `*_Points_Export.xml` for CARTO, the four text files for ARGO, and
never opens anything else in the folder. Reading uses the browser's File API; nothing is sent.

**Rationale**: A CARTO export is a folder of a hundred files. Asking the user to zip it adds a step
and a zip library. Reading only the named files means electrograms, ECGs and settings are never even
loaded into memory, which is the least exposure possible for FR-013j.

**Alternatives considered**:

| Option | Why it lost |
|---|---|
| Zip upload parsed in the browser | Needs a zip library, and the user has to make the zip |
| Drag and drop of individual files | Works for ARGO's four files; painful for CARTO's mesh plus XML pairing |

## R-008: Reproducibility and the manifest

**Decision**: `python -m tools.anatomy build` writes `heart.glb`, `heart.manifest.json` and prints
the SHA-256. `python -m tools.anatomy verify` rebuilds into a temporary path and compares bytes to
the committed file. The manifest records source DOI, source file hash, numpy version, Python version,
every decimation cell size, triangle and vertex counts per structure, segment counts, and the output
hash. A pinned `requirements-anatomy.txt` names numpy exactly.

**Rationale**: FR-020 wants byte-identical. FR-020b wants the counts beside the hash so a future
mismatch is diagnosable. `verify` is the reader's one-line check; `test_rebuild.py` runs it in CI.

**Alternatives considered**: Geometric tolerance was offered and rejected by the author in
clarification. Recorded there.

## R-009: Segment rendering without implying a result

**Decision**: Segments are an overlay the reader switches on, drawn as per-vertex colour from a
fixed 17-entry palette with a legend naming each segment. Off by default. The page states that the
colours name regions and encode no measurement.

**Rationale**: FR-006 permits colour that distinguishes anatomy and forbids colour that encodes a
result. A segment is anatomy. Defaulting it off and labelling it keeps the first thing a reader sees
uncoloured, which is the honest default.

## R-010: Manual coordinates

**Decision**: Three numeric inputs and a button. A point is drawn as a small sphere at the given
position in the frame of the active document, with a label stating that frame. A point outside the
geometry's bounding box is drawn anyway and flagged "outside the geometry". Points are listed and
individually removable, with a clear-all.

**Rationale**: FR-013f to FR-013i verbatim. Spheres carry no colour scale, so nothing is encoded.

## R-011: Testing the privacy requirements

**Decision**: Playwright, already available. `test_privacy.py` loads a fixture through the directory
picker, then asserts: no request was made after page load other than to the page's own origin for
its own assets, and none carried a body; `localStorage`, `sessionStorage` and IndexedDB are empty
before and after; after `page.reload()` the viewer is in mean mode with no points. `test_disabled.py`
reads each disabled control's text for the reason and the date.

**Rationale**: SC-012 and SC-013 say "confirmed by inspecting"; a test that inspects is the only
honest way to claim them.

## What research did not settle

| Open | Handled by |
|---|---|
| Which `PHI` peak is anterior | A computation in `segments.py` from the RV centroid, checked by the insertion test. If ambiguous, segments are disabled and it is recorded |
| Whether 150 triangles per structure and 60,000 total can both hold | `test_decimate.py` asserts both; SC-003a governs a failure |
| What the 24 structure ids mean | Names come from the Rodero paper's labelling if it can be found; otherwise the viewer shows "structure 7" honestly rather than guessing "left atrial appendage". Recorded either way |
| ARGO's files have not been inspected | `fetch.py` downloads it; an inspection task runs FR-013n and records the result before `test_argo.py` may run |
