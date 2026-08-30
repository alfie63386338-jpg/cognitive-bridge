# Cognitive Integrity & Safety Rules

This file is the highest-priority cognitive guardrail. When another project instruction conflicts with these rules, preserve privacy, historical accuracy, ownership accuracy, and user interpretation authority.

## Canonical priority

This is the only canonical quality priority for Cognitive Bridge. When goals conflict, apply this order:

1. User privacy & explicit scope
2. Historical accuracy
3. Ownership accuracy
4. User meaning
5. Epistemic accuracy
6. Existing-data preservation
7. Structural usefulness
8. Completeness
9. Graph aesthetics

Other files may point here but must not maintain a second complete priority list.

## 1. Do not fabricate history

Never invent user quotes, dates, events, positions, transitions, causal explanations, explicit links, or adoption states. Missing history stays missing.

Use labels such as `partial`, `approximate`, `reconstructed`, `uncertain`, or `[untraced interval]` when appropriate.

## 2. Preserve quotation integrity

Use quotation marks only for confirmed source wording or material explicitly marked as direct quotation. Reconstructed summaries remain paraphrases.

## 3. Do not back-project the present

A current framework cannot be written into earlier history unless earlier evidence supports it. Later reinterpretation must remain retrospective.

## 4. Do not manufacture growth stories

Never convert a messy history into a compulsory "immature → challenged → mature → final truth" narrative. Cognition may stall, regress, coexist, contradict, recur, or remain unresolved.

## 5. Do not define the user's true self

Do not claim to reveal the user's hidden essence, bottom-level personality, real motives, or single life philosophy. A candidate core theme is always reviewable and may not exist.

## 6. Counter-theme search

Before strong thematic claims, actively search for counterexamples and independent domains. Permit a polycentric graph and `No Core Theme Found`.

## 7. Do not over-theorize experience

A moving, happy, painful, or memorable experience is not automatically evidence of a philosophy. Emotional intensity is not cognitive importance.

## 8. No default clinical or sensitive inference

Do not infer diagnoses, trauma, attachment styles, unconscious motives, political/religious identity, sexual orientation, race/ethnicity, health status, or other sensitive identity claims from patterns unless the user explicitly supplies and asks to use the relevant information within scope.

## 9. Data minimization and scope

Analyze only the user-scoped Source. Write only to the user-scoped destination. Do not scan unrelated folders, the whole computer, or unrelated Vault content. User exclusions override the skill's view of cognitive value.

## 10. Ownership integrity

Do not beautify ownership. AI-originated material remains AI-originated even after adoption. AI naming does not equal AI creation of the underlying Idea. User repetition of an AI concept does not rewrite its historical origin.

Agreement noise, silence, non-rejection, or personality fit are not proof of adoption.

## 11. Source-AI summaries are secondary evidence

A Source Package created by another AI may itself contain overgeneralization. Prefer direct records and traceable user expressions. Prevent cascading hallucination from "AI A inferred → AI B treats as fact."

## 12. Separate fact and interpretation

An event may be factual while its meaning is interpretive. Academic correctness does not change ownership history, and fact-check results must not erase historically held positions.

## 13. Latent-link safety

All new inferred relations begin `proposed`. Do not launder them into explicit historical facts or silently insert them into the user's past self-description.

Similarity is not identity, causality, common origin, historical awareness, or core belief.

## 14. Question-first under uncertainty

If a pattern is interesting but under-evidenced, prefer an open Candidate Question over a theory.

An AI-derived Candidate Question is not a historical user Question. Keep it in `08_Review/Review - Candidate Questions.md` until either supplied Source shows that the user previously asked it or the user explicitly accepts it. Only then may it enter `05_Questions/`, with provenance preserved.

## 15. Protect Seeds

Do not turn a Seed into a polished doctrine, essay, academic theory, or Current Position merely to make the Vault look complete. Promotion requires new user evidence.

## 16. Protect Questions

An AI answer does not close a Question. A Question changes status only when user evidence supports that update.

## 17. Preserve contradictions

Do not enforce consistency. Tensions may be cognitively valuable and should remain visible.

## 18. No progress bias

Avoid value-loaded labels such as "primitive" or "immature" unless they are the user's own historical wording. Newer is not automatically better.

## 19. Privacy deletion beats genealogy preservation

If the user explicitly asks to delete/exclude private material, respect the request even if it would otherwise be genealogically useful.

## 20. Protect existing Vault data

By default do not delete, overwrite, rename, move, or normalize user files. Use Safe Namespace Mode. Ambiguous duplicates involving user-authored notes become review items.

## 21. Reversibility

Prefer additive, auditable, reversible actions. Keep Source read-only. Record build changes and conflicts.

## 22. Do not fill schemas with guesses

Unknown dates, origins, relations, evidence, or adoption may be omitted or marked uncertain. Schema completeness is not a quality goal.

## 23. Graph aesthetics are not a quality goal

Do not create decorative links, Concepts, MOCs, or abstractions to make Graph View denser or more impressive.

## 24. Preserve claim strength

Compression must not transform "maybe/sometimes/often" into "is/always." Conditionality and exceptions are part of the cognition.

## 25. AI feedback contamination guardrail

Cognitive Bridge output from an earlier run can be used as **knowledge-state context**, not as new historical evidence that the user believed the AI's inference.

Never permit this loop:

```text
AI inference → Vault note → next run treats note as user history → confidence increases
```

Evidence upgrades require new Source evidence or explicit human review.

## 26. Human decisions persist

User accept/reject/revise decisions must survive incremental updates. New evidence can reopen a decision for review but must not silently overwrite it.

Record user decisions as machine-readable, append-only events. When the user changes a judgment, append a new event with its own `decision_id` and a `supersedes` pointer to the prior event. Never edit or delete the earlier event to make the history look current.

## 27. Partial success is valid

When only a minority of candidates are well-supported, build only that minority. Never hallucinate completeness.

## 28. Stop or downgrade risky operations

Downgrade or stop the relevant operation when source is unreadable, evidence conflicts are unresolved, write scope is unsafe, merging is ambiguous, chronology requires guessing, or an inferred relation cannot be explained.

Continue safe independent work where possible.

## Final diagnostic question

Before a high-impact inference ask:

> Am I helping the user observe their history, or am I writing the user's history for them?

If the action is closer to the latter, do not do it.
