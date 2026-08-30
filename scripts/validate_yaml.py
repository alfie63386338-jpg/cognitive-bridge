#!/usr/bin/env python3
"""Validate Markdown YAML frontmatter under a Cognitive Bridge Vault.

Uses PyYAML when available. Without PyYAML, performs conservative delimiter and
key-shape checks so the tool remains useful in a stdlib-only environment.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

try:
    from ._script_utils import (
        markdown_files,
        print_json,
        read_utf8,
        relative_posix,
        require_directory,
        split_frontmatter,
    )
except ImportError:
    from _script_utils import (  # type: ignore
        markdown_files,
        print_json,
        read_utf8,
        relative_posix,
        require_directory,
        split_frontmatter,
    )

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

PAIR_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:")


def top_level_key_issues(frontmatter: str):
    issues = []
    seen = set()
    for i, line in enumerate(frontmatter.splitlines(), 1):
        if line.startswith("\t"):
            issues.append(f"line {i}: tab indentation is not valid YAML")
            continue
        if line.startswith(" ") or not line.strip() or line.lstrip().startswith("#"):
            continue
        match = PAIR_RE.match(line)
        if not match:
            issues.append(f"line {i}: suspicious YAML syntax: {line!r}")
            continue
        key = match.group(1)
        if key in seen:
            issues.append(f"line {i}: duplicate top-level key: {key}")
        seen.add(key)
    return issues


def basic_scalar_issues(frontmatter: str):
    """Catch malformed flow/quoted values without pretending to parse all YAML."""
    issues = []
    for i, line in enumerate(frontmatter.splitlines(), 1):
        if line.startswith((" ", "\t")):
            continue
        match = PAIR_RE.match(line)
        if not match:
            continue
        value = line[match.end() :].strip()
        if value in {"?", ":", "-"}:
            issues.append(f"line {i}: reserved YAML indicator must be quoted: {value}")
        elif value.startswith("[") and not value.endswith("]"):
            issues.append(f"line {i}: unterminated flow sequence")
        elif value.startswith("{") and not value.endswith("}"):
            issues.append(f"line {i}: unterminated flow mapping")
        elif value.startswith('"') and not re.search(r'(?<!\\)"\s*(?:#.*)?$', value[1:]):
            issues.append(f"line {i}: unterminated double-quoted scalar")
        elif value.startswith("'") and not re.search(r"'\s*(?:#.*)?$", value[1:]):
            issues.append(f"line {i}: unterminated single-quoted scalar")
        elif (
            value
            and not value.startswith(('"', "'", "[", "{", "|", ">", "-"))
            and re.search(r":(?:[ \t]|$)", value)
        ):
            issues.append(f"line {i}: unquoted scalar contains a mapping indicator")
    return issues

def validate_file(path: Path):
    text = read_utf8(path)
    fm, _ = split_frontmatter(text)
    issues = []
    if fm is None:
        return issues
    if fm == 'UNTERMINATED':
        return ['unterminated frontmatter']
    issues.extend(top_level_key_issues(fm))
    if yaml:
        try:
            data = yaml.safe_load(fm)
            if data is not None and not isinstance(data, dict):
                issues.append('frontmatter root is not a mapping')
        except Exception as e:
            issues.append(f'YAML parse error: {e}')
    else:
        issues.extend(basic_scalar_issues(fm))
    return issues

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root', type=Path)
    ap.add_argument('--json', action='store_true')
    ns = ap.parse_args()
    ns.root = require_directory(ap, ns.root)
    rows = []
    for p in markdown_files(ns.root):
        try:
            issues = validate_file(p)
        except (OSError, UnicodeError) as exc:
            issues = [f'cannot read as UTF-8: {exc}']
        for issue in issues:
            rows.append({'file': relative_posix(p, ns.root), 'issue': issue})
    result = {'ok': not rows, 'issues': rows, 'parser': 'pyyaml' if yaml else 'basic'}
    if ns.json:
        print_json(result)
    else:
        print('YAML/frontmatter OK' if result['ok'] else f"Found {len(rows)} frontmatter issue(s)")
        for r in rows: print(f"- {r['file']}: {r['issue']}")
    return 0 if result['ok'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
