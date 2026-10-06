# complexity-lens

A Claude Code mod. It runs `scripts/complexity_rank.py` on each code file Claude
reads, edits, or writes, and shows the worst four files above the prompt: file
complexity, density, functions over the per-function limit, recent churn, and
hotspot score.

After an Edit or Write, the model also gets one extra context line when the file
has a function over the limit. A toast appears when an edit adds one.

`scripts/complexity_rank.py` is a copy of `skills/whittle/scripts/complexity_rank.py`.
`python3 scripts/release_metadata.py set` copies it and `check` fails when the
two differ. Edit the whittle copy only.

Needs `scc` on `PATH`, and `biome` or `lizard` for per-function counts (see the
script). Needs function hooks (early access): Claude Code 2.1.259 or later with
`CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`. Test with
`claude plugin test plugins/complexity-lens`.
