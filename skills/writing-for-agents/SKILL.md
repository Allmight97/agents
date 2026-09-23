---
name: writing-for-agents
description: Write or audit agent-consumed guidance, including skills, repository instructions, issues, and handoffs. Use when instruction clarity, placement, or execution scope is the task.
---

# Writing for Agents

Give the next agent the context and decision criteria it needs to complete the
requested work. Retain instructions that change a decision, preserve a
non-obvious constraint, or express a real user preference. Scale the document
to its job; routine edits do not need a new process.

## Establish the job

Infer the audience, intended outcome, durable owner, and edit authority from
the whole request. Inspect the target and the sources needed to support claims
that change the next action. An audit alone reports findings; an audit with
authorized fixes continues through those fixes and their relevant checks.

Read branch guidance when the requested change needs it:

- [Skill mechanics](SKILL-MECHANICS.md) for skill triggers, structure,
  client metadata, or behavioral validation.
- [Instruction networks](INSTRUCTION-NETWORK-MECHANICS.md) for repository
  instructions, global guidance, or deciding where a rule belongs.

For an issue, spec, or handoff, use the shared guidance here. Use
[visual-brief](../visual-brief/SKILL.md) when substantial material needs a
visual orientation; keep its execution requirements with their existing owner.

## Write the useful difference

Lead with current state and the outcome or next decision. Include scope,
constraints, unresolved choices, and completion evidence where they affect
execution. Distinguish facts, proposals, and unverified claims. Mixed
human-agent documents must make the human decision understandable while
keeping execution requirements explicit.

Keep each rule with one owner. Reference code, configuration, or other live
sources for facts they own. Keep shared instructions in the entrypoint and
substantial conditional material behind a pointer that says when to load it.
Create another file or skill only when separate discovery or use earns it.

Describe outcomes and decision criteria. Prescribe an order only when it
prevents a concrete failure. Keep approval boundaries tied to the action and
existing authority, and make completion include the requested implementation
and verification when both are in scope.

Remove duplicate meanings, stale state, process narration, and generic advice
already supplied by the environment. Prefer the intended behavior; retain a
prohibition when it protects a specific costly boundary. After a decision,
rewrite around the new state rather than appending history.

## Finish

Inspect the final artifact or diff for missing requirements, conflicting rules,
and stale pointers. Use validation appropriate to the changed surface.
An audit connects each material finding to evidence and a proposed disposition;
an edit reports the change and the checks actually performed. Claim behavioral
improvement only when observed, and label untested effects as hypotheses.
