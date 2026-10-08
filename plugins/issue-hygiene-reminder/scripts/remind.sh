#!/bin/sh
# PreToolUse reminder before a GitHub issue write. Reads the hook's JSON on
# stdin; prints the reminder as hook JSON only for an issue write; never blocks.
input=$(cat)
tool=$(printf '%s' "$input" | jq -r '.tool_name // ""')
case "$tool" in
  Bash)
    cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')
    # An actual gh invocation at a command position, not text inside a string.
    gh_issue='(^|[;&|(]|&&)[[:space:]]*gh[[:space:]]+issue[[:space:]]+(create|edit|close|reopen|comment|delete|transfer|lock|unlock|pin|unpin|develop)([[:space:]]|$)'
    gh_api='(^|[;&|(]|&&)[[:space:]]*gh[[:space:]]+api[[:space:]][^;&|]*issues[^;&|]*(-X|--method|-f|-F|--input|--raw-field|--field)'
    printf '%s' "$cmd" | grep -Eq "$gh_issue" || printf '%s' "$cmd" | grep -Eq "$gh_api" || exit 0
    ;;
  mcp__*)
    printf '%s' "$tool" | grep -Eq 'issue' || exit 0
    printf '%s' "$tool" | grep -Eq '(create|update|edit|add|delete|remove|close|reopen|set|label|assign|transfer|lock)' || exit 0
    ;;
  *) exit 0 ;;
esac
msg="Issue write ahead. Before it: (1) the user authorized this specific write in chat; agreement on content is not that. (2) The body leads with current state and one next action, keeps evidence in the repo or the issue, has at most one open fork with a default, no decision checklists, no agent names. (3) Labels follow the repo's meanings (gh label list); ready-for-agent only with no human decision open. (4) A close is one or two sentences with proof and where leftovers went. Full rules: the issue-hygiene skill (/personal-skills:issue-hygiene in Claude Code, \$issue-hygiene in Codex)."
jq -n --arg m "$msg" '{systemMessage: $m, hookSpecificOutput: {hookEventName: "PreToolUse", additionalContext: $m}}'
