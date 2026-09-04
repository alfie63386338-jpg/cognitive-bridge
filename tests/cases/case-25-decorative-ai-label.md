# Decorative AI Label

## Purpose
Verify that a one-off rhetorical label does not create graph decoration.

## Input
Use `../fixtures/25-decorative-ai-label/source.md` plus a clean temporary destination.

## Expected behavior
Keep the one-off label inside its source context and do not create a standalone Concept.

## Forbidden behavior
Do not create a Concept merely because the AI supplied a memorable or attractive phrase.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
