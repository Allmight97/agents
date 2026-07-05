# codex

Lean Codex (GPT-5.5) delegation for Claude Code, wrapping the `codex` CLI directly — no companion runtime, no hooks.

## Why this exists

Replaces `codex@openai-codex` (openai/codex-plugin-cc), which required re-porting local mutations after every vendor update (its prompting guidance targets GPT-5.4 and duplicates the forwarding contract across files). This plugin owns the same core workflow with the naming and structure we actually use, updates only when we change it, and can be disabled independently.

## Surface

- `/codex:rescue [--background|--wait] [--resume|--fresh] [--model <m|spark>] [--effort <e>] <task>` — delegate to the `codex-rescue` subagent, which runs one `codex exec` (write-capable by default, `exec resume --last` for continuations) and returns stdout verbatim.
- `/codex:review [--uncommitted|--base <branch>] [focus]` — thin passthrough to `codex review`, Codex's native non-interactive reviewer.
- `gpt-5-5-prompting` skill (internal) — block-structured prompt guidance the subagent uses to tighten forwarded prompts.

## What the vendor plugin had that this deliberately drops

- Cross-session job store (`/codex:status`, `/codex:result`, `/codex:cancel`) → use Claude Code background tasks and `codex resume` in a terminal.
- `/codex:transfer` → `codex resume --last` / the `codex resume` picker.
- Stop-time review gate hook → never used.
- `/codex:adversarial-review` → pass focus instructions to `/codex:review` instead.

## Requirements

`codex` CLI on PATH, authenticated (`codex login`); model default comes from `~/.codex/config.toml`.

## Attribution

`skills/gpt-5-5-prompting/` is adapted from [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) (Apache-2.0); see NOTICE and LICENSE-APACHE-2.0.
