# Design It Twice

Design the interface twice: use when the choice is consequential enough that
comparing alternatives may change it. Start from the owned invariant, real
callers, dependencies, and proof constraints. Use [DEEPENING.md](DEEPENING.md)
when existing modules will be merged.

Sketch two or more materially different designs. When a design already exists,
include it as one candidate, judged by the same criteria. Useful axes include
caller simplicity, ownership placement, and dependency isolation. Each design
must meet the same required behavior; do not manufacture a speculative
extensibility framework merely to make the alternatives look different.

For each viable design, show:

- its interface, including ordering, errors, and resource ownership;
- one realistic caller example;
- complexity it hides and knowledge it leaves with callers;
- dependency and verification strategy;
- migration cost and principal tradeoff.

Compare caller burden, locality, failure semantics, and total upkeep. Recommend
one design and identify the evidence that could change the choice. Match the
output to the decision; a small sketch can be sufficient.

Work locally by default; use subagents with bounded briefs and the same
constraints when delegation is authorized and useful.
