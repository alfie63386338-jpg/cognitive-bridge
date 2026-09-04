# Cognitive Bridge v0.2.0-beta.1 — Engineering Report

**Review period:** 2026-09-02 to 2026-09-03
**Review-time release state:** unpublished release candidate; publication not performed

> This is a dated pre-distribution review snapshot. Statements below about unperformed commit, tag, ZIP, retrieval, and Release actions describe the state at review close; current distribution status is recorded by the release notes, installation matrix, and GitHub Release.

## Executive verdict

The Beta 1 UX refinement and the bounded Step 15.6 Product Rule Clarification are implemented. The candidate accepts pasted Source and one Markdown Source natively, keeps structured directory/ZIP compatibility, uses one normalization path, records truthful build provenance, minimizes new persistent paths, and preserves recognizable legacy audit content without copying its private paths forward.

Step 15.6 resolves the previously open AI-originated proposed-Concept boundary. A durable, reusable, substantively relevant, non-decorative AI term may optionally become a standalone Concept. Without genuine user uptake it defaults to `A0 / proposed / unconfirmed`; direct AI-origin evidence may be E3 without implying Adoption, while Source-AI reconstruction does not inherit E3. The six Note Types and existing Origin, Adoption, Evidence, and Evolution taxonomies are unchanged.

All 63 repository regressions and the 26-case behavior-contract validator pass. Three independent post-patch adjudications also converged on the same fictional Source. At the close of this review snapshot, the checkout had not yet been committed, tagged, pushed, packaged as a v0.2 Skill ZIP, installed as the active v0.2 Skill, or published as a Release.

## P1 — Native Source Intake

- `pasted_text`, `single_markdown`, `structured_directory`, and `structured_zip` enter one transport-only normalization model.
- Paste mode preserves the selected UTF-8 payload byte-for-byte in run-scoped staging outside the long-term Vault.
- A clear request-envelope rule separates the user's active request from the Source payload. Prompts, commands, paths, or policy-like text inside Source are untrusted historical data and cannot authorize actions or change scope, methodology, destination, or permissions.
- Source identity binds each safe logical artifact name to its bytes. Swapping content between `thought-events.md` and `attribution-evidence.md` therefore changes identity, while equivalent directory/ZIP containers remain identical.
- Empty optional artifacts in a Beta 1-style structured package remain valid when at least one readable artifact is non-empty.
- Paste, file, and directory size/count limits are enforced before unbounded reads. ZIP traversal, absolute/drive/UNC members, links, encryption, portable-name collisions, size, and expansion limits fail closed.
- `build_source_registry.py` accepts a normalized manifest or legacy input, permits a sibling Vault for a single file/ZIP, and can append a v0.2 record without rewriting legacy Registry bytes.
- Source Preparation prompts prefer one `cognitive-bridge-source.md`, use a paste-ready Source-only block as fallback, and keep multi-file packages optional.

## P2 — Build provenance and execution auditability

- `references/build-provenance-manifest.json` declares candidate version `0.2.0-beta.1`, unchanged protocol version `1`, additive schema version `1.1`, and the exact canonical rule-file set.
- `build_execution_fingerprint.py` hashes normalized canonical rule bytes plus declared execution mode, intake mode, and Source hashes.
- Empty, duplicate, escaping, or linked canonical rule paths fail closed.
- Build Log entries require version/protocol/schema, execution/intake modes, Source IDs/hashes, ruleset hash, execution fingerprint, and all five outcome summaries.
- The fingerprint explicitly identifies declared build inputs only. It does not authenticate an Agent, runtime, native loader, plugin invocation, or environment.
- Runtime-claim QA covers prose and common quoted/YAML variants without manufacturing positive attestations.

## P3 — Persistent path minimization

