# Personal Claude Marketplace

A Claude plugin marketplace for claude.ai, Claude Desktop (Chat, Cowork, and
the Code tab), and Claude Code. The catalog is
`.claude-plugin/marketplace.json`; every plugin is a folder under `plugins/`.

## Install

Install through claude.ai, so one install reaches every surface:

1. On claude.ai, open **Customize** → **Plugins** → **Add** → **Add
   marketplace**, and enter `Allmight97/agents`.
2. Turn on **Sync automatically** for the marketplace.
3. Search the Plugins page for each plugin by name (for example `Personal
   skills`), open it, and select **Add**. An added marketplace lists its plugins
   nowhere else.

Installs attach to your account. Chat and Cowork use them directly; Claude Code
syncs them at each start as `<plugin>@synced`.

The mods and `issue-hygiene-reminder` are installed from the Claude Code
command line today: `claude plugin marketplace add Allmight97/agents`, then
`claude plugin install <plugin>@personal`.

Install each plugin one way only. If the same plugin is also installed from the
Claude Code command line, Claude Code loads that copy and skips the synced one.

## Plugins

- `personal-skills`: the shared skill tree (`plugins/personal-skills/skills/`).
  Skills are namespaced, for example `/personal-skills:diagnose`.
- `complexity-lens`, `session-meter`, `nested-agents-md`, `explore-model`,
  `progress-watch`: Claude Code mods. They run only in Claude Code 2.1.287 or
  later.
- `issue-hygiene-reminder`: a command hook that reminds the model of the
  `issue-hygiene` rules before a GitHub issue write. Hooks run in Cowork and
  Claude Code, not in Chat.
- `codex-review`: a skill and launcher that runs an adversarial Codex review.
  It needs the Codex CLI on the machine.

`plugins/complexity-lens/scripts/complexity_rank.py` is a copy of
`plugins/personal-skills/skills/whittle/scripts/complexity_rank.py`; a plugin
is installed as its own folder and cannot reach the other's file.

## Publish a change

Plugins carry no `version`: claude.ai keeps its own version for synced
plugins, and a command-line install without one tracks commits.

1. Validate. CI runs the same commands on every push:

   ```bash
   python3 scripts/validate_skills.py
   python3 scripts/validate_marketplace.py
   claude plugin validate .
   for p in plugins/*/; do claude plugin validate "$p"; done
   python3 scripts/test_plugins.py
   ```

2. Push to `main`. claude.ai syncs the marketplace; if a change has not
   arrived, open the marketplace on claude.ai and choose **Check for updates**.
   Claude Code picks up the synced copy at its next start.

## Upstream Skill Tracking

Skills adapted from `mattpocock/skills` record the upstream path and last
reviewed commit in their `THIRD_PARTY_NOTICES.md`. To see upstream changes for
one path since that commit, using a scratch clone in OS temp:

```bash
d=$(mktemp -d) && git clone -q https://github.com/mattpocock/skills "$d" &&
  git -C "$d" diff <reviewed-commit> HEAD -- <upstream-path>
```

After reviewing, update the recorded commit.
