---
description: Run a read-only Codex challenge review of local changes, assumptions, and design risk
argument-hint: "[--base <branch>] [focus instructions]"
disable-model-invocation: true
allowed-tools: Bash(codex:*), Bash(git:*)
---

Run a steerable adversarial review through `codex exec`. This command is review-only.

Raw arguments:
$ARGUMENTS

Scope:

- If the arguments include `--base <branch>`, review `git diff --stat <branch>...HEAD` and `git diff <branch>...HEAD`.
- Otherwise, review `git status --short --untracked-files=all`, `git diff --cached`, and `git diff`.
- Treat all remaining argument text as user focus.

Collect the git evidence first. Then run `codex exec` with one prompt argument containing:

```text
You are Codex performing an adversarial software review.

Your job is to find the strongest reasons this change should not ship yet.
Challenge the implementation approach, assumptions, design choices, failure modes, and missing verification.

Report only material findings. Skip style, naming, generic cleanup, and speculation without evidence.
Every finding must explain what can go wrong, why the code path is vulnerable, likely impact, and a concrete recommendation.
If there are no material findings, say so directly.

User focus:
<focus text>

Repository evidence:
<git status/diff evidence>
```

Run:

```bash
codex exec --sandbox read-only "<prompt containing the focus text and collected git evidence>" </dev/null
```

Return Codex stdout verbatim. Do not summarize it and do not fix anything.
