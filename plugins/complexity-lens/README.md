# complexity-lens

A Claude Code mod. It runs `scripts/complexity_rank.py` on each code file Claude
reads, edits, or writes for the current message, and shows the four that most
need attention above the prompt. Each new message starts the list over.

- Red, bold: this request added a function over the per-function limit
  (`3 over limit (+1)`).
- Yellow: the file has functions over the limit.
- Dim: nothing over the limit.

Each row also shows file complexity, density, recent churn, and hotspot score.

After an Edit or Write, the model also gets one extra context line when the file
has a function over the limit. A toast appears when an edit adds one.

`scripts/complexity_rank.py` is a copy of
`plugins/personal-skills/skills/whittle/scripts/complexity_rank.py`.
`python3 scripts/release_metadata.py set` copies it and `check` fails when the
two differ. Edit the whittle copy only.

Needs `scc` on `PATH`, and `biome` or `lizard` for per-function counts (see the
script). Needs Claude Code 2.1.287 or later (mods are on by default). Test with
`claude plugin test plugins/complexity-lens`.
