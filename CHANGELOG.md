# Changelog

This file records released behavior, interface, availability, and ownership
changes across the repository. It does not preserve intermediate churn,
unchanged surfaces, or commit-by-commit narration.

## Release convention

- The repository release version is also the `personal-skills` plugin version.
- Tags named `vX.Y.Z` identify repository releases. Nested plugins keep their
  own versions and are named inline; use component-prefixed tags such as
  `codex-v0.4.0` only if a nested plugin ever needs a separate tag.
- One completed revision pass becomes one repository release, including a pass
  that changes only a nested plugin.
- Use a patch for compatible fixes and bounded refinements. While the repository
  is pre-1.0, use a minor for new capabilities and incompatible changes. Treat
  `1.0.0` as a deliberate stability commitment.
- `[Unreleased]` exists only while a pass is active. Before publication, move
  its entries into a dated version section, run
  `python3 scripts/release_metadata.py set X.Y.Z`, commit, and tag the release.
- Claude and Cursor marketplace entries are version-free locators. Their
  plugin manifests and the Codex plugin manifest own the release version;
  `scripts/release_metadata.py check` enforces alignment with this changelog.
- Codex `+codex.<timestamp>` build metadata is a cache-buster. Changelog
  sections and git tags use the base version only.

## [0.9.1] - 2026-08-06

### Fixed

- Made Claude and Cursor marketplace entries version-free locators and added
  executable release-metadata synchronization plus CI drift detection, keeping
  each harness manifest aligned with the latest changelog release.

## [0.9.0] - 2026-08-05

### Added

- Added `grok-cli` for isolated, explicitly authorized Grok Build reviews and
  bounded implementation lanes with fail-closed discovery checks.

### Changed

- Scoped architecture scans toward named areas and recent change hotspots,
  made grilling ask the complete dependency-safe frontier each round, and made
  Wayfinder map its decision frontier breadth-first before creating child
  issues.
- Reduced model-visible skill descriptions and moved presentation-artifact and
  Wayfinder execution detail behind targeted references.
- Added the environment-as-source and prose-as-cache test to shared skill
  guidance, and kept deep-module vocabulary from overriding clearer project
  language.

### Fixed

- Synchronized Claude, Cursor, and Codex personal-skills versions and corrected
  stale canonical-source paths in the Apple build plugin documentation.

## [0.8.0] - 2026-08-03

### Added

- Added the `edge-browser` 0.1.0 plugin, a thin routing layer that selects
  Microsoft Edge through the first-party ChatGPT extension and the official
  Chrome plugin runtime without using desktop Accessibility.

## [0.7.4] - 2026-08-01

### Changed

- Made Wayfinder treat the repository-local setup needed for an explicitly
  requested roadmap as operational work, while keeping pre-publication review
  focused on unresolved content choices instead of permission gating.

## [0.7.3] - 2026-07-31

### Changed

- Made `create-presentation-artifact` lead with literal subject identity and
  reject compact openings that require charitable interpretation.
- Added a comparison-workspace pattern for equal side-by-side inspection,
  candidate focus, optional multi-subject switching, and same-origin full
  output without making hosting the default.

## [0.7.2] - 2026-07-31

### Changed

- Made `create-presentation-artifact` minimize cognitive reconstruction through
  an explicit reader job, visible operational structure, artifact-wide prose
  budget, progressive disclosure, and a subtraction pass derived from the
  repository's sharp-writing guidance.
- Added subject-specific visual-taste guidance distilled from successful
  generated artifacts, including domain metaphor, structural form, type roles,
  semantic color, surface behavior, and an anti-slop taste check.

## [0.7.1] - 2026-07-31

### Changed

- Made `grill-me` stay project-agnostic for personal and non-repository
  decisions while inspecting applicable guidance, owner docs, code, and tests
  when a repository owns material facts or durable capture.

## [0.7.0] - 2026-07-31

### Added

- Added `wayfinder` to calibrate large or materially foggy efforts, preserve
  accepted program truth, resolve only action-changing uncertainty, and carry
  one GitHub-native parent roadmap from discovery into execution slicing.

### Changed

- Made `to-issues` publish parent and blocking relationships through native
  GitHub issue relationships without duplicating them in issue bodies.

## [0.6.1] - 2026-07-31

