# Review Mechanics

Read this branch for a read-only audit of accidental complexity. The shared
judgment and guardrails remain in [SKILL.md](SKILL.md).

## Pin The Scope

Choose the target the user named:

- **Diff**: inspect the current change in diff order.
- **Path or repository**: rank concrete cuts by expected reduction in concepts,
  dependencies, maintenance, and change surface.
- **Tests**: judge each test or shared group by the contract it protects, as
  [SKILL.md](SKILL.md) says, and measure runtime or flakiness when that cost
  is part of the finding.

Exclude generated, vendored, and dependency trees. Inspect active owner and
boundary guidance, then trace enough of each call path to distinguish accidental
indirection from load-bearing policy. Apply nothing during review mode.

## Finding Standard

Report only a cut whose replacement and preserved behavior are supportable.
Before a `delete`, search the whole tree for the name, including config, docs,
and string or dynamic references. References only from tests do not keep code
alive; the cut removes those tests. Number findings so the user can pick them:

`<n>. <location> — <tag>: <what this code is and the complexity to remove>. <smaller owner or replacement>. <why behavior remains covered>. Skipping it costs: <the upkeep that stays>.`

Use the tag that identifies the mechanism:

- `delete`: behavior or flexibility with no present requirement;
- `reuse`: functionality with an existing owner in the codebase or an already-owned
  dependency;
- `stdlib`: bespoke code replaced by a named standard-library capability;
- `native`: code or dependency replaced by a platform capability;
- `collapse`: an abstraction or configuration surface that has no independent
  responsibility;
- `shrink`: the same owned logic expressed more directly.

A test takes the same tags: `delete` one that protects nothing a broader test
does not; `collapse` duplicates of one contract; `reuse` one whose contract
belongs in another proof tier, whether an existing test there proves it or the
test moves there; `shrink` one to its contract. A test worth keeping as it is
gets no finding. For a test, the coverage slot names the test that still proves
the contract, or the protection the cut loses. When the code blocks the broader
proof, name the refactor that would allow it.

Do not report correctness, security, performance, or merge-readiness findings
as Whittle findings. Route a material observation to its specialist owner and
keep it separate from the deletion audit.

## Stop And Summarize

When defensible, summarize the net reduction in concepts, dependencies, or
approximate lines. Do not manufacture precision or use line count as the reason
for a cut.

When remaining ideas are taste, speculative, or governed indirection, stop with
`Lean already. Ship.`

End every report, `Lean already. Ship.` included, with `Not checked:` naming
the parts you did not read or run, or `none`.
