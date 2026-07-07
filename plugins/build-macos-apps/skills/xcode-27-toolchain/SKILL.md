---
name: xcode-27-toolchain
description: Verify Xcode 27, Command Line Tools, Apple SDKs, destinations, simulators, and device readiness before Apple platform builds. Use when setup, DEVELOPER_DIR, SDK, simulator runtime, or toolchain drift could affect macOS, iOS, or watchOS work.
---

# Xcode 27 Toolchain

## Quick Start

Use this skill before blaming app code for failures that may come from Xcode,
Command Line Tools, selected developer directories, missing SDKs, stale
simulator runtimes, or unavailable destinations.

Prefer per-command `DEVELOPER_DIR` when the machine has both Command Line Tools
and a full Xcode install. Do not change global `xcode-select` unless the user
explicitly asks for that system-level mutation.

## Workflow

1. Locate candidate developer directories.
   - Check `xcode-select -p`.
   - Check likely full Xcode paths such as `/Applications/Xcode.app` and
     `/Applications/Xcode-beta.app`.
   - If needed, search with `mdfind "kMDItemCFBundleIdentifier == 'com.apple.dt.Xcode'"`.

2. Prove the selected toolchain.
   - Run `DEVELOPER_DIR=<path> xcodebuild -version`.
   - Run `DEVELOPER_DIR=<path> xcrun swift --version`.
   - Run `DEVELOPER_DIR=<path> xcrun xcodebuild -showsdks`.
   - Report the exact Xcode, build number, Swift version, and selected
     developer directory.

3. Prove platform SDK availability.
   - macOS: `DEVELOPER_DIR=<path> xcrun --sdk macosx --show-sdk-version`
   - iOS device: `DEVELOPER_DIR=<path> xcrun --sdk iphoneos --show-sdk-version`
   - iOS simulator: `DEVELOPER_DIR=<path> xcrun --sdk iphonesimulator --show-sdk-version`
   - watchOS device: `DEVELOPER_DIR=<path> xcrun --sdk watchos --show-sdk-version`
   - watchOS simulator: `DEVELOPER_DIR=<path> xcrun --sdk watchsimulator --show-sdk-version`

4. Prove simulator and device inventory.
   - List runtimes with `DEVELOPER_DIR=<path> xcrun simctl list runtimes`.
   - List available devices with `DEVELOPER_DIR=<path> xcrun simctl list devices available`.
   - List Xcode-visible devices with `DEVELOPER_DIR=<path> xcrun xctrace list devices`.
   - For a specific scheme, prefer
     `DEVELOPER_DIR=<path> xcodebuild -showdestinations -scheme <scheme>`.

5. Classify missing pieces.
   - Wrong selected developer directory
   - Command Line Tools selected when full Xcode is required
   - Missing platform SDK
   - Missing simulator runtime
   - Destination mismatch
   - Physical device unavailable, locked, untrusted, offline, or not provisioned

6. Keep fixes scoped.
   - Use per-command `DEVELOPER_DIR` for build proof.
   - If the runtime is missing, tell the user which platform/runtime is missing
     and verify the current `xcodebuild -help` platform-download options before
     suggesting a command.
   - Do not sign in, mutate Apple account state, trust a device, or change
     global Xcode selection without explicit approval.

## Useful Commands

- `xcode-select -p`
- `DEVELOPER_DIR=<path> xcodebuild -version`
- `DEVELOPER_DIR=<path> xcrun swift --version`
- `DEVELOPER_DIR=<path> xcrun xcodebuild -showsdks`
- `DEVELOPER_DIR=<path> xcrun simctl list runtimes`
- `DEVELOPER_DIR=<path> xcrun simctl list devices available`
- `DEVELOPER_DIR=<path> xcrun xctrace list devices`
- `DEVELOPER_DIR=<path> xcodebuild -showdestinations -scheme <scheme>`

## Guardrails

- Do not assume `/Applications/Xcode.app` is the active or newest toolchain.
- Do not hardcode a simulator name when `-showdestinations` can reveal the
  valid destinations for the scheme.
- Do not treat generic device builds, simulator builds, and physical-device
  install/run proof as equivalent.
- Do not change global `xcode-select` just to make one build pass.

## Output Expectations

Provide:
- selected developer directory
- exact Xcode version and build number
- Swift version
- SDK versions found or missing
- relevant simulator runtimes and destinations
- the smallest next action if a required toolchain piece is missing
