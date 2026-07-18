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
  its entries into a dated version section, synchronize the root Claude and
  Codex manifests, commit, and tag the release.
- Codex `+codex.<timestamp>` build metadata is a cache-buster. Changelog
  sections and git tags use the base version only.

## [Unreleased]

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
  clear implementation-record boundary; `handoff` remains the owner of
  session-transfer structure.
- Consolidated Whittle into one implementation skill and one read-only review
  skill inside `personal-skills`.

### Removed

- Moved `ask-abb` out of the shared tree to the Audiobook Boss project-local
  skill owner.
- Removed the obsolete GPT-5.5 prompt-instruction skill.

## [0.1.0] - 2026-06-24

### Added

- Established the personal agent workspace and initial shared skill set for
  diagnosis, consultation, design, security, teaching, planning, handoff,
  architecture, and document work.
