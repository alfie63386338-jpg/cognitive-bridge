#!/usr/bin/env python3
"""Run deterministic Cognitive Bridge QA helpers and write a Markdown report."""
from __future__ import annotations
import argparse,datetime,hashlib,json,os,subprocess,sys
from pathlib import Path

try:
    from ._script_utils import has_physical_absolute_path,markdown_files,require_directory,write_text_safely
except ImportError:
    from _script_utils import has_physical_absolute_path,markdown_files,require_directory,write_text_safely  # type: ignore

SCRIPTS=['validate_yaml.py','check_cb_ids.py','validate_statuses.py','detect_file_conflicts.py','check_wikilinks.py','detect_duplicates.py','detect_orphans.py','check_persistent_metadata.py']

def _redacted_text(value:str):
    digest='sha256:'+hashlib.sha256(value.encode('utf-8')).hexdigest()
    return f'[redacted physical path; {digest}]'

def _sanitize_for_persistence(value):
    if isinstance(value,str):
        return _redacted_text(value) if has_physical_absolute_path(value) else value
    if isinstance(value,list):
        return [_sanitize_for_persistence(item) for item in value]
    if isinstance(value,dict):
        sanitized={}
        for key,item in value.items():
            safe_key=(
                _redacted_text(key)
                if isinstance(key,str) and has_physical_absolute_path(key)
                else key
            )
            sanitized[safe_key]=_sanitize_for_persistence(item)
        return sanitized
    return value

def run(script:Path,root:Path):
    env=os.environ.copy(); env['PYTHONIOENCODING']='utf-8'
    cp=subprocess.run([sys.executable,'-B',str(script),str(root),'--json'],capture_output=True,text=True,encoding='utf-8',errors='replace',env=env)
    parsed=True
    try:
        raw_data=json.loads(cp.stdout)
        if not isinstance(raw_data,dict):
            raise ValueError('helper JSON root must be an object')
        data=_sanitize_for_persistence(raw_data)
    except Exception:
        parsed=False
        data={
            'ok':False,
            'error_kind':'helper_failed_without_json',
            'stdout_sha256':'sha256:'+hashlib.sha256(cp.stdout.encode('utf-8')).hexdigest(),
            'stderr_sha256':'sha256:'+hashlib.sha256(cp.stderr.encode('utf-8')).hexdigest(),
            'returncode':cp.returncode,
        }
    if cp.stderr and 'stderr_sha256' not in data:
        data['stderr_sha256']='sha256:'+hashlib.sha256(cp.stderr.encode('utf-8')).hexdigest()
    helper_reported_ok=bool(data.get('ok',False))
    duplicate_findings=(
        script.name == 'detect_duplicates.py'
        and cp.returncode == 1
        and isinstance(data.get('findings'),list)
        and bool(data['findings'])
        and all(
            isinstance(item,dict) and item.get('kind') != 'encoding_error'
            for item in data['findings']
        )
    )
    execution_ok=parsed and (cp.returncode == 0 or duplicate_findings)
    data['helper_reported_ok']=helper_reported_ok
    data['execution_ok']=execution_ok
    data['ok']=helper_reported_ok and cp.returncode == 0
    data['returncode']=cp.returncode
    return data

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root',type=Path); ap.add_argument('--output',type=Path); ap.add_argument('--force',action='store_true',help='explicitly replace an existing QA report'); ns=ap.parse_args()
    ns.root=require_directory(ap,ns.root)
    if not markdown_files(ns.root):
        ap.error(f'root contains no Markdown files: {ns.root}')
    out=(ns.output.expanduser() if ns.output else ns.root/'00_System'/'QA Report.md')
    if out.exists() and not ns.force:
        ap.error(f'output already exists: {out} (use --force to replace it)')
    here=Path(__file__).resolve().parent; results={s:run(here/s,ns.root) for s in SCRIPTS}
    advisory={'detect_duplicates.py','detect_orphans.py'}
    hard_fail=[
        s for s,r in results.items()
        if not r.get('execution_ok',False)
        or (s not in advisory and not r.get('ok',False))
    ]
    status='PASS' if not hard_fail else 'NEEDS REVIEW'
    lines=['# QA Report','',f'**Date:** {datetime.date.today().isoformat()}',f'**Technical status:** {status}','','## Technical QA','']
    for s,r in results.items():
        lines += [f'### {s}', '```json', json.dumps(r,ensure_ascii=False,indent=2), '```','']
    lines += ['## Cognitive Integrity QA','',
             '- [ ] No fabricated quotes, dates, chronology, causality, or inaccessible history.',
             '- [ ] AI-originated ideas were not silently relabeled as user-originated.',
             '- [ ] Agreement noise was not treated as `integrated` adoption.',
             '- [ ] Retrospective interpretation was not backdated.',
             '- [ ] Inferred relations remain clearly distinct from explicit relations.',
             '- [ ] High-impact latent links include a rationale and counterexample/boundary check.',
             '- [ ] Seeds remain intentionally incomplete.',
             '- [ ] Open Questions were not closed merely because AI produced an answer.',
             '- [ ] No decorative Concepts/MOCs/links were created for graph density.',
             '- [ ] Existing user files and human edits were preserved.',
             '- [ ] Prior AI-generated Vault content was not upgraded into historical user evidence without new Source/human review.',
             '', '## Notes', '', '> Technical PASS does not imply cognitive PASS. Complete the checklist above before delivery.', '']
    try:
        write_text_safely(out,'\n'.join(lines),overwrite=ns.force)
    except FileExistsError:
        ap.error(f'output already exists: {out} (use --force to replace it)')
    except OSError as exc:
        ap.error(f'cannot write output {out}: {exc}')
    print(f'Wrote {out} ({status})')
    return 0 if not hard_fail else 1
if __name__=='__main__': raise SystemExit(main())
