# Explore model benchmark

Which model and effort should the Explore subagent use? Measured on
audiobook-boss at commit `de9aa91e`, Claude Code 2.1.296, 2026-10-10. Not a
plugin or skill: no catalog lists this folder.

## Result

Haiku 5.5 matched the default Explore (which runs on the main model, here
Opus 5.5) on all 9 tasks, at about 1/30 the cost. Effort above low bought no
measured quality; the mod uses medium as cheap insurance.

- Round 1: 6 combinations x 5 tasks. Opus low and Sonnet medium dropped steps
  of call chains while costing more. Results: `round1-results.md`.
- Round 2: Haiku low, medium and high plus the default, 4 harder tasks x 2
  runs. All tied on quality. Haiku low was cheapest and fastest. Results:
  `round2-results.md`.
- Round 3: Haiku medium against Sonnet medium and Opus medium on 3 hard,
  multi-module tasks, 2 runs each. Scores 0.979, 0.979 and 1.000; Haiku cost
  about 1/17 of Sonnet and 1/30 of Opus. Results: `round3-results.md`.
- No run in any round invented a location, including the false-premise
  task.

The cost gap is structural: Explore sends a fixed prompt of about 40k tokens
with every request, billed at the model's cache-read price.

## Re-running

1. Check that each answer key still matches the target repo. The keys pin file
   lines at `de9aa91e`; rebuild them from the code (`round1-key.md`,
   `round2-key.md`) before grading.
2. In one Claude Code session, launch each task in `tasks.md` as an Explore
   subagent per combination, passing `model` and `effort` on the Agent call
   (none for the default; disable the `explore-model` mod first, or it
   fills Haiku in). Run them in the background.
3. Grade each report against the key with the rubric (`round1-rubric.md`; the
   round 2 and 3 rubrics are inside their keys) before mapping codes to
   combinations. A fabricated location scores the task 0.
4. `python3 cost.py ~/.claude/projects/<project dir>/<session id>` prints cost,
   time and tool calls per run.

Deployment is the `explore-model` mod (`plugins/explore-model`). It fills
`model` and `effort` on Explore calls that name neither, so Explore keeps the
built-in prompt and tools this measured. A user-level
`~/.claude/agents/Explore.md` would replace both. Benchmark calls name their
model and effort, so the mod leaves them alone.
