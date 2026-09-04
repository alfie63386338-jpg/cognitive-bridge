#!/usr/bin/env python3
"""Create a path-minimized Source Registry from any supported intake form.

The legacy ``SOURCE_DIR OUTPUT`` invocation remains valid. All path inputs use
the same format-neutral intake model as ``normalize_source_intake.py``. Hashes
support duplicate identity; they are never cognitive evidence.
"""
from __future__ import annotations

import argparse
import datetime
from pathlib import Path

try:
    from ._script_utils import (
        append_text_safely,
        is_within,
        markdown_code_cell,
        write_text_safely,
    )
    from .normalize_source_intake import (
        INTAKE_MODES,
        IntakeError,
        collect_path,
        load_intake_manifest,
        normalize_include,
        public_manifest,
        safe_metadata_label,
    )
except ImportError:
    from _script_utils import (  # type: ignore
        append_text_safely,
        is_within,
        markdown_code_cell,
        write_text_safely,
    )
    from normalize_source_intake import (  # type: ignore
        INTAKE_MODES,
        IntakeError,
        collect_path,
        load_intake_manifest,
        normalize_include,
        public_manifest,
        safe_metadata_label,
    )


def _cell(value: object) -> str:
    return markdown_code_cell(str(value))


def _record_lines(
    intake: dict[str, object], *, processed_at: str, build_id: str | None
) -> list[str]:
    source_location = intake.get("source_location")
    if source_location not in {"external", "run-scoped"}:
        source_location = "external"
    lines = [
        f"**Processed at:** {_cell(processed_at)}",
        "",
        "| Source ID | Source Name | Source Type | Intake Mode | Source Location | Artifacts | Bytes | SHA-256 |",
        "|---|---|---|---|---|---:|---:|---|",
        "| "
        + " | ".join(
            [
                _cell(intake["source_id"]),
                _cell(intake["logical_source_name"]),
                _cell(intake["source_type"]),
                _cell(intake["source_intake_mode"]),
                _cell(source_location),
                str(intake["artifact_count"]),
                str(intake["total_bytes"]),
                f"`{intake['source_hash']}`",
            ]
        )
        + " |",
    ]
    if build_id:
        lines += ["", f"**Build ID:** {_cell(build_id)}"]
    source_ai = intake.get("source_ai")
    if isinstance(source_ai, str) and source_ai:
        lines += ["", f"**Source AI/platform (explicit):** {_cell(source_ai)}"]
    run_id = intake.get("run_id")
    if isinstance(run_id, str) and run_id:
        lines += ["", f"**Run ID:** {_cell(run_id)}"]
    lines += [
        "",
        "## Source components",
        "",
        "Component names below are logical, package-relative identifiers; physical Source paths are not persisted.",
        "",
        "| Artifact ID | Logical Name | Media Type | Bytes | SHA-256 |",
        "|---|---|---|---:|---|",
    ]
    artifacts = intake.get("artifacts", [])
    if not isinstance(artifacts, list):
        raise IntakeError("intake manifest artifacts are invalid")
    for item in artifacts:
        if not isinstance(item, dict):
            raise IntakeError("intake manifest artifact is invalid")
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(item.get("artifact_id", "")),
                    _cell(item["logical_name"]),
                    _cell(item.get("media_type", "text/plain")),
                    str(item.get("bytes", "")),
                    f"`{item['sha256']}`",
                ]
            )
            + " |"
        )
    lines += [
        "",
        "> Hashes support duplicate-ingestion detection. Container format does not raise or lower Evidence, and hashes do not establish historical or ownership evidence.",
        "",
    ]
    return lines


def render_registry(
    intake: dict[str, object], *, processed_at: str, build_id: str | None
) -> str:
    lines = [
        "# Source Registry",
        "",
        f"**Registry refreshed:** {datetime.date.today().isoformat()}",
        "",
        *_record_lines(intake, processed_at=processed_at, build_id=build_id),
    ]
    return "\n".join(lines)


