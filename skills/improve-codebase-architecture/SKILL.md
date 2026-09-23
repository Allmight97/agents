---
name: improve-codebase-architecture
description: Find refactor opportunities when the user explicitly requests an architecture review or a scan for structural friction.
---

# Improve Codebase Architecture

Surface architectural friction and deepening opportunities — shallow modules worth refactoring for testability and navigability.

User must request this scan explicitly. Do not publish issues unless asked.

Read `codebase-design` for the shared design criteria. Use its terms where they
clarify the problem, alongside the project's domain vocabulary.

Read every applicable guidance file along the selected path, including root,
package, and nested module instructions, before loading optional architecture
material. Load an architecture overview only when that guidance names a trigger
matching the scan. Verify terminology against the owning interface and code
instead of assuming a repository-wide glossary. Respect `docs/DECISIONS.md` or
`docs/adr/` when present. Surface conflicts only when the friction warrants
reopening them.

## Process

### 1. Explore

Scope before scanning. Use the area named by the user. Otherwise inspect enough
recent history to find modules that change repeatedly and start there; widen the
scan only when changes are scattered or the evidence points across owners.

Read vocabulary and decision notes from every applicable guidance file along
the path. Walk it and note friction:

- Understanding one concept requires bouncing across many modules?
- Interface nearly as complex as the implementation?
- Pure helpers extracted for testability but bugs hide in composition?
- Tightly coupled modules leak across seams?
- Untested or hard to test through the current interface?

Apply the **deletion test** on suspected shallow modules.

### 2. Recommend candidates

For each supported candidate, name the location, current friction, preserved
obligation, proposed owner, expected benefit, proof path, and migration risk.
Omit speculative candidates without evidence of recurring cost.

Lead with the strongest recommendation. Use a concise chat report for a small
scope. For several candidates or diagram-heavy comparisons, use
[HTML-REPORT.md](HTML-REPORT.md) to create a report in OS temp and open it for the
user. Include the absolute path.

For a scan-only request, let the user choose what to explore. When they already
selected a candidate or authorized a bounded refactor, continue within that
scope rather than reopening the selection.

### 3. Explore a selected candidate

Use `grill-me` when material user decisions remain and
`codebase-design`'s [interface comparison guidance](../codebase-design/DESIGN-IT-TWICE.md)
when alternatives would help. Update governing guidance only when the accepted
change alters its contract; do not create a glossary as a side effect.
