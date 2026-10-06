---
name: grill-me
description: "Pressure-test a plan, design, or decision by asking the open questions that change it, with a recommendation for each. Use when the user asks to be grilled or to pressure-test a choice."
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

Finding discoverable facts is your job, never the user's. Read the applicable
`AGENTS.md`, owner documentation, code, tests, and tools yourself, or use an
authorized bounded subagent. Ask the user only for decisions.

## Loop

For the first response and every later round:

1. Name the decision or proposal being grilled in one sentence. Do not only
   acknowledge the request.
2. Separate facts from decisions, and resolve the facts that change a decision.
3. Map the decision tree. The **frontier** is every unresolved user decision
   whose prerequisites are settled.
4. Ask the actionable frontier in a manageable round, with a recommendation for
   each question. Split a wide frontier to respect the user's attention and the
   question tool's limits; prioritize decisions that unblock the most work. Each
   question and recommendation must stand without assuming
   the answer to another question in the same round; otherwise it waits for a
   later round.
5. After each answer, record settled decisions and recompute the frontier.
   Resolve any new fact the answer exposes.

Treat a fact still being found as an unsettled prerequisite for its downstream
questions, and continue the round with the rest of the unblocked frontier.

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

Do not pad the frontier with cosmetic preferences or questions whose answers
would not change the result.

## Stop Conditions

Keep pushing until the frontier is empty: every action-changing branch has been
visited, and remaining uncertainty is either a named proof question or explicit
non-scope. Stop earlier when the user asks.

Reaching a stop condition ends the questioning. Summarize the settled direction
before handing off; ask for confirmation only when a material interpretation
remains unresolved. A summary does not authorize a new action. Proceed only when
the user has explicitly requested that action with
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
