# Later Active Reuse of an AI Concept

## Purpose
Verify that genuine later uptake preserves AI-first history while allowing the existing A→U transition.

## Input
Copy `../fixtures/22-ai-concept-later-active-reuse/existing-vault/` to a temporary destination. Treat `run-1-source.md` only as baseline provenance and run the update using `source.md` as the sole new Source.

## Expected behavior
Preserve the existing Concept and cb_id. The direct, year-later autonomous cross-context application supports `origin: A→U`, `adoption: integrated`, and `evidence_level: E3` under the existing model. Concept status remains governed by the existing type-scoped lifecycle rather than this patch.

## Forbidden behavior
Do not rewrite the historical AI introduction as U0, U→A, or C, replace the existing cb_id, or infer the update from the old Vault node instead of the new Source evidence.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
