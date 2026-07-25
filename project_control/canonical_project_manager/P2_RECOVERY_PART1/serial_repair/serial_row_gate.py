#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, csv, hashlib, subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
P1=ROOT/'project_control/canonical_project_manager/P2_RECOVERY_PART1'
LEDGER=ROOT/'project_control/canonical_project_manager/P2_ABSOLUTE_SEMANTIC_READ_LEDGER.tsv'
LOG=P1/'serial_repair/SERIAL_EXECUTION_LOG.tsv'
MAN=P1/'serial_repair/FULL_READ_MANIFEST.tsv'

def sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()
def row(seq:str):
    rs=list(csv.DictReader(LEDGER.open(),delimiter='\t'))
    return next(r for r in rs if r['SEQUENCE']==seq)
def imports(test:Path):
    tree=ast.parse(test.read_text(encoding='utf-8'))
    out=[]
    for n in ast.walk(tree):
        mods=[]
        if isinstance(n,ast.ImportFrom) and n.module: mods=[n.module]
        elif isinstance(n,ast.Import): mods=[a.name for a in n.names]
        for m in mods:
            if m.startswith('nvda_desk'):
                base=ROOT/'src'/Path(*m.split('.'))
                for c in (base.with_suffix('.py'),base/'__init__.py'):
                    if c.is_file(): out.append(c); break
    return sorted(set(out))
def append(path:Path,line:str,header:str):
    if not path.exists(): path.write_text(header+'\n',encoding='utf-8')
    with path.open('a',encoding='utf-8') as f:f.write(line+'\n')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['start','complete']);ap.add_argument('sequence');a=ap.parse_args()
    seq=a.sequence.zfill(3); r=row(seq); test=ROOT/r['TEST_PATH']; rec=ROOT/r['RECEIPT_PATH']; now=datetime.now(timezone.utc).isoformat()
    if a.mode=='start':
        if r['SEMANTICALLY_READ']!='NO': raise SystemExit('row must be NO at start')
        test_text=test.read_text(encoding='utf-8'); rec_text=rec.read_text(encoding='utf-8')
        # The gate records deterministic evidence only. Human semantic reading is not certified here.
        paths=[test,*imports(test)]
        for p in paths:
            append(MAN,f'{seq}\t{p.relative_to(ROOT)}\t{sha(p)}\tYES\tcurrent serial cycle full-read claim; requires human accountability',
                   'SEQUENCE\tPATH\tSHA256\tREAD_STATUS\tNOTE')
        out=P1/f'serial_repair/rows/{seq}';out.mkdir(parents=True,exist_ok=True)
        (out/'LEDGER_BEFORE.tsv').write_bytes(LEDGER.read_bytes())
        (out/'TEST_FULL_TEXT.txt').write_text(test_text,encoding='utf-8')
        (out/'RECEIPT_FULL_TEXT.txt').write_text(rec_text,encoding='utf-8')
        tr=subprocess.run(['pytest','-q',r['TEST_PATH']],cwd=ROOT,text=True,capture_output=True)
        (out/'TARGETED_TEST_RAW.txt').write_text(tr.stdout+tr.stderr+f'\nEXIT_CODE={tr.returncode}\n',encoding='utf-8')
        vr=subprocess.run(['python',str(P1/'P2_RECOVERY_PART1_VALIDATE_ROW.py'),'--repo-root',str(ROOT),'--sequence',seq,'--allow-ledger-no'],cwd=ROOT,text=True,capture_output=True)
        (out/'PRE_ADMISSION_VALIDATOR_RAW.txt').write_text(vr.stdout+vr.stderr+f'\nEXIT_CODE={vr.returncode}\n',encoding='utf-8')
        if tr.returncode or vr.returncode: raise SystemExit(f'gate failed test={tr.returncode} validator={vr.returncode}')
        append(LOG,f'{seq}\tIN_PROGRESS\t{now}\t{r["TEST_PATH"]}\tpre-admission test and structural validator pass; semantic decision remains human',
               'SEQUENCE\tSTATE\tTIMESTAMP_UTC\tTEST_PATH\tNOTE')
    else:
        if r['SEMANTICALLY_READ']!='YES': raise SystemExit('row must be YES at complete')
        vr=subprocess.run(['python',str(P1/'P2_RECOVERY_PART1_VALIDATE_ROW.py'),'--repo-root',str(ROOT),'--sequence',seq],cwd=ROOT,text=True,capture_output=True)
        out=P1/f'serial_repair/rows/{seq}';out.mkdir(parents=True,exist_ok=True)
        (out/'POST_ADMISSION_VALIDATOR_RAW.txt').write_text(vr.stdout+vr.stderr+f'\nEXIT_CODE={vr.returncode}\n',encoding='utf-8')
        if vr.returncode: raise SystemExit('post validator failed')
        (out/'LEDGER_AFTER.tsv').write_bytes(LEDGER.read_bytes())
        before=list(csv.DictReader((out/'LEDGER_BEFORE.tsv').open(),delimiter='\t'))
        after=list(csv.DictReader((out/'LEDGER_AFTER.tsv').open(),delimiter='\t'))
        diffs=[]
        for b,c in zip(before,after):
            if b!=c: diffs.append((b['SEQUENCE'],{k:(b[k],c[k]) for k in b if b[k]!=c[k]}))
        expected=[(seq,{'SEMANTICALLY_READ':('NO','YES')})]
        comparison='RESULT=PASS\n' if diffs==expected else 'RESULT=FAIL\n'+repr(diffs)+'\n'
        (out/'NO_OTHER_ROW_CHANGE.txt').write_text(comparison,encoding='utf-8')
        if diffs!=expected: raise SystemExit('more than one ledger field changed')
        append(LOG,f'{seq}\tCOMPLETE\t{now}\t{r["TEST_PATH"]}\tsingle row admitted after current receipt confirmation and validation',
               'SEQUENCE\tSTATE\tTIMESTAMP_UTC\tTEST_PATH\tNOTE')
if __name__=='__main__':main()
