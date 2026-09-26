# Quickstart: The first 3D viewer

How to prove the feature works, end to end, on a clean machine.

## Prerequisites

| Need | Why |
|---|---|
| Python 3.11 or newer, numpy at the version in `requirements-anatomy.txt` | Preprocessing and tests |
| Playwright with Chromium | Browser tests. `npx playwright install chromium` |
| Network access, once | To fetch the source mesh and the two fixtures. Nothing else needs it |

## Setup

```bash
git clone https://github.com/vanioljantunes/aleArrhythmia.git
cd aleArrhythmia
git config core.hooksPath .githooks
pip install -e ".[dev]" -r requirements-anatomy.txt
python tests/fixtures/fetch.py
```

The last line downloads `average.tar.gz` (58 MB), the porcine CARTO export (10.5 MB) and ARGO
(183 MB) into `tests/fixtures/external/`, which git ignores. It prints each file's SHA-256 and refuses
to continue if one does not match the recorded value.

---

## Scenario 1, The geometry rebuilds byte for byte

Validates FR-019, FR-020, FR-020a, FR-020b, SC-006.

```bash
python -m tools.anatomy verify
echo "exit: $?"
```

**Expected**

```text
rebuilt heart.glb in 41.2 s
sha256 matches the committed file
exit: 0
```

To see what a mismatch looks like, change one cell size in `tools/anatomy/decimate.py` and run
again. The exit is 1 and the count table prints, so the difference is visible, not just the hash.

---

## Scenario 2, Every structure survives, and the budget holds

Validates FR-005, SC-003, SC-003a.

```bash
python -m pytest tests/anatomy/test_decimate.py -v
```

**Expected**: one test per structure asserting at least 150 triangles, one asserting the total is at
most 60,000, one asserting the file is under 2 MB after gzip.

---

## Scenario 3, Segments are placed where the anatomy says

Validates FR-025, FR-026.

```bash
python -m pytest tests/anatomy/test_segments.py -v
```

**Expected**: the boundary between segments 1 and 2 lies within 15 degrees of the anterior RV
insertion found from the data, and the boundary between 3 and 4 within 15 degrees of the other. If
this fails, `heart.manifest.json` records `segments.shipped: false` and the page shows the control
disabled with the reason. That outcome is also a pass for the feature; it is not a pass for
segments.

---

## Scenario 4, The heart is on screen and moves

Validates US1, SC-001, SC-002, SC-007.

```bash
python -m pytest tests/browser/test_viewer.py -v
```

**Expected**: model visible within 2 s under a 20 Mbps throttle; drag rotates; wheel zooms within
limits; reset restores; each of the 24 toggles hides its part; with segments on, only left
ventricular vertices are coloured and the legend lists 17 names.

---

## Scenario 5, The reader knows what it is

Validates US2, SC-004, SC-005, SC-010.

Open the page with scripting disabled. Confirm the research-use statement, the mean statement, the
no-result statement, the exploratory label and the provenance block are all readable, and that the
DOI link resolves to the Zenodo record.

---

## Scenario 6, A study loads and nothing leaves

Validates US5, FR-013j, FR-013k, SC-012, SC-013.

```bash
python -m pytest tests/browser/test_privacy.py tests/browser/test_modes.py -v
```

**Expected**: after picking the porcine export folder, the mode indicator reads "Patient", the
shell and its two points are drawn, the mean is detached, no network request left the origin, and
all three storage mechanisms are empty. After reload the page is back on the mean with no points.

---

## Scenario 7, The parsers read real exports

Validates FR-013q.

```bash
python -m pytest tests/readers -v
```

**Expected**: the CARTO reader produces 4 maps with 3,513, 3,513, 2,916 and 2,083 vertices and 0,
0, 2, 0 points. The ARGO reader produces 9 studies totalling 1,962 mapped points. `test_argo.py` is
skipped with a stated reason until the FR-013n inspection result is recorded in
`docs/vault/literature/argo-ventricular-tachycardia-dataset.md`.

---

## Scenario 8, Every gap is visible

Validates FR-023, FR-024, FR-013p, SC-008.

```bash
python -m pytest tests/browser/test_disabled.py -v
```

**Expected**: each disabled control names its reason and a date, and links to the vault note that
holds the evidence.

---

## Scenario 9, No study file is in the repository

Validates FR-013m, SC-016.

```bash
git ls-files tests/fixtures/external web/viewer/data | grep -v -E "heart\.glb|heart\.manifest\.json|LICENSE"
echo "exit: $?"
```

**Expected**: no output, exit 1 from grep, meaning nothing but the three committed files is tracked.

---

## Done when

- [ ] Scenarios 1 to 9 pass on a fresh clone
- [ ] `python -m tools.vaultcheck` is clean, with the three fixture notes and ADR-0009 present
- [ ] The manifest's counts and hash match the committed geometry
- [ ] The page carries every statement in `contracts/viewer-page.md`
