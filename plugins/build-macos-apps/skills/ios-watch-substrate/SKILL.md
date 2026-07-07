---
name: ios-watch-substrate
description: Build, run, and prove iOS and watchOS SwiftUI app workflows from macOS using Xcode 27, simulators, devices, capabilities, and logs. Use when target platform is iPhone, iPad, Apple Watch, simulator, watch companion, or Apple platform capability beyond macOS.
---

# iOS / watchOS Substrate

## Quick Start

Use this skill for iOS and watchOS build, install, launch, screenshot, log, and
capability proof from a Mac. If the selected Xcode, SDK, simulator runtime, or
destination is uncertain, use `xcode-27-toolchain` first.

Separate four proofs:

- simulator compile proof
- simulator runtime proof
- generic device compile proof
- signed physical-device install/run proof

These are different failure surfaces. Do not collapse them into one vague
"Xcode build failed" result.

## Workflow

1. Discover the project shape.
   - Look for `.xcworkspace`, `.xcodeproj`, and `Package.swift`.
   - Use `xcodebuild -list` for schemes.
   - Use `xcodebuild -showdestinations -scheme <scheme>` before choosing a
     simulator or device destination.

2. Prove simulator compile.
   - Use a destination that appears in `-showdestinations`.
   - For unsigned simulator compile proof, use `CODE_SIGNING_ALLOWED=NO`.
   - Example shape:

```bash
DEVELOPER_DIR=<xcode-developer-path> \
xcodebuild -scheme <scheme> \
  -destination 'platform=iOS Simulator,name=<available-device>' \
  build CODE_SIGNING_ALLOWED=NO
```

3. Prove simulator runtime behavior when build success is not enough.
   - Prefer a deterministic derived data path when you need to locate the app.
   - Boot the destination, install the built `.app`, launch by bundle ID, take a
     screenshot, and stream logs.

```bash
DERIVED_DATA_DIR=.build/XcodeDerivedData
DEVELOPER_DIR=<xcode-developer-path> \
xcodebuild -scheme <scheme> \
  -destination 'platform=iOS Simulator,name=<available-device>' \
  -derivedDataPath "$DERIVED_DATA_DIR" \
  build CODE_SIGNING_ALLOWED=NO

DEVELOPER_DIR=<xcode-developer-path> xcrun simctl boot <device-udid>
DEVELOPER_DIR=<xcode-developer-path> xcrun simctl bootstatus <device-udid> -b
APP_PATH=$(find "$DERIVED_DATA_DIR/Build/Products" -path '*-iphonesimulator/*.app' -print -quit)
BUNDLE_ID=$(/usr/libexec/PlistBuddy -c 'Print CFBundleIdentifier' "$APP_PATH/Info.plist")
DEVELOPER_DIR=<xcode-developer-path> xcrun simctl install <device-udid> "$APP_PATH"
DEVELOPER_DIR=<xcode-developer-path> xcrun simctl launch <device-udid> "$BUNDLE_ID"
DEVELOPER_DIR=<xcode-developer-path> xcrun simctl io <device-udid> screenshot /tmp/<app>-ios.png
```

4. Handle watchOS deliberately.
   - Use watchOS destinations surfaced by `-showdestinations`; do not guess a
     watch model.
   - Check simulator pairs with `xcrun simctl list pairs` when a watch app
     depends on a paired iPhone simulator.
   - Keep iOS companion and watch extension failures separate in the summary.

5. Prove generic device compile when runtime proof is not needed.
   - Use a generic device destination and `CODE_SIGNING_ALLOWED=NO` only for
     compile/link validation.
   - Do not present this as an installable-device proof.

```bash
DEVELOPER_DIR=<xcode-developer-path> \
xcodebuild -scheme <scheme> \
  -destination 'generic/platform=iOS' \
  build CODE_SIGNING_ALLOWED=NO
```

6. Inspect capabilities and app metadata.
   - Check `.entitlements`, `Info.plist`, bundle identifiers, app groups,
     HealthKit, iCloud, background modes, widgets, complications, and App
     Intents only when relevant to the failure or accepted scope.
   - For iOS 27 SDK builds, verify scene lifecycle and `Info.plist` expectations
     when launch or blank-screen behavior points there.
   - Use `signing-entitlements` for signing and provisioning diagnosis. Do not
     repair Apple account, team, or profile state without explicit approval.

7. Classify failures.
   - Toolchain or destination
   - Build setting
   - Compiler or linker
   - Simulator boot/install/launch
   - Info.plist or scene lifecycle
   - Capability or entitlement
   - Code signing or provisioning
   - Runtime crash, assertion, or blank UI

## Useful Commands

- `DEVELOPER_DIR=<path> xcodebuild -list`
- `DEVELOPER_DIR=<path> xcodebuild -showdestinations -scheme <scheme>`
- `DEVELOPER_DIR=<path> xcrun simctl list runtimes`
- `DEVELOPER_DIR=<path> xcrun simctl list devices available`
- `DEVELOPER_DIR=<path> xcrun simctl list pairs`
- `DEVELOPER_DIR=<path> xcrun simctl boot <udid>`
- `DEVELOPER_DIR=<path> xcrun simctl install <udid> <app>`
- `DEVELOPER_DIR=<path> xcrun simctl launch <udid> <bundle-id>`
- `DEVELOPER_DIR=<path> xcrun simctl io <udid> screenshot <path>`

## Guardrails

- Do not hardcode "iPhone 17 Pro" or any watch model as canonical; discover
  available destinations and use the user's named target when provided.
- Do not use `CODE_SIGNING_ALLOWED=NO` for physical-device install or launch.
- Do not treat a generic device compile as proof that provisioning, install,
  launch, push, HealthKit, or watch pairing works.
- Do not mutate signing teams, Apple account state, device trust, or simulator
  inventories without explicit approval.
- Do not claim UI correctness without at least a simulator screenshot,
  accessibility inspection, or direct user-visible evidence.

## Output Expectations

Provide:
- selected Xcode developer directory when it matters
- scheme and destination used
- proof type: simulator compile, simulator runtime, generic device compile, or signed device run
- command run
- build/install/launch result
- screenshot or log path when produced
- top failure category and smallest next proof step
