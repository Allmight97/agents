# Personal Agent Marketplace Guidance

## Start Here

- `skills/` is the canonical shared Agent Skills source. Keep `SKILL.md`
  frontmatter valid against the [Agent Skills specification](https://agentskills.io/specification).
- The repository is one personal-skills package for multiple clients. Use the
  [Agent Plugins specification](https://agent-plugins.org/) as the portable
  packaging floor; create a separate plugin only for an independent install,
  permission, runtime, MCP, hook, audience, or release boundary.
- `README.md` owns installation, refresh, and release commands. `CHANGELOG.md`
  owns released behavior. Do not cache those procedures here.
- When changing an Agent Skill or repository guidance, use
  `skills/writing-for-agents`; its disclosed mechanics own skill structure,
  invocation metadata, instruction placement, and behavioral proof.

## Harness Compatibility

The shared skill body is portable; discovery, manual-only policy, distribution,
and refresh are client behavior. Keep those differences explicit and prove each
consumer separately.

| Surface | Invocation and policy owner | Distribution and proof |
| --- | --- | --- |
| Codex | Explicit invocation uses `$skill`. Put Codex-only policy in `skills/<name>/agents/openai.yaml`; `policy.allow_implicit_invocation: false` makes a skill explicit-only. | Install from the Codex `personal` marketplace. Prove the installed version, enabled state, and explicit invocation after refresh. |
| Claude Code / Desktop | Plugin skills use namespaced `/plugin:skill` invocation. Claude honors `disable-model-invocation: true` in `SKILL.md` frontmatter: the description is not loaded and the skill runs only when the user calls it. The flag also blocks one skill invoking another. | Install from the Claude `personal` marketplace. Reload plugins or start a fresh session, then prove namespaced invocation. Cowork and cloud sessions do not inherit this Mac's user skill directories. |
| Cursor local | Explicit invocation uses `/skill-name`. Cursor reads Claude's skill folders, so it honors the same `disable-model-invocation: true` flag. It does not read Claude settings or Claude plugin manifests. | Import this GitHub repository as a user marketplace, install Personal Skills, reload the window, and prove the exact cached release plus slash-palette availability. Never infer freshness from the marketplace card alone. |
| Cursor Cloud | Runs in an isolated Linux environment with cloned repositories; local `~/.cursor` state and plugin caches are absent. | Prove a configured team/repository delivery path in a fresh Cloud run and retain a release-specific invocation result. Local Cursor proof does not transfer. |
| Grok Build | Skills appear as `/skill-name`, or `/plugin:skill` when names collide. Grok honors `disable-model-invocation` in skill frontmatter. It reads Claude marketplaces, plugins, skills, hooks, and `CLAUDE.md`, but not Claude's `settings.json`. | Install from the Grok `personal` marketplace via `.grok-plugin/marketplace.json`. Prove with `grok plugin details` and `grok inspect` after refresh. Keep Grok Build separate from Grok Bot. |
| Grok Bot | Uses account-saved cloud skills, `/` references, and per-Bot private-skill enablement. Current official documentation does not establish Cursor marketplace ingestion or version parity. | Prove the skill in a Bot task. Keep Grok Bot separate from Grok Build CLI and do not claim synchronization from Cursor or Grok Build state. |

Explicit-only means two switches: `disable-model-invocation: true` in `SKILL.md`
(Claude, Cursor, Grok Build) and `policy.allow_implicit_invocation: false` in
`agents/openai.yaml` (Codex, which ignores unknown frontmatter keys).
`scripts/validate_skills.py` allows only those extension keys (and
`user-invocable`), validates a copy without them against the pinned
Agent Skills validator, and requires the Codex switch wherever the flag is set.
A skill another skill invokes by name stays unflagged, because the flag blocks
that call: `whittle` (invoked by `pre-pr-gut-check`) and
`improve-codebase-architecture` (a `pre-pr-gut-check` lens) are Codex-only.

## Editing And Release Boundaries

- Keep one meaning in one owner: portable behavior in `SKILL.md`, substantial
  mode-specific behavior in disclosed references, client UI/policy in supported
  client metadata, and operator commands in `README.md` or scripts.
- Do not split a skill into its own plugin merely because it gains references or
  ordinary helper scripts. Split when the component needs its own installation,
  authority, runtime, or lifecycle.
- A release is not complete until manifests, tag, GitHub Release, locally
  installed consumers, and applicable remote consumers are proven separately.

## Validation

Before release, run the repository commands documented in `README.md`, inspect
the final diff, and verify:

- `python3 scripts/validate_skills.py` passes (pinned Agent Skills validator plus the explicit-only parity rule);
- native and portable plugin metadata remain aligned;
- removed skill names have no stale routes;
- manual-only claims match the client mechanism actually shipped;
- Cursor Cloud and Grok Bot are reported as unproven unless live tasks establish
  their current release behavior.
