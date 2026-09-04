# Cognitive Bridge Installation Matrix

This matrix records evidence, not platform assumptions. Status values are `Verified`, `Unverified`, `Unsupported`, or `Unknown`.

| Mode | Status | Intended path | Current evidence and boundary |
|---|---|---|---|
| A — Managed Codex Skill Installation | Verified (v0.1 only) | Install `cognitive-bridge/` through Codex's Skill installer. | Public tag `v0.1.0-beta.1` was installed on 2026-08-30 and a later task exposed `cognitive-bridge` in the available-Skills catalog. This is a real signal for that Codex installation and historical version only; it does not attest to a managed/native v0.2 installation or other platforms. |
| B1 — Git / Local Skill Installation (v0.2) | Verified | Clone the repository or point an Agent at a local checkout containing `SKILL.md`. | The v0.2 checkout passed component discovery, 63 unit regressions, all 26 behavior-contract structures, all 8 example-Vault technical validators, a four-mode technical Vault harness with Aggregate QA, compilation, strict UTF-8, path/privacy checks, and the Step 15.6 independent semantic probe through 2026-09-03. This verifies package operability from a checkout, not native-loader discovery. |
| B2 — GitHub Skill Installation | Verified (v0.1); Unverified (v0.2 native install) | Install from the public GitHub repository when the Agent supports that feature. | Codex's installer retrieved public tag `v0.1.0-beta.1` on 2026-08-30. The public `v0.2.0-beta.1` tag is available for retrieval, but native platform installer behavior has not yet been revalidated for v0.2. |
| C1 — Manual Skill ZIP Installation (v0.1 historical) | Verified | Download `cognitive-bridge-v0.1.0-beta.1.zip`, extract `cognitive-bridge/`, and import or open that folder. | The v0.1 asset remains the verified historical release. |
| C2 — Manual Skill ZIP Installation (v0.2) | Verified | Download `cognitive-bridge-v0.2.0-beta.1.zip`, extract `cognitive-bridge/`, and import or open that folder. | The commit-derived v0.2 asset passed single-root inventory, clean extraction, compilation, repository regressions, behavior-contract validation, example-Vault QA, UTF-8, and privacy checks. A Source ZIP is still a different runtime input container. |
| D — Portable Export | Unverified | When an Agent cannot write directly to an Obsidian Vault, generate an Obsidian-ready ZIP for the user to download and extract. | The concept is supported by ordinary Markdown output, but the end-to-end export workflow is not yet validated. |

## Minimum package discovery

Regardless of installation mode, the Agent must be able to find:

- `SKILL.md`
- `references/`
- `prompts/`
- `templates/`
- `scripts/`

Tests, fictional examples, and docs are distribution support material and should remain available in the GitHub Beta package.

## Source Intake is not Skill installation

A structured Source ZIP is private runtime input. It is not the public Skill ZIP used by installation Mode C. Cognitive Bridge v0.2 accepts these Source modes through one pipeline:

- pasted Markdown text;
- one Markdown file;
- a structured directory;
- a structured Source ZIP.

None of these Source containers proves how a runtime discovered or loaded the Skill.

## v0.2 Beta recommended path

Use verified local-checkout Mode B1 or manual Skill ZIP Mode C2 in a disposable environment. Native GitHub installer behavior remains platform-specific and must be tested separately. Then run:

```text
Gemini Source Preparation Prompt
        ↓
copy the private Markdown result
        ↓
Cognitive Bridge
        ↓
new test Obsidian Vault
```

The private Source and generated personal Vault are runtime data. They are never part of the Skill installation or public repository. A directory or Source ZIP remains an optional advanced input.
