# Reconstructed AI-Origin Evidence

## Purpose
Verify that a later Source AI reconstruction is not treated as the original direct record.

## Input
Use `../fixtures/24-reconstructed-ai-origin-evidence/source.md` plus a clean temporary destination.

## Expected behavior
When the reconstruction is the best available attribution, keep the qualifying Concept tentative at `status: proposed`, `origin: A0`, `adoption: unconfirmed`, and `evidence_level: E1`.

## Forbidden behavior
Do not upgrade Source-AI reconstruction to E3 or present the unavailable original exchange as directly observed.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
