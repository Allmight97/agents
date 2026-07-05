# Changelog

All notable changes to this personal agent workspace are recorded here.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- `codex@personal` plugin (`plugins/codex/`): lean Codex (GPT-5.5) delegation
  wrapping the `codex` CLI directly — `codex-rescue` subagent, `/codex:rescue`,
  `/codex:review` (native reviewer passthrough), and the `gpt-5-5-prompting`
  internal skill (adapted from openai/codex-plugin-cc, Apache-2.0; see plugin
  NOTICE). Replaces the vendor `codex@openai-codex` plugin, whose updates
  clobbered local GPT-5.5 retarget mutations and whose companion-runtime
  job-store surface (`status`/`result`/`cancel`/`transfer`) we don't use.

### Changed
- Integrated Whittle as two shared skills. Folded `whittle-audit` into
  `whittle-review` as a repo-audit scope branch and dropped `whittle-debt`
  because the `whittle:` marker convention was not adopted.
- Refined all whittle skills against `writing-great-skills` audit loop: cut
  sediment, no-ops, plugin-specific toggle boundaries, and flavor lines.
- Moved Whittle publishing into `personal-skills`; removed standalone
  `whittle@personal` marketplace entries.
- Clarified Codex source policy: this development Mac uses the local
  `/Users/jstar/.agents/skills` tree directly, while fresh machines can install
  `personal-skills@personal` from the marketplace.

### Removed
- Standalone Whittle skill surfaces for `whittle-debt` and `whittle-audit`;
  repo-wide audit now lives in `whittle-review`.
- Standalone `whittle` plugin catalog entries sourced from
  `Allmight97/whittle.git`.

## 2026-06-29

### Added
- Whittle listed in Claude and Codex marketplace manifests as a separate plugin
  sourced from `Allmight97/whittle.git`.

## 2026-06-25

### Changed
- Moved ABB router skill (`ask-abb`) out of shared skills into the
  audiobook-boss project-local skills tree.

## 2026-06-24

### Added
- `skills/codebase-design/`, `skills/create-presentation-artifact/`,
  `skills/grill-me/`, `skills/improve-codebase-architecture/`,
  `skills/resolving-merge-conflicts/`, `skills/to-issues/`,
  `skills/write-sharp-docs/`, `skills/writing-great-skills/`.
- Codex marketplace catalog at `.agents/plugins/marketplace.json`.

## 2026-06-16

### Added
- Initial personal agent workspace: shared skills, Claude/Codex plugin
  manifests, local `env/` and `bin/` directories.
