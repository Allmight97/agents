# Verified pass-cli contract

Use this reference when pass-cli behavior, permission scope, audit coverage, or a less-common command matters. It reflects pass-cli 2.2.3 and Proton's public documentation and source at commit `554fa9217c9451c3accaa52ad39d9141a9089911` (2026-07-10). Recheck the current release before relying on version-sensitive details.

## Authority and scope

- An agent is a personal access token with agent audit behavior.
- A grant may target an entire vault or one item. A vault grant covers all current and future items in that vault.
- `Viewer` can read but cannot edit, delete, or share. `Editor` and `Manager` are not read-only.
- `personal-access-token access list-access` in the token owner's session reports the token's effective grant type and role. An agent session cannot list or manage PATs.
- `share list` reports the logged-in principal's share relationship. Its `share_role` is not a substitute for the token's grant record.
- Proton's web creation flow intentionally presents the token and setup instructions for transfer to the AI agent. That intended one-time handoff is not, by itself, credential exposure.

## Session behavior

- `PROTON_PASS_SESSION_DIR` isolates session data. The skill defaults to `~/.agents/state/proton-pass/codex`.
- On macOS, the default key provider stores the session encryption key in Keychain. Do not switch automatically to the filesystem or environment key providers.
- `info` describes the local session; `test` verifies an authenticated connection. A primary user report shows that server-side invalidation can leave stale local session state, so task startup runs both once.
- `logout` removes local authentication data and the stored key. `logout --force` removes local state without completing remote invalidation. Use either only for an intended logout or confirmed stale-session recovery.

## Item reads and references

- `item view`, `item get`, and `item show` are the live 2.2.3 aliases. One public subpage still says `item read`; live help and source do not support it.
- `item view --field <name>` prints only the field value. Prefer IDs when titles are duplicated.
- A secret reference is `pass://<vault-or-share>/<item>/<field>`. Use exact field names. Do not depend on case behavior because the public reference page is internally inconsistent.
- A TOTP field reference returns the current code by default. `?totp=uri` returns the underlying `otpauth://` value; never expose or paste that URI as a login code.
- `item list --show-secrets` requires JSON and is rejected for agent sessions. The skill forbids it on every session.

## Reasons and audit coverage

- `PROTON_PASS_AGENT_REASON` must be non-empty and at most 300 characters for audited agent operations.
- Source verifies reason enforcement for `item view`, `item totp`, secret resolution used by `run` and `inject`, and item/vault mutations. The public agent command page's command list is incomplete for TOTP, `run`, and `inject`.
- Source in 2.2.3 does not send an agent monitor event for attachment downloads or SSH-agent key scans/loads. Proton's broad marketing statement that every access is logged should not be treated as a command-level guarantee for those paths.

## Secret transport

- `run` resolves references in inherited environment values and files passed with `--env-file`; it has no `--env` flag. It masks resolved secret values in child stdout/stderr by default. Never use `--no-masking`.
- `inject` resolves `{{ pass://... }}` templates. Supply the template with `--in-file`. Without `--out-file`, it writes rendered secrets to stdout. With `--out-file`, the Unix default mode is `0600`.
- `item totp --output json` returns an object containing a `tokens` map. The helper accepts exactly one entry and copies only its value; human output includes the field label.
- Attachment download creates or truncates its output path. Confirm the path and overwrite intent first.
- SSH-agent operations decrypt private keys into an agent process. `--create-new-identities` can write newly added keys back to Proton Pass and is blocked.

## Known reports and limits

- A firsthand Proton UserVoice report says server-revoked sessions can remain locally present until logout/login; use `test` before assuming the session is valid.
- Early community reports include ordinary platform rough edges such as a Windows PATH installer bug that Proton subsequently fixed. No Proton or GitHub security advisory was found for the agent-token feature as of this verification.
- A community post calls browser approval from an already-authenticated Proton web session a vulnerability. That is a concern about the web session's authentication boundary, not evidence that a scoped PAT becomes writable or exceeds its recorded grants.

## Primary sources

- <https://protonpass.github.io/pass-cli/commands/agent/>
- <https://protonpass.github.io/pass-cli/commands/personal-access-token/>
- <https://protonpass.github.io/pass-cli/objects/share/>
- <https://protonpass.github.io/pass-cli/get-started/configuration/>
- <https://protonpass.github.io/pass-cli/commands/item/>
- <https://protonpass.github.io/pass-cli/commands/run/>
- <https://protonpass.github.io/pass-cli/commands/inject/>
- <https://protonpass.github.io/pass-cli/commands/ssh-agent/>
- <https://github.com/protonpass/pass-cli/tree/554fa9217c9451c3accaa52ad39d9141a9089911>
- <https://proton.me/blog/pass-access-tokens>
- <https://protonmail.uservoice.com/forums/953584-proton-pass-authenticator/suggestions/51006544-pass-cli-doesn-t-detect-server-side-session-invali>
