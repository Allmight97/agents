# Build Apple Apps Plugin

This is JStar's personal `build-apple-apps` plugin, published through the personal Codex marketplace as `build-apple-apps@personal`.

It replaces the separate `build-macos-apps` and `build-ios-apps` surfaces. The curated plugin caches remain source material only; do not keep overlapping Apple build plugins installed alongside this one.

## Included Skills

- `apple-27-toolchain`
- `apple-build-run-debug`
- `apple-swiftui-patterns`
- `apple-app-intents`
- `apple-foundation-models`
- `apple-localization-accessibility`
- `apple-signing-distribution`
- `apple-performance-memory`
- `apple-preview-browser`

## Apple 27 Defaults

The bundled XcodeBuildMCP server is pinned to `xcodebuildmcp@2.6.2` and runs with:

```bash
DEVELOPER_DIR=/Applications/Xcode-beta.app/Contents/Developer
XCODEBUILDMCP_ENABLED_WORKFLOWS=simulator,simulator-management,device,macos,project-discovery,project-scaffolding,swift-package,debugging,ui-automation,doctor,coverage,utilities,xcode-ide
```

This intentionally avoids mutating global `xcode-select`. On this Mac, the global Command Line Tools path can resolve `xcodebuild` but cannot provide simulator tools such as `simctl`; per-plugin `DEVELOPER_DIR` keeps Apple 27 workflows reproducible inside Codex sessions.

## What It Covers

- verifying Xcode 27, Swift 6.4, SDKs, simulator runtimes, devices, Icon Composer 2, and XcodeBuildMCP readiness
- building, testing, running, launching, logging, screenshotting, and debugging Apple apps across Simulator, macOS, and physical-device paths
- creating project-local build/run scripts and Codex Run-button wiring where that is the lowest-friction durable path
- shaping SwiftUI, AppKit interop, WatchKit-adjacent, Liquid Glass, windowing, settings, tab, toolbar, split-view, preview, and Observation-heavy surfaces
- adding App Intents, entities, shortcuts, Spotlight/Siri/widget/control routes, and one clear in-app handoff path
- adopting Foundation Models with availability checks, guided generation, tool calling, local privacy boundaries, and Instruments proof
- localizing and accessibility-testing Apple apps with string catalogs, previews, Dynamic Type, VoiceOver, contrast, motion, locale, and layout proof
- diagnosing signing, entitlements, provisioning-adjacent settings, packaging, notarization, TestFlight, and App Store validation blockers
- profiling launch/runtime latency, SwiftUI invalidation, hangs, ETTrace output, dSYMs, memgraphs, leaks, and Foundation Models traces
- mirroring iOS Simulator and rendering SwiftUI package previews in the Codex in-app browser

## What It Does Not Cover

- Android, cross-platform UI frameworks, custom app servers, or third-party LLM APIs by default
- automatic Apple account sign-in, device trust, team selection, certificate creation, or provisioning repair
- App Store Connect release automation or Xcode Cloud workflow ownership unless a later accepted design says that complexity earns its keep
- broad Xcode GUI control when shell, XcodeBuildMCP, or app-native proof is cleaner

## Install And Refresh

The source lives at:

- `/Users/jstar/.agents/plugins/build-apple-apps`

The personal marketplace entry lives at:

- `/Users/jstar/.agents/.agents/plugins/marketplace.json`

Refresh and install:

```bash
codex plugin marketplace upgrade personal
codex plugin add build-apple-apps@personal
```

Remove old overlapping Apple build plugins if active:

```bash
codex plugin list --json
codex plugin remove build-macos-apps@personal
codex plugin remove build-ios-apps@openai-curated
```

Verify the final state:

```bash
codex plugin list --json --available
```

There should be exactly one installed and enabled Apple build plugin: `build-apple-apps@personal`.
