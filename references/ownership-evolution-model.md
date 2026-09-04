# Ownership & Evolution Model

## Separate three questions

Never collapse:
- **Origin** — how did this idea enter the recorded cognitive process?
- **Adoption** — to what extent did the user take it up?
- **Evidence** — what supports the judgment?

`Origin ≠ Adoption ≠ Current Position`.

## Origin values

- `U0` — core observation/claim/question is user-originated in available evidence.
- `A0` — AI introduced it and user internalization is not established.
- `U→A` — user supplied the core intuition; AI mainly named, structured, expanded, or theorized it.
- `A→U` — AI introduced it; later user behavior demonstrates genuine uptake.
- `C` — genuinely co-constructed through substantive back-and-forth.
- `?` — origin cannot be responsibly determined.

Origin tracks cognitive formation, not legal authorship and never pseudo-precise contribution percentages.

When an AI explicitly introduces a standalone Concept, keep `origin: A0` merely because the user discussed it, did not reject it, or passively agreed. Discussion alone is not co-construction and does not justify `C` or `U→A`. Use `A→U` only when later user behavior supplies genuine uptake under the existing taxonomy; use `C` only for substantive joint reconstruction.

Apply Origin to the specific cognitive node. A separate U0 Idea that motivated or relates to an AI-introduced Concept does not make that Concept `U→A`. The existing `U→A` value still applies when the user supplied the Concept's own core semantic content and the AI mainly named, structured, expanded, or theorized it.

Unknown Origin is a valid result. A reconstructed statement such as “the user seems to have considered this for a long time” does not justify `U0`, `A0`, or `C` without stronger attribution evidence. Use `origin: "?"` with an appropriately low Evidence level, or omit the optional field when even that judgment is unsupported.

## Adoption values

- `unconfirmed`
- `considering`
- `partially-accepted`
- `accepted`
- `integrated`
- `rejected`

`integrated` requires strong evidence such as later autonomous reuse, re-expression in the user's own language, cross-context application, use as a premise, or active modification. "Yes," "makes sense," silence, and non-rejection do not establish integration.

Adoption can move in either direction over time.

### AI-originated Concept adoption boundary

For an otherwise valid AI-originated proposed Concept, default to `adoption: unconfirmed` when there is no user uptake evidence. An AI proposal, non-rejection, continued conversation, a passive response such as "yes," "makes sense," or "mm-hm," an answer to the AI's follow-up question, or later appearance in an AI-generated summary does not justify `considering`.

`considering` requires active user cognitive participation, such as a substantive follow-up question, re-expression in the user's own language, a counterexample or boundary, attempted application to a concrete problem, an explicit statement that the Concept may be useful, or later active reuse. Higher Adoption values continue to require the stronger evidence already defined by this model.

## Evidence levels

- `E3` — direct explicit user evidence or an attributable direct expression.
- `E2` — strong later reuse/application behavior.
- `E1` — weak inference from context.

No evidence is not a valid strong attribution. Use `?`, omit a field, or keep the judgment tentative.

Evidence level describes the strength of evidence for the stated claim or attribution. Direct evidence that an AI introduced a Concept may support `evidence_level: E3` for that historical occurrence and A0 attribution while `adoption: unconfirmed` remains correct. The same E3 does not, by itself, support `considering`, `accepted`, or any other user-uptake claim.

### Evidence source strength

Prefer:
1. direct user messages / direct historical records;
2. explicit later reuse;
3. reconstructed summaries from another AI;
4. Cognitive Bridge inference.

A source AI's statement that "the user believes X" is reconstruction evidence, not automatically E3.

Likewise, when a later Source AI reconstructs that an earlier AI appears to have introduced a Concept but the direct record is unavailable, preserve the reconstruction boundary. A tentative `origin: A0`, `adoption: unconfirmed`, and `evidence_level: E1` may be appropriate when that is the best available attribution; never upgrade the reconstruction to E3 merely because an AI summary states it confidently.

## Contribution Trail

For important nodes, record real contribution roles when useful:
- original observation
- original question
- concept naming
- distinction
- counterexample
- theoretical expansion
- empirical correction
- reformulation
- application
- final restatement

Do not invent symmetry or percentages.

AI naming a standard term does not mean AI created the underlying user Idea. Conversely, a user saying an existing term first does not mean the user invented the academic concept.

## Evolution model

Important Ideas may contain:
- Earliest Traceable Position
- Trigger
- Conceptual Refinement
- Substantive Revision
- Retrospective Interpretation
- Current Position
- Still Unresolved

### Earliest traceable
"Earliest traceable" means the oldest reliable record in available evidence, not a birth date.

### Conceptual refinement
Core judgment remains substantially similar while wording, boundaries, or distinctions improve.

### Substantive revision
The claim itself materially changes.

### Retrospective interpretation
A later framework is used to reinterpret earlier experience or thought. Never backdate the later interpretation.

### Current Position
The best evidence-backed estimate of the user's present position as of available sources. Never call it a Final Conclusion.

## Time integrity

Unknown time is valid. Use approximate dates or ordering when justified. Preserve `[untraced interval]` when an important gap exists. Never interpolate a smooth development merely because it would tell a coherent story.

## Historical vs semantic relations

`superseded-by` and `refined-into` are historical relations. `supports` and `challenges` are semantic relations. Do not mix them.

## Human review

User review has highest authority over current adoption and current self-description, but it does not erase direct historical evidence. A user may now reject a view they explicitly held in the past; preserve both facts.

## Incremental update

New sources can strengthen, weaken, or complicate Origin, Adoption, Evidence, or Current Position. Preserve earlier evidence and reviewed decisions rather than overwriting history.

An AI-originated Concept created by an earlier Cognitive Bridge run is knowledge-state context, not new evidence of user uptake. Without new Source evidence of active user participation or explicit human review, preserve its prior Adoption value.
