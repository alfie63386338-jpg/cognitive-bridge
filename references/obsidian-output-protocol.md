# Obsidian Universal Output Protocol

## Target

Output ordinary UTF-8 Markdown that works in Obsidian without third-party plugins. Plugin enhancements may be added later but never carry the only copy of core meaning.

## Modes

### Safe Namespace Mode — default

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

### Existing Vault Integration Mode
Only when explicitly requested. Inspect the allowed existing structure first. Adapt Cognitive Bridge to the user's architecture, not the reverse.

## Storage vs meaning

Folders group by note type. Topics and multiple membership are expressed through MOCs and WikiLinks.

## Stable identity

Every generated cognitive note should have a stable machine identifier:

```yaml
cb_id: cb-idea-xxxxxxxx
```

Human-readable filenames remain primary navigation. IDs support renames, deduplication, review decisions, and incremental updates.

### ID minting, reuse, and collisions

- Before writing, inventory every existing `cb_id` and relation ID in the destination namespace.
- Reuse an existing ID exactly when updating the same note or relation, including after a filename or title change. Never derive a replacement ID from mutable title/body text.
- For a genuinely new node, mint `cb-{type}-{uuid4hex}` once; for a new relation, mint `cb-rel-{uuid4hex}` once. Use lowercase hexadecimal UUID4 text without separators in the final segment.
- Check the candidate against the inventoried IDs before writing. On a new-ID collision, mint another candidate. On a duplicate involving an existing record, stop automatic mutation and create an actionable conflict review item.
- When identity is ambiguous, do not guess whether two records are the same. Preserve both and defer the merge/split decision to review.

The random minting step need not reproduce the same ID in a clean rebuild. Stability comes from recording and reusing the first assigned ID during incremental updates.

## Date semantics

`created` and `updated` are file/system dates. They are not thought birth dates. Historical time belongs in fields such as `earliest_traceable` and in Evolution sections.

## Minimal common frontmatter

```yaml
---
cb_id: cb-idea-xxxxxxxx
type: idea
status: stable
created: 2026-01-01
updated: 2026-01-01
---
```

Omit unknown optional fields rather than guessing values.

The legal `status` values are type-scoped and defined only in `references/cognitive-knowledge-model.md`. Use the single `status` property; do not create per-type status properties.

## Suggested Idea properties

```yaml
claim_status:
origin:
adoption:
evidence_level:
earliest_traceable:
current_position_as_of:
source_reconstruction:
mocs:
```

## Suggested Concept properties

```yaml
term_status:
aliases:
definition_scope:
mocs:
```

## Suggested Question properties

```yaml
status: open
priority:
origin:
evidence_level:
mocs:
```

## Suggested Seed properties
Keep minimal: `cb_id`, `type`, `status`, optional Origin/Evidence, creation/update dates.

## Core system notes

Under `00_System/` maintain when applicable:
- `README - Cognitive Bridge.md`
- `Schema.md`
- `Terminology Registry.md`
- `Source Registry.md`
- `User Decisions.md`
- `Build Log.md`
- `QA Report.md`

## Review surfaces

Under `08_Review/`, create only files that have actual review items, for example:
- `Review - Proposed Connections.md`
- `Review - Candidate Questions.md`
- `Review - Proposed Core Themes.md`
- `Review - Ambiguous Ownership.md`
- `Review - Possible Duplicates.md`
- `Review - Vault Conflicts.md`
- `Review - Update Conflicts.md`
- `Review - Low Confidence Reconstructions.md`

Review items must be actionable and remain clearly candidate judgments.

### Candidate Questions

An AI-derived question is a review item, not a formal historical Question. Give it a stable candidate ID and keep it in `08_Review/Review - Candidate Questions.md` with:

- the proposed question;
- `proposal_origin: inferred`;
- `proposal_status: proposed`;
- rationale and supporting Source clues;
- uncertainty or counterexample;
- the condition for promotion.

Do not create a file under `05_Questions/` unless Source establishes that the user asked the Question or an explicit user decision accepts the candidate. When promoted, preserve the candidate ID or a traceable link and record the actual Origin; do not relabel AI proposal wording as historical user wording.

## WikiLinks

Use normal Obsidian links:

```text
[[Exact File Name]]
[[Exact File Name|Natural display text]]
```

Do not create empty notes merely to eliminate a broken link. Do not link every noun.

## Relation separation

Confirmed/explicit semantic relations may live in the note body under `## Relations`.

Proposed inferred relations should live primarily in the review registry and/or a clearly separate `## Proposed Connections` section. Do not silently pollute the confirmed graph.

A proposed relation should have a stable relation ID and record:
- A
- B
- relation mode
- origin
- status
- confidence
- short rationale
- supporting evidence
- counterexample/tension when material

Accepted inferred relations retain `relation_origin: inferred`.

## Naming

- Idea: complete claim, not vague topic.
- Concept: noun/short phrase.
- Question: complete durable question.
- Discussion: meaningful original/core question.
- Seed: preserve raw expression when useful.
- MOC: `MOC - {Theme}`.

Avoid opaque numeric filenames.

## Main entry point

Create `01_MOC/MOC - Cognitive Bridge.md` with, as applicable:
- Start Here
- Major Areas
- Important Ideas
- Open Questions
- Important/Recent Evolution
- Proposed Connections
- Review Needed
- Source Coverage

Do not turn the MOC into a technical manual.

## Source registry

Track source identity, file/path, ingestion date, direct vs reconstructed status when known, scope, and processed identity/hash where practical. Source remains read-only.

## Build log

Each first/update build should record a build ID, date, source IDs, created nodes, updated nodes, skipped work, conflicts, and review items. This supports auditability and rollback planning.

## User Decisions

`00_System/User Decisions.md` is an append-only event log. Each event uses a stable decision ID and a machine-readable YAML block:

````markdown
## cb-decision-0123456789abcdef

```yaml
decision_id: cb-decision-0123456789abcdef
target_id: cb-rel-0123456789abcdef
decision: rejected
decided_at: 2026-08-30
supersedes: null
```

Optional human-readable context may follow the block.
````

Allowed `decision` values are `accepted`, `rejected`, `revised`, and `unresolved`. When a user changes a decision, append a new event and set `supersedes` to the earlier `decision_id`. Never delete or edit the earlier event. A system reopening caused by new evidence is a review-state change, not a new user decision; append a Decision Event only after explicit user review.

## Incremental updates

Before an update, read the Source Registry, every append-only User Decision event, the Build Log, and existing `cb_id`s. Do not rebuild the namespace from scratch.

Preserve user edits. If an automatic update would overwrite meaningful human-edited body content, perform a local safe merge or create a review item instead.

Existing Cognitive Bridge notes are current knowledge-state context, not fresh user-history evidence.

## Existing Vault collisions

Never overwrite a same-name file automatically. Determine whether it is truly the same concept. When uncertain, use a more specific generated filename and add a review item.

## QA

Technical QA should include frontmatter/YAML structure, cb_id uniqueness, WikiLinks, filename collisions, and orphan candidates. Cognitive QA must separately inspect ownership, inferred/explicit relation separation, chronology, Seed/Question protection, and AI feedback contamination.
