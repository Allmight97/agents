# Build / Run Apple App

Use `apple-build-run-debug`.

First classify the target platform and project shape:

- `.xcworkspace`
- `.xcodeproj`
- `Package.swift`
- macOS app, iOS/iPadOS app, watchOS app, or another Apple platform target

Prefer XcodeBuildMCP for simulator/device/macOS workflows when the tool surface is available. Use shell `xcodebuild` or `swift` commands when they are narrower, more reproducible, or better aligned with the repo's documented validation.

Always report the exact command or MCP action used and the real first blocker if the build fails.
