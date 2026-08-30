# Cognitive Bridge

> **v0.1 Beta — Experimental. Use a new test Vault for initial testing.**

Cognitive Bridge turns longitudinal AI conversations and other user-provided cognitive sources into a user-owned Obsidian knowledge system while preserving provenance, uncertainty, evolution, and latent connections.

It is a portable Agent Skill, not a chat-history service. It works only with material the user deliberately provides and produces ordinary Markdown files that remain under the user's control.

## Source and Skill are different things

- **Cognitive Bridge Skill:** the public files in this repository—method, prompts, templates, validation scripts, tests, and fictional examples.
- **Source Package:** the user's private conversation history or prepared evidence package used during an actual run.

Cognitive Bridge **does not automatically fetch conversations from ChatGPT, Gemini, Claude, or another platform**. A Source Package must first be prepared or exported, then supplied to an Agent running this Skill.

> A Source Package is private user data. Do not upload it to this public repository, commit it to a fork, or attach it to a GitHub Issue.

## Beta workflow

```text
Existing AI
    ↓
Source Preparation Prompt
    ↓
Private Source Package
    ↓
Cognitive Bridge
    ↓
Obsidian-native output
```

## Quick start

1. Choose the preparation prompt for the AI that currently holds the relevant history:
   - **Gemini Beta 1 path:** [Gemini Source Preparation Prompt](prompts/prepare-source-gemini.md)
   - [ChatGPT Source Preparation Prompt](prompts/prepare-source-chatgpt.md)
   - [Claude Source Preparation Prompt](prompts/prepare-source-claude.md)
   - [Generic AI Source Preparation Prompt](prompts/prepare-source-generic-ai.md)
2. Ask that AI to create an evidence-rich, structure-light Source Package.
3. Keep the Source Package private and provide it directly to the Agent that will run Cognitive Bridge.
4. Create a new disposable or backed-up test Obsidian Vault as the destination.
5. Ask the Agent to use `SKILL.md` with the private Source and test-Vault destination.
6. When complete, open `Cognitive-Bridge/01_MOC/MOC - Cognitive Bridge.md` in Obsidian.

The first Beta target is:

```text
Gemini Source → Cognitive Bridge → Test Obsidian Vault
```

## What the Skill produces

By default, output is isolated under a safe namespace:

```text
Cognitive-Bridge/
├── 00_System/
├── 01_MOC/
├── 02_Discussions/
├── 03_Ideas/
├── 04_Concepts/
├── 05_Questions/
├── 06_Seeds/
├── 07_Sources/
├── 08_Review/
└── 09_Archive/
```

The result distinguishes user evidence from AI contribution, preserves unknown history as unknown, keeps AI-proposed connections and questions reviewable, and records changes in ordinary Markdown. No Obsidian plugin is required for the core files.

## What it will not do

Cognitive Bridge will not:

- access conversations or files the user did not provide;
- infer a perfect model, “true self,” hidden motive, or compulsory life philosophy;
- silently turn prior AI output into evidence that the user historically believed it;
- close a Question merely because an AI supplied an answer;
- overwrite an important existing Vault by default;
- require users to understand internal provenance codes before reading the result.

## Current Beta limitations

`v0.1.0-beta.1` is intended to test installation and end-to-end workflow friction, not to claim production readiness.

- The project remains experimental.
- First Build is the preferred and better-tested path.
- Incremental Update behavior is not yet fully validated.
- Human-edit merge protection is not mature.
- Do not use an important primary Vault for a first test; use a new test Vault or a recoverable copy.
- Cognitive content quality still requires later Cognitive QA and human review.
- Installation behavior varies by Agent/platform; see [Installation Matrix](docs/installation-matrix.md).

## Privacy and safe bug reports

Cognitive Bridge does not require private cognitive history to be uploaded to this GitHub project. Do not:

- create an Issue containing a real Source Package;
- commit a Source Package to a fork or branch;
- upload a private generated Vault to a public repository;
- publish test logs that quote or reconstruct private Source;
- include API keys, tokens, credentials, or environment files in a report.

For bug reports, create a small synthetic or anonymized reproduction. If a problem cannot be reproduced without private content, report only the technical symptom and ask for a safe disclosure path before sharing data.

## Repository map

- `SKILL.md` — Agent entry point and eight-phase orchestration
- `references/` — canonical method and output rules
- `prompts/` — Source Preparation prompts
- `templates/` — Obsidian Markdown templates
- `scripts/` — deterministic technical validators
- `tests/` — fictional behavior contracts and regressions
- `examples/` — fictional example Source and output Vault
- `docs/` — development, installation, and release documentation

## Installation

Native Skill installation, Git/local loading, manual ZIP installation, and portable export are tracked separately in [docs/installation-matrix.md](docs/installation-matrix.md). A mode is not claimed as supported until it has been verified on the relevant platform.

## License

**License: To be determined before public release.** No open-source license has been selected. Until the owner explicitly chooses one, the repository should be created with **No license**.

## Version

Current distribution target: **Cognitive Bridge v0.1.0-beta.1**.

See [CHANGELOG.md](CHANGELOG.md) for changes and [docs/release-checklist.md](docs/release-checklist.md) for distribution checks.
