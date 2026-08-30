---
cb_id: {{cb_id}}
type: idea
status: {{status}}
{{#if claim_status}}
claim_status: {{claim_status}}
{{/if}}
{{#if origin}}
origin: "{{origin}}"
{{/if}}
{{#if adoption}}
adoption: {{adoption}}
{{/if}}
{{#if evidence_level}}
evidence_level: {{evidence_level}}
{{/if}}
created: {{created}}
updated: {{updated}}
---

# {{title}}

{{#if current_position}}
> [!summary] Current Position
> {{current_position}}
{{/if}}

{{#if why_this_matters}}
## Why this matters
{{why_this_matters}}
{{/if}}

{{#if reasoning}}
## Reasoning
{{reasoning}}
{{/if}}

{{#if assumptions}}
## Assumptions
{{assumptions}}
{{/if}}

{{#if challenges}}
## Challenges
{{challenges}}
{{/if}}

{{#if evolution}}
## Evolution
{{evolution}}
{{/if}}

{{#if open_questions}}
## Open Questions
{{open_questions}}
{{/if}}

{{#if relations}}
## Relations
{{relations}}
{{/if}}

{{#if source_trace}}
## Source Trace
{{source_trace}}
{{/if}}
