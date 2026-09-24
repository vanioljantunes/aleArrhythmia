# Quickstart: Validating the Theory Vault and Traceability Check

**Feature**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

This is the run guide that proves the phase works end to end. It is written to be followed on a
fresh clone by someone who has not seen the project. Implementation detail belongs in `tasks.md`;
what follows is only how to run and what to expect.

---

## Prerequisites

- Python 3.11 or newer
- Git
- No Obsidian. Deliberately: the vault must be legible without it (SC-005)

---

## Setup

```bash
git clone https://github.com/vanioljantunes/aleArrhythmia
cd aleArrhythmia

# the check runs before anything is installed
python -m tools.vaultcheck

# install the tool and the local enforcement, the one documented step (FR-023a)
pip install -e ".[dev]"
git config core.hooksPath .githooks
```

Expected after the bare `python -m tools.vaultcheck`: one warning, a summary line, and exit code
`0`. If the repository is clean, it says so before you have installed a thing.

```text
.githooks/pre-push:1: HOOK-NOT-INSTALLED: warning: the local pre-push check is not active; run: git config core.hooksPath .githooks
vaultcheck: N notes, M decision records, L links, C citations verified: clean
```

The warning is correct and expected on a fresh clone: you have not run the `git config` line yet. It
is a warning, not an error, so the exit code stays `0`. It disappears once the hook is active.

---

## Scenario 1, A clean vault passes

Validates FR-022, SC-003.

```bash
vaultcheck
echo "exit: $?"
```

**Expected**

```text
vaultcheck: N notes, M decision records, L links, C citations verified: clean
exit: 0
```

The counts are the point: a checker that verified nothing would also exit `0`, so the summary has to
state what it looked at.

---

## Scenario 2, Each defect kind is caught

Validates FR-015 through FR-021, SC-004. Run against the fixture vaults, which exist precisely so
these failures are reproducible:

```bash
pytest tests/ -v
```

**Expected**: one passing test per defect kind, each asserting both the exit code and the rule id.

Every registered rule has a fixture, and a meta-test fails the suite if a rule is ever added
without one, so this table is not maintained by hand. Each fixture is named after the rule it
provokes: `tests/fixtures/adr-empty-section/` triggers `ADR-EMPTY-SECTION`.

```bash
ls tests/fixtures/
```

Four fixtures are named for what they prove rather than for a rule:

| Fixture | Proves |
|---|---|
| `clean/` | A correct vault passes |
| `empty-vault/` | Zero notes is not an error, and the counts say zero |
| `prose-mentions-adr/` | Prose naming a record in passing is not a citation, so the exact-form rule raises no false positive |
| `adr-options-as-table/` | Options are counted from a Markdown table, not only from a list (ADR-0005) |

To see a failure by hand rather than through pytest:

```bash
vaultcheck --root tests/fixtures/adr-empty-section
echo "exit: $?"
```

**Expected**

```text
docs/vault/decisions/ADR-0001-example.md:19: ADR-EMPTY-SECTION: '## Trade-offs' has no content
vaultcheck: 6 notes, 1 decision records, 8 links, 4 citations verified: 1 violation
exit: 1
```

Every line names a file and a line number, so an editor can jump straight to it (FR-021).

---

## Scenario 3, A broken push is refused locally

Validates FR-023, FR-023a, SC-011. This edits a tracked file and then reverts; run it on a clean
working tree so the reset destroys nothing you wanted.

```bash
# break a record on purpose: empty the References section
python - <<'PY'
import pathlib
p = pathlib.Path("docs/vault/decisions/ADR-0001-repository-layout.md")
t = p.read_text(encoding="utf-8")
head, _, _ = t.partition("## References")
p.write_text(head + "## References\n\n<!-- emptied on purpose -->\n", encoding="utf-8")
PY

git add -A && git commit -m "temp: deliberately break a record"
git push
```

The break has to remove the section's contents, not merely add a line to it. Inserting a comment
after the heading leaves the references below it intact, so the record stays valid and the push
succeeds. That looks like the hook failing when in fact nothing was broken.

**Expected**: the push never reaches the network.

```text
docs/vault/decisions/ADR-0001-repository-layout.md:56: ADR-NO-REFERENCE: '## References' has no content
vaultcheck: N notes, M decision records, L links, C citations verified: 1 violation

pre-push: vaultcheck found violations. Push refused.
Fix what is listed above, or override deliberately with: git push --no-verify
An override is still checked on the repository and recorded there as a failure.
```

Then undo:

```bash
git reset --hard HEAD~1
```

---

## Scenario 4, The public repository catches what the hook missed

Validates the second half of FR-023.

```bash
git push --no-verify          # deliberate override
gh run list --limit 1
```

**Expected**: the push succeeds locally, and the traceability workflow on the repository reports a
failure for that commit. The override is possible and visible, which is the design, not a gap.

---

## Scenario 5, The vault reads without Obsidian

Validates FR-002, FR-005, SC-005.

```bash
cat docs/vault/index.md
ls docs/vault/decisions docs/vault/questions
```

**Expected**: `index.md` links to every note type and lists every open question and decision record.
Open any note in a plain editor: frontmatter at the top, prose below, no syntax that needs a plugin
to make sense.

Reader test: hand the `docs/vault/` folder to someone and ask them to find the project's open
questions and one method note. They should succeed on the first attempt, without instructions.

---

## Scenario 6, The survey is present and honest

Validates FR-024 through FR-029, SC-006, SC-007.

```bash
ls docs/vault/literature/
cat docs/vault/questions/canonical-reference-space.md
```

**Expected**: one literature note per candidate reference space, per open cardiac atlas, and per
commercial export format investigated. The reference-space question has `status: open`, links to
every candidate under `## Candidates`, and states under `## What would settle it` what evidence
would close it.

Then confirm nothing was invented:

```bash
grep -ril "unknown" docs/vault/literature/
```

Case-insensitive on purpose: the notes carry an `## Unknowns` heading, which a case-sensitive grep
misses. Every literature note should appear.

**Expected**: every item the survey could not establish appears as an explicitly recorded unknown
stating what was tried, not as an absence, and not as a guess.

And confirm the phase claims nothing:

```bash
grep -ri "we find\|we show\|results indicate" docs/vault/ || echo "no claims, correct"
```

---

## Scenario 7, Timing

Validates SC-008.

```bash
python -c "
import subprocess, time
t = time.perf_counter()
subprocess.run(['vaultcheck', '--quiet'], check=False)
print(f'{time.perf_counter() - t:.2f}s')
"
```

**Expected**: well under a second at present size; the budget is 60 seconds at 1000 notes. If it
ever approaches that, the hook becomes something people work around, and the guarantee dies.

---

## Done when

- [ ] Scenarios 1 through 7 behave as described on a fresh clone
- [ ] `pytest` is green, with one test per defect kind
- [ ] ADR-0001 through ADR-0004 exist, each with two or more options, per-option trade-offs, a
      reason for the choice, a reason per rejection, and at least one resolvable reference
- [ ] `docs/vault/index.md` reaches every note type within two links
- [ ] The reference-space question is open and links to every candidate
