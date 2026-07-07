---
name: test-triage
description: Triage Apple platform tests across Xcode and SwiftPM. Use when narrowing macOS, iOS, watchOS, simulator, host-app, assertion, crash, or setup failures.
---

# Test Triage

## Quick Start

Use this skill to run the smallest meaningful test scope first, classify
failures precisely, and avoid treating every test failure like a product bug.
For toolchain or destination uncertainty, use `xcode-27-toolchain` before
rerunning tests.

## Workflow

1. Detect the test harness.
   - Use `xcodebuild test` for Xcode-based projects.
   - Use `swift test` for SwiftPM packages.
   - For iOS and watchOS, list destinations with
     `xcodebuild -showdestinations -scheme <scheme>` before choosing a
     simulator.

2. Narrow the scope.
   - If the user gave a target, product, or test filter, use it.
   - If not, prefer the smallest likely failing target before a full suite.
   - Prefer a single test plan, test target, or test identifier when available.
   - Use `test-without-building` only after a successful build-for-testing
     artifact exists and the environment has not changed.

3. Classify the result.
   - Build failure
   - Assertion failure
   - Crash or signal
   - Async timing or flake
   - Environment or fixture setup issue
   - Missing entitlement or host app issue
   - Simulator runtime or destination issue
   - Watch/iPhone pairing issue
   - Code signing or provisioning issue for device tests

4. Rerun intelligently.
   - Use focused reruns when a specific case fails.
   - Avoid burning time on full-suite reruns without new information.

5. Summarize clearly.
   - What command ran
   - Which tests failed
   - What kind of failure it was
   - The best next proof step or fix path

## Guardrails

- Distinguish compilation failures from test execution failures.
- Call out when a test assumes a simulator, host app, paired watch, HealthKit
  capability, or physical-device-only behavior.
- Do not use `CODE_SIGNING_ALLOWED=NO` for physical-device test execution.
- Mark likely flakes as such instead of overstating confidence.

## Useful Commands

- `swift test`
- `xcodebuild test -scheme <scheme> -destination '<destination>'`
- `xcodebuild test -scheme <scheme> -only-testing:<target>/<case>`
- `xcodebuild build-for-testing -scheme <scheme> -destination '<destination>'`
- `xcodebuild test-without-building -scheme <scheme> -destination '<destination>'`

## Output Expectations

Provide:
- the command used
- the smallest failing scope
- the top failure category
- a concise explanation of the likely cause
- the next rerun or fix step
