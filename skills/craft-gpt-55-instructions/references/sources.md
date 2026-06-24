# Sources

Primary sources behind the craft rules in SKILL.md. Consult when a specific decision needs grounding in the original guidance.

## OpenAI GPT-5.5 prompt guidance

URL: https://developers.openai.com/api/docs/guides/prompt-guidance

Key guidance (GPT-5.5-specific):

- Shorter, outcome-first prompts usually work better than process-heavy prompt stacks. Legacy prompts over-specify process because earlier models needed help staying on track; with GPT-5.5 that adds noise, narrows the search space, or produces overly mechanical answers.
- Define the outcome and leave room for the model to choose an efficient solution path. Describe what good looks like, what constraints matter, what evidence is available, and what the final answer should contain.
- Avoid unnecessary absolute rules (`ALWAYS`, `NEVER`, `must`, `only`) for judgment calls. Use those words for true invariants: safety rules, required output fields, actions that should never happen. For judgment calls (when to search, ask for clarification, use a tool, keep iterating), prefer decision rules.
- Add explicit stopping conditions: "After each result, ask: can I answer the user's core request now with useful evidence? If yes, answer."
- Define missing-evidence behavior: "Use the minimum evidence sufficient to answer correctly, cite it precisely, then stop."
- Personality controls how the assistant sounds; collaboration style controls how it works (when to ask, when to assume, how proactive, when to check work). Keep both short.
- Preamble pattern for streaming: a short user-visible update acknowledging the request and stating the first step improves perceived responsiveness on multi-step tasks.
- Formatting: plain paragraphs as default; reach for headers/bullets/lists only when they improve comprehension or the product UI needs a stable artifact. Respect user formatting preferences.
- Retrieval budgets are stopping rules for search: start with one broad search; search again only when top results fail, a required fact is missing, the user asked for exhaustive coverage, or a specific artifact must be read.
- Creative drafting: distinguish source-backed facts from creative wording; do not invent specifics to make a draft sound stronger; use placeholders or labeled assumptions when evidence is thin.
- Prompt the model to check its work: targeted tests, type/lint/build checks, smoke tests; for visual artifacts, render and inspect before finalizing.
- Suggested prompt structure: Role, Personality, Goal, Success criteria, Constraints, Output, Stop rules. Keep each section short; add detail only where it changes behavior.

Version note: GPT-5.5 vs GPT-5.4 — shorter outcome-first prompts preferred; `low`/`medium` reasoning effort should be re-evaluated before escalating; preambles and `phase` handling remain important for tool-heavy workflows.

## OpenAI Codex AGENTS.md guide

URL: https://developers.openai.com/codex/guides/agents-md

Key guidance:

- Codex reads global guidance before project guidance. Project and local files layer after global and override by proximity.
- Global guidance should be persistent defaults: posture and rules that hold across all projects.
- Use AGENTS.md for project instructions, commands, testing, gotchas, and nested local guidance where needed.
- Nested local AGENTS.md files own path-specific surfaces and can override broader rules for their subtree.

## Claude Code best practices — CLAUDE.md

URL: https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md

Key guidance:

- Keep CLAUDE.md short and human-readable. It is loaded every session, so include only things that apply broadly.
- For each line, ask: "Would removing this cause Claude to make mistakes?" If not, cut it. Bloated files cause the model to ignore actual instructions.
- Include: bash commands the model can't guess, code style rules that differ from defaults, testing instructions, repo etiquette, architectural decisions, environment quirks, common gotchas.
- Exclude: anything the model can figure out by reading code, standard language conventions, detailed API docs (link instead), frequently-changing info, long tutorials, file-by-file descriptions, self-evident practices like "write clean code."
- Use skills for domain knowledge or workflows only relevant sometimes; skills load on demand without bloating every conversation.
- If the model keeps doing something unwanted despite a rule against it, the file is probably too long and the rule is getting lost.
- Tune adherence with emphasis ("IMPORTANT", "YOU MUST") when needed. Treat the file like code: review when things go wrong, prune regularly, test changes by observing behavior shifts.

## agents.md format

URL: https://agents.md/

Key guidance:

- AGENTS.md is for project instructions: commands, testing, gotchas, and nested local guidance.
- Place at repo root for project-wide guidance; nest in subdirectories for path-specific surfaces.
- Keep command lists runnable and exact; include build/test/lint commands the agent should run.

## Cross-source synthesis

- Always-loaded files (AGENTS.md, CLAUDE.md) are a shared, scarce resource. Both OpenAI and Anthropic guidance converge: short, persistent, non-inferable defaults only; push conditional material to skills and detailed material to references.
- GPT-5.5's precision means contradictions and ambiguity are more costly than for earlier models. Prune conflicting rules; prefer decision rules with escape clauses over absolutes for judgment calls.
- Outcome-first shape is GPT-5.5-specific guidance; the leanness and layering principles are durable across model versions.
