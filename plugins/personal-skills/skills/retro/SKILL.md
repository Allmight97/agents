---
name: retro
description: "Retrospective on a coding session: environment, check, and guidance improvements backed by session evidence."
---

# Retro

The user asked for a retrospective. Suggest improvements to the coding agent's
environment so that future runs go better. Do not change anything until the
user picks candidates.

## Steps

1. Load `writing-for-agents` for the writing guidance.
2. Read the primary sources for the session the user names, such as session
   logs on this machine. Default to the current session.
3. Test every category's trigger below against the session; report which fired
   and which did not.
4. Present the candidates in order of severity. Give each one the evidence
   from the session and the smallest change that fixes it.
5. Apply only the picked candidates, each with its check proven to fail on the
   cited instance.

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
- **Coding standards.** Should `code-review` be given a new rule, or should an
  existing rule change? Apply writing-for-agents' "Should the line exist"
  order; name a past instance of the mistake the check must fail on. Use when
  `code-review` missed a mistake.
- **Always-loaded guidance.** Find lines in the instruction files, in the
  repository and in the user's global scope, that belong in a check or state
  what the agent does by default; move or delete them. Use when a line in an
  always-loaded file failed to steer the session or states what the agent does
  by default.
- **Tool economy.** Did the agent make expensive tool calls that a better tool
  or script would avoid? Use when a call cost a lot of context or time.
- **Information access.** Would the agent have decided better with more
  information, such as dev server logs or read-only access to a service? Use
  when a crucial fact was out of reach.

## Where each fix lives

Review runs through `code-review`, which reads the `AGENTS.md` chain along the
changed paths. Put a judgement rule there, in the nearest nested file; put a
mechanical one in a check.

- Docs are reference files that other files point to. Look for an existing doc
  before writing a new one.
- Use a skill for reference material or a user-invoked command.
