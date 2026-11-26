# complexity-lens

A Claude Code mod. It runs `scripts/complexity_rank.py` on each code file Claude
reads, edits, or writes for the current message, and shows the four that most
need attention above the prompt. Each new message starts the list over.

- Red, bold: this request added a function over the per-function limit
  (`3 over limit (+1)`).
- Yellow: the file has functions over the limit.
- Dim: nothing over the limit.

Each row also shows file complexity, density, recent churn, and hotspot score.

The rows and the toast (when an edit adds a function over the limit) go only to
the person. The model gets one line, as a system reminder after the tool result:

- After a Read: when the file has a function over the limit. Each agent loop (the
  main session and each subagent) gets this once per file per user message, because
  each has its own context. A Read after an Edit of that file adds nothing.
- After every Edit or Write: when the file has a function over the limit, or has
  no per-function count (no `biome.json`, no lizard) and a hotspot score above 0.
  That second case reads `unknown function(s)`.

The Read waits for the measurement the first time per message, so it takes about
as long as the script does on that file. Changes made through Bash fire nothing.

`scripts/complexity_rank.py` is a copy of
`plugins/personal-skills/skills/whittle/scripts/complexity_rank.py`.
`python3 scripts/release_metadata.py set` copies it and `check` fails when the
two differ. Edit the whittle copy only.

Needs `scc` on `PATH`, and `biome` or `lizard` for per-function counts (see the
script). Needs Claude Code 2.1.287 or later (mods are on by default). Test with
`claude plugin test plugins/complexity-lens`.
