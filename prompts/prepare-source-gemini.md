# Gemini Source Preparation Prompt

This is a convenience wrapper around the canonical generic protocol. Use only Gemini history, memory/context, connected user-provided materials, or other records actually available in this Gemini environment. Do not imply access to chats you cannot inspect.

Copy the prompt below into Gemini:

---

I want to migrate useful long-term thinking from my history here into **Cognitive Bridge**, which will later create an Obsidian knowledge base.

Use only Gemini history, memory/context, connected user-provided materials, or other records actually available in this Gemini environment. Do not imply access to chats you cannot inspect.

Respect every user-specified exclusion and analyze only the explicitly included scope. Do not expand scope merely because additional connected material or account context is technically accessible.

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

Prefer one complete Markdown artifact named conceptually:

```text
cognitive-bridge-source.md
```

Use headings for scope/gaps, source coverage, thought events, important discussions, original expressions, evolution clues, explicit connections, unresolved questions, candidate Seeds, and attribution evidence.

If Gemini cannot create a file in this environment, output the entire Markdown content directly as one complete block so I can copy and paste it into Cognitive Bridge without reformatting. Put only the Source Markdown in that block; do not add commands addressed to Cognitive Bridge before or after it. A multi-file directory or ZIP is an optional advanced output only when Gemini can genuinely create it; it is not required and carries no higher Evidence.

For each important entry include only supported fields: time, evidence type (direct/reconstructed), user expression, AI contribution, later reuse, explicit connections, uncertainty, and a traceable source clue.

Before finishing, check that you did not invent quotes, dates, missing conversations, or a unified life philosophy. The next system must receive evidence, not a finished interpretation.

---

For the full canonical protocol see `prepare-source-generic-ai.md`.
