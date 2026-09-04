# AI Concept With Active Exploration

## Purpose
Verify that active user reasoning can establish `considering` without automatically implying stronger adoption.

## Input
Use `../fixtures/21-ai-concept-active-exploration/source.md` plus a clean temporary destination.

## Expected behavior
Record the qualifying Concept as `origin: A→U`, `adoption: considering`, and `evidence_level: E3` because the AI introduced it and the user's later message actively questions and applies it. This preserves AI-first history under the existing Origin taxonomy. Concept status remains governed by the existing type-scoped lifecycle rather than this patch.

## Forbidden behavior
Do not rewrite Origin as U0, U→A, or C, and do not upgrade the Concept above `considering` from this single episode of active exploration.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
