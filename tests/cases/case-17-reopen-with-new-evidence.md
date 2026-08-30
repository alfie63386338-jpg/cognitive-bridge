# New Evidence Reopens Relation

## Purpose
Verify the behavior described by this case.

## Input
Copy ../fixtures/17-reopen-with-new-evidence/existing-vault/ to a temporary destination, then update from ../fixtures/17-reopen-with-new-evidence/source.md.

## Expected behavior
Reopen relation cb-rel-rj0001 for review with the explicit new Source evidence while preserving append-only decision event cb-decision-rjcase170001.

## Forbidden behavior
Do not automatically accept it, edit/delete the previous decision event, append a fabricated superseding user decision, or mint a replacement relation ID that breaks the decision history.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
