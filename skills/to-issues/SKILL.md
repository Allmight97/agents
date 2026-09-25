---
name: to-issues
description: Turn a settled plan or parent GitHub issue into child issues, one per coherent vertical pull request, with native dependencies. Use when the user asks to split work into issues or create actionable tickets; resolve material scope choices before publishing.
---

# To Issues

Break a plan into the fewest issues that each track one coherent vertical pull
request (tracer bullets).

Read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md` when present in the repo.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes an issue reference (issue number, URL, or path) as an argument, fetch it from the issue tracker and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current
state of the code. Use terminology from the owning interface and nearest local
guidance, and respect relevant recorded decisions in the touched area. Do not
create a repository-wide glossary or architecture document merely to name the
issues.

Identify prerequisite refactors only when they demonstrably reduce implementation
risk or effort. Keep a prerequisite in its consuming issue unless it is a
contract other issues must build on.

### 3. Group vertical slices into pull requests

Use the plan's slices, or break it into complete outcomes through the layers
that actually participate. A backend-only outcome need not invent a UI; a
user-facing handoff must include the integration that makes it work.

<vertical-slice-rules>

- Each issue tracks one PR that delivers complete behavior with its necessary integration and proof, demoable or verifiable on its own; a large coherent PR is fine, and a slice that could be demoed alone is not a reason for its own issue
- Slices that change the same owner, frontend or backend, share an issue, so no later PR reopens that owner; a contract change ships with all its consumers
- Split a group, or cut work horizontally, only for a named technical reason: a contract that must merge before its dependents build on it, a proof lane that must be gated separately (such as a migration that completes before dependent code deploys), or a diff too large to review coherently, judged from the expected change rather than the number of capabilities. Different owners, languages, test commands, proof types, or App checks are not reasons
- Put genuine prerequisites before the work that depends on them
- An issue may span several agent sessions on one branch; each session completes a bounded part with its proof

</vertical-slice-rules>

For a genuinely wide mechanical refactor where a vertical slice would be
artificial, use **expand → migrate → contract**: add the compatible path, move
callers in bounded batches, then remove the old path. Keep the phases in one
issue unless the diff would be too large to review coherently.

### 4. Resolve the breakdown

Present the proposed breakdown as a numbered list. For each issue, show:

- **Title**: short descriptive name
- **Slices**: what it includes, why they ship together, and why it is separate from the next issue
- **Blocked by**: which other issues (if any) must complete first
- **App check**: yes or no
- **User stories covered**: which user stories this addresses (if the source material has them)

Ask only about unresolved choices that change scope, granularity, or dependency
order. If the user supplied the breakdown or delegated slicing and publication,
proceed within that authority. A draft-only request ends with the breakdown.

### 5. Publish the issues to the issue tracker

For each authorized issue, reuse a matching existing child or publish a new issue. Use the issue body template below. These issues are considered ready for AFK agents; apply the repository's documented triage label when one exists, otherwise add none.

Publish issues in dependency order (blockers first) so you can reference real
issue identifiers in the native blocked-by relationship or fallback body field.

When publishing to GitHub, verify live CLI support and use native relationships
as the source of truth:

- create children with `gh issue create --parent <parent>`;
- add dependencies with `--blocked-by` during creation or
  `gh issue edit --add-blocked-by` afterward;
- omit the `Parent` and `Blocked by` body sections below when those native
  relationships carry the same information.

Use the body sections only when the active tracker lacks native parent or
dependency relationships. Do not encode a second copy of a native relationship.

<issue-template>
## Parent

A reference to the parent issue on the issue tracker (if the source was an existing issue, otherwise omit this section).

## What to build

A concise description of the PR's end-to-end behavior, not layer-by-layer implementation. Name the included slices and any slice-scope issues holding their audit records, why they ship together, and the technical reason this PR is separate from its neighbors. When work starts, revalidate this scope against the current default branch and record any change here.

Include stable owner or entrypoint paths when they help the next agent find the
work; verify them against current code. Avoid prescribing incidental file
layouts. Include a small type, state machine, or schema only when it expresses
an accepted decision more precisely than prose.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## App check

**Yes**: open the PR as a draft; a maintainer tries <workflow> in the running app, then marks it ready. Or **No**: open it ready for review once <automated proof> passes, so the automated PR reviewer runs immediately.

## Blocked by

- A reference to the blocking ticket (if any)

Or "None - can start immediately" if no blockers.

</issue-template>

App check is yes when a maintainer must try any included behavior in the running
app. Reconfirm it before opening the PR; a newly affected interaction, platform
integration, or unproved runtime route makes it yes.

Keep the parent issue's title, state, and accepted plan unchanged; fill in
coordinating-issue links only where its approved PR-group table awaits them.
Add only the approved native sub-issue or dependency relationships needed to
publish the breakdown.