- New Source Registry records contain logical names, Source IDs, content hashes, safe location labels, and intake metadata—not physical Source or staging paths.
- Execution fingerprints exclude timestamps, run/build IDs, destination paths, usernames, hostnames, model names, and unverified loader fields.
- Persistent-metadata QA detects drive paths, backslash and forward-slash UNC/rooted paths, Unicode POSIX paths, and file URIs without echoing matched values.
- Physical paths are recursively redacted from parsed helper JSON; non-JSON helper streams are represented only by hashes.
- Recognizable pre-v0.2 paths in preserved Source Registry/Build Log content are non-echoing `legacy_absolute_path_warning` items. They do not fail Aggregate QA by themselves and are never copied into a new v0.2 entry. New paths remain hard failures unless explicitly authorized and marked as potentially sensitive metadata.

## P4 — Step 15.6 Product Rule Clarification

- `references/cognitive-knowledge-model.md` now defines when an AI-originated semantic tool may optionally exist as a standalone Concept and excludes one-off decorative labels.
- `references/ownership-evolution-model.md` separates node-specific Origin, Adoption, and claim-scoped Evidence: a related user Idea does not transfer its Origin to a distinct AI-introduced Concept.
- Passive agreement, silence, non-rejection, continued conversation, answers to AI follow-ups, and later AI-authored summaries do not establish `considering`.
- Active user questioning, re-expression, boundary testing, concrete application, explicit usefulness, or later active reuse may establish `considering`; stronger Adoption still follows the existing model.
- A direct record of AI introduction may support E3 for that origin claim while Adoption remains unconfirmed. Source-AI reconstruction is indirect and may remain E1.
- A prior generated `A0 / unconfirmed` Concept is knowledge-state context, never automatic user-uptake evidence in a later run.
- `SKILL.md`, the Concept template, output protocol, example Concept, cases 04 and 18, eight new cases 19–26, and structured product regressions implement and lock the decision.
- `references/cognitive-integrity-rules.md` required no change because its ownership, reconstruction, decoration, and feedback-contamination protections already cover the risk.

## Confirmed defects repaired during review

1. Structured packages incorrectly rejected empty optional Beta 1 files.
2. Source identity did not bind logical artifact roles, allowing a role/content swap to retain the same ID.
3. Non-ZIP modes could read beyond configured limits before rejection.
4. A single Markdown Source and sibling Vault were rejected by an over-broad parent-directory boundary.
5. Source Registry had no append-only legacy update path.
6. The request-envelope boundary did not explicitly prevent commands embedded in historical Source from authorizing the current run.
7. The fingerprint manifest accepted empty/duplicate canonical lists and used a containment check that was too weak for linked or escaping rule paths.
8. Runtime-claim scanning missed quoted and underscored positive attestations.
9. Aggregate QA could persist a physical path from otherwise valid helper JSON.
10. Preserved Beta 1 absolute paths were treated as new-build hard failures.
11. Forward-slash UNC, rooted Windows, and Unicode POSIX path forms were not covered.
12. The earlier persistent-path matcher treated generated HTML closing tags as POSIX paths; the narrowed matcher and regression remain in place.

## Files changed

### Orchestration and canonical engineering contracts

- `SKILL.md`
- `references/universal-protocol.md`
- `references/obsidian-output-protocol.md`
- `references/cognitive-knowledge-model.md`
- `references/ownership-evolution-model.md`
- `references/terminology.md`
- `references/build-provenance-manifest.json` (new)

### Runtime helpers

- `scripts/normalize_source_intake.py` (new)
- `scripts/build_source_registry.py`
- `scripts/build_execution_fingerprint.py` (new)
- `scripts/check_persistent_metadata.py` (new)
- `scripts/build_qa_report.py`
- `scripts/_script_utils.py`

### User workflow and documentation

- `README.md`
- `CHANGELOG.md`
- `docs/source-intake.md` (new)
- `docs/build-provenance.md` (new)
- `docs/installation-matrix.md`
- `docs/release-checklist.md`
- all four `prompts/prepare-source-*.md` files
- `templates/build-log-entry.md` (new)
- `templates/concept.md`
- the fictional example Concept metadata

### Tests and reports

