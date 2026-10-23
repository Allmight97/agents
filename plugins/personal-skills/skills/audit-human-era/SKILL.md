---
name: audit-human-era
description: "Audit a repo's CI, hooks, checks, and workflows for steps built around human speed or gestures, and for checks that do not prove what they claim. Report only. Use when the owner asks for a human-era, process, or validation audit."
disable-model-invocation: true
---

# Audit Human-Era Processes

Find processes that exist because a human is slow, or that go green without
proving anything. Output is a ranked report. Change nothing.

## Boundary

Report only. Do not add tools, harnesses, scripts, PRs, issues, or rule
changes, and do not start apps or desktop harnesses, without the owner's yes.
Read-only commands and read-only API calls are fine. A check you run must not
touch the working tree. Why: an audit once started an unrequested desktop
harness.

## Two lenses, both required

Run both. One audit that found only pace problems missed every proof problem.

**Pace and gesture.** A step built around human speed, attention, or a manual
act. Examples: CI triggered by toggling a PR between draft and ready, output
sized for terminal scrollback, a failure that only reaches a human's inbox,
a scheduled job nobody reads, a review that must be requested by hand.

**Proof validity.** Does each check prove what it claims? Examples: a file no
rule maps still gets a green gate; a pre-commit hook reads working files, not
staged bytes; a check mutates the tree it checks; tests that only match
strings. For each required check, ask what input would make it pass while the
claim is false, then try that input read-only.

## Evidence

Every finding cites one of: `file:line`, a run ID, or a command with its
output. Label anything else `inference`. Check live state (workflow runs,
branch rules, hook files) before you state what a process does.

## Output

Ranked findings, worst first. Each has:

- label: `ADOPT` (replace the step with the machine-first alternative),
  `ADAPT` (keep the step, reshape it), `DROP` (remove it, nothing replaces
  it), `GAP` (a check is missing), or `OWNER` (the owner decides);
- the evidence;
- one line on what it costs, in plain language;
- a one-line machine-first alternative;
- the accountability that stays with the human: the decision only the owner
  can make, such as release, spend, or product choice.

End with what you did not check.

## Cross-check

Claude and Codex audit independently. Then each fact-checks the other's
findings against sources and marks each `confirmed`, `refuted`, or
`unverifiable`. Different models catch different things; the owner keeps Codex
as a second opinion. From Claude Code, Cursor, or Grok Build, run Codex
through the `codex-review` skill when it is installed; otherwise run
`codex exec ... </dev/null` (stdin closed). Merge into one report. If only one model is
available, say so at the top of the report.
