# done-gate

A Claude Code mod. It stops Claude from ending a turn while changed code has
not passed the repository's check command.

```
done-gate: 2 file(s) changed since the last passing check (src/greet.py, tests/test_greet.py).
Run `bash scripts/check.sh` and fix any failure before you finish.
```

- Proof is the state of the working tree, not the order of tool calls. When a
  Bash command that matches `checks` ends without error, the mod records a git
  tree id of the whole working tree: tracked and untracked files, ignored files
  left out. An edit made later through Edit, Write, `sed -i` or a subagent
  changes that id.
- At the end of a main-loop turn, the mod compares the tree with the last
  proven one, or with the tree at session start when nothing passed yet. If a
  changed file is under `paths`, it blocks the turn once and names the check.
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

Limits: a check passes when the tests it runs pass, so deleting a failing test
passes too. The tree id is written through a private index at
`.git/done-gate.index`; `git add --all` there writes blob objects to
`.git/objects`, which `git gc` removes when unreferenced.

Needs function hooks (early access): Claude Code 2.1.287 or later. Test with
`claude plugin test plugins/done-gate`.
