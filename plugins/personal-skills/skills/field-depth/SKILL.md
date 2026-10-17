---
name: field-depth
description: "Do a task the way a field-leading expert would: pick Speed, Altitude, Depth, or Range, then run the Depth opener before acting."
disable-model-invocation: true
---

# Field Depth

Raise the current task from the digested layer to the methods a field-leading
expert would actually use. Default to Depth. Deeper, not bigger: fewer
options, harder evidence, not a longer list.

The four ambition types and the Depth prompt come from Felix Rieseberg,
[How to be more ambitious](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/).
Read [assets/ambition-four-types.jpg](assets/ambition-four-types.jpg) or
[assets/depth-prompt.jpg](assets/depth-prompt.jpg) only when a visual of that
framing would help.

## Ambition Types

Pick one:

- **Speed** — the same work in less time. Skip unless that is all they want.
- **Altitude** — go up in abstraction: the outcome over the task. Ask what
  should happen next; design the system, not the slide.
- **Depth** — do the task the way a field-leading expert would. Touch the
  underlying data, tools, and problems, not the digested layer.
- **Range** — pull in other fields. Prefer verbs over nouns; assemble
  techniques from those fields, not role-play characters.

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
4. What, other than you or the user, would show the result is right.

Then rewrite the ask to request exactly that, and do the deeper version.

## Fuzzy Asks

Do not stall asking them to rephrase. Infer the clearer ask they would make if
they already had field experience:

1. State in one sentence what you think they are trying to get done (outcome,
   not wording).
2. Run the Depth four lines on that outcome.
3. Offer the reframed prompt as what you will do, then do it unless they
   object.
4. If two interpretations would change the result a lot, pick the one that
   increases Depth (or Altitude if the ask is clearly an outcome loop) and
   name the fork in one line.

Preserve their intent; upgrade the method.

## Agent Guidance

When writing a skill, persona, or other agent-facing guidance for professional
work, bake this into the default behavior; do not only mention the skill:

- The Depth opener runs before search or a hard decision.
- Hard evidence gates before ranking; the user's stated take outweighs the
  model's score.
- Raw sources only. Do not invent numbers or treat another agent's recap as
  evidence.
- One next lock step when they are stuck.

Use [writing-for-agents](../writing-for-agents/SKILL.md) for how to place
those rules.

## Pressure Test

When asked to pressure-test this method, pick one stuck ask. Run once with the
Depth opener visible. Score: opener present, raw sources named, methods and
proof named, gates before ranking, no invented facts, deeper not bigger. Fail
any item, then fix the guidance rather than blaming the user.

## Anti-Patterns

- Switching vocabulary to sound expert without switching methods.
- Making the task bigger (more options, more role-play) instead of deeper.
- Letting the model judge itself; prefer an outside check the model can run.
- Skipping the four lines because the ask felt clear enough.

## Boundaries

- `task-compass` owns the primary outcome, mode, and verification budget for a
  mixed or rambling request. This skill owns the ambition type and the Depth
  opener once that outcome is in view.
- `grill-me` owns pressure-testing a decision with questions. This skill
  upgrades the method and then does the work.
