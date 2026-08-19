# Changelog

This file records released behavior, interface, availability, and ownership
changes across the repository. It does not preserve intermediate churn,
unchanged surfaces, or commit-by-commit narration.

## [0.13.3] - 2026-08-19

### Removed

- Removed `consult-pro`; use the relevant domain skill and validate external
  consultation findings against current source truth directly.
- Removed `create-presentation-artifact`; use the active presentation,
  visualization, document, or site surface that owns the requested artifact.

## [0.13.2] - 2026-08-19

### Changed

- Made `orchestrate` respond to explicit natural-language requests for subagent
  delegation, select current roles and batch work from the live surface, and
  require bounded ownership, complete assignments, and integrated results
  without inferring delegation from task size alone.

## [0.13.1] - 2026-08-19

### Changed

- Made `writing-great-skills` distinguish read-only audits from authorized
  edits, tighten invocation around existing skills, test completion demand and
  client metadata, and repair consequential pointer or no-op uncertainty with
  focused behavioral evidence.
- Made `grill-me` reserve interviews for explicit grilling and pressure-testing,
  co-locate its first-round behavior, and align its OpenAI prompt with complete
  dependency-safe frontier rounds instead of an obsolete two-question cap.

### Fixed

- Replaced `improve-codebase-architecture`'s dead repo-alignment handoff with
  the live `grill-me` route for unresolved capture decisions.

## [0.13.0] - 2026-08-13

### Added

- Added the explicit-only `orchestrate` skill for bounded Codex subagent
  research, evidence gathering, adversarial review, and collision-safe parallel
  implementation selected from the live custom-agent catalog.

## [0.12.1] - 2026-08-10

### Fixed

- Made the `audit-entra` macOS path executable end to end: invoke PowerShell
  through `pwsh`, install only Graph authentication for the current user,
  preserve PSGallery's trust setting, keep one process-scoped device-auth batch,
  drive the visible private-browser device-code handoff, stop for unexpected
  tenant consent, and reject effective scopes that exceed the reviewed request.
- Required an MSP-owned application client ID for client-tenant Graph access;
  the shared Microsoft Graph Command Line Tools application is now an explicit
  stop condition because tenant-local delegated grants can accumulate authority.

## [0.12.0] - 2026-08-10

### Added

- Added `m365-tenant-ops` 0.1.0 as an Agent Plugins v1 package with the
  `audit-entra` skill for bounded, read-only Microsoft Entra and Microsoft 365
  tenant troubleshooting through delegated Graph and current admin surfaces.

### Changed

- Extended repository validation to check portable manifests for every nested
  plugin and enforce native/portable name, version, and description parity.

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

## [0.11.0] - 2026-08-10

### Changed

- Released `edge-browser` 0.2.0 with evidence-led Edge provider, extension,
  native-host, and derived Chrome-plugin cache diagnosis; corrected native-host
  ownership to `chrome@openai-bundled`; and required a live Edge tab-enumeration
  proof after recovery.

### Fixed

- Added a signed-source recovery path for incomplete Chrome-plugin caches
  without fabricating manifests, downloading helper binaries, modifying Edge
  profiles, or silently switching browser families.

## [0.10.0] - 2026-08-06

### Changed

- Distinguished the portable Agent Skills core from OpenAI-specific metadata,
  added standards-aware token budgets and validation guidance, and documented
  the client marketplace inventory plus operational rather than topical plugin
  boundaries.
- Released `build-apple-apps` 0.2.0 with XcodeBuildMCP 2.7.0, refreshed its Apple 27
  Foundation Models, App Intents, Liquid Glass, accessibility, performance,
  preview, and toolchain procedures, and added one shared skill tree packaged
  for Codex, Agent Plugins v1, and Xcode 27.

### Fixed

- Replaced Cursor's rejected out-of-boundary plugin symlink with a real local
  Git clone and made harness refresh synchronize it at the exact published
  commit, then require post-refresh Cursor loader and skill-count proof.
- Added pinned Agent Skills validation for every root and nested skill to the
  repository CI gate.
- Added native marketplace-plugin validation, official Agent Plugins v1 schema
  checks, and native/portable MCP drift detection for `build-apple-apps`.
- Removed the invalid XcodeBuildMCP `doctor` workflow entry while preserving its
  diagnostics resource, pinned `serve-sim` instead of executing `latest`, and
  disabled XcodeBuildMCP Sentry error telemetry by default.

### Removed

- Removed the unused Claude/Fable `codex` delegation plugin and its personal
  marketplace entry.
- Removed four duplicate Apple command wrappers and stale plugin-level agent
  metadata that Xcode 27 misclassified as extra skills and a subagent.

## [0.9.2] - 2026-08-06

### Fixed

- Routed this Mac's Cursor installation through the canonical checkout as a
  local plugin and made harness verification prove its symlink target, clean
  Git state, published commit, and manifest version instead of trusting
  Cursor's stale personal-marketplace cache.
- Limited release-metadata CI pushes to `main`, avoiding a duplicate tag run
  that GitHub could cancel and misreport as a failed validation.

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
