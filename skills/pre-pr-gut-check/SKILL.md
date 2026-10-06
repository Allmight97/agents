---
name: pre-pr-gut-check
description: "Run a holistic end-of-implementation review of a branch diff and apply the fixes that earn their keep. Use before a PR is opened, updated, or marked ready, or when the user asks for a gut check."
---

# Pre-PR Gut Check

Review a finished branch for shape, simplicity, correctness, tests, and agent
guidance by composing the skills that own each lens, then apply the fixes that
bring the branch to its intended end state.

Fully load each composed skill, including the mechanics files it names for the
mode in use. Loading a skill here is the explicit invocation it may require.
A skill that is unavailable is a skipped lens; report it as skipped.

## Establish the review

Gather once and give every lens:

- the diff against the base branch (the PR base when one exists, otherwise the
  default branch), including uncommitted work;
- the intended end state in one or two sentences, inferred from the PR, issue,
  commits, or conversation; ask only when those sources conflict or are silent;
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
- **code-review** on the changed behavior, unless the user drops it.
- **security-best-practices** when the diff changes a trust boundary such as
  authentication, authorization, input parsing, secrets, or outbound requests.
- **impeccable** critique when the diff changes a user interface.

## Decide and apply

Merge candidates from every lens and drop duplicates. Give each one
disposition, written as one plain sentence: what it is, whether a user would
notice, and whether it is a real bug or tidiness. Judge severity apart from
disposition: a defect a user would notice is a real bug even when it predates
the branch or is deferred, and a structural change that also removes one is a
bug fix.

- **fix**: changes behavior, prevents a person or agent from acting wrongly,
  or is needed to reach the end state; stays within the branch; and can be
  proven with the repository's checks;
- **defer**: real, but outside the end state or owned by other work; it goes
  in the PR body, and opening issues is outside this check;
- **reject**: taste, tidiness that changes no behavior or next action,
  speculative, or costs more than it returns.

Apply structural fixes (moves and deletions) before simplifications, and both
before correctness fixes, so later fixes land on code that survives.

## Consequence lenses

Run these on the diff after shape fixes, since they judge what the code became:

- **The repository's test-value skill**, if it has one: whether tests pin
  required behavior of the final shape, including assumptions the fixes removed.
- **writing-for-agents** on the guidance and documents the branch affects:
  stale rules, pointers, or interface lists, and new invariants without an
  owner. Each skill the branch adds or changes gets its own check.

Disposition and apply their candidates the same way.

## Verify and report

Re-run the repository's verification for the touched owners. Report:

- the dispositions, real bugs first, with deferred items ready for the PR body;
- which lenses ran and which were skipped, with the reason;
- the checks re-run after fixes and their results.

If nothing earns a fix, say so in one line.

When no gut-check fixes remain uncommitted, record the reviewed commit so a
pre-PR reminder hook can tell the check is current:
`git rev-parse HEAD > "$(git rev-parse --git-dir)/pre-pr-gut-check"`.
Otherwise skip the record and say so.
