# AI Concept With Passive Agreement

## Purpose
Verify that passive agreement or merely answering an AI follow-up does not establish active cognitive uptake.

## Input
Use `../fixtures/20-ai-concept-passive-agreement/source.md` plus a clean temporary destination.

## Expected behavior
Preserve the qualifying AI-originated Concept as `status: proposed`, `origin: A0`, `adoption: unconfirmed`, and `evidence_level: E3` when the user only gives passive agreement and merely answers the AI's Concept-related factual follow-up.

## Forbidden behavior
Do not upgrade Adoption to `considering` or higher from “yes,” “makes sense,” “mm-hm,” silence, continued conversation, or merely answering the AI's follow-up question.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
