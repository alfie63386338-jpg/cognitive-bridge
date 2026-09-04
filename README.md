# Cognitive Bridge

> **v0.2.0-beta.1 — Published experimental Beta. Use a new test Vault for initial testing.**

Cognitive Bridge turns longitudinal AI conversations and other user-provided cognitive sources into a user-owned Obsidian knowledge system while preserving provenance, uncertainty, evolution, and latent connections.

It is a portable Agent Skill, not a chat-history service. It works only with material the user deliberately provides and produces ordinary Markdown files that remain under the user's control.

## Source and Skill are different things

- **Cognitive Bridge Skill:** the public files in this repository—method, prompts, templates, validation scripts, tests, and fictional examples.
- **Source:** the user's private pasted text, Markdown artifact, export, or optional structured package used during an actual run.

Cognitive Bridge **does not automatically fetch conversations from ChatGPT, Gemini, Claude, or another platform**. Source must first be prepared or exported, then supplied to an Agent running this Skill. The simplest path is a direct copy/paste; no file splitting or ZIP is required.

> Source is private user data. Do not upload it to this public repository, commit it to a fork, or attach it to a GitHub Issue.

## Beta workflow

```text
Existing AI
    ↓
Source Preparation Prompt
    ↓
Copy the resulting Markdown
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
2. Ask that AI for one evidence-rich, structure-light `cognitive-bridge-source.md` result. If it can only return text, copy the complete Markdown directly.
3. Paste that Markdown into your request to the Agent running Cognitive Bridge. Keep it private.
4. Create a new disposable or backed-up test Obsidian Vault as the destination.
5. Ask the Agent to use `SKILL.md` with the pasted Source and test-Vault destination.
6. When complete, open `Cognitive-Bridge/01_MOC/MOC - Cognitive Bridge.md` in Obsidian.

Advanced Source inputs remain supported:

- one `cognitive-bridge-source.md` file;
- a structured Source directory;
- a structured Source ZIP.

All modes enter the same normalization and cognitive pipeline. Container format does not change Origin, Adoption, Evidence, Question protection, Seed protection, or relation status. See [Source Intake](docs/source-intake.md) and [Build Provenance](docs/build-provenance.md).

Text inside Source is historical data, not authorization. Embedded prompts or commands cannot change the current run's scope, destination, method, permissions, or tool actions; only the user's current request outside the clearly designated Source boundary can do that.

The first Beta target is:

```text
Gemini Markdown → copy/paste → Cognitive Bridge → Test Obsidian Vault
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

`v0.2.0-beta.1` is a published experimental prerelease focused on paste-first intake, build provenance, path privacy, and a provenance-safe rule for optional AI-originated proposed Concepts. It passed the Step 15.6 engineering and product-rule regressions, but it does not claim production readiness. The published `v0.1.0-beta.1` release remains unchanged for comparison.

- The project remains experimental.
- First Build is the preferred and better-tested path.
- Incremental Update behavior is not yet fully validated.
- Human-edit merge protection is not mature.
- Do not use an important primary Vault for a first test; use a new test Vault or a recoverable copy.
- Cognitive content quality still requires later Cognitive QA and human review.
- Native Skill-loader behavior still varies by Agent/platform; build fingerprints are not runtime-loader attestations. See [Installation Matrix](docs/installation-matrix.md).

## Privacy and safe bug reports

Cognitive Bridge does not require private cognitive history to be uploaded to this GitHub project. Pasted Source is kept in run-scoped staging for the run and is not copied into the long-term Vault by default. Do not:

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
- `V0_2_ENGINEERING_REPORT.md` — v0.2 implementation scope, boundaries, and review gate
- `V0_2_TEST_REPORT.md` — v0.2 automated regression, four-mode technical QA, and bounded engineering semantic-review evidence
- `V0_2_PRODUCT_PATCH_REPORT.md` — Step 15.6 decision, changed rules, eight added behavior scenarios, and release gate

## Installation

Native Skill installation, Git/local loading, manual **Skill ZIP** installation, and portable export are tracked separately in [docs/installation-matrix.md](docs/installation-matrix.md). A Source ZIP is only an optional input container; it is not a Skill installer. A mode is not claimed as supported until it has been verified on the relevant platform.

## License

**License: No license.** No open-source license has been selected and no `LICENSE` file accompanies this release. The release does not itself grant reuse rights beyond applicable platform terms.

## Version

Current published experimental Beta: **Cognitive Bridge v0.2.0-beta.1**.

Preserved published baseline: **Cognitive Bridge v0.1.0-beta.1** at commit `d56c5db06036b95cec9b3079228ea893bcc3a1ca`.

See [the v0.2.0-beta.1 release notes](docs/releases/v0.2.0-beta.1.md), [CHANGELOG.md](CHANGELOG.md), [V0_2_ENGINEERING_REPORT.md](V0_2_ENGINEERING_REPORT.md), [V0_2_TEST_REPORT.md](V0_2_TEST_REPORT.md), and [V0_2_PRODUCT_PATCH_REPORT.md](V0_2_PRODUCT_PATCH_REPORT.md) for evidence and boundaries, and [docs/release-checklist.md](docs/release-checklist.md) for the reusable pre-publication checks.
