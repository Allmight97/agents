# Build macOS Apps Plugin

This is JStar's personal `build-macos-apps` plugin, published through the personal Codex marketplace as `build-macos-apps@personal`.

The curated plugin is source material only. The active install target is this personal plugin; do not keep a second active curated `build-macos-apps` install alongside it.

## Included Skills

- `xcode-27-toolchain`
- `ios-watch-substrate`
- `build-run-debug`
- `test-triage`
- `signing-entitlements`
- `swiftpm-macos`
- `packaging-notarization`
- `swiftui-patterns`
- `liquid-glass`
- `window-management`
- `appkit-interop`
- `view-refactor`
- `telemetry`

## What It Covers

- discovering and verifying Xcode 27, CLT, selected developer directories, SDKs, simulator runtimes, destinations, and attached devices
- building and running macOS apps with shell-first desktop workflows
- creating one project-local `script/build_and_run.sh` entrypoint and wiring `.codex/environments/environment.toml` so the Codex app Run button works for macOS projects
- proving iOS and watchOS simulator builds, installs, launches, screenshots, and logs from the shell
- separating simulator compile proof, simulator runtime proof, generic device compile proof, and signed physical-device runs
- implementing native macOS SwiftUI scenes, menus, settings, toolbars, multiwindow flows, and AppKit interop where it earns its keep
- adopting Apple 27-era Liquid Glass and SwiftUI structure while avoiding legacy compatibility flags as the primary fix path
- tailoring windows, sidebars, inspectors, and toolbars with platform-native structure before custom chrome
- adding lightweight `Logger` / `os.Logger` instrumentation and verifying runtime events with `log stream`
- triaging SwiftPM, Xcode, simulator, and host-app test failures
- inspecting signing identities, entitlements, provisioning-adjacent settings, capabilities, hardened runtime, and Gatekeeper issues
- preparing macOS packaging and notarization workflows for distribution

## What It Does Not Cover

- Android, cross-platform UI frameworks, web app scaffolding, or custom app servers
- App Store Connect release management
- automatic personal-team provisioning repair or Apple account mutation
- broad Xcode GUI automation
- pixel-perfect visual design or design-system generation

## Plugin Structure

- `.codex-plugin/plugin.json`: Codex plugin manifest
- `agents/`: plugin-level UI metadata
- `commands/`: reusable workflow entrypoints
- `skills/`: skill payloads
- `references/apple-27-roadmap.md`: high-ROI later work that is not part of the essential surface yet

## Install And Refresh

The source lives at:

- `/Users/jstar/.agents/plugins/build-macos-apps`

The personal marketplace entry lives at:

- `/Users/jstar/.agents/.agents/plugins/marketplace.json`

Refresh and install:

```bash
codex plugin marketplace upgrade personal
codex plugin add build-macos-apps@personal
```

If a curated stock copy is active, remove the exact installed ID shown by:

```bash
codex plugin list --json
```

Use the exact ID, for example:

```bash
codex plugin remove build-macos-apps@openai-curated
```

Verify the final state with:

```bash
codex plugin list --json --available
```

There should be exactly one installed and enabled `build-macos-apps`, from `personal`.
