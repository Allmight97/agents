---
description: Transfer the current Claude Code session into a resumable Codex thread
argument-hint: "[--source <claude-jsonl>]"
disable-model-invocation: true
allowed-tools: Bash(node:*)
---

Run:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-transfer.mjs" $ARGUMENTS
```

Present the command output exactly as returned. Preserve the Codex session ID and the `codex resume <session-id>` command.

If transfer fails because the transcript path is missing, tell the user to retry with `--source <path-to-claude-jsonl>`.
