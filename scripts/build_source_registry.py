#!/usr/bin/env python3
"""Create a Markdown Source Registry from a user-provided source directory.

This does not mutate source files. Hashes help detect repeated ingestion; they are not cognitive evidence.
"""
from __future__ import annotations
import argparse,datetime,hashlib,unicodedata
from pathlib import Path

try:
    from ._script_utils import (
        is_within,
        markdown_code_cell,
        relative_posix,
        require_directory,
        write_text_safely,
    )
except ImportError:
    from _script_utils import (  # type: ignore
        is_within,
        markdown_code_cell,
        relative_posix,
        require_directory,
        write_text_safely,
    )

def sha256(path:Path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('source',type=Path); ap.add_argument('output',type=Path); ap.add_argument('--include',nargs='*',default=['.md','.txt','.json','.html']); ap.add_argument('--force',action='store_true',help='explicitly replace an existing registry'); ns=ap.parse_args()
    ns.source=require_directory(ap,ns.source,'source')
    ns.output=ns.output.expanduser()
    if is_within(ns.output,ns.source):
        ap.error('output must be outside the read-only source directory')
    if ns.output.exists() and not ns.force:
        ap.error(f'output already exists: {ns.output} (use --force to replace it)')
    include={(value if value.startswith('.') else f'.{value}').casefold() for value in ns.include}
    rows=[]
    files=sorted((p for p in ns.source.rglob('*') if p.is_file()),key=lambda p:unicodedata.normalize('NFC',relative_posix(p,ns.source)).casefold())
    source_resolved=ns.source.resolve(strict=True)
    for p in files:
        if p.suffix.casefold() not in include:
            continue
        try:
            resolved=p.resolve(strict=True)
            if resolved != source_resolved and not resolved.is_relative_to(source_resolved):
                ap.error(f'source file resolves outside source directory: {p}')
            rows.append((relative_posix(p,ns.source),p.stat().st_size,sha256(p)))
        except OSError as exc:
            ap.error(f'cannot hash source file {p}: {exc}')
    date=datetime.date.today().isoformat()
    lines=['# Source Registry','',f'**Registry refreshed:** {date}','','| Source Path | Bytes | SHA-256 |','|---|---:|---|']
    for rel,size,digest in rows: lines.append(f'| {markdown_code_cell(rel)} | {size} | `{digest}` |')
    lines += ['','> Hashes support duplicate-ingestion detection. They do not establish historical or ownership evidence.','']
    try:
        write_text_safely(ns.output,'\n'.join(lines),overwrite=ns.force)
    except FileExistsError:
        ap.error(f'output already exists: {ns.output} (use --force to replace it)')
    except OSError as exc:
        ap.error(f'cannot write output {ns.output}: {exc}')
    print(f'Wrote {ns.output} with {len(rows)} source file(s).')
    return 0
if __name__=='__main__': raise SystemExit(main())
