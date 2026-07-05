---
name: agents-md-steward
description: Maintain AGENTS.md, CLAUDE.md, CODEX.md, and similar repo instruction networks. Use when asked to create, edit, audit, prune, harmonize, compress, or route agent-facing guidance; when guidance files feel bloated, narrative, stale, duplicated, or too generic; when deciding whether a rule belongs in root instructions, nested owner instructions, a skill, a spec, an issue, ordinary docs, or a memory store; or when the user asks to scrutinize opportunities for new instruction files without defaulting to adding more files.
---

# AGENTS.md Steward

## Goal

Keep agent instruction networks concise, current, scoped, and behavior-changing.
Prefer pruning, routing, and clearer ownership over adding another rule.

## Boundary

Do not use this skill for ordinary code edits, test fixes, reviews, or docs
work unless agent-facing instruction files are being created, edited, audited,
or routed.

## First Move

1. Inspect the active instruction surfaces before editing:
   - root `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, or equivalent;
   - nested files that apply to the changed paths;
   - existing skills or scripts that may already own the workflow.
2. Name the intended behavior change in one sentence.
3. Decide the smallest durable home:
   - root instructions for repo-wide invariants;
   - nested instructions for path-local ownership, boundaries, commands, or gotchas;
   - a skill for reusable workflows or conditional procedures;
   - specs/issues/docs for temporary planning, narrative, history, or context.

## Edit Rules

- Use exact owner, path, command, and boundary names. Replace generic quality
  words like "thorough", "detailed", "clean", "robust", or "easy to read" with
  observable checks, or delete the sentence.
- Keep only instructions that change agent behavior. Remove generic advice that
  competent coding agents already know.
- Prefer attractors over long prohibition lists. Use repellors only for common,
  costly failure modes.
- Remove narration, provenance, experiment history, old roadmap language,
  session recap, and model/tool anecdotes from instruction files.
- Keep root instructions short enough to scan. Move local detail down to nested
  instruction files or into skills.
- Do not duplicate the same rule across root, nested files, and skills. Keep the
  broad invariant at root and the operational procedure in the owner surface.
- Do not promote memory or learnings entries into root or nested instruction
  files automatically. Each promotion must pass classification and earn its
  always-loaded cost.
- Do not create a new nested instruction file unless a path has distinct rules
  that future agents cannot reliably infer from code and existing guidance.
- When a refactor, test, command, or owner-local doc would remove the need for a
  rule, prefer that over growing the instruction network.

## Classification

Classify proposed guidance before writing:

| Kind | Home |
| --- | --- |
| Repo-wide invariant | Root instruction file |
| Path ownership, public surface, commands, local gotcha | Nearest nested instruction file |
| Repeatable workflow, decision routing, external reference procedure | Skill |
| Temporary plan, roadmap, implementation state | Spec or issue |
| Historical explanation or rationale | Ordinary docs or decision record, only if durable |
| Durable personal learning or recurring correction, not repo-invariant | Memory store, only with explicit user authorization and dedupe against existing entries |
| Generic advice, recap, agent shorthand, stale process | Delete |

## New File Gate

Suggest a new `AGENTS.md` only when at least one condition holds:

- repeated wrong-path edits or imports show the current network does not route
  agents correctly;
- a subtree has a distinct public surface, command menu, or safety invariant;
- local behavior is non-obvious and expensive to rediscover;
- the rule would be too noisy at root and too important to leave implicit.

If none hold, improve the existing owner file, skill, test, or code boundary.

## Validation

For guidance-only edits, run:

```bash
git diff --check
```

Also run targeted stale-language searches for:

- removed filenames, specs, commands, or modules;
- generic no-op quality words such as "thorough", "detailed", "clean",
  "robust", "easy to read", and "best practices";
- agent shorthand, model names, experiment/provenance terms, and old roadmap
  labels;
- duplicate copies of newly routed rules.

Report what moved, what was deleted, and why the remaining guidance earns its
space.

## References

When shaping or auditing an instruction network, apply the shared principles in
`references/source-principles.md` and these primary sources:

- Claude Code — [Write an effective CLAUDE.md](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md)
- OpenAI Codex — [AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)
- AGENTS.md project — [agents.md](https://agents.md)

Use those sources to keep guidance tactical, project-specific, and free of
generic advice, historical narrative, and behavior attractors that do not match
repo intent.
