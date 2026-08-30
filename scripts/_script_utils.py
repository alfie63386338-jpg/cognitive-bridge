#!/usr/bin/env python3
"""Shared deterministic helpers for the Cognitive Bridge engineering scripts."""
from __future__ import annotations

import html
import json
import os
import re
import sys
import tempfile
import unicodedata
from pathlib import Path
from typing import Any


FENCE_START_RE = re.compile(r"^[ \t]*(?P<marker>`{3,}|~{3,})")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def configure_text_streams() -> None:
    """Prevent an unencodable path from crashing human-readable CLI output."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="backslashreplace")
            except (AttributeError, OSError, ValueError):
                pass


def require_directory(parser: Any, path: Path, label: str = "root") -> Path:
    """Return an existing directory or terminate through argparse."""
    path = path.expanduser()
    try:
        exists = path.exists()
        is_dir = path.is_dir()
    except OSError as exc:
        parser.error(f"cannot inspect {label} directory {path}: {exc}")
    if not exists:
        parser.error(f"{label} directory does not exist: {path}")
    if not is_dir:
        parser.error(f"{label} path is not a directory: {path}")
    return path


def markdown_files(root: Path) -> list[Path]:
    """Return Markdown files in a cross-platform deterministic order."""
    return sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file() and path.suffix.casefold() == ".md"
        ),
        key=lambda path: unicodedata.normalize(
            "NFC", path.relative_to(root).as_posix()
        ).casefold(),
    )


def read_utf8(path: Path) -> str:
    """Read strict UTF-8 while accepting the optional UTF-8 BOM."""
    return path.read_text(encoding="utf-8-sig")


def markdown_visible_text(text: str) -> str:
    """Remove fenced code and HTML comments from Markdown link-scanning input."""
    text = HTML_COMMENT_RE.sub("", text)
    visible: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines(keepends=True):
        if fence_character is None:
            match = FENCE_START_RE.match(line)
            if match:
                marker = match.group("marker")
                fence_character = marker[0]
                fence_length = len(marker)
                visible.append("\n" if line.endswith(("\n", "\r")) else "")
                continue
            visible.append(line)
            continue

        closing = re.match(
            rf"^[ \t]*{re.escape(fence_character)}{{{fence_length},}}[ \t]*(?:\r?\n)?$",
            line,
        )
        if closing:
            fence_character = None
            fence_length = 0
        visible.append("\n" if line.endswith(("\n", "\r")) else "")
    return "".join(visible)


def relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def portable_name_key(value: str) -> str:
    """Normalize names for case-insensitive and Unicode-normalizing filesystems."""
    return unicodedata.normalize("NFC", value).casefold()


def split_frontmatter(text: str) -> tuple[str | None, str | None]:
    """Split Obsidian-style frontmatter, returning a sentinel when unterminated."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "UNTERMINATED", None
    return text[4:end], text[end + 5 :]


def frontmatter_scalar(frontmatter: str | None, key: str) -> str | None:
    """Read a simple quoted or unquoted top-level scalar from frontmatter."""
    if not frontmatter or frontmatter == "UNTERMINATED":
        return None
    pattern = re.compile(
        rf'^{re.escape(key)}:\s*(?:"([^"]*)"|\'([^\']*)\'|([^#\n]*?))'
        rf'\s*(?:#.*)?$',
        re.MULTILINE,
    )
    match = pattern.search(frontmatter)
    if not match:
        return None
    return next((value for value in match.groups() if value is not None), "").strip()


def print_json(value: Any) -> None:
    """Emit ASCII-safe JSON even under legacy Windows console encodings."""
    print(json.dumps(value, ensure_ascii=True, indent=2))


def markdown_code_cell(value: str) -> str:
    """Render an arbitrary filename safely inside a Markdown table cell."""
    escaped = html.escape(value, quote=False).replace("|", "&#124;")
    escaped = escaped.replace("\r", "\\r").replace("\n", "\\n")
    return f"<code>{escaped}</code>"


def is_within(path: Path, directory: Path) -> bool:
    """Check lexical and resolved containment (including the directory itself)."""
    path_absolute = path.absolute()
    directory_absolute = directory.absolute()
    lexical = path_absolute == directory_absolute or path_absolute.is_relative_to(
        directory_absolute
    )
    try:
        path_resolved = path.resolve(strict=False)
        directory_resolved = directory.resolve(strict=True)
        resolved = path_resolved == directory_resolved or path_resolved.is_relative_to(
            directory_resolved
        )
    except OSError:
        resolved = False
    return lexical or resolved


def write_text_safely(path: Path, text: str, *, overwrite: bool = False) -> None:
    """Write UTF-8 text without overwriting unless explicitly authorized."""
    path = path.expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not overwrite:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        return

    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_name = handle.name
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
        temporary_name = None
    finally:
        if temporary_name is not None:
            try:
                Path(temporary_name).unlink()
            except FileNotFoundError:
                pass


configure_text_streams()
