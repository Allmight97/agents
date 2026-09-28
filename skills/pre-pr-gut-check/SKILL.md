---
name: pre-pr-gut-check
description: "Run an end-of-implementation gut check on a branch diff before a PR is opened, updated, or marked ready, or when the user says \"gut check\". Composes whittle review, codebase-design, the repository's test-value skill, a writing-for-agents check of docs and guidance, and an optional low-effort code review, then applies only fixes that earn their keep."
---

# Pre-PR Gut Check

A gut check, not a directive. Look for the few changes that clearly earn their
keep before reviewers see the branch; leave everything else alone. No busywork,
no churn to show effort.

## Scope and scale

Review the branch diff against its base branch (the PR base when one exists,
otherwise the repository default branch), including uncommitted work.

Scale to the diff:

- **Trivial** (docs, config, a small mechanical edit): report one line —
  `Gut check: trivial diff, nothing to check.` — and stop.
- **Substantial** (behavior, interfaces, tests, or multiple owners): run the
  full pass below.

## Passes

Fully load each skill, including any mechanics files it tells you to read, and
apply it to this diff. Loading a skill here is the explicit invocation it may
require.

1. **whittle** in review mode: accidental complexity the diff adds or leaves.
2. **codebase-design** on the interfaces the diff changed: caller knowledge,
   owners, seams.
3. **The repository's test-value skill**, if one exists (for example ABB's
   `.agents/skills/audit-test-value`): tests the diff added, changed, or
   orphaned.
4. **Docs and guidance** with **writing-for-agents**: the repository's
   instruction network (`AGENTS.md`/`CLAUDE.md` chain, owner guidance, skills,
   and documents such as changelogs) against what the diff
   changed. Look for stale rules, pointers, or interface lists, and for a new
   invariant with no owner. Any skill the diff adds or changes gets its own
   writing-for-agents check. Doc fixes follow writing-for-agents.
5. **Code review at low effort** for correctness (Claude Code: `/code-review
   low`). Optional: skip it when the user drops it or the client has no
   equivalent, and say so.

A skill that is not installed or cannot load is a skipped pass, not a silent
one.

## Dispositions

Merge candidates from all passes; drop duplicates. Give each surviving
candidate exactly one disposition:

- **fix** — clear value, inside the branch's scope, cheap to prove;
- **defer** — real, but belongs to later work or another owner;
- **reject** — taste, speculative, or not worth its cost.

Write each as one plain sentence: what it is, whether a user would notice, and
whether it is a real bug or just tidiness.

## Apply and report

Apply only the `fix` items, then re-run the focused checks for the touched
owners (the repository's own verification commands). Put `defer` items in the
PR body. Do not open issues for them.

Report:

- the dispositions;
- which passes ran and which were skipped, with the reason — never claim a pass
  that did not run;
- the checks re-run after fixes and their results.

If nothing earns a fix, say so in one line and stop.

Once the report is final and any fix commits are made, record the reviewed
commit so a pre-PR reminder hook can tell the check is current:
`git rev-parse HEAD > "$(git rev-parse --git-dir)/pre-pr-gut-check"`.
