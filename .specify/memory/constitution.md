<!--
Sync Impact Report
==================
Version change: 1.1.0 -> 1.1.1
Bump rationale: PATCH. Resolves two deferred TODOs without changing any principle: the licence
(Apache-2.0 for code, CC-BY-4.0 for vault prose) and the repository layout (own standalone public
repository, not nested in a larger repository). Both are recorded as resolved rather than
deleted so the deferral and its resolution stay readable.
(1.1.1: resolves TODO(LICENSE) and records the standalone-repository rule, 2026-09-20.
1.1.0: Principle VIII and the theory vault, 2026-09-20.
1.0.0: initial ratification, seven principles, 2026-09-20.)

Modified principles: none

Modified sections:
  - Deferred TODOs (TODO(LICENSE) and repository layout resolved)

Added sections: none

Removed sections: none

Templates and dependent files:
  ✅ .specify/memory/constitution.md        (amended)
  ✅ .specify/templates/plan-template.md    (reviewed; generic "Constitution Check" gate, no edit needed)
  ✅ .specify/templates/spec-template.md    (reviewed; no edit needed)
  ✅ .specify/templates/tasks-template.md   (reviewed; no edit needed)
  ⚠ README.md                               (pending; repo not yet created)
  ⚠ CLAUDE.md                               (pending; repo not yet created)
  ⚠ vanioantunes.com                        (pending; 4th homepage section not yet built)

Deferred TODOs:
  - TODO(REFERENCE_SPACE): the canonical cardiac reference space is deliberately undecided.
    Candidates under evaluation: Universal Ventricular/Atrial Coordinates (UVC/UAC) on an open
    statistical heart atlas; AHA 17-segment and atrial-segment models; fixed-atlas vertex space;
    a hybrid. Principle II binds the project to choosing exactly one canonical, versioned space
    and recording the choice in an ADR before any statistical result is published. Until then all
    space-dependent work is exploratory and MUST be labelled as such.
  - TODO(VENDOR_INTEROP): which export formats of EnSite X EP (Abbott), Rhythmia HDx (Boston
    Scientific) and KODEX-EPD (Philips) can actually be read, and under what licence terms,
    is unresearched. Principle V holds regardless of the answer.
  - RESOLVED 2026-09-20 (was TODO(LICENSE)): Apache-2.0 for the software, CC-BY-4.0 for the vault
    prose. Apache-2.0 for its explicit patent grant, which matters in a field where device vendors
    hold patents; CC-BY-4.0 so the theory can be quoted and reused with attribution. Both licences
    and their scopes ship at the repository root. To be recorded as an ADR on first push.
  - RESOLVED 2026-09-20: the project lives in its own standalone public repository, not nested
    inside a larger repository. Standing rule for every project under that monorepo. To be
    recorded as ADR-0001.
-->

# aleArrhythmia Constitution

aleArrhythmia brings Activation Likelihood Estimation (ALE) — the coordinate-based meta-analysis
method developed for functional MRI (Turkeltaub 2002; Eickhoff et al. 2009, 2012) — to cardiac
electrophysiology. The goal is to make it possible for individual ablation studies to report
arrhythmia origins as coordinates in a shared cardiac space, and then to pool those coordinates
across studies into a statistically thresholded likelihood map of where a given arrhythmia
arises. The intended clinical payoff is shorter mapping time, higher first-pass ablation
efficacy, and fewer lesions delivered off target.

aleArrhythmia is not a competitor to EnSite X EP, Rhythmia HDx or KODEX-EPD. It is an open,
add-on layer that those systems — and the literature around them — can feed and consume. Its
viewer takes its shape from Mango (mangoviewer.com): a small, focused, free tool that displays a
statistical map on a reference anatomy and nothing more.

The project is also a public portfolio artifact. It is built in the open so that its
correctness, its documentation and its engineering can be inspected by anyone.

## Core Principles

### I. Open by Default

Every artifact of this project — source, reference atlas, statistical method, example data,
documentation — MUST be public under an OSI-approved licence and developed in a public
repository. No component may depend on a proprietary SDK, a paid dataset or a closed binary as a
requirement to build, test or run the core. Vendor interoperability is achieved by reading
exported files, never by embedding vendor code.

Rationale: an unopenable meta-analysis map cannot be checked, and a method nobody can run does
not change practice. The project's credibility and its portfolio value both rest on this.

### II. One Canonical, Versioned Reference Space

All coordinates MUST be expressed in a single canonical cardiac reference space that the project
defines, names and versions. The space MUST be documented well enough that an independent group
can transform their own coordinates into it. Any change to the space MUST bump its version, and
every stored coordinate MUST record which space version it was expressed in. Results computed in
different space versions MUST NOT be pooled.

