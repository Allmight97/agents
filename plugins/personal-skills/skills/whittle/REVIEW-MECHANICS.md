# Review Mechanics

Read this branch for a read-only audit of accidental complexity. The shared
judgment and guardrails remain in [SKILL.md](SKILL.md).

## Pin The Scope

Choose the target the user named:

- **Diff**: inspect the current change in diff order.
- **Path or repository**: rank concrete cuts by expected reduction in concepts,
  dependencies, maintenance, and change surface.

Exclude generated, vendored, and dependency trees. Inspect active owner and
boundary guidance, then trace enough of each call path to distinguish accidental
indirection from load-bearing policy. Apply nothing during review mode.

## Finding Standard

Report only a cut whose replacement and preserved behavior are supportable:

`<location> — <tag>: <complexity to remove>. <smaller owner or replacement>. <why behavior remains covered>.`

Use the tag that identifies the mechanism:

- `delete`: behavior or flexibility with no present requirement;
- `reuse`: functionality with an existing owner in the codebase or an already-owned
  dependency;
- `stdlib`: bespoke code replaced by a named standard-library capability;
- `native`: code or dependency replaced by a platform capability;
- `collapse`: an abstraction or configuration surface that has no independent
  responsibility;
- `shrink`: the same owned logic expressed more directly.

Do not report correctness, security, performance, or merge-readiness findings
as Whittle findings. Route a material observation to its specialist owner and
keep it separate from the deletion audit.

## Stop And Summarize

When defensible, summarize the net reduction in concepts, dependencies, or
approximate lines. Do not manufacture precision or use line count as the reason
for a cut.

When remaining ideas are taste, speculative, or governed indirection, stop with
`Lean already. Ship.`
