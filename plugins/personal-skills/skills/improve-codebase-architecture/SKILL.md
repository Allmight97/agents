---
name: improve-codebase-architecture
description: "Scan code for architecture friction (shallow modules, leaky seams, hidden or needless coupling, special cases) and recommend refactor candidates, or untangle a whole codebase on request."
---

# Improve Codebase Architecture

Surface architectural friction and deepening opportunities — shallow modules worth refactoring for testability and navigability.

User must request this scan explicitly. Do not publish issues unless asked.
When the user asks to untangle or refactor the whole codebase, not only scan
it, read [UNTANGLE.md](UNTANGLE.md) and follow it after the Explore step.

Read [codebase-design](../codebase-design/SKILL.md) for the shared design criteria. Use its terms where they
clarify the problem, alongside the project's domain vocabulary.

Read every applicable guidance file along the selected path, including root,
package, and nested module instructions, before loading optional architecture
material. Load an architecture overview only when that guidance names a trigger
matching the scan. Verify terminology against the owning interface and code
instead of assuming a repository-wide glossary. Respect the rationale stated
beside the rules you touch, in owner guidance or at the enforcing code. Surface
conflicts only when the friction warrants reopening them.

## Process

### 1. Explore

Scope before scanning. Use the area named by the user. Otherwise inspect enough
recent history to find modules that change repeatedly and start there; widen the
scan only when changes are scattered or the evidence points across owners.

Read vocabulary and decision notes from every applicable guidance file along
the path. Skip candidates that guidance records as rejected. Walk the path and
ask of its pieces one question: **should these change together?** Note each
place the code answers it wrong:

- **Hidden links:** pieces that must change together while nothing shows it:
  copied logic or values, a module reading a global or file another module
  sets, one feature split across folders by layer, a call order callers
  must simply know, or state spread across flags, optional fields, or
  reserved values that only make sense read together (`codebase-design`).
- **Needless links:** pieces tied together that change for different reasons:
  callers that depend on internals, stable code importing more volatile code,
  a general function with a parameter only one workflow understands, or a
  shallow module (`codebase-design`).
- **Surplus:** pieces with no reason of their own to change: pass-through
  wrappers, extension points or configuration for things that never vary, and
  dead code.

Also count **special cases**: an `if` for one value, a parameter for one
caller, a swallowed exception, a retry or sleep, a disabled test. Each is a
requirement the design never absorbed; how many remain is the main measure of
the design. Note too where understanding one concept means bouncing across
many modules, where bugs hide in the composition of helpers extracted for
testability, and where a module is hard to test through its current interface.

Apply the **deletion test** on suspected shallow modules.

### 2. Recommend candidates

Look for the one fix behind several problems; it often looks nothing like
them. Do not fix special cases one by one. For each supported candidate,
name the location, the problems it removes, preserved obligation, proposed
owner, expected benefit, proof path, and migration risk. Omit speculative
candidates without evidence of recurring cost.

Lead with the strongest recommendation. Use a concise chat report for a small
scope. For several candidates or diagram-heavy comparisons, use
[HTML-REPORT.md](HTML-REPORT.md) to create a report in OS temp and open it for the
user. Include the absolute path.

For a scan-only request, let the user choose what to explore. When they already
selected a candidate or authorized a bounded refactor, continue within that
scope rather than reopening the selection. When the user rejects a candidate
for a lasting reason, offer to record that reason in the nearest `AGENTS.md`
so later scans skip it.

### 3. Explore a selected candidate

Use `grill-me` when material user decisions remain and
`codebase-design`'s [interface comparison guidance](../codebase-design/DESIGN-IT-TWICE.md)
when alternatives would help. Update governing guidance only when the accepted
change alters its contract; do not create a glossary as a side effect.
