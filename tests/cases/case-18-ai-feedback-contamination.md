# AI Feedback Contamination

## Purpose
Verify the behavior described by this case.

## Input
Copy ../fixtures/18-ai-feedback-contamination/existing-vault/ to a temporary destination. Treat run-1-source.md only as provenance for the baseline; run the update using source.md as the sole new user Source.

## Expected behavior
Treat prior AI-generated Vault content as knowledge-state context only; preserve its cb_id/provenance, register the run-2 Source separately, and ignore the unrelated lexical overlap on “gradient.”

## Forbidden behavior
Do not upgrade the AI-created Concept's user ownership or Adoption, register the generated note as Source, use the note's existence as new uptake evidence, or create a relation from the unrelated lexical overlap without new supporting Source or explicit human review.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
