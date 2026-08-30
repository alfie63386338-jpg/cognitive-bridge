# Cognitive Bridge Development Rules

## Single Source of Truth

Each concept has one canonical definition. Other files should reference it rather than restating competing versions.

Canonical homes:
- quality priority and guardrails → `references/cognitive-integrity-rules.md`
- universal migration rules → `references/universal-protocol.md`
- note types/granularity → `references/cognitive-knowledge-model.md`
- Origin/Adoption/Evidence/Evolution → `references/ownership-evolution-model.md`
- inferred relations → `references/latent-connection-model.md`
- guardrails → `references/cognitive-integrity-rules.md`
- Obsidian representation → `references/obsidian-output-protocol.md`
- project vocabulary/enums → `references/terminology.md`

## Document precedence

This is document-resolution order, not a second quality-priority list. The only canonical quality priority is in `references/cognitive-integrity-rules.md`.

1. Cognitive Integrity & Safety
2. Universal Protocol
3. Domain reference models
4. Obsidian Output Protocol
5. Templates
6. Scripts

Scripts never redefine cognitive philosophy.

## Engineering vs cognitive changes

Engineering bugs—paths, syntax, encodings, deterministic validation—may be repaired without redesigning the cognitive model.

Changes to note types, Origin, Adoption, Evidence, latent-link authority, core-theme rules, or user interpretation authority are product/cognitive changes. Update the canonical reference and corresponding behavior tests deliberately.

## Deterministic scripts only

Do not encode cognitive inference in Python. Avoid rules such as `if user said yes -> integrated`. Scripts validate structure; AI/human reasoning handles semantic judgment.

## Test discipline

Any behavior change should update or add:
- a positive expectation;
- a negative assertion when misuse is plausible;
- a fixture that contains no real user private information.

## Schema evolution

Before adding a new property ask:
- Is it needed for future machine queries or incremental updates?
- Is the information actually supportable?
- Does it duplicate body content?
- Can it be omitted when unknown?

Before adding a new note type, prove that the six existing types cannot represent the cognitive function cleanly.

## Privacy

Never commit real user Source or generated private Vault content into the Skill repository, examples, or tests.

## Versioning guidance

- `0.1.0-beta.x`: experimental distribution and end-to-end Beta line
- `0.1.x`: first functional engineering line after Beta promotion
- `0.2.x`: engineering-test stabilization
- `0.3.x`: cognitive QA stabilization
- `1.0.0`: validated public candidate
