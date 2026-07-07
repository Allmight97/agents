---
name: apple-27-toolchain
description: Verify Xcode 27, Command Line Tools, Apple SDKs, simulators, devices, XcodeBuildMCP, Xcode native agent access, and Icon Composer 2 before Apple platform work. Use when setup, DEVELOPER_DIR, SDK, runtime, simulator, device, MCP, or toolchain drift could affect macOS, iOS, iPadOS, watchOS, tvOS, or visionOS builds.
---

# Apple 27 Toolchain

## Purpose

Use this skill before blaming app code for failures that may come from the selected developer directory, missing SDKs, unavailable simulator runtimes, stale MCP workflows, or device state.

On JStar's Mac, prefer per-command or per-plugin `DEVELOPER_DIR=/Applications/Xcode-beta.app/Contents/Developer`. Do not change global `xcode-select` unless the user explicitly approves that system-level mutation.

## Workflow

1. Locate the active and candidate developer directories.
   - Run `xcode-select -p`.
   - Check `/Applications/Xcode.app` and `/Applications/Xcode-beta.app`.
   - If needed, use `mdfind "kMDItemCFBundleIdentifier == 'com.apple.dt.Xcode'"`.

2. Prove the selected Xcode.
   - `DEVELOPER_DIR=<path> xcodebuild -version`
   - `DEVELOPER_DIR=<path> xcrun swift --version`
   - `DEVELOPER_DIR=<path> xcrun xcodebuild -showsdks`
   - Report Xcode version, build number, Swift version, selected developer directory, and SDK versions.

3. Prove required platform tooling.
   - macOS SDK: `DEVELOPER_DIR=<path> xcrun --sdk macosx --show-sdk-version`
   - iOS device SDK: `DEVELOPER_DIR=<path> xcrun --sdk iphoneos --show-sdk-version`
   - iOS Simulator SDK: `DEVELOPER_DIR=<path> xcrun --sdk iphonesimulator --show-sdk-version`
   - watchOS SDK: `DEVELOPER_DIR=<path> xcrun --sdk watchos --show-sdk-version`
   - watchOS Simulator SDK: `DEVELOPER_DIR=<path> xcrun --sdk watchsimulator --show-sdk-version`
   - Simulator availability: `DEVELOPER_DIR=<path> xcrun simctl list devices available`
   - Xcode-visible devices: `DEVELOPER_DIR=<path> xcrun xctrace list devices`

4. Prove destination fit for the actual project.
   - Use `DEVELOPER_DIR=<path> xcodebuild -list` for schemes.
   - Use `DEVELOPER_DIR=<path> xcodebuild -showdestinations -scheme <scheme>` before hardcoding a simulator or device destination.
   - Classify simulator compile proof, simulator runtime proof, generic device compile proof, signed physical-device proof, and macOS launch proof separately.

5. Check Apple 27 adjacent tools when relevant.
   - Icon Composer 2: verify `/Applications/Xcode-beta.app/Contents/Applications/Icon Composer.app` before advising layered Liquid Glass icon workflows.
   - XcodeBuildMCP: verify a fresh session can see the configured workflows and `DEVELOPER_DIR`.
   - Xcode native agent access or Device Hub: treat as a UI/state surface; verify availability before depending on it.

6. Keep fixes scoped.
   - Prefer per-command `DEVELOPER_DIR` and plugin `.mcp.json` environment settings.
   - Do not sign in, trust devices, mutate teams, change certificates, download runtimes, or change global developer directory without explicit approval.
   - If an SDK/runtime is missing, report exactly what is missing and verify current Xcode 27 download commands before suggesting one.

## Output

Provide:

- selected developer directory
- exact Xcode and Swift versions
- SDKs and runtimes found or missing
- relevant destinations and devices
- MCP readiness if MCP was involved
- smallest next action

## References

- `../../references/apple-27-roadmap.md`
