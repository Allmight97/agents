---
name: signing-entitlements
description: Inspect Apple platform signing, entitlements, capabilities, sandbox, Gatekeeper, and provisioning-adjacent failures. Use when diagnosing code signing, trust, HealthKit, iCloud, App Groups, or device install problems.
---

# Signing & Entitlements

## Quick Start

Use this skill when the failure smells like codesigning, entitlements, or
capabilities rather than compilation: launch refusal, missing entitlement,
invalid signature, sandbox mismatch, hardened runtime confusion, trust-policy
rejection, simulator install failure, or physical-device provisioning failure.

## Workflow

1. Inspect the bundle or binary.
   - Locate the `.app` or executable.
   - For macOS, identify the main binary inside `Contents/MacOS/`.
   - For iOS or watchOS simulator builds, inspect the built `.app`, embedded
     extensions, and `Info.plist`.
   - For physical devices, classify provisioning/team/device-trust state before
     suggesting fixes.

2. Read signing details.
   - Use `codesign -dvvv --entitlements :- <path>`.
   - Use `spctl -a -vv <path>` when Gatekeeper behavior matters.
   - Use `plutil -p` for entitlements or Info.plist inspection.

3. Classify the failure.
   - Unsigned or ad hoc signed
   - Wrong identity
   - Entitlement mismatch
   - Hardened runtime issue
   - App Sandbox issue
   - Nested code signing issue
   - Distribution/notarization prerequisite issue
   - Provisioning profile or development team issue
   - Capability/entitlement mismatch, such as HealthKit, iCloud, App Groups,
     widgets, complications, or background modes
   - Device trust, locked device, or unavailable destination

4. Explain the minimum fix path.
   - Say exactly what is wrong.
   - Show the shortest set of validation or repair commands.
   - Distinguish local development problems from distribution problems.
   - Distinguish unsigned simulator compile proof from signed physical-device
     install/run proof.
   - Keep Apple account, team, provisioning, and device trust mutations
     approval-gated.

## Useful Commands

- `codesign -dvvv --entitlements :- <app-or-binary>`
- `spctl -a -vv <app-or-binary>`
- `security find-identity -p codesigning -v`
- `plutil -p <path-to-entitlements-or-plist>`
- `xcodebuild -showBuildSettings -scheme <scheme>`
- `xcrun xctrace list devices`
- `xcrun devicectl list devices`

## Guardrails

- Never invent missing entitlements.
- Do not conflate notarization with local debug signing.
- If the real issue is a build setting or provisioning profile, say so directly.
- Do not use `CODE_SIGNING_ALLOWED=NO` as a device install/run workaround. It is
  only a compile-proof tool for simulator or generic-device validation.
- Do not sign in, change development teams, trust devices, or repair
  provisioning profiles without explicit approval.

## Output Expectations

Provide:
- what artifact was inspected
- what signing state it is in
- the exact failure class
- the minimum fix or validation sequence
