---
name: apple-app-intents
description: Design and implement App Intents, App Entities, App Shortcuts, Spotlight, Siri, widgets, controls, and app-routing handoffs for Apple apps. Use when exposing app actions or content to system surfaces across iOS, iPadOS, macOS, watchOS, widgets, Shortcuts, Siri, or Spotlight.
---

# Apple App Intents

## Purpose

Expose the smallest useful action and entity surface to Apple system experiences. Start with verbs and objects people would actually want outside the app, then implement a narrow App Intents layer that routes cleanly into app services or UI.

Consult current Apple Developer documentation when API syntax or platform availability matters.

## Workflow

1. Start with actions, not screens.
   - Identify the 1-3 highest-value actions for Shortcuts, Siri, Spotlight, widgets, controls, or watch surfaces.
   - Prefer verbs such as open, start, log, find, filter, compose, continue, inspect, or summarize.
   - Do not mirror the app's whole navigation tree.

2. Define a small entity surface.
   - Add `AppEntity` only for objects the system needs to understand or route.
   - Keep entity display data narrower than the app's persistence model.
   - Add `EntityQuery`, `EnumerableEntityQuery`, or `AppEnum` only when suggestions, disambiguation, or fixed choices are actually useful.

3. Decide completion mode.
   - Inline intents should complete without opening the app.
   - Open-app intents should route to one clear app destination or workflow.
   - When the app must react inside the main scene, add one predictable handoff path instead of scattering global side effects.

4. Make the surface discoverable.
   - Add `AppShortcutsProvider` for high-value actions.
   - Use direct, user-facing titles and phrases.
   - Reuse the same action/entity model for widgets and controls when those surfaces need the same parameters.

5. Prove the integration.
   - Build the intents target and app target.
   - Verify entity display, parameter resolution, shortcut exposure, and runtime handoff.
   - Summarize exposed actions, backing entities, phrases, and app routing behavior.

## Strong Defaults

- Prefer a dedicated intents target or module for the system-facing layer.
- Keep intent types thin; business logic belongs in app services or domain modules.
- Treat App Intents as system integration infrastructure, not only a Shortcuts feature.
- Prefer one open-app intent, one inline action intent, one or two entities, and one `AppShortcutsProvider` for a first pass.

## Anti-Patterns

- Every tab or screen gets an intent.
- App entities mirror the whole persistence graph.
- Runtime handoff hides in global state with no clear route.
- Shortcut phrases are vague, generic, or taxonomy-driven.

## References

- `references/first-pass-checklist.md`
- `references/example-patterns.md`
- `references/code-templates.md`
- `references/system-surfaces.md`
