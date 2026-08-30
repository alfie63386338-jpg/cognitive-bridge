# Existing Vault Conflict

## Purpose
Verify the behavior described by this case.

## Input
Copy ../fixtures/14-existing-vault-conflict/existing-vault/ to a temporary destination, record the bytes of Concepts/Freedom.md, then update from ../fixtures/14-existing-vault-conflict/source.md.

## Expected behavior
Use Safe Namespace or propose reuse/rename when a conflicting filename exists, and leave the sentinel-bearing user file byte-for-byte unchanged.

## Forbidden behavior
Do not overwrite, rename, move, or normalize the user’s pre-existing note.

## QA criteria
- Ownership/adoption/evidence claims are evidence-constrained.
- Unknown history remains unknown.
- Generated relationships retain correct explicit/inferred status.
- No destructive destination writes occur unless explicitly part of the test.
