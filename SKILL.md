---
name: cognitive-bridge
description: Transform user-provided long-term AI conversation exports, source packages, notes, and other text records into a user-owned Obsidian cognitive knowledge base. Recover durable ideas, concepts, questions, seeds, important discussions, ownership/evidence, evolution, and proposed latent connections while preserving uncertainty and never rewriting the user's history.
---

# Cognitive Bridge

Cognitive Bridge migrates **user-provided source material** into an Obsidian-native cognitive knowledge base.

The skill does **not** fetch a user's historical AI conversations. If the material still lives inside another long-term AI, direct the user to the appropriate prompt under `prompts/` so that AI can prepare a Source Package first.

## Core contract

Cognitive Bridge is a **Source → User-Owned Obsidian Cognitive Knowledge Base** skill.

Use the single canonical priority in `references/cognitive-integrity-rules.md`. Do not restate or reorder it in lower-level resources. Revisit that file whenever a lower-level rule appears to conflict with the contract.

## Use this skill when

Use Cognitive Bridge when the user asks to:

- turn long-term AI chats or exports into Obsidian notes;
- migrate a prepared Cognitive Bridge Source Package into Obsidian;
- reconstruct durable ideas, questions, concepts, and thought evolution from supplied personal records;
- update an existing Cognitive Bridge namespace with new source material;
- discover cross-time, cross-domain, or cross-expression cognitive connections in supplied records.

Do not use it as a generic archive importer, chat backup tool, web scraper, psychotherapy system, or automatic life-philosophy generator.

## Required inputs

The run requires:

- **Source**: files or folders the user has explicitly provided or scoped for analysis.
- **Destination**: an Obsidian Vault, Vault subfolder, or directory intended to become an Obsidian-readable knowledge base.

Optional preferences may include scope exclusions, language, compact/medium/detailed granularity, deep integration, academic fact-checking, or latent-link sensitivity.

Do not interrogate the user for settings that safe defaults can resolve.

## Default mode

Unless the user explicitly requests otherwise:

- use **Safe Namespace Mode**;
- create `Cognitive-Bridge/` inside the destination;
- do not edit or delete pre-existing user notes;
- use **medium granularity**;
- enable Origin, Adoption, Evidence, Evolution Reconstruction, and Latent Connection Discovery;
- keep inferred latent relations `proposed` until human review;
- do not automatically confirm a core theme;
- create a concise Review Queue for high-impact uncertainty;
- keep Source material read-only.

## Progressive reference loading

Load only what is needed for the current phase, except that the integrity rules may be revisited at any high-risk step.

### Phase 1 — Source Intake
Read:
- `references/universal-protocol.md`
- `references/cognitive-integrity-rules.md`

Inventory supplied files, determine readability, identify duplicated source material, recognize whether the material is raw or reconstructed, and establish scope. Do **not** ask where the source platform came from unless parsing genuinely requires it.

If source material is unavailable and the user says it still lives inside another AI, give the corresponding prompt under `prompts/`. Do not pretend to retrieve inaccessible history.

### Phase 2 — Cognitive Mining
Read:
- `references/universal-protocol.md`
- `references/cognitive-knowledge-model.md`

Extract durable candidate cognitive units rather than summarizing each chat. Prefer ideas, concepts, long-lived questions, seeds, important discussions, meaningful methods, and evolution clues. Exclude disposable factual queries, ordinary logistics, generated boilerplate, and low-value repetition unless they acquire durable cognitive significance.

### Phase 3 — Ownership & Evidence
Read:
- `references/ownership-evolution-model.md`
- `references/cognitive-integrity-rules.md`

For important nodes, distinguish Origin, Adoption, and Evidence. Never infer user ownership from mere agreement, silence, personality fit, or AI summaries without supporting evidence.

### Phase 4 — Knowledge Modeling
Read:
- `references/cognitive-knowledge-model.md`

Model only six default note types:
- Discussion
- Idea
- Concept
- Question
- Seed
- MOC

Apply the Independent Existence Test before creating a standalone node. Prefer meaningful atomicity over maximal atomization.

Use the type-scoped legal values for the single `status` property. Never create parallel properties such as `idea_status` or `question_status`. Treat Discussion as a historical process: semantic similarity across separate conversations is not enough to merge them into one Discussion.

### Phase 5 — Evolution Reconstruction
Read:
- `references/ownership-evolution-model.md`

Recover only traceable evolution. Separate conceptual refinement from substantive revision and retrospective interpretation. Use "earliest traceable" rather than inventing birth dates. Preserve gaps and unresolved tensions.

### Phase 6 — Latent Connection Discovery
Read:
- `references/latent-connection-model.md`
- `references/cognitive-integrity-rules.md`

Latent connection discovery is **on by default**. Search for cross-temporal, cross-domain, and cross-expression structure, including tensions and missing bridges. Before calling a connection inferred, search for evidence that the user already made it explicitly.

