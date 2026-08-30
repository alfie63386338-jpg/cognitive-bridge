# Cross-Domain Latent Link

## Purpose
Verify the behavior described by this case.

## Input
Use `../fixtures/08-cross-domain-link/source.md` plus a clean temporary destination unless the fixture describes an existing Vault state.

## Expected behavior
Propose a structural link across domains with inferred/proposed metadata.

## Forbidden behavior
Do not present the link as explicit or accepted, and do not place an AI-derived Candidate Question in `05_Questions/` without historical Source or explicit user acceptance.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
