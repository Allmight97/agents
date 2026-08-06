---
name: grok-cli
description: Run and manage xAI Grok Build through the local Grok CLI. Use for Grok 4.5 code feedback, a bounded external implementation lane, Grok authentication or updates, or diagnosing Grok CLI configuration and isolation.
---

# Grok CLI

Use Grok Build as an external coding agent, not a native Codex subagent. Run it through `scripts/grok-isolated` so its personal state and compatibility discovery are isolated from the task.

Read [references/grok-build-contract.md](references/grok-build-contract.md) before authentication, an update, a networked model call, or any implementation run.

## Establish a clean agent context

1. Resolve `grok` and the installed skill directory. Do not assume either is available from a prior machine.
2. Run the context preflight before the first model call for a repository:

   ```bash
   <skill-dir>/scripts/grok-isolated --cwd <absolute-repository-path> --check-only
   ```

3. Stop if preflight reports a foreign instruction, skill, plugin, hook, MCP server, agent, or configuration source. Do not weaken the check by adding a broad allowlist. Decide whether that source belongs in the Grok task, then remove it from discovery or use a different task boundary.

The wrapper gives Grok a dedicated `GROK_HOME`, turns off Claude and Cursor
compatibility cells, disables automatic updates, pins the strict sandbox and
gitignore filtering, and verifies the resulting discovery graph. It retains
only instructions inside the requested working directory. It creates local
agent state under `~/.agents/state/grok-cli` unless `GROK_CLI_STATE_DIR` names
another directory; that state is machine-local and must not be committed.

## Ask Grok for feedback

Treat the first request in a task as an external, potentially billed operation.
Identify the repository, prompt, model, reasoning effort, and exact disclosure
manifest. Authorization must name the patch and context files that may leave the
machine; a general statement that "code" may leave is insufficient.

Use a single-turn, read-only request against a disclosure bundle by default:

1. Agree the diff base and paths under review.
2. Create an OS-temp directory containing only the approved patch and context
   files. Do not copy `.git`, the repository tree, ignored files, or untracked
   files unless each untracked file is named, inspected, and explicitly approved.
3. Inspect the bundle locally for credentials, tokens, private keys, personal
   data, and unrelated customer or repository content. Remove or redact them.
4. Show the bundle manifest and obtain authorization for that exact disclosure.
5. Run Grok with the bundle—not the live repository—as its working directory.

`dontAsk` plus only `Read` and `Grep` prevents unapproved tools; strict sandbox,
gitignore filtering, and disabled memory, subagents, and web search reduce the
remaining surface. Do not treat them as substitutes for the disclosure bundle.

```bash
<skill-dir>/scripts/grok-isolated --cwd <absolute-disclosure-bundle> -- \
  --no-auto-update \
  -m grok-4.5 \
  --reasoning-effort high \
  --permission-mode dontAsk \
  --allow Read \
  --allow Grep \
  --no-memory \
  --no-subagents \
  --disable-web-search \
  --output-format json \
  -p '<bounded review question>'
```

State the requested output shape in the prompt: findings ordered by severity,
bundle-relative file paths and lines, evidence, and no patch application. Read
`json` or `streaming-json` output as an external opinion, then verify each claim
against the live repository before acting on it. Remove the temporary bundle
after the result and receipt are captured.

## Use Grok for implementation

Do not turn a feedback call into an implementation call. Before the first effectful run, record and obtain authorization for:

- the exact repository and write destination;
- the exact repository content that may be disclosed, including any untracked
  files needed for the task;
- the bounded task and acceptance proof;
- permitted commands, network access, tests, account/device state, and data isolation;
- branch or worktree policy, commit authority, and whether Grok may create files;
- the rollback boundary.

Start with Grok producing a patch or a plan. Review and test it locally before
accepting it. Use `--permission-mode acceptEdits` only when the owner has
explicitly authorized file edits. The wrapper rejects `--always-approve`, its
`--yolo` alias, and `bypassPermissions` because those modes can approve shell
operations as well as edits.

Run the same preflight after a Grok CLI update or an isolation/configuration change. Do not claim the agent is isolated from a label, sandbox name, temporary directory, or successful previous run; require current `grok inspect --json` evidence from the wrapper.

## Manage authentication and lifecycle

Keep API keys out of prompts, source, shell history, and model-visible output. Use browser or device-code login only when the user has authorized that account action. Use a per-session `XAI_API_KEY` only when the user provides an approved secret-injection path.

Run `grok update` only when explicitly requested. The normal model-call command includes `--no-auto-update` so a review cannot silently change the CLI. Re-run preflight and a small read-only feedback request after a deliberate update.
