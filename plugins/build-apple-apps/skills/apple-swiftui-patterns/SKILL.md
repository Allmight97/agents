---
name: apple-swiftui-patterns
description: Build and refactor Apple SwiftUI, AppKit interop, Liquid Glass, navigation, windowing, settings, tabs, toolbars, Observation, previews, and platform-native UI structure. Use when shaping Apple app presentation surfaces across macOS, iOS, iPadOS, watchOS, tvOS, or visionOS.
---

# Apple SwiftUI Patterns

## Purpose

Use this skill when the task is UI structure, view refactoring, platform fit, or Apple 27 SwiftUI adoption. Keep the app native: Swift, SwiftUI, AppKit where necessary, WatchKit-adjacent patterns where relevant, and platform-specific behavior behind small interfaces.

## Workflow

1. Identify the platform and surface.
   - macOS window, menu, settings, toolbar, command, inspector, or AppKit bridge
   - iOS/iPadOS navigation, tab, sheet, list, form, toolbar, search, focus, media, or haptics
   - watchOS glanceable flow, widget/control handoff, or companion-app surface
   - cross-platform SwiftUI view, state owner, model adapter, or preview

2. Preserve local architecture.
   - Keep business logic outside view bodies.
   - Use Observation and explicit state ownership where it reduces invalidation and unclear data flow.
   - Add a seam only when there are at least two real adapters, usually production plus test.
   - Prefer platform conditionals at narrow edges instead of mixing incompatible UI assumptions in one view.

3. Adopt Apple 27 UI affordances where they earn their keep.
   - Use Liquid Glass for system-aligned surfaces, not as a generic decoration layer.
   - Prefer native tab, toolbar, split-view, search, sheet, popover, window, command, settings, and inspector APIs before custom chrome.
   - Use Icon Composer 2 only for app/icon work that needs layered Liquid Glass assets.

4. Refactor views deliberately.
   - Split large views around state ownership, repeated subcomponents, platform variants, or testable interactions.
   - Keep file movement small unless the current structure blocks understanding or proof.
   - Update previews when they are useful for the edited surface.

5. Prove behavior.
   - Build through `apple-build-run-debug`.
   - Use previews, screenshots, simulator/browser proof, or macOS launch proof when visual behavior matters.
   - Use `apple-performance-memory` if the concern is jank, body churn, layout cost, or memory growth.

## References

Use only the references needed for the current platform and component:

- `references/ios/`
- `references/macos/`
- `references/appkit/`
- `references/window-management/api-snippets.md`
- `references/liquid-glass-ios.md`
