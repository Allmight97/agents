---
name: codex-prompting
description: Internal guidance for shaping focused Codex prompts and preserving deliberate model and reasoning choices when Claude forwards coding, review, diagnosis, or research work
user-invocable: false
---

# Codex Prompting

Shape one focused request for Codex without taking over Codex's planning or routing.

## Preserve routing authority

- Preserve an explicit user model and reasoning effort.
- When the user leaves either unspecified, omit its CLI flag. Codex then uses its configured default and retains freedom to route native subagents appropriately.
- Treat `sol`, `terra`, and `luna` as convenience aliases for `gpt-5.6-sol`, `gpt-5.6-terra`, and `gpt-5.6-luna`.

When the user asks for a recommendation:

- Sol fits ambiguous, consequential, long-horizon work; architecture; difficult implementation; planning; and final review.
- Terra fits bounded implementation, source-heavy research, repository exploration, and supporting-agent work where balanced cost and capability matter.
- Luna fits latency-sensitive, repeated, high-volume work such as classification, extraction, simple transformations, and lightweight agents.

Reasoning effort scales with task uncertainty and consequence. Start from the configured default. Raise it for genuinely difficult search, synthesis, or verification. Reserve `max` for rare quality-first tasks; `ultra` is a Codex orchestration setting available only on supported models and is most useful when work divides cleanly across agents.

## Write the task contract

Include only what changes execution:

1. Outcome: the concrete result and finish line.
2. Context: relevant repository, failure, prior decision, or source constraints.
3. Authority: whether Codex should answer, inspect, diagnose, plan, edit, or verify.
4. Evidence: checks or proof that make the result trustworthy.
5. Output: the smallest useful response shape.

Natural prose is the default. Use headings or XML tags when the request has several independent constraints and the structure improves parsing.

## Match behavior to the request

- For implementation, authorize edits and name the required verification.
- For diagnosis, ask for root cause and evidence; leave implementation authority unchanged unless the user requested a fix.
- For review, request material findings ordered by severity and grounded in inspected evidence.
- For research, separate sourced fact, inference, and unresolved questions; prefer current primary sources.
- For a continuation, send the delta instruction and preserve the existing Codex thread context.

Keep the prompt compact. Codex already knows its general workflow, tool use, and coding practices; task-specific context and acceptance criteria carry the useful signal.

## Reference

Use [references/prompt-recipes.md](references/prompt-recipes.md) when a concrete starting shape would help.
