# Phase 0 Research: Theory Vault and Decision Traceability

**Feature**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Date**: 2026-09-20

Every item below resolves a technical unknown from the plan's Technical Context. Four of them
(R-001 repository layout, R-002 licensing, R-008 enforcement, R-009 scan scope) restate decisions the
operator already made during clarification; they are recorded here and become ADR-0001 through
ADR-0004 in implementation, because Principle VIII binds the project to the ADR form, not to a
research note.

---

## R-001: Repository layout

**Decision**: The project lives in its own standalone public repository,
`github.com/vanioljantunes/aleArrhythmia`.

**Rationale**: Constitution Principle I requires a public repository. Living as a folder inside a
larger private repository would mean either publishing unrelated private work or maintaining a
snapshot copy that drifts. A standalone repository also lets the project carry its own licences, its own issue
tracker and its own CI, which is what a portfolio artifact needs.

**Alternatives considered**: (a) Folder in a larger private repository with periodic export to a
public snapshot, rejected: snapshots drift, and history is lost, which contradicts Principle VIII;
(b) Git submodule inside a larger repository, rejected: adds a moving part for no gain now, and can be
added later without cost.

**Note for ADR-0001**: the repository was created before this record existed. That sequencing is
recorded honestly rather than back-dated.

---

## R-002: Licensing

**Decision**: Apache-2.0 at `LICENSE` covering code; CC-BY-4.0 at `LICENSE-docs` covering
`docs/vault/`. The README states which licence covers which path.

**Rationale**: Apache-2.0 carries an explicit patent grant, which matters in a field where device
vendors hold patents on mapping and ablation technique, a permissive licence without one leaves
downstream users exposed. CC-BY-4.0 on the prose lets the theory be quoted and reused with
attribution, which is the mechanism by which academic credit reaches the author.

**Alternatives considered**: (a) MIT everywhere, rejected: no patent grant, and its text speaks of
"the Software", which fits prose badly; (b) Apache-2.0 everywhere, rejected: workable, but gives
no citation-style attribution requirement for the theory, which is the portfolio's whole point;
(c) CC-BY-SA for prose, rejected: copyleft on notes would complicate quoting them in a journal
article.

---

## R-003: Note header format

**Decision**: YAML frontmatter delimited by `---` at the top of every note, parsed with
`yaml.safe_load`. Required keys for all notes: `title`, `type`, `status`, `created`, `updated`.
Decision notes add `id`, and optionally `supersedes` / `superseded_by`.

**Rationale**: YAML frontmatter is what Obsidian, Jekyll, Quartz, Hugo and every static renderer
already understand, so the Phase 2 renderer needs no custom parsing. `safe_load` refuses arbitrary
object construction, so a malformed or hostile note cannot execute anything.

**Alternatives considered**: (a) TOML frontmatter, rejected: Obsidian does not read it, which
breaks the operator's own editing workflow; (b) JSON sidecar files, rejected: doubles the file
count and separates metadata from the note it describes; (c) Inferring metadata from file paths -
rejected: silent and unverifiable.

---

## R-004: Link syntax and resolution

**Decision**: Wikilinks in the forms `[[note-basename]]`, `[[note-basename|display text]]` and
`[[note-basename#heading]]`. A link resolves against note basenames without the `.md` extension,
searched across the whole vault. Basenames must be unique vault-wide, and that uniqueness is itself a
checked rule.

**Rationale**: Basename resolution is Obsidian's default and keeps links stable when a note moves
between folders, which will happen as the vault grows. The uniqueness rule is what makes it
unambiguous; without it, resolution silently picks one of two candidates. Making uniqueness a
checked rule converts a latent ambiguity into a loud failure.

**Alternatives considered**: (a) Relative-path links, rejected: every folder move rewrites links,
and merge conflicts follow; (b) Obsidian's "shortest path when possible" with duplicate basenames
allowed, rejected: resolution becomes editor-dependent, and a file-based checker cannot reproduce
the editor's choice; (c) Standard Markdown links only, rejected: loses the backlink and graph
affordances the vault is for.

---

## R-005: Decision-record structure and extraction

**Decision**: An ADR is a Markdown file whose body contains five level-two headings with fixed
wording: `## Options considered`, `## Trade-offs`, `## Chosen`, `## Rejected`, `## References`. The
checker locates each heading and treats the text until the next heading as that field's content. A
field is empty if it contains no non-whitespace content other than the template's own placeholder
comments.

**Rationale**: Headings are readable prose to a human and a reliable anchor to a parser, so one
artifact serves both audiences, no separate machine format to keep in sync. Fixed wording is what
makes the check possible; the cost is that the headings cannot be renamed casually, which is
acceptable for five strings.

