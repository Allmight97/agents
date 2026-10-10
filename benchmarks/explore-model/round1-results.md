# Round 1 (5 tasks x 6 combos, 1 run each)
combo | T1 T2 T3 T4 T5 | mean | usd | secs | tool calls
Explore default (Opus) | 1.00 1.00 0.86 1.00 1.00 | 0.971 | $1.558 | 174 | 55
Opus low | 0.80 1.00 0.71 0.88 1.00 | 0.878 | $1.203 | 147 | 46
Sonnet medium | 1.00 1.00 0.86 0.88 1.00 | 0.946 | $0.896 | 154 | 44
Haiku low | 1.00 1.00 0.86 1.00 1.00 | 0.971 | $0.049 | 126 | 44
Haiku medium | 1.00 1.00 0.86 1.00 1.00 | 0.971 | $0.053 | 139 | 49
Haiku high | 1.00 1.00 0.86 1.00 1.00 | 0.971 | $0.069 | 187 | 64
Zero fabrications. Ceiling hit (24/30 cells = 1.0). T3 item 5 missed by all (weak key item).
Prune (Pareto: lower score AND higher cost than another cell): Opus low, Sonnet medium out.
Finalists: Haiku low/medium/high + Explore default as control.
