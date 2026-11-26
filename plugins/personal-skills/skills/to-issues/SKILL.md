---
name: to-issues
description: "Split a settled plan or parent GitHub issue into child issues, one per commit group of vertical slices. Use when the user asks to split work into issues or tickets."
---

# To Issues

Break a plan into the fewest issues that each track one coherent commit group:
vertical-slice commits that land on the default branch together.

Follow `issue-hygiene` for publish authorization, label gates, and body rules;
the template below is the child-issue shape.

## Process

### 1. Gather context

If the user passes an issue reference (issue number, URL, or path) as an
argument, fetch it from the issue tracker and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current
state of the code. Use terminology from the owning interface and nearest local
guidance, and respect the rationale that guidance records for the touched area.

Identify prerequisite refactors only when they demonstrably reduce implementation
risk or effort. Keep a prerequisite in its consuming issue unless one of the
split reasons below requires a separate commit group.

Done when you can name, for each slice, the owning module or entrypoint it
changes and the check that proves it.

### 3. Group vertical slices into commit groups

When the parent holds an approved commit-group table, use its groups as given
and skip to step 5.

Otherwise use the plan's slices, or break it into complete outcomes through the
layers that actually participate. A backend-only outcome need not invent a UI; a
user-facing handoff must include the integration that makes it work.

<vertical-slice-rules>

- Each issue tracks one commit group that delivers complete behavior with its
  necessary integration and proof, demoable or verifiable on its own. A large
  coherent group is fine, and a slice that could be demoed alone is not a
  reason for its own issue.
- Slices that change the same module, frontend or backend, share an issue, so
  no later group reopens that module. A contract change lands with all its
  consumers.
- Split a group, or cut work horizontally, only for a named technical reason: a
  contract that must land before its dependents build on it, a proof lane that
  must be gated separately (such as a migration that completes before dependent
  code deploys), or a change too large to verify or review coherently, judged
  from the expected change rather than the number of capabilities. Different
  modules, languages, test commands, proof types, or App checks are not
  reasons.
- Put genuine prerequisites before the work that depends on them.
- An issue may span several agent sessions; each session lands a bounded part
  with its proof.

</vertical-slice-rules>

Work that is horizontal by nature (a rename, an upgrade, updating every caller)
cannot be sliced coherently: it lands whole as one commit group in one issue.

### 4. Resolve the breakdown

Before proposing a parent issue, apply `issue-hygiene`'s parent threshold.

Present the proposed breakdown as a numbered list. For each issue, show:

- **Title**: short descriptive name
- **Slices**: what it includes, why they land together, and why it is separate
  from the next issue
- **Blocked by**: which other issues (if any) must complete first
- **App check**: yes when a maintainer must try any included behavior in the
  running app; a newly affected interaction, platform integration, or unproved
  runtime route makes it yes. Otherwise no.
- **User stories covered**: which user stories this addresses (if the source
  material has them)

Ask only about unresolved choices that change scope, granularity, or dependency
order. If the user supplied the breakdown or delegated slicing and publication,
proceed within that authority. A draft-only request ends with the breakdown.

### 5. Publish the issues to the issue tracker

For each authorized issue, reuse a matching existing child or publish a new
issue with the body template below. Apply labels by `issue-hygiene`.

Publish issues in dependency order (blockers first) so you can reference real
issue identifiers in the native blocked-by relationship.

Use native relationships as the source of truth:

- create children with `gh issue create --parent <parent>`;
- add dependencies with `--blocked-by` during creation or
  `gh issue edit --add-blocked-by` afterward.

On a tracker without native parent or dependency links, add `## Parent` and
`## Blocked by` sections to the body.

Keep the parent issue's title, state, and accepted plan unchanged. When the
parent is a wayfinder roadmap, link each new issue from its commit-group table.
Add only the approved native sub-issue or dependency relationships needed to
publish the breakdown.

```markdown
## Current state and next action

What is true on the default branch now for this group, and the first action
that starts it.

## What to build

A concise description of the group's end-to-end behavior, not layer-by-layer
implementation. Name the included slices, why they land together, and the
technical reason this group is separate from its neighbors. When the group needs
a pull request, name the technical need. When work starts, revalidate this scope
against the current default branch and record any change here.

Include stable owner or entrypoint paths when they help the next agent find the
work; verify them against current code. Avoid prescribing incidental file
layouts. Include a small type, state machine, or schema only when it expresses
an accepted decision more precisely than prose.

## Acceptance criteria

- Criterion 1
- Criterion 2
- Criterion 3

## App check

**Yes**: a maintainer tries <workflow> in the running app before the group is
pushed to the default branch. Or **No**: push once <automated proof> passes
locally. Reconfirm before pushing.
```

Done when every approved issue exists, `gh issue view` shows each parent and
blocked-by link, and the parent's group table links each issue.
