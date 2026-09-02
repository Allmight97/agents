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
| Claude Code / Desktop | Plugin skills use namespaced `/plugin:skill` invocation. Claude supports `disable-model-invocation: true`, but that field is a client extension rather than portable Agent Skills frontmatter. | Install from the Claude `personal` marketplace. Reload plugins or start a fresh session, then prove namespaced invocation. Cowork and cloud sessions do not inherit this Mac's user skill directories. |
| Cursor local | Explicit invocation uses `/skill-name`. Cursor supports `disable-model-invocation: true`, also as non-portable frontmatter. | Import this GitHub repository as a user marketplace, install Personal Skills, reload the window, and prove the exact cached release plus slash-palette availability. Never infer freshness from the marketplace card alone. |
| Cursor Cloud | Runs in an isolated Linux environment with cloned repositories; local `~/.cursor` state and plugin caches are absent. | Prove a configured team/repository delivery path in a fresh Cloud run and retain a release-specific invocation result. Local Cursor proof does not transfer. |
| Grok Build | Skills appear as `/skill-name`, or `/plugin:skill` when names collide. Grok honors `disable-model-invocation` in skill frontmatter; do not add that field to portable `SKILL.md` files. | Install from the Grok `personal` marketplace via `.grok-plugin/marketplace.json`. Prove with `grok plugin details` and `grok inspect` after refresh. Keep Grok Build separate from Grok Bot. |
| Grok Bot | Uses account-saved cloud skills, `/` references, and per-Bot private-skill enablement. Current official documentation does not establish Cursor marketplace ingestion or version parity. | Prove the skill in a Bot task. Keep Grok Bot separate from Grok Build CLI and do not claim synchronization from Cursor or Grok Build state. |

For a strict shared skill, do not add client-extension frontmatter that fails the
portable validator. If cross-client explicit-only behavior justifies a
client-specific projection later, name its owner and validation cost before
adding it. Until then, only Codex's separate `openai.yaml` policy is a
deterministic portable-tree-safe manual-only control.

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

- every changed skill passes the pinned Agent Skills validator;
- native and portable plugin metadata remain aligned;
- removed skill names have no stale routes;
- manual-only claims match the client mechanism actually shipped;
- Cursor Cloud and Grok Bot are reported as unproven unless live tasks establish
  their current release behavior.
