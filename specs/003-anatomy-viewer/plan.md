# Implementation Plan: The first 3D viewer

**Branch**: `main` | **Date**: 2026-09-25 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/003-anatomy-viewer/spec.md`, clarified in two sessions on
2026-09-25.

## Summary

A page in the project's web section draws a real heart. It opens on the population mean adopted in
ADR-0008, lets the reader rotate it, hide and show its 24 structures, see AHA-17 segments derived from
coordinates the mesh already carries, and place coordinates by hand. A second mode reads one study's
own export inside the browser and shows that study's shell with its own points, in its own frame,
transmitting and storing nothing. The two modes never mix. Nothing is computed.

Two pieces of work, one pipeline each:

| Piece | Turns | Into |
|---|---|---|
| Preprocessing, Python, numpy only | The 187 MB source mesh | A 60,000 triangle glTF binary with 24 named parts, segment labels, a manifest and a checksum |
| Viewer, one small 3D library, no framework | That file, or a study export the reader picks | A page inside the existing section |

## Technical Context

**Language/Version**: Python 3.11 or newer for preprocessing and tests, as feature 001 already
requires. Browser JavaScript, ES2020, no transpiler, for the viewer.

**Primary Dependencies**: numpy for preprocessing, pinned. One vendored 3D library for the browser,
pinned by file and hash (chosen in research). Playwright for browser tests, already present.
Nothing else. No mesh library, no bundler, no framework.

**Storage**: Files only. One derived geometry file and its manifest, committed. The source mesh and
both study fixtures are fetched on demand and never committed.

**Testing**: pytest for preprocessing, parsers and the checksum. Playwright for interaction, mode
exclusivity, and the network and storage inspections SC-012 and SC-013 require.

**Target Platform**: A static site with no build step, served by the same route feature 002 defines.
Current desktop and mobile browsers with WebGL.

**Project Type**: Static web page plus a command-line preprocessing tool.

**Performance Goals**: Model visible within 2 s at 20 Mbps. 30 frames per second rotating on
integrated graphics. At most 2 MB compressed, 60,000 triangles.

**Constraints**: Study files never leave the browser and never persist. Two mutually exclusive modes.
No registration between frames. No colour on the model encodes a result. Byte-identical rebuild from
the published source with pinned versions. Data licence recorded apart from code licence.

**Scale/Scope**: One mesh, 24 structures, 17 segments. One CARTO reader, one plain-text reader. Two
fixtures at test time. One page.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Test | Before design | After design |
|---|---|---|---|
| I. Open by default | Everything shipped carries an open licence | PASS. Geometry CC-BY-4.0 with attribution, code Apache-2.0, the 3D library under its own permissive licence, recorded per file | PASS. `web/viewer/data/LICENSE` and `web/vendor/LICENSE` record each |
| II. One canonical space | No coordinate presented as canonical; exploratory label present | PASS. FR-011, FR-013, FR-013e | PASS. Every coordinate is scoped to the displayed geometry's frame; the page carries the label |
| III. Statistical validity | Nothing statistical is shown | PASS. Out of scope entirely | PASS |
| IV. Provenance | The mesh traces to its source | PASS. Manifest names source, DOI, settings, hash | PASS. Manifest contract in `contracts/geometry-manifest.md` |
| V. Add-on, not replacement | Offline files only, no live connection, no branding | PASS. Reads exports the user already holds | PASS. Directory picker, nothing else |
| VI. Research tool | Research-use statement on every page | PASS. FR-012 | PASS. In the page shell shared with feature 002 |
| VII. Small, legible, installable | No heavy framework; preprocessing runs with what is installed | PASS. numpy only; one 3D library | PASS. See Complexity Tracking for the one library |
| VIII. Traceable by construction | Findings in the vault; decisions cited | PASS. Three vault notes already record the measurements | PASS. One new ADR required, see research |

Governance: this feature amends no principle. It requires one new decision record, ADR-0009, for
the patient-data architecture, because that decision is hard to reverse, would surprise a reader, and
was chosen over real alternatives. Written as a task before any patient-mode code lands.

## Project Structure

### Documentation (this feature)

```text
specs/003-anatomy-viewer/
  plan.md               this file
  research.md           Phase 0, every decision with its alternatives
  data-model.md         Phase 1, the entities and their invariants
  quickstart.md         Phase 1, how to prove it works
  contracts/
    geometry-manifest.md   what the derived geometry file and its manifest promise
    study-shape.md         what every reader must produce, regardless of source format
    viewer-page.md         what the page promises the reader and the tests
  tasks.md              Phase 2, written by /speckit-tasks
