---
name: apple-preview-browser
description: Mirror iOS Simulator into the Codex in-app browser and render SwiftUI package previews with hot reload. Use when the user needs browser-visible Simulator proof, interactive iOS app viewing, SwiftUI preview iteration outside Xcode Canvas, or screenshot evidence from the Codex browser.
---

# Apple Preview Browser

## Purpose

Use this skill when the user needs to see or interact with an iOS Simulator or SwiftUI previews inside the Codex browser. This is proof tooling, not a substitute for a real app build.

Use `apple-build-run-debug` first when the app is not built, launched, or assigned to a known Simulator UDID.

## Simulator Mirror Workflow

1. Obtain an explicit Simulator UDID from XcodeBuildMCP or `DEVELOPER_DIR=<path> xcrun simctl list devices available`.
2. Start `serve-sim` in a long-running terminal scoped to that UDID.

```bash
SIM="<simulator-udid>"
cleanup_serve_sim() {
  npx --yes serve-sim@latest --kill "$SIM" >/dev/null 2>&1 || true
}
trap cleanup_serve_sim EXIT INT TERM HUP
cleanup_serve_sim
npx --yes serve-sim@latest "$SIM"
```

3. Open the exact local URL printed by `serve-sim` in the Codex in-app browser.
4. Verify a real simulator frame is rendering before reporting success.
5. When finished, stop the terminal and wait for the trap to clean up the scoped helper.

Never run an unscoped `serve-sim --kill`; another thread may own a different simulator mirror.

## SwiftUI Preview Workflow

Use the bundled launcher for importable Swift packages:

```bash
node <skill-root>/scripts/swiftui-preview-browser.mjs \
  /absolute/path/to/Package.swift \
  --package-target "<target>" \
  --device "<simulator-udid>"
```

The launcher creates a disposable host outside the user's source tree, installs and launches it in Simulator, and watches package edits. Use `--preview-filter <regex[, ...]>` to show a subset.

Once the launcher prints the selected Simulator UDID, start `serve-sim` for that same UDID and open the printed URL.

## Boundaries

- Support Swift Package-backed `PreviewProvider` and `#Preview` declarations.
- Do not edit the user's `.xcodeproj`, `.xcworkspace`, `Package.swift`, schemes, or build settings to force preview support.
- Do not claim browser proof from a loaded page alone; verify pixels or capture a screenshot of the simulator frame.

## Bundled Scripts

- `scripts/swiftui-preview-browser.mjs`
- `scripts/lib/xcode-project.mjs`
- `scripts/templates/`
