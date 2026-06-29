# Personal Agent Workspace

Private workspace for personal agent skills, Claude/Codex plugin marketplace
metadata, and small shared agent configuration.

## Tracked

- `skills/`: personal reusable skills.
- `.claude-plugin/`: Claude marketplace/plugin manifests for `personal-skills`.
- `.codex-plugin/`: Codex plugin manifest for `personal-skills`.
- `.agents/plugins/marketplace.json`: Codex marketplace catalog for repo subscribers.
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

## Codex Marketplace

Codex subscribes to this repo as the `personal` marketplace:

```bash
codex plugin marketplace add Allmight97/agents
```

Then Codex installs the shared skill tree as the `personal-skills` plugin:

```bash
codex plugin add personal-skills@personal
```

The installed plugin exposes namespaced skills, for example
`personal-skills:diagnose`. Keep direct symlinks from `/Users/jstar/.codex/skills`
disabled once the plugin install is validated, otherwise Codex may see duplicate
skills.

The Codex catalog intentionally lives at `.agents/plugins/marketplace.json`.
That is the path Codex expects inside a Git marketplace checkout. Do not keep a
second root-level `plugins/marketplace.json`; it causes this Mac to see duplicate
`personal` marketplace roots.

Future plugins should be added as their own entries in the Codex marketplace
catalog. Installing `personal-skills` does not install `whittle`, and installing
`whittle` does not install `personal-skills`.

To publish a new shared skill for Codex, edit `skills/<skill-name>/SKILL.md`,
commit, push, refresh the marketplace, and reinstall `personal-skills@personal`:

```bash
codex plugin marketplace upgrade personal
codex plugin add personal-skills@personal
```

The Codex plugin manifest does not need a per-skill edit.

To publish a new plugin, create the plugin, add one marketplace entry for it, and
commit/push. Do not fold separate plugins into `personal-skills`.

## Local Only

- `env/`: machine-local environment files.
- `bin/`: machine-local executable shims and MCP binaries.
