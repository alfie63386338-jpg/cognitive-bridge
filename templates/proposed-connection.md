## {{relation_id}}

**A:** [[{{node_a}}]]<br>
**B:** [[{{node_b}}]]

**Relation origin:** inferred<br>
**Status:** proposed<br>
**Mode:** {{mode}}<br>
**Confidence:** {{confidence}}

### Why this connection was proposed
{{rationale}}

{{#if evidence}}
### Evidence
{{evidence}}
{{/if}}

{{#if counterexample}}
### Counterexample / Boundary
{{counterexample}}
{{/if}}

### Review
Choose exactly one outcome: `accepted`, `rejected`, `revised`, or `unresolved`.

Record the explicit user choice as a new append-only event in `00_System/User Decisions.md` using `templates/user-decision-event.md`. If the choice changes later, append a new event whose `supersedes` field points to the prior decision event; do not edit the old event.
