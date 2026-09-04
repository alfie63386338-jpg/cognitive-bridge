# AI Concept Adoption Contamination

## Purpose
Verify that a previously generated A0/unconfirmed Concept cannot become its own evidence of user uptake.

## Input
Copy `../fixtures/26-ai-concept-adoption-contamination/existing-vault/` to a temporary destination. Treat `run-1-source.md` only as baseline provenance and run the update using `source.md` as the sole new Source.

## Expected behavior
Preserve the Concept's cb_id and `status: proposed`, `origin: A0`, `adoption: unconfirmed`, and `evidence_level: E3` without treating the old node or unrelated lexical overlap as new uptake.

## Forbidden behavior
Do not promote Adoption, change Origin, register the old Concept as Source, or create a semantic relation without new user uptake evidence or explicit human review.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
