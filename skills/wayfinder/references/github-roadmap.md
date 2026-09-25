# GitHub Roadmap Publication

Read this reference only after Wayfinder has chosen an existing or new parent
issue and the destination plus current decision frontier are clear enough to
publish.

## Parent Body

```markdown
## Destination

<The concrete state this effort is finding a route toward.>

## Current phase

Discovering

## Decision frontier

<Unresolved questions that materially change the route.>

## Decisions settled

<Link durable resolutions; add a brief outcome when the title does not convey it.>

## Pull request groups

<Empty until the grouping is approved. One row per delivery PR: its slices,
coordinating issue and any slice-scope issues, why its slices ship together,
and the technical reason it is separate from the next PR.>

## Execution slices

<Vertical capability slices, each naming the owners it changes in every layer,
runtime boundary, resulting UI or artifact, proof, and App check (yes/no). For
a whole-surface destination, add the shared-responsibility assignments.>

## Out of scope

<Explicit exclusions and why they sit beyond this destination.>
```

## Discovery Child Body

```markdown
## Question

<The precise decision or investigation this child resolves.>

## Resolution criterion

<The observable condition that makes this question settled.>
```

Name Grill, Research, Prototype, or Prerequisite in the title or question only
when it changes how the child is resolved. Research supplies facts; it does not
decide user-owned preferences. A prototype is throwaway evidence, not an
implementation slice. A prerequisite performs only the manual work required to
unblock a decision.

## Relationships

Prepare the parent, children, and blocking edges before publishing. Resolve
material content choices; existing publication authority does not need another
approval. Verify the live CLI supports the operations below, then use native
GitHub relationships:

- create children with `gh issue create --parent <parent>`;
- wire dependencies during creation with `--blocked-by` or afterward with
  `gh issue edit --add-blocked-by`;
- inspect `parent`, `subIssues`, `blockedBy`, and `blocking` with
  `gh issue view --json`.

Operate without assignments for a solo user. Use explicit issue numbers to
coordinate parallel agents. Add a claim mechanism only after a real concurrency
collision demonstrates the need.
