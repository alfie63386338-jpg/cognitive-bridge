# Build Provenance

Cognitive Bridge v0.2 records what the project can determine from declared build inputs without guessing how an Agent runtime discovered the Skill.

The machine-readable declaration is `references/build-provenance-manifest.json`. It identifies:

- `cognitive_bridge_version`;
- `release_status`;
- `protocol_version`;
- `schema_version`;
- fingerprint format;
- the canonical rule files included in the ruleset hash.

`release_status` is `prerelease` for the published experimental Beta. `protocol_version` remains `1` because Step 15.6 clarifies one decision boundary inside the existing Note Type, Origin, Adoption, Evidence, and Evolution model; it does not change those taxonomies or redesign the method. `schema_version` is `1.1` because Source Registry and Build Log metadata are extended additively.

## Create a fingerprint

```text
python -B scripts/build_execution_fingerprint.py \
  --execution-mode first_build \
  --source-intake-mode pasted_text \
  --source-hash sha256:<normalized-source-hash>
```

The deterministic payload contains version/protocol/schema values, execution mode, intake mode, sorted normalized Source hashes, and a ruleset hash. It excludes timestamps, build/run IDs, physical paths, usernames, hostnames, destination paths, Agent/model names, and unverified loader/plugin fields.

To write one standalone entry:

```text
python -B scripts/build_execution_fingerprint.py ... \
  --build-id cb-build-... \
  --source-id cb-source-... \
  --created-summary "3 nodes" \
  --updated-summary "none" \
  --skipped-summary "none" \
  --conflicts-summary "none" \
  --review-items-summary "1 candidate question" \
  --output <new-entry-file>
```

To preserve an existing or legacy Build Log byte-for-byte and append a v0.2 entry atomically:

```text
python -B scripts/build_execution_fingerprint.py ... \
  --build-id cb-build-... \
  --source-id cb-source-... \
  --created-summary "3 nodes" \
  --updated-summary "none" \
  --skipped-summary "none" \
  --conflicts-summary "none" \
  --review-items-summary "1 candidate question" \
  --append-to <vault>/Cognitive-Bridge/00_System/Build Log.md
```

The five outcome summaries are required whenever an entry is written, so the helper cannot produce a provenance-only record that contradicts the Build Log contract.

Every generated entry states the boundary explicitly: the fingerprint identifies declared build inputs; it does not authenticate an Agent, runtime, native loader, plugin invocation, or execution environment.

## Runtime evidence

Do not emit `runtime_skill_loaded: true` or equivalent claims just because the Agent followed Cognitive Bridge behavior. Record `skill_path`, runtime manifests, loader signals, or plugin attestations only when the runtime actually supplies the exact evidence.

## Existing Vaults

Missing v0.2 fields in an older Build Log or Source Registry mean `legacy-unversioned`, not invalid. Append a new entry during the next build. Do not rewrite old entries, old Source Registry tables, User Decisions, or `cb_id` values.

An absolute path already present in recognizable pre-v0.2 audit content is reported as a non-echoing `legacy_absolute_path_warning`. It does not fail Aggregate QA by itself and must not be copied forward. Absolute paths introduced in a new v0.2 entry or cognitive note remain hard failures unless the user explicitly requested sensitive debug metadata and the file is marked accordingly.

Aggregate QA recursively redacts physical absolute paths from parsed helper JSON as well as hashing non-JSON failure streams. A helper failure therefore cannot copy a private path into the persistent QA Report merely because its stdout was valid JSON.
