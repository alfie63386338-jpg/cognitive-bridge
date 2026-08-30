# Human Edited Note

## Purpose
Verify the behavior described by this case.

## Input
Copy ../fixtures/15-human-edited-note/existing-vault/ to a temporary destination, record the existing note's cb_id and sentinel text, treat run-1-source.md only as baseline provenance, then update from source.md as the sole new Source.

## Expected behavior
Preserve manual edits and cb_id during an incremental update, retain registry/log history, append a distinct source/build record, and surface any unsafe merge as a conflict.

## Forbidden behavior
Do not regenerate the whole note, allocate a second identity for the same node, replace prior registry/build history, or treat the human paragraph as new Source evidence.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
