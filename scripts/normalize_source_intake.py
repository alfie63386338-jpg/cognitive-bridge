#!/usr/bin/env python3
"""Normalize supported Source inputs into one run-scoped, format-neutral model.

This module performs transport work only: byte preservation, safe ZIP extraction,
strict UTF-8 validation, deterministic ordering, and hashing. It never assigns
cognitive Origin, Adoption, Evidence, note types, or relations.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import shutil
import stat
import sys
import unicodedata
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from ._script_utils import (
        has_physical_absolute_path,
        is_within,
        portable_name_key,
        print_json,
    )
except ImportError:
    from _script_utils import (  # type: ignore
        has_physical_absolute_path,
        is_within,
        portable_name_key,
        print_json,
    )


INTAKE_SCHEMA_VERSION = "1"
INTAKE_MODES = (
    "pasted_text",
    "single_markdown",
    "structured_directory",
    "structured_zip",
)
SUPPORTED_SUFFIXES = {".md", ".txt", ".json", ".html"}
MEDIA_TYPES = {
    ".md": "text/markdown",
    ".txt": "text/plain",
    ".json": "application/json",
    ".html": "text/html",
}
MAX_FILES = 2_000
MAX_MEMBER_BYTES = 64 * 1024 * 1024
MAX_TOTAL_BYTES = 256 * 1024 * 1024
MAX_COMPRESSION_RATIO = 200
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
DRIVE_RE = re.compile(r"^[A-Za-z]:")
WINDOWS_INVALID_SEGMENT_RE = re.compile(r'[<>:"|?*\x00-\x1f]')
WINDOWS_DEVICE_RE = re.compile(
    r"^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)", re.I
)


class IntakeError(ValueError):
    """A source cannot be normalized without crossing a safety boundary."""


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _validate_text(
    data: bytes, logical_name: str, *, allow_empty: bool = False
) -> bool:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise IntakeError(f"source artifact is not valid UTF-8: {logical_name}") from exc
    has_content = bool(text.strip())
    if not has_content and not allow_empty:
        raise IntakeError(f"source artifact is empty: {logical_name}")
    return has_content


def _read_path_limited(path: Path, logical_name: str) -> bytes:
    """Read at most one artifact limit plus a sentinel byte."""
    try:
        with path.open("rb") as handle:
            data = handle.read(MAX_MEMBER_BYTES + 1)
    except OSError as exc:
        raise IntakeError(f"cannot read source artifact: {logical_name}") from exc
    if len(data) > MAX_MEMBER_BYTES:
        raise IntakeError(
            f"source artifact exceeds the {MAX_MEMBER_BYTES}-byte safety limit: "
            f"{logical_name}"
        )
    return data


def _safe_relative_name(value: str) -> str:
    value = unicodedata.normalize("NFC", value.replace("\\", "/"))
    if not value or value.startswith(("/", "//")) or DRIVE_RE.match(value):
        raise IntakeError("source artifact name must be a safe relative identifier")
    raw_parts = value.split("/")
    if (
        not raw_parts
        or any(part in {"", ".", ".."} for part in raw_parts)
        or any(
            WINDOWS_INVALID_SEGMENT_RE.search(part)
            or part.endswith((".", " "))
            or WINDOWS_DEVICE_RE.match(part)
            for part in raw_parts
        )
    ):
        raise IntakeError("source artifact name contains an unsafe path segment")
    return "/".join(PurePosixPath(value).parts)


def _safe_logical_source_name(value: str) -> str:
    value = unicodedata.normalize("NFC", value.strip())
    if (
        not value
        or len(value) > 200
        or "\n" in value
        or "\r" in value
        or "/" in value
        or "\\" in value
        or DRIVE_RE.match(value)
        or value in {".", ".."}
    ):
        raise IntakeError("logical source name must be a short name, not a path")
    return value


def safe_metadata_label(value: str | None, label: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise IntakeError(f"{label} must be a short single-line value")
    value = unicodedata.normalize("NFC", value.strip())
    if (
        not value
        or len(value) > 200
        or any(ch in value for ch in "\r\n")
        or has_physical_absolute_path(value)
    ):
        raise IntakeError(f"{label} must be a short single-line value")
    return value


def normalize_include(values: list[str] | None) -> set[str]:
    if values is None:
        return set(SUPPORTED_SUFFIXES)
    normalized = {
        (value if value.startswith(".") else f".{value}").casefold()
        for value in values
        if value.strip()
    }
    if not normalized:
        raise IntakeError("include list must contain at least one extension")
    return normalized


def _artifact(
    logical_name: str,
    data: bytes,
    include_suffixes: set[str] | None = None,
    *,
    allow_empty: bool = False,
) -> dict[str, Any]:
    logical_name = _safe_relative_name(logical_name)
    suffix = PurePosixPath(logical_name).suffix.casefold()
    include_suffixes = include_suffixes or SUPPORTED_SUFFIXES
    if suffix not in include_suffixes:
        raise IntakeError(f"unsupported source artifact type: {logical_name}")
    if len(data) > MAX_MEMBER_BYTES:
        raise IntakeError(
            f"source artifact exceeds the {MAX_MEMBER_BYTES}-byte safety limit: "
            f"{logical_name}"
        )
    has_content = _validate_text(data, logical_name, allow_empty=allow_empty)
    return {
        "logical_name": logical_name,
        "media_type": MEDIA_TYPES.get(suffix, "text/plain"),
        "bytes": len(data),
        "sha256": sha256_bytes(data),
        "_has_content": has_content,
        "data": data,
    }


def _directory_artifacts(
    root: Path, include_suffixes: set[str]
) -> list[dict[str, Any]]:
    root_resolved = root.resolve(strict=True)
    candidates: list[Path] = []
    declared_total = 0
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.casefold() not in include_suffixes:
            continue
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise IntakeError(f"source package contains a linked artifact: {relative}")
        candidates.append(path)
        if len(candidates) > MAX_FILES:
            raise IntakeError(
                f"source package exceeds the {MAX_FILES}-artifact safety limit"
            )
        try:
            declared_size = path.stat().st_size
        except OSError as exc:
            raise IntakeError(f"cannot inspect source artifact: {relative}") from exc
        if declared_size > MAX_MEMBER_BYTES:
            raise IntakeError(
                f"source artifact exceeds the {MAX_MEMBER_BYTES}-byte safety limit: "
                f"{relative}"
            )
        declared_total += declared_size
        if declared_total > MAX_TOTAL_BYTES:
            raise IntakeError("source package exceeds the total-size safety limit")
    candidates.sort(
        key=lambda path: portable_name_key(path.relative_to(root).as_posix())
    )
    artifacts: list[dict[str, Any]] = []
    seen: set[str] = set()
    actual_total = 0
    for path in candidates:
        relative = path.relative_to(root).as_posix()
        resolved = path.resolve(strict=True)
        if resolved != root_resolved and not resolved.is_relative_to(root_resolved):
            raise IntakeError(f"source artifact resolves outside the package: {relative}")
        logical_name = _safe_relative_name(relative)
        key = portable_name_key(logical_name)
        if key in seen:
            raise IntakeError("source package contains duplicate portable artifact names")
        seen.add(key)
        data = _read_path_limited(path, logical_name)
        actual_total += len(data)
        if actual_total > MAX_TOTAL_BYTES:
            raise IntakeError("source package exceeds the total-size safety limit")
        artifacts.append(
            _artifact(logical_name, data, include_suffixes, allow_empty=True)
        )
    return artifacts


def _zip_artifacts(path: Path, include_suffixes: set[str]) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    seen: set[str] = set()
    total_bytes = 0
    file_count = 0
    try:
        archive = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as exc:
        raise IntakeError("source ZIP is unreadable or invalid") from exc
    with archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            file_count += 1
            if file_count > MAX_FILES:
                raise IntakeError(f"source ZIP exceeds the {MAX_FILES}-file safety limit")
            if info.flag_bits & 0x1:
                raise IntakeError("encrypted ZIP members are not supported")
            mode = (info.external_attr >> 16) & 0o170000
            if mode == stat.S_IFLNK:
                raise IntakeError("source ZIP contains a symbolic link")
            logical_name = _safe_relative_name(info.filename)
            key = portable_name_key(logical_name)
            if key in seen:
                raise IntakeError("source ZIP contains duplicate portable member names")
            seen.add(key)
            total_bytes += info.file_size
            if info.file_size > MAX_MEMBER_BYTES or total_bytes > MAX_TOTAL_BYTES:
                raise IntakeError("source ZIP exceeds the uncompressed-size safety limit")
            ratio = info.file_size / max(info.compress_size, 1)
            if info.file_size > 1024 * 1024 and ratio > MAX_COMPRESSION_RATIO:
                raise IntakeError("source ZIP has an unsafe compression ratio")
            if PurePosixPath(logical_name).suffix.casefold() not in include_suffixes:
                continue
            try:
                with archive.open(info) as member:
                    data = member.read(MAX_MEMBER_BYTES + 1)
            except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
                raise IntakeError(f"cannot read ZIP member: {logical_name}") from exc
            if len(data) != info.file_size:
                raise IntakeError(f"ZIP member size does not match metadata: {logical_name}")
            artifacts.append(
                _artifact(logical_name, data, include_suffixes, allow_empty=True)
            )
    return artifacts


def _aggregate_source_hash(artifacts: list[dict[str, Any]]) -> str:
    # Transport/container metadata is excluded, but a structured artifact's
    # safe logical role remains bound to its bytes. This preserves identity
    # across equivalent containers while detecting content swapped between
    # meaningfully named package artifacts.
    content_manifest = sorted(
        (
            {
                "logical_name": _safe_relative_name(item["logical_name"]),
                "bytes": item["bytes"],
                "sha256": item["sha256"],
            }
            for item in artifacts
        ),
        key=lambda item: portable_name_key(item["logical_name"]),
    )
    encoded = json.dumps(
        content_manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def build_intake(
    *,
    mode: str,
    artifacts: list[dict[str, Any]],
    logical_source_name: str,
    source_ai: str | None = None,
    run_id: str | None = None,
) -> dict[str, Any]:
    if mode not in INTAKE_MODES:
        raise IntakeError(f"unsupported source intake mode: {mode}")
    if not artifacts:
        raise IntakeError("source contains no supported readable artifacts")
    artifacts = sorted(artifacts, key=lambda item: portable_name_key(item["logical_name"]))
    if len(artifacts) > MAX_FILES:
        raise IntakeError(f"source exceeds the {MAX_FILES}-artifact safety limit")
    total_bytes = sum(int(item["bytes"]) for item in artifacts)
    if total_bytes > MAX_TOTAL_BYTES:
        raise IntakeError("source exceeds the total-size safety limit")
    if not any(bool(item.get("_has_content", True)) for item in artifacts):
        raise IntakeError("source contains no non-empty readable artifacts")
    source_hash = _aggregate_source_hash(artifacts)
    public_artifacts = []
    for index, item in enumerate(artifacts, 1):
        public_artifacts.append(
            {
                "artifact_id": f"source-{index:03d}",
                "logical_name": item["logical_name"],
                "media_type": item["media_type"],
                "bytes": item["bytes"],
                "sha256": item["sha256"],
                "normalized_relative_path": f"artifacts/{item['logical_name']}",
            }
        )
    intake: dict[str, Any] = {
        "intake_schema_version": INTAKE_SCHEMA_VERSION,
        "source_id": f"cb-source-{source_hash.removeprefix('sha256:')[:32]}",
        "logical_source_name": _safe_logical_source_name(logical_source_name),
        "source_type": (
            "markdown"
            if mode in {"pasted_text", "single_markdown"}
            else "structured_package"
        ),
        "source_intake_mode": mode,
        "source_location": "run-scoped" if mode == "pasted_text" else "external",
        "source_hash": source_hash,
        "artifact_count": len(public_artifacts),
        "total_bytes": total_bytes,
        "processed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "raw_representation_preserved": True,
        "vault_persistence_default": False,
        "evidence_policy": "content-and-provenance-not-container",
        "artifacts": public_artifacts,
    }
    source_ai = safe_metadata_label(source_ai, "source AI")
    run_id = safe_metadata_label(run_id, "run ID")
    if source_ai is not None:
        intake["source_ai"] = source_ai
    if run_id is not None:
        intake["run_id"] = run_id
    intake["_artifact_bytes"] = [item["data"] for item in artifacts]
    return intake


def collect_path(
    source: Path,
    *,
    mode: str | None = None,
    logical_name: str | None = None,
    source_ai: str | None = None,
    run_id: str | None = None,
    include_suffixes: set[str] | None = None,
) -> dict[str, Any]:
    source = source.expanduser()
    if not source.exists():
        raise IntakeError("source does not exist")
    include_suffixes = include_suffixes or set(SUPPORTED_SUFFIXES)
    if mode is None:
        if source.is_dir():
            mode = "structured_directory"
        elif source.suffix.casefold() == ".md":
            mode = "single_markdown"
        elif source.suffix.casefold() == ".zip":
            mode = "structured_zip"
        else:
            raise IntakeError("source path must be a Markdown file, directory, or ZIP")
    if mode == "pasted_text":
        raise IntakeError("pasted_text intake requires --stdin")
    if mode == "single_markdown":
        if not source.is_file() or source.suffix.casefold() != ".md":
            raise IntakeError("single_markdown intake requires one .md file")
        artifacts = [
            _artifact(
                "cognitive-bridge-source.md",
                _read_path_limited(source, "cognitive-bridge-source.md"),
            )
        ]
        default_name = "cognitive-bridge-source.md"
    elif mode == "structured_directory":
        if not source.is_dir():
            raise IntakeError("structured_directory intake requires a directory")
        artifacts = _directory_artifacts(source, include_suffixes)
        default_name = "cognitive-bridge-source-package"
    elif mode == "structured_zip":
        if not source.is_file() or source.suffix.casefold() != ".zip":
            raise IntakeError("structured_zip intake requires a .zip file")
        artifacts = _zip_artifacts(source, include_suffixes)
        default_name = "cognitive-bridge-source-package"
    else:
        raise IntakeError(f"unsupported source intake mode: {mode}")
    return build_intake(
        mode=mode,
        artifacts=artifacts,
        logical_source_name=logical_name or default_name,
        source_ai=source_ai,
        run_id=run_id,
    )


def collect_pasted_text(
    data: bytes,
    *,
    logical_name: str | None = None,
    source_ai: str | None = None,
    run_id: str | None = None,
) -> dict[str, Any]:
    artifact_name = "cognitive-bridge-source.md"
    return build_intake(
        mode="pasted_text",
        artifacts=[_artifact(artifact_name, data)],
        logical_source_name=logical_name or artifact_name,
        source_ai=source_ai,
        run_id=run_id,
    )


def public_manifest(intake: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in intake.items() if not key.startswith("_")}


def load_intake_manifest(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise IntakeError("intake manifest is unreadable or invalid JSON") from exc
    if not isinstance(payload, dict) or payload.get("intake_schema_version") != "1":
        raise IntakeError("unsupported intake manifest schema")
    mode = payload.get("source_intake_mode")
    if mode not in INTAKE_MODES:
        raise IntakeError("intake manifest has an invalid source_intake_mode")
    source_hash = payload.get("source_hash")
    if not isinstance(source_hash, str) or not SHA256_RE.fullmatch(source_hash):
        raise IntakeError("intake manifest has an invalid source_hash")
    name = payload.get("logical_source_name")
    if not isinstance(name, str):
        raise IntakeError("intake manifest is missing logical_source_name")
    _safe_logical_source_name(name)
    expected_source_id = f"cb-source-{source_hash.removeprefix('sha256:')[:32]}"
    if payload.get("source_id") != expected_source_id:
        raise IntakeError("intake manifest source_id does not match source_hash")
    expected_source_type = (
        "markdown"
        if mode in {"pasted_text", "single_markdown"}
        else "structured_package"
    )
    if payload.get("source_type") != expected_source_type:
        raise IntakeError("intake manifest has an invalid source_type")
    expected_location = "run-scoped" if mode == "pasted_text" else "external"
    if payload.get("source_location") != expected_location:
        raise IntakeError("intake manifest has an invalid source_location")
    if payload.get("evidence_policy") != "content-and-provenance-not-container":
        raise IntakeError("intake manifest has an invalid evidence_policy")
    if payload.get("raw_representation_preserved") is not True:
        raise IntakeError("intake manifest does not attest raw representation preservation")
    if payload.get("vault_persistence_default") is not False:
        raise IntakeError("intake manifest has an invalid Vault persistence default")
    processed_at = safe_metadata_label(payload.get("processed_at"), "processed timestamp")
    try:
        parsed_time = datetime.datetime.fromisoformat(
            processed_at.replace("Z", "+00:00")
        )
    except (AttributeError, ValueError) as exc:
        raise IntakeError("intake manifest processed_at must be ISO 8601") from exc
    if parsed_time.tzinfo is None:
        raise IntakeError("intake manifest processed_at must include a timezone")
    if "source_ai" in payload:
        if safe_metadata_label(payload.get("source_ai"), "source AI") is None:
            raise IntakeError("intake manifest source_ai must be omitted when unknown")
    if "run_id" in payload:
        if safe_metadata_label(payload.get("run_id"), "run ID") is None:
            raise IntakeError("intake manifest run_id must be omitted when unknown")
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise IntakeError("intake manifest has no artifacts")
    if len(artifacts) > MAX_FILES:
        raise IntakeError("intake manifest exceeds the artifact-count safety limit")
    if type(payload.get("artifact_count")) is not int or payload["artifact_count"] != len(artifacts):
        raise IntakeError("intake manifest artifact_count does not match artifacts")
    seen: set[str] = set()
    portable_order: list[str] = []
    aggregate_items: list[dict[str, Any]] = []
    total_bytes = 0
    has_content = False
    for index, item in enumerate(artifacts, 1):
        if not isinstance(item, dict):
            raise IntakeError("intake manifest artifact is invalid")
        logical = item.get("logical_name")
        digest = item.get("sha256")
        if not isinstance(logical, str) or not isinstance(digest, str):
            raise IntakeError("intake manifest artifact metadata is incomplete")
        logical = _safe_relative_name(logical)
        key = portable_name_key(logical)
        if key in seen:
            raise IntakeError("intake manifest contains duplicate portable artifact names")
        seen.add(key)
        portable_order.append(key)
        if not SHA256_RE.fullmatch(digest):
            raise IntakeError("intake manifest artifact hash is invalid")
        if item.get("artifact_id") != f"source-{index:03d}":
            raise IntakeError("intake manifest artifact_id order is invalid")
        if item.get("normalized_relative_path") != f"artifacts/{logical}":
            raise IntakeError("intake manifest normalized path is invalid")
        media_type = safe_metadata_label(item.get("media_type"), "artifact media type")
        expected_media_type = MEDIA_TYPES.get(
            PurePosixPath(logical).suffix.casefold(), "text/plain"
        )
        if media_type != expected_media_type:
            raise IntakeError("intake manifest artifact media type is invalid")
        if media_type is None:
            raise IntakeError("intake manifest artifact media type is missing")
        size = item.get("bytes")
        if type(size) is not int or size < 0 or size > MAX_MEMBER_BYTES:
            raise IntakeError("intake manifest artifact byte count is invalid")
        artifact_path = path.parent.joinpath(
            *PurePosixPath(item["normalized_relative_path"]).parts
        )
        if artifact_path.is_symlink() or not artifact_path.is_file():
            raise IntakeError("intake manifest artifact is unavailable")
        try:
            artifact_resolved = artifact_path.resolve(strict=True)
            staging_resolved = path.parent.resolve(strict=True)
        except OSError as exc:
            raise IntakeError("intake manifest artifact is unavailable") from exc
        if (
            artifact_resolved != staging_resolved
            and not artifact_resolved.is_relative_to(staging_resolved)
        ):
            raise IntakeError("intake manifest artifact resolves outside staging")
        data = artifact_path.read_bytes()
        has_content = (
            _validate_text(
                data,
                logical,
                allow_empty=mode in {"structured_directory", "structured_zip"},
            )
            or has_content
        )
        if len(data) != size or sha256_bytes(data) != digest:
            raise IntakeError("intake manifest artifact content does not match metadata")
        aggregate_items.append(
            {"logical_name": logical, "bytes": size, "sha256": digest}
        )
        total_bytes += size
    if portable_order != sorted(portable_order):
        raise IntakeError("intake manifest artifacts are not in deterministic order")
    if type(payload.get("total_bytes")) is not int or payload["total_bytes"] != total_bytes:
        raise IntakeError("intake manifest total_bytes does not match artifacts")
    if total_bytes > MAX_TOTAL_BYTES:
        raise IntakeError("intake manifest exceeds the total-size safety limit")
    if not has_content:
        raise IntakeError("intake manifest contains no non-empty readable artifacts")
    if _aggregate_source_hash(aggregate_items) != source_hash:
        raise IntakeError("intake manifest source_hash does not match artifacts")
    return payload


def materialize(intake: dict[str, Any], output: Path) -> Path:
    output = output.expanduser()
    if output.exists():
        raise IntakeError("normalization output already exists")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir()
    try:
        artifact_bytes = intake.get("_artifact_bytes", [])
        artifacts = intake["artifacts"]
        if len(artifact_bytes) != len(artifacts):
            raise IntakeError("normalization artifacts are unavailable")
        for metadata, data in zip(artifacts, artifact_bytes):
            relative = _safe_relative_name(metadata["normalized_relative_path"])
            destination = output.joinpath(*PurePosixPath(relative).parts)
            if not is_within(destination, output):
                raise IntakeError("normalized artifact would escape the run directory")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        manifest_path = output / "intake-manifest.json"
        manifest_path.write_text(
            json.dumps(public_manifest(intake), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        return manifest_path
    except Exception:
        shutil.rmtree(output, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source", type=Path)
    group.add_argument("--stdin", action="store_true", help="read pasted UTF-8 Source from stdin")
    parser.add_argument("--output", type=Path, required=True, help="new run-scoped directory outside the Vault")
    parser.add_argument("--intake-mode", choices=INTAKE_MODES)
    parser.add_argument("--logical-name")
    parser.add_argument("--source-ai", help="record only when explicitly known")
    parser.add_argument("--run-id")
    parser.add_argument(
        "--include",
        nargs="*",
        help="package text extensions; defaults to md txt json html",
    )
    parser.add_argument("--vault-root", type=Path, help="reject staging inside this Vault")
    args = parser.parse_args()
    try:
        if args.vault_root is not None and is_within(args.output, args.vault_root):
            raise IntakeError("normalization output must be outside the long-term Vault")
        if args.source is not None:
            expanded_source = args.source.expanduser()
            output_conflicts = (
                is_within(args.output, expanded_source)
                if expanded_source.is_dir()
                else args.output.absolute() == expanded_source.absolute()
            )
            if output_conflicts:
                raise IntakeError("normalization output must be outside the read-only source location")
        if args.stdin:
            if args.intake_mode not in (None, "pasted_text"):
                raise IntakeError("--stdin can only use pasted_text intake")
            pasted_bytes = sys.stdin.buffer.read(MAX_MEMBER_BYTES + 1)
            if len(pasted_bytes) > MAX_MEMBER_BYTES:
                raise IntakeError(
                    f"pasted Source exceeds the {MAX_MEMBER_BYTES}-byte safety limit"
                )
            intake = collect_pasted_text(
                pasted_bytes,
                logical_name=args.logical_name,
                source_ai=args.source_ai,
                run_id=args.run_id,
            )
        else:
            intake = collect_path(
                args.source,
                mode=args.intake_mode,
                logical_name=args.logical_name,
                source_ai=args.source_ai,
                run_id=args.run_id,
                include_suffixes=normalize_include(args.include),
            )
        materialize(intake, args.output)
    except (IntakeError, OSError) as exc:
        parser.error(str(exc))
    print_json(
        {
            "ok": True,
            "manifest": "intake-manifest.json",
            "source_id": intake["source_id"],
            "source_hash": intake["source_hash"],
            "source_intake_mode": intake["source_intake_mode"],
            "artifact_count": intake["artifact_count"],
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
