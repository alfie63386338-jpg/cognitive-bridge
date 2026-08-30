# ChatGPT Source Preparation Prompt

This is a convenience wrapper around the canonical generic protocol. Use only conversation history, memories, and context that this ChatGPT session/account actually exposes to you. If an older conversation is not accessible, say so rather than reconstructing it from a vague profile.

Copy the prompt below into ChatGPT:

---

I want to migrate useful long-term thinking from my history here into **Cognitive Bridge**, which will later create an Obsidian knowledge base.

Use only conversation history, memories, and context that this ChatGPT session/account actually exposes to you. If an older conversation is not accessible, say so rather than reconstructing it from a vague profile.

Respect every user-specified exclusion and analyze only the explicitly included scope. Do not expand scope merely because additional account history or context is technically accessible.

Act as an **archaeological source preparer**, not as the final theorist. Recover evidence-rich material about:

- important judgments I personally expressed;
- important AI-introduced ideas that I later clearly reused, applied, modified, accepted, or rejected;
- high-value discussions and turning points;
- repeated concepts and my distinctive language;
- unresolved long-term questions;
- unfinished candidate Seeds;
- changes, refinements, rejections, returns, contradictions, and untraced gaps;
- explicit cross-topic links I personally made;
- evidence that helps distinguish my contribution from the AI's contribution.

Whenever possible preserve exact user wording and label it **direct quote**. If you only have a summary/memory, label it **reconstructed** and do not invent quotation marks. Preserve exact/approximate timing only when supported.

Do not create a final philosophy, Obsidian schema, final MOCs, latent AI-inferred connections, or a polished growth story. Do not treat agreement noise or silence as deep adoption.

If you can create files, use this package:

```text
source-package/
├── README.md
├── source-index.md
├── thought-events.md
├── important-discussions.md
├── original-expressions.md
├── evolution-clues.md
├── explicit-connections.md
├── unresolved-questions.md
├── candidate-seeds.md
└── attribution-evidence.md
```

If not, produce one Markdown document with those headings. For each important entry include only supported fields: time, evidence type (direct/reconstructed), user expression, AI contribution, later reuse, explicit connections, uncertainty, and a traceable source clue.

Before finishing, check that you did not invent quotes, dates, missing conversations, or a unified life philosophy. The next system must receive evidence, not a finished interpretation.

---

For the full canonical protocol see `prepare-source-generic-ai.md`.
