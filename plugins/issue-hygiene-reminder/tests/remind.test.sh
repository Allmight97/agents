#!/bin/sh
# Feeds PreToolUse JSON to remind.sh and checks when it reminds. Run from anywhere.
set -u
here=$(cd "$(dirname "$0")" && pwd)
script="$here/../scripts/remind.sh"
fail=0
check() {
  want=$1; name=$2; json=$3
  out=$(printf '%s' "$json" | sh "$script")
  if [ "$want" = reminds ] && ! printf '%s' "$out" | grep -q additionalContext; then
    echo "FAIL (expected reminder): $name"; fail=1
  elif [ "$want" = silent ] && [ -n "$out" ]; then
    echo "FAIL (expected silence): $name"; fail=1
  fi
}
bash_json() { jq -nc --arg c "$1" '{tool_name:"Bash",tool_input:{command:$c}}'; }
check reminds "gh issue create"            "$(bash_json 'gh issue create --title x --body-file /tmp/b.md')"
check reminds "gh issue edit after cd"     "$(bash_json 'cd /repo && gh issue edit 12 --add-label bug')"
check reminds "gh issue close"             "$(bash_json 'gh issue close 12 -c "done"')"
check reminds "gh issue comment"           "$(bash_json 'gh issue comment 12 --body hi')"
check reminds "gh api POST issues"         "$(bash_json 'gh api repos/o/r/issues -X POST -f title=x')"
check silent  "gh issue view"              "$(bash_json 'gh issue view 12 --json body')"
check silent  "gh issue list"              "$(bash_json 'gh issue list --state open')"
check silent  "gh api GET issues"          "$(bash_json 'gh api repos/o/r/issues/12')"
check silent  "gh pr create"               "$(bash_json 'gh pr create --title x')"
check silent  "issue word inside a string" "$(bash_json 'git commit -m "gh issue close later"')"
check reminds "mcp create_issue"           '{"tool_name":"mcp__github__create_issue","tool_input":{}}'
check reminds "mcp add_issue_comment"      '{"tool_name":"mcp__github__add_issue_comment","tool_input":{}}'
check reminds "mcp update_issue"           '{"tool_name":"mcp__github__update_issue","tool_input":{}}'
check silent  "mcp get_issue"              '{"tool_name":"mcp__github__get_issue","tool_input":{}}'
check silent  "mcp list_issues"            '{"tool_name":"mcp__github__list_issues","tool_input":{}}'
check silent  "mcp search_issues"          '{"tool_name":"mcp__github__search_issues","tool_input":{}}'
check silent  "unrelated tool"             '{"tool_name":"Read","tool_input":{"file_path":"/x"}}'
out=$(bash_json 'gh issue close 1' | sh "$script")
printf '%s' "$out" | jq -e '.hookSpecificOutput.hookEventName == "PreToolUse" and (.systemMessage|length) > 0' >/dev/null || { echo "FAIL: output shape"; fail=1; }
[ "$fail" = 0 ] && echo "remind.sh: all checks passed"
exit $fail
