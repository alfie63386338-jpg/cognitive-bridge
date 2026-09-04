# Release Checklist

This is a reusable pre-publication checklist, not a live status board. Unchecked boxes do not mean that an already published release is incomplete. For a specific release, use its dated release notes, evidence reports, and GitHub Release as the status record.

## Package
- [ ] `SKILL.md` frontmatter is valid and description matches actual scope.
- [ ] No user private Source or generated private Vault data is included.
- [ ] README describes Source → Obsidian boundary accurately.
- [ ] CHANGELOG reflects the release.
- [ ] Version is labeled Beta / Experimental and no unselected License is implied.
- [ ] `references/build-provenance-manifest.json` reports the intended release version and unchanged protocol version.

## Source Intake

- [ ] Pasted text is accepted without file splitting or ZIP creation.
- [ ] One `cognitive-bridge-source.md` file is accepted directly.
- [ ] Structured directories and Source ZIPs remain compatible.
- [ ] All modes use one transport-only normalization contract.
- [ ] Raw pasted Source remains run-scoped and outside the long-term Vault by default.
- [ ] The current request envelope is separated from Source, and embedded Source instructions remain untrusted data.
- [ ] Container format does not change cognitive Evidence or ownership rules.
- [ ] Structured packages retain empty optional artifacts when at least one readable artifact is non-empty.
- [ ] Logical artifact-to-content mapping is bound into structured Source identity.
- [ ] ZIP traversal, absolute members, links, duplicate portable names, encryption, and unsafe expansion fail closed.
- [ ] Pasted/file/directory resource limits apply before unbounded reads.

## References
- [ ] No conflicting enum definitions.
- [ ] Integrity rules retain highest priority.
- [ ] The single canonical quality priority exists only in `references/cognitive-integrity-rules.md`.
- [ ] Type-scoped note statuses match `references/cognitive-knowledge-model.md`.
- [ ] Latent relations default to inferred/proposed.
- [ ] AI-derived Candidate Questions remain in Review until Source or explicit acceptance permits promotion.
- [ ] AI feedback contamination guardrail remains explicit.
- [ ] A qualifying AI-originated standalone Concept defaults to `A0 / proposed / unconfirmed`; Concept creation, passive agreement, silence, and continued conversation are not Adoption.
- [ ] Direct AI-origin evidence may be E3 without user uptake; Source-AI reconstruction is not automatically E3.
- [ ] Node-specific provenance prevents a related user Idea from transferring `U0` or `U→A` to a distinct AI-introduced Concept.

## Prompts
- [ ] Generic Source Preparation prompt is the canonical behavior.
- [ ] Platform variants do not claim capabilities the platform may not actually expose.
- [ ] Prompts preserve direct vs reconstructed evidence.
- [ ] Prompts preserve explicit scope exclusions even when more account or connected context is accessible.

## Templates
- [ ] Templates do not require empty sections.
- [ ] Seeds remain minimal.
- [ ] Questions remain open by default.
- [ ] User Decision events are append-only and later changes use `supersedes`.
- [ ] Concept templates can record optional Origin, Adoption, and Evidence fields without implying uptake.

## Scripts
- [ ] `python -c "from pathlib import Path; [compile(path.read_bytes(), str(path), 'exec') for path in Path('scripts').glob('*.py')]"` passes without creating package artifacts.
- [ ] QA scripts run on `examples/example-output-vault/Cognitive-Bridge/`.
- [ ] `validate_statuses.py` passes on the example Vault.
- [ ] Scripts report candidates instead of making semantic merge decisions.
- [ ] `normalize_source_intake.py` and `build_execution_fingerprint.py` pass their stdlib regressions.
- [ ] Aggregate QA includes `check_persistent_metadata.py`.
- [ ] Raw helper streams and physical paths inside parsed helper JSON cannot be copied into a persistent QA Report by default.

## Behavioral tests
- [ ] All 26 case specifications are present.
- [ ] Mixed ownership, evolution gap, retrospective interpretation, false similarity, no-core-theme, Seed protection, open Question, human edit, rejected relation, and AI feedback contamination are explicitly tested.
- [ ] Cases 19–26 cover AI Concept no-uptake, passive agreement, active exploration, later active reuse, direct AI-origin evidence, reconstructed AI-origin evidence, decorative labels, and adoption contamination.
- [ ] Paste, single Markdown, structured directory, and structured ZIP tests pass.
- [ ] Transport-level Evidence invariance and the manual semantic comparison matrix are complete.

## Output safety
- [ ] Safe Namespace remains default.
- [ ] Deep Integration requires explicit user intent.
- [ ] Existing files are never silently overwritten.
- [ ] New Source Registry records append without rewriting recognizable legacy bytes.
- [ ] Incremental updates preserve human decisions and edits.
- [ ] Existing IDs are reused; new IDs follow the canonical mint/collision procedure.
- [ ] Source Registry, Build Log, MOC, and cognitive notes contain no avoidable physical absolute Source paths.
- [ ] Build Log contains version, protocol, schema, execution mode, intake mode, and execution fingerprint.
- [ ] Execution fingerprint is described as build provenance, not runtime attestation.
- [ ] Unsupported native-loader/runtime/plugin claims are absent.
- [ ] Preserved pre-v0.2 absolute paths are non-echoing warnings; new v0.2 paths remain failures.

## Distribution and privacy

- [ ] `.gitignore` excludes caches, local outputs, private Source/Vault paths, secrets, and `dist/` without excluding tests/examples/templates.
- [ ] Prospective tracked files pass the privacy/secrets/absolute-path scan.
- [ ] `python -B scripts/check_persistent_metadata.py examples/example-output-vault/Cognitive-Bridge --json` passes.
- [ ] Release ZIP contains one root folder named `cognitive-bridge/` and no `.git/` or private runtime data.
- [ ] A clean temporary clone or extraction passes compilation and example technical QA.
- [ ] Repository owner, visibility, and Release publication are explicitly authorized.

## Human usability
- [ ] Example Vault opens from `MOC - Cognitive Bridge`.
- [ ] Core output is readable without plugins.
- [ ] User-facing completion does not require understanding internal codes.
- [ ] Gemini Source Preparation Prompt is directly linked from the README.
- [ ] Paste-first Source Preparation is shown before optional `.md`, directory, and ZIP modes.
- [ ] Engineering, test, and product-patch reports state `Ready to publish v0.2.0-beta.1: YES / NO`.
- [ ] Public `V0_2_PRODUCT_PATCH_REPORT.md` records the Step 15.6 decision and no remaining Product Review blockers; the optional local `PRODUCT_REVIEW_REQUIRED.md` audit agrees when present.
- [ ] Publication still requires an explicit, separate release/distribution authorization; this checklist does not authorize commit, tag, push, ZIP creation, or Release publication.
