---
name: apple-build-run-debug
description: Build, run, test, launch, log, screenshot, and debug Apple apps with Xcode 27, XcodeBuildMCP, xcodebuild, SwiftPM, simulators, devices, and macOS paths. Use when launching an app, proving a build, inspecting runtime behavior, wiring a Codex Run button, or diagnosing Apple build/test/runtime failures.
---

# Apple Build / Run / Debug

## Purpose

Use this skill for end-to-end Apple app proof. Classify the project and platform first, then choose XcodeBuildMCP, `xcodebuild`, SwiftPM, or a project-local script based on the narrowest reliable proof path.

Use `apple-27-toolchain` first when `DEVELOPER_DIR`, SDKs, destinations, simulator runtimes, or MCP availability are uncertain.

## Project Discovery

1. Check whether the workspace is inside a git repo before adding any tooling.
2. Look for `.xcworkspace`, `.xcodeproj`, and `Package.swift`.
3. Use `xcodebuild -list` or XcodeBuildMCP project discovery to identify schemes.
4. Confirm target platform: macOS, iOS, iPadOS, watchOS, tvOS, visionOS, or package-only Swift.
5. If more than one project or scheme fits, state the default and why.

## MCP Workflow

When XcodeBuildMCP is available, prefer it for simulator, device, macOS, UI automation, log capture, screenshots, coverage, and Xcode-aware discovery.

Before the first MCP build, run, or test action in a fresh session:

1. Show current MCP session defaults.
2. If project/workspace, scheme, and simulator/device are already correct, run the build/run/test action directly.
3. If defaults are missing, set only the needed defaults from real project discovery.
4. Do not boot a simulator as a separate prerequisite when the MCP build/run tool owns booting.
5. Verify launch with UI description, screenshot, logs, process proof, or destination-specific output before reporting success.

Use shell commands immediately when MCP output is ambiguous, unavailable, stale, or less reproducible than a direct command.

## Shell Workflow

Use `DEVELOPER_DIR=/Applications/Xcode-beta.app/Contents/Developer` unless the repo or user names another Xcode.

Common proofs:

- list schemes: `DEVELOPER_DIR=<path> xcodebuild -list`
- show destinations: `DEVELOPER_DIR=<path> xcodebuild -showdestinations -scheme <scheme>`
- iOS Simulator build: `DEVELOPER_DIR=<path> xcodebuild -scheme <scheme> -destination 'platform=iOS Simulator,name=<device>' build CODE_SIGNING_ALLOWED=NO`
- macOS build: `DEVELOPER_DIR=<path> xcodebuild -scheme <scheme> -destination 'platform=macOS' build CODE_SIGNING_ALLOWED=NO`
- SwiftPM build: `DEVELOPER_DIR=<path> swift build`
- SwiftPM test: use the repo's documented test wrapper when one exists

## Mac Run Button Workflow

For macOS apps where repeated local launch matters, create or update one project-local `script/build_and_run.sh` and wire `.codex/environments/environment.toml` to the Run action.

Use `references/run-button-bootstrap.md` as the canonical script and environment contract. Keep the run script outside app source.

Do not turn that macOS run script into a simulator runner. Simulator and device workflows belong in XcodeBuildMCP or explicit `xcodebuild` commands.

## Failure Classification

Classify the first real blocker:

- selected Xcode or missing SDK/runtime
- scheme/destination mismatch
- compiler or Swift language error
- linker or package resolution error
- signing, entitlement, provisioning, or device trust error
- launch, crash, log, or UI automation failure
- test harness or assertion failure

Quote the smallest useful error snippet and state the next command or edit.

## References

- `references/run-button-bootstrap.md`