- `tests/test_source_intake.py` (new)
- `tests/test_build_provenance.py` (new)
- `tests/test_v02_methodology_lock.py` (new)
- `tests/test_templates.py`
- `tests/test_product_decisions.py`
- `tests/README.md`
- `tests/v02-forward-test.md` (new)
- `tests/product-fixtures/intake-invariance-source.md` (new)
- `tests/product-fixtures/ai-originated-proposed-concepts.json` (new)
- behavior cases, fixtures, and expected contracts 19–26 (new)
- behavior cases 04 and 18 plus their expected/baseline data
- `V0_2_ENGINEERING_REPORT.md`, `V0_2_TEST_REPORT.md`, and `V0_2_PRODUCT_PATCH_REPORT.md` (new)
- `PRODUCT_REVIEW_REQUIRED.md` (local historical record; Step 15.6 item resolved)

## Compatibility and methodology boundary

- The local v0.1 baseline remains `HEAD`/`origin/main` commit `d56c5db06036b95cec9b3079228ea893bcc3a1ca`. This checkout contains no local tag refs, so the public release tag mapping was not revalidated by this local-only check.
- The historical v0.1 distribution ZIP remains byte-locked at SHA-256 `3a0645c11f18bbf9c95773bd3dc2255014cc18e36433822b6fad8c4a7251b07a`.
- Untouched v0.1 cognitive/release assets retain their historical byte locks. The two clarified references, Concept template, and product-decision test module have separate approved Step 15.6 candidate locks.
- Existing `cb_id` values, human edits, append-only User Decisions, and AI feedback-contamination rules retain their v0.1 behavior.

**Change classification: Product Rule Clarification.**
**Methodology Redesign: NONE.**
**Taxonomy/model changes: NONE.**

The clarification resolves how existing Concept, Origin, Adoption, and Evidence values apply to one previously ambiguous case. It does not add or remove a Note Type, enum value, Evolution state, hierarchy level, or integrity priority. Historical Discussion boundaries, Latent Connection handling, Question-first behavior, Candidate Question protection, Seed protection, core-theme rules, Unknown Origin, User Decisions, and Cognitive Integrity priority were not redesigned.

The original three-mode probe exposed the ambiguity and triggered Product Review. After the owner-authorized Step 15.6 clarification, three isolated read-only passes re-read the canonical references and independently evaluated the same fictional Source without expected files or reports. All three classified the user Idea as `U0 / accepted / E3` and the distinct AI-introduced Concept as `A0 / proposed / unconfirmed / E3`. `PRODUCT_REVIEW_REQUIRED.md` records the decision and reports no remaining Product Review blockers. That local audit file remains excluded from public distribution.

## Installation/runtime boundary

The installed `cognitive-bridge` available to this Codex environment during review was the historical v0.1 release. The v0.2 candidate was reviewed and executed from this local checkout; that proved checkout/package operability, not native loading of the candidate. At review close, no v0.2 installation, commit, tag, push, Skill ZIP, or Release had been performed.

The Skill Creator `quick_validate.py` was attempted with both available Python runtimes but could not start because its own environment lacks the `yaml` module. No dependency was installed. Local frontmatter/name/surface checks and the full repository suite passed; the external-validator limitation is reported rather than converted into a PASS.

## Remaining limitations

- The unpublished candidate was tested with synthetic data and was intended for disposable or recoverable test Vaults.
- Cognitive quality still requires human review; deterministic normalization and QA do not prove semantic correctness.
- First Build remains better tested than arbitrary Incremental Update or full human-edit merge behavior.
- The dependency-free YAML checker is conservative and is not a full PyYAML replacement.
- At review close, native candidate installation, v0.2 Skill ZIP installation, GitHub retrieval of v0.2, and portable export had not yet been verified; later distribution evidence is outside this snapshot.

## Release gate

The Step 15.6 Product Review decision is implemented and verified; no Product Review blocker remains. This is the engineering/product gate defined by the Step 15.6 contract. It authorizes no publication action and does not represent the separately authorized distribution checklist, Skill ZIP build, clean extraction, GitHub retrieval, or Release publication as completed.

Ready to publish v0.2.0-beta.1: YES
