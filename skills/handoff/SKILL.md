---
name: handoff
description: Write a session handoff to OS temp when the user asks to continue in a new thread or pass work to another agent.
---

# Handoff

Write a handoff so a fresh agent can continue. Save to the OS temporary directory — not the workspace.

Read `docs/agents/issue-tracker.md` when present; otherwise infer GitHub from `git remote`.

## Include

- Objective in one sentence
- Accepted direction and explicit non-decisions
- Links to issues, PRs, or commits — do not duplicate their bodies
- Assumptions the next agent must validate
- Verification commands that matter

## Omit

- Duplicated issue, spec, or canon content (link instead)
- Process history, research methodology, or how the plan was produced
- API keys, passwords, or PII

If the user passed arguments, use them as the next session focus.