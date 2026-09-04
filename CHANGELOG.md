# Changelog

## v0.2.0-beta.1 — 2026-09-04

### Added
- Added native pasted Source intake with a run-scoped raw Markdown representation; no manual file split or ZIP is required.
- Added single-Markdown Source intake and a shared format-neutral normalizer for paste, Markdown, structured directories, and structured ZIPs.
- Added safe ZIP extraction, normalized intake manifests, content-stable Source identity, and path-minimized Source Registry output.
- Added truthful build provenance metadata, canonical ruleset hashing, and a deterministic execution fingerprint with an explicit non-attestation boundary.
- Added persistent-metadata QA for absolute-path candidates and unsupported runtime claims.
- Added an explicit request-envelope and untrusted-Source boundary so embedded prompts cannot authorize actions or alter the current run.
- Added append-only v0.2 Source Registry records for legacy Vaults without rewriting prior bytes.
- Added v0.2 engineering and test reports with four-mode intake invariance, a synthetic four-mode technical Vault harness, and bounded engineering semantic-review evidence.
- Added eight Step 15.6 behavior contracts (cases 19–26), eight structured product-decision regressions, and `V0_2_PRODUCT_PATCH_REPORT.md` for the AI-originated proposed-Concept decision.

### Changed
- Made one `cognitive-bridge-source.md` artifact the preferred Source Preparation output, direct Markdown the fallback, and multi-file packages an optional advanced format.
- Reordered the README around the copy/paste workflow and documented Source ZIP separately from Skill installation ZIP.
- Prevented aggregate QA from persisting raw helper stdout/stderr that could contain private physical paths.
- Bound structured Source identity to logical artifact roles, retained empty optional Beta 1 package files, and enforced resource limits before non-ZIP reads.
- Redacted physical paths recursively from parsed helper JSON and downgraded preserved pre-v0.2 audit paths to non-echoing legacy warnings.
- Extended Source Registry and Build Log schemas additively while treating older Vault metadata as `legacy-unversioned`.
- Clarified that a durable, reusable, non-decorative AI-originated term may become an optional standalone `A0 / proposed / unconfirmed` Concept; Concept creation is not user Adoption, direct AI-origin evidence may be E3, and Source-AI reconstruction does not inherit E3.
- Clarified the node-specific Origin boundary: a related user Idea does not transfer `U0` or `U→A` to a distinct semantic tool introduced by AI.

### Engineering audit stabilization

#### Fixed
- QA and registry writers now refuse silent overwrites, validate roots, preserve Source boundaries, and use atomic replacement only with explicit `--force`.
- Deterministic validators now handle UTF-8 failures, portable filename collisions, frontmatter-scoped IDs, safer WikiLink/orphan resolution, and common YAML fallback errors.
- The basic YAML fallback now rejects unquoted mapping indicators, WikiLink checks ignore fenced examples and HTML comments, and duplicate findings return a failure code consistent with their JSON result.
- Unknown Origin values render safely in templates; optional metadata and sections no longer force empty or guessed content.
- The MOC template now separates confirmed and proposed connections and exposes the canonical entry-point sections.
- Source-preparation prompts now preserve explicit user exclusions, and stable-ID mint/reuse/collision behavior is canonicalized.

#### Tests
- Added stdlib engineering regressions and deterministic structural validation for all 18 original behavioral contracts.
- Rebuilt incremental fixtures for collisions, human edits, rejected/reopened relations, and AI feedback contamination using separate fictional Source and existing-Vault state.
- Completed rejected-relation fixture links, corrected two inconsistent assertions, and added a lexical-overlap trap to the contamination case.

#### Documentation and examples
- Added an auditable example Source Registry, Build Log, and generated technical QA report.
- Corrected example system-date metadata so generated notes do not predate their fictional Source evidence.
- Kept the example's system-created Concept explicitly proposed on both its frontmatter and MOC surface.
- Added explicit product-review and Codex engineering/test reporting artifacts.
- Replaced the reserved Codex handoff placeholder with the formal engineering/test contract and made the release syntax check shell-independent.

### Preserved
- The six Note Types, Origin/Adoption/Evidence taxonomies, Evolution states, Cognitive Integrity priority, Discussion boundary, latent-link handling, Question/Seed protections, core-theme rules, unknown-Origin handling, User Decisions, and hierarchy remain unchanged. Step 15.6 is a bounded Product Rule Clarification within those existing taxonomies, not a methodology redesign.
- Published `v0.1.0-beta.1`, its baseline commit/tag, release notes, and distribution asset remain untouched.

## v0.1.0-beta.1 — 2026-08-30

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
