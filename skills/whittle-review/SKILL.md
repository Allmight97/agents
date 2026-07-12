---
name: whittle-review
description: >
  Review for over-engineering without applying fixes: find what to delete,
  replace with stdlib/native, or shrink. Use when asked to review a diff or
  audit a repo for unnecessary complexity, bloat, deletion candidates, or YAGNI
  violations. Correctness, requested behavior, merge readiness, security, and
  performance are out of scope; route ordinary code review to code-review.
---

Review for unnecessary complexity. One line per finding:
`<tag> <what to cut>. <replacement>.` The best outcome is getting shorter.

## Scope

Pick one per invocation:

- **Diff** ("review this diff", "review for over-engineering"): scan the current changes.
  Report findings in diff order.
- **Repo** ("audit this codebase", "find bloat"): scan the whole tree.
  Rank findings biggest cut first.

## Tags

- `delete:` dead code, unused flexibility, speculative feature. Replacement: nothing.
- `stdlib:` hand-rolled thing the standard library ships. Name the function.
- `native:` dependency or code doing what the platform already does. Name the feature.
- `yagni:` abstraction with one implementation, config nobody sets, layer with one caller.
- `shrink:` same logic, fewer lines. Show the shorter form.

## Governance guard

Before flagging, check the path for an owner/boundary doc (AGENTS.md, a
public-API strip, an adapter layer); governed indirection is not a cut. Trace
the call path enough to be sure a "wrapper" or "extra layer" isn't load-bearing.
A "wrapper that only delegates" guarding a documented boundary stays.

## Hunt

Deps the stdlib or platform already ships, single-implementation interfaces,
factories with one product, wrappers that only delegate, files exporting one
thing, dead flags and config, hand-rolled stdlib. Exclude generated, vendored,
and dependency trees from findings.

## Examples

`L12-38: stdlib: 27-line validator class. "@" in email, 1 line, real validation is the confirmation mail.`

`L4: native: moment.js imported for one format call. Intl.DateTimeFormat, 0 deps.`

`repo.py:L88: yagni: AbstractRepository with one implementation. Inline it until a second one exists.`

`L52-71: delete: retry wrapper around an idempotent local call. Nothing replaces it.`

`L30-44: shrink: manual loop builds dict. dict(zip(keys, values)), 1 line.`

## Stop Condition

Line count is evidence, not the objective. Never recommend a cut solely to
increase the total. When the estimate is defensible, end with `net: about -<N>
lines possible` and, for repo audits, `-<M> deps possible`. Otherwise end with
`cuts: <N> concrete candidates` rather than manufacturing precision.

When the remaining ideas are taste, speculative, or governed indirection, stop:
`Lean already. Ship.` Do not invent another cleanup round.

## Out of scope

Correctness bugs, requested behavior, merge readiness, security holes, and
performance route to `code-review` or the matching specialist. A single smoke
test or `assert`-based self-check is the whittle minimum, not bloat; never flag
it for deletion. Lists findings, applies nothing.
