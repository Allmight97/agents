---
name: writing-great-skills
description: Audit and refine existing portable Agent Skills and Codex-specific skill metadata. Use when reviewing skill text, pruning descriptions, deciding what belongs in SKILL.md versus references, or diagnosing invocation, hierarchy, completion, no-op, sediment, sprawl, and predictability failures.
---

# Writing Great Skills

A skill exists to wrangle predictability out of a stochastic system: the same process every run, not the same output every run. Use this as a reference lens when authoring, pruning, or reviewing skills.

For procedural creation mechanics, use `$skill-creator`. This skill owns quality vocabulary and audit judgement. For AGENTS.md and instruction-file networks, use `$agents-md-steward`.

Bold terms are defined in [GLOSSARY.md](GLOSSARY.md). Read that file when you need exact definitions or when auditing a subtle skill-design trade-off.

## Portable Core And Client Extensions

Author shared `SKILL.md` files against the [Agent Skills specification](https://agentskills.io/specification):

- Require `name` and `description`; make `name` match the parent directory and make `description` state both the job and its triggers.
- Use optional `license`, `compatibility`, `metadata`, or experimental `allowed-tools` only when a real consumer or constraint needs them.
- Treat `scripts/`, `references/`, and `assets/` as optional conventions. Create only the resources the skill actually uses.

Keep client policy and presentation outside the portable core. `agents/openai.yaml` is OpenAI-specific UI metadata, not a portable requirement. Put an explicit-only policy or other harness behavior in that harness's supported metadata, then validate it in every target client.

Budget progressive disclosure in tokens: catalog metadata should usually stay near 50-100 tokens, the activated `SKILL.md` body below 5,000 tokens and 500 lines, and supporting resources load only when needed. These are ceilings for context hygiene, not targets to fill.

## Invocation

Two costs govern invocation:

- **Context load**: model-visible descriptions spend tokens and attention every turn.
- **Cognitive load**: explicit-only skills make the human remember when to invoke them.

In this shared skill library, keep `SKILL.md` frontmatter Codex-valid. Do not add `disable-model-invocation` to shared `SKILL.md` files; the current Codex validator rejects unsupported frontmatter. If a target harness supports explicit-only invocation through a harness-specific metadata file, keep that policy outside shared `SKILL.md` and validate every target harness before relying on it.

Default shared strategy: leave skills model-invocable, make descriptions tight, and keep one trigger per branch. Use explicit-only routing only when the target harness can support it without breaking Codex.

## Description

A model-visible description does two jobs: state what the skill does and list the branches that should trigger it. Every word pays context load.

- Front-load a pretrained leading word users already use in prompts, docs, or
  code. Coined labels spend definition tokens and weaken invocation unless the
  skill truly needs new domain language.
- Keep one trigger per branch. Synonyms that rename the same branch are duplication.
- Cut identity that belongs in the body. Keep the description to triggers plus any reach clause another skill needs.
- Avoid long example catalogs. Use representative examples only when they change trigger accuracy.

## Information Hierarchy

Put material where the agent needs it:

1. **In-skill steps**: ordered action in `SKILL.md`; each step needs a checkable completion criterion demanding enough to force the necessary legwork.
2. **In-skill reference**: definitions, rules, or facts every branch needs.
3. **Disclosed reference**: sibling files reached by a clear context pointer.
4. **External reference**: ordinary project files, docs, specs, or source trees outside the skill.

Push too little down and `SKILL.md` sprawls. Push too much down and the agent misses material it actually needs. The context pointer wording decides whether disclosed material is reached reliably.

When a disclosed reference is missed, sharpen its context pointer first. Inline
only material every branch needs or material that a focused retest shows the
repaired pointer still misses consequentially; a buried reference creates
behavioral variance, not merely untidy organization.

## Splitting

Split only when the cut earns one of the costs:

- Split by invocation when a distinct leading word should trigger independently or another skill must reach the material.
- Split by sequence when visible post-completion steps tempt the agent to rush
  the current step. Make the split a real context boundary, such as a fresh
  subagent or new task; new headings inside one loaded skill leave the pull
  intact.
- Keep shared reference in one place when several skills need the same nouns, rules, or taxonomy.

## Pruning

Keep each meaning in a single source of truth. Check every line for relevance, then hunt no-ops sentence by sentence.

Treat the environment as a source of truth too. A skill that restates a command,
version, path, config value, or directory shape that the agent can inspect cheaply
is a **cache**. Keep the lookup in the environment; cache only expensive
discovery, non-obvious ownership, rationale, or a recurring trap.

Delete lines that do not change behavior versus the model default. No-ops are
model-relative. When uncertainty would change a consequential edit, settle it
with a focused forward test instead of debate. Prefer a stronger leading word
over a weak sentence that merely asks the agent to be good.

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
- **Negation**: prohibitions prime the behavior they name. State the positive
  target; reserve a prohibition for a hard guardrail and pair it with what to do
  instead.

## Audit Loop

1. Set the mode, owner, and target clients. An audit reports findings without
   modifying files; an edit patches only the surface the user authorized.
2. Name the skill's job and leading word. Map positive and near-miss trigger
   prompts from its description and client metadata.
3. Inspect the first move and interaction shape. Check that each procedural step
   has a clear completion criterion demanding enough to force the required
   legwork.
4. Classify material as step, in-skill reference, disclosed reference, or
   external reference. Check context pointers and co-locate each meaning with
   its rules and caveats.
5. Find duplication, sediment, sprawl, caches, no-ops, and negation. Resolve
   conflicting guidance against the surface that owns the behavior.
6. In audit mode, report evidence and the smallest recommended patch without
   editing. In edit mode, apply that patch and keep client metadata aligned.
7. Run `skills-ref validate <skill-dir>` for portable structure when available,
   then every target client's validator. Treat structural success as shape proof
   only.
8. Forward-test realistic positive, ambiguous, near-miss, and regression prompts
   when behavior is complex or uncertainty would change a consequential edit.
   In edit mode, inspect the final diff before declaring the skill done.
