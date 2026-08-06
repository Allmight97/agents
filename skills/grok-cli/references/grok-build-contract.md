# Grok Build contract

Last verified: 2026-08-05 against xAI documentation and local Grok Build `0.2.118`.

## Operating model

- Grok Build is an interactive coding agent, a headless CLI, and an ACP server (`grok agent stdio`). Codex does not expose an ACP client or Grok as a native subagent, so invoke it as an external CLI process.
- Use `-m grok-4.5` for the Grok 4.5 model. Headless requests use `-p`; structured results use `--output-format json` or `streaming-json`; `--session-id`, `--resume`, and `--continue` retain session state.
- Headless requests, ACP, and CLI updates can communicate with xAI. Treat a model prompt as external disclosure and potentially billable. Suppress update checks for scripted work with `--no-auto-update`.

Official sources: [overview](https://docs.x.ai/build/overview), [CLI reference](https://docs.x.ai/build/cli/reference), [headless scripting](https://docs.x.ai/build/cli/headless-scripting), and [Grok 4.5](https://docs.x.ai/developers/grok-4-5).

## Permissions, sandbox, and implementation authority

- `dontAsk` denies anything not explicitly allowed, which makes it the default for headless feedback.
- `acceptEdits` auto-approves edits but still prompts for shell commands.
- `--always-approve`, its `--yolo` alias, and `bypassPermissions` auto-approve
  tool calls. The wrapper rejects them.
- Permission rules are not a substitute for scope authorization. Sandboxing is separate from approval and should not be inferred to protect account state, test data, or an intended write target.
- Grok's sandbox is off by default. The wrapper pins `strict`, which limits reads
  to the working directory and system paths, and forces gitignore filtering for
  read/search tools. The model API remains networked. For feedback, make the
  working directory an explicit disclosure bundle rather than the live repo.

Sources: [permissions](https://docs.x.ai/build/features/permissions),
[sandbox](https://docs.x.ai/build/features/sandbox), [settings
reference](https://docs.x.ai/build/settings/reference), and [enterprise
deployment controls](https://docs.x.ai/build/enterprise).

## Discovery isolation

Grok normally discovers user Grok state, plugins, hooks, skills, MCP servers, and Claude/Cursor-compatible sources. Its compatibility cells default on. A dedicated `GROK_HOME` removes normal user Grok state from discovery. The wrapper writes a constrained configuration that disables every documented Claude and Cursor compatibility cell and ignores `~/.agents` skill/command roots.

Repository instructions are intentionally retained when they are physically inside the requested repository. The wrapper rejects all other active instructions and rejects any active plugin, hook, MCP server, external skill, non-built-in agent, or configuration source. Disabled compatibility entries may still appear in `grok inspect --json`; the wrapper treats their explicit disabled state as evidence that they are inactive.

Discovery varies with the machine's active plugin and compatibility state. The
wrapper passed its isolated preflight on this machine on 2026-08-05. It still
fails closed if a Claude marketplace plugin, hook, or other foreign source
appears active; use a separate macOS account or container rather than bypassing
that failure with an allowlist.

Generic `AGENTS.md`/`CLAUDE.md` files placed inside the repository remain part of the task context by design. Put unrelated personal guidance outside the repository and do not bypass a failed preflight.

Source: [settings](https://docs.x.ai/build/settings), [skills/plugins](https://docs.x.ai/build/features/skills-plugins-marketplaces), and [MCP servers](https://docs.x.ai/build/features/mcp-servers).
