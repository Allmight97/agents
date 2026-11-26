# Skill Mechanics

Use when the document is a skill: invocation, router skills, client metadata,
and behavioral proof. Shared writing guidance lives in [SKILL.md](SKILL.md).

## Invocation

The choice trades the two loads.

- **Model-invoked:** the description stays in context, so the agent can load
  the skill by itself and the user can still call it by name. It costs context
  load on every turn. A skill of pure reference that several skills need can
  live here as one shared owner.
- **User-invoked** (`disable-model-invocation: true`): only the human can start
  it, and the skill tool refuses it to other skills. Zero context load; the
  human is the index and must remember it exists. Another skill can still read
  it by file path. Claude Code documents the flag; claude.ai does not, and its
  standalone skill uploads reject frontmatter keys outside the Agent Skills
  specification.

Make a skill model-invoked by default. Make it user-invoked only for a real
risk: a description long enough to crowd the skill listing, or a skill that
would trigger unasked in ordinary work. Put an action's sensitivity in its
permission boundary, not in the invocation choice alone.

Split off a model-invoked skill only when a distinct leading word should
trigger it on its own, or another skill must load it through the skill tool.
The new description must earn its always-on cost.

## Router skills

When user-invoked skills pile up past what the owner remembers, give them one
router: a user-invoked skill that names the others and when to reach for each.
The owner remembers one name instead of many. A router can only point; it
cannot start a user-invoked skill.

## Descriptions

A description is the skill's pointer; the pointer rules in
[SKILL.md](SKILL.md) apply in full. Name the capability and the task that needs
it. Add an exclusion only when it prevents a plausible misroute, and check
neighbouring descriptions whose jobs overlap. A user-invoked skill's
description is for the human: one line on what calling it gets them.

## Portability

Keep each skill valid against the
[Agent Skills specification](https://agentskills.io/specification): directory
and name agree, and every metadata key is one its consumer supports. Codex
policy belongs in `agents/openai.yaml`; preserve unrelated settings there.
Verify client-specific behavior for the clients a change affects; a body edit
does not require proving every distribution channel again.

Do not drop a guardrail on the assumption that one model no longer needs it;
consider every model and client the skill serves.

## Behavioral proof

Structural validity proves packaging, not behavior. When a routing or workflow
change carries consequential uncertainty, compare realistic tasks under the
current and proposed guidance: one task that should trigger it, a nearby task
that should not, and any known regression. Run without the skill as well when
its added value is the question. Compare task quality, needless reads or
questions, and whether the work finishes; word count cannot decide it.

Use independent trials only when delegation is authorized and the evidence
earns the cost. Give the evaluator the request and the minimum raw artifacts,
not the preferred answer. Keep trial output outside the source tree. Report
what was observed and what remains uncertain.
