# Latent Connection Discovery Model

## Purpose

Discover potentially useful structural relationships in supplied cognitive history that the user has not explicitly connected. This is **Cognitive Structure Discovery**, not a generic related-notes recommender.

## First-person perspective barrier

A person cannot simultaneously inspect all past selves, domains, and expressions. Cognitive Bridge contributes an **externalized longitudinal perspective** by comparing material across time and context. This does not make the AI the final interpreter of the person.

## Default discovery modes

Enabled by default:
- **cross-temporal** — recurring or transformed structures across time;
- **cross-domain** — similar cognitive structures in different life/problem domains;
- **cross-expression** — semantically similar structures stated in different language.

An optional high-value mode is **structural analogy**: similar relation patterns among different actors or domains.

## Explicit first

Before labeling a relation inferred, search for evidence that the user already made the connection. If so:

```yaml
relation_origin: explicit
relation_status: accepted
```

New system discoveries begin as:

```yaml
relation_origin: inferred
relation_status: proposed
relation_confidence: low|medium|high
```

Confidence means confidence that the material contains a worthwhile structural relationship—not confidence that the relationship is the user's true worldview.

## Evidence ladder

- L1 lexical similarity — insufficient alone.
- L2 semantic similarity — candidate signal.
- L3 structural similarity — meaningful shared causal/value/problem structure.
- L4 cross-context reuse — strong candidate even without an explicit link.

Prefer structural evidence over word overlap.

## Useful relation families

Search for:
- structural similarity;
- tension / contradiction;
- generalization or application;
- missing bridge (often a Question or Concept that would connect two areas).

## Question-first rule

When a pattern is interesting but evidence is insufficient for a new Idea, generate a Candidate Question instead of a doctrine.

An AI-derived Candidate Question belongs in `08_Review/Review - Candidate Questions.md`, not `05_Questions/`. Promote it to a formal Question only when Source proves the user historically asked it or the user explicitly accepts it. Preserve whether it began as an AI proposal.

Example:

> "Do these different forms of support share a common criterion around future autonomy?"

is safer than:

> "The user's core philosophy is autonomy."

## Candidate Concepts

Create them rarely. A system-created abstraction must be marked `project-defined` and `proposed` unless evidence shows it became user language. Repeated AI-generated abstractions are not user evidence.

## Counter-theme / counterexample search

Before proposing a strong cross-domain pattern or candidate core theme, actively search for:
- contradictory nodes;
- domains where the pattern fails;
- alternative explanations;
- semantic differences hidden by similar words.

Similarity is not identity, causality, common origin, historical awareness, or core belief.

## Novelty and utility

A proposed relation should add cognitive value, not merely repeat category membership. Prefer a small number of explainable, high-value relations over dense linking.

Useful heuristic for medium granularity: usually no more than 3–5 high-value proposed relations per important node in the first build. This is not a hard schema rule.

## Review lifecycle

Relation states:
- `proposed`
- `accepted`
- `rejected`
- `revised`
- `unresolved`

Accepted inferred relations keep `relation_origin: inferred`. Rejection persists across future runs unless materially new evidence justifies reopening. Reopening must be explicit and explain the new evidence.

A user may revise a proposed connection rather than merely accept/reject it. Preserve the original proposal and human reformulation when useful.

## No psychologizing

Latent-link analysis targets relationships among supplied cognitive material. Do not infer trauma, disorders, hidden motives, sensitive identities, or a "true self" as part of default latent-link discovery.

## Success criterion

The ideal reaction is:

> "I had not connected these before, but this is worth thinking about."

not:

> "The AI is inventing a story about who I am."
