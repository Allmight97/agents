---
description: Delegate a task to Codex (GPT-5.5) via the codex-rescue subagent
argument-hint: "[--background|--wait] [--resume|--fresh] [--model <model|spark>] [--effort <none|minimal|low|medium|high|xhigh>] [what Codex should investigate, solve, or continue]"
allowed-tools: Agent
---

Invoke the `codex:codex-rescue` subagent via the `Agent` tool (`subagent_type: "codex:codex-rescue"`), forwarding the raw user request below as the prompt. It is a subagent, not a skill — do not route it through the Skill tool.

Raw user request:
$ARGUMENTS

Execution mode:

- `--background`: run the subagent in the background. Do not forward this flag.
- `--wait` or no flag: run in the foreground. Do not forward this flag.
- Forward `--resume`, `--fresh`, `--model`, and `--effort` untouched — the subagent owns them.

Return the subagent's output verbatim. Do not paraphrase, summarize, or add commentary. To continue the thread later, use `/codex:rescue --resume <delta instruction>`.

If no task text was given, ask what Codex should investigate or fix.
