#!/usr/bin/env python3
"""Build deterministic Cognitive Bridge provenance without runtime attestation."""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

try:
    from ._script_utils import (
        append_text_safely,
        has_physical_absolute_path,
        portable_name_key,
        print_json,
        resolves_within,
        write_text_safely,
    )
except ImportError:
    from _script_utils import (  # type: ignore
        append_text_safely,
        has_physical_absolute_path,
        portable_name_key,
        print_json,
        resolves_within,
        write_text_safely,
    )


EXECUTION_MODES = ("first_build", "update_build")
INTAKE_MODES = (
    "pasted_text",
    "single_markdown",
    "structured_directory",
    "structured_zip",
)
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
DISCLAIMER = (
    "The execution fingerprint is a deterministic identifier for declared build "
    "inputs. It does not authenticate an agent, runtime, native loader, plugin "
    "invocation, or execution environment."
)


class ProvenanceError(ValueError):
    pass


def _single_line(value: str, label: str, *, max_length: int = 500) -> str:
    if (
        not isinstance(value, str)
        or not value.strip()
        or len(value) > max_length
        or "\r" in value
        or "\n" in value
    ):
        raise ProvenanceError(f"{label} must be a non-empty single-line value")
    return value


def _identifier(value: str, label: str) -> str:
    if not isinstance(value, str) or not IDENTIFIER_RE.fullmatch(value):
        raise ProvenanceError(f"{label} must be a portable identifier")
    return value


def _outcome(value: str, label: str) -> str:
    value = _single_line(value, label)
    if has_physical_absolute_path(value):
        raise ProvenanceError(f"{label} must not contain a physical absolute path")
    return value


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _hash_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _normalized_rule_bytes(path: Path) -> bytes:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as exc:
        raise ProvenanceError(f"canonical rule file is unreadable: {path.name}") from exc
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    return text.encode("utf-8")


def load_manifest(path: Path) -> tuple[dict[str, Any], Path]:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProvenanceError("build provenance manifest is unreadable or invalid") from exc
    required = {
        "cognitive_bridge_version",
        "protocol_version",
        "schema_version",
        "fingerprint_format",
        "canonical_rule_files",
    }
    if not isinstance(manifest, dict) or not required.issubset(manifest):
        raise ProvenanceError("build provenance manifest is missing required fields")
    for key in (
        "cognitive_bridge_version",
        "protocol_version",
        "schema_version",
        "fingerprint_format",
    ):
        _identifier(manifest[key], key)
    if (
        not isinstance(manifest["canonical_rule_files"], list)
        or not manifest["canonical_rule_files"]
    ):
        raise ProvenanceError("canonical_rule_files must be a non-empty list")
    project_root = path.resolve(strict=True).parent.parent
    return manifest, project_root


def build_provenance(
    manifest_path: Path,
    *,
    execution_mode: str,
    source_intake_mode: str,
    source_hashes: list[str],
) -> dict[str, Any]:
    if execution_mode not in EXECUTION_MODES:
        raise ProvenanceError(f"invalid execution mode: {execution_mode}")
    if source_intake_mode not in INTAKE_MODES:
        raise ProvenanceError(f"invalid source intake mode: {source_intake_mode}")
    normalized_hashes = sorted(set(source_hashes))
    if not normalized_hashes or any(not SHA256_RE.fullmatch(value) for value in normalized_hashes):
        raise ProvenanceError("at least one valid sha256: source hash is required")
    manifest, project_root = load_manifest(manifest_path)
    entries: list[dict[str, str]] = []
    seen_paths: set[str] = set()
    for raw_relative in manifest["canonical_rule_files"]:
        if not isinstance(raw_relative, str):
            raise ProvenanceError("canonical rule path must be a string")
        relative = Path(raw_relative)
        if relative in {Path(""), Path(".")} or relative.is_absolute() or ".." in relative.parts:
            raise ProvenanceError("canonical rule path must stay inside the project")
        portable_key = portable_name_key(relative.as_posix())
        if portable_key in seen_paths:
            raise ProvenanceError("canonical rule paths must be portable-unique")
        seen_paths.add(portable_key)
        path = project_root / relative
        if not path.is_file() or not resolves_within(path, project_root):
            raise ProvenanceError(f"canonical rule file is missing: {raw_relative}")
        current = project_root
        for part in relative.parts:
            current = current / part
            is_junction = getattr(current, "is_junction", lambda: False)
            if current.is_symlink() or is_junction():
                raise ProvenanceError(
                    f"canonical rule path must not traverse a link: {raw_relative}"
                )
        entries.append(
            {
                "path": relative.as_posix(),
                "sha256": _hash_bytes(_normalized_rule_bytes(path)),
            }
        )
    entries.sort(key=lambda item: item["path"])
    ruleset_hash = _hash_bytes(_canonical_json(entries))
    fingerprint_payload = {
        "fingerprint_format": manifest["fingerprint_format"],
        "cognitive_bridge_version": manifest["cognitive_bridge_version"],
        "protocol_version": manifest["protocol_version"],
        "schema_version": manifest["schema_version"],
        "ruleset_hash": ruleset_hash,
        "execution_mode": execution_mode,
        "source_intake_mode": source_intake_mode,
        "source_hashes": normalized_hashes,
    }
    return {
        **fingerprint_payload,
        "execution_fingerprint": _hash_bytes(_canonical_json(fingerprint_payload)),
        "build_provenance_manifest": manifest_path.resolve(strict=True)
        .relative_to(project_root)
        .as_posix(),
        "fingerprint_meaning": DISCLAIMER,
    }