def render_registry_entry(
    intake: dict[str, object], *, processed_at: str, build_id: str | None
) -> str:
    lines = [
        f"## Source record: {_cell(intake['source_id'])}",
        "",
        *_record_lines(intake, processed_at=processed_at, build_id=build_id),
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source", type=Path, help="Markdown, directory, ZIP, or normalized intake manifest"
    )
    parser.add_argument("output", type=Path, nargs="?")
    parser.add_argument(
        "--append-to",
        type=Path,
        help="append one v0.2 Source record while preserving an existing/legacy registry",
    )
    parser.add_argument("--intake-mode", choices=INTAKE_MODES)
    parser.add_argument("--logical-name")
    parser.add_argument("--source-ai", help="record only when explicitly known")
    parser.add_argument("--run-id")
    parser.add_argument(
        "--include",
        nargs="*",
        default=None,
        help="legacy directory/package text extensions; defaults to md txt json html",
    )
    parser.add_argument("--build-id")
    parser.add_argument("--processed-at")
    parser.add_argument(
        "--force",
        action="store_true",
        help="explicitly replace an existing registry; never use as an update-build strategy",
    )
    args = parser.parse_args()
    source = args.source.expanduser()
    if (args.output is None) == (args.append_to is None):
        parser.error("provide exactly one output path or --append-to path")
    output = (args.output or args.append_to).expanduser()
    append_mode = args.append_to is not None
    try:
        if not source.exists():
            raise IntakeError("source does not exist")
        is_manifest = source.is_file() and source.suffix.casefold() == ".json"
        if source.is_dir() or is_manifest:
            source_boundary = source if source.is_dir() else source.parent
            if is_within(output, source_boundary):
                raise IntakeError("output must be outside the read-only source location")
        elif output.resolve(strict=False) == source.resolve(strict=True):
            raise IntakeError("output must not replace the read-only Source")
        if args.force and append_mode:
            raise IntakeError("--force cannot be used with --append-to")
        if output.exists() and not args.force and not append_mode:
            raise FileExistsError
        if is_manifest:
            intake = load_intake_manifest(source)
        else:
            intake = public_manifest(
                collect_path(
                    source,
                    mode=args.intake_mode,
                    logical_name=args.logical_name,
                    source_ai=args.source_ai,
                    run_id=args.run_id,
                    include_suffixes=normalize_include(args.include),
                )
            )
        # Explicit CLI metadata may supplement a run-scoped manifest, but is
        # never inferred from the physical path or filename.
        if args.source_ai:
            intake["source_ai"] = safe_metadata_label(args.source_ai, "source AI")
        if args.run_id:
            intake["run_id"] = safe_metadata_label(args.run_id, "run ID")
        build_id = safe_metadata_label(args.build_id, "build ID")
        processed_at = safe_metadata_label(
            args.processed_at or intake.get("processed_at"), "processed timestamp"
        )
        if processed_at is None:
            raise IntakeError("processed timestamp is unavailable")
        try:
            parsed_time = datetime.datetime.fromisoformat(
                processed_at.replace("Z", "+00:00")
            )
        except ValueError as exc:
            raise IntakeError("processed timestamp must be ISO 8601") from exc
        if parsed_time.tzinfo is None:
            raise IntakeError("processed timestamp must include a timezone")
        if append_mode:
            if output.exists():
                existing = output.read_text(encoding="utf-8-sig")
                if str(intake["source_id"]) in existing:
                    raise IntakeError("Source Registry already contains this Source ID")
            text = render_registry_entry(
                intake, processed_at=processed_at, build_id=build_id
            )
            append_text_safely(output, text, header="# Source Registry")
        else:
            text = render_registry(
                intake, processed_at=processed_at, build_id=build_id
            )
            write_text_safely(output, text, overwrite=args.force)
    except FileExistsError:
        parser.error(f"output already exists: {output} (use --force to replace it)")
    except (IntakeError, OSError, KeyError, TypeError, ValueError) as exc:
        parser.error(str(exc))
    print(f"Wrote Source Registry with {intake['artifact_count']} source artifact(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
