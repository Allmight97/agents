# Round 2 (4 harder tasks x 4 finalists x 2 runs; graded by blind code k1-k4, mapped after)
combo | R1 Superseded sites | R2 false premise | R3 stale allowlist | R4 begin_lookup_apply | mean | usd (8 runs) | secs | tool calls
Haiku low (k4) | 1.0 | 0.5 | 1.0 | 1.0 | 0.875 | $0.044 | 127 | 45
Haiku medium (k1) | 1.0 | 0.5 | 1.0 | 1.0 | 0.875 | $0.050 | 151 | 53
Haiku high (k3) | 1.0 | 0.5 | 1.0 | 1.0 | 0.875 | $0.056 | 214 | 64
Explore default/Opus (k2) | 1.0 | 0.5 | 1.0 | 1.0 | 0.875 | $1.418 | 165 | 42
Zero fabrications in 32 runs (false-premise task: all correctly said the frontend does none).
R2 0.5 everywhere = rubric demanded an engine code location; every run stayed inside the asked scope (src/). Uniform, not discriminating.
Tie on quality; tiebreak on cost then speed: Haiku low wins.
