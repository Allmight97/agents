# Compare Interface Alternatives

Use when the choice is consequential enough that comparing alternatives may
change it. Start from the owned invariant, real callers, dependencies, and proof
constraints. Use [DEEPENING.md](DEEPENING.md) when existing modules will be merged.

Sketch two or more materially different designs. Useful axes include caller
simplicity, ownership placement, and dependency isolation. Each design must meet
the same required behavior; do not manufacture a speculative extensibility
framework merely to make the alternatives look different.

For each viable design, show:

- its interface, including ordering, errors, and resource ownership;
- one realistic caller example;
- complexity it hides and knowledge it leaves with callers;
- dependency and verification strategy;
- migration cost and principal tradeoff.

Compare caller burden, locality, failure semantics, and total upkeep. Recommend
one design and identify the evidence that could change the choice. Match the
output to the decision; a small sketch can be sufficient.

Work locally by default. When independent design work is authorized and useful,
use available subagents with bounded briefs and the same constraints. Follow
`orchestrate` if available; do not assume a particular agent tool, role, count,
or repository glossary exists. Continue implementation only within the user's
accepted scope.
