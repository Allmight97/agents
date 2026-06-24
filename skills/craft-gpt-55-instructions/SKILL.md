---
name: craft-gpt-55-instructions
description: Craft GPT-5.5-focused instructions, system prompts, task prompts, and agent guidance when model-specific wording, stop rules, validation criteria, ambiguity policy, or loading-surface placement affects behavior. Use for reducing compliance theater, over-literal rules, provenance-heavy narration, or fragile prompt structure; use `$writing-great-skills` for skill architecture and `$agents-md-steward` for AGENTS.md/CLAUDE.md network ownership.
---

# Craft GPT-5.5 Instructions

GPT-5.5 follows instructions precisely: vague or contradictory guidance hurts reasoning, and over-specified process adds noise, narrows the search space, and produces mechanical answers. This skill distills the source guidance into craft rules for instructions that improve judgment without becoming a cage.

For the source excerpts and URLs behind each rule, read `references/sources.md` when a specific decision needs grounding.

## Boundary

Use this for GPT-5.5/Codex wording choices: outcome shape, rule strength,
ambiguity policy, validation criteria, stop rules, and loading-surface tradeoffs.
For skill invocation, splitting, references, no-ops, and failure modes, use
`$writing-great-skills`. For AGENTS.md/CLAUDE.md networks, owner routing, and
nested guidance placement, use `$agents-md-steward`.

## Shape the instruction

Define the outcome, not the procedure. Describe what good looks like, the constraints that matter, the evidence available, and what the final answer must contain. Let the model choose the path. Reserve step-by-step procedure for genuinely fragile sequences.

Prefer decision rules over absolutes for judgment calls. Use `ALWAYS`, `NEVER`, `must`, and `only` for true invariants: safety, required output fields, forbidden actions. For judgment calls (when to search, ask, iterate, use a tool, stop), write rules with escape clauses: "Do X unless Y." A rule without an escape clause becomes a brittle absolute that invites compliance theater.

One rule per line when the triggers differ. Line-separated rules get independent attention slots and fire on the right trigger; sentences collapsed into a run-on get averaged into a vague stance, and the middle clause loses weight. Facets of one stance (e.g., several bullets about prose economy) may share a paragraph. Token cost is trivial; signal cost of blurring distinct triggers is not.

For complex prompts, use the suggested structure and add detail only where it changes behavior:

```
Role: [1-2 sentences defining function, context, and job]
# Personality
[tone, demeanor, collaboration style — keep short]
# Goal
[user-visible outcome]
# Success criteria
[what must be true before the final answer]
# Constraints
[policy, safety, business, evidence, side-effect limits]
# Output
[sections, length, tone]
# Stop rules
[when to retry, fallback, abstain, ask, or stop]
```

## Steer Judgment

Lead with the strongest useful claim. Then give only the evidence, implication, and action needed for the reader to move.

Use domain-neutral vocabulary unless the domain is the point. Words like "engineering," "repo," or "machine" anchor the model toward that framing even for unrelated asks. Drop domain anchors when guidance should apply broadly; keep them when the instruction is domain-scoped.

Set an ambiguity policy. Default: proceed with a stated assumption when the path is reversible and low-risk; ask only when missing information would materially change the outcome or create risk. Without this, GPT-5.5 can default to over-asking or over-assuming.

Mark temporary approaches as temporary. This is the anti-compliance-theater guardrail: it prevents a workaround from being silently delivered as a final resolution.

Name the check the model can run: targeted tests, type/lint/build checks, a smoke test, or a rendered-output inspection. If validation cannot run, require explaining why and naming the next best check. "Looks done" is not a signal.

## Keep it lean

Apply the cut test to every line of an always-loaded file: "Would removing this cause mistakes?" If not, cut it. Bloated always-loaded files cause the model to lose important rules in noise.

Keep always-loaded files short and human-readable. Include only broadly applicable context the model cannot infer from code, docs, or environment.

Do not narrate provenance, process, compliance, or tool usage unless it changes a decision, reduces future risk, satisfies an explicit requirement, or prevents likely misunderstanding. This applies to the instructions themselves: do not write process narration into the file.

For no-op and sediment pruning, apply `$writing-great-skills`: if a line matches the model default, delete it or replace it with a stronger leading word that changes behavior.

## Layer by scope

Global guidance is persistent defaults. Project and local files layer after global and override by proximity. Write global guidance to hold across all projects; push project-specific commands, gotchas, and conventions into local files.

Right-size the loading surface:

- **Always-loaded** (AGENTS.md, CLAUDE.md): persistent defaults the model cannot infer — commands, non-obvious conventions, hard invariants.
- **Skills**: conditional workflows and domain knowledge loaded on demand. Use for material that applies only sometimes.
- **References**: detailed documentation loaded only when a specific decision needs it. Keep SKILL.md lean; push schemas, long examples, and source excerpts here.

## Revision loop

1. Name the instruction's job and loading surface.
2. Classify each line: outcome, hard invariant, decision rule, validation, stop rule, or no-op.
3. Delete no-ops and route skill/network structure questions to the owning skill.
4. Check for contradictions and ambiguity. GPT-5.5 follows instructions precisely; conflicting rules degrade reasoning.
5. Confirm hard invariants use absolutes and judgment calls use decision rules with escape clauses.
6. Verify one-rule-per-line where triggers differ.
7. Forward-test with a realistic prompt when behavior is complex or taste-sensitive.

## Sources

Grounded in four primary sources. Read `references/sources.md` for excerpts and URLs:

- OpenAI GPT-5.5 prompt guidance — outcome-first prompts, decision rules over absolutes, stop rules, prompt structure.
- OpenAI Codex AGENTS.md guide — global-before-project, override by proximity, persistent defaults.
- Claude Code CLAUDE.md best practices — short and human-readable, cut test, skills for conditional workflows.
- agents.md format — project instructions, commands, testing, gotchas, nested local guidance.