**Alternatives considered**: (a) Put the five fields in frontmatter, rejected: multi-paragraph
prose in YAML is miserable to write and read; (b) A separate structured file per ADR alongside the
prose, rejected: two sources of truth, guaranteed to diverge; (c) Free-form prose with a language
model judging completeness, rejected: non-deterministic, unreviewable, and needs network access.

---

## R-006: Decision-record identity and filename

**Decision**: Filename `ADR-NNNN-kebab-slug.md` in `docs/vault/decisions/`, with `id: ADR-NNNN` in
frontmatter. The number is zero-padded to four digits. The checker verifies that the filename prefix
and the frontmatter `id` agree, and that no two records share a number.

**Rationale**: The number is the stable citation handle; the slug is what makes a directory listing
readable. Requiring both to agree removes the class of error where a file is copied and its id is
not updated.

**Alternatives considered**: (a) Numeric id only, slug in frontmatter, rejected: unreadable
directory listing; (b) Date-based ids, rejected: not sequential, awkward to cite, and collides when
two decisions land the same day; (c) Hash or UUID ids, rejected: uncitable in conversation.

---

## R-007: Reference resolvability, what a checker can actually verify

**Decision**: The checker verifies the *shape* and *local* resolvability of references, never their
liveness. It accepts: a DOI matching the standard pattern, an http(s) URL, a repository path with
optional line number, a dataset identifier with a declared scheme, or a wikilink to a note holding a
recorded conversation. For repository paths it verifies the file exists and, if a line is given, that
the file has that many lines. It makes no network request.

**Rationale**: Constitution VI and the offline constraint forbid the checker phoning out, and link
liveness is not a property the project controls anyway. Verifying shape catches the real failure mode
- a reference field filled with "see the paper", while file-and-line verification catches the
common case of a citation that has drifted as code moved.

**Alternatives considered**: (a) Resolve URLs over the network, rejected: makes the check slow,
flaky, and dependent on connectivity, and would fail on every offline push; (b) Accept any non-empty
string, rejected: FR-009 requires resolvable, and "see the paper" is not; (c) Require DOIs only -
rejected: excludes repository files and conversations, both of which are legitimate evidence here.

**Consequence recorded in the spec**: link rot is handled by requiring enough identifying detail
(title, author, date, identifier) that a dead URL remains traceable, a human-review rule, not a
machine one.

---

## R-008: Enforcement mechanism

**Decision**: Two points. Locally, a tracked `.githooks/pre-push` script, activated by
`git config core.hooksPath .githooks`: one documented command, no framework. On the server, a
workflow that runs the same checker on every push to the public repository.

**Rationale**: The local hook gives failure in under a second, before anything is public. The
workflow proves the discipline to an outside reader and catches the case where the hook was never
installed or was bypassed. Tracking the hook in the repository means it is reviewable and versioned
like everything else. `--no-verify` remains possible, which is intentional: a bypass should be
available and visible, not impossible.

**Alternatives considered**: (a) Pull requests with required status checks, rejected: forces the
solo author to open a pull request against themselves for every note, and the operator explicitly
chose against it; (b) The `pre-commit` framework, rejected: a dependency and a config file to
replace four lines of shell; (c) Server-side check only, rejected: broken records become public
before anyone learns of them.

---

## R-009: Citation scan scope and file discovery

**Decision**: Enumerate candidate files with `git ls-files -z`, so only version-controlled files are
considered and `.gitignore` is honoured for free. Drop files that are not text (null byte in the
first 8 KiB). Drop paths matching `.vaultcheckignore`. Scan what remains for citations matching the
exact pattern `ADR-` followed by exactly four digits, on a word boundary.

**Rationale**: `git ls-files` is the definition of "version-controlled" and avoids walking
`node_modules` or build output by construction. The exact four-digit form makes false positives rare;
the ignore list handles the rest and, being a tracked file, is itself reviewable, which is the
property the operator asked for.

**Alternatives considered**: (a) Walk the filesystem directly, rejected: picks up untracked scratch
files and build output, and needs its own ignore logic; (b) Scan only the vault, rejected: leaves
FR-012 unenforced exactly where drift does damage, in code; (c) Loose citation pattern such as
`ADR-\d+`: rejected: matches prose like "ADR-1" and version strings.

---

## R-010: Ignore-list format

**Decision**: A tracked `.vaultcheckignore` at the repository root. One glob per line, matched with
`fnmatch` against repository-relative POSIX paths. Blank lines and `#` comments allowed. Every entry
must carry a trailing `#` comment explaining why it is excluded, and the checker fails if an entry
lacks one.

**Rationale**: Reusing gitignore's full semantics would mean either a dependency or reimplementing
negation and directory-anchoring rules, too much machinery for a short exclusion list. Requiring a
reason per line is what stops the ignore list from quietly becoming the place inconvenient files go.

