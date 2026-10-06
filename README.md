# Personal Agent Marketplace

One marketplace repository for Claude Code, Claude Desktop, claude.ai, Codex,
Cursor, and Grok Build. The root holds one catalog per harness; every plugin is
a folder under `plugins/`; each catalog lists only the plugins its harness can
use. A GitHub Release is the immutable publication record; `main` supplies
marketplace refreshes. Agent harnesses consume published plugins rather than an
authoring checkout.

## Tracked

- `.claude-plugin/marketplace.json`: Claude catalog (`personal-skills`,
  `complexity-lens`, `cache-meter`).
- `.agents/plugins/marketplace.json`: Codex catalog (`personal-skills`,
  `build-apple-apps`, `m365-tenant-ops`, `native-browser-bridge`).
- `.cursor-plugin/marketplace.json`: Cursor catalog (`personal-skills`).
- `.grok-plugin/marketplace.json`: Grok Build catalog (same four plugins as
  Codex).
- `plugins/personal-skills/`: the shared skill tree (`skills/`) with its
  `.claude-plugin`, `.codex-plugin`, `.cursor-plugin`, and `.grok-plugin`
  manifests.
- `plugins/complexity-lens/`, `plugins/cache-meter/`: Claude-only Claude Code
  mods (see Claude Marketplace).
- `plugins/build-apple-apps/`, `plugins/m365-tenant-ops/`,
  `plugins/native-browser-bridge/`: Codex-native plugins, also listed for Grok.
- `plugins/oura-mcp/`: a hosted Streamable HTTP service for a private ChatGPT
  MCP connection; not in any catalog.
- `mcp/README.md`: local MCP notes.

No plugin folder contains another plugin's manifest, and the repo root carries
no `plugin.json`: claude.ai's marketplace sync skips a plugin whose tree holds a
nested `.claude-plugin/plugin.json`. `scripts/validate_marketplace_plugins.py`
enforces both.

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

The Claude catalog also lists two Claude Code mods, `complexity-lens` and
`cache-meter`. They need function hooks (Claude Code
2.1.259 or later with `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`):

```bash
claude plugin install complexity-lens@personal
claude plugin install cache-meter@personal
```

They are Claude-only. Codex, Cursor, and Grok auto-discover a plugin's
`hooks/hooks.json` and cannot parse a mod's, so keep these plugins out of every
other catalog and manifest; `scripts/validate_marketplace_plugins.py` enforces
that. `plugins/complexity-lens/scripts/complexity_rank.py` is a copy of
`plugins/personal-skills/skills/whittle/scripts/complexity_rank.py`;
`release_metadata.py set` refreshes it. Test a mod with
`claude plugin test plugins/<name>`.

To publish a new skill or revision, follow the repository release workflow
below, then update or reload the installed plugin.

Install from GitHub rather than the local `/Users/jstar/.agents` path. Claude's
local-path plugin cache can copy ignored local-only directories such as `env/`
and `bin/`; GitHub installation uses the tracked repo contents only.

## Cursor Marketplace

For distribution testing, this repository can be added as a private Cursor
marketplace and `personal-skills` installed from it. Cursor reads the root
`.cursor-plugin/marketplace.json` and the plugin's
`plugins/personal-skills/.cursor-plugin/plugin.json`, sharing the same skill
tree used by Claude and Codex. A Cursor catalog entry allows only `name`,
`source`, `description`, and `minClientVersions`; one other key makes the import
index zero plugins.

Cursor reads Claude's skill folders but not Claude plugin manifests or
settings. The harness manifests are intentionally thin wrappers around one
shared skill source.

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
`personal` marketplace roots. Every entry is a local source
(`./plugins/<name>`); Codex copies the folder out of its marketplace clone.

Codex's CLI ships inside ChatGPT.app
(`/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex`);
`scripts/refresh_harnesses.py` finds it there when `codex` is not on `PATH`.

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

## Grok Build Marketplace

Subscribe Grok Build to this repo as the `personal` marketplace, then install
the plugins you want. Grok reads `.grok-plugin/marketplace.json`; the Claude
catalog is not a substitute on current Grok Build:

```bash
grok plugin marketplace add Allmight97/agents
grok plugin marketplace update
grok plugin install personal-skills --trust
```

Name the source `personal` so the qualifier matches Codex and Claude
(`personal-skills@personal`). If this Mac already added the repo under another
source name, keep that qualifier or rename the `[[marketplace.sources]]` entry
in `~/.grok/config.toml`.

