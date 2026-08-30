---
cb_id: {{cb_id}}
type: seed
status: seed
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

## Spark
{{spark}}

{{#if context}}
## Context
{{context}}
{{/if}}

{{#if possible_connections}}
## Possible Connections
{{possible_connections}}
{{/if}}
