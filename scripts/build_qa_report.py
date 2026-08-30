#!/usr/bin/env python3
"""Run deterministic Cognitive Bridge QA helpers and write a Markdown report."""
from __future__ import annotations
import argparse,datetime,json,os,subprocess,sys
from pathlib import Path

try:
    from ._script_utils import markdown_files,require_directory,write_text_safely
except ImportError:
    from _script_utils import markdown_files,require_directory,write_text_safely  # type: ignore

SCRIPTS=['validate_yaml.py','check_cb_ids.py','validate_statuses.py','detect_file_conflicts.py','check_wikilinks.py','detect_duplicates.py','detect_orphans.py']

def run(script:Path,root:Path):
    env=os.environ.copy(); env['PYTHONIOENCODING']='utf-8'
    cp=subprocess.run([sys.executable,'-B',str(script),str(root),'--json'],capture_output=True,text=True,encoding='utf-8',errors='replace',env=env)
    try: data=json.loads(cp.stdout)
    except Exception: data={'ok':False,'raw_stdout':cp.stdout,'stderr':cp.stderr,'returncode':cp.returncode}
    if cp.stderr and 'stderr' not in data: data['stderr']=cp.stderr
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
    hard_fail=[s for s,r in results.items() if s not in {'detect_duplicates.py','detect_orphans.py'} and not r.get('ok',False)]
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
