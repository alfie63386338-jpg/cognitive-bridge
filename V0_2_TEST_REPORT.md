# Cognitive Bridge v0.2.0-beta.1 — Test Report

**Test period:** 2026-09-02 to 2026-09-03
**Test-time candidate status:** PASS; Step 15.6 Product Review boundary resolved; publication not performed

> This is a dated pre-distribution test snapshot. Statements below about unperformed commit, tag, ZIP, retrieval, and Release actions describe the state at test close; current distribution status is recorded by the release notes, installation matrix, and GitHub Release.

## Result summary

| Area | Actual result |
|---|---|
| Final stdlib regression suite | PASS — 63/63 |
| Behavior-contract structure/fixture integrity | PASS — 26/26, 0 issues |
| Python source compilation | PASS — 20/20 files |
| Example Vault deterministic validators | PASS — 8/8 |
| Example Vault Aggregate QA | PASS |
| A/B/C plus directory/ZIP Source byte/identity invariance | PASS |
| Eight Step 15.6 product-rule scenarios | PASS — 8/8 structured regressions and behavior contracts |
| Independent post-patch semantic probe | PASS — 3/3 converged on node-specific Origin, Adoption, and Evidence |
| Four-mode technical Vault harness | PASS — 4/4 Aggregate QA |
| Path privacy and unsupported runtime claims | PASS |
| Protected v0.1 locks, authorized candidate locks, and 34-file Step 15.6 contract aggregate | PASS |
| Strict UTF-8/no BOM | PASS — 186 prospective candidate text files |

Automated transport/structure results and manual cognitive review are reported separately. Neither normalization nor a technical PASS is represented as proof of cognitive correctness.

## Commands executed

The following locally executable checks were run against the candidate checkout:

```text
python -B -m unittest discover -s tests -p "test_*.py" -v
python -B tests/validate_behavior_contract.py --json
python -B scripts/<each validator>.py examples/example-output-vault/Cognitive-Bridge --json
python -B scripts/build_qa_report.py examples/example-output-vault/Cognitive-Bridge --output <temporary-report>
python -B -c <compile every scripts/tests Python source in memory>
git diff --check
```

The manual forward-test procedure is preserved in `tests/v02-forward-test.md`.

## Automated regression coverage

The 63 tests cover:

- existing engineering helpers, source/output boundaries, overwrite protection, WikiLinks, IDs, statuses, YAML, duplicates, and orphans;
- all six approved v0.1 product decisions;
- prompt ordering and Source-only fallback output;
- pasted text, one Markdown file, structured directory, and structured ZIP intake;
- raw-byte preservation, empty optional Beta 1 package artifacts, safe ZIP rejection, pre-read size/count limits, and inert embedded Source instructions;
- container identity invariance and logical artifact-role binding;
- path-minimized Registry output, sibling-Vault use, append-only legacy Registry preservation, and duplicate Source-ID rejection;
- deterministic fingerprints, exact non-empty canonical rule scope, ruleset sensitivity, and Build Log completeness;
- parsed-JSON and non-JSON helper path sanitization;
- Windows drive/rooted paths, backslash/forward-slash UNC, Unicode POSIX paths, file URIs, legacy warnings, and runtime-claim variants;
- protected methodology, templates, historical release notes, v0.1 distribution asset, AI feedback contamination, and changed-file semantic boundaries;
- the Step 15.6 rule matrix: no uptake, passive agreement, active exploration, later active reuse, direct AI-origin evidence, Source-AI reconstruction, decorative labels, and prior-generated-node contamination;
- preservation of the six Note Types and the existing Origin, Adoption, Evidence, and Evolution taxonomies while candidate-specific locks cover the authorized clarification.

Observed result: **63/63 PASS**.

`tests/validate_behavior_contract.py --json` returned `ok: true`, `case_count: 26`, and `issues: []`. Its scope remains contract structure and fixture integrity; it does not execute an AI cognitive transformation. Incremental preservation anchors cover cases 14–18, 22, and 26.

All 20 Python files under `scripts/` and `tests/` compiled from source without creating bytecode artifacts.

## Example Vault QA

Target: `examples/example-output-vault/Cognitive-Bridge`

| Helper | Result |
|---|---|
| `validate_yaml.py` | PASS |
| `check_cb_ids.py` | PASS |
| `validate_statuses.py` | PASS |
| `detect_file_conflicts.py` | PASS |
| `check_wikilinks.py` | PASS |
| `detect_duplicates.py` | PASS — no candidates |
| `detect_orphans.py` | PASS — no candidates/errors |
| `check_persistent_metadata.py` | PASS — no issues/warnings |