All newly inferred connections begin as:

```yaml
relation_origin: inferred
relation_status: proposed
```

When evidence is insufficient for a theory, prefer proposing a Candidate Question rather than inventing a new doctrine. Keep an AI-derived Candidate Question in `08_Review/Review - Candidate Questions.md`; do not write it into `05_Questions/` until Source proves the user historically asked it or the user explicitly accepts it.

### Phase 7 — Obsidian Build
Read:
- `references/obsidian-output-protocol.md`
- `references/terminology.md`

Use the templates under `templates/` selectively. Do not generate empty boilerplate sections. In Safe Namespace Mode, use:

```text
Cognitive-Bridge/
├── 00_System/
├── 01_MOC/
├── 02_Discussions/
├── 03_Ideas/
├── 04_Concepts/
├── 05_Questions/
├── 06_Seeds/
├── 07_Sources/
├── 08_Review/
└── 09_Archive/
```

Every generated cognitive node should receive a stable `cb_id`. Follow the mint/reuse/collision procedure in `references/obsidian-output-protocol.md`; existing IDs survive renames and updates. A file's `created` date is the note creation date, never an idea birth date.

Build in batches for large sources:
1. high-confidence spine;
2. major Discussions and Ideas;
3. Concepts, Questions, Seeds;
4. latent connections;
5. MOCs and navigation.

### Phase 8 — QA & Handoff
Read:
- `references/cognitive-integrity-rules.md`
- `references/obsidian-output-protocol.md`

Run applicable deterministic checks from `scripts/` and perform cognitive QA manually using the integrity checklist. Technical success is not enough.

The deterministic pass consists of `validate_yaml.py`, `check_cb_ids.py`, `validate_statuses.py`, `detect_file_conflicts.py`, `check_wikilinks.py`, `detect_duplicates.py`, and `detect_orphans.py`; `build_qa_report.py` aggregates them without turning duplicate/orphan candidates into automatic semantic edits.

At minimum check:
- YAML/frontmatter structure;
- duplicate `cb_id`s;
- filename collisions;
- broken expected WikiLinks;
- orphan candidates;
- accidental writes outside scope;
- AI ideas mislabeled as user ideas;
- inferred relations laundered into explicit relations;
- fabricated chronology;
- over-expanded Seeds;
- prematurely closed Questions;
- AI-generated prior output used as new user-history evidence.

## First build vs update build

### First build
Create the Safe Namespace, registries, high-confidence nodes, latent-link review surface, MOCs, and QA report.

### Update build
Before writing, read:
- `00_System/Source Registry.md`
- `00_System/User Decisions.md`
- `00_System/Build Log.md`
- existing `cb_id`s

Process only genuinely new or changed source. Preserve human edits and previous accept/reject/revise decisions. Never delete and regenerate the whole namespace as an update strategy.

Treat `User Decisions.md` as an append-only event log. A changed user judgment receives a new Decision Event whose `supersedes` field points to the earlier event; the earlier event is never edited or deleted. New evidence may reopen review, but it does not itself create a user decision.

Existing Cognitive Bridge output is a representation of current knowledge state, **not fresh historical user evidence**. New Origin/Adoption/Evidence claims require source evidence or explicit human review.

## Review Queue policy

Prefer deferred review over blocking questions when the action is reversible and non-destructive.

Put high-impact uncertainty into `08_Review/`, especially:
- proposed latent connections;
- AI-derived Candidate Questions;
- proposed core themes;
- ambiguous ownership;
- ambiguous merges;
- update conflicts;
- terminology conflicts;
- low-confidence historical reconstruction.

The Review Queue must be small, actionable, and clearly framed as candidate judgments—not hidden truths waiting for confirmation.

## Existing Vault deep integration

Only perform deep integration when the user explicitly requests it. First inspect the allowed destination scope and produce a safe integration plan. Reuse existing Concepts only when meaning is genuinely aligned. Never rewrite existing notes merely to match Cognitive Bridge templates.

## User-facing completion

Do not dump implementation logs on the user. Report:
- number of Discussions, Ideas, Concepts, Questions, Seeds created or updated;
- number of proposed latent connections;
- number of review items;
- source coverage limitations;
- exact start note, normally `MOC - Cognitive Bridge`.

The user should be able to open Obsidian and start reading without understanding YAML, MOCs, or the internal ownership codes.

## Hard prohibitions

Never:
- fabricate inaccessible history, quotes, dates, transitions, or causality;
- silently turn AI-originated ideas into user-originated ideas;
- treat "yes", silence, or non-rejection as integration;
- back-project a present framework onto past material;
- force a single core life theme;
- create links for Graph View aesthetics;
- automatically delete or overwrite user files;
- mutate the Source Package;
- let AI-generated prior notes recursively become evidence that the user historically believed the same AI inference;
- hide uncertainty just to satisfy a schema.
