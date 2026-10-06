# Threat Model Report Guide

Read when preparing the model's output. The workflow and scope are owned by
[SKILL.md](../SKILL.md); this guide defines what makes the result reviewable.

## Evidence Contract

- Support major architectural and control claims with repository paths and
  relevant symbols or configuration keys. Redact credentials and private data.
- Distinguish source facts, deployment assumptions, candidate abuse paths, and
  validated vulnerabilities. A plausible path is not proof of exploitation.
- Keep attacker control explicit at each consequential transition. Adjust
  priority when the required control or access is implausible.
- Use qualitative likelihood and impact with short reasoning. State which
  unresolved assumptions would materially change the ranking.
- Separate existing protections from proposed mitigations and identify the
  owner that can implement each change.

## Output Shape

Scale the document to the system. Combine sections when that improves clarity;
include only tables and diagrams that make the evidence easier to assess.

1. **Recommendation and scope:** highest-risk areas, inspected paths, deployment
   context, exclusions, and consequential assumptions.
2. **System model:** primary components, assets, entrypoints, data flows, and
   trust boundaries, with evidence anchors. A compact Mermaid flowchart helps
   when multiple actors or trust zones interact.
3. **Attacker model:** plausible capabilities and relevant limits.
4. **Abuse paths:** supported attacker goals, prerequisites, control transitions,
   and impact. Use stable IDs such as TM-001 when referencing threats elsewhere.
5. **Risk and mitigations:** likelihood, impact, existing controls, gaps,
   recommended changes, and residual risk for each material path. Avoid one
   oversized table when several short findings would be more readable.
6. **Next evidence or review:** concrete paths or checks that would validate a
   consequential assumption, plus any unanswered context question.

Before finalizing, check coverage of major in-scope entrypoints and boundaries.
A boundary with adequate controls can be recorded as considered without
inventing a threat. Explain missing evidence rather than filling a numeric
quota with speculative findings.
