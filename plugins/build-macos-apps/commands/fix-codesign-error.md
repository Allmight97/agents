# /fix-codesign-error

Inspect an Apple platform signing, entitlement, capability, or trust failure and
explain the minimum fix path.

## Arguments

- `app`: path to `.app` bundle, extension, or binary (optional)
- `identity`: signing identity hint (optional)
- `mode`: `inspect` or `repair-plan` (optional, default: `inspect`)

## Workflow

1. Inspect the app bundle, executable, signing info, entitlements, and relevant `Info.plist`.
2. Determine whether the problem is identity, provisioning, hardened runtime, sandboxing, capability mismatch, device trust, or trust policy.
3. Summarize the exact failure class in plain language.
4. Provide the minimal repair sequence or validation command.

## Guardrails

- Never invent entitlements; read them from the binary or source files.
- Distinguish local development signing problems from distribution or notarization failures.
- Prefer verifiable commands like `codesign -d`, `spctl`, and `plutil` over guesswork.
- Do not mutate Apple account, team, provisioning, or device trust state without explicit approval.
