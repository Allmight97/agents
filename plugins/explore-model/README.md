# explore-model

A Claude Code mod. The built-in Explore subagent runs on the main
conversation's model unless the Agent call names one. This mod fills `model`
and `effort` on Explore calls that leave them out: Haiku at medium effort by
default. Explore keeps Anthropic's prompt and read-only tools; only the model
and effort change. A call that names its own model or effort keeps it.

Why Haiku: `benchmarks/explore-model/` in this repository. On audiobook-boss,
Haiku matched the main-model Explore on every task at about 1/30 the cost.

Options (`model`, `effort`) are in `.claude-plugin/plugin.json`. Needs function
hooks (early access).

Install with `/plugin install explore-model --marketplace Allmight97/agents`.
Test with `claude plugin test plugins/explore-model`.
