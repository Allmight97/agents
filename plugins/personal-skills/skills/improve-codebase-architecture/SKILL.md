---
name: improve-codebase-architecture
description: "Architecture scan: find shallow modules, hidden or needless links, surplus code, and special cases, and recommend refactor candidates; or untangle a whole codebase or area on request."
---

# Improve Codebase Architecture

Surface architectural friction and recommend refactors that remove it.

When the user asks to untangle or refactor the whole codebase or a named area,
read [UNTANGLE.md](UNTANGLE.md) and follow it instead of the Process steps.

Read [codebase-design](../codebase-design/SKILL.md) for the shared design
criteria and vocabulary.

## Process

### 1. Explore

Scope before scanning. Use the area named by the user. Otherwise inspect recent
history to find modules that change repeatedly and start there; widen the scan
only when changes are scattered or the evidence points across owners.

Read every applicable guidance file along the selected path, including root,
package, and nested module instructions, for vocabulary and decision notes,
before loading optional architecture material. Load an architecture overview
only when that guidance names a trigger matching the scan. Verify terminology
against the owning interface and code. Respect the rationale stated beside the
rules you touch, in owner guidance or at the enforcing code. Surface conflicts
only when the friction warrants reopening them. Skip candidates that guidance
records as rejected.

Walk the path and ask of its pieces one question: **should these change
together?** Note each place the code answers it wrong:

- **Hidden links:** pieces that must change together while nothing shows it:
  copied logic or values, a module reading a global or file another module
  sets, one feature split across folders by layer, one concept spread across
  many modules, a call order callers must simply know, or state spread across
  flags, optional fields, or reserved values that only make sense read
  together (`codebase-design`).
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
the design.

Apply the **deletion test** on suspected shallow modules.

Done when every module in scope has been asked the question, and each wrong
answer and special case is noted with `file:line`.

### 2. Recommend candidates

Recommend the one fix behind several problems; it often looks nothing like
them. For each supported candidate, name the location, the problems it
removes, preserved obligation, proposed owner, expected benefit, proof path,
and migration risk. Omit speculative candidates without evidence of recurring
cost.

Lead with the strongest recommendation. Use a concise chat report for a small
scope. For several candidates or diagram-heavy comparisons, use
[HTML-REPORT.md](HTML-REPORT.md).

For a scan-only request, let the user choose what to explore. When they already
selected a candidate or authorized a bounded refactor, continue within that
scope rather than reopening the selection. When the user rejects a candidate
for a lasting reason, offer to record that reason in the nearest `AGENTS.md`
so later scans skip it.

### 3. Design the selected candidate

Use `grill-me` when material user decisions remain and
`codebase-design`'s
[interface comparison guidance](../codebase-design/DESIGN-IT-TWICE.md) when
alternatives would help. Update governing guidance only when the accepted
change alters its contract. Done when the user accepts one design or the open
decisions are listed.
