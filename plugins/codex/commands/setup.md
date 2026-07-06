---
description: Check whether the local Codex bridge is ready for Claude/Fable routing
argument-hint: ""
disable-model-invocation: true
allowed-tools: Bash(codex:*), Bash(claude:*), Bash(grep:*)
---

Run a read-only readiness check for the personal Codex bridge. Do not install, update, enable, disable, or toggle anything.

Run these checks:

```bash
codex --version
codex app-server --help
codex mcp get computer-use
grep -E '^(model|model_reasoning_effort)[[:space:]]*=' "$HOME/.codex/config.toml"
claude plugin list
```

Report a compact readiness summary with:

- Codex CLI: ready or not ready, including version if available.
- App-server transfer support: ready or not ready.
- Computer Use wiring: ready or not ready.
- Codex defaults: model and reasoning effort from `~/.codex/config.toml` when present.
- Claude plugin: whether `codex@personal` is installed and enabled.
- Next action: the single most useful fix if anything is missing.

Do not mention the optional upstream review gate.
