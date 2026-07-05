---
description: Run Codex's native non-interactive review of local changes
argument-hint: "[--uncommitted|--base <branch>] [focus instructions]"
disable-model-invocation: true
allowed-tools: Bash(codex:*), Bash(git:*)
---

Run Codex's native reviewer and return its output verbatim.

Raw arguments:
$ARGUMENTS

Scope:

- If the arguments include `--uncommitted` or `--base <branch>`, pass them through unchanged.
- Otherwise: use `--uncommitted` when `git status --short` shows changes, else `--base main`.
- Pass any remaining argument text to `codex review` as custom review instructions.

Run:

```bash
codex review <scope flags> "<focus instructions, if any>"
```

Rules:

- Review-only: do not fix issues, apply patches, or suggest you are about to make changes.
- Return stdout verbatim, findings first, ordered by severity as Codex reports them.
- After presenting the findings, stop. Do not change any file unless the user then asks for specific fixes.