Aggregate QA returned exit 0 and wrote `Technical status: PASS`; all eight helpers reported `execution_ok: true`. The temporary Aggregate report contained no local path and was removed after inspection.

## A/B/C Source Intake invariance

The fictional `tests/product-fixtures/intake-invariance-source.md` was supplied as:

- A: pasted text;
- B: one Markdown file;
- C1: one-artifact structured directory;
- C2: the equivalent structured ZIP.

All four modes produced one 813-byte `cognitive-bridge-source.md` artifact with identical bytes, artifact hash, aggregate Source hash, and Source ID:

- artifact SHA-256: `9a1b44b8d615a8f2730fdcb944df2d329fc4b393e6593c8bef88621f02982e2a`
- aggregate Source SHA-256: `3d693d145d22fa5e61b3689a35052fcdc489196d5178ba8c17bc4afcdbd6e89e`
- Source ID: `cb-source-3d693d145d22fa5e61b3689a35052fcd`

Only truthful transport provenance differed. A separate Beta 1-style multi-file directory/ZIP pair containing empty optional files normalized successfully with matching identities. A role-swap regression proved that exchanging content between provenance-bearing filenames changes Source identity.

No code path assigns Origin, Adoption, Evidence, Note Type, Candidate Question status, Seed maturity, or relation status during normalization.

## Deterministic build provenance

For the invariant fixture and final canonical rule set:

- ruleset hash: `sha256:9083c4117eedd0a377215fc9ed53059dede71d63bbe1cc86d5ad56d057df17d3`
- pasted fingerprint: `sha256:772c4687769cef517152f054437c955b3cb8cfb4ea16d4721bf29e646cae6247`
- single-Markdown fingerprint: `sha256:73a5d649b32f465f6b2d42770fa146138d77b0f632b7ea661e6fc2802f6b7446`
- structured-directory fingerprint: `sha256:76aee04987ef61a66d18ce3bfd3e54f290a213284d1288f0674aff03b0ae8c8b`
- structured-ZIP fingerprint: `sha256:53aeccb5257c70812d34ed6e1512fa50bd39bf580d833ac577d180c7ff7e8dc5`

The Source identity is invariant while fingerprints differ because the declared intake mode is intentionally part of provenance. None of these values attests to a native loader, runtime, plugin, model, or host.

## Temporary four-mode technical Vault harness

A new isolated test root outside the repository was used. Each normalized form received its own disposable Vault, path-minimized Source Registry, complete Build Log entry, Safe Namespace, and Aggregate QA report. To isolate transport/provenance behavior, the engineering agent constructed the fictional cognitive projection once for the pasted form and copied that projection unchanged into the other three Vaults before generating mode-specific system metadata and QA.

| Output per mode | Count/result |
|---|---:|
| Safe Namespace directories | 10 |
| Markdown files | 11 |
| Discussion | 0 |
| Idea | 1 |
| Concept | 1 |
| formal Question | 0 |
| Seed | 1 |
| MOC | 1 |
| Candidate Question | 1 |
| inferred/proposed relation | 1 |
| raw Source files under `07_Sources` | 0 |
| Aggregate QA | PASS — 8/8 helpers |

All non-system cognitive files were therefore byte-identical across the four Vaults (`0` mismatches by harness construction). This proves the four normalized forms can carry an identical projection through Registry, Build Log, Safe Namespace, and Aggregate QA; it is not evidence of four independent semantic transformations. System metadata differed only where intake provenance required it. Temporary artifacts were removed after the results were recorded.

## Manual cognitive integrity review

The engineering agent separately inspected the fictional output and confirmed:

- the direct user Idea remained `U0 / accepted / E3`;
- the AI term remained an `A0 / unconfirmed` proposed, project-defined Concept; direct attribution did not become user adoption;
- the Seed remained `origin: "?" / E1 / seed` and intentionally incomplete;
- the Candidate Question remained only in `08_Review`, with no file in `05_Questions`;
- the relation remained `inferred / proposed`, medium confidence, with the one-off-emergency boundary retained;
- no Discussion, chronology, formal user Question, core theme, or unsupported user adoption was fabricated.

This was a manual semantic review, not an independent external model evaluation. That limitation is explicit.

## Step 15.6 behavior and independent semantic verification

The owner-authorized Product Rule Clarification was encoded in eight structured scenarios and behavior contracts:

