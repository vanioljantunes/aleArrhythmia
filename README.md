# aleArrhythmia

Activation Likelihood Estimation (ALE), the coordinate-based meta-analysis method developed for
functional MRI, adapted to cardiac electrophysiology.

The aim is to let individual ablation studies report arrhythmia origins as coordinates in a shared
cardiac reference space, and then pool those coordinates across studies into a statistically
thresholded map of where a given arrhythmia tends to arise. The intended payoff is shorter mapping
time, higher first-pass ablation efficacy, and fewer lesions delivered off target.

This is an add-on layer, not a mapping system. It is designed to be fed by, and to feed back into,
the exported data of existing electroanatomic mapping platforms. It does not compete with them.

> **Research use only.** This software is for research and educational use. It is **not a medical
> device**, is not validated for diagnosis or treatment, and must not be used to guide clinical
> decisions for an individual patient. It does not ingest, store or transmit identifiable patient
> data, and it sends no telemetry.

## Status

Phase 0 — groundwork. No statistics are implemented yet, and the project makes no claim about
cardiac results. Current work: the theory vault, the decision-record machinery, and a survey of
candidate cardiac reference spaces.

## Where things are

| Path | What it is |
|---|---|
| `docs/vault/` | The theory, as plain Markdown notes. Start at `docs/vault/index.md` |
| `docs/vault/decisions/` | Every non-trivial decision, as a numbered record with options, trade-offs and references |
| `tools/vaultcheck/` | The checker that refuses untraceable work |
| `specs/` | Specifications, plans and task lists for each feature |
| `.specify/memory/constitution.md` | The principles every change is checked against |

You do not need Obsidian to read the vault. Every note is ordinary Markdown with a short header.

## Running the checker

```bash
# works on a fresh clone, before installing anything
python -m tools.vaultcheck

# install the tool and the local pre-push enforcement
pip install -e ".[dev]"
git config core.hooksPath .githooks
```

## Licence

Two licences, one per kind of work. Every file in the repository is covered by exactly one of them.

| Path | Licence | File |
|---|---|---|
| `docs/vault/` — the theory, decision records, notes and logs | Creative Commons Attribution 4.0 International (CC-BY-4.0) | [`LICENSE-docs`](LICENSE-docs) |
| Everything else — code, tests, tooling, specifications, configuration | Apache License 2.0 | [`LICENSE`](LICENSE) |

In short: reuse the code freely, including commercially, under Apache-2.0's terms and patent grant;
quote and adapt the theory freely, with attribution.

Why two licences, and why these two: ADR-0002, at
[`docs/vault/decisions/ADR-0002-licensing.md`](docs/vault/decisions/ADR-0002-licensing.md).
