# Apple 27 Roadmap

This reference is for high-ROI future work that is not part of the essential
`build-macos-apps@personal` surface yet. Do not add stub skills for these areas
until the repo has repeated real use cases or an accepted design doc.

## High-ROI Candidates

### App Intents And Shortcuts

- Add guidance for App Intents, Spotlight, Shortcuts, widgets, and action
  donation when the app has real user actions worth exposing.
- Keep App Intents behind app-domain interfaces. Do not let intent handlers
  reach directly into view state or lane-owned storage.

### Foundation Models

- Add a narrow skill only after a local project needs on-device intelligence
  design, availability checks, privacy boundaries, prompt safety, and fallback
  behavior.
- Keep Foundation Models behind an intelligence module interface. Treat cloud
  LLM calls as out of scope unless a design doc accepts that dependency.

### Instruments And Performance

- Add Instruments workflows once there are repeated CPU, memory, startup, UI
  hitching, Energy, or HealthKit query performance issues.
- Prefer reproducible `xctrace` templates and saved trace paths over vague
  "profile it" advice.

### Localization And Accessibility

- Add localization guidance when user-facing strings and supported locales
  become part of an accepted product slice.
- Add accessibility verification when there is enough UI surface to justify
  VoiceOver, Dynamic Type, keyboard, contrast, and reduced motion checks.

### Xcode-Native Agent Skills

- Add Xcode GUI or XcodeBuildMCP workflows only when they beat shell-first
  commands for a repeated task.
- Keep them adapter-shaped. Shell commands remain the baseline proof path.

## Adoption Bar

Each candidate must earn its own skill by meeting at least two criteria:

- repeated use across real app work
- clearer trigger boundary than an existing skill
- measurable reduction in setup or debugging time
- behavior that cannot be carried cleanly by a reference section
- validation command or artifact that proves the work