def render_markdown(
    provenance: dict[str, Any],
    *,
    build_id: str,
    processed_at: str,
    source_ids: list[str],
    outcomes: dict[str, str],
) -> str:
    build_id = _identifier(build_id, "build ID")
    source_ids = [_identifier(value, "source ID") for value in source_ids]
    processed_at = _single_line(processed_at, "processed timestamp", max_length=100)
    try:
        parsed_time = datetime.datetime.fromisoformat(processed_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ProvenanceError("processed timestamp must be ISO 8601") from exc
    if parsed_time.tzinfo is None:
        raise ProvenanceError("processed timestamp must include a timezone")
    outcomes = {
        key: _outcome(value, key.replace("_", " ")) for key, value in outcomes.items()
    }
    quote = lambda value: json.dumps(str(value), ensure_ascii=False)
    hashes = "\n".join(f"  - {quote(value)}" for value in provenance["source_hashes"])
    ids = "\n".join(f"  - {quote(value)}" for value in source_ids)
    lines = [
        f"## {build_id}",
        "",
        "```yaml",
        f"build_id: {quote(build_id)}",
        f"processed_at: {quote(processed_at)}",
        f'cognitive_bridge_version: {quote(provenance["cognitive_bridge_version"])}',
        f'protocol_version: {quote(provenance["protocol_version"])}',
        f'schema_version: {quote(provenance["schema_version"])}',
        f'execution_mode: {quote(provenance["execution_mode"])}',
        f'source_intake_mode: {quote(provenance["source_intake_mode"])}',
        "source_ids:",
        ids,
        "source_hashes:",
        hashes,
        f'ruleset_hash: {quote(provenance["ruleset_hash"])}',
        f'execution_fingerprint: {quote(provenance["execution_fingerprint"])}',
        f'build_provenance_manifest: {quote(provenance["build_provenance_manifest"])}',
        f'created_nodes: {quote(outcomes["created_nodes"])}',
        f'updated_nodes: {quote(outcomes["updated_nodes"])}',
        f'skipped_work: {quote(outcomes["skipped_work"])}',
        f'conflicts: {quote(outcomes["conflicts"])}',
        f'review_items: {quote(outcomes["review_items"])}',
        "```",
        "",
        f"> {DISCLAIMER}",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=project_root / "references" / "build-provenance-manifest.json",
    )
    parser.add_argument("--execution-mode", choices=EXECUTION_MODES, required=True)
    parser.add_argument("--source-intake-mode", choices=INTAKE_MODES, required=True)
    parser.add_argument("--source-hash", action="append", required=True)
    parser.add_argument("--source-id", action="append")
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument("--output", type=Path, help="write one standalone entry")
    destination.add_argument(
        "--append-to", type=Path, help="atomically append the entry to an existing/legacy Build Log"
    )
    parser.add_argument("--build-id")
    parser.add_argument("--processed-at")
    parser.add_argument("--created-summary")
    parser.add_argument("--updated-summary")
    parser.add_argument("--skipped-summary")
    parser.add_argument("--conflicts-summary")
    parser.add_argument("--review-items-summary")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        provenance = build_provenance(
            args.manifest,
            execution_mode=args.execution_mode,
            source_intake_mode=args.source_intake_mode,
            source_hashes=args.source_hash,
        )
        if args.output or args.append_to:
            if not args.build_id:
                raise ProvenanceError("--build-id is required when writing an entry")
            outcomes = {
                "created_nodes": args.created_summary,
                "updated_nodes": args.updated_summary,
                "skipped_work": args.skipped_summary,
                "conflicts": args.conflicts_summary,
                "review_items": args.review_items_summary,
            }
            if not args.source_id or any(value is None for value in outcomes.values()):
                raise ProvenanceError(
                    "a written Build Log entry requires --source-id and all five outcome summaries"
                )
            processed_at = args.processed_at or datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()
            entry = render_markdown(
                provenance,
                build_id=args.build_id,
                processed_at=processed_at,
                source_ids=args.source_id,
                outcomes=outcomes,
            )
            if args.output:
                write_text_safely(args.output, entry, overwrite=args.force)
            else:
                if args.force:
                    raise ProvenanceError("--force is not used with --append-to")
                append_text_safely(args.append_to, entry, header="# Build Log")
    except FileExistsError:
        parser.error(f"output already exists: {args.output} (use --force to replace it)")
    except (OSError, ProvenanceError) as exc:
        parser.error(str(exc))
    print_json(provenance)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
