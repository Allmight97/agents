# session-meter

A Claude Code mod. It shows the session's plan-limit use, context fill and
prompt-cache state as one row above the prompt, and counts down to the moment
the cache lapses.

```
5h 17% 2h1m · wk ▰▰▰│▱▱ 62% · ctx 44% · cache 98% 58:35
```

- `5h N%`, then the time until the five-hour limit resets.
- `wk`: a bar of the weekly limit's use, with a tick where an even pace
  through the week would be, so fill past the tick means ahead of pace; then
  its percentage.
- `ctx N%`: share of the context window in use.
- Limits and context are green below 50%, yellow below 80%, red from 80%.
- `cache N%`: share of the last request's prompt that the cache served (green
  from 90%, yellow from 50%, red below), then the time until the cache lapses.
  It starts at the cache lifetime (5:00 or 1:00:00) and turns yellow, then red
  as the cache runs out. `/meter` names the lifetime and shows the tokens read,
  written and sent uncached.
- Advice shows when it matters: `expires soon`, `expired: /compact`,
  `expired`, `missed`, `uncached`, or `off`.

The Desktop app draws the week bar as a small fixed-size picture and the rest
as text; the terminal draws the row in coloured cells, cut at the right edge.

When the five-hour or weekly limit crosses 90%, the mod submits one prompt that
tells the agent to pause at a clean point if work would run past the limit. It
wakes an idle session, and it fires once per five-hour or weekly window, across all sessions.
The figures come from model replies, so a session with no replies never wakes.

`/meter` opens a pane:

- context and each plan limit as a bar, with the time until the limit resets;
- the cache countdown and one row per turn;
- one row per subagent this session: turns, tokens in and out, and its share
  of all tokens the session used. The share counts tokens, not plan-limit
  points: Claude Code reports limit use for the account, not per agent.

`/meter stop` closes it. Options (`ttl`, `warnSeconds`, `compactAtTokens`,
`band`, `status`, `toast`) are in `.claude-plugin/plugin.json`.

Needs function hooks (early access): Claude Code 2.1.259 or later with
`CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`. The lifetime follows Claude Code's own
cache rules; see `hooks/cache.ts` (`decideTtl`).

Install with `/plugin install session-meter --marketplace Allmight97/agents`.
Test with `claude plugin test plugins/session-meter`. Preview the Desktop band
with `bun plugins/session-meter/scripts/preview.ts <out.html>`. Adapted from MIT-licensed
work; see `THIRD_PARTY_NOTICES.md`.
