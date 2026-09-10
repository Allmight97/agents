---
name: writing-for-agents
description: Write or audit agent-consumed guidance, including skills, repository instructions, issues, and handoffs. Use when instruction clarity, placement, or execution scope is the task.
---

# Writing for Agents

Shape agent-consumed information so the next agent can determine what is true,
what to do, in what order, and how to know the work is complete. Mixed
human-agent documents must serve the human decision first without hiding the
agent's execution contract.

When a substantial mixed human-agent document needs a visual orientation, use
[visual-brief](../visual-brief/SKILL.md) for the HTML presentation. Keep the
execution contract and durable truth with their existing owner.

## First Move

Before drafting or editing:

1. Infer the mode from the whole request: an audit alone reports findings;
   requested updates include edits to the named surface.
2. Name the audience, document job, current state, durability, and owner.
3. Inspect the target plus the active pointers and owning sources needed to
   verify action-changing claims.

Proceed when the target and authority are clear and claims that could change
the next action are grounded or identified as uncertain. Scale inspection to
the requested change.

## Branches

- When the target is an Agent Skill or skill metadata, read
  [SKILL-MECHANICS.md](SKILL-MECHANICS.md) completely before judging or changing
  invocation, structure, disclosure, validation, or behavioral proof.
- When the target is an `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, or another
  instruction network—or the task asks where agent guidance belongs—read
  [INSTRUCTION-NETWORK-MECHANICS.md](INSTRUCTION-NETWORK-MECHANICS.md)
  completely before routing or editing guidance.
- For an issue, spec, handoff, decision record, audit, or other agent-consumed
  document, use the shared rules below without loading branch-only mechanics.

## State Before Story

Lead with the smallest useful statement of current state, recommendation, and
next action. Background follows after the reader knows why it matters.

For mixed-status work, use only the states that contain material information:

- **Completed**: outcome and durable proof or location.
- **Remaining**: unfinished work, owner, and next action.
- **Decision needed**: unresolved choice and recommendation.
- **Deferred or rejected**: work intentionally not happening and why.

Separate findings from dispositions. When an audit led to action, preserve the
chain **finding -> decision -> change -> proof**. When work advances, rewrite
the document around its new state; remove settled questions, obsolete future
tense, and proposal-shaped narration.

## Information Hierarchy

Place each meaning where the agent needs it:

1. **In-file steps** when order matters. Make consequential transitions and
   completion checkable.
2. **In-file reference** for rules every branch needs.
3. **Disclosed reference** for material needed only when a named branch fires.
4. **External reference** for truth owned by code, configuration, issues, specs,
   or other project surfaces.

A pointer must say what the referenced material owns and when to read it. If a
reference is missed, strengthen that condition before inlining the material.
Keep a concept's rule, definition, and caveat together once placed.

Split by invocation only when a distinct trigger needs independent discovery or
another skill must reach it directly. Split by sequence only when visible later
steps demonstrably pull the agent into premature completion and a sharper
criterion does not solve it.

## Action Shape

An executable document makes these explicit in proportion to the task:

- objective and current state;
- owner and allowed surface;
- constraints and unresolved decisions;
- ordered actions and their completion criteria;
- evidence that can falsify completion;
- deferred work and stop conditions.

Describe outcomes and decision criteria for open-ended work. Prescribe a fixed
sequence only when deviation has a concrete cost. The first layer must stand
alone for a competent reader who will not read the supporting detail.

## Pruning

Keep each meaning in one owning location. Treat cheaply inspectable code,
configuration, commands, and directory structure as external truth rather than
caching them in prose.

Delete or compress:

- provenance, chronological process narration, session recap, and model or tool
  anecdotes that do not change current action;
- generic quality advice and instructions the target agent already follows;
- duplicated meanings, stale roadmap language, settled proposals, and obsolete
  caveats;
- risks without impact, trigger, owner, or mitigation;
- examples and reference that belong only to an unselected branch.

Prefer positive target behavior. Keep a prohibition only for a costly guardrail
that cannot be expressed safely as a positive, and pair it with what to do.

## Output Modes

Match the authorization:

- **Write or rewrite**: return or apply the improved artifact.
- **Audit**: report evidence and the smallest recommended change; apply it when
  the same request also authorizes updates.
- **Structure**: provide the hierarchy and explain only decisions that change
  reader or agent action.
- **Route**: identify the durable owner, temporary surface, and material to
  delete rather than relocate.

## Completion Check

Before finishing, verify:

- the first screen establishes current state and next action;
- every material finding has a disposition;
- consequential transitions and the requested outcome have checkable completion;
- each pointer names the condition for loading its target;
- fact, inference, recommendation, and open question remain distinguishable;
- every retained meaning has one owner and earns its context or maintenance
  cost;
- completed claims name falsifiable proof when it matters;
- the final artifact or diff was inspected and authorized validation was run.
