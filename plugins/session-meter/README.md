# session-meter

A Claude Code mod. It shows the session's context fill, plan-limit use and
prompt-cache use as one line above the prompt, and counts down to the moment
the cache lapses.

```
ctx 12% · 5h 2% · wk 2% · cache 100% · read 566k · wrote 1.1k · new 2 · 59:38 / 1h · warm
```

- `ctx N%`: share of the context window in use.
- `5h N%`, `wk N%`: share of the five-hour and weekly plan limits used, as the
  last API response reported them. Absent off a subscription. Green below 50%,
  yellow below 80%, red from 80%.
- `cache N%`: share of the last request's prompt that the cache served. Green
  from 90%, yellow from 50%, red below.
- `read`, `wrote`, `new`: tokens read from the cache, written to it, and sent
  uncached.
- `59:38 / 1h`: time left, then the cache lifetime. The clock turns yellow, then
  red as the cache runs out.
- The last word is the advice: `warm`, `expires soon`, `expired: /compact`,
  `expired`, `missed`, `cold`, `uncached`, or `off`.

The line stays on one row. When the width is short it drops the advice, then
`new`, `wrote`, `read` and `wk`. It draws below whatever other band mods return.

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
Test with `claude plugin test plugins/session-meter`. Adapted from MIT-licensed
work; see `THIRD_PARTY_NOTICES.md`.
