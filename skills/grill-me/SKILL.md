---
name: grill-me
description: Interview the user about a plan, design, implementation, or decision until the action-changing branches are resolved. Use when the user wants to stress-test an idea, pressure-test tradeoffs, expose blind spots, get grilled on a proposal, compare options, or explicitly says "grill me"; ask no more than two sharp questions at a time and stay project-agnostic while using provided artifacts as evidence when useful.
---

# Grill Me

Drive the conversation as an active design review. The goal is not more
questions; the goal is to resolve the branches that change the decision,
implementation, risk, proof path, or next action.

## Boundary

Use this for project-agnostic plans, personal decisions, general technical
design, or repo discussions that do not need project-specific durable routing.
Use source artifacts as evidence when available, but do not switch into durable
routing unless current repo truth or accepted-decision capture is actually
needed. If a repo has a dedicated alignment skill and the prompt depends on that
repo's current truth, docs, issue/spec routing, or durable capture, prefer that
repo-specific skill.

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
2. Identify the highest-leverage unresolved branch.
3. Inspect available artifacts when they can answer the question more reliably
   than the user can.
4. Ask one or two sharp questions at a time.
5. Include your recommended answer so the user can accept, reject, or refine.
6. After each answer, lock the decision, narrow the next branch, inspect more
   source material, or summarize the coherent shape.

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

## Output

When the conversation stabilizes, summarize:
- the decisions made,
- the main risks or open questions,
- the recommended next action,
- and the proof or evidence that would change the recommendation.
