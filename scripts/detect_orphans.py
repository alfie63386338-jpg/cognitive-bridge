#!/usr/bin/env python3
"""Report likely cognitive notes with no incoming WikiLinks.

Orphans are review candidates. Never create decorative links just to remove them.
"""
from __future__ import annotations
import argparse,json,re
from collections import defaultdict
from pathlib import Path

try:
    from ._script_utils import (
        frontmatter_scalar,
        markdown_files,
        markdown_visible_text,
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
        markdown_visible_text,
        print_json,
        read_utf8,
        relative_posix,
        require_directory,
        split_frontmatter,
    )

LINK_RE=re.compile(r'\[\[([^\]]+)\]\]')
CHECK={'idea','concept','question','seed','discussion'}


def normalize_target(raw:str):
    target=raw.split('|',1)[0].split('#',1)[0].strip()
    if target.lower().endswith('.md'):
        target=target[:-3]
    return target


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root',type=Path); ap.add_argument('--json',action='store_true'); ns=ap.parse_args()
    ns.root = require_directory(ap, ns.root)
    notes=markdown_files(ns.root); incoming=defaultdict(int); candidates=[]; errors=[]
    stems=defaultdict(list); rel_no_ext={}
    for p in notes:
        stems[p.stem].append(p)
        rel_no_ext[p.relative_to(ns.root).with_suffix('').as_posix()]=p
    for p in notes:
        rel=relative_posix(p,ns.root)
        try:
            txt=read_utf8(p)
        except (OSError,UnicodeError) as exc:
            errors.append({'file':rel,'issue':f'cannot read as UTF-8: {exc}'})
            continue
        frontmatter,_=split_frontmatter(txt)
        typ=frontmatter_scalar(frontmatter,'type')
        if typ in CHECK: candidates.append(p)
        for raw in LINK_RE.findall(markdown_visible_text(txt)):
            target=normalize_target(raw)
            if not target:
                continue
            if '/' in target:
                matches=[rel_no_ext[target]] if target in rel_no_ext else []
            else:
                matches=stems.get(target,[])
            if len(matches)==1 and matches[0] != p:
                incoming[matches[0]]+=1
    orphans=[relative_posix(p,ns.root) for p in candidates if incoming[p]==0]
    result={'ok':not errors,'orphans':orphans,'errors':errors,'note':'Orphans are informational only; do not auto-link for graph aesthetics.'}
    if ns.json:
        print_json(result)
    else:
        print(f"Orphan candidates: {len(orphans)}\n"+'\n'.join('- '+x for x in orphans))
        for error in errors: print(f"ERROR {error['file']}: {error['issue']}")
    return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
