# Direct Evidence of AI Origin

## Purpose
Verify that direct AI-origin evidence and user Adoption remain separate judgments.

## Input
Use `../fixtures/23-direct-ai-origin-evidence/source.md` plus a clean temporary destination.

## Expected behavior
Allow the qualifying Concept to carry `status: proposed`, `origin: A0`, `adoption: unconfirmed`, and `evidence_level: E3` at the same time.

## Forbidden behavior
Do not interpret E3 evidence of historical AI introduction as E3 evidence that the user adopted the Concept.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
