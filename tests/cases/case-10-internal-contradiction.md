# Internal Contradiction

## Purpose
Verify the behavior described by this case.

## Input
Use `../fixtures/10-internal-contradiction/source.md` plus a clean temporary destination unless the fixture describes an existing Vault state.

## Expected behavior
Preserve tension between the two positions expressed at different points in the supplied record.

## Forbidden behavior
Do not auto-resolve them into one “true” position.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
