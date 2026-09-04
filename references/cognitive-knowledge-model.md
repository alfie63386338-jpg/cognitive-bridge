# Cognitive Knowledge Model

## Core unit

The fundamental unit is a **Cognitive Unit**, not a message, chat, or file. A unit may be supported by one sentence or by years of material.

## Six default note types

### Discussion
Preserves **how an important cognitive process happened**: original question, initial position, key distinctions, turning points, contributions, produced nodes, and unresolved residue. Ordinary Q&A does not deserve a Discussion note.

Discussion is historical. Do not combine separate conversations merely because they later appear structurally similar. A cross-conversation Discussion requires Source evidence of continuity; otherwise preserve separate units and connect them through a proposed relation or MOC.

### Idea
A complete claim that can be supported, challenged, refined, contradicted, or applied. Prefer one independently changeable proposition per Idea.

### Concept
A reusable semantic tool across multiple Ideas, Discussions, or domains. Do not create a Concept for every noun.

An AI-originated term may become a standalone Concept when it passes the Independent Existence Test, remains understandable and reusable on its own over time, has substantive relevance to the user's actual discussion, and is not a decorative label invented for one answer. If those conditions are met but the Source contains no real user uptake, use:

```yaml
type: concept
status: proposed
origin: A0
adoption: unconfirmed
```

Creating the Concept preserves a provenance-bearing semantic tool; it does not mean the user adopted it. Keep one-off labels, rhetorical renamings, ordinary vocabulary, context-dependent phrases, and other graph decoration inside their source context rather than creating standalone Concepts.

Assign provenance to the node actually created. A related U0 Idea does not transfer its Origin to a separate semantic tool or Concept that the AI introduced; that Concept starts at A0 while the user Idea keeps its own Origin. Use `U→A` instead only when Source evidence shows that the user had already supplied the Concept's core semantic content and the AI mainly named, structured, or expanded that same Concept.

### Question
A durable open question with continued generative value. It is not every sentence with a question mark.

### Seed
A valuable but intentionally immature spark: intuition, strange association, observation, or not-yet-formed question. Preserve incompleteness.

### MOC
A navigation surface derived from actual content. MOCs are not folders and do not carry original doctrine.

Do not add `Method`, `Experience`, `Evolution`, or `CoreTheme` as default note types. Represent such material through the six types unless a later product decision explicitly changes the schema.

## Independent Existence Test

Before creating a standalone note ask:

> If this unit were removed from the original Discussion, could the user still understand it six months later and plausibly reuse or reference it elsewhere?

If not, keep it inside the Discussion.

## Supporting tests

- **Reusability**: is another note likely to link to it?
- **Changeability**: if two claims can independently change, consider splitting them.
- **Cognitive density**: avoid both giant notes containing many unrelated claims and micro-notes that have no independent meaning.

Default to **medium granularity**.

## Deduplication classes

1. **Exact duplicate** — merge generated duplicates.
2. **Semantic duplicate** — same cognitive function in different wording; usually merge and preserve aliases/historical wording.
3. **Overlapping** — partly shared but distinct; relate rather than force-merge.
4. **Related but distinct** — keep separate.

If an existing user-authored Vault note is involved, an ambiguous merge is proposed, not automatic.

## Experiences, emotions, facts, and generated output

An experience or emotion enters the cognitive layer only when it generates a durable insight, question, concept, method, or evolution event. Ordinary factual knowledge is not the target of this skill. AI-generated assignments, copy, explanations, and code are excluded unless the user's later critique, modification, reuse, or method makes them cognitively durable.

This generated-deliverable exclusion does not bar a qualifying AI-originated proposed Concept under the rule above.

## Type-scoped `status`

Use one property named `status`. Its legal values depend on note `type`:

| Note type | Legal `status` values |
|---|---|
| Idea | `developing`, `reasoned`, `stable`, `core`, `dormant`, `superseded`, `rejected` |
| Concept | `proposed`, `developing`, `stable`, `deprecated` |
| Question | `open`, `refined`, `dormant`, `closed` |
| Seed | `seed`, `promoted`, `dormant` |
| Discussion | `developing`, `reasoned`, `revisited`, `closed` |
| MOC | `active`, `dormant`, `archived` |

Do not create parallel properties such as `idea_status`, `question_status`, or `concept_status`. Question closure requires user evidence; an AI answer alone never changes a Question to `closed`.

Lifecycle is not a moral ranking. Newer does not mean better.

Rejected and superseded Ideas may remain valuable as genealogy and should not be deleted solely because the current user no longer accepts them.

## Promotion

A Seed can become an Idea, Concept, Question, or Discussion only with new evidence of development. AI enthusiasm alone is not promotion evidence.

## Contradictions

Allow contradictions and tensions. Do not auto-resolve a user's cognition into a single internally consistent system.

## Latent abstraction boundary

A repeated cross-domain pattern may justify a **proposed relation**, Candidate Question, or rare Candidate Concept. It does not automatically create a new user-endorsed Idea or "underlying theory."

## First-build restraint

The first build should be slightly sparse rather than overpopulated. It is easier to add a real node later than to unwind hundreds of decorative AI-generated notes.

## Human-readable body

YAML serves machines. The body serves the user. Preserve original wording where it has distinctive cognitive value, while allowing titles and summaries to be clarified without strengthening the claim beyond the source evidence.
