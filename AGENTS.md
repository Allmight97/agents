# Personal Claude Marketplace Guidance

## Start Here

- This repo is a Claude plugin marketplace for Claude Code, Claude Desktop,
  Cowork, and claude.ai. `.claude-plugin/marketplace.json` is the only catalog;
  each plugin is one folder under `plugins/<name>/`.
- `plugins/personal-skills/skills/` is the shared skill tree. Keep `SKILL.md`
  frontmatter within the
  [Agent Skills specification](https://agentskills.io/specification), because
  claude.ai skill uploads reject other keys. The one exception is
  `disable-model-invocation: true` for a skill only the owner starts: the
  claude.ai plugin sync accepted it in the earlier repo, and Claude Code honors
  it. `scripts/validate_skills.py` checks both.
- `README.md` owns installation and publishing commands.
- When changing a skill or repository guidance, use the `writing-for-agents`
  skill.

## Editing

- Split a skill into its own plugin only when it needs its own installation,
  permission, runtime, MCP server, hook, audience, or release lifecycle. A skill
  that gains references or helper scripts stays in `personal-skills`.

## Validation

`main` has no required check on purpose. Do not add required checks, rulesets,
or review steps, and do not report their absence as a gap. Before a push,
run the commands in `README.md` and inspect the final diff.