| Case | Boundary | Result |
|---:|---|---|
| 19 | qualifying AI Concept with no uptake | `A0 / proposed / unconfirmed`; PASS |
| 20 | passive agreement plus a bare answer to an AI Concept follow-up | remains `A0 / proposed / unconfirmed / E3`; PASS |
| 21 | active exploration | `A→U / considering / E3`, no automatic higher Adoption; PASS |
| 22 | later active reuse | preserves `cb_id`; `A→U / integrated / E3` is supported by direct cross-context reuse; PASS |
| 23 | direct AI-origin evidence | E3 may support origin without Adoption; PASS |
| 24 | Source-AI reconstruction | no automatic E3; weak reconstruction remains E1; PASS |
| 25 | decorative AI label | no standalone Concept; PASS |
| 26 | prior AI Concept in a later run | old node is not uptake evidence; PASS |

Cases 04 and 18 were tightened so passive agreement cannot become `considering` and prior generated content cannot bootstrap user Adoption. Case 20 also covers a user who merely answers an AI's Concept-related factual follow-up. Template/YAML coverage verifies the `A0 / unconfirmed / E3` combination, taxonomy-lock coverage verifies that no Note Type or enum value changed, and a deterministic aggregate hash locks the product matrix, behavior validator, all cases/expected files 19–26, and every associated fixture file (34 files total).

Three isolated, read-only engineering subagents first evaluated the new cases without reading expected files or reports. Their judgments satisfied all eight contract boundaries; later active cross-context reuse in case 22 appropriately reached a stronger existing Adoption state while preserving `A→U` history and the stable `cb_id`.

The original pre-patch intake-invariance probe had exposed the AI-named-term ambiguity. After the canonical clarification, the same three subagents re-read `references/cognitive-knowledge-model.md` and `references/ownership-evolution-model.md` and independently re-evaluated the same fictional Source. They did not read expected files, test code, or reports and made no edits.

All three converged on:

- user Idea: `type: idea`, `status: developing`, `origin: U0`, `adoption: accepted`, `evidence_level: E3`;
- distinct AI-introduced `Independence Gradient` Concept: `type: concept`, `status: proposed`, `origin: A0`, `adoption: unconfirmed`, `evidence_level: E3`.

The post-patch result verifies that the node-specific provenance ambiguity is resolved for this fictional probe. It remains bounded evidence from independent passes within one agent system, not an external-model evaluation or a substitute for the next cognitive QA stage.

## Privacy, compatibility, and tooling checks

- A synthetic path shaped like `C:\Users\RealName\Private\Gemini\source.md` did not enter new persistent output.
- Valid helper JSON containing a physical path was recursively redacted; invalid/raw streams were hashed.
- Common positive runtime-attestation prose/YAML variants failed; negative/disclaimer forms passed.
- A real-style pre-v0.2 Registry/Build Log prefix with an absolute path remained byte-for-byte unchanged, produced only a non-echoing legacy warning, and did not copy the path into the v0.2 entry.
- Strict UTF-8/no-BOM validation passed for 186 prospective candidate text files; the historical binary distribution ZIP was excluded from text decoding and remained covered by its byte lock.
- The candidate scan found no real local path, credential pattern, cache, bytecode, or private Source/Vault artifact.
- `git diff --check` passed.
- Local `HEAD` and `origin/main` remained at v0.1 baseline commit `d56c5db06036b95cec9b3079228ea893bcc3a1ca`; the checkout contains no local tag refs, so no local release-tag mapping was claimed. The historical distribution ZIP hash remained unchanged.
- No commit, tag, push, Release publication, or v0.2 ZIP action occurred.

The Skill Creator `quick_validate.py` did not run to completion because both available Python runtimes lack its external `yaml` dependency. No package was installed. Local package/frontmatter checks and all repository tests passed; the external validator is recorded as unavailable, not PASS.

## Change classification

**Change classification: Product Rule Clarification.**
**Methodology Redesign: NONE.**
**Taxonomy/model changes: NONE.**

The previously open AI-originated proposed-Concept item is resolved in `PRODUCT_REVIEW_REQUIRED.md`. No remaining Product Review blocker was found.

## Release gate

All in-scope Step 15.6 engineering checks pass. This is the engineering/product gate defined by the Step 15.6 contract; it does not itself authorize or represent completion of a commit, tag, push, Skill ZIP build, clean extraction, GitHub retrieval, or GitHub Release.

Ready to publish v0.2.0-beta.1: YES
