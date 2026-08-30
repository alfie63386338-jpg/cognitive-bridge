#!/usr/bin/env python3
"""Validate type-scoped Cognitive Bridge note status values."""
from __future__ import annotations

import argparse
from pathlib import Path

try:
    from ._script_utils import (
        frontmatter_scalar,
        markdown_files,
        print_json,
        read_utf8,
        relative_posix,
        require_directory,
        split_frontmatter,
    )
except ImportError:
    from _script_utils import (  # type: ignore
        frontmatter_scalar,
        markdown_files,
        print_json,
        read_utf8,
        relative_posix,
        require_directory,
        split_frontmatter,
    )


ALLOWED_STATUSES = {
    "idea": {
        "developing",
        "reasoned",
        "stable",
        "core",
        "dormant",
        "superseded",
        "rejected",
    },
    "concept": {"proposed", "developing", "stable", "deprecated"},
    "question": {"open", "refined", "dormant", "closed"},
    "seed": {"seed", "promoted", "dormant"},
    "discussion": {"developing", "reasoned", "revisited", "closed"},
    "moc": {"active", "dormant", "archived"},
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    args.root = require_directory(parser, args.root)

    issues = []
    for path in markdown_files(args.root):
        relative = relative_posix(path, args.root)
        try:
            text = read_utf8(path)
        except (OSError, UnicodeError) as exc:
            issues.append({"file": relative, "issue": f"cannot read as UTF-8: {exc}"})
            continue

        frontmatter, _ = split_frontmatter(text)
        note_type = frontmatter_scalar(frontmatter, "type")
        if note_type not in ALLOWED_STATUSES:
            continue
        status = frontmatter_scalar(frontmatter, "status")
        if status is None:
            issues.append(
                {"file": relative, "issue": f"missing status for type: {note_type}"}
            )
        elif status not in ALLOWED_STATUSES[note_type]:
            allowed = ", ".join(sorted(ALLOWED_STATUSES[note_type]))
            issues.append(
                {
                    "file": relative,
                    "issue": (
                        f"invalid status for type {note_type}: {status} "
                        f"(allowed: {allowed})"
                    ),
                }
            )

    result = {"ok": not issues, "issues": issues}
    if args.json:
        print_json(result)
    elif issues:
        print(f"Found {len(issues)} type-scoped status issue(s)")
        for issue in issues:
            print(f"- {issue['file']}: {issue['issue']}")
    else:
        print("Type-scoped statuses OK")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
