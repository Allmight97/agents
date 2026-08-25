# Instruction Network Mechanics

Read this branch when creating, auditing, pruning, relocating, or routing
repository agent guidance. The shared writing rules remain in
[SKILL.md](SKILL.md).

## Inspect Before Routing

1. Inspect the root and every nested `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, or
   equivalent file that applies to the target path.
2. Inspect existing skills, scripts, tests, code boundaries, specs, issues, and
   decision records that may already own the behavior.
3. Name the intended behavior change in one sentence.
4. Choose the smallest durable owner.

Inspection is complete when every applicable instruction surface and plausible
existing owner has been accounted for; a single-file inspection cannot support
an instruction-network decision.

## Route Each Meaning

| Meaning | Owner |
| --- | --- |
| Repository-wide invariant | Root instruction file |
| Path ownership, public surface, commands, or local trap | Nearest applicable nested instruction file |
| Repeatable workflow, decision procedure, or external-reference process | Skill |
| Temporary plan, roadmap, or implementation state | Issue or active spec |
| Durable rationale that prevents re-litigation | Decision record or ordinary canon |
| Personal learning that is not a repository invariant | Memory, only with explicit user authorization and deduplication |
| Generic advice, recap, stale process, or agent shorthand | Delete |

Keep the broad invariant at the highest applicable owner and operational detail
at the surface that performs it. Do not duplicate the same rule across root,
nested, skill, issue, and memory surfaces.

A durable rule may cite an issue as evidence, but it must state its operative
behavior without depending on mutable issue wording.

## Instruction Rules

- Keep only project-specific guidance that changes agent behavior and cannot be
  inferred cheaply from the environment.
- Use exact owners, paths, commands, public surfaces, and completion checks.
- Prefer positive attractors; reserve explicit repellors for common, costly
  failures and pair them with the intended action.
- Remove provenance, experiment history, session recap, model anecdotes, stale
  roadmap state, and generic quality language.
- Move frequently changing state out of always-loaded instructions.
- Prefer a code boundary, type, test, script, or owner-local documentation fix
  when it removes the need for an instruction.

## New Instruction File Gate

Create a new nested instruction file only when at least one condition holds:

- repeated wrong-path work shows the current network fails to route agents;
- the subtree has a distinct public surface, command menu, or safety invariant;
- local behavior is non-obvious and expensive to rediscover;
- the rule is too noisy at root and too consequential to remain implicit.

If none hold, improve the existing owner, code boundary, test, skill, or script.

## Validation

For guidance-only edits:

1. Run `git diff --check`.
2. Search for removed names, commands, modules, roadmap labels, generic quality
   language, and stale or duplicated copies of rerouted rules.
3. Re-read the active instruction chain for representative target paths.
4. Report what moved, what was deleted, and why the remaining guidance changes
   behavior enough to earn its always-loaded cost.

Validation is complete when the resulting instruction chain is internally
consistent, every moved meaning has one owner, and no stale pointer or duplicate
copy remains in the inspected scope.

Primary references:

- [Claude Code: effective CLAUDE.md](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md)
- [OpenAI Codex: AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)
- [AGENTS.md project](https://agents.md)
