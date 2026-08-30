# Open Question

## Purpose
Verify the behavior described by this case.

## Input
Use `../fixtures/13-open-question/source.md` plus a clean temporary destination unless the fixture describes an existing Vault state.

## Expected behavior
Keep the Question open after an AI answer when user adoption is absent.

## Forbidden behavior
Do not close the question because the answer sounds good.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
