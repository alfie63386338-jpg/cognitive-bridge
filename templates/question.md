---
cb_id: {{cb_id}}
type: question
status: open
{{#if origin}}
origin: "{{origin}}"
{{/if}}
{{#if evidence_level}}
evidence_level: {{evidence_level}}
{{/if}}
created: {{created}}
updated: {{updated}}
---

# {{title}}

## Why this matters
{{why_this_matters}}

{{#if current_intuition}}
## Current Intuition
{{current_intuition}}
{{/if}}

{{#if competing_possibilities}}
## Competing Possibilities
{{competing_possibilities}}
{{/if}}

{{#if remains_open}}
## What Remains Open
{{remains_open}}
{{/if}}

{{#if related}}
## Related
{{related}}
{{/if}}
