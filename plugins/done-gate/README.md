# done-gate

A Claude Code mod. It stops Claude from ending a turn while changed code has
not passed the repository's check command.

```
done-gate: 2 file(s) changed since the last passing check (src/greet.py, tests/test_greet.py).
Run `bash scripts/check.sh` and fix any failure before you finish.
```

- It counts only the files this session changes: each file an Edit or Write
  call names, and each file a Bash command changes. For Bash, the mod records
  a git tree id of the whole working tree (tracked and untracked files,
  ignored files left out) before and after the command and diffs the two. A
  command that is only `git checkout`, `switch`, `merge`, `pull`, `rebase`,
  `reset` or `fetch` counts nothing, so branch switches and merges are not the
  session's changes. Edits by another agent between commands do not count.
- A Bash command that matches `checks` and ends without error covers every
  change the session made before it. At the end of a main-loop turn, if a file
  changed since the last pass is under `paths`, the mod blocks the turn once
  and names the check. With `resolve`, the repository's own command decides
  instead (below).
- The second stop in a row goes through, so a turn cannot loop. A toast then
  says the turn finished without a passing check.
- A broken config blocks once with the reason. A failure inside the mod blocks
  once and asks Claude to say the work is unverified.

Each repository opts in with `.claude/done-gate.json`. Without that file the
mod does nothing.

```json
{
  "checks": ["^bash scripts/verify\\.sh"],
  "paths": ["src/", "crates/"],
  "hint": "bash scripts/verify.sh <lane>"
}
```

- `checks`: regular expressions matched against the Bash command. Required.
- `paths`: path prefixes from the repository root that need proof. Empty or
  absent means every file.
- `hint`: the command named in the block message. Defaults to the first
  pattern.
- `resolve`: optional. A command and its arguments, run from the repository
  root, that decides which checks are unmet. It reads JSON on stdin,
  `{ "changed": [files the session changed], "passes": [{ "command",
  "changed": [files the session changed since that command passed] }] }`, and prints one
  unmet check per line (nothing when all are met). With `resolve`, `paths` and
  `hint` are unused. Use it when the repository already owns a map from paths
  to checks, so the map has one owner.

Limits: a check passes when the tests it runs pass, so deleting a failing test
passes too. A change another process makes while one of the session's Bash
commands runs counts as the session's; so does the whole diff of a chained
command such as `git checkout x && make`, and of git commands not listed above
(`git stash pop`, `git restore`). Files a background Bash command changes after
it returns, or that an MCP tool or NotebookEdit writes, do not count. The tree id is written through a private index at
`.git/done-gate.index`; `git add --all` there writes blob objects to
`.git/objects`, which `git gc` removes when unreferenced.

Needs function hooks (early access): Claude Code 2.1.287 or later. Test with
`claude plugin test plugins/done-gate`.
