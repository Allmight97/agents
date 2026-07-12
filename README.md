# Personal Agent Marketplace

Canonical source for personal skills, Claude/Codex marketplace metadata, and
small shared agent configuration. GitHub `main` is the publication source;
agent harnesses consume the published plugins rather than a permanent local
skills checkout.

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

To publish a new skill or revision, follow the repository release workflow
below, then update or reload the installed plugin.

Install from GitHub rather than the local `/Users/jstar/.agents` path. Claude's
local-path plugin cache can copy ignored local-only directories such as `env/`
and `bin/`; GitHub installation uses the tracked repo contents only.

## Codex Marketplace

Subscribe Codex to this repo as the `personal` marketplace:

```bash
codex plugin marketplace add Allmight97/agents
```

Then install the shared skill tree as the `personal-skills` plugin:

```bash
codex plugin add personal-skills@personal
```

The plugin exposes namespaced skills, for example `personal-skills:diagnose`.
Do not keep a checkout at `/Users/jstar/.agents/skills`: Codex discovers that as
a user-scope skill root, which duplicates the marketplace plugin. A local
working clone used to author a change belongs in an ordinary project or
temporary work directory and can be removed after publication.

The Codex catalog intentionally lives at `.agents/plugins/marketplace.json`.
That is the path Codex expects inside a Git marketplace checkout. Do not keep a
second root-level `plugins/marketplace.json`; it causes this Mac to see duplicate
`personal` marketplace roots.

Future plugins should be added as their own entries in the Codex marketplace
catalog only when they are genuinely separate products. Personal workflow skills,
including Whittle, belong in `personal-skills`.

After publishing a repository release, refresh the existing marketplace and
install or update `personal-skills@personal`:

```bash
codex plugin marketplace upgrade personal
codex plugin add personal-skills@personal
```

To publish a new plugin, create the plugin, add one marketplace entry for it, and
include its version in the repository release. Do not split ordinary personal
skills out of `personal-skills`.

## Release Workflow

One completed revision pass becomes one repository release. Follow the version
rules at the top of `CHANGELOG.md`:

1. Make the bounded skill, plugin, or repository changes.
2. Move the net released changes from `[Unreleased]` into a dated version
   section; omit intermediate churn and unchanged surfaces.
3. Synchronize the root Claude and Codex `personal-skills` base versions. Give
   changed nested plugins their own component versions and name them in the same
   changelog section.
4. Validate changed skills plus both plugin manifests.
5. Commit, tag the repository release as `vX.Y.Z`, and push the commit and tag.
6. Refresh the existing marketplaces and update installed plugins in each
   harness.

## Machine-Local Support

`/Users/jstar/.agents` may remain as a non-repository machine-state directory
for paths already used by local clients:

- `env/`: machine-local environment files.
- `bin/`: machine-local executable shims and MCP binaries.

Those directories are not the personal-skill source of truth.
