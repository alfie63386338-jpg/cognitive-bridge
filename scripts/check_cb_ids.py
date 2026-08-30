#!/usr/bin/env python3
"""Check presence/format/uniqueness of cb_id on generated cognitive notes."""
from __future__ import annotations
import argparse, json, re
from collections import defaultdict
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

VALID_RE = re.compile(r'^cb-[a-z][a-z0-9-]*-[a-z0-9]{6,}$')
EXPECTED_TYPES = {'idea','concept','question','seed','discussion','moc','source-trace'}
COGNITIVE_FOLDERS = {
    '01_MOC', '02_Discussions', '03_Ideas', '04_Concepts',
    '05_Questions', '06_Seeds', '07_Sources',
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root', type=Path)
    ap.add_argument('--json', action='store_true')
    ns = ap.parse_args()
    ns.root = require_directory(ap, ns.root)
    ids = defaultdict(list); issues=[]
    for p in markdown_files(ns.root):
        rel = relative_posix(p, ns.root)
        try:
            text = read_utf8(p)
        except (OSError, UnicodeError) as exc:
            issues.append({'file': rel, 'issue': f'cannot read as UTF-8: {exc}'})
            continue
        frontmatter, _ = split_frontmatter(text)
        note_type = frontmatter_scalar(frontmatter, 'type')
        cid = frontmatter_scalar(frontmatter, 'cb_id')
        in_cognitive_folder = any(part in COGNITIVE_FOLDERS for part in p.relative_to(ns.root).parts[:-1])
        if note_type not in EXPECTED_TYPES and cid is None and not in_cognitive_folder:
            continue
        if cid is None:
            issues.append({'file': rel, 'issue':'missing cb_id'}); continue
        ids[cid].append(rel)
        if not VALID_RE.fullmatch(cid):
            issues.append({'file': rel, 'issue':f'invalid cb_id format: {cid}'})
    for cid, paths in ids.items():
        if len(paths)>1:
            issues.append({'file': ', '.join(paths), 'issue':f'duplicate cb_id: {cid}'})
    result={'ok':not issues,'issues':issues}
    if ns.json:
        print_json(result)
    else:
        print('cb_id OK' if result['ok'] else '\n'.join(f"- {i['file']}: {i['issue']}" for i in issues))
    return 0 if result['ok'] else 1
if __name__=='__main__': raise SystemExit(main())
