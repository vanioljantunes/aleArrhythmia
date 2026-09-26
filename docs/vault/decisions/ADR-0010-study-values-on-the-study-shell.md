---
title: A study's own values may colour the study's own shell
type: adr
status: proposed
id: ADR-0010
created: 2026-09-26
updated: 2026-09-26
---

# ADR-0010: A study's own values may colour the study's own shell

The author asked, on 2026-09-26, for the viewer to look like the mapping system it is an add-on
to, shown by a CARTO 3 screenshot of a left atrial voltage map. Most of that look is presentation.
One part is not: the shell coloured by voltage. FR-006 forbids any colour that encodes a
measurement, and the readers were written never to open the voltage file. This records whether
that rule should bend for a study's own values in patient mode, and how far.

## Options considered

| Option | What the viewer shows |
|---|---|
| A. Study values on the study shell only | In patient mode, an opt-in control colours that study's shell by a value the export itself carries (bipolar voltage, local activation time), with the export's own scale, labelled as that study's own data. Never on the mean. Never pooled, thresholded or compared |
| B. Keep FR-006 as written | The look is copied, the shell stays one colour. The voltage file stays unopened |
| C. Any value on any geometry | Values may also be shown on the mean, or combined across studies |

## Trade-offs

| Option | Cost | Gain |
|---|---|---|
| A | The no-result statement needs a second clause. A reader who does not read it may take a voltage map for an output of this project. The reader must open one more file per study | The page shows what an electrophysiologist expects to see when they open their own map, which is the whole point of an add-on. The value is the study's own, unchanged, in the study's own frame |
| B | The viewer looks like the software but draws a grey shell where the clinician expects a map; the add-on reads as a toy | No rule changes. Nothing on screen can be mistaken for a result |
| C | Values on the mean would need registration, which Principle II forbids until a space is chosen. Pooling values is the statistical core, which does not exist yet | None the project can take now |

## Chosen

Proposed: A, under these rules. Not yet accepted; the author decides.

| Rule | Reason |
|---|---|
| Only in patient mode, only on that study's shell | FR-013c. A value from one frame is never drawn in another |
| Only values the export carries, passed through unchanged, with the export's own units and range | FR-013e and Principle IV. The viewer computes nothing |
| Off by default; the control names the file and the field it reads | Least surprise, and the reader knows one more file is opened |
| The colour bar states the value, its unit, its source file and the study label | So the map cannot be read as this project's output |
| Never on the population mean, never across studies | Principle II and Principle III. The mean has no values; pooling is the statistical core |
| The no-result statement gains one clause: in patient mode, colour may show a value that the study's own export carries, and that value is the study's, not this project's | FR-006 and SC-007 are amended by FR-006a, not silently broken |

## Rejected

| Option | Why it lost |
|---|---|
| B | Copying the frame of the software while refusing its content is the worst of both: it looks like a map and is not one |
| C | Both halves are forbidden by principles the project has not yet earned the right to relax |

## References

- Constitution, Principles II, III, IV and V: `.specify/memory/constitution.md`
- Specification, FR-006, FR-006a, FR-013c, FR-013e, SC-007: `specs/003-anatomy-viewer/spec.md`
- Where study data may go: [[ADR-0009-study-data-in-the-browser]]
- The voltage file this would read: [[argo-ventricular-tachycardia-dataset]], `MESHcoloring.txt`; for CARTO, `<map>_car.txt` carries a bipolar and unipolar voltage per point, not per vertex
- Session log: [[log-2026-09-25-viewer-build]]
