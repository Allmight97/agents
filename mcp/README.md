# Local MCP Management

This machine uses `/Users/jstar/.agents` as the shared agent tooling home.

## Source Of Truth

- Shared MCP manifest: `/Users/jstar/.config/mcp/mcp.json`
- Shared MCP and agent secrets: `/Users/jstar/.agents/env/*.env`
- Shared stdio launchers: `/Users/jstar/.agents/bin/*-mcp`

Secrets should live only in env files under `/Users/jstar/.agents/env`.
Client configs should reference wrapper commands or environment variable names,
not raw credential values.

## Current Shared Servers

- `context7`: `/Users/jstar/.agents/bin/context7-mcp`
- `pencil`: `/Users/jstar/.agents/bin/pencil-mcp`
- `codebase-memory-mcp`: `/Users/jstar/.agents/bin/codebase-memory-mcp`

## Client Adapters

- Codex: `/Users/jstar/.codex/config.toml`
- OpenCode: `/Users/jstar/.config/opencode/opencode.json`
- Cursor: `/Users/jstar/.cursor/mcp.json`
- Claude Code: `/Users/jstar/.claude.json`
- Gemini: `/Users/jstar/.gemini/settings.json`
- Pi staged config: `/Users/jstar/.pi/agent/mcp.json`

Cursor, OpenCode, Codex, Claude Code, Gemini, and the staged Pi config use the
local Context7 wrapper. `codebase-memory-mcp` is wired as a local stdio server
across the shared manifest and client adapters; Cursor may still require
explicit approval before loading local stdio MCP servers.

## Maintenance Rule

Edit the shared manifest first, then update client adapters deliberately. Back
up client config before changing it, and validate with each client after edits.
