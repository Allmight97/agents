---
name: field-depth
description: "Expert-depth pass: redo a task the way a field-leading professional would, from raw material and the field's own methods. Use when asked to go deeper, act like a pro, or be more ambitious."
---

# Field Depth

Raise the current task from the digested layer to the methods a field-leading
expert would actually use. Default to Depth. Deeper, not bigger: fewer
options, harder evidence, not a longer list.

The four ambition types and the Depth prompt come from Felix Rieseberg,
[How to be more ambitious](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/).

## Ambition Types

Pick one. The Depth opener runs for every type except Speed.

- **Speed** — the same work in less time. When that is all they want, drop
  this skill and do the task directly.
- **Altitude** — go up in abstraction: the outcome over the task. Ask what
  should happen next; design the system, not the slide. Before opener line 1,
  name the outcome loop.
- **Depth** — do the task the way a field-leading expert would. Touch the
  underlying data, tools, and problems, not the digested layer.
- **Range** — pull in other fields. Prefer verbs over nouns; assemble
  techniques from those fields, not role-play characters. In opener line 3,
  name the second field's technique.

For most "act like a professional" asks, use **Depth**. Use Altitude when they
want an outcome loop. Use Range when one field's toolkit is obviously too
narrow.

## Depth Opener

Before rewriting or doing the work, say in a few short lines:

1. What a top professional in this field would do here that the user is not
   asking for.
2. The rawest material that pro would start from instead of what has already
   been digested.
3. The specific methods and tools they would use.
4. What, other than you or the user, would show the result is right: an
   outside check the agent can run.

Then rewrite the ask to request exactly that, and do the deeper version.

## Fuzzy Asks

Do not stall asking them to rephrase. Infer the clearer ask they would make if
they already had field experience:

1. State in one sentence what you think they are trying to get done (outcome,
   not wording).
2. Run the Depth opener on that outcome.
3. Offer the reframed prompt as what you will do, then do it unless they
   object.
4. If two interpretations would change the result a lot, pick the one that
   increases Depth (or Altitude if the ask is clearly an outcome loop) and
   name the fork in one line.

Preserve their intent; upgrade the method.

When writing a skill, persona, or other agent-facing guidance for professional
work, read [AGENT-GUIDANCE.md](AGENT-GUIDANCE.md).

## Boundaries

- `task-compass` sets the outcome first.
- `grill-me` owns pressure-testing a decision with questions. This skill
  upgrades the method and then does the work.
