# issue-hygiene-reminder

A command hook for Claude Code and Codex. Before a GitHub issue write it adds
one paragraph to the model's context: check the write was authorized, the body
leads with current state and one next action, evidence lives in the repo or the
issue, at most one open fork, no decision checklists, no agent names, labels per
the repo's meanings, and a close is one or two sentences. It names the
`issue-hygiene` skill in `personal-skills` for the full rules. It never blocks.

It fires on `gh issue create|edit|close|reopen|comment|delete|transfer|lock|unlock|pin|unpin|develop`,
on `gh api ... issues ...` with a write flag, and on a GitHub MCP tool whose name
contains `issue` and a write verb (`create_issue`, `update_issue`,
`add_issue_comment`, ...). Reads, lists, and searches stay silent.

Why a hook and not only a skill: a skill loads when the model decides to load
it; the hook fires at the moment that matters, whatever the model remembered.

Codex skips a plugin's hooks until you review and trust them (`/hooks` in
Codex). Claude Code runs them once the plugin is enabled.

Test: `sh plugins/issue-hygiene-reminder/tests/remind.test.sh` (needs `jq`).
