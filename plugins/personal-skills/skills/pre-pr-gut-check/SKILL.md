---
name: pre-pr-gut-check
description: "Gut-check finished work before it lands on the default branch or a PR opens, and apply the fixes that earn their keep."
---

# Pre-PR Gut Check

Review finished work for shape, simplicity, correctness, tests, and agent
guidance by composing the skills that own each lens, then apply the fixes that
bring the work to its intended end state. Run it before the work is pushed to
the default branch, or before a PR opens or goes ready when the work needs one.

Fully load each composed skill, including the mechanics files it names for the
mode in use.
Load [improve-codebase-architecture](../improve-codebase-architecture/SKILL.md)
and [code-review](../code-review/SKILL.md) from these paths, not by bare name,
which can resolve to a built-in skill. A skill that is unavailable is a skipped
lens; report it as skipped.

## Establish the review

Gather once and give every lens:

- the diff against the base: the PR base when a PR exists, otherwise the
  remote default branch tip (for example `origin/main`, so unpushed commits on
  local `main` are included), plus uncommitted work;
- the intended end state in one or two sentences, inferred from the issue,
  commits, PR, or conversation; ask only when those sources conflict or are
  silent;
- the target repository's guidance along the changed paths and its
  verification commands.

A diff that changes behavior, interfaces, tests, skills, or agent guidance gets
the full check. Otherwise report `Gut check: trivial diff, nothing to check.`
and stop.

## Shape lenses

These judge the diff against the end state and do not depend on each other.
When the client supports delegation, run each in its own subagent so one skill's
criteria do not blur into another's.

- **improve-codebase-architecture**, its Explore and Recommend steps, scoped
  to the modules the diff touches. Its candidates feed the dispositions below
  in place of its report and candidate selection.
- **whittle** in review mode on the diff.
- **code-review** on the changed behavior, including its security search;
  skip the security search only when the user says so.

## Decide and apply

Merge candidates from every lens and drop duplicates. Give each one
disposition, written as one plain sentence: what it is, whether a user would
notice, and whether it is a real bug or tidiness. Judge severity apart from
disposition: a defect a user would notice is a real bug even when it predates
this work or is deferred, and a structural change that also removes such a
defect is a bug fix.

- **fix**: changes behavior, prevents a person or agent from acting wrongly,
  or is needed to reach the end state; stays within this work; and can be
  proven with the repository's checks;
- **defer**: real, but outside the end state or owned by other work; it goes
  in the report, and in the PR body when a PR exists; opening issues is outside
  this check;
- **reject**: taste, tidiness that changes no behavior or next action,
  speculative, or costs more than it returns.

Apply structural fixes (moves and deletions) before simplifications, and both
before correctness fixes, so later fixes land on code that survives.

## Consequence lenses

Run these on the diff after shape fixes, since they judge what the code became:

- **A test-review skill in the target repository's own skills**, if one
  exists (look under its `.claude/skills/`): whether tests pin required
  behavior of the final shape, including assumptions the fixes removed.
- **writing-for-agents** on the guidance and documents the work affects:
  stale rules, pointers, or interface lists, and new invariants without an
  owner. Each skill the work adds or changes gets its own check.

Disposition and apply their candidates the same way.

## Verify and report

Re-run the repository's verification for the touched owners. Report:

- the dispositions, real bugs first, with deferred items listed (ready for the
  PR body when a PR exists);
- which lenses ran and which were skipped, with the reason;
- the checks re-run after fixes and their results;
- whether the change is a one-way or two-way door (hard or easy to reverse)
  and its blast radius.

If nothing earns a fix, say so in one line.
