#!/usr/bin/env python3
"""Detect default-private paths and unsupported runtime claims in a built Vault."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    from ._script_utils import (
        frontmatter_scalar,
        markdown_files,
        physical_absolute_path_matches,
        print_json,
        read_utf8,
        require_directory,
        split_frontmatter,
    )
except ImportError:
    from _script_utils import (  # type: ignore
        frontmatter_scalar,
        markdown_files,
        physical_absolute_path_matches,
        print_json,
        read_utf8,
        require_directory,
        split_frontmatter,
    )


UNSUPPORTED_CLAIM_PATTERNS = (
    re.compile(
        r"\bnative(?:\s+skill)?\s+loader\s+"
        r"(?:(?:is|was)\s+|has\s+been\s+)?(?:confirmed|verified|loaded)\b",
        re.I,
    ),
    re.compile(
        r"\bruntime\s+skill\s+(?:(?:is|was)\s+|has\s+been\s+)?loaded\b",
        re.I,
    ),
    re.compile(
        r"\bcodex\s+(?:has\s+)?verified\s+(?:the\s+)?installation\b", re.I
    ),
    re.compile(
        r"\bplugin\s+invocation\s+"
        r"(?:(?:is|was)\s+|has\s+been\s+)?confirmed\b",
        re.I,
    ),
)
RUNTIME_ATTESTATION_RE = re.compile(
    r"^\s*(?:"
    r"runtime[_ -]?skill[_ -]?loaded|"
    r"native(?:[_ -]?skill)?[_ -]?loader[_ -]?(?:confirmed|verified|loaded)|"
    r"plugin[_ -]?invocation[_ -]?(?:confirmed|verified)|"
    r"codex[_ -]?verified[_ -]?installation"
    r")\s*:\s*(?:[\"']\s*)?(?:true|yes|1|confirmed|verified|loaded)"
    r"(?:\s*[\"'])?\s*(?:#.*)?$",
    re.I | re.M,
)
V02_SOURCE_RECORD_RE = re.compile(r"^## Source record:\s", re.M)
V02_BUILD_FIELD_RE = re.compile(r"^cognitive_bridge_version:\s", re.M)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _legacy_prefix_end(path: Path, text: str) -> int:
    """Return the byte-character boundary before append-only v0.2 metadata."""
    if path.name == "Source Registry.md":
        record = V02_SOURCE_RECORD_RE.search(text)
        if record:
            return record.start()
        if "| Source ID | Source Name | Source Type | Intake Mode |" in text:
            return 0
        return len(text)
    if path.name == "Build Log.md":
        version = V02_BUILD_FIELD_RE.search(text)
        if version:
            heading = text.rfind("\n## ", 0, version.start())
            return 0 if heading < 0 else heading + 1
        return len(text)
    return 0


def inspect_file(
    path: Path, root: Path
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    relative = path.relative_to(root).as_posix()
    try:
        text = read_utf8(path)
    except (OSError, UnicodeDecodeError):
        return ([{"file": relative, "line": 1, "kind": "unreadable_utf8"}], [])
    issues: list[dict[str, object]] = []
    warnings: list[dict[str, object]] = []
    is_audit_surface = (
        relative.startswith("00_System/")
        or path.name in {"Build Log.md", "QA Report.md", "Source Registry.md"}
    )
    if is_audit_surface:
        seen_claim_offsets: set[int] = set()
        for pattern in UNSUPPORTED_CLAIM_PATTERNS:
            for match in pattern.finditer(text):
                if match.start() in seen_claim_offsets:
                    continue
                seen_claim_offsets.add(match.start())
                issues.append(
                    {
                        "file": relative,
                        "line": line_number(text, match.start()),
                        "kind": "unsupported_runtime_claim",
                    }
                )
        for match in RUNTIME_ATTESTATION_RE.finditer(text):
            if match.start() in seen_claim_offsets:
                continue
            seen_claim_offsets.add(match.start())
            issues.append(
                {
                    "file": relative,
                    "line": line_number(text, match.start()),
                    "kind": "unsupported_runtime_attestation",
                }
            )
    frontmatter, _ = split_frontmatter(text)
    sensitive_value = frontmatter_scalar(frontmatter, "potentially_sensitive_metadata")
    allow_sensitive_paths = (
        sensitive_value is not None
        and sensitive_value.casefold() in {"true", "yes", "1"}
    )
    if not allow_sensitive_paths:
        legacy_prefix_end = _legacy_prefix_end(path, text)
        seen_offsets: set[int] = set()
        for match in physical_absolute_path_matches(text):
            if match.start() in seen_offsets:
                continue
            seen_offsets.add(match.start())
            item = {
                "file": relative,
                "line": line_number(text, match.start()),
                "kind": (
                    "legacy_absolute_path_warning"
                    if match.start() < legacy_prefix_end
                    else "absolute_path_candidate"
                ),
            }
            (warnings if match.start() < legacy_prefix_end else issues).append(item)
    return issues, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = require_directory(parser, args.root)
    issues: list[dict[str, object]] = []
    warnings: list[dict[str, object]] = []
    for path in markdown_files(root):
        file_issues, file_warnings = inspect_file(path, root)
        issues.extend(file_issues)
        warnings.extend(file_warnings)
    result = {"ok": not issues, "issues": issues, "warnings": warnings}
    if args.json:
        print_json(result)
    else:
        print("Persistent metadata: PASS" if not issues else "Persistent metadata: NEEDS REVIEW")
        for warning in warnings:
            print(
                f"- {warning['file']}:{warning['line']} "
                f"({warning['kind']})"
            )
        for issue in issues:
            print(f"- {issue['file']}:{issue['line']} ({issue['kind']})")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