```

### Source Code (repository root)

```text
tools/
  anatomy/
    __init__.py
    __main__.py          python -m tools.anatomy build | verify
    vtk_reader.py        parses the source VTK ASCII into arrays
    surface.py           boundary faces of a tetrahedral mesh
    decimate.py          per-structure vertex clustering
    segments.py          UVC to AHA-17, with the insertion check
    gltf.py              writes a .glb with named primitives, no library
    manifest.py          counts, settings, hash
  vaultcheck/            unchanged

web/
  viewer/
    index.html           the page, inside the section shell from feature 002
    viewer.js            scene, controls, modes, structure toggles
    modes.js             the two documents and the switch
    readers/
      carto.js           .mesh and *_Points_Export.xml
      argo.js            XYZmesh.txt, ConnectivityList.txt, POS_POINTS.txt, AblationPoints.txt
    data/
      heart.glb          derived geometry, committed
      heart.manifest.json
      LICENSE            CC-BY-4.0 and the attribution the licence requires
  vendor/
    three.module.min.js  pinned, with LICENSE and a recorded hash

tests/
  anatomy/
    test_surface.py
    test_decimate.py
    test_segments.py
    test_gltf.py
    test_manifest.py
    test_rebuild.py      byte-identical check against the committed file
  readers/
    test_carto.py        against the porcine fixture, fetched at test time
    test_argo.py         against ARGO, fetched at test time, after the FR-013n inspection
  browser/
    test_viewer.py       Playwright: rotate, zoom, reset, toggles, segments
    test_modes.py        exclusivity, switch, reload
    test_privacy.py      SC-012 network, SC-013 storage
    test_disabled.py     ADR-0007 controls
  fixtures/
    fetch.py             downloads both study fixtures into an ignored directory
```

**Structure Decision**: The preprocessing tool sits beside `vaultcheck` under `tools/`, sharing its
Python conventions. The viewer sits under `web/`, which feature 002's publication job copies into the
site, so the viewer reaches the public page by the route already decided rather than a second one.
Fixtures download into `tests/fixtures/external/`, which is ignored by git and forbidden from ever
being committed by a test that fails if a study file is tracked.

## Phase 0 and Phase 1 outputs

| Artifact | Status |
|---|---|
| [research.md](research.md) | Written. Eleven decisions, each with alternatives and the reason |
| [data-model.md](data-model.md) | Written. Six entities, invariants, the mode state machine |
| [contracts/geometry-manifest.md](contracts/geometry-manifest.md) | Written |
| [contracts/study-shape.md](contracts/study-shape.md) | Written |
| [contracts/viewer-page.md](contracts/viewer-page.md) | Written |
| [quickstart.md](quickstart.md) | Written. Nine scenarios |

## Staging

The feature ships in two stages so the viewer is public before the importer is proven.

| Stage | Ships | Import controls |
|---|---|---|
| A | Population mean, toggles, segments if the insertion check passes, manual coordinates, page text, provenance | CARTO disabled: "importer not yet verified against a real export, checked 2026-09-25". Affera disabled: "no public export format, checked 2026-09-25" |
| B | CARTO reader, ARGO reader, patient mode, ADR-0009 | CARTO enabled once `test_carto.py` and `test_argo.py` pass. Affera stays disabled |

Stage A depends on feature 002's publication route to reach the public site. Until that route
exists, the viewer is proven on the local preview server the same way the section was.

Recorded 2026-09-25 at the end of implementation: both stages are built and tested locally, and the
public route still depends on feature 002's publication job, which has not been started. The link
from the section page and the home tile (T054) lands with that job; the local preview builder
already carries it.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| One vendored 3D library, about 650 KB | Drawing 60,000 lit, pickable triangles with orbit controls and glTF loading | Raw WebGL would be a few thousand lines of matrix, shader, buffer and picking code to write and maintain, for a rendering problem the library already solves. Principle VII asks for small and legible; a single pinned file is smaller and more legible than the same code written by hand |
