---
name: resolving-merge-conflicts
description: Resolve an in-progress git merge or rebase conflict. Use when Codex sees conflict markers, unmerged paths, rebase/merge state, or the user asks to finish a conflicted merge/rebase while preserving both sides' intent and project checks.
---

# Resolving Merge Conflicts

Resolve the conflict that exists now. Preserve intent, avoid invention, and finish only after the project can prove the result.

## Workflow

1. **Read the current state.** Run `git status --short`, identify whether this is a merge or rebase, list unmerged paths, and inspect each conflicting file before editing.

2. **Find primary intent.** For each side of each conflict, read the relevant commits, messages, nearby history, PR/issue references when available, and surrounding code. Prefer source evidence over guessing from marker text.

3. **Resolve each hunk.** Preserve both intents where they are compatible. Where they conflict, choose the behavior that matches the merge/rebase goal and state the trade-off. Do not invent unrelated behavior while resolving.

4. **Protect user work.** Never run `git merge --abort`, `git rebase --abort`, `git reset --hard`, `git checkout --`, or clean untracked files unless the user explicitly asks. Do not discard untracked or unstaged work to make the conflict easier.

5. **Run project checks.** Discover the repository's command map before choosing checks. In ABB, start with `scripts/AGENTS.md`; typical checks are `cargo fmt`, `cargo clippy`, `cargo test` from the workspace root, plus Biome for TypeScript when touched. Fix only failures caused by the conflict resolution.

6. **Finish deliberately.** Stage the resolved files. If rebasing, continue the rebase until complete. If merging, create the merge commit only when the user asked you to commit or the repo workflow clearly requires it.

## Output

Report the resolved files, the intent preserved from each side, checks run, and any residual risk or checks skipped.
