---
name: wayfinder
description: "Map large or foggy work into a GitHub roadmap issue, or advance an existing roadmap by its number or URL. Use when work spans sessions with decisions still open."
---

# Wayfinder

Calibrate first: map only work whose uncertainty or span cannot fit one
session. Judge size from repository evidence, not how large the work feels.

## Calibrate The Effort

1. Inspect first. Read the supplied concept and the nearest repository truth:
   owning instructions, current implementation, relevant issues, accepted
   decisions, and tests and checks. Resolve discoverable facts without asking
   the user to estimate technical complexity.
   If the target repository is neither supplied nor discoverable, classify
   from the supplied facts and ask for its path before asserting
   implementation state.
   Treat mixed-abstraction input as normal. Separate user outcomes, product or
   UX choices, technical proposals, and uncertainty into user decisions,
   discoverable facts, research or prototype questions, and possible
   implementation work. Do not make the user sort those layers first.
   Done when every fact the route depends on is cited from the repository or
   marked unknown.
2. Find the action-changing unknowns. An existing roadmap or phase inventory
   does not prove the route is clear: test whether it names a concrete
   destination, decision frontier (the open decisions whose prerequisites are
   settled, as `grill-me` defines it), sequencing, and proof-backed execution
   shape. Keep what the existing plan already settles, and map only the
   missing route. Consider touched ownership surfaces,
   reversibility, independent research or prototypes, unresolved user choices,
   proof burden, and whether the work fits one fresh agent context.
   Done when each unknown is labelled user decision, discoverable fact, or
   research/prototype question.
3. Use `grill-me` when user decisions still change the classification. Ask the
   complete dependency-safe decision frontier, with a recommendation for each
   question. Skip questioning when the evidence already makes the shape clear.
4. Recommend one route:
   - **Small and clear:** direct implementation as vertical-slice commits.
   - **One commit group and mostly clear:** one issue or plan with its slices
     as commits, however large; no child issues merely to represent slices or
     commits.
   - **Large or materially foggy:** one parent roadmap issue and the Wayfinder
     process below.

State why the chosen route fits. A user may still request Wayfinder for a
smaller effort; keep the calibration useful and the resulting map proportional.

## Contract

- Use one existing or new GitHub parent issue as the roadmap through discovery
  and execution. Do not create a second roadmap issue for the same
  destination.
- Use separate linked parent roadmaps only for genuinely different destinations.
  Give the successor an explicit entry condition from its predecessor and keep
  it thin until active; a possible future destination does not require an issue
  yet.
- Wayfinder owns the discovery phase: destination, decision frontier, settled
  decisions, and the execution shape.
- `grill-me` owns sharp questioning for user decisions. `to-issues` owns
  commit grouping and the coordinating issue for each group after the route is
  clear.
- After drafting a roadmap or adjudicating findings, get an independent check
  through the `codex-review` skill, or name the missing check. Verify its
  claims in the repository before adopting.
- Keep GitHub native: parent/sub-issue and blocked-by/blocking relationships
  are the whole tracker.
- Treat the issue tracker as shared state and the repository as factual
  evidence. Keep each decision's full resolution in one place.
- Cross-reference issues as `issue-hygiene` says.

## Publication And Operational Setup

Follow `issue-hygiene` for write authorization and body rules; a request to
create or update a roadmap names the parent, its scoped children, and their
native relationships. Draft the concrete content before raising unresolved
choices.

Changing repository settings, authentication, or access is a separate operation.
If Issues are disabled or access is missing, prepare the roadmap and describe
the exact blocker. If the user already authorized that repair, make it;
otherwise ask before changing the configuration. "Continue roadmap #123"
authorizes recording the resolution and advancing that map. "Help me think
this through" keeps the work in the conversation until the user requests
durable capture.

## Chart One Roadmap

Prefer an existing issue when it genuinely owns the destination. Create a new
parent only when no existing issue owns it or expanding an existing issue would
make that issue misleading.

Once the destination is settled, map action-changing unknowns breadth-first;
create children only for questions that remain precise after that pass. Done
when every unknown that could change the route is listed in `Decision
frontier`.

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

1. Load the parent body and open sub-issue relationships, titles and states
   only. Read full child bodies and closed resolutions only when they bear on
   the current frontier.
2. Use the named child when the user supplied one. Otherwise recommend the
   highest-leverage open, unblocked child; do not make the user rediscover the
   graph.
3. Resolve the active frontier through `grill-me` when user decisions remain.
   Continue through settled children while the requested scope and user pace
   support it. Independent research may run in parallel when delegation is
   authorized; each result returns to its owning child.
4. Record the full resolution once in the child, close it, and link it from
   `Decisions settled`. Add a brief outcome when its title alone is
   insufficient for orientation.
5. Put newly visible but still imprecise work in `Decision frontier`. Create a
   child when the question becomes precise and passes the child-issue threshold.
   Move work beyond the destination to `Out of scope`.

Expect live tracker state to change between sessions. Re-read relationships
before editing and preserve concurrent work.

## Shape Execution

Slices organize investigation, review, and commits; issues organize tracking,
so one slice is not one issue.

Draw each slice vertically: one user-facing capability from intent through its
backend owner and runtime boundary to the resulting UI or artifact. A
backend-only slice stays vertical when it names the route whose contract stays
stable. Shared helpers and contracts ride with the capability that uses them.
For a whole-surface destination such as an audit, reconcile coverage so each
owned responsibility belongs to exactly one capability, with no residual
horizontal cleanup bucket. Mark each slice's App check: whether the user
must try it in the running app. A group with any such slice is pushed only
after that trial passes; otherwise it is pushed once its automated proof passes
locally.

Group slices into commit groups by the rules in `to-issues`. Record for each
group why its slices land together and why it is separate from the next.

## Hand Off When The Route Is Clear

The route is clear when:

- the destination is concrete and accepted;
- no action-changing decision remains unresolved;
- remaining implementation uncertainty has a named proof path inside a slice;
  and
- the commit groups and their landing order are known.

Update `Current phase` to `Route clear`, then recommend one handoff:

- **Multiple commit groups:** use `to-issues` on the same parent for one
  coordinating issue per group, within the accepted grouping or the user's
  delegated authority. Link each from the parent's `Commit groups` section.
- **One commit group:** keep one issue or plan with its slices as commits. Add
  no execution children.
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

When the roadmap is hard to absorb in prose, use the `visual-brief` skill for
a compact current/target and progress view. Keep the issue authoritative and
label the visual a snapshot.
