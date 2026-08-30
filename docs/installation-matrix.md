# Cognitive Bridge Installation Matrix

This matrix records evidence, not platform assumptions. Status values are `Verified`, `Unverified`, `Unsupported`, or `Unknown`.

| Mode | Status | Intended path | Current evidence and boundary |
|---|---|---|---|
| A — Native Skill Installation | Unverified | Install `cognitive-bridge/` through a platform's native Skill mechanism. | The package shape is valid, but no specific external platform installation has been completed for Beta 1. |
| B1 — Git / Local Skill Installation | Verified | Clone the repository or point an Agent at a local checkout containing `SKILL.md`. | A fresh non-local-optimized clone of the release commit into a new temporary directory passed required-component discovery, strict UTF-8 checks, compilation, 19 unit tests, all 18 behavior-contract cases, and all 7 example-Vault validators on 2026-08-30. Retrieval from the future GitHub remote remains unverified until publication. |
| B2 — GitHub Skill Installation | Unknown | Install directly from a GitHub repository if the Agent supports that feature. | Platform support has not been claimed or tested. |
| C — Manual ZIP Installation | Verified | Download `cognitive-bridge-v0.1.0-beta.1.zip`, extract `cognitive-bridge/`, and import or open that folder. | The local release candidate was built from the Git index, extracted into a fresh temporary directory, and passed compilation, 19 unit tests, all 18 behavior-contract cases, all 7 example-Vault validators, strict UTF-8 checks, and the distribution privacy scan on 2026-08-30. GitHub asset retrieval remains pending publication. |
| D — Portable Export | Unverified | When an Agent cannot write directly to an Obsidian Vault, generate an Obsidian-ready ZIP for the user to download and extract. | The concept is supported by ordinary Markdown output, but the end-to-end export workflow is not yet validated. |

## Minimum package discovery

Regardless of installation mode, the Agent must be able to find:

- `SKILL.md`
- `references/`
- `prompts/`
- `templates/`
- `scripts/`

Tests, fictional examples, and docs are distribution support material and should remain available in the GitHub Beta package.

## Beta 1 recommended path

Use verified Mode B1 or C in a disposable environment for Beta 1. GitHub-hosted retrieval must still be rechecked after publication. Then run:

```text
Gemini Source Preparation Prompt
        ↓
private Source Package
        ↓
Cognitive Bridge
        ↓
new test Obsidian Vault
```

The private Source Package and generated personal Vault are runtime data. They are never part of the Skill installation or public repository.
