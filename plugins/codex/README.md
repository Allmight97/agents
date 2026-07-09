# codex

Lean Codex delegation for Claude Code and Fable, wrapping the local `codex` install directly.

Owned here so the surface changes only when we change it and can be disabled independently (`claude plugin disable codex@personal`).

## Surface

- `/codex:rescue [--background|--wait] [--resume|--fresh] [--model <sol|terra|luna|model>] [--effort <e>] <task>` — intentionally delegate to the `codex-rescue` subagent, which runs one `codex exec` (write-capable by default, `exec resume --last` for continuations) and returns stdout verbatim. Model and effort inherit Codex configuration unless supplied.
- `/codex:review [--uncommitted|--base <branch>] [focus]` — thin passthrough to `codex review`, Codex's native non-interactive reviewer.
- `/codex:adversarial-review [--base <branch>] [focus]` — read-only `codex exec` challenge review for assumptions, design risk, and failure modes.
- `/codex:setup` — read-only readiness check for Codex CLI, app-server transfer support, Computer Use MCP wiring, config defaults, and Claude plugin install state.
- `/codex:transfer [--source <claude-jsonl>]` — import the current Claude session into a resumable Codex thread and print `codex resume <session-id>`.
- `codex-prompting` skill (internal) — outcome-focused prompt and routing guidance for forwarded tasks.

Job control uses Claude Code background tasks; continue a rescue thread from a terminal with `codex resume --last`.
For GUI, browser, simulator, or desktop-app work, transfer or resume in the Codex app and use Computer Use there instead of forcing GUI control through `codex exec`.

## Requirements

`codex` CLI on PATH, authenticated (`codex login`); Node.js for `/codex:transfer`; model default comes from `~/.codex/config.toml`.

## Attribution

`skills/codex-prompting/` is adapted from [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) (Apache-2.0); see NOTICE and LICENSE-APACHE-2.0.
