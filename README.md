# Personal Agent Marketplace

Canonical source for personal skills, Cursor/Claude/Codex marketplace metadata, and
small shared agent configuration. GitHub `main` is the publication source;
agent harnesses consume the published plugins rather than a permanent local
skills checkout.

## Tracked

- `skills/`: personal reusable skills.
- `.cursor-plugin/`: Cursor marketplace/plugin manifests for `personal-skills`.
- `.claude-plugin/`: Claude marketplace/plugin manifests for `personal-skills`.
- `.codex-plugin/`: Codex plugin manifest for `personal-skills`.
- `.agents/plugins/marketplace.json`: Codex marketplace catalog for repo subscribers.
- `plugins/`: separately installable Codex plugins, currently
  `build-apple-apps` and `edge-browser`.
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

## Cursor Marketplace

For distribution testing, this repository can be added as a private Cursor
marketplace and `personal-skills` installed from it. Cursor reads the native
`.cursor-plugin/marketplace.json` and `.cursor-plugin/plugin.json` manifests
while sharing the same root `skills/` tree used by Claude and Codex.

Keep Cursor metadata in `.cursor-plugin/` rather than relying on Cursor's
fallback parsing of Claude manifests. The harness manifests are intentionally
thin wrappers around one shared skill source.

Cursor's personal Git marketplace can remain pinned to its first imported
commit even after update or reinstall. Cursor also rejects a local-plugin
symlink when its target is outside `~/.cursor/plugins/local`. On this Mac, keep
a dedicated Git clone inside Cursor's local-plugin boundary instead:

```bash
git clone https://github.com/Allmight97/agents.git \
  /Users/jstar/.cursor/plugins/local/personal-skills
```

Keep the Git marketplace for distribution testing, but do not treat its cache
as the trusted personal installation. After publishing, the release verifier
fetches and detaches this local clone at the exact release commit, then proves
its clean Git state, `origin/main` commit, and Cursor manifest version. When the
clone advances, the verifier stops with an explicit reload instruction. Run
`Developer: Reload Window` in Cursor, then rerun the verifier; it checks Cursor's
loader log and loaded skill count before reporting success.

## Codex Marketplace

Subscribe Codex to this repo as the `personal` marketplace:

```bash
codex plugin marketplace add Allmight97/agents
```

The Codex marketplace exposes three plugins: `personal-skills`,
`build-apple-apps`, and `edge-browser`.

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

Create a separate plugin only when it needs an independent install or enablement
boundary, permission or authentication surface, runtime dependency, audience, or
release lifecycle. Do not split skills into plugins merely because they share a
topic. Personal workflow skills, including Whittle, belong in `personal-skills`.

`build-apple-apps` keeps one shared nine-skill tree with Codex-native and Agent
Plugins v1 manifests. Xcode 27's file importer recognizes the same skills and
native MCP file. Repository validation keeps its native and portable metadata
and MCP definitions aligned.

`edge-browser` is a separately toggleable routing plugin for controlling
Microsoft Edge through the first-party ChatGPT browser extension. It requires
the official `chrome@openai-bundled` plugin to remain installed and enabled.
Version 0.2.0 adds Edge-specific provider, extension, native-host, and derived
plugin-cache diagnosis. OpenAI officially supports the extension with Google
Chrome, so the Edge route proves its live provider handshake after relevant
updates:

```bash
codex plugin add edge-browser@personal
```

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
3. Synchronize every root `personal-skills` manifest from that changelog
   version. The command also gives Codex a fresh cache-buster and ensures the
   Claude and Cursor marketplace entries remain version-free locators:

   ```bash
   python3 scripts/release_metadata.py set X.Y.Z
   ```

   Give changed nested plugins their own component versions and name them in
   the same changelog section.
4. Validate changed skills plus all three plugin manifests. CI validates every
   root and nested `SKILL.md` against a pinned Agent Skills reference validator.
   Release metadata alignment can be checked locally with:

   ```bash
   python3 scripts/release_metadata.py check
   ```
5. Commit, tag the repository release as `vX.Y.Z`, and push the commit and tag.
6. After the release commit and tag are published, refresh the CLI-supported
   harnesses and prove every installed artifact against that exact release:

   ```bash
   python3 scripts/refresh_harnesses.py
   ```

   Codex and Claude Code are refreshed automatically when their CLIs are
   installed. Cursor's local clone is synchronized against the exact release.
   If it advances, run `Developer: Reload Window` and rerun this command; success
   requires post-refresh loader proof, not marketplace display metadata or
   filesystem state alone.

## Machine-Local Support

`/Users/jstar/.agents` may remain as a non-repository machine-state directory
for paths already used by local clients:

- `env/`: machine-local environment files.
- `bin/`: machine-local executable shims and MCP binaries.

Those directories are not the personal-skill source of truth.
