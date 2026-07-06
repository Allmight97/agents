# codex

Lean Codex (GPT-5.5) delegation for Claude Code and Fable, wrapping the local `codex` install directly.

Owned here so the surface changes only when we change it and can be disabled independently (`claude plugin disable codex@personal`).

## Surface

- `/codex:rescue [--background|--wait] [--resume|--fresh] [--model <m|spark>] [--effort <e>] <task>` — delegate to the `codex-rescue` subagent, which runs one `codex exec` (write-capable by default, `exec resume --last` for continuations) and returns stdout verbatim.
- `/codex:review [--uncommitted|--base <branch>] [focus]` — thin passthrough to `codex review`, Codex's native non-interactive reviewer.
- `/codex:adversarial-review [--base <branch>] [focus]` — read-only `codex exec` challenge review for assumptions, design risk, and failure modes.
- `/codex:setup` — read-only readiness check for Codex CLI, app-server transfer support, Computer Use MCP wiring, config defaults, and Claude plugin install state.
- `/codex:transfer [--source <claude-jsonl>]` — import the current Claude session into a resumable Codex thread and print `codex resume <session-id>`.
- `gpt-5-5-prompting` skill (internal) — block-structured prompt guidance the subagent uses to tighten forwarded prompts.

Job control uses Claude Code background tasks; continue a rescue thread from a terminal with `codex resume --last`.
For GUI, browser, simulator, or desktop-app work, transfer or resume in the Codex app and use Computer Use there instead of forcing GUI control through `codex exec`.

## Requirements

`codex` CLI on PATH, authenticated (`codex login`); Node.js for `/codex:transfer`; model default comes from `~/.codex/config.toml`.

## Attribution

`skills/gpt-5-5-prompting/` is adapted from [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) (Apache-2.0); see NOTICE and LICENSE-APACHE-2.0.
