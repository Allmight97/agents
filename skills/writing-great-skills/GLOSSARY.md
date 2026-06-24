# Glossary - Building Great Skills

The domain model for making skills predictable. A skill should make the agent behave the same way every run, even when the output changes.

## Language

### Predictability

The degree to which a skill makes the agent follow the same process every run. Predictability is not output determinism; a brainstorming skill should predictably diverge.

Avoid: consistency, reliability, robustness, output-determinism.

### Model-Invoked

A skill whose description is visible to the model, so the agent can invoke it autonomously and other skills can reach it. It pays context load every turn.

In Codex-compatible shared skills, this is the default because `description` is required. Control context load by pruning descriptions unless the target harness has a validated, non-`SKILL.md` policy for explicit-only invocation.

Avoid: ability, tool, capability.

### User-Invoked

A skill meant to be reached only by the human typing its name. It trades context load for cognitive load. In shared Codex-visible `SKILL.md` files, do not implement this by adding unsupported frontmatter such as `disable-model-invocation`.

Avoid: procedure, workflow, command.

### Description

The model-visible trigger and the highest-rank context pointer for a model-invoked skill. It should say what the skill does and name the distinct branches that should trigger it.

Avoid: frontmatter, summary.

### Context Pointer

A phrase in loaded context that tells the agent when to reach for unloaded material. The wording, not the target path, decides whether the agent reaches the material reliably.

Avoid: link, reference, import.

### Context Load

The token and attention cost imposed by model-visible descriptions and inlined skill material.

Avoid: token cost, context bloat.

### Cognitive Load

The cost a human pays to remember which explicit skills exist and when to invoke them. A router skill can reduce this when explicit-only skills multiply.

Avoid: human index, burden, overhead.

### Router Skill

A user-invoked skill whose job is to point the human at the right explicit skill. It helps memory; it does not magically invoke skills that are invisible to the model.

Avoid: dispatcher, menu, registry, index.

### Information Hierarchy

The ranking of skill material by how immediately the agent needs it:

- steps in `SKILL.md`,
- reference in `SKILL.md`,
- disclosed reference behind a context pointer,
- external reference outside the skill.

Avoid: structure, organization, layout.

### Co-location

Keeping a concept's definition, rules, and caveats together so reading one part brings the neighboring facts with it.

Avoid: grouping, clustering, cohesion.

### Branch

A distinct way a skill can be invoked or used. Different branches need different steps or reference.

Avoid: path, case, fork.

### Progressive Disclosure

Moving reference down the information hierarchy behind a context pointer so `SKILL.md` stays legible. Disclose what only some branches need; inline what every branch must have.

Avoid: lazy loading, chunking.

### Steps

Ordered actions the agent performs. Every step needs a completion criterion.

Avoid: workflow, instructions, choreography.

### Completion Criterion

The condition that tells the agent a step is done. Strong criteria are checkable and demanding enough to force the necessary legwork.

Avoid: done condition, exit condition, stopping rule.

### Post-Completion Steps

The steps that follow the current step. When too visible, they can pull the agent into premature completion.

Avoid: horizon, lookahead.

### Legwork

The work an agent does inside a step: reading, searching, testing, inspecting artifacts, and proving claims rather than asking the user for facts the environment can answer.

Avoid: scope, effort, diligence, coverage.

### Reference

Material the agent consults on demand: definitions, facts, parameters, examples, conditionals, and policies.

Avoid: supporting material, docs, background.

### External Reference

Reference that lives outside the skill system: repo docs, source files, specs, issue text, manuals, or ordinary project artifacts.

Avoid: doc, resource, knowledge base.

### Leading Word

A compact concept already living in the model's prior knowledge that anchors behavior in few tokens. Use leading words in descriptions and bodies when they improve invocation or execution.

Avoid: keyword, term, motif.

### Single Source of Truth

The state where each meaning has exactly one authoritative home. Duplication violates it.

Avoid: home, canonical location.

### Relevance

Whether a line still bears on what the skill does. Relevant lines can still be no-ops.

Avoid: load-bearing, staleness, freshness.

## Failure Modes

### Premature Completion

Ending the current step before it is genuinely done. Defend first by sharpening the completion criterion, then by splitting sequence only when the rush is observed and cannot be solved locally.

Avoid: premature closure, rushing, shortcutting.

### Duplication

The same meaning appears in more than one place. It costs maintenance, spends tokens, and overweights the idea.

Avoid: repetition, redundancy.

### Sediment

Old material that remains because adding feels safe and removing feels risky. Sediment makes the live instruction harder to find.

Avoid: accretion, bloat, cruft, rot.

### Sprawl

A skill is too long even if the lines are live and unique. Use progressive disclosure or split by branch/sequence.

Avoid: length, size, verbosity.

### No-Op

An instruction that changes nothing relative to default model behavior. Delete it or replace it with a stronger leading word that changes behavior.

Avoid: redundant instruction, restating the obvious.
