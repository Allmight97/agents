# Personal Agent Workspace

Private workspace for personal agent skills, Claude/Codex plugin marketplace
metadata, and small shared agent configuration.

## Tracked

- `skills/`: personal reusable skills.
- `.claude-plugin/`: Claude marketplace/plugin manifests for `personal-skills`.
- `plugins/marketplace.json`: personal plugin marketplace.
- `mcp/README.md`: local MCP notes.

## Claude Marketplace

Claude Desktop, Cowork, and Claude Code can install the shared skill tree from
the private GitHub repo as the `personal-skills` plugin:

```bash
claude plugin marketplace add Allmight97/agents
claude plugin install personal-skills@personal
```

Plugin skills are namespaced, for example `/personal-skills:diagnose`.

To publish a new skill, add `skills/<skill-name>/SKILL.md`, commit it, push to
`main`, then update or reload the installed plugin. The Claude plugin manifest
does not need a per-skill edit.

Install from GitHub rather than the local `/Users/jstar/.agents` path. Claude's
local-path plugin cache can copy ignored local-only directories such as `env/`
and `bin/`; GitHub installation uses the tracked repo contents only.

## Local Only

- `env/`: machine-local environment files.
- `bin/`: machine-local executable shims and MCP binaries.