### Changed

- Made `writing-great-skills` prefer positive steering over negation, distinguish
  real context boundaries from in-file headings, and favor pretrained leading
  words that already appear in prompts, docs, or code.
- Made `grill-me` resolve discoverable facts from source artifacts, reserve
  action-changing decisions for the user, and separate confirmation of shared
  understanding from authorization to act.

## [0.6.0] - 2026-07-30

### Changed

- Folded the useful operational-model and spatial-grammar behavior from
  `externalize-structure` into `create-presentation-artifact`, including
  original references for convergence, parallel ownership, guarded state
  changes, and zoomed hierarchy.
- Made presentation artifacts favor recognition over recall, expose visible
  completion, and replace prose that merely narrates their geometry.

### Removed

- Removed the overlapping `externalize-structure` skill and its model-visible
  trigger surface.

## [0.5.1] - 2026-07-29

### Fixed

- Added native Cursor plugin and marketplace manifests while keeping the shared
  skill tree single-source across Cursor, Claude, and Codex.
- Removed Claude manifest `$schema` hints that Claude ignores at runtime but
  Cursor 3.13 treats as unsupported plugin schema versions.

## [0.5.0] - 2026-07-29

### Added

- Added `externalize-structure` to turn dependency-heavy or stateful material
  into the smallest useful inline table, flow, tree, timeline, graph, wireframe,
  or prose form.

### Changed

- Made `use-proton-pass` recover its disposable CLI session from a
  session-scoped Viewer PAT stored in macOS Keychain, with non-disclosing
  clipboard provisioning and explicit missing, rejected, or expired token
  outcomes.

## [0.4.0] - 2026-07-17

### Added

- Added `use-proton-pass` for read-only Proton Pass agent sessions, non-disclosing
  credential handoffs, portal login, secret injection, scope diagnosis, and
  versioned pass-cli behavior references.

## [0.3.0] - 2026-07-12

### Added

- Added `code-review` as the read-only owner for changed-code correctness,
  requested behavior, regressions, proof gaps, and merge readiness.

### Changed

- Routed over-engineering-only reviews to `whittle-review` and repository-wide
  structural scans to the explicit `improve-codebase-architecture` workflow.
- Made Whittle line-count summaries conditional on defensible estimates and
  added an explicit stop against manufacturing another cleanup round.

## [0.2.0] - 2026-07-12

### Added

- Published the shared skill tree as `personal-skills@personal` for Claude and
  Codex marketplace installation.
- Added `codex@personal` 0.3.0 for model-dynamic Codex delegation from Claude:
  rescue, review, setup, transfer, and adversarial review.
- Added the Codex-only `build-apple-apps@personal` 0.1.0 plugin for Apple 27,
  Swift, SwiftUI, Xcode, simulator, signing, performance, and distribution work.
- Added `parallels-windows-ops`, `whittle`, and `whittle-review` to the shared
  personal skill tree.

### Changed

- Established one-pass-one-release versioning across the repository, with root
  personal-skills manifests synchronized and nested plugin versions named
  explicitly.
- Made GitHub `main` canonical for personal skills; Claude and Codex consume the
  marketplace plugin while `/Users/jstar/.agents` retains machine-local support
  only.
- Made `agents-md-steward` route durable personal learnings through authorized,
  deduplicated memory updates instead of promoting them into always-loaded
  guidance automatically.
- Made `impeccable` resolve bundled scripts from its installed skill directory.
- Made `consult-pro` model-dynamic and removed its GPT-5.5-specific dependency.
- Tightened `diagnose` around a red-capable loop and `to-issues` around
  one-agent-context slices plus expand-migrate-contract migrations.
- Made `write-sharp-docs` lead mixed-status documents with current-state
  orientation, finding-to-disposition chains, progressive disclosure, and a
  clear implementation-record boundary.
- Consolidated Whittle into one implementation skill and one read-only review
  skill inside `personal-skills`.

### Removed

- Moved `ask-abb` out of the shared tree to the Audiobook Boss project-local
  skill owner.
- Removed the obsolete GPT-5.5 prompt-instruction skill.

## [0.1.0] - 2026-06-24

### Added

- Established the personal agent workspace and initial shared skill set for
  diagnosis, consultation, design, security, teaching, planning, architecture,
  and document work.
