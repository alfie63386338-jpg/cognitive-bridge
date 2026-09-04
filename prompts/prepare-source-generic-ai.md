# Generic AI Source Preparation Prompt

Copy the prompt below into the AI system that already has access to the historical conversations, memories, or context you want to migrate.

---

I am preparing material for **Cognitive Bridge**, a separate system that will reconstruct my long-term cognitive history into an Obsidian knowledge base.

Your job is **source preparation, not final interpretation**. Use only history, memory, and context you can actually access. Do not invent inaccessible conversations or fill missing periods.

Respect every user-specified exclusion and analyze only the explicitly included scope. Do not expand scope merely because additional history, memory, connected material, or account context is technically accessible.

Please produce an **evidence-rich, structure-light Markdown Source** that helps another AI later determine what I thought, what you contributed, what changed, and what remains uncertain.

## What to recover

Prioritize material that has durable cognitive value:

1. Important ideas or judgments I actively expressed.
2. Important ideas first introduced by you/AI that I later clearly reused, applied, modified, accepted, or rejected.
3. Discussions that materially changed my understanding or produced important distinctions.
4. Concepts I repeatedly used, including personal language or unusual meanings I gave standard words.
5. Long-lived questions that remained open or changed form over time.
6. Candidate Seeds: promising intuitions, odd associations, or unfinished observations that never became mature conclusions.
7. Evolution clues: earlier positions, later positions, revisions, refinements, rejections, returns, and unresolved tensions.
8. Explicit connections I personally made between topics, time periods, or domains.
9. Contribution evidence: what I supplied versus what AI supplied in important co-developed ideas.
10. Time/order evidence sufficient to say when something is exact, approximate, earliest traceable, or merely retrospective.

## Preserve evidence

Whenever possible include:
- my exact original wording, clearly marked as a direct quote;
- the surrounding context necessary to interpret it;
- date/time or reliable ordering if available;
- what the AI said that materially influenced the discussion;
- later examples where I reused or applied the idea;
- explicit acceptance, rejection, uncertainty, or qualification;
- contradictions and counterexamples.

If you only remember or can reconstruct something through summary rather than direct messages, clearly label it **reconstructed**. Never present reconstructed wording as a direct quote.

## Do not over-process

Do **not**:
- create my final Obsidian structure;
- declare a single life philosophy or "true self";
- turn every experience into a theory;
- make all my beliefs internally consistent;
- treat "yes", silence, or non-rejection as deep adoption;
- infer missing dates or missing steps;
- turn your own earlier ideas into my ideas unless later evidence shows I genuinely took them up;
- generate latent cross-domain connections on behalf of Cognitive Bridge unless I explicitly made those connections historically.

The next system will do final atomization, ownership analysis, evolution reconstruction, and latent-link discovery.

## Preferred output

Prefer one complete Markdown artifact named conceptually:

```text
cognitive-bridge-source.md
```

Organize it with clear headings for scope and gaps, source index/coverage, thought events, important discussions, original expressions, evolution clues, explicit connections, unresolved questions, candidate Seeds, and attribution evidence. Do not split it merely to look formal.

## Fallback for text-only platforms

If you cannot create a file, output the entire Markdown content directly in one complete block. Put only the Source Markdown in that block; do not add commands addressed to Cognitive Bridge before or after it. Do not require the user to reformat or package it. The user must be able to copy the result and paste it directly into Cognitive Bridge.

## Optional advanced output

Only when multi-file creation is genuinely available and useful, you may instead produce a structured package containing files such as `source-index.md`, `thought-events.md`, `important-discussions.md`, `candidate-seeds.md`, and `attribution-evidence.md`. A directory or ZIP is an optional container, not a prerequisite, and it has no higher evidentiary status than the same content in one Markdown artifact.

## Entry format

For important entries, use as many of these fields as the evidence supports:

- **Approximate/Exact Time:**
- **Evidence Type:** direct / reconstructed
- **Topic:**
- **User Expression:**
- **AI Contribution:**
- **What Changed / Why Important:**
- **Later Reuse or Application:**
- **Explicit Connection:**
- **Uncertainty / Missing Evidence:**
- **Traceable Source Clue:** conversation title, date, or another locator if available

Do not fill fields that you cannot support.

## Final quality check

Before finishing, verify:
- no invented quotes;
- no invented dates;
- no unsupported unified philosophy;
- important user wording has not been unnecessarily rewritten into AI language;
- user-originated and AI-originated contributions remain distinguishable;
- uncertainty and historical gaps remain visible.

The goal is not to make me look coherent. The goal is to give Cognitive Bridge the best possible evidence from which to reconstruct my real cognitive history.

---
