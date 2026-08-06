---
name: wayfinder
description: Roadmap large or materially foggy work as one evolving GitHub parent issue, resolve its decision frontier, then hand settled execution structure to to-issues. Use for consequential multi-session work whose destination or route is unclear and for explicit Wayfinder requests; exit to a single-PR plan or direct implementation when no durable map is needed.
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
  decisions, and the evidence needed to choose an execution shape.
- `grill-me` owns sharp questioning for user decisions. `to-issues` owns
  implementation child issues after the route is clear.
- Keep GitHub native: parent/sub-issue and blocked-by/blocking relationships.
  Add no setup skill, tracker abstraction, project board, milestone, label set,
  or local mirror unless a demonstrated need earns it.
- Treat the issue tracker as shared state and the repository as factual
  evidence. Keep each decision's full resolution in one place.

## Publication And Operational Setup

An instruction such as "create a Wayfinder roadmap" or "use Wayfinder for this
repository" authorizes the ordinary repository-local operations required to
make the roadmap functional: enable GitHub Issues, create or update the reviewed
parent and children, and wire their native relationships. Treat disabled
Issues, API failures, and authentication failures as operational conditions to
correct in scope or report precisely, not as new permission decisions.

Show the proposed parent content and child graph before publishing when choices
remain. That review aligns the roadmap's content; it is not a separate approval
gate for operational prerequisites. "Continue roadmap #123" authorizes
recording the resolution and advancing that map. "Help me think this through"
keeps the work in the conversation until the user requests durable capture.

## Calibrate The Effort

1. Inspect first. Read the supplied concept and the nearest repository truth:
   owning instructions, current implementation, relevant issues, accepted
   decisions, and proof surfaces. Resolve discoverable facts without asking the
   user to estimate technical complexity.
   When the target repository or product is not unambiguously supplied or
   discoverable from the active workspace, classify from the supplied facts
   only and ask for the source path before asserting implementation state.
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
   - **One PR and mostly clear:** one issue or PR plan with work slices and
     coherent commit blocks; no child issues merely to represent commits.
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
3. Resolve one human-in-the-loop child per session through `grill-me`. Bounded,
   independent research children may run in parallel through available tools or
   subagents, but each returns evidence to its own child.
4. Record the full resolution once in the child, close it, and link it from
   `Decisions settled`. Add a brief outcome when its title alone is insufficient
   for low-resolution orientation.
5. Put newly visible but still imprecise work in `Decision frontier`. Create a
   child when the question becomes precise and passes the child-issue threshold.
   Move work beyond the destination to `Out of scope`.

Expect live tracker state to change between sessions. Re-read relationships
before editing and preserve concurrent work.

## Hand Off When The Route Is Clear

The route is clear when:

- the destination is concrete and accepted;
- no action-changing decision remains unresolved;
- remaining implementation uncertainty has a named proof path inside a work
  slice; and
- the execution shape is known.

Update `Current phase` to `Ready to slice`, then recommend one handoff:

- **Multiple PRs:** use `to-issues` on the same parent. Add one implementation
  child per independently verifiable PR slice after the user approves the
  breakdown.
- **One PR:** keep one issue or PR plan with work slices and coherent commit
  blocks. Add no execution children unless independence or blocking earns them.
- **Direct implementation:** proceed only when that action has been explicitly
  requested with adequate scope.

Wayfinder stops at the handoff. The roadmap persists; the discovery process
does not silently become implementation.

## Output

Lead each turn with the current state: no roadmap needed, draft ready, frontier
item resolved, or route clear. Show the recommendation, evidence that determines
the scale, durable links when they exist, and the next action. Keep the user
oriented without making them reconstruct the graph.
