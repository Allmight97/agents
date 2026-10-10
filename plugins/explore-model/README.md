# explore-model

A Claude Code mod. The built-in Explore subagent runs on the main
conversation's model unless the Agent call names one. This mod fills `model`
and `effort` on Explore calls that leave them out: Haiku at medium effort by
default. Explore keeps Anthropic's prompt and read-only tools; only the model
and effort change. A call that names its own model or effort keeps it.

Why Haiku: `benchmarks/explore-model/` in this repository. On audiobook-boss,
Haiku matched the main-model Explore on every task at about 1/30 the cost.

## Model version

The mod sets the alias `haiku`. The Agent tool accepts only aliases (`haiku`,
`sonnet`, `opus`, `fable`), and Claude Code resolves each one to a model:

- Anthropic API (Claude subscriptions and API keys), Claude Code 2.1.293 or
  later: the newest model of that family. `haiku` is Haiku 5.5 today and moves
  to the next Haiku when it ships.
- Amazon Bedrock, Google Vertex AI, Microsoft Foundry, or Claude Platform on
  AWS: `haiku` is Haiku 4.5.

To pin an exact model, set `ANTHROPIC_DEFAULT_HAIKU_MODEL` to a full model ID
in the `env` block of your Claude Code settings. The pin applies everywhere
`haiku` is used, not only to Explore.

## Options and install

Options (`model`, `effort`) are in `.claude-plugin/plugin.json`. Needs
function hooks (early access).

Install with `/plugin install explore-model --marketplace Allmight97/agents`.
Test with `claude plugin test plugins/explore-model`.
