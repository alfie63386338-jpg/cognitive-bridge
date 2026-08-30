# Cognitive Bridge Behavioral Tests

These tests are primarily **behavior specifications**, not exact-output golden files. A generative cognitive system may produce different wording while still being correct.

For each case:
- `cases/` explains the purpose and forbidden behavior;
- `fixtures/` contains minimal fictional Source;
- `expected/` lists required and prohibited properties of a correct result.

Run these cases through the Skill in a clean temporary destination. Evaluate both positive behavior and **negative assertions**—things the system must not do.

The deterministic scripts under `scripts/` should also be run against generated outputs.

No fixture contains real user private data.

## Deterministic contract check

Run:

    python tests/validate_behavior_contract.py

Run the engineering and template regressions with:

    python -B -m unittest -v tests.test_engineering_scripts tests.test_templates tests.test_product_decisions

Use --json for machine-readable results. The validator checks all 18
case/fixture/expected triplets, UTF-8 readability, positive and negative
assertions, the multi-file longitudinal fixture, and concrete preservation
anchors for cases 14–18.

This is deliberately not a cognitive-output oracle. A passing contract check
does not mean the Skill passed the behavioral cases. For execution, run each
case through the Skill, retain the produced Vault, and review the result against
both Must and Must not constraints.

For cases 14–18, copy the fixture's existing-vault directory to a temporary
destination before the update. Never run the update directly against the
committed baseline. Compare baseline bytes/IDs/decision history afterward;
the validator's JSON output includes SHA-256 values for the committed baseline
files.

`tests.test_product_decisions` verifies the six approved Step 12 invariants:
the single canonical priority, type-scoped status values, Candidate Question
review isolation, valid unknown Origin, historical Discussion boundaries, and
append-only superseding User Decision events.
