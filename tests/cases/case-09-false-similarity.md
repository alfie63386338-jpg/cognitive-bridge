# False Similarity

## Purpose
Verify the behavior described by this case.

## Input
Use `../fixtures/09-false-similarity/source.md` plus a clean temporary destination unless the fixture describes an existing Vault state.

## Expected behavior
Recognize that shared vocabulary alone is insufficient.

## Forbidden behavior
Do not link two notes solely because both use the word “freedom”.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
