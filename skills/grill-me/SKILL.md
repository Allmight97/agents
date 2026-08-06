---
name: grill-me
description: Interview the user about a plan, design, implementation, or decision in dependency-safe frontier rounds until every action-changing branch is resolved. Use when the user wants to stress-test an idea, pressure-test tradeoffs, expose blind spots, compare options, or explicitly says "grill me"; inspect repository truth first when it owns material facts or constraints.
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
one sentence, map the current decision frontier, then ask every action-changing
question whose prerequisites are already settled. Number each question and give
your recommended answer.

## Loop

1. Name the decision or proposal being grilled in one sentence.
2. For repository-grounded work, inspect the nearest applicable `AGENTS.md`,
   owner documentation, code, and tests needed to resolve material facts.
3. Separate facts from decisions: resolve discoverable facts from artifacts or
   tools, and put each action-changing decision to the user.
4. Map the decision tree. The **frontier** is every unresolved user decision
   whose prerequisites are settled.
5. Ask the whole frontier in one numbered round, with a recommended answer for
   each question. Each question and recommendation must stand without assuming
   the answer to another question in the same round; otherwise it waits for a
   later round.
6. After each answer, lock the settled decisions, inspect more source material,
   and recompute the frontier.

When a frontier branch needs a discoverable fact, use tools or a bounded
subagent to find it. Treat that fact as an unsettled prerequisite for its
downstream questions, but continue the round with the rest of the unblocked
frontier.

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

Do not pad the frontier with fact requests, cosmetic preferences, or questions
whose answers would not change the result. Do not ask the user to restate facts
that available artifacts can answer.

## Stop Conditions

Keep pushing until the frontier is empty: every action-changing branch has been
visited, and remaining uncertainty is either a named proof question or explicit
non-scope. Stop earlier when the user asks.

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
