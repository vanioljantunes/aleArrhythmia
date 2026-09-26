# Tasks: The first 3D viewer

**Input**: Design documents from `specs/003-anatomy-viewer/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included. The specification requires them: SC-012 and SC-013 are satisfied only by
inspection, FR-020 requires a byte-identical verify, FR-026 requires the insertion check to gate
segments, and FR-013q forbids claiming importer support without a real export passing.

**Organization**: Tasks are grouped by user story. Stage A of the plan is Phases 1 to 6. Stage B is
Phase 7.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1 to US5)
- Include exact file paths in descriptions

## Path Conventions

Preprocessing in `tools/anatomy/`, viewer in `web/viewer/`, vendored library in `web/vendor/`, tests
in `tests/anatomy/`, `tests/readers/`, `tests/browser/`, fixtures fetched into
`tests/fixtures/external/` which is ignored by git. Vault notes in `docs/vault/`.

---

## Phase 1: Setup

**Purpose**: Directories, pins, ignores, the vendored library, and a way to see the page locally.

- [X] T001 Create `tools/anatomy/__init__.py`, `web/viewer/readers/`, `web/viewer/data/`, `web/vendor/`, `tests/anatomy/`, `tests/readers/`, `tests/browser/`, `tests/fixtures/external/.gitkeep` per plan.md
- [X] T002 [P] Write `requirements-anatomy.txt` pinning numpy to the exact installed version, and add `tests/fixtures/external/` to `.gitignore` with a comment citing FR-013m
- [X] T003 [P] Write `tests/fixtures/fetch.py`: downloads `average.tar.gz` (Zenodo 4593739), `carto.zip` (Zenodo 6651600) and the ARGO archive (PhysioNet 10.13026/8gh2-e660) into `tests/fixtures/external/`, verifies each SHA-256 against constants recorded in the file, refuses on mismatch, prints sizes; ARGO download is behind a `--argo` flag so it is not fetched until T042 permits
- [X] T004 [P] Vendor three.js: download the ES module build at one pinned version into `web/vendor/three.module.min.js` plus `OrbitControls.js` and `GLTFLoader.js` from the same release into `web/vendor/`, copy the MIT licence to `web/vendor/LICENSE`, and record version and SHA-256 of each file in `web/vendor/MANIFEST.md`
- [X] T005 [P] Write `web/serve_dev.py`: a loopback static server on port 8788 over `web/` that rewrites `/projects/ale/viewer/*` to `web/viewer/index.html`, mirroring the production rewrite; loopback only, no writes
- [X] T006 [P] Write `tests/test_no_study_files.py`: fails if `git ls-files` lists anything under `tests/fixtures/external/` or anything under `web/viewer/data/` other than `heart.glb`, `heart.manifest.json`, `heart-still.png`, `LICENSE` (FR-013m, SC-016)

---

## Phase 2: Foundational

**Purpose**: The preprocessing pipeline that produces the one committed heart. Every story draws it.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T007 Write `tools/anatomy/vtk_reader.py`: streams the VTK 3.0 ASCII file, returns points (N,3) float64, tetrahedra (M,4) int32, cell ids (M,) int32, and point scalars RHO, PHI, Z, V as float64 arrays; passes the -10 sentinel through unchanged; numpy only
- [X] T008 [P] Write `tests/anatomy/test_vtk_reader.py`: against `tests/fixtures/external/average.vtk`, asserts 379158 points, 1766006 tetrahedra, 24 distinct ids, bounding box 129.4 x 108.1 x 124.9 mm within 0.1, and each scalar's range as recorded in `docs/vault/literature/rodero-mesh-contents.md`; skipped with a stated reason if the fixture is absent
- [X] T009 Write `tools/anatomy/surface.py`: boundary faces of a tetrahedral mesh by sorting the 4M candidate faces and keeping the unpaired ones, returning triangles (K,3) int32 with the owning cell id per triangle and outward-consistent winding
- [X] T010 [P] Write `tests/anatomy/test_surface.py`: asserts 334550 boundary triangles on the fixture, every id from 1 to 24 present on the surface, and closedness (every edge shared by exactly two boundary triangles)
- [X] T011 Write `tools/anatomy/decimate.py`: per-structure vertex clustering on a regular grid; takes a cell size per structure id; merges structures afterwards with shared vertices welded by position; recomputes area-weighted smooth normals; fully deterministic (sort before every reduction); returns positions, normals, per-structure index arrays
- [X] T012 Write `tools/anatomy/budget.py`: chooses cell sizes so every structure keeps at least 150 triangles and the total is at most 60000, by starting from a global size and refining the small structures; records the chosen sizes; raises `BudgetConflict` naming the structure if both constraints cannot hold (SC-003a)
- [X] T013 [P] Write `tests/anatomy/test_decimate.py`: asserts total triangles at most 60000, every structure at least 150 triangles, no primitive over 65535 vertices, determinism (two runs give identical arrays), and that `BudgetConflict` is raised on a synthetic mesh where it must
- [X] T014 Write `tools/anatomy/segments.py`: AHA-17 from Z, PHI, V per research R-004; finds the two RV insertion peaks from PHI at LV epicardial points within 1.5 mm of RV points; picks the anterior peak by projecting the RV centroid onto the LV short-axis plane; assigns basal 6, mid 6, apical 4, apex 1 for V == -1 only; returns a uint8 per-vertex array and a report dict with both peak angles, the chosen origin, and the resulting segment boundary angles
- [X] T015 [P] Write `tests/anatomy/test_segments.py`: the insertion check from research R-004: segment 1/2 boundary within 15 degrees of the anterior peak, segment 3/4 boundary within 15 degrees of the other; all 17 segments present; zero segment on every non-LV vertex; on failure the test asserts the report says `check: fail` rather than passing silently (FR-025, FR-026)
- [X] T016 Write `tools/anatomy/gltf.py`: writes a glTF 2.0 binary from positions, normals, per-structure indices and the segment array; one mesh, primitives named `structure-<id>`, attributes POSITION, NORMAL, `_SEGMENT`; uint16 indices; 4-byte aligned buffer views; deterministic byte output; no library
- [X] T017 [P] Write `tests/anatomy/test_gltf.py`: parses the written file's JSON chunk, asserts 24 primitives with the expected names, attribute accessor counts match the arrays, byte length matches the header, and the file passes a minimal validator function that checks alignment
- [X] T018 Write `tools/anatomy/manifest.py`: builds the record in `contracts/geometry-manifest.md`: source DOI and file hash, Python and numpy versions, cell sizes, per-structure counts, segment report, output hash and byte size, build date; writes `heart.manifest.json`
- [X] T019 Write `tools/anatomy/__main__.py`: `build --source <path> --out web/viewer/data/` runs reader, surface, budget, decimate, segments, gltf, manifest and prints the SHA-256; `verify` rebuilds into a temporary directory from the same source and compares bytes with the committed `heart.glb`, exit 0 identical, exit 1 with a per-structure count diff table
- [X] T020 Research the meaning of the 24 structure ids: read the Rodero 2021 paper and its supplementary text for the labelling table; write the result to `tools/anatomy/structures.json` as `{id: name}` only for ids the paper names, leaving the rest as `structure <id>`; record what was found and what was not in `docs/vault/literature/rodero-mesh-contents.md` under a new heading
- [X] T021 Run `python -m tools.anatomy build --source tests/fixtures/external/average.tar.gz --out web/viewer/data/` and commit `heart.glb`, `heart.manifest.json`; record triangle count, byte size, cell sizes, segment check result and the hash in a new vault note `docs/vault/literature/derived-heart-geometry.md` with frontmatter `title, type: literature, status: active, created, updated`, and add it to `docs/vault/index.md`
- [X] T022 [P] Write `web/viewer/data/LICENSE`: the CC-BY-4.0 text and the attribution line "Rodero C, Strocchi M, Marciniak M, Longobardi S, Whitaker J, O'Neill MD, Gillette K, Augustin C, Plank G, Vigmond EJ, Lamata P, Niederer SA. Virtual cohort of extreme and average four-chamber heart meshes from statistical shape model. Zenodo, 2021. 10.5281/zenodo.4593739"

**Checkpoint**: `heart.glb` exists, is under 2 MB gzipped, and `python -m tools.anatomy verify` exits 0.

---

## Phase 3: User Story 1, A visitor sees the heart (Priority: P1) MVP

**Goal**: The heart is on screen, rotates, zooms, resets, and every structure can be hidden.

**Independent Test**: Open the page on `web/serve_dev.py`, drag, scroll, reset, toggle. Scenario 4 of quickstart.md.

- [X] T023 [P] [US1] Write `web/viewer/index.html`: the section shell from feature 002's preview (site bar, `page-main wrap`), a `<canvas>` region, a controls column with a structure list container, a segment toggle, a reset button, a mode indicator reading "Population mean", and a `<noscript>` block; script tag type module pointing at `viewer.js`
- [X] T024 [P] [US1] Write `web/viewer/modes.js`: a `Document` class holding `group` (a three.js Group), `points` (array), `frame` (string) and `label`; a `Modes` controller with `mean` and `patient` slots and exactly one `active`; `activate(doc)` detaches and disposes the other group's children before attaching; no other point list anywhere (research R-006)
- [X] T025 [US1] Write `web/viewer/viewer.js`: scene, perspective camera, WebGL renderer sized to the canvas, ambient plus one directional light, OrbitControls with min and max distance set from the model's bounding sphere, a reset that restores the initial camera; loads `data/heart.glb` with GLTFLoader into the mean document; on load builds one checkbox per primitive from `structures.json` names (or `structure <id>`), wired to `mesh.visible`; shows a loading indicator until the model is visible (FR-029)
- [X] T026 [US1] Add the segment overlay in `web/viewer/viewer.js`: reads `_SEGMENT`, builds a per-vertex colour attribute from a fixed 17-entry palette with zero for unsegmented, toggled by the segment checkbox, off by default, with a legend of 17 AHA names; if `heart.manifest.json` reports `segments.shipped: false`, renders the toggle disabled with `segments.check` as the reason and the date (ADR-0007)
- [X] T027 [US1] Add manual coordinates in `web/viewer/viewer.js`: three numeric inputs, an add button, each point a small sphere of fixed colour in the active document's group, listed with its frame label and a remove control, a clear-all, and an "outside the geometry" flag when beyond the bounding box (FR-013f to FR-013i)
- [X] T028 [US1] Write `tests/browser/conftest.py`: starts `web/serve_dev.py` on a free port for the session, provides a Playwright page fixture with a 20 Mbps throttle option and a helper that waits for the mean document to have a loaded mesh
- [X] T029 [US1] Write `tests/browser/test_viewer.py`: model visible within 2 s under throttle (SC-001); drag changes the camera quaternion; wheel changes distance and stays within limits; reset restores the initial camera; each of the 24 toggles sets its primitive invisible; segment toggle colours only LV vertices and the legend has 17 entries; frame time while rotating recorded and asserted under 33 ms only when the test machine reports integrated graphics (SC-002)

**Checkpoint**: Scenario 4 passes. A visitor can look at the heart.

---

## Phase 4: User Story 2, The reader knows what they are looking at (Priority: P1)

**Goal**: Every statement the contract requires is on the page, readable without scripting.

**Independent Test**: Scenario 5 of quickstart.md, scripting disabled.

- [X] T030 [P] [US2] Add to `web/viewer/index.html` the static text blocks from `contracts/viewer-page.md`: research-use statement, exploratory label, mean statement, no-result statement, provenance block with dataset title, authors, DOI as a link, licence and attribution line; all in plain HTML outside any script
- [X] T031 [P] [US2] Render a still image `web/viewer/data/heart-still.png` from the built geometry (a Playwright screenshot of the loaded viewer at the reset camera, 1200 px wide) and add it inside `<noscript>` and in the WebGL-unavailable fallback with the stated reason (FR-027)
- [X] T032 [US2] Add WebGL detection in `web/viewer/viewer.js`: if no context, hide the canvas, show the still image and a one-line reason; if `heart.glb` fails to load or exceeds a 10 s wait, show a stated error and a link back to the section (FR-028)
- [X] T033 [US2] Add phone layout in `web/viewer/index.html` styles: controls stack below the canvas under 640 px, the canvas keeps a 4:3 box, touch rotates and pinches, and the page body never scrolls sideways (FR-008, SC-009)
- [X] T034 [US2] Write `tests/browser/test_page_text.py`: with JavaScript disabled, asserts every statement in the contract table is present, the DOI link resolves with HTTP 200, and the still image is displayed; with JavaScript enabled, asserts the same text is still visible

**Checkpoint**: A stranger can say what the heart is and where it came from.

---

## Phase 5: User Story 3, Anyone can reproduce the geometry (Priority: P2)

**Goal**: A reader rebuilds the committed file byte for byte from the published source.

**Independent Test**: Scenario 1 of quickstart.md on a fresh clone.

- [X] T035 [P] [US3] Write `tests/anatomy/test_rebuild.py`: runs `python -m tools.anatomy verify`, asserts exit 0; then patches one cell size in a copy and asserts exit 1 with a count table in stdout (FR-020, FR-020b)
- [X] T036 [P] [US3] Write `tests/anatomy/test_manifest.py`: the committed manifest's `output.sha256` equals the SHA-256 of `heart.glb`; `pipeline.numpy` equals the pin in `requirements-anatomy.txt`; every structure id 1 to 24 appears under `per_structure`; no string field contains a drive letter, a home directory or the word "Users" (FR-020a, FR-035)
- [X] T037 [US3] Write `tools/anatomy/README.md`: the route from DOI to committed file in numbered steps, the two commands, what the manifest fields mean, and what a mismatch means (FR-019, FR-024)
- [X] T038 [US3] Add `tests/anatomy` and `tests/browser` to `.github/workflows/traceability.yml` as a second job that runs `fetch.py` (without `--argo`), `verify`, and the pytest suites, caching `tests/fixtures/external/` by hash

**Checkpoint**: Scenario 1 passes on a fresh clone in CI.

---

## Phase 6: User Story 4, The page is honest about what it cannot do (Priority: P2)

**Goal**: Every committed but unavailable capability shows as a disabled control with reason, date and evidence link.

**Independent Test**: Scenario 8 of quickstart.md.

- [X] T039 [P] [US4] Add to `web/viewer/index.html` three disabled controls with `aria-disabled`, each with its reason, date and link: "Load CARTO export", reason "importer not yet verified against a real export, checked 2026-09-25", link `/projects/ale/openep-testingdata-carto-export`; "Load ARGO study", same reason and date, link `/projects/ale/argo-ventricular-tachycardia-dataset`; "Affera", reason "no public export format found, checked 2026-09-24", link `/projects/ale/affera-export`; plus the local-only statement beside them (FR-013l, FR-023, FR-024, FR-013p)
- [X] T040 [US4] Write `tests/browser/test_disabled.py`: each disabled control is present, not clickable, its text contains the reason and an ISO date, and its link returns HTTP 200 on the preview server (SC-008)

**Checkpoint**: Stage A complete. Phases 1 to 6 can ship to the section with the importer disabled.

---

## Phase 7: User Story 5, Someone looks at one study's own map (Priority: P2)

**Goal**: A study export is read in the browser, drawn in its own frame, and never leaves the machine. This is Stage B.

**Independent Test**: Scenarios 6 and 7 of quickstart.md.

- [X] T041 [US5] Write `docs/vault/decisions/ADR-0009-study-data-in-the-browser.md`: options considered (browser only; server-side; browser plus opt-in local save; no import at all), trade-offs, chosen (browser only, nothing persisted, modes never mixed), rejected, references to the constitution Principles II, V and VI, the clarification session in spec.md, and [[log-2026-09-25-eam-datasets]]; add to `docs/vault/index.md`; five sections, none empty
- [ ] T042 [US5] Run `python tests/fixtures/fetch.py --argo`, then inspect the ARGO files per FR-013n: search every text file for names, dates of birth, record numbers, institution names and file paths; read the WFDB headers for patient fields; record method and findings in `docs/vault/literature/argo-ventricular-tachycardia-dataset.md` under the De-identification heading; if anything identifying is found, stop, record it, and do not proceed with T044 or T047 (FR-013n, FR-013o)
- [X] T043 [P] [US5] Write `web/viewer/readers/carto.js`: given a `FileList` from a directory picker, finds `<map>.mesh` and `<map>_Points_Export.xml` pairs, lists map names, parses `[VerticesSection]` X Y Z and `[TrianglesSection]` indices from the chosen mesh, parses point id and position from `<map>_car.txt` and ablation sites from `VisiTagExport/Sites.txt` (corrected 2026-09-25: this export's `Points_Export.xml` carries no positions), returns the Study shape in `contracts/study-shape.md` with `frame: "study"`; opens no other file; throws `ReadError` naming what was expected on any failure
- [ ] T044 [P] [US5] Write `web/viewer/readers/argo.js`: given a `FileList`, reads `XYZmesh.txt`, `ConnectivityList.txt` (1-based, converted), `POS_POINTS.txt` (origin `mapped`) and `AblationPoints.txt` (origin `ablation`); never opens `MESHcoloring.txt`; returns the Study shape; throws `ReadError` on any failure
- [X] T045 [US5] Wire patient mode in `web/viewer/viewer.js` and `web/viewer/modes.js`: a directory picker per reader, a map chooser when a CARTO folder holds several, a `Study` becomes a patient `Document` with its own mesh and spheres for its points, `Modes.activate(patient)` on success, the mode indicator reads "Patient: <label>, this study's own frame", a close-study control returns to mean, a `ReadError` shows its message and leaves the mode unchanged (FR-013a to FR-013e, FR-013r)
- [X] T046 [US5] Write `tests/readers/test_carto.py`: through Playwright, feeds the porcine export directory to `carto.js` and asserts 4 maps named 1-Map, 1-1-ReMap, 2-Map, 3-Map with 3513, 3513, 2916, 2083 vertices and 0, 0, 2, 0 points; `frame` is `study`; positions match the first three vertices of each `.mesh` file read directly by the test, and the two mapped points match `2-Map_car.txt`; each map also carries the 22 VisiTag sites (FR-013q)
- [ ] T047 [US5] Write `tests/readers/test_argo.py`: skipped with a stated reason unless the FR-013n result in the vault note says the files were inspected and clear; then feeds each of the 9 patient directories to `argo.js` and asserts 1962 mapped points in total, ablation points carry origin `ablation`, and `MESHcoloring.txt` was never requested (FR-013q)
- [X] T048 [US5] Write `tests/browser/test_modes.py`: loading the porcine export attaches the patient document and the mean group has zero children; the indicator names the study and its frame; close returns to mean with the mean's manual points intact; reload returns to mean with no points; a folder with no `.mesh` shows the `ReadError` and the mode is unchanged (SC-014, SC-015)
- [X] T049 [US5] Write `tests/browser/test_privacy.py`: records every request from page load; loads the porcine export; asserts no request after load except same-origin GETs already seen, none with a body; asserts `localStorage.length == 0`, `sessionStorage.length == 0`, and `indexedDB.databases()` empty before and after; after reload the same (SC-012, SC-013)
- [ ] T050 [US5] Enable the CARTO and ARGO import controls in `web/viewer/index.html` only when T046, T047, T048 and T049 pass, removing `aria-disabled` and the reason; leave Affera disabled; update `tests/browser/test_disabled.py` to expect exactly one disabled import control (FR-013p)

**Checkpoint**: Stage B complete. Patient mode works on two real exports and nothing leaves the browser.

---

## Phase 8: Polish and cross-cutting

- [ ] T051 [P] Write `docs/vault/logs/log-2026-09-25-viewer-build.md`: what building the geometry found (chosen cell sizes, the segment check result, structure names found and not found, anything about the mesh not previously recorded), and add it to `docs/vault/index.md` (FR-036)
- [ ] T052 [P] Update `CONTRIBUTING.md`: how to fetch fixtures, that study files are never committed and why, how to run `verify`, and how the two modes are kept apart
- [ ] T053 Walk every scenario in `specs/003-anatomy-viewer/quickstart.md` on a fresh clone in an empty directory, fix the guide where it and reality disagree, record the walk in `docs/vault/logs/log-2026-09-25-viewer-build.md`
- [ ] T054 Link the viewer from the feature 002 section page listing and the home tile so it is reachable in two clicks; record that the public route still depends on feature 002's publication job in `specs/003-anatomy-viewer/plan.md` under Staging
- [ ] T055 Final run: `python -m tools.vaultcheck` clean, full `pytest` green, `python -m tools.anatomy verify` exit 0, commit citing ADR-0008 and ADR-0009, push, confirm CI green

---

## Dependencies and execution order

### Phase dependencies

| Phase | Depends on | Blocks |
|---|---|---|
| 1 Setup | Nothing | Everything |
| 2 Foundational | Phase 1 | Every story |
| 3 US1 | Phase 2 | US2 shares the page file; US5 shares `modes.js` |
| 4 US2 | Phase 3 for the page file | Nothing |
| 5 US3 | Phase 2 | Nothing |
| 6 US4 | Phase 3 for the page file | US5 flips its controls |
| 7 US5 | Phases 3 and 6, and T041, T042 inside it | Nothing |
| 8 Polish | All desired stories | Nothing |

### Within a story

- T041 (ADR-0009) and T042 (ARGO inspection) come before any patient-mode code in Phase 7.
- T047 stays skipped until T042 records a clear result. If T042 finds identifiers, T044, T047 and the ARGO half of T050 do not run and the finding is recorded instead.
- T050 flips controls only after T046 to T049 pass.

### Parallel opportunities

| Phase | Tasks that can run together |
|---|---|
| 1 | T002, T003, T004, T005, T006 |
| 2 | T008 with T007; T010 with T009; T013 with T011; T015 with T014; T017 with T016; T022 with anything |
| 3 | T023 and T024 before T025 |
| 4 | T030, T031 |
| 5 | T035, T036 |
| 7 | T043 and T044 after T042; T046 to T049 after T045 |
| 8 | T051, T052 |

---

## Parallel example: Phase 2

```text
Task: "Write tools/anatomy/surface.py"            (T009)
Task: "Write tests/anatomy/test_surface.py"       (T010, same time, different file)
Task: "Write tools/anatomy/segments.py"           (T014)
Task: "Write tests/anatomy/test_segments.py"      (T015, same time, different file)
Task: "Write web/viewer/data/LICENSE"             (T022, independent)
```

---

## Implementation strategy

### MVP first

1. Phases 1 and 2. The committed heart exists and verifies.
2. Phase 3. The heart is on screen. Stop and look at it.
3. Phase 4. The page says what it is.
4. Phase 6. The gaps are visible.

That is Stage A. It can ship with the importer disabled and is already the first public 3D artifact
of the project.

### Stage B

5. Phase 7, in order: ADR-0009, the ARGO inspection, the readers, patient mode, the four tests,
   then the control flip.
6. Phase 8.

### What stays honest whichever way tests fall

| If | Then |
|---|---|
| T015 fails the insertion check | Segments ship disabled with the recorded reason. The feature still passes |
| T012 raises `BudgetConflict` | Recorded in the vault, the budget or the structure list is revisited, nothing is dropped silently |
| T042 finds an identifier in ARGO | ARGO is not used. The porcine export alone proves the parser, and FR-013q keeps the ARGO control disabled |
| T049 finds a request | Patient mode does not ship until it is gone |

---

## Notes

- Every commit that closes a decision cites its record: ADR-0008 for anatomy, ADR-0009 for study data.
- Stage new vault notes before running the checker, or discovery will not see them.
- No em dashes, no curly quotes, in code comments or prose. The checker scans tracked text.
