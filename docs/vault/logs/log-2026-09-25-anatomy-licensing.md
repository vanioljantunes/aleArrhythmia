---
title: Finding an anatomy the project may ship
type: log
status: active
created: 2026-09-25
updated: 2026-09-25
---


# Anatomy licensing, 2026-09-25

The project wanted a 3D viewer. The reference anatomy was recorded as blocked, because the only
surveyed candidate states no licence. A focused search found several that do. Session run with an AI
coding assistant (Claude).

## Questions and answers

| # | Question | Options offered | Answer |
|---|---|---|---|
| 1 | What should the first 3D viewer do? | Anatomy plus real statistics on synthetic foci (recommended); anatomy only; a fake heatmap | Anatomy only, no statistics |
| 2 | Which anatomy should it render? | Rodero average four-chamber (recommended); generated ventricle first; both switchable | Rodero average four-chamber |

## Checked during the session

| Claim | Source | Result |
|---|---|---|
| An openly licensed four-chamber mesh exists | https://zenodo.org/records/4593739 | Confirmed by reading the record. Creative Commons Attribution 4.0 International |
| An openly licensed atrial shape model exists | https://zenodo.org/records/5095379 | Confirmed by reading the record. Creative Commons Attribution 4.0 International |
| An idealised ventricle can carry all 17 segments | Computed during the session | Confirmed. 3136 vertices, 6144 triangles, 37 KB, all 17 segments present |
| Commercial anatomy could be used | Zygote, Living Heart, the segmentation challenge data, the Virtual Population | Confirmed unusable. Each forbids redistribution or requires a click-through agreement |

Six further datasets were reported by the search pass and are recorded in
[[other-open-cardiac-meshes]] as not read directly, because their record pages were not opened.

## What changed

| Before | After |
|---|---|
| No anatomy the project may ship | Two, both Attribution-only, one four-chamber and one atrial |
| No open atrial atlas found at all | Found. See [[nagel-biatrial-shape-model]] |
| Reference anatomy recorded as a blocking unknown | Resolved |

## Correction

An earlier statement in this project held that shipping a reference anatomy was blocked on a
licence. That was true of the candidate then in hand and is no longer true in general. The blocking
entry has been answered in place rather than deleted, so the reasoning stays visible.

## Follow-ups

| Item | Where |
|---|---|
| Read the record pages of the six datasets not read directly, before adopting any of them | [[other-open-cardiac-meshes]] |
| Measure how far the surface can be decimated before anatomy distorts | Feature 003 |
| Decide how AHA-17 segments are placed on a real mesh | Feature 003 |
