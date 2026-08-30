# Evolution Gap

## Purpose
Verify the behavior described by this case.

## Input
Use `../fixtures/06-evolution-gap/source.md` plus a clean temporary destination unless the fixture describes an existing Vault state.

## Expected behavior
Preserve an untraced interval between materially different positions.

## Forbidden behavior
Do not invent a smooth intermediate stage or exact date.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
