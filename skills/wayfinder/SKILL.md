---
name: wayfinder
description: Develop or advance a GitHub roadmap for work that spans sessions and has unresolved scope or design decisions.
---

# Wayfinder

Calibrate first. Map only work whose uncertainty or span cannot fit safely in
one session. The user's experience affects how large work feels; repository
evidence and decision structure determine how large it is.

## Contract

- Use one existing or new GitHub parent issue as the roadmap through discovery
  and execution. Do not create a separate Wayfinder shell and implementation
  roadmap for the same destination.
- Use separate linked parent roadmaps only for genuinely different destinations.
  Give the successor an explicit entry condition from its predecessor and keep
  it thin until active; a possible future destination does not require an issue
  yet.
- Wayfinder owns the discovery phase: destination, decision frontier, settled
  decisions, and the execution shape.
- `grill-me` owns sharp questioning for user decisions. `to-issues` owns
  the coordinating issue for each delivery PR after the route is clear.
- After drafting a roadmap or adjudicating findings, get an independent
  holistic check from a different reviewer model when the host can delegate, or
  name the missing check. Verify its claims in the repository before adopting.
- Keep GitHub native: parent/sub-issue and blocked-by/blocking relationships.
  Add no setup skill, tracker abstraction, project board, milestone, label set,
  or local mirror unless a demonstrated need earns it.
- Treat the issue tracker as shared state and the repository as factual
  evidence. Keep each decision's full resolution in one place.

## Publication And Operational Setup

A request to create or update a GitHub roadmap authorizes the parent, scoped
children, and native relationships needed for that map. Draft the concrete
content before raising unresolved choices. Use existing authorization when
publishing; do not ask again merely because a command writes to the tracker.

Changing repository settings, authentication, or access is a separate operation.
If Issues are disabled or access is missing, prepare the roadmap and describe
the exact blocker; use any existing authorization for its repair, otherwise ask
before changing that configuration. "Continue roadmap #123" authorizes
recording the resolution and advancing that map. "Help me think this through"
keeps the work in the conversation until the user requests durable capture.

## Calibrate The Effort

1. Inspect first. Read the supplied concept and the nearest repository truth:
   owning instructions, current implementation, relevant issues, accepted
   decisions, and proof surfaces. Resolve discoverable facts without asking the
   user to estimate technical complexity.
   If the target repository is neither supplied nor discoverable, classify
   from the supplied facts and ask for its path before asserting
   implementation state.
   Treat mixed-abstraction input as normal. Separate user outcomes, product or
   UX choices, technical proposals, and uncertainty into user decisions,
   discoverable facts, research or prototype questions, and possible
   implementation work. Do not make the user sort those layers first.
2. Find the action-changing unknowns. An existing roadmap or phase inventory
   does not prove the route is clear: test whether it names a concrete
   destination, decision frontier, sequencing, and proof-backed execution
   shape. Preserve accepted program truth and Wayfind only the missing route.
   Consider touched ownership surfaces,
   reversibility, independent research or prototypes, unresolved user choices,
   proof burden, and whether the work fits one fresh agent context.
3. Use `grill-me` when user decisions still change the classification. Ask the
   complete dependency-safe decision frontier, with a recommendation for each
   question. Skip questioning when the evidence already makes the shape clear.
4. Recommend one route:
   - **Small and clear:** direct implementation; coherent commits only if useful.
   - **One coherent PR and mostly clear:** one issue or PR plan with work
     slices and commit blocks, however large; no child issues merely to
     represent slices or commits.
   - **Large or materially foggy:** one parent roadmap issue and the Wayfinder
     process below.

State why the chosen route fits. A user may still request Wayfinder for a
smaller effort; keep the calibration useful and the resulting map proportional.

## Chart One Roadmap

Prefer an existing issue when it genuinely owns the destination. Create a new
parent only when no existing issue owns it or expanding an existing issue would
make that issue misleading.

Once the destination is settled, map action-changing unknowns breadth-first;
create children only for questions that remain precise after that pass.

Create a discovery child issue only when its resolution:

- needs a separate agent context;
- can run independently or in parallel;
- produces a durable answer other work depends on; or
- needs a native blocking relationship.

Resolve smaller decisions through `grill-me` in the current conversation and
record the result in the parent. Do not manufacture an issue per question.