The Grok catalog exposes four plugins: `personal-skills`, `build-apple-apps`,
`native-browser-bridge`, and `m365-tenant-ops`, each a local folder
(`./plugins/<name>`) in the catalog checkout. Grok rejects the marketplace root
itself as a plugin path, so the shared skills must live in their own folder.
After install, enable a plugin if `grok plugin list` shows it disabled:

```bash
grok plugin enable personal-skills
```

Plugin skills appear as `/diagnose` or, on a name collision,
`/personal-skills:diagnose`. Prove the install with `grok plugin details
personal-skills` and `grok inspect`. Do not copy the skill tree into
`~/.grok/skills` or `~/.agents/skills`; those user-scope roots duplicate the
plugin.

`native-browser-bridge` can be installed for catalog parity. Its ChatGPT Chrome
runtime is Codex-specific; Grok gets the skill text, not a working native
browser bridge.

After publishing, refresh the git marketplace and reinstall or update:

```bash
grok plugin marketplace update
grok plugin install personal-skills --trust
```

Grok Bot is a separate consumer. Do not infer Bot skill availability or version
parity from this CLI marketplace.

## Release Workflow

One completed revision pass becomes one repository release. Follow the version
rules at the top of `CHANGELOG.md`:

1. Make the bounded skill, plugin, or repository changes.
2. Move the net released changes from `[Unreleased]` into a dated version
   section; omit intermediate churn and unchanged surfaces.
3. Synchronize every `plugins/personal-skills` manifest from that changelog
   version. The command also gives Codex a fresh cache-buster and ensures each
   catalog's `personal-skills` entry is a version-free local source:

   ```bash
   python3 scripts/release_metadata.py set X.Y.Z
   ```

   The command also copies whittle's `complexity_rank.py` into
   `plugins/complexity-lens/`. Give changed mods and plugins their own component
   versions and name them in the same changelog section.
4. Validate changed skills, every plugin manifest, and the catalogs. CI runs
   `scripts/validate_skills.py` on every `SKILL.md` (pinned Agent Skills
   reference validator, `skills-ref` on `PATH`, plus explicit-only parity),
   `scripts/validate_codex_plugins.py` with the pinned Codex validator (it
   strips `disable-model-invocation`, which that validator predates and the
   Codex runtime ignores), `scripts/validate_marketplace_plugins.py`, and
   `scripts/release_metadata.py check`. Check locally with:

   ```bash
   python3 scripts/validate_skills.py
   python3 scripts/validate_marketplace_plugins.py
   python3 scripts/release_metadata.py check
   claude plugin validate .
   for p in plugins/*/; do claude plugin validate "$p"; done
   claude plugin test plugins/complexity-lens
   claude plugin test plugins/cache-meter
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

   Codex, the Claude Code CLI, and Grok Build are refreshed automatically when
   their CLIs are installed; the script also finds the CLIs bundled with the
   ChatGPT and Claude Desktop apps. Claude Desktop syncs Personal Skills from the
   claude.ai account: the script verifies that copy, but updating it happens in
   the app's plugin settings. Cursor's Git marketplace may require removal and reimport before
   it exposes the new commit. Run `Developer: Reload Window` after reinstalling,
   then rerun this command; success requires exact cached release proof, not
   marketplace display metadata alone.
7. Verify the remote consumers independently. A local success does not prove
   either cloud surface:
   - Cursor Cloud: invoke a skill changed in this release and retain the run URL.
   - Grok Bot: enable the account-saved skill for the Bot and retain a successful
     `/` invocation task URL. Do not infer personal-plugin version parity.

## Upstream Skill Tracking

Skills adapted from `mattpocock/skills` record the upstream path and last
reviewed commit in their `THIRD_PARTY_NOTICES.md`. To see upstream changes for
one path since that commit, using a scratch clone in OS temp:

```bash
d=$(mktemp -d) && git clone -q https://github.com/mattpocock/skills "$d" &&
  git -C "$d" diff <reviewed-commit> HEAD -- <upstream-path>
```

After reviewing, update the recorded commit.

## Machine-Local Support

`/Users/jstar/.agents` may remain as a non-repository machine-state directory
for paths already used by local clients:

- `env/`: machine-local environment files.
- `bin/`: machine-local executable shims and MCP binaries.

Those directories are not the personal-skill source of truth.
