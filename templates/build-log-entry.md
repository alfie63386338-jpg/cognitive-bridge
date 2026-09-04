## {{build_id}}

```yaml
build_id: "{{build_id}}"
processed_at: "{{processed_at}}"
cognitive_bridge_version: "{{cognitive_bridge_version}}"
protocol_version: "{{protocol_version}}"
schema_version: "{{schema_version}}"
execution_mode: "{{execution_mode}}"
source_intake_mode: "{{source_intake_mode}}"
source_ids:
{{source_ids}}
source_hashes:
{{source_hashes}}
ruleset_hash: "{{ruleset_hash}}"
execution_fingerprint: "{{execution_fingerprint}}"
build_provenance_manifest: "references/build-provenance-manifest.json"
created_nodes: "{{created_nodes}}"
updated_nodes: "{{updated_nodes}}"
skipped_work: "{{skipped_work}}"
conflicts: "{{conflicts}}"
review_items: "{{review_items}}"
```

> The execution fingerprint is a deterministic identifier for declared build inputs. It does not authenticate an agent, runtime, native loader, plugin invocation, or execution environment.
