from pathlib import Path
import subprocess,json,hashlib,tarfile
A=Path('/workspace/recovery-assets');O=Path('/workspace/nvda/handoff/astra_adr_completion_20261115');log=[]
def run(args,cwd):
 p=subprocess.run(args,cwd=cwd,text=True,capture_output=True);log.append({'command':args,'cwd':str(cwd),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p
checks=[]
for l in (A/'SHA256SUMS.txt').read_text().splitlines():
 sha,name=l.split(maxsplit=1);p=A/name;checks.append({'path':str(p),'expected_sha256':sha,'actual_sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None,'bytes':p.stat().st_size if p.exists() else None})
b='NVDA_DOWNSTREAM_RECONCILIATION_L00_CHECKPOINT_20261028_FULL_HISTORY.bundle';a='NVDA_M02_COMPLETION28_L00_ADDITIVE_FROM_97f944d51ab9.bundle'
d=Path('/workspace/original-successor-restore.git');run(['git','init','--bare',str(d)],A)
for name in [b,a]:
 run(['git','bundle','verify',str(A/name)],d);run(['git','fetch',str(A/name),'refs/*:refs/*'],d)
run(['git','symbolic-ref','HEAD','refs/heads/execution/accepted-r1-20261030'],d)
run(['git','fsck','--full','--no-reflogs'],d)
head=run(['git','rev-parse','HEAD'],d).stdout.strip();tree=run(['git','rev-parse','HEAD^{tree}'],d).stdout.strip();listing=run(['git','ls-tree','-r','--full-tree','HEAD'],d).stdout
x=json.loads((A/'CURRENT_REF_MANIFEST.json').read_text());refs=x['exported_refs'];bad=[]
for ref,tip in refs.items():
 p=run(['git','rev-parse',ref],d)
 if p.stdout.strip()!=tip:bad.append({'ref':ref,'expected':tip,'actual':p.stdout.strip()})
# Verify every member as bytes without extracting instructions or unsafe paths.
archives=[]
for f in A.glob('*.tar.gz'):
 with tarfile.open(f) as t:
  members=[{'path':m.name,'bytes':m.size,'sha256':hashlib.sha256(t.extractfile(m).read()).hexdigest()} for m in t.getmembers() if m.isfile()]
 archives.append({'archive':f.name,'members':members})
(O/'ORIGINAL_BUNDLE_RESTORE.json').write_text(json.dumps({'release':'nvda-l00-transfer-successor-40960483921','checksums':checks,'head':head,'tree':tree,'manifest_ref_count':len(refs),'ref_mismatches':bad,'tracked_inventory_equal':listing==(A/'L00_TRACKED_BLOBS.txt').read_text(),'commands':log,'scope':'Worker fresh restore of actual original base + published successor additive; distinct Tester acceptance pending'},indent=2)+'\n')
(O/'RECOVERED_ARCHIVE_MEMBERS.json').write_text(json.dumps(archives,indent=2)+'\n')
print(head,tree,len(refs),len(bad))
