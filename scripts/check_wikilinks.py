#!/usr/bin/env python3
"""Report missing or ambiguous Obsidian WikiLink targets."""
from __future__ import annotations
import argparse, json, re
from collections import defaultdict
from pathlib import Path

try:
    from ._script_utils import (
        markdown_files,
        markdown_visible_text,
        portable_name_key,
        print_json,
        read_utf8,
        relative_posix,
        require_directory,
    )
except ImportError:
    from _script_utils import (  # type: ignore
        markdown_files,
        markdown_visible_text,
        portable_name_key,
        print_json,
        read_utf8,
        relative_posix,
        require_directory,
    )

LINK_RE = re.compile(r'\[\[([^\]]+)\]\]')

def normalize_target(raw: str):
    target = raw.split('|', 1)[0].split('#', 1)[0].strip()
    if target.lower().endswith('.md'):
        target = target[:-3]
    return target

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root', type=Path)
    ap.add_argument('--json', action='store_true')
    ns = ap.parse_args()
    ns.root = require_directory(ap, ns.root)
    notes = markdown_files(ns.root)
    by_stem = defaultdict(list); by_portable_stem = defaultdict(list)
    rel_no_ext = {}; by_portable_rel = defaultdict(list)
    for p in notes:
        by_stem[p.stem].append(p)
        by_portable_stem[portable_name_key(p.stem)].append(p)
        rel = p.relative_to(ns.root).with_suffix('').as_posix()
        rel_no_ext[rel] = p
        by_portable_rel[portable_name_key(rel)].append(p)
    missing, ambiguous, non_exact, errors = [], [], [], []
    for p in notes:
        rel_source = relative_posix(p, ns.root)
        try:
            text = read_utf8(p)
        except (OSError, UnicodeError) as exc:
            errors.append({'file': rel_source, 'issue': f'cannot read as UTF-8: {exc}'})
            continue
        for raw in LINK_RE.findall(markdown_visible_text(text)):
            target = normalize_target(raw)
            if not target:
                continue
            if '/' in target:
                exact = [rel_no_ext[target]] if target in rel_no_ext else []
                portable = by_portable_rel.get(portable_name_key(target), [])
            else:
                exact = by_stem.get(target, [])
                portable = by_portable_stem.get(portable_name_key(target), [])
            if len(portable) > 1:
                ambiguous.append({'file': rel_source, 'target': target,
                                  'matches': [relative_posix(x, ns.root) for x in portable]})
            elif exact:
                continue
            elif portable:
                non_exact.append({'file': rel_source, 'target': target,
                                  'actual': relative_posix(portable[0], ns.root)})
            else:
                missing.append({'file': rel_source, 'target': target})
    result = {
        'ok': not missing and not ambiguous and not non_exact and not errors,
        'missing': missing,
        'ambiguous': ambiguous,
        'non_exact': non_exact,
        'errors': errors,
    }
    if ns.json:
        print_json(result)
    else:
        print(f"missing={len(missing)} ambiguous={len(ambiguous)} non_exact={len(non_exact)} errors={len(errors)}")
        for x in missing: print(f"MISSING {x['file']} -> {x['target']}")
        for x in ambiguous: print(f"AMBIGUOUS {x['file']} -> {x['target']}: {x['matches']}")
        for x in non_exact: print(f"NON-EXACT {x['file']} -> {x['target']}: {x['actual']}")
        for x in errors: print(f"ERROR {x['file']}: {x['issue']}")
    return 0 if result['ok'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
