# Codex Prompt Recipes

Use the smallest shape that fits the task. Replace bracketed text with task-specific facts.

## Implementation

```text
Implement [outcome] in [repository or path]. Preserve [important behavior or boundary].

You may inspect and edit the workspace. Finish when [acceptance criteria]. Verify with [checks], then report the result, evidence, and any residual risk.
```

## Diagnosis or review

```text
Inspect [failure, change, or surface] and determine [decision or root-cause question]. Ground claims in repository and tool evidence.

This is read-only. Lead with the verdict or severity-ordered material findings, then give the supporting evidence and smallest useful next step. Label inference and unresolved uncertainty.
```

## Research or recommendation

```text
Research [question] using current primary sources and recommend [decision]. Focus on evidence that changes the choice among [options or constraints].

Separate sourced facts, inference, and open questions. Lead with the recommendation, then give tradeoffs and citations.
```
