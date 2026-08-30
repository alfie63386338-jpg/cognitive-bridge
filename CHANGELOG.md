# Changelog

## Unreleased — v0.1.0-beta.1 distribution candidate

### Product decisions
- Established `references/cognitive-integrity-rules.md` as the only canonical nine-item quality priority.
- Added type-scoped legal values for the single `status` property and deterministic status validation.
- Kept AI-derived Candidate Questions in the Review Queue until historical Source or explicit user acceptance permits promotion.
- Confirmed unknown Origin as valid and corrected the reconstructed example Question to `origin: "?"` with E1 evidence.
- Defined Discussion as a historical cognitive unit and removed the example's unsupported cross-conversation Discussion.
- Defined machine-readable append-only User Decision events with `supersedes` history.

### Beta distribution
- Reworked the README for ordinary Beta users, Gemini-first testing, limitations, and private Source handling.
- Added repository hygiene rules, installation matrix, Beta 1 Release notes, and a local release report.
- Added regressions for all six approved product decisions and the new status validator.

## Unreleased — Engineering audit stabilization

### Fixed
- QA and registry writers now refuse silent overwrites, validate roots, preserve Source boundaries, and use atomic replacement only with explicit `--force`.
- Deterministic validators now handle UTF-8 failures, portable filename collisions, frontmatter-scoped IDs, safer WikiLink/orphan resolution, and common YAML fallback errors.
- The basic YAML fallback now rejects unquoted mapping indicators, WikiLink checks ignore fenced examples and HTML comments, and duplicate findings return a failure code consistent with their JSON result.
- Unknown Origin values render safely in templates; optional metadata and sections no longer force empty or guessed content.
- The MOC template now separates confirmed and proposed connections and exposes the canonical entry-point sections.
- Source-preparation prompts now preserve explicit user exclusions, and stable-ID mint/reuse/collision behavior is canonicalized.

### Tests
- Added stdlib engineering regressions and deterministic structural validation for all 18 behavioral contracts.
- Rebuilt incremental fixtures for collisions, human edits, rejected/reopened relations, and AI feedback contamination using separate fictional Source and existing-Vault state.
- Completed rejected-relation fixture links, corrected two inconsistent assertions, and added a lexical-overlap trap to the contamination case.

### Documentation and examples
- Added an auditable example Source Registry, Build Log, and generated technical QA report.
- Corrected example system-date metadata so generated notes do not predate their fictional Source evidence.
- Kept the example's system-created Concept explicitly proposed on both its frontmatter and MOC surface.
- Added explicit product-review and Codex engineering/test reporting artifacts.
- Replaced the reserved Codex handoff placeholder with the formal engineering/test contract and made the release syntax check shell-independent.

## 0.1.0 — Initial functional build

### Added
- Thin-orchestrator `SKILL.md` with eight-phase execution workflow.
- Universal cognitive migration, knowledge-model, ownership/evolution, latent-link, integrity, and Obsidian output references.
- Generic and platform convenience Source Preparation prompts.
- Obsidian note templates for Ideas, Concepts, Questions, Seeds, Discussions, MOCs, proposed connections, source traces, and QA reports.
- Deterministic QA scripts for frontmatter, WikiLinks, duplicate IDs/content, orphans, file conflicts, source registry, and aggregate QA reporting.
- Eighteen cognitive behavior test specifications with fixtures and expected constraints.
- A fictional minimal example Vault and reference implementation note.

### Safety
- AI-generated prior output is explicitly barred from recursively becoming historical user evidence.
- Latent relations default to `inferred + proposed`.
- Safe Namespace Mode is the default.
- Unknown history and metadata remain unknown instead of being fabricated.
