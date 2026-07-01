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

Plugin skills are namespaced, for example `/personal-skills:diagnose` and
`/personal-skills:whittle`. Whittle lives in this shared skill tree, not as a
separate plugin.

To publish a new skill, add `skills/<skill-name>/SKILL.md`, commit it, push to
`main`, then update or reload the installed plugin. The Claude plugin manifest
does not need a per-skill edit.

Install from GitHub rather than the local `/Users/jstar/.agents` path. Claude's
local-path plugin cache can copy ignored local-only directories such as `env/`
and `bin/`; GitHub installation uses the tracked repo contents only.

## Codex Skill Source

On this development Mac, Codex reads the local clone directly because
`/Users/jstar/.agents/skills` is the documented user-scope skill root. Do not
also install `personal-skills@personal` in Codex here; that creates duplicate
skills from the local tree and the plugin cache.

For a fresh machine without the `/Users/jstar/.agents` clone, Codex can subscribe
to this repo as the `personal` marketplace:

```bash
codex plugin marketplace add Allmight97/agents
```

Then install the shared skill tree as the `personal-skills` plugin:

```bash
codex plugin add personal-skills@personal
```

The plugin exposes namespaced skills, for example `personal-skills:diagnose`.
Use either the local user-scope tree or the plugin install, not both. Codex does
not merge duplicate skill names across roots.

The Codex catalog intentionally lives at `.agents/plugins/marketplace.json`.
That is the path Codex expects inside a Git marketplace checkout. Do not keep a
second root-level `plugins/marketplace.json`; it causes this Mac to see duplicate
`personal` marketplace roots.

Future plugins should be added as their own entries in the Codex marketplace
catalog only when they are genuinely separate products. Personal workflow skills,
including Whittle, belong in `personal-skills`.

To publish a new shared skill for Codex, edit `skills/<skill-name>/SKILL.md`,
commit, and push. On machines using the plugin path, refresh the marketplace and
reinstall `personal-skills@personal`:

```bash
codex plugin marketplace upgrade personal
codex plugin add personal-skills@personal
```

The Codex plugin manifest does not need a per-skill edit.

To publish a new plugin, create the plugin, add one marketplace entry for it, and
commit/push. Do not split ordinary personal skills out of `personal-skills`.

## Local Only

- `env/`: machine-local environment files.
- `bin/`: machine-local executable shims and MCP binaries.
