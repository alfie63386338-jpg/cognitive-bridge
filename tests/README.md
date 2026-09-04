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

    python -B -m unittest -v tests.test_engineering_scripts tests.test_source_intake tests.test_build_provenance tests.test_templates tests.test_product_decisions tests.test_v02_methodology_lock

Use --json for machine-readable results. The validator checks all 26
case/fixture/expected triplets, UTF-8 readability, positive and negative
assertions, the multi-file longitudinal fixture, and concrete preservation
anchors for cases 14–18, 22, and 26.

This is deliberately not a cognitive-output oracle. A passing contract check
does not mean the Skill passed the behavioral cases. For execution, run each
case through the Skill, retain the produced Vault, and review the result against
both Must and Must not constraints.

For cases 14–18, 22, and 26, copy the fixture's existing-vault directory to a temporary
destination before the update. Never run the update directly against the
committed baseline. Compare baseline bytes/IDs/decision history afterward;
the validator's JSON output includes SHA-256 values for the committed baseline
files.

`tests.test_product_decisions` verifies the six approved Step 12 invariants:
the single canonical priority, type-scoped status values, Candidate Question
review isolation, valid unknown Origin, historical Discussion boundaries, and
append-only superseding User Decision events. It also verifies the eight
approved Step 15.6 AI-originated proposed-Concept decisions: no uptake,
passive agreement, active participation, later reuse, direct AI-origin
evidence, Source-AI reconstruction, decorative labels, and prior-generated
node contamination.

`tests.test_source_intake` verifies pasted text, one Markdown file, structured
directory/ZIP compatibility, raw-byte preservation, fail-closed ZIP handling,
path-minimized registry output, append-only legacy Registry compatibility,
empty optional package files, pre-read resource limits, untrusted embedded
instructions, logical-role identity, and transport-level Evidence invariance.

`tests.test_build_provenance` verifies deterministic fingerprints, truthful
version/protocol/schema/mode metadata, non-empty portable-unique canonical rule
scope, ruleset sensitivity, raw and parsed-JSON QA sanitization, legacy path
warnings, path privacy, and rejection of unsupported runtime claims.

These deterministic intake tests prove that equivalent Source bytes reach the
same normalized payload without container-based evidence weighting. They do
not replace semantic review of generated cognitive output. For manual
forward-testing, run the fictional intake-invariance fixture through each mode
and compare Origin, Adoption, Evidence, Candidate Question placement, Seed
protection, and inferred/proposed relations; only transport provenance may
differ.

The repeatable manual procedure and semantic acceptance matrix are defined in
`tests/v02-forward-test.md`. Keep its temporary Vaults outside the repository,
and report automated transport checks separately from human cognitive review.

`tests.test_v02_methodology_lock` keeps separate locks for untouched protected
v0.1 methodology/release assets and for the explicitly authorized Step 15.6
candidate files. It confirms that v0.2 keeps protocol version 1, preserves the
six Note Types and existing Origin/Adoption/Evidence taxonomies, and extends
behavior-case numbering continuously from 18 through 26. A separate aggregate
hash covers the Step 15.6 product matrix, behavior validator, all case/expected
contracts 19–26, and every associated fixture file (34 files total).
