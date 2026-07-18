---
name: use-proton-pass
description: Read credentials and secrets from Proton Pass through pass-cli with scoped agent sessions and non-disclosing handoffs. Use when retrieving passwords, TOTP codes, pass:// references, attachments, or other vault fields; logging into a website or application; running commands with Proton Pass secrets; inspecting vault, item, share, agent, or access-token metadata; using Proton Pass SSH keys; or diagnosing pass-cli installation, authentication, session, and permission failures.
---

# Use Proton Pass

Use Proton Pass as the read-only credential source without placing secret values in model-visible output. Treat broad visibility as permission to find the requested item, not an invitation to inspect unrelated contents.

## Resolve the helpers

Resolve paths from this skill's installed directory, not the current working directory:

- `scripts/pass-agent`: run `pass-cli` in the dedicated machine-local agent session.
- `scripts/pass-agent-login`: authenticate that session from a hidden terminal prompt.
- `scripts/pass-copy-secret`: copy one field or TOTP code to the system clipboard without printing it.
- `scripts/pass-clear-clipboard`: clear the system clipboard after use.

The default session lives at `~/.agents/state/proton-pass/codex`. Override it with `PROTON_PASS_SESSION_DIR` when isolation between agents or tasks is required. Never commit that directory.

Read `references/verified-contract.md` before diagnosing permissions, choosing a command not covered below, using attachments or SSH keys, or claiming what Proton audits. It records the verified 2.2.3 behavior and known documentation mismatches.

## Start a task

1. Run `pass-cli --version` when installation is unverified. If missing, use the official installation instructions at <https://protonpass.github.io/pass-cli/get-started/installation/>.
2. Run `scripts/pass-agent info >/dev/null`, then `scripts/pass-agent test >/dev/null`. This catches a locally present session that the server has invalidated. Do not repeat both checks before every command.
3. If the session is invalid, ask the user to run `scripts/pass-agent-login` in a visible terminal. Do not ask them to paste a PAT into chat.
4. Identify the exact destination, account/item, fields, and requested action. Ask only when ambiguity could select the wrong account or transmit a credential to the wrong destination.

Do not log out or reauthenticate after an arbitrary failure. First classify authentication, authorization, lookup, argument, or network failure. Clear a session only after confirmed stale-session evidence.

## Choose the narrowest path

### Access a website or application

1. Prefer an existing authenticated session or Proton Pass extension autofill in the user's requested browser.
2. Otherwise retrieve only the required field with `pass-copy-secret`, focus the verified field on the authorized destination, and paste without reading the clipboard.
3. Clear the clipboard immediately after each field is accepted. Retrieve TOTP only when the site is ready for it.
4. Verify the destination origin before entering a password, TOTP, recovery code, payment field, or identity field.

Use Chrome when the task depends on the user's Chrome profile, sessions, or extensions. Respect an explicit in-app Browser choice. Use Computer Use for browser chrome, extension popups, or a browser that the dedicated browser tools cannot control. If no supported surface can paste without revealing the value to the model, ask the user to paste it.

The user's request to log into a named destination authorizes that ordinary login. It does not authorize saving the credential, changing it, accepting unexpected permissions, or using the same credential at another origin.

### Supply a secret to a command or file

Prefer `pass-agent run` or `pass-agent inject` with `pass://` references so the secret travels directly to the target process or file rather than through chat. Set `PROTON_PASS_AGENT_REASON` first.

- Keep `run`'s default masking. The helper blocks `--no-masking`.
- Give `inject` a new or explicitly approved output path. The helper requires `--out-file`; pass-cli otherwise renders to stdout. The default Unix mode is `0600`.
- Do not print the rendered environment, command, file, or debug trace when it could contain secrets.

Use the verified 2.2.3 command shapes:

```bash
export PROTON_PASS_AGENT_REASON='Deploy the requested service using its database credential'
export DB_PASSWORD='pass://<vault-or-share>/<item>/password'
scripts/pass-agent run -- <command> <arguments>
unset DB_PASSWORD

export PROTON_PASS_AGENT_REASON='Render the requested service configuration'
scripts/pass-agent inject --in-file <template> --out-file <new-or-approved-output>
```

`run` resolves secret references already present in the environment or supplied through `--env-file`; it has no `--env` flag. `inject` takes its template through `--in-file`, not as a positional argument.

### Inspect or retrieve vault data

- Use `share list`, `vault list`, or `item list --output json` only when discovery is needed. Do not add `--show-secrets`.
- Narrow by vault, item title/ID, item type, or `pass://` URI before reading fields.
- Use `item view --field <field>` instead of reading a complete item. `view`, `get`, and `show` are the 2.2.3 aliases; do not use the stale documented `read` alias.
- Provide `PROTON_PASS_AGENT_REASON` for audited commands. State the actual destination and task, for example `Log into billing.example.com as requested to download the July invoice`.
- Summarize metadata rather than reproducing vault names, item titles, IDs, usernames, notes, or URLs unless the user needs those exact values.

### Stay read-only

Do not create, update, move, trash, delete, share, transfer, import, or export Proton Pass data. Do not create, renew, grant, change, or revoke agent/PAT access. The `pass-agent` helper enforces this boundary even when the underlying token has a broader role.

When checking scope from an owner session, use `personal-access-token access list-access`; its `role` is the token's effective grant. The agent session cannot list or manage PATs. Do not infer token authority from `share list`, whose `share_role` describes that logged-in principal's relationship to the underlying vault.

`Viewer` is the read-only role. A vault-level viewer grant exposes all current and future items in that vault for reading; an item-level viewer grant exposes only that item. Either is a formally supported Proton Pass agent configuration.

### Use attachments or SSH keys

- Treat an attachment download as an explicit file-write task. Confirm the destination path and whether overwriting is allowed before running it.
- In pass-cli 2.2.3, attachment downloads and SSH-agent key scans/loads do not emit the same agent reason event as `item view`, TOTP, `run`, or `inject`. Do not describe those operations as audited until a later version is verified.
- `ssh-agent load`, `start`, and `daemon start` place decrypted private-key material in an SSH agent process. Run them only for an explicit SSH task and narrow by vault/share when possible.
- Never pass `--create-new-identities`; it can create Proton Pass items and the helper blocks it.

## Keep secrets out of durable surfaces

- Never place a PAT, password, TOTP seed/code, recovery code, private key, session file, vault export, or retrieved secret in a skill, repository, memory, issue, commit, message, command argument, or tool output.
- Passing an agent token from Proton's creation flow to its intended agent is expected. Persist the resulting isolated session, not the raw token.
- Do not read browser password stores, cookies, local storage, Proton session files, or clipboard contents.
- Do not enable shell tracing around Proton Pass commands.
- If a secret reaches an unintended audience or durable surface, report the exact exposure boundary and recommend rotation. Do not call an intended one-time agent handoff a compromise by itself.

## Diagnose failures

Use this order:

1. `scripts/pass-agent info >/dev/null`
2. `scripts/pass-agent test`
3. the failed command's `--help`
4. a narrow share/vault/item metadata check
5. reauthentication only for confirmed authentication expiry

Report whether the failure is installation, session, network, permission, lookup ambiguity, unsupported browser interaction, or command usage. Do not dump full command output when it contains account or vault metadata.
