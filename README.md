# Personal Agent Marketplace

Canonical source for personal skills, Cursor/Claude/Codex marketplace metadata, and
small shared agent configuration. A GitHub Release is the immutable publication
record; `main` supplies marketplace refreshes. Agent harnesses consume published
plugins rather than an authoring checkout.

## Tracked

- `skills/`: personal reusable skills.
- `.cursor-plugin/`: Cursor marketplace/plugin manifests for `personal-skills`.
- `.claude-plugin/`: Claude marketplace/plugin manifests for `personal-skills`.
- `.codex-plugin/`: Codex plugin manifest for `personal-skills`.
- `.agents/plugins/marketplace.json`: Codex marketplace catalog for repo subscribers.
- `plugins/`: separately installable plugins and their owned runtimes. In addition to the Codex
  plugins, `oura-mcp` is a hosted Streamable HTTP service for a private ChatGPT MCP connection.
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

Cursor's personal Git marketplace can remain pinned to an earlier imported
commit. On this Mac, the GitHub user marketplace is the installed owner; do not
add a competing local-plugin clone. After publishing, remove and reimport the
marketplace when an ordinary reload does not advance it, reinstall Personal
Skills, run `Developer: Reload Window`, and rerun the release verifier. The
verifier requires the exact release commit and manifest version from Cursor's
marketplace cache rather than trusting the marketplace card.

### Cursor Cloud and Grok Bot

Do not infer cloud availability from Cursor's local plugin cache. Cursor
Cloud runs in an isolated VM and cannot read this Mac's `~/.cursor` state.
Grok Bot's current official documentation describes account-saved cloud skills
and per-Bot enablement; it does not establish Cursor marketplace ingestion or
plugin-version parity.

The preferred distribution owner is a private Cursor Team Marketplace with
GitHub auto-refresh: publish this repository, make `personal-skills` Default On
or Required, and smoke-test one release-specific skill in Cursor Cloud and Grok
Bot. Repository-owned ABB skills remain under ABB's `.agents/skills`; they are
project guidance, not a substitute for the personal plugin.

When the Cursor account has no Team Marketplace entitlement, there is no native
automatic path shared by Cursor local, Cursor Cloud, and Grok Bot. Do not copy
the skill tree into each product and call it synchronized. Keep this repository
canonical, use a version-pinned cloud environment adapter only where necessary,
and record Cloud and Bot proof separately for every release.

## Codex Marketplace

Subscribe Codex to this repo as the `personal` marketplace:

```bash
codex plugin marketplace add Allmight97/agents
```

The Codex marketplace exposes four plugins: `personal-skills`,
`build-apple-apps`, `native-browser-bridge`, and `m365-tenant-ops`.

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

`native-browser-bridge` is a separately toggleable selector for controlling an
explicitly named Microsoft Edge or Brave instance through the native ChatGPT
browser-extension bridge. It requires the official `chrome@openai-bundled`
plugin to remain installed and enabled. Invoke the bridge and name the browser;
it preserves that browser instead of silently substituting Chrome, Computer
Use, or macOS Accessibility:

```bash
codex plugin add native-browser-bridge@personal
```

`m365-tenant-ops` is a separately installable Agent Plugins v1 package for
bounded Microsoft Entra and Microsoft 365 tenant operations. Its first skill,
`audit-entra`, keeps delegated Graph and admin-portal investigations read-only
until exact mutations are collected for review:

```bash
codex plugin add m365-tenant-ops@personal
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
   Then create the GitHub Release object; a pushed tag alone is not a formal
   repository release:

   ```bash
   gh release create vX.Y.Z --verify-tag --title "Personal Skills X.Y.Z" \
     --notes-from-tag
   ```

6. After the GitHub Release is published, refresh the locally verifiable
   harnesses and prove every installed artifact against that exact release:

   ```bash
   python3 scripts/refresh_harnesses.py
   ```

   Codex and Claude Code are refreshed automatically when their CLIs are
   installed. Cursor's Git marketplace may require removal and reimport before
   it exposes the new commit. Run `Developer: Reload Window` after reinstalling,
   then rerun this command; success requires exact cached release proof, not
   marketplace display metadata alone.
7. Verify the remote consumers independently. A local success does not prove
   either cloud surface:
   - Cursor Cloud: invoke a skill changed in this release and retain the run URL.
   - Grok Bot: enable the account-saved skill for the Bot and retain a successful
     `/` invocation task URL. Do not infer personal-plugin version parity.

## Machine-Local Support

`/Users/jstar/.agents` may remain as a non-repository machine-state directory
for paths already used by local clients:

- `env/`: machine-local environment files.
- `bin/`: machine-local executable shims and MCP binaries.

Those directories are not the personal-skill source of truth.
