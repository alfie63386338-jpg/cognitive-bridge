# Cognitive Bridge Terminology

Use these terms consistently across the project.

| Term | Meaning |
|---|---|
| Cognitive Asset | Durable thought material worth preserving for future understanding, reuse, revision, or connection. |
| Cognitive Unit | The basic semantic unit extracted from Source; not equivalent to a message/chat/file. |
| Source | User-provided material authorized for analysis. |
| Source Package | Evidence-rich, structure-light package prepared from historical material for Cognitive Bridge. |
| Source Intake | Readability, inventory, duplication, coverage, and scope assessment of supplied Source. |
| Cognitive Mining | Extraction of durable candidate cognitive units across files/conversations. |
| Origin | How an idea entered the recorded user–AI cognitive process. |
| Adoption | Degree to which the user took up a thought. |
| Evidence | Support for an Origin/Adoption/history judgment. |
| Contribution Trail | Record of meaningful user/AI contribution roles in forming an important node. |
| Earliest Traceable | Oldest reliable appearance in available evidence; not the thought's birth date. |
| Current Position | Best evidence-backed present stance as of available Source; never a final conclusion. |
| Conceptual Refinement | Clearer expression/boundaries without major change to the core claim. |
| Substantive Revision | Material change to the claim itself. |
| Retrospective Interpretation | Later framework applied to earlier experience/thought, explicitly marked as later interpretation. |
| Latent Connection | Potentially valuable relationship not explicitly established by the user in available history. |
| Explicit Relation | Relationship the user explicitly connected in historical Source. |
| Inferred Relation | Relationship proposed by Cognitive Bridge. |
| Proposed | Awaiting user evaluation; not user-endorsed. |
| Review Queue | Small collection of high-impact uncertain judgments for human review. |
| Safe Namespace | Isolated `Cognitive-Bridge/` destination that avoids editing existing user notes. |
| Deep Integration | Explicitly requested integration into the user's existing Vault architecture. |
| Incremental Update | Processing new/changed Source without rebuilding or erasing prior human decisions. |
| First-Person Perspective Barrier | Limits of comparing one's own cognition across long time spans, domains, and changing expressions. |
| Externalized Longitudinal Perspective | AI-assisted comparison across those materials without claiming final interpretive authority. |
| AI Feedback Contamination | Recursive error where prior AI-generated output is later mistaken for user historical evidence. |
| Candidate Question | AI-proposed open question kept in Review until historical Source or explicit user acceptance permits promotion to a formal Question. |
| Decision Event | Machine-readable append-only record of a user's review decision; a later change points to the prior event with `supersedes`. |

## Canonical enum index

- Origin, Adoption, and Evidence values are defined only in [ownership-evolution-model.md](ownership-evolution-model.md).
- Relation origin, status, and confidence values are defined only in [latent-connection-model.md](latent-connection-model.md).
- Type-scoped note status values are defined only in [cognitive-knowledge-model.md](cognitive-knowledge-model.md).
- Term status and Claim status values are defined below.

### Term status
`standard-academic`, `personal-language`, `project-defined`, `borrowed-and-adapted`, `personal-language-with-conflict`

### Claim status
Common values include `personal-position`, `philosophical-hypothesis`, `empirically-supported`, `empirically-contested`, `project-model`.
