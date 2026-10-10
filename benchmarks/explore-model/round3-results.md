# Round 3 (3 hard tasks x Haiku medium, Sonnet medium, Opus medium x 2 runs)
Tasks: H1 settings across launches and upgrades; H2 cancel cleanup of partial files and folders; H3 every file a new metadata field touches.
combo | H1 | H2 | H3 | mean | usd (6 runs) | secs | tool calls
Haiku medium | 0.875, 1.0 | 1.0, 1.0 | 1.0, 1.0 | 0.979 | $0.091 | 236 | 81
Sonnet medium | 1.0, 1.0 | 1.0, 0.875 | 1.0, 1.0 | 0.979 | $1.513 | 243 | 54
Opus medium | 1.0, 1.0 | 1.0, 1.0 | 1.0, 1.0 | 1.000 | $2.693 | 260 | 60
No fabrications. Haiku's one miss also stated that AGENTS.md is silent on settings compatibility, which is false (a doc claim, not code).
Haiku makes more tool calls but costs about 1/17 of Sonnet and 1/30 of Opus.
