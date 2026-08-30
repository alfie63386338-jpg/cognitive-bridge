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

## Evidence levels

- `E3` — direct explicit user evidence or an attributable direct expression.
- `E2` — strong later reuse/application behavior.
- `E1` — weak inference from context.

No evidence is not a valid strong attribution. Use `?`, omit a field, or keep the judgment tentative.

### Evidence source strength

Prefer:
1. direct user messages / direct historical records;
2. explicit later reuse;
3. reconstructed summaries from another AI;
4. Cognitive Bridge inference.

A source AI's statement that "the user believes X" is reconstruction evidence, not automatically E3.

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
