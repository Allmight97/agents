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

2. Choose the current App Intents contract before defining entities.
   - For a supported schema domain, use its domain model only when it matches the app's real objects and behavior; otherwise keep a narrow app-specific intent and entity surface.
   - When the feature has more than one possible execution target or supported mode, state which targets and modes are allowed before implementing it.
   - Confirm that the app owns, or is authorized to act on, each sensitive or shared entity before exposing it to a system surface.
   - Use a stable cross-device entity identity only when the intent must resolve the same object across devices, restores, or shared state; do not add sync identity by default.

3. Define a small entity surface.
   - Add `AppEntity` only for objects the system needs to understand or route.
   - Keep entity display data narrower than the app's persistence model.
   - Add `EntityQuery`, `EnumerableEntityQuery`, or `AppEnum` only when suggestions, disambiguation, or fixed choices are actually useful.

4. Decide completion mode.
   - Inline intents should complete without opening the app.
   - Open-app intents should route to one clear app destination or workflow.
   - When the app must react inside the main scene, add one predictable handoff path instead of scattering global side effects.

5. Make the surface discoverable.
   - Add `AppShortcutsProvider` for high-value actions.
   - Use direct, user-facing titles and phrases.
   - Reuse the same action/entity model for widgets and controls when those surfaces need the same parameters.

6. Prove the integration.
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
- A sensitive or shared entity is exposed before ownership and authorization are clear.
- An intent is described as a Siri capability without confirming that its platform and mode support it.

## References

- `references/first-pass-checklist.md`
- `references/example-patterns.md`
- `references/code-templates.md`
- `references/system-surfaces.md`
