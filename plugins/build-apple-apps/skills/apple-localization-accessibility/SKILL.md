---
name: apple-localization-accessibility
description: Localize and accessibility-test Apple apps with string catalogs, assets, previews, locale/layout proof, Dynamic Type, VoiceOver, contrast, motion, keyboard, switch/control access, and Xcode 27 localization workflows. Use when preparing Apple app UI for multiple languages, accessible interaction, App Store quality, or regression-proof visual behavior.
---

# Apple Localization / Accessibility

## Purpose

Use this skill when text, layout, voice, input, color, motion, or locale behavior can affect whether the app is usable. Treat localization and accessibility as behavior, not polish.

## Localization Workflow

1. Inventory user-visible strings.
   - Prefer string catalogs where the project uses Xcode-native localization.
   - Keep format strings, pluralization, dates, units, and measurements locale-aware.
   - Do not concatenate localized sentence fragments.

2. Check assets and app metadata.
   - Localize assets only when meaning changes by locale.
   - Check app name, widgets, shortcuts, App Intents phrases, permissions, privacy strings, and notifications.

3. Prove layout.
   - Test long strings, right-to-left layout when relevant, narrow widths, Dynamic Type, and platform-specific title/toolbar constraints.
   - Use Xcode 27 localization assistance where it reduces mechanical misses, but verify in the app or previews.

## Accessibility Workflow

1. Define the interaction contract.
   - Every meaningful control has an accessible label, value, hint where useful, and action.
   - Decorative visuals are hidden from accessibility.
   - Dynamic content announces changes only when it helps the user.

2. Check major modes.
   - Dynamic Type and large content sizes
   - VoiceOver order and grouping
   - high contrast and differentiate-without-color
   - reduce motion and reduce transparency
   - keyboard, switch, and pointer/focus behavior where platform-relevant
   - haptics and audio that do not carry exclusive meaning

3. Prove with app-native evidence.
   - Use previews for variant coverage.
   - Use Simulator or device proof for VoiceOver, focus, and layout.
   - Use screenshots only after verifying that controls still fit and do not overlap.

## Strong Defaults

- Put localization keys near the user-facing feature, not in generic dumping grounds.
- Keep accessibility modifiers next to the view that owns the semantics.
- Do not add visible instructional text to compensate for inaccessible controls.
- Do not rely on color alone for health, alert, success, or failure state.

## Output

Provide:

- localized surfaces changed or checked
- accessibility behaviors changed or checked
- exact locale/content-size/mode proof
- remaining untested modes
