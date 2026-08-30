# Rejected Relation

## Purpose
Verify the behavior described by this case.

## Input
Copy ../fixtures/16-rejected-relation/existing-vault/ to a temporary destination, then update from ../fixtures/16-rejected-relation/source.md.

## Expected behavior
Preserve relation cb-rel-rj0001 and append-only decision event cb-decision-rjcase160001 when no materially new evidence appears.

## Forbidden behavior
Do not silently re-propose it, mint a replacement relation ID, edit/delete the rejection event, or treat the new unrelated Source as supporting evidence.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
