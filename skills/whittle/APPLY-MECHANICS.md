# Apply Mechanics

Read this branch when the user authorized implementation changes. The shared
judgment and guardrails remain in [SKILL.md](SKILL.md).

## Apply The Cut

1. Inspect the target, its owner guidance, the real flow, and existing proof.
2. Name the requirement and the complexity that does not help satisfy it.
3. Choose the earliest shared ladder option that fully preserves the outcome.
4. Make the smallest coherent change, including cleanup made obsolete by it.
5. Run proof proportionate to the changed owner and inspect the final diff.

Prefer deletion and existing owners over new layers. Do not introduce a new
interface, factory, configuration surface, dependency, or extension point
without a present requirement whose benefit exceeds its upkeep.

Smallness is a design result:

- A direct expression is better than a ceremony-heavy one when both are equally
  clear and correct; one line is not inherently better than five.
- A narrow diff is better when it localizes the invariant; do not preserve the
  wrong owner merely to touch fewer files.
- Focused proof is better than test expansion; match proof to plausible
  regression risk and the repository's owning boundary.

## Output

Lead with the implemented result and proof. Briefly name material machinery
that was deliberately skipped and the condition that would justify it later.
Give a fuller explanation when the user asked for one or the tradeoff genuinely
affects their next decision.
