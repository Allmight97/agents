# codex

Lean Codex (GPT-5.5) delegation for Claude Code, wrapping the `codex` CLI directly — no runtime scripts, no hooks.

Owned here so the surface changes only when we change it and can be disabled independently (`claude plugin disable codex@personal`).

## Surface

- `/codex:rescue [--background|--wait] [--resume|--fresh] [--model <m|spark>] [--effort <e>] <task>` — delegate to the `codex-rescue` subagent, which runs one `codex exec` (write-capable by default, `exec resume --last` for continuations) and returns stdout verbatim.
- `/codex:review [--uncommitted|--base <branch>] [focus]` — thin passthrough to `codex review`, Codex's native non-interactive reviewer.
- `gpt-5-5-prompting` skill (internal) — block-structured prompt guidance the subagent uses to tighten forwarded prompts.

Job control uses Claude Code background tasks; continue a thread from a terminal with `codex resume --last`.

## Requirements

`codex` CLI on PATH, authenticated (`codex login`); model default comes from `~/.codex/config.toml`.

## Attribution

`skills/gpt-5-5-prompting/` is adapted from [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) (Apache-2.0); see NOTICE and LICENSE-APACHE-2.0.
