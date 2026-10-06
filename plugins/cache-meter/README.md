# cache-meter

A Claude Code mod. It shows prompt-cache use as one line above the prompt and
counts down to the moment the cache lapses.

```
cache 100% · read 566k · wrote 1.1k · new 2 · 59:38 / 1h · warm
```

- `cache N%`: share of the last request's prompt that the cache served. Green
  from 90%, yellow from 50%, red below.
- `read`, `wrote`, `new`: tokens read from the cache, written to it, and sent
  uncached.
- `59:38 / 1h`: time left, then the cache lifetime. The clock turns yellow, then
  red as the cache runs out.
- The last word is the advice: `warm`, `expires soon`, `expired: /compact`,
  `expired`, `missed`, `cold`, `uncached`, or `off`.

The line stays on one row. When the width is short it drops the advice, then
`new`, then `wrote`. It draws below whatever other band mods return.

`/cache` opens a pane with the full advice and one row per turn. `/cache stop`
closes it. Options (`ttl`, `warnSeconds`, `compactAtTokens`, `band`, `status`,
`toast`) are in `.claude-plugin/plugin.json`.

Needs function hooks (early access): Claude Code 2.1.259 or later with
`CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`. The lifetime follows Claude Code's own
cache rules; see `hooks/cache.ts` (`decideTtl`).

Test with `claude plugin test plugins/cache-meter`. Adapted from MIT-licensed
work; see `THIRD_PARTY_NOTICES.md`.
