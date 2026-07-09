---
description: Delegate a task to Codex via the codex-rescue subagent
argument-hint: "[--background|--wait] [--resume|--fresh] [--model <sol|terra|luna|model>] [--effort <none|minimal|low|medium|high|xhigh|max|ultra>] [what Codex should investigate, solve, or continue]"
allowed-tools: Agent
---

Invoke the `codex:codex-rescue` subagent via the `Agent` tool (`subagent_type: "codex:codex-rescue"`), forwarding the request below as the prompt after handling the command-owned execution flags. It is a subagent, not a skill — do not route it through the Skill tool.

Raw user request:
$ARGUMENTS

Execution mode:

- `--background`: run the subagent in the background. Do not forward this flag.
- `--wait` or no flag: run in the foreground. Do not forward this flag.
- Forward `--resume`, `--fresh`, `--model`, and `--effort` untouched — the subagent owns them.

Return the subagent's output verbatim. Do not paraphrase, summarize, or add commentary. To continue the thread later, use `/codex:rescue --resume <delta instruction>`.

If no task text was given, ask what Codex should investigate or fix.
