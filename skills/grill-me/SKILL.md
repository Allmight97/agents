---
name: grill-me
description: Interview the user about a plan, design, implementation, or decision until the action-changing branches are resolved. Use when the user wants to stress-test an idea, pressure-test tradeoffs, expose blind spots, get grilled on a proposal, compare options, or explicitly says "grill me"; ask no more than two sharp questions at a time. Stay project-agnostic unless a repository owns material facts, constraints, terminology, or durable capture; then inspect its guidance and source before asking.
---

# Grill Me

Drive the conversation as an active design review. The goal is not more
questions; the goal is to resolve the branches that change the decision,
implementation, risk, proof path, or next action.

## Boundary

Use this for personal decisions, product or design questions, general technical
design, and repository discussions. Stay project-agnostic when no repository
owns the decision. When one does, follow its applicable instructions and source
without importing repository-specific nouns or routing into this shared skill.

## First Response

When invoked, do not only acknowledge the request. Name the decision space in
one sentence, then ask one or two sharp questions with your recommended answers.

Use two questions when that materially improves progress. They do not need to be
inseparable, but both must be high-value and must move the conversation toward
shared coherence, a locked decision, a proof path, or a concrete next action.
Lists of requested facts count as questions; do not use them to bypass the
two-question cap.

## Loop

1. Name the decision or proposal being grilled in one sentence.
2. For repository-grounded work, inspect the nearest applicable `AGENTS.md`,
   owner documentation, code, and tests needed to resolve material facts.
3. Separate facts from decisions: resolve discoverable facts from artifacts or
   tools, and put each action-changing decision to the user.
4. Identify the highest-leverage unresolved branch.
5. Ask one or two sharp questions at a time with your recommended answer.
6. After each answer, lock the decision, narrow the next branch, inspect more
   source material, or summarize the coherent shape.

For repository-grounded work, identify the owning behavior when instructions,
documentation, code, or tests conflict. Ask which source should change only
when that choice is a genuine user decision. When durable capture is part of
the accepted outcome, use the repository-defined destination and shape.

## Question Quality

Good questions change what happens next. Prefer questions that affect scope,
ownership, sequencing, risk, reversibility, validation, cost, or user impact.
Each question should accrete: constrain the decision space, expose a real branch,
or convert uncertainty into an action, proof path, or explicit non-decision.

Use concrete scenarios when abstractions stay fuzzy: name the actor, input,
boundary crossed, expected outcome, and what evidence would settle it.

If the user is overloaded, tired, or time-constrained, reduce the active surface:
ask for the next executable decision rather than opening a full decision tree.

Do not dump a questionnaire. Do not ask the user to restate facts that available
artifacts can answer.

## Stop Conditions

Keep pushing until one of these is true:
- the design has a coherent end-to-end shape,
- the remaining uncertainty is explicitly bounded,
- the next proof step is clear,
- or the user wants to stop.

Reaching a stop condition ends the questioning. Confirm the shared understanding
before handing off. Confirmation locks the decisions; it does not authorize a
new action. Proceed only when the user has explicitly requested that action with
adequate scope, whether earlier in the conversation or after the decisions are
resolved.

## Output

When the conversation stabilizes, summarize:
- the decisions made,
- the main risks or open questions,
- the recommended next action,
- and the proof or evidence that would change the recommendation.

For repository-grounded work, also name the owner or boundary, resolved facts,
and intended durable-capture destination when relevant. Make the summary usable
by a fresh agent without hidden dependence on the conversation.
