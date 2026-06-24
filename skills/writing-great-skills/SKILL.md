---
name: writing-great-skills
description: Reference for writing, editing, and auditing Codex-compatible skills. Use when creating or refining skill text, pruning descriptions, deciding what belongs in SKILL.md versus references, diagnosing skill failure modes, or when another skill needs quality vocabulary for invocation, hierarchy, no-ops, sediment, sprawl, and predictable behavior.
---

# Writing Great Skills

A skill exists to wrangle predictability out of a stochastic system: the same process every run, not the same output every run. Use this as a reference lens when authoring, pruning, or reviewing skills.

For procedural creation mechanics, use `$skill-creator`. This skill owns quality vocabulary and audit judgement. For AGENTS.md and instruction-file networks, use `$agents-md-steward`.

Bold terms are defined in [GLOSSARY.md](GLOSSARY.md). Read that file when you need exact definitions or when auditing a subtle skill-design trade-off.

## Invocation

Two costs govern invocation:

- **Context load**: model-visible descriptions spend tokens and attention every turn.
- **Cognitive load**: explicit-only skills make the human remember when to invoke them.

In this shared skill library, keep `SKILL.md` frontmatter Codex-valid. Do not add `disable-model-invocation` to shared `SKILL.md` files; Codex rejects unsupported frontmatter and the skill fails to load. If a target harness supports explicit-only invocation through a harness-specific metadata file, keep that policy outside shared `SKILL.md` and validate every target harness before relying on it.

Default shared strategy: leave skills model-invocable, make descriptions tight, and keep one trigger per branch. Use explicit-only routing only when the target harness can support it without breaking Codex.

## Description

A model-visible description does two jobs: state what the skill does and list the branches that should trigger it. Every word pays context load.

- Front-load the skill's leading word.
- Keep one trigger per branch. Synonyms that rename the same branch are duplication.
- Cut identity that belongs in the body. Keep the description to triggers plus any reach clause another skill needs.
- Avoid long example catalogs. Use representative examples only when they change trigger accuracy.

## Information Hierarchy

Put material where the agent needs it:

1. **In-skill steps**: ordered action in `SKILL.md`; each step needs a checkable completion criterion.
2. **In-skill reference**: definitions, rules, or facts every branch needs.
3. **Disclosed reference**: sibling files reached by a clear context pointer.
4. **External reference**: ordinary project files, docs, specs, or source trees outside the skill.

Push too little down and `SKILL.md` sprawls. Push too much down and the agent misses material it actually needs. The context pointer wording decides whether disclosed material is reached reliably.

## Splitting

Split only when the cut earns one of the costs:

- Split by invocation when a distinct leading word should trigger independently or another skill must reach the material.
- Split by sequence when visible post-completion steps tempt the agent to rush the current step.
- Keep shared reference in one place when several skills need the same nouns, rules, or taxonomy.

## Pruning

Keep each meaning in a single source of truth. Check every line for relevance, then hunt no-ops sentence by sentence.

Delete lines that do not change behavior versus the model default. Prefer a stronger leading word over a weak sentence that merely asks the agent to be good.

Do not add license files, copyright notices, or licensing narration to skills
merely because their guidance was adapted from another skill. Skills are
instruction prose, not bundled runtime source, unless the user explicitly asks
for provenance or license handling.

## Failure Modes

- **Premature completion**: the agent ends a step before the completion criterion is truly met. Sharpen the criterion first; split sequence only when the criterion cannot get sharper and the rush is observed.
- **Duplication**: the same meaning lives in more than one place. Collapse it to the owning surface.
- **Sediment**: stale layers remain because adding feels safer than removing. Delete stale lines instead of adding compensating text.
- **Sprawl**: `SKILL.md` is too long even when live and unique. Use the information hierarchy.
- **No-op**: a line changes nothing relative to default model behavior. Delete or replace with a stronger leading word.

## Audit Loop

1. Name the skill's job and leading word.
2. Identify its trigger branches from the description.
3. Classify each body section as step, reference, disclosed reference, or external reference.
4. Find duplication, sediment, sprawl, and no-ops.
5. Patch the smallest surface that improves predictability.
6. Validate with `quick_validate.py`; forward-test with realistic prompts when behavior is complex.
