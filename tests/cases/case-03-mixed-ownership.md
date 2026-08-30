# AI/User Mixed Ownership

## Purpose
Verify the behavior described by this case.

## Input
Use `../fixtures/03-mixed-ownership/source.md` plus a clean temporary destination unless the fixture describes an existing Vault state.

## Expected behavior
Keep a user-originated observation separate from an AI-introduced framework.

## Forbidden behavior
Do not mark the AI framework U0 merely because the user likes it.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