**Alternatives considered**: (a) Full gitignore semantics via the `pathspec` package, rejected: a
third dependency for a file expected to hold single-digit entries; (b) Ignore patterns in
`pyproject.toml`: rejected: buries a reviewable policy inside build configuration; (c) No ignore
list at all, rejected: this document and the templates legitimately contain example identifiers.

---

## R-011: Status vocabularies

**Decision**: Closed vocabularies, checked. Notes generally: `draft`, `active`, `archived`. Decision
records: `proposed`, `accepted`, `superseded`. Open questions: `open`, `answered`. A `superseded`
record must carry `superseded_by`; an `answered` question must link to the record that answered it.

**Rationale**: Free-text status fields become `wip`, `WIP`, `in progress` and `started` within a
month, at which point no index can be generated from them. Tying `superseded` and `answered` to the
presence of their link is what makes FR-018 checkable rather than aspirational.

**Alternatives considered**: (a) Free-text status, rejected above; (b) A single shared vocabulary
across all note types, rejected: "accepted" is meaningless for a work log, "answered" for a
derivation.

---

## R-012: Packaging and invocation

**Decision**: A `pyproject.toml` declaring the `vaultcheck` package with a console entry point, so
the checker runs as `vaultcheck` after `pip install -e .`, and as `python -m tools.vaultcheck`
without installing. Dependencies: PyYAML at runtime, pytest under a `dev` extra.

**Rationale**: The hook and the workflow both need a stable invocation; the module form means a
fresh clone can run the check before installing anything, which matters for the fresh-clone edge case
in the spec.

**Alternatives considered**: (a) A loose script in `scripts/`: rejected: no test story, no
dependency declaration, and Principle VII's "installable" is a requirement not a preference;
(b) Publishing to PyPI, rejected: premature for a tool with one user and one repository.

---

## R-013: Output format and exit codes

**Decision**: One violation per line, `path:line: RULE-ID: message`, on stderr; a summary on stdout
naming how many notes, citations and links were verified. Exit 0 clean, 1 on violations, 2 on the
checker's own error (unreadable file, malformed YAML it cannot attribute).

**Rationale**: The `path:line:` prefix is what every editor and CI annotator already parses, so
failures become clickable with no extra work. Separating the checker's own failure (2) from a vault
violation (1) means a crash never reads as a clean vault.

**Alternatives considered**: (a) JSON output, rejected: nothing consumes it yet; can be added
behind a flag when something does; (b) Everything on stdout, rejected: makes the summary and the
failures indistinguishable when piped.

---

## R-014: Survey scope and method

**Decision**: One literature note per surveyed item, in three groups, candidate reference spaces,
open cardiac atlases, commercial export formats. Each note records what the thing is, its anatomical
coverage, its licence and availability, and its consequences for pooling coordinates. Sources are
published documentation and openly available datasets only. Anything not establishable becomes an
explicit unknown note stating what was tried.

**Rationale**: One note per item is what makes the backlink graph useful, the open question links to
candidates, candidates link to the atlases they need. Recording unknowns as first-class notes is
FR-027, and it is also how the survey stays honest: a gap is visible rather than absent.

**Alternatives considered**: (a) A single survey document, rejected: no backlinks, no per-item
status, and it cannot be superseded piecewise; (b) Contacting vendors for documentation, rejected
for this phase: unbounded latency, and Principle V means the project must work from public material
anyway.

**Known unknown going in**: whether the named commercial systems' export formats are documented
publicly at all. If they are not, that outcome is itself the recorded finding, and
TODO(VENDOR_INTEROP) in the constitution stays open.

---

## Resolved unknowns summary

| Plan unknown | Resolved by | Outcome |
|---|---|---|
| Header format and parser | R-003 | YAML frontmatter, `yaml.safe_load` |
| Link syntax and resolution | R-004 | Basename wikilinks, uniqueness enforced |
| ADR machine-readability | R-005, R-006 | Fixed H2 headings, `ADR-NNNN` id matching filename |
| What "resolvable reference" can mean to a checker | R-007 | Shape plus local resolution, never network |
| Enforcement surface | R-008 | Tracked pre-push hook plus push workflow |
| Which files are scanned | R-009, R-010 | `git ls-files`, text only, `.vaultcheckignore` with reasons |
| Status values | R-011 | Closed vocabularies per note type |
| Invocation | R-012 | `pyproject.toml`, console script plus module form |
| Failure reporting | R-013 | `path:line: RULE-ID: message`, exit 0/1/2 |
| Survey shape | R-014 | One note per item, unknowns recorded explicitly |

No NEEDS CLARIFICATION markers remain.
