#!/usr/bin/env python3
"""Validate the deterministic structure of the behavioral test contract.

This validator does not pretend to judge generative cognitive output. It checks
that every required case has a readable case specification, fictional fixture,
positive expectation, negative assertion, and (for update cases) a concrete
baseline Vault state with observable preservation sentinels.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent

CASES = {
    "01": "clean-long-term-source",
    "02": "sparse-source",
    "03": "mixed-ownership",
    "04": "agreement-not-integration",
    "05": "genuine-a-to-u",
    "06": "evolution-gap",
    "07": "retrospective",
    "08": "cross-domain-link",
    "09": "false-similarity",
    "10": "internal-contradiction",
    "11": "no-core-theme",
    "12": "seed-protection",
    "13": "open-question",
    "14": "existing-vault-conflict",
    "15": "human-edited-note",
    "16": "rejected-relation",
    "17": "reopen-with-new-evidence",
    "18": "ai-feedback-contamination",
    "19": "ai-concept-no-uptake",
    "20": "ai-concept-passive-agreement",
    "21": "ai-concept-active-exploration",
    "22": "ai-concept-later-active-reuse",
    "23": "direct-ai-origin-evidence",
    "24": "reconstructed-ai-origin-evidence",
    "25": "decorative-ai-label",
    "26": "ai-concept-adoption-contamination",
}

CASE_HEADINGS = (
    "Purpose",
    "Input",
    "Expected behavior",
    "Forbidden behavior",
    "QA criteria",
)
EXPECTED_HEADINGS = ("Must", "Must not")
QA_REQUIREMENTS = (
    "evidence-constrained",
    "Unknown history remains unknown",
    "explicit/inferred",
    "No destructive destination writes",
)

INCREMENTAL_REQUIREMENTS = {
    "14": {
        "files": (
            "source.md",
            "existing-vault/Concepts/Freedom.md",
        ),
        "tokens": {
            "existing-vault/Concepts/Freedom.md": (
                "CASE14-USER-FILE-SENTINEL",
            ),
        },
    },
    "15": {
        "files": (
            "source.md",
            "run-1-source.md",
            "existing-vault/Cognitive-Bridge/03_Ideas/Support should build independence.md",
            "existing-vault/Cognitive-Bridge/00_System/Source Registry.md",
            "existing-vault/Cognitive-Bridge/00_System/Build Log.md",
            "existing-vault/Cognitive-Bridge/00_System/User Decisions.md",
        ),
        "tokens": {
            "existing-vault/Cognitive-Bridge/03_Ideas/Support should build independence.md": (
                "cb-idea-humaned1",
                "CASE15-HUMAN-EDIT-SENTINEL",
            ),
            "existing-vault/Cognitive-Bridge/00_System/Source Registry.md": (
                "src-case15-run1",
                "cb-build-case15-001",
                "sha256:6f2c0957dc98dfbb87e107476778034bfda787650bd61c6330ac7ec25b93b8c1",
            ),
            "existing-vault/Cognitive-Bridge/00_System/Build Log.md": (
                "cb-build-case15-001",
                "cb-idea-humaned1",
            ),
        },
    },
    "16": {
        "files": (
            "source.md",
            "existing-vault/Cognitive-Bridge/03_Ideas/Teaching Support.md",
            "existing-vault/Cognitive-Bridge/03_Ideas/AI Support.md",
            "existing-vault/Cognitive-Bridge/00_System/User Decisions.md",
            "existing-vault/Cognitive-Bridge/08_Review/Review - Proposed Connections.md",
        ),
        "tokens": {
            "existing-vault/Cognitive-Bridge/00_System/User Decisions.md": (
                "cb-rel-rj0001",
                "decision_id: cb-decision-rjcase160001",
                "decision: rejected",
                "supersedes: null",
                "CASE16-REJECTION-SENTINEL",
            ),
            "existing-vault/Cognitive-Bridge/08_Review/Review - Proposed Connections.md": (
                "cb-rel-rj0001",
                "Status:** rejected",
            ),
        },
    },
    "17": {
        "files": (
            "source.md",
            "existing-vault/Cognitive-Bridge/03_Ideas/Teaching Support.md",
            "existing-vault/Cognitive-Bridge/03_Ideas/AI Support.md",
            "existing-vault/Cognitive-Bridge/00_System/User Decisions.md",
            "existing-vault/Cognitive-Bridge/08_Review/Review - Proposed Connections.md",
        ),
        "tokens": {
            "source.md": ("support should help me stand on my own later",),
            "existing-vault/Cognitive-Bridge/00_System/User Decisions.md": (
                "cb-rel-rj0001",
                "decision_id: cb-decision-rjcase170001",
                "decision: rejected",
                "supersedes: null",
                "CASE17-REJECTION-HISTORY-SENTINEL",
            ),
        },
    },
    "18": {
        "files": (
            "source.md",
            "run-1-source.md",
            "existing-vault/Cognitive-Bridge/04_Concepts/Autonomy Gradient.md",
            "existing-vault/Cognitive-Bridge/00_System/Source Registry.md",
            "existing-vault/Cognitive-Bridge/00_System/Build Log.md",
        ),
        "tokens": {
            "existing-vault/Cognitive-Bridge/04_Concepts/Autonomy Gradient.md": (
                "cb-concept-autonomy-gradient",
                "term_status: project-defined",
                "origin: A0",
                "adoption: unconfirmed",
                "CASE18-AI-PROVENANCE-SENTINEL",
            ),
            "existing-vault/Cognitive-Bridge/00_System/Source Registry.md": (
                "src-case18-run1",
                "sha256:8ffa893725881a00afad12cdf32345a7053f4ccf7f538e582ab8a359414e45f8",
                "Generated Vault notes are not Source Registry entries",
            ),
            "existing-vault/Cognitive-Bridge/00_System/Build Log.md": (
                "cb-build-case18-001",
                "cb-concept-autonomy-gradient",
            ),
        },
    },
    "22": {
        "files": (
            "source.md",
            "run-1-source.md",
            "existing-vault/Cognitive-Bridge/04_Concepts/Reversibility Margin.md",
            "existing-vault/Cognitive-Bridge/00_System/Source Registry.md",
            "existing-vault/Cognitive-Bridge/00_System/Build Log.md",
        ),
        "tokens": {
            "source.md": (
                "using the reversibility margin from our earlier discussion",
            ),
            "existing-vault/Cognitive-Bridge/04_Concepts/Reversibility Margin.md": (
                "cb-concept-reversibility-margin",
                "origin: A0",
                "adoption: unconfirmed",
                "CASE22-AI-FIRST-SENTINEL",
            ),
            "existing-vault/Cognitive-Bridge/00_System/Source Registry.md": (
                "src-case22-run1",
            ),
            "existing-vault/Cognitive-Bridge/00_System/Build Log.md": (
                "cb-build-case22-001",
            ),
        },
    },
    "26": {
        "files": (
            "source.md",
            "run-1-source.md",
            "existing-vault/Cognitive-Bridge/04_Concepts/Autonomy Gradient.md",
            "existing-vault/Cognitive-Bridge/00_System/Source Registry.md",
            "existing-vault/Cognitive-Bridge/00_System/Build Log.md",
        ),
        "tokens": {
            "source.md": (
                "temperature gradient",
            ),
            "existing-vault/Cognitive-Bridge/04_Concepts/Autonomy Gradient.md": (
                "cb-concept-adoption-guard",
                "origin: A0",
                "adoption: unconfirmed",
                "evidence_level: E3",
                "CASE26-NO-UPTAKE-SENTINEL",
            ),
            "existing-vault/Cognitive-Bridge/00_System/Source Registry.md": (
                "src-case26-run1",
            ),
            "existing-vault/Cognitive-Bridge/00_System/Build Log.md": (
                "cb-build-case26-001",
            ),
        },
    },
}


def read_utf8(path: Path, issues: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(f"missing file: {path.relative_to(ROOT)}")
    except UnicodeDecodeError as exc:
        issues.append(f"not valid UTF-8: {path.relative_to(ROOT)} ({exc})")
    return ""


def sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^## ([^\r\n]+)\r?$", text))
    result = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[match.group(1).strip()] = text[start:end].strip()
    return result


def normalized_assertion(text: str) -> str:
    bullet = re.search(r"(?m)^\s*-\s+(.+)$", text)
    if bullet:
        text = bullet.group(1)
    text = re.sub(r"(?m)^\s*-\s*", "", text.strip())
    return " ".join(text.split()).casefold()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def validate() -> tuple[list[str], dict[str, str]]:
    issues: list[str] = []
    baseline_hashes: dict[str, str] = {}

    case_names = {path.name for path in (ROOT / "cases").glob("case-*.md")}
    expected_case_names = {f"case-{case_id}-{slug}.md" for case_id, slug in CASES.items()}
    for name in sorted(expected_case_names - case_names):
        issues.append(f"missing case specification: cases/{name}")
    for name in sorted(case_names - expected_case_names):
        issues.append(f"unexpected case specification: cases/{name}")

    expected_names = {path.name for path in (ROOT / "expected").glob("*.md")}
    required_expected_names = {f"{case_id}-{slug}.md" for case_id, slug in CASES.items()}
    for name in sorted(required_expected_names - expected_names):
        issues.append(f"missing expected constraints: expected/{name}")
    for name in sorted(expected_names - required_expected_names):
        issues.append(f"unexpected expected constraints: expected/{name}")

    fixture_names = {path.name for path in (ROOT / "fixtures").iterdir() if path.is_dir()}
    required_fixture_names = {f"{case_id}-{slug}" for case_id, slug in CASES.items()}
    for name in sorted(required_fixture_names - fixture_names):
        issues.append(f"missing fixture directory: fixtures/{name}")
    for name in sorted(fixture_names - required_fixture_names):
        issues.append(f"unexpected fixture directory: fixtures/{name}")

    for case_id, slug in CASES.items():
        case_path = ROOT / "cases" / f"case-{case_id}-{slug}.md"
        expected_path = ROOT / "expected" / f"{case_id}-{slug}.md"
        fixture_dir = ROOT / "fixtures" / f"{case_id}-{slug}"
        source_path = fixture_dir / "source.md"

        case_text = read_utf8(case_path, issues)
        expected_text = read_utf8(expected_path, issues)
        source_text = read_utf8(source_path, issues)
        case_sections = sections(case_text)
        expected_sections = sections(expected_text)

        for heading in CASE_HEADINGS:
            if not case_sections.get(heading):
                issues.append(f"{case_path.relative_to(ROOT)}: missing/non-empty section {heading}")
        for heading in EXPECTED_HEADINGS:
            if not expected_sections.get(heading):
                issues.append(f"{expected_path.relative_to(ROOT)}: missing/non-empty section {heading}")

        if case_sections.get("Expected behavior") and expected_sections.get("Must"):
            if normalized_assertion(case_sections["Expected behavior"]) != normalized_assertion(
                expected_sections["Must"]
            ):
                issues.append(f"case {case_id}: Expected behavior and Must constraints diverge")
        if case_sections.get("Forbidden behavior") and expected_sections.get("Must not"):
            if normalized_assertion(case_sections["Forbidden behavior"]) != normalized_assertion(
                expected_sections["Must not"]
            ):
                issues.append(f"case {case_id}: Forbidden behavior and Must not constraints diverge")

        qa_text = case_sections.get("QA criteria", "")
        for phrase in QA_REQUIREMENTS:
            if phrase not in qa_text:
                issues.append(f"case {case_id}: QA criteria missing phrase: {phrase}")

        if source_text and not any(
            "Fictional" in line for line in source_text.splitlines()[0:2]
        ):
            issues.append(f"case {case_id}: source fixture is not explicitly labeled fictional")

    case01_dir = ROOT / "fixtures" / "01-clean-long-term-source"
    case01_sources = sorted(case01_dir.glob("*.md"))
    if len(case01_sources) < 3:
        issues.append("case 01: rich longitudinal fixture must span at least three Source files")
    case01_text = "\n".join(read_utf8(path, issues) for path in case01_sources)
    for year in ("2024", "2025", "2026"):
        if year not in case01_text:
            issues.append(f"case 01: longitudinal fixture missing year {year}")
    if "User:" not in case01_text or "AI:" not in case01_text:
        issues.append("case 01: fixture must expose both user and AI contribution signals")

    for case_id, requirement in INCREMENTAL_REQUIREMENTS.items():
        fixture_dir = ROOT / "fixtures" / f"{case_id}-{CASES[case_id]}"
        for relative in requirement["files"]:
            path = fixture_dir / relative
            if not path.is_file():
                issues.append(f"case {case_id}: missing incremental fixture file {relative}")
                continue
            read_utf8(path, issues)
            if relative.startswith("existing-vault/"):
                baseline_hashes[str(path.relative_to(ROOT)).replace("\\", "/")] = sha256(path)
        for relative, tokens in requirement["tokens"].items():
            path = fixture_dir / relative
            text = read_utf8(path, issues)
            for token in tokens:
                if token not in text:
                    issues.append(f"case {case_id}: {relative} missing anchor {token}")

    contamination_source = read_utf8(
        ROOT / "fixtures" / "18-ai-feedback-contamination" / "source.md", issues
    )
    if "temperature gradient" not in contamination_source.casefold():
        issues.append("case 18: run-2 Source is missing the unrelated lexical-overlap trap")
    for forbidden in ("Autonomy Gradient", "cb-concept-autonomy-gradient", "src-case18-run1"):
        if forbidden in contamination_source:
            issues.append(
                f"case 18: run-2 Source improperly contains prior generated-state token {forbidden}"
            )

    adoption_contamination_source = read_utf8(
        ROOT / "fixtures" / "26-ai-concept-adoption-contamination" / "source.md",
        issues,
    )
    if "temperature gradient" not in adoption_contamination_source.casefold():
        issues.append("case 26: run-2 Source is missing the unrelated lexical-overlap trap")
    for forbidden in (
        "Autonomy Gradient",
        "cb-concept-adoption-guard",
        "src-case26-run1",
    ):
        if forbidden in adoption_contamination_source:
            issues.append(
                "case 26: run-2 Source improperly contains prior generated-state token "
                f"{forbidden}"
            )

    return issues, baseline_hashes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable results")
    args = parser.parse_args()

    issues, baseline_hashes = validate()
    result = {
        "ok": not issues,
        "case_count": len(CASES),
        "issues": issues,
        "incremental_baseline_sha256": baseline_hashes,
        "scope": "contract structure and fixture integrity only",
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    elif issues:
        print(f"Behavior contract FAIL ({len(issues)} issue(s))")
        for issue in issues:
            print(f"- {issue}")
    else:
        print(
            f"Behavior contract OK: {len(CASES)} case/fixture/expected triplets and "
            "incremental preservation anchors are structurally valid."
        )
        print("Note: generative behavior still requires observed run outputs and manual review.")
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
