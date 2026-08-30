#!/usr/bin/env python3
"""Detect filename-stem collisions that can make Obsidian WikiLinks ambiguous."""
from __future__ import annotations
import argparse,json
from collections import defaultdict
from pathlib import Path

try:
    from ._script_utils import (
        markdown_files,
        portable_name_key,
        print_json,
        relative_posix,
        require_directory,
    )
except ImportError:
    from _script_utils import (  # type: ignore
        markdown_files,
        portable_name_key,
        print_json,
        relative_posix,
        require_directory,
    )

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root',type=Path); ap.add_argument('--json',action='store_true'); ns=ap.parse_args()
    ns.root = require_directory(ap, ns.root)
    stems=defaultdict(list)
    labels={}
    for p in markdown_files(ns.root):
        key=portable_name_key(p.stem)
        labels.setdefault(key,p.stem)
        stems[key].append(relative_posix(p,ns.root))
    conflicts=[{'stem':labels[k],'portable_key':k,'files':v} for k,v in sorted(stems.items()) if len(v)>1]
    result={'ok':not conflicts,'conflicts':conflicts}
    if ns.json:
        print_json(result)
    else:
        print(f"Filename conflicts: {len(conflicts)}"+'\n'+ '\n'.join(f"- {x['stem']}: {x['files']}" for x in conflicts))
    return 0 if not conflicts else 1
if __name__=='__main__': raise SystemExit(main())
