# Release Checklist

## Package
- [ ] `SKILL.md` frontmatter is valid and description matches actual scope.
- [ ] No user private Source or generated private Vault data is included.
- [ ] README describes Source → Obsidian boundary accurately.
- [ ] CHANGELOG reflects the release.
- [ ] Version is labeled Beta / Experimental and no unselected License is implied.

## References
- [ ] No conflicting enum definitions.
- [ ] Integrity rules retain highest priority.
- [ ] The single canonical quality priority exists only in `references/cognitive-integrity-rules.md`.
- [ ] Type-scoped note statuses match `references/cognitive-knowledge-model.md`.
- [ ] Latent relations default to inferred/proposed.
- [ ] AI-derived Candidate Questions remain in Review until Source or explicit acceptance permits promotion.
- [ ] AI feedback contamination guardrail remains explicit.

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

## Scripts
- [ ] `python -c "from pathlib import Path; [compile(path.read_bytes(), str(path), 'exec') for path in Path('scripts').glob('*.py')]"` passes without creating package artifacts.
- [ ] QA scripts run on `examples/example-output-vault/Cognitive-Bridge/`.
- [ ] `validate_statuses.py` passes on the example Vault.
- [ ] Scripts report candidates instead of making semantic merge decisions.

## Behavioral tests
- [ ] All 18 case specifications are present.
- [ ] Mixed ownership, evolution gap, retrospective interpretation, false similarity, no-core-theme, Seed protection, open Question, human edit, rejected relation, and AI feedback contamination are explicitly tested.

## Output safety
- [ ] Safe Namespace remains default.
- [ ] Deep Integration requires explicit user intent.
- [ ] Existing files are never silently overwritten.
- [ ] Incremental updates preserve human decisions and edits.
- [ ] Existing IDs are reused; new IDs follow the canonical mint/collision procedure.

## Distribution and privacy

- [ ] `.gitignore` excludes caches, local outputs, private Source/Vault paths, secrets, and `dist/` without excluding tests/examples/templates.
- [ ] Prospective tracked files pass the privacy/secrets/absolute-path scan.
- [ ] Release ZIP contains one root folder named `cognitive-bridge/` and no `.git/` or private runtime data.
- [ ] A clean temporary clone or extraction passes compilation and example technical QA.
- [ ] Repository owner, visibility, and Release publication are explicitly authorized.

## Human usability
- [ ] Example Vault opens from `MOC - Cognitive Bridge`.
- [ ] Core output is readable without plugins.
- [ ] User-facing completion does not require understanding internal codes.
- [ ] Gemini Source Preparation Prompt is directly linked from the README.
