# Retrospective Interpretation

## Purpose
Verify the behavior described by this case.

## Input
Use `../fixtures/07-retrospective/source.md` plus a clean temporary destination unless the fixture describes an existing Vault state.

## Expected behavior
Record a later interpretation as retrospective.

## Forbidden behavior
Do not claim the user already held the later framework at the earlier event.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
