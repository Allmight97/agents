# codex-review

One launcher for an adversarial Codex review, for harnesses that call Codex:
Claude Code, Cursor, and Grok Build. Codex's own catalog leaves it out.

The skill (`skills/codex-review/SKILL.md`) tells the calling agent when and how
to run `skills/codex-review/scripts/codex-review`. The script:

- refuses a repository under a temp folder and an `--out` path inside the
  repository, and checks `codex login status`;
- runs `codex exec` in `workspace-write` with network on, from a scratch run
  folder, with no extra writable roots, so the repository stays read-only
  while heredocs, git, `gh`, and uv's cache work;
- feeds the prompt from a file (`codex exec -`), so stdin is never left open;
- prints a start line, a 10-minute heartbeat, and the result path, and stops
  the run's whole process group on a timeout, a silent log, an expired login,
  or an interrupt.

Why the sandbox shape: read-only `codex exec` runs could not write zsh's
heredoc temp file or reach GitHub. `codex sandbox` tests on 2026-10-22
(codex-cli 0.163.0) showed that `workspace-write` from a scratch folder
refuses writes to the repository and allows both.

Accepted risk: `gh` keeps the owner's GitHub login, so the reviewer could
write remotely; the prompt preamble forbids it.

Test: `sh plugins/codex-review/tests/codex-review.test.sh` (a fake `codex`;
no network, no model call). `python3 scripts/test_plugins.py` runs it.
