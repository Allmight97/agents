---
name: to-issues
description: Turn a settled plan or parent GitHub issue into independently verifiable child issues with native dependencies. Use when the user asks to split work into issues or create actionable tickets; resolve material scope choices before publishing.
---

# To Issues

Break a plan into independently-grabbable issues using vertical slices (tracer bullets).

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
risk or effort. Keep a prerequisite in its consuming slice unless independent
verification or reuse justifies a separate issue.

### 3. Draft vertical slices

Break the plan into thin, complete outcomes through the layers that actually
participate. A backend-only outcome need not invent a UI; a user-facing handoff
must include the integration that makes it work.

<vertical-slice-rules>

- Each slice delivers a narrow, complete behavior with its necessary integration and proof
- A completed slice is demoable or verifiable on its own
- Put genuine prerequisites before the work that depends on them
- Each slice fits one fresh agent context, including only the discovery needed to complete it safely

</vertical-slice-rules>

For a genuinely wide mechanical refactor where a vertical slice would be
artificial, use **expand → migrate → contract**: add the compatible path, move
callers in bounded batches, then remove the old path. Keep each issue independently
verifiable and state its dependency explicitly.

### 4. Resolve the breakdown

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories this addresses (if the source material has them)

Ask only about unresolved choices that change scope, granularity, or dependency
order. If the user supplied the breakdown or delegated slicing and publication,
proceed within that authority. A draft-only request ends with the breakdown.

### 5. Publish the issues to the issue tracker

For each authorized slice, reuse a matching existing child or publish a new issue. Use the issue body template below. These issues are considered ready for AFK agents, so publish them with the correct triage label unless instructed otherwise.

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

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Include stable owner or entrypoint paths when they help the next agent find the
work; verify them against current code. Avoid prescribing incidental file
layouts. Include a small type, state machine, or schema only when it expresses
an accepted decision more precisely than prose.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- A reference to the blocking ticket (if any)

Or "None - can start immediately" if no blockers.

</issue-template>

Keep the parent issue's title, body, and state unchanged. Add only the approved
native sub-issue or dependency relationships needed to publish the breakdown.
