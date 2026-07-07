---
name: apple-signing-distribution
description: Diagnose Apple signing, entitlements, capabilities, provisioning, device install, sandbox, hardened runtime, Gatekeeper, notarization, TestFlight, and App Store validation issues. Use when builds or launches fail because of trust, identity, entitlement, provisioning, packaging, or distribution state.
---

# Apple Signing / Distribution

## Purpose

Use this skill when the blocker is trust or distribution, not app logic. Classify the surface before changing anything.

Do not mutate Apple ID, team, device trust, certificates, provisioning profiles, keychains, App Store Connect, or global Xcode settings without explicit user approval.

## Failure Classes

- missing, wrong, or extra entitlement
- capability enabled in code but not target/project/profile
- bundle identifier mismatch
- team or signing identity mismatch
- provisioning profile mismatch or expiration
- physical device locked, untrusted, not paired, or not provisioned
- sandbox, hardened runtime, library validation, or app group issue
- Gatekeeper, quarantine, notarization, stapling, or archive/export failure
- TestFlight or App Store validation issue

## Workflow

1. Identify platform and destination.
   - macOS local run, macOS distribution, iOS Simulator, generic iOS device build, physical-device install, watchOS companion, TestFlight, or App Store.
   - Do not treat simulator success as physical-device or distribution success.

2. Collect narrow evidence.
   - Build error snippet
   - target bundle identifier
   - selected team and signing style
   - entitlements file
   - embedded provisioning profile when present
   - signing identity
   - destination device state

3. Inspect artifacts.
   - `codesign -dv --verbose=4 <app>`
   - `codesign --display --entitlements :- <app>`
   - `security find-identity -v -p codesigning`
   - `xcrun notarytool history` only when notarization state is explicitly relevant and credentials are already configured
   - `xcodebuild -showBuildSettings -scheme <scheme>` for signing settings

4. Choose the smallest fix.
   - code/project entitlement mismatch: update the target-owned entitlements or capability setting
   - profile mismatch: explain profile/team/bundle ID mismatch; do not auto-repair account state
   - simulator-only target: use `CODE_SIGNING_ALLOWED=NO` only for simulator proof, not distribution proof
   - physical device: require explicit user approval before trust, account, or provisioning mutation
   - macOS distribution: separate local launch, archive, export, notarize, staple, and Gatekeeper proof

## Output

Provide:

- platform/destination class
- exact signing/distribution failure class
- evidence inspected
- smallest fix
- what was not changed because it requires approval
