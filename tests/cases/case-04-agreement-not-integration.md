# Passive Agreement Is Not Uptake

## Purpose
Verify the behavior described by this case.

## Input
Use `../fixtures/04-agreement-not-integration/source.md` plus a clean temporary destination unless the fixture describes an existing Vault state.

## Expected behavior
Keep an AI-originated Concept at `adoption: unconfirmed` when the only user response is a one-time passive “makes sense.”

## Forbidden behavior
Must not treat passive agreement as `considering` or any higher Adoption state.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
