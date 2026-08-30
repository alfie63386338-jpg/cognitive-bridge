#!/usr/bin/env python3
"""Find duplicate IDs, duplicate filenames and high-text-similarity candidates.

This script reports candidates only. Semantic merge decisions belong to the AI/human review layer.
"""
from __future__ import annotations
import argparse, difflib, json, re
from collections import defaultdict
from pathlib import Path

try:
    from ._script_utils import (
        frontmatter_scalar,
        markdown_files,
        portable_name_key,
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
        portable_name_key,
        print_json,
        read_utf8,
        relative_posix,
        require_directory,
        split_frontmatter,
    )

def body(text:str):
    frontmatter, remainder=split_frontmatter(text)
    if frontmatter not in (None,'UNTERMINATED') and remainder is not None:
        text=remainder
    return re.sub(r'\s+',' ',text).strip().lower()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root',type=Path); ap.add_argument('--threshold',type=float,default=.94); ap.add_argument('--json',action='store_true'); ns=ap.parse_args()
    ns.root = require_directory(ap, ns.root)
    if not 0 <= ns.threshold <= 1:
        ap.error('--threshold must be between 0 and 1')
    notes=markdown_files(ns.root); ids=defaultdict(list); stems=defaultdict(list); labels={}; docs=[]; findings=[]
    for p in notes:
        rel=relative_posix(p,ns.root); key=portable_name_key(p.stem)
        labels.setdefault(key,p.stem); stems[key].append(rel)
        try:
            txt=read_utf8(p)
        except (OSError,UnicodeError) as exc:
            findings.append({'kind':'encoding_error','files':[rel],'issue':f'cannot read as UTF-8: {exc}'})
            continue
        frontmatter,_=split_frontmatter(txt)
        cid=frontmatter_scalar(frontmatter,'cb_id')
        if cid: ids[cid].append(rel)
        b=body(txt)
        if len(b)>=80: docs.append((rel,b))
    for k,v in ids.items():
        if len(v)>1: findings.append({'kind':'duplicate_cb_id','value':k,'files':v})
    for k,v in stems.items():
        if len(v)>1: findings.append({'kind':'duplicate_filename_stem','value':labels[k],'portable_key':k,'files':v})
    for i,(a,ta) in enumerate(docs):
        for b,tb in docs[i+1:]:
            ratio=difflib.SequenceMatcher(None,ta,tb).ratio()
            if ratio>=ns.threshold:
                findings.append({'kind':'high_text_similarity','similarity':round(ratio,3),'files':[a,b]})
    result={'ok':not findings,'findings':findings,'note':'Similarity findings are review candidates, not automatic merge instructions.'}
    if ns.json:
        print_json(result)
    else:
        print(f"Found {len(findings)} duplicate candidate(s)" if findings else 'No duplicate candidates')
    return 0 if result['ok'] else 1
if __name__=='__main__': raise SystemExit(main())