The choice of that space is an open research question at ratification time — see
TODO(REFERENCE_SPACE). Exploration of candidates is expected and encouraged; publishing a
statistical result before the choice is recorded in an ADR is not.

Rationale: ALE only means something because fMRI agreed on MNI/Talairach. Without the cardiac
equivalent there is no meta-analysis, only a pile of incompatible numbers.

### III. Statistical Validity Is Non-Negotiable

The statistical core MUST implement the modern ALE formulation, not a count-per-region
approximation: per-focus modeled activation with an uncertainty kernel, union across foci within
a study, random-effects pooling across studies, a null distribution obtained analytically or by
permutation, and correction for multiple comparisons (cluster-level FWE or voxel/vertex-level
FDR) with the method and threshold stated in every output.

Every statistical routine MUST be covered by tests that assert numerical behaviour, including at
least one test reproducing a published fMRI-ALE result within stated tolerance before the method
is adapted to cardiac geometry. No statistical map may be produced by a code path that lacks
such a test.

Rationale: a plausible-looking heat map that is statistically wrong is worse than no map, because
it will be believed and it will direct a catheter.

### IV. Provenance on Every Number

Every map, cluster and coordinate the system emits MUST carry machine-readable provenance: the
input studies with their identifiers, the number of foci and subjects per study, the reference
space version, the kernel and thresholding parameters, the software version and the random seed.
Any analysis MUST be reproducible from its provenance record alone.

Rationale: meta-analysis is only as trustworthy as its audit trail, and reviewers will ask.

### V. Add-On, Not Replacement

The system MUST NOT position itself as, or attempt to become, a real-time electroanatomic
mapping system. It MUST NOT be placed in the intraprocedural control loop, MUST NOT drive or
annotate ablation hardware, and MUST NOT be required for any procedural step. Its integration
surface with EnSite X EP, Rhythmia HDx, KODEX-EPD and any successor is limited to importing
exported geometry and point data, and to exporting maps in documented open formats those systems
or their users can read.

Rationale: real-time mapping is a regulated-device problem with a multi-year approval path.
Staying an offline research add-on keeps the project shippable, safe and legal.

### VI. Research Tool, Not a Medical Device

Every user-facing surface MUST state that the software is for research and educational use and is
not a medical device, not validated for diagnosis or treatment, and not to be used to guide
clinical decisions in an individual patient. The project MUST NOT ingest, store or transmit
identifiable patient data; all inputs are either published aggregate coordinates or
user-supplied, locally-held, de-identified geometry. No telemetry.

Rationale: the whole point is to influence ablation practice — which is exactly why the boundary
between "evidence synthesis" and "device" has to be drawn explicitly and defended.

### VII. Small, Legible, Installable

Python is the language of the statistical core; it ships as a pip-installable package exposing
both a library API and a CLI, with text/JSON in and out. The viewer is a browser application
(TypeScript, WebGL) that runs client-side with zero install and can be embedded as a panel
alongside other tools. Core and viewer communicate only through documented file formats — the
viewer MUST remain optional, and the core MUST remain usable headless.

Prefer the smallest thing that works: a readable 200-line module beats a framework. Dependencies
are added only when they replace code the project would otherwise have to test itself.

Rationale: Mango's value was that it was small and it opened. The same applies here, and a
headless core is what makes the method usable inside other people's pipelines.

### VIII. Traceable by Construction

Every non-trivial decision — statistical, anatomical, architectural, or product — MUST be
recorded as a numbered Architecture Decision Record note in the theory vault before the decision
is acted on, with all five fields filled:

- **Options considered** — at least two, each named and described, including the option of doing
  nothing where that is real.
- **Trade-offs** — what each option costs and buys, stated per option, not as a single summary.
- **Chosen** — the option taken and the reason it beat the others.
- **Rejected** — why each other option lost. "Not chosen" alone is not an answer.
- **References** — DOI, URL, `file:line`, dataset id, or the transcript of the conversation where
  the call was made. A decision with no reference is not traceable and does not pass.

Code, specs, plans and vault notes cite decisions by ADR id (`ADR-0007`). CI MUST fail when an
ADR has an empty Options, Trade-offs or References field, when a cited ADR id does not exist,
when two ADRs share a number, or when an ADR is superseded without the superseding id recorded.

Rationale: the point is that any step can be re-opened a year later and understood — what was on
the table, what it cost, why this one. Convention alone erodes exactly when a session is rushed,
so the check is mechanical.

## Theory Vault and Public Surface

- **The vault is the theory**: all derivations, method notes, literature summaries, open
  questions and ADRs live in an Obsidian vault at `docs/vault/` inside the public repository.
  Plain Markdown with `[[wikilinks]]` and YAML frontmatter only — no note may depend on a
  proprietary or optional Obsidian plugin to be readable or renderable.
