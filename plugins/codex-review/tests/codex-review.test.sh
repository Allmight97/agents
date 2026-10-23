#!/bin/sh
# Runs codex-review against a fake codex on PATH; no network, no model call. Run from anywhere.
set -u
here=$(cd "$(dirname "$0")" && pwd)
script="$here/../skills/codex-review/scripts/codex-review"
work=$(mktemp -d "${TMPDIR:-/tmp}/codex-review-test.XXXXXX")
trap 'rm -rf "$work"' EXIT
mkdir -p "$work/bin" "$work/repo" "$work/tmp"
git -C "$work/repo" init -q
echo "Review the README." > "$work/brief.md"

# FAKE_LOGIN=0 fails `login status`. FAKE_MODE picks what `exec` does. The fake
# records its argv and stdin so the test can check how codex was launched.
cat > "$work/bin/codex" <<'EOF'
#!/bin/sh
if [ "$1" = login ]; then [ "${FAKE_LOGIN:-1}" = 1 ]; exit; fi
printf '%s\n' "$@" > "$FAKE_DIR/argv"; cat > "$FAKE_DIR/stdin"
out=""; while [ $# -gt 0 ]; do [ "$1" = -o ] && out=$2; shift; done
case "$FAKE_MODE" in
  ok) echo "codex working"; printf 'finding one\n' > "$out" ;;
  empty) echo "codex working" ;;
  fails) echo "codex broke"; exit 7 ;;
  auth) echo "2026-10-17T00:14:39.664888Z ERROR codex_login::auth::manager: Failed to refresh token"; sleep 30 ;;
  quote) echo "the brief says: ERROR codex_login:: is the auth pattern"; printf 'ok\n' > "$out" ;;
  silent) echo "codex working"; sleep 30 & echo $! > "$FAKE_DIR/child"; wait ;;
esac
EOF
chmod +x "$work/bin/codex"

fail=0
run() {
  want=$1; name=$2; shift 2
  out=$(cd "$work/repo" && TMPDIR="$work/tmp" PATH="$work/bin:$PATH" FAKE_DIR="$work" "$script" "$@" 2>&1)
  got=$?
  if [ "$got" != "$want" ]; then echo "FAIL ($name): exit $got, expected $want"; echo "$out"; fail=1; fi
  last_out=$out
}

FAKE_MODE=ok run 0 "a review completes" "$work/brief.md"
review=$(printf '%s\n' "$last_out" | sed -n 's/^\[codex-review\] review: //p')
[ "$(cat "$review" 2>/dev/null)" = "finding one" ] || { echo "FAIL: the review line names no review file"; fail=1; }
grep -qx -- - "$work/argv" || { echo "FAIL: codex does not read the prompt from stdin"; fail=1; }
grep -qx workspace-write "$work/argv" && grep -qx sandbox_workspace_write.network_access=true "$work/argv" \
  || { echo "FAIL: codex not launched in workspace-write with network"; fail=1; }
workdir=$(sed -n '/^-C$/{n;p;}' "$work/argv")
case "$workdir" in "$(cd "$work/repo" && pwd -P)"* | "") echo "FAIL: codex's working folder is not a separate run folder: '$workdir'"; fail=1 ;; esac
grep -q "reviewing the repository at $(cd "$work/repo" && pwd -P)" "$work/stdin" \
  || { echo "FAIL: the prompt does not name the repository"; fail=1; }
grep -q "Review the README." "$work/stdin" || { echo "FAIL: the brief is not in the prompt"; fail=1; }

FAKE_MODE=ok run 0 "brief on stdin" - < "$work/brief.md"
FAKE_MODE=quote run 0 "log text that quotes the auth pattern is not an auth error" "$work/brief.md"
FAKE_MODE=empty run 1 "codex ends without a review" "$work/brief.md"
FAKE_MODE=fails run 7 "codex's own failure code passes through" "$work/brief.md"
FAKE_MODE=auth run 126 "an expired login stops the run" "$work/brief.md"
FAKE_MODE=silent run 125 "a silent log stops the run" --stall 4s "$work/brief.md"
FAKE_MODE=silent run 124 "the timeout stops the run" --timeout 4s --stall 1m "$work/brief.md"
kill -0 "$(cat "$work/child")" 2>/dev/null && { echo "FAIL: a stopped run left codex's child running"; fail=1; }
mkdir -p "$work/tmp/repo"
FAKE_MODE=ok run 2 "a repository in the temp folder is refused" --repo "$work/tmp/repo" "$work/brief.md"
FAKE_MODE=ok run 2 "--out inside the repository is refused" --out "$work/repo/review.md" "$work/brief.md"
FAKE_LOGIN=0 FAKE_MODE=ok run 3 "not logged in" "$work/brief.md"
FAKE_MODE=ok run 2 "no brief"
FAKE_MODE=ok run 2 "bad duration" --stall soon "$work/brief.md"
FAKE_MODE=ok run 2 "an option without its value" "$work/brief.md" --repo
[ "$fail" = 0 ] && echo "codex-review: all checks passed"
exit "$fail"
