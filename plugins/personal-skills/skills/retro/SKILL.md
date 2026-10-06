---
name: retro
description: "Conduct a retrospective on a coding session and suggest improvements to the agent's environment. Use only when the user asks for a retro or retrospective."
disable-model-invocation: true
---

# Retro

The user asked for a retrospective. Suggest improvements to the coding agent's
environment so that future runs go better. Do not change anything until the
user picks candidates.

## Steps

1. Load `writing-for-agents` for the writing guidance.
2. Read the primary sources for the session the user names, such as session
   logs on this machine. Default to the current session.
3. Look for candidates in the categories below. Use a category only when its
   trigger applies.
4. Present the candidates in order of severity. Give each one the evidence
   from the session and the smallest change that fixes it.

## Categories

- **Navigation.** How easy was it to find the right files? Are there hidden
  dependencies between files? A pointer in the nearest instruction file may
  help. Use when finding one piece of information took a long time.
- **Automated checks.** Could a linter, type, test, or filesystem check have
  caught the agent's mistake? Read the repository's own check commands and CI
  first. A check that exists but is unwired or silently broken is the finding;
  do not reinvent it. A repository with no pre-commit hook and no CI job for
  lint, typecheck, and tests is itself a finding. Use when an automated check
  could have caught a mistake, or the repository has no guardrail.
- **Coding standards.** Should the reviewer be given a new rule, or should an
  existing rule change? Classify the violation first. A mechanical violation (a
  fixed pattern, a banned API, an import shape, a file location) gets a
  deterministic check: a linter rule, a hook, or a CI job, whichever is
  cheapest here. Write a standard only for judgement calls that no check can
  decide. Use when the reviewer missed a mistake.
- **Always-loaded guidance.** Move steering lines that belong in a coding
  standard or an automated check out of the instruction files, in the
  repository and in the user's global scope. Use when those files are large.
- **Tool economy.** Did the agent make expensive tool calls that a better tool
  or script would avoid? Use when a call cost a lot of context or time.
- **No-ops.** Find instructions the agent already obeys by default; delete
  them. Use when the instruction files are large.
- **Information access.** Would the agent have decided better with more
  information, such as dev server logs or read-only access to a service? Use
  when a crucial fact was out of reach.

## Where each fix lives

Work has two stages: implementation and review. The implementation agent has
the most context pressure: it explores, writes code, and debugs. The review
agent receives a diff and needs no exploration, so it can enforce standards.
Put standards in the reviewer's path, not the implementer's.

- Always-loaded instruction files reach every agent on every turn. Keep them
  to navigation pointers and rules that change decisions.
- A coding-standards file is read during review, not implementation.
- Docs are reference files that other files point to. Look for an existing doc
  before writing a new one.
- A skill description is always loaded; a user-invoked skill costs nothing
  until called. Use a skill for reference material or for a user-invoked
  command.
