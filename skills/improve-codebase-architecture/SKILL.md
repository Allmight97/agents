---
name: improve-codebase-architecture
description: Find architecture refactor candidates when the user explicitly asks for deep-module opportunities, structural friction, or an architecture review. Scope the scan to the named area or recent change hotspots, present an HTML report in OS temp, and stop unless the user picks a candidate.
---

# Improve Codebase Architecture

Surface architectural friction and deepening opportunities — shallow modules worth refactoring for testability and navigability.

User must request this scan explicitly. Do not publish issues unless asked.

Use `codebase-design` vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) in every suggestion.

Read the repo glossary and architecture spine named in root or nested `AGENTS.md` (for ABB: `docs/ubiquitous-language.md`, `docs/system-map.md`). Respect `docs/DECISIONS.md` or `docs/adr/` — surface ADR conflicts only when friction warrants reopening.

## Process

### 1. Explore

Scope before scanning. Use the area named by the user. Otherwise inspect enough
recent history to find modules that change repeatedly and start there; widen the
scan only when changes are scattered or the evidence points across owners.

Read domain glossary and decision notes for the selected area. Walk it and note
friction:

- Understanding one concept requires bouncing across many modules?
- Interface nearly as complex as the implementation?
- Pure helpers extracted for testability but bugs hide in composition?
- Tightly coupled modules leak across seams?
- Untested or hard to test through the current interface?

Apply the **deletion test** on suspected shallow modules.

### 2. HTML report

Write a self-contained HTML file to OS temp: `<tmpdir>/architecture-review-<timestamp>.html`. Open it for the user and give the absolute path.

Each candidate card: **Files**, **Problem**, **Solution**, **Benefits**, **Before/After diagram**, **Recommendation strength** (`Strong` | `Worth exploring` | `Speculative`).

End with **Top recommendation**.

Use domain vocabulary from the repo glossary and architecture terms from `codebase-design`.

See [HTML-REPORT.md](HTML-REPORT.md) for scaffold and styling.

Do not propose interfaces yet. Ask which candidate to explore.

### 3. After pick

Use `grill-me` or repo alignment skill when capture is next. Propose glossary or decision-note updates only when the user asks. Use `codebase-design` DESIGN-IT-TWICE.md for interface alternatives.
