# Codex Handoff — Formal Engineering Review & Test Contract

## Role and scope

Perform a complete engineering review of Cognitive Bridge v0.1 as a maintainable Codex Skill. Inspect the full package, run every deterministic check that can execute locally, simulate or execute all defined behavioral cases, repair clear engineering defects, and report observed results honestly.

The product boundary is:

> User-provided Source → User-Owned Obsidian Cognitive Knowledge Base

Do not redesign the cognitive methodology during engineering work.

## Required review

1. Inspect the full project structure and internal references.
2. Verify that `SKILL.md` correctly orchestrates the eight phases: Source Intake, Cognitive Mining, Ownership & Evidence, Knowledge Modeling, Evolution Reconstruction, Latent Connection Discovery, Obsidian Build, and QA & Handoff.
3. Review every file under `references/`, `templates/`, and `prompts/`.
4. Statically check every Python file under `scripts/` and run all applicable QA.
5. Run technical QA against `examples/example-output-vault/`.
6. Evaluate all behavioral cases under `tests/`, including their positive and negative assertions.
7. Add only the minimum deterministic test infrastructure needed when an executable harness is missing.
8. Repair confirmed engineering defects when safe.

## Protected methodology

Do not change Origin, Adoption, Evidence, Note Types, Evolution, Latent Connection, Core Theme, Seed/Question Protection, Cognitive Integrity, or user interpretation authority merely to make tests pass. Record genuine ambiguities in `PRODUCT_REVIEW_REQUIRED.md` instead.

Canonical rule priority:

1. `references/cognitive-integrity-rules.md`
2. `references/universal-protocol.md`
3. domain reference models
4. `references/obsidian-output-protocol.md`
5. `templates/`
6. `scripts/`

## Safety requirements

- Explicitly test AI feedback contamination: prior Cognitive Bridge output must not automatically become user historical evidence in a later run.
- Do not overwrite, delete, rename, move, or pollute files outside the intended test destination.
- Keep Source read-only and separate from generated output.
- Use only fictional, synthetic, or anonymized test data.
- Preserve human edits and accepted/rejected/revised decisions during incremental updates; when reliable protection is unavailable, report `HUMAN EDIT PROTECTION INCOMPLETE`.

## Required deliverables

- `CODEX_ENGINEERING_REVIEW.md`
- `CODEX_TEST_REPORT.md`
- `CODEX_MODIFICATIONS.md`
- `PRODUCT_REVIEW_REQUIRED.md` only when genuine product-design decisions remain

Conclude with exactly one readiness decision:

`Safe for next cognitive QA stage: YES / NO`

Technical success alone is insufficient. Truth, ownership accuracy, uncertainty preservation, and non-destructive behavior take priority over a superficially complete result.