- **Vault-first**: a method that exists in code but not in the vault is undocumented and
  incomplete. Any change to the statistical method, the reference space or the file formats MUST
  land with its vault note in the same commit.
- **Frontmatter is machine-readable**: every note carries at minimum `title`, `type`
  (`theory` | `adr` | `literature` | `question` | `log`), `status`, `created`, `updated`, and for
  ADRs the `id` and any `supersedes` / `superseded_by`.
- **Rendered, not exported**: the site build reads `docs/vault/` directly and emits static HTML —
  wikilinks resolved to links, backlinks listed per note, a graph view over the whole vault, and
  full-text search. No Obsidian Publish, no second copy to keep in sync, no build-time network
  call. A broken wikilink fails the build.
- **Public surface**: the rendered vault and the viewer are published on `vanioantunes.com` under
  a fourth homepage section, "My projects in 3D reconstruction", reusing that site's existing
  static-HTML stack, styling and hosting rather than introducing a framework.
- **Reader-facing**: the rendered vault MUST be navigable by someone who has never opened
  Obsidian — index page, per-note breadcrumbs, and an ADR list ordered by number and status.

## Scientific and Clinical Constraints

- **Anatomical scope**: the project MUST state, per analysis, which chambers and structures the
  reference space covers. Coordinates outside the declared scope are rejected, not silently
  projected.
- **Arrhythmia taxonomy**: study foci MUST be tagged with a controlled arrhythmia classification
  (mechanism, chamber, substrate) so that pooling is between like and like. Pooling across
  mechanisms requires an explicit, documented opt-in.
- **Minimum study count**: ALE is unstable with few experiments. The software MUST refuse, or
  loudly warn on, analyses below a documented minimum number of contributing studies, and MUST
  report per-cluster contribution so a single study cannot silently drive a cluster.
- **Reporting standard**: the project MUST publish a short reporting guideline telling authors
  how to report arrhythmia origin coordinates in the canonical space, including what to do when
  only a segment label is available. Adoption of this guideline is a project deliverable, not a
  side note.
- **Uncertainty is first-class**: registration error, mapping-system spatial error and anatomical
  variability MUST be represented in the kernel width or otherwise propagated, never assumed
  zero.

## Delivery Phases

- **Phase 0 — Groundwork (current)**: the vault skeleton and the ADR template come first, since
  everything after is recorded in them. Then: survey of candidate reference spaces, of open
  cardiac atlases, and of vendor export formats; reproduction of a published fMRI-ALE result with
  the Python core. Output: vault notes and ADRs, no public claims.
- **Phase 1 — Core**: Python package implementing cardiac ALE end to end on synthetic and
  literature-derived coordinates, with the canonical space fixed and versioned. Output: public
  repo, tests, CLI, documented file formats.
- **Phase 2 — Viewer and public surface**: browser viewer rendering the likelihood map on the
  reference anatomy, with cluster inspection and provenance display, running client-side; plus
  the static vault renderer. Both published under the "My projects in 3D reconstruction" section
  of vanioantunes.com.
- **Phase 3 — Interoperability**: import of exported geometry/point data from at least one
  commercial mapping system, and export of maps in a format such a system's users can load.
- **Phase 4 — Corpus and guideline**: a curated, citable set of extracted arrhythmia coordinates
  plus the published reporting guideline.

A phase is complete only when its output is public, tested and documented. Phases MAY overlap;
they MUST NOT be skipped — in particular no viewer work may substitute for Phase 0 reproduction.

## Governance

This constitution supersedes other practice in this repository. Where a plan, spec or task
conflicts with it, the constitution wins and the conflicting artifact is amended.

**Amendment procedure**: amendments are made by editing this file, with a Sync Impact Report at
its top recording the version change, the rationale, and the status of every dependent artifact.
Any change to Principles II, III, V or VI additionally requires an ADR in
`docs/vault/decisions/` explaining the trade-off, because those four define what the project
scientifically and legally is. ADRs are never deleted or rewritten: a reversed decision gets a
new ADR that supersedes the old one, and both stay readable.

**Versioning policy**: semantic versioning of this document. MAJOR for removing or redefining a
principle in a backward-incompatible way; MINOR for adding a principle or section, or materially
expanding guidance; PATCH for clarification and wording.

**Compliance review**: every plan produced by `/speckit-plan` MUST pass an explicit Constitution
Check before tasks are generated, and MUST re-run that check after design. Every pull request
description MUST state which principles it touches and cite the ADR ids behind any decision it
embodies. Complexity that violates Principle VII MUST
be justified in writing in the plan's Complexity Tracking section, or removed.

**Version**: 1.1.1 | **Ratified**: 2026-09-20 | **Last Amended**: 2026-09-20
