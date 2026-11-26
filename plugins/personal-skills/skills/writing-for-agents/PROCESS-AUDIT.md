# Process Audit

Shared writing guidance lives in [SKILL.md](SKILL.md).

Find rules that live only in prose, checks that go green without proving
anything, and steps that wait on a human. Output is a ranked report. Change
nothing.

## Boundary

Report only. Do not add tools, harnesses, scripts, PRs, issues, or rule
changes, and do not start apps or desktop harnesses, without the owner's yes.
Read-only commands and read-only API calls are fine. A check you run must not
touch the working tree. Why: starting an app or harness changes the owner's
machine.

## Three lenses, all required

Run all three. Each lens finds problems the others miss.

**Prose that should be a check.** Sort each rule in the guidance by the three
questions in [SKILL.md](SKILL.md). A rule a fixed pattern decides, enforced
only by prose, is a finding; so is a prose rule the code already breaks.

**Proof validity.** Does each check prove what it claims? Examples: a file no
rule maps still gets a green gate; a pre-commit hook reads working files, not
staged bytes; a check mutates the tree it checks; tests that only match
strings. For each required check, ask what input would make it pass while the
claim is false, then try that input read-only.

**Pace and gesture.** A step built around human speed, attention, or a manual
act. Examples: CI triggered by toggling a PR between draft and ready, output
sized for terminal scrollback, a failure that only reaches a human's inbox,
a scheduled job nobody reads, a review that must be requested by hand.

## Evidence

Every finding cites one of: `file:line`, a run ID, or a command with its
output. Label anything else `inference`. Check live state (workflow runs,
branch rules, hook files) before you state what a process does.

## Output

Ranked findings, worst first. Each has:

- label: `ADOPT` (replace the step or prose with the machine-first
  alternative), `ADAPT` (keep it, reshape it), `DROP` (remove it, nothing
  replaces it), `GAP` (a check is missing), or `OWNER` (the owner decides);
- the evidence;
- one line on what it costs, in plain language;
- a one-line machine-first alternative;
- the accountability that stays with the human: the decision only the owner
  can make, such as release, spend, or product choice.

End with what you did not check.

## Cross-check

Claude and Codex audit independently. Then each fact-checks the other's
findings against sources and marks each `confirmed`, `refuted`, or
`unverifiable`. Run Codex through the `codex-review` skill. Merge into one
report. If `codex-review` is not installed, audit with one model and say so at
the top of the report.
