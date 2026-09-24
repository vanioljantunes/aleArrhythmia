---
title: "Hybrid: continuous coordinates with segment labels"
type: literature
status: draft
created: 2026-09-24
updated: 2026-09-24
---


# Hybrid: continuous coordinates with segment labels

Store continuous coordinates, report segment names. Candidate for the canonical space in
[[canonical-reference-space]]. No publication defines this as a system; it is the combination of
two of the other candidates.

## What it is

| Item | Detail |
|---|---|
| Storage | A continuous system such as [[universal-ventricular-coordinates]], [[cobiveco-biventricular-coordinates]] or [[universal-atrial-coordinates]] |
| Reporting | Every coordinate also carries the [[aha-17-segment-model]] name of the segment it falls in |
| Ingestion | A study that reports only a segment name enters as a distribution over that segment, not as a point |

## Coverage

| Covered | Not covered |
|---|---|
| Whatever the chosen continuous system covers | Nothing extra. The labels add naming, not reach |

## Licence and availability

| Item | Detail |
|---|---|
| Inherited from the two parts | See each candidate note |

## Consequences for pooling

| Point | Effect |
|---|---|
| Kernels work | Statistics run in the continuous space, which is what ALE requires |
| Readable output | Clusters can be named in the language clinicians already use |
| Segment-only studies usable | They contribute as a spread over the segment, with their lower precision made explicit rather than hidden |
| Extra machinery | Two representations to keep consistent, and a documented rule for turning a segment into a distribution |

## Unknowns

| Unknown | What was tried |
|---|---|
| Whether treating a segment as a uniform distribution is defensible, or whether it biases clusters toward large segments | Not established. A statistical question for the method notes |

## References

- Bayer and others, Universal ventricular coordinates, Medical Image Analysis 2018: 10.1016/j.media.2018.01.005
- Cerqueira and others, Circulation 2002: 10.1161/hc0402.102975
