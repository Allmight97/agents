---
name: gpt-5-5-prompting
description: Internal guidance for composing Codex and GPT-5.5 prompts for coding, review, diagnosis, and research tasks inside the Codex Claude Code plugin
user-invocable: false
---

# GPT-5.5 Prompting

Use this skill when `codex:codex-rescue` needs to ask Codex or another GPT-5.5-based workflow for help.

Prompt Codex like an operator. State the outcome, the output contract, the follow-through default, and the few extra constraints that matter — then let Codex choose the path. GPT-5.5 follows instructions precisely, so a tight contract beats long prose or extra reasoning effort.

## Default recipe

Compose the prompt from XML-tagged blocks. Use stable tag names that match the reference block names so structure stays predictable.

- `<task>`: the concrete job plus the relevant repository or failure context, and what the end state looks like.
- `<structured_output_contract>` or `<compact_output_contract>`: the smallest output shape that still makes the answer easy to use.
- `<default_follow_through_policy>`: what Codex should do by default instead of asking routine questions.
- `<verification_loop>` or `<completeness_contract>`: for debugging, implementation, or risky fixes.
- `<grounding_rules>` or `<citation_rules>`: for review, research, or anything that could drift into unsupported claims.

## When to add blocks

- Coding or debugging: add `completeness_contract`, `verification_loop`, and `missing_context_gating`.
- Review or adversarial review: add `grounding_rules`, `structured_output_contract`, and `dig_deeper_nudge`.
- Research or recommendation: add `research_mode` and `citation_rules`.
- Write-capable tasks: add `action_safety` so Codex stays narrow and avoids unrelated refactors.

## Choosing prompt shape

- Use `codex review` (the `/codex:review` command) when the job is reviewing local git changes — the native reviewer already carries the review contract.
- Use `codex exec` for diagnosis, planning, research, or implementation, where you need direct control of the prompt.
- Use `codex exec resume --last` for follow-ups on the same thread. Send only the delta instruction unless the direction changed materially.

## Working rules

- Prefer one clear task per run; split unrelated asks into separate runs unless they share state that makes a single run cheaper.
- State what done looks like — do not assume Codex will infer the desired end state.
- Add grounding and verification blocks for any task where an unsupported guess would hurt quality.
- Tighten the prompt contract before raising reasoning effort or switching model.
- Anchor claims to observed evidence; label hypotheses as hypotheses.
- Ask for brief, outcome-based progress only on long-running or tool-heavy runs.
- Prune redundant instructions before sending.

## References

- Reusable blocks: [references/prompt-blocks.md](references/prompt-blocks.md)
- End-to-end templates: [references/codex-prompt-recipes.md](references/codex-prompt-recipes.md)
- Failure modes to avoid: [references/codex-prompt-antipatterns.md](references/codex-prompt-antipatterns.md)