Before drafting or publishing the parent and any children, read
[`references/github-roadmap.md`](references/github-roadmap.md) for the owned
body shapes and native GitHub relationship commands.

## Advance A Roadmap

When the user provides a roadmap URL or number:

1. Load the parent body and open sub-issue relationships at low resolution.
   Read full child bodies and closed resolutions only when they bear on the
   current frontier.
2. Use the named child when the user supplied one. Otherwise recommend the
   highest-leverage open, unblocked child; do not make the user rediscover the
   graph.
3. Resolve the active frontier through `grill-me` when user decisions remain.
   Continue through settled children while the requested scope and user pace
   support it. Independent research may run in parallel when delegation is
   authorized; each result returns to its owning child.
4. Record the full resolution once in the child, close it, and link it from
   `Decisions settled`. Add a brief outcome when its title alone is insufficient
   for low-resolution orientation.
5. Put newly visible but still imprecise work in `Decision frontier`. Create a
   child when the question becomes precise and passes the child-issue threshold.
   Move work beyond the destination to `Out of scope`.

Expect live tracker state to change between sessions. Re-read relationships
before editing and preserve concurrent work.

## Shape Execution

Slices organize investigation and review; pull requests organize delivery, so
one slice is not one PR.

Draw each slice vertically: one user-facing capability from intent through its
backend owner and runtime boundary to the resulting UI or artifact. A
backend-only slice stays vertical when it names the route whose contract stays
stable. Shared helpers and contracts ride with the capability that uses them.
For a whole-surface destination such as an audit, reconcile coverage so each
owned responsibility belongs to exactly one capability, with no residual
horizontal cleanup bucket. Mark each slice's App check: whether a maintainer
must try it in the running app. A PR with any such slice opens as a draft until
that trial passes; otherwise it opens ready for the automated PR reviewer.

Group slices into the fewest coherent vertical PRs. First merge every slice
that changes the same owner, frontend or backend, so no owner is reopened
across PRs; each contract change ships with all its consumers. Keep neighboring
PRs apart, or cut horizontally, only for a named technical reason: a contract
that must merge before its dependents build on it, a proof lane that must be
gated separately (such as a migration that completes before dependent code
deploys), or a combined diff too large to review coherently. Judge size from
the expected change, not the number of capabilities, and cut a size split where
the fewest owners are shared. Different owners, languages, test commands, proof
types, or App checks are not reasons. Record for each PR why its slices ship
together and why it is separate from the next. Large coherent PRs are expected:
several capabilities on one owner form one PR, reviewed through its commits,
even when each could be demoed alone. Per-slice PRs for a solo maintainer are
ceremony without payoff.

One coordinating issue tracks each delivery PR. Slice-scope issues may hold
bounded audit records under the parent; they do not each become a PR. Merge
order follows concrete contract dependencies. Review each PR's slices in detail
when it starts, against the current default branch, and record the adopted
scope in its coordinating issue.

## Hand Off When The Route Is Clear

The route is clear when:

- the destination is concrete and accepted;
- no action-changing decision remains unresolved;
- remaining implementation uncertainty has a named proof path inside a slice;
  and
- the delivery PRs and their merge dependencies are known.

Update `Current phase` to `Route clear`, then recommend one handoff:

- **Multiple PRs:** use `to-issues` on the same parent for one coordinating
  issue per delivery PR, within the accepted grouping or the user's delegated
  authority. Link each from the parent's group table.
- **One PR:** keep one issue or PR plan with its slices and coherent commit
  blocks. Add no execution children.
- **Direct implementation:** proceed only when that action has been explicitly
  requested with adequate scope.

The discovery workflow ends at the handoff. Continue through the selected
workflow when the user already authorized it; a roadmap-only request ends with
the map and recommended next action.

## Output

Lead each turn with the current state: no roadmap needed, draft ready, frontier
item resolved, or route clear. Show the recommendation, evidence that determines
the scale, durable links when they exist, and the next action. Keep the user
oriented without making them reconstruct the graph.

When the roadmap is hard to absorb in prose, use
[visual-brief](../visual-brief/SKILL.md) for a compact current/target and progress
view. Keep the issue authoritative and label the visual a snapshot.
