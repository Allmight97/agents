# Spatial Grammar

Use these patterns only when topology is the hard part. They are structural
references, not visual templates or a requirement to add more diagrams.

![Three spatial grammar examples: transform and merge, parallel ownership and
join, and guarded state change](spatial-grammar.svg)

If the current harness cannot inspect the SVG, use the text descriptions below.

## Transform And Merge

Several sources may enter at different points, undergo operations with different
scopes, and converge into a named result.

```text
Source A -> transform A --\
                           +-> merge -> result -> verification
Source B -> transform B --/
Source C ----------------/
```

Use this when a prose sequence would make the reader remember which inputs are
already present at each operation. The motivating example is Cooking for
Engineers' [Espresso Brownies recipe
table](https://www.cookingforengineers.com/recipe/327/Espresso-Brownies), where
row and column spans make ingredient entry, operation scope, convergence, and
baking visible at once. The original schematic above carries that grammar into
the shared skill without depending on the recipe content.

## Parallel Ownership And Join

Separate ownership from sequence. Show which actor or lane owns each action and
make the synchronization point explicit.

```text
Evidence lane: collect -> normalize ---\
                                        +-> decision gate
Review lane:   inspect -> challenge ----/
```

Use this for handoffs, parallel investigation, release gates, or coordinated
work. A join is a real dependency, not decorative convergence.

## Guarded State Change

Make the current state, condition, and resulting state visible. Include blocked,
retry, or recovery paths when they affect the decision.

```text
Draft --[checks pass]--> Ready --> Published
  ^                         |
  \---[rework complete]-- Rework
```

Use this when the same input can produce different next states or when a reader
must know why progress stopped.

## Zoomed Hierarchy

Do not force context, ownership, and implementation detail into one diagram.
Use progressively narrower views when each level answers a distinct question.
The [C4 diagram guidance](https://c4model.com/diagrams) is a useful external
reference for context-to-component zooming. Link to it rather than copying its
examples.

## Selection Check

Before using a pattern, confirm:

- it exposes a relationship prose would hide;
- labels are literal and locally defined;
- the result and stopping condition are visible;
- one primary visual is enough;
- removing the visual would materially increase reconstruction work.
