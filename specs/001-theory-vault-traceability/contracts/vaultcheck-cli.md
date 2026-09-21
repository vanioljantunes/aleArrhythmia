# Contract: `vaultcheck` Command-Line Interface

**Consumers**: the author at a terminal, `.githooks/pre-push`, `.github/workflows/traceability.yml`.

**Stability**: exit codes and the violation line format are the interface. Adding a flag is
backward-compatible; changing an exit code's meaning or the line format is breaking.

---

## Invocation

```bash
vaultcheck                      # after `pip install -e .`
python -m tools.vaultcheck      # from a fresh clone, nothing installed
```

Both forms behave identically. The module form exists so a fresh clone can verify itself before any
install step (FR-023a, and the fresh-clone edge case in the spec).

---

## Arguments

| Argument | Default | Meaning |
|---|---|---|
| `--root PATH` | repository root, discovered via `git rev-parse --show-toplevel` | Repository to check |
| `--vault PATH` | `docs/vault` relative to root | Vault directory |
| `--ignore-file PATH` | `.vaultcheckignore` relative to root | Exclusion list |
| `--quiet` | off | Suppress the summary; violations still print |
| `--version` |, | Print version, exit 0 |

No `--fix`. The checker never edits files: a tool that silently repairs a decision record would
defeat the point of recording decisions.

No network flag, because there is no network path.

---

## Exit codes

| Code | Meaning | Consumer behaviour |
|---|---|---|
| `0` | Clean. Every rule passed | Hook allows the push; workflow reports success |
| `1` | One or more violations | Hook refuses the push; workflow fails the run |
| `2` | The checker itself failed, unreadable file, not a Git repository, malformed ignore file | Hook refuses the push; investigate the tool, not the vault |

Code `2` is deliberately distinct from `1`: a crash must never be mistaken for a clean vault.

---

## Output

**Violations**: one per line, on **stderr**:

```text
docs/vault/decisions/ADR-0003-enforcement.md:14: ADR-EMPTY-SECTION: '## Trade-offs' has no content
docs/vault/theory/ale-kernel.md:7: NOTE-BAD-STATUS: 'in-progress' is not valid for type 'theory' (expected: draft, active, archived)
tools/vaultcheck/links.py:88: CITE-DANGLING: cites ADR-0042, which does not exist
```

Format: `path:line: RULE-ID: message`

- `path` is repository-relative, POSIX separators, on every platform.
- `line` is 1-based. When a violation is not line-bound (a duplicate basename, a missing file) the
  line is `1` and the message names the counterpart file.
- Violations are sorted by path, then line, so output is stable across runs and diffable.

**Summary**: on **stdout**, suppressed by `--quiet`:

```text
vaultcheck: 34 notes, 7 decision records, 61 links, 12 citations verified: clean
```

On failure the summary states the counts and the number of violations. Separating the two streams
means a consumer can pipe violations without the summary getting mixed in.

---

## Rules enforced

Grouped by contract. Full condition tables live in the contracts named.

| Group | Rule ids | Source |
|---|---|---|
| Note headers | `NOTE-*` | [note-frontmatter.md](./note-frontmatter.md) |
| Decision records | `ADR-*` | [decision-record.md](./decision-record.md) |
| Citations | `CITE-DANGLING` | FR-017, this contract |
| Links | `LINK-UNRESOLVED`, `LINK-BAD-ANCHOR` | FR-019, R-004 |
| Questions | `Q-NO-CANDIDATES`, `Q-NO-CRITERIA`, `Q-ANSWERED-NO-TARGET` | FR-028, R-011 |
| Index | `INDEX-INCOMPLETE` | FR-005 |
| Ignore file | `IGNORE-NO-REASON` (error), `IGNORE-STALE` (warning) | R-010 |
| Local enforcement | `HOOK-NOT-INSTALLED` (warning) | ADR-0003, added during implementation |

Warnings print in the same format but do not affect the exit code.

---

## File discovery

1. `git ls-files -z` from `--root`. Only version-controlled files are considered.
2. Drop files containing a null byte in the first 8 KiB, treated as binary.
3. Drop paths matching any glob in the ignore file.
4. Notes are the surviving `.md` files under `--vault`; citation scanning covers all survivors.

An empty vault is not an error: the checker reports zero notes and exits `0`.

---

## Ignore file format

```text
# one glob per line, each with a reason
specs/**                      # spec prose cites example identifiers
docs/vault/templates/**       # templates contain placeholder ids by design
```

Globs are `fnmatch` patterns over repository-relative POSIX paths. A line without a trailing `#`
reason is `IGNORE-NO-REASON` and fails the run. A glob matching nothing is `IGNORE-STALE`, a
warning.

---

## Performance

Full run under 60 seconds at 1000 notes (SC-008), single-threaded, no caching. At the present scale
it completes in well under a second, which is what makes a pre-push hook tolerable.
