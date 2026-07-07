# Apple 27 Roadmap

This plugin adopts the Apple 27 stack where it changes day-to-day agent behavior now. Future work is reserved for surfaces that need app-specific choices, credentials, or heavier automation.

## Adopted Now

- Xcode 27 toolchain discovery and per-plugin `DEVELOPER_DIR`
- pinned `xcodebuildmcp@2.6.2`
- Simulator, macOS, device, SwiftPM, debugging, UI automation, coverage, utilities, doctor, project discovery, project scaffolding, and Xcode IDE MCP workflows
- App Intents, entities, shortcuts, Spotlight/Siri/widget/control exposure
- Foundation Models availability, guided generation, tool calling, transcript hygiene, and Instruments proof
- Liquid Glass and Apple 27 SwiftUI guidance
- localization and accessibility proof loops
- Instruments, Top Functions, ETTrace, memgraph, and leak workflows
- Icon Composer 2 awareness for layered Liquid Glass icons

## Still Deliberately Later

- App Store Connect automation: requires credentials, release policy, and app-specific promotion rules.
- Xcode Cloud automation: requires team-level CI ownership and repository policy.
- automatic signing/provisioning repair: too likely to mutate Apple account or device trust state without explicit approval.
- deep SF Symbols 8 production workflow: useful, but usually secondary to app build/run/debug proof.
- full visionOS and tvOS interaction guidance: use Apple-wide build and SwiftUI defaults first; add dedicated guidance only after real project demand.

## Adoption Rule

Move an item from later to active guidance only when it changes a recurring agent decision, removes repeated user steering, or lets Codex prove Apple app behavior with less manual intervention.
