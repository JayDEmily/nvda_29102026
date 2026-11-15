from pathlib import Path
import json,hashlib,collections,zipfile,base64,csv,io
R=Path('/workspace/nvda');O=R/'handoff/astra_adr_completion_20261115';A=Path('/workspace/recovery-assets');rows=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def add(path,expected,source,bytes_expected=None,data=None):
 rows.append({'expected_location':path,'expected_sha256':expected,'inventory':source,'expected_bytes':bytes_expected,'available_bytes':len(data) if data is not None else None,'actual_sha256':sha(data) if data is not None else None,'status':'VERIFIED' if data is not None and (expected is None or sha(data)==expected) else 'BLOCKED','missing_prerequisite':None if data is not None and (expected is None or sha(data)==expected) else 'Exact original bytes at expected location or independently verified original archive member required'})
# All members of original baseline archival inventory, not just Git bundle.
src='handoff/m02_completion_28_execution/L00/transfer_repair_20261030/ORIGINAL_ARCHIVE_INVENTORY.json';orig=json.loads((R/src).read_text());recovered=json.loads((O/'RECOVERED_ARCHIVE_MEMBERS.json').read_text());membermap={m['path']:m for ar in recovered for m in ar['members']}
for m in orig['members']:
 found=membermap.get(m['path']);rows.append({'expected_location':m['path'],'expected_sha256':m['sha256'],'expected_bytes':m['bytes'],'inventory':src,'available_bytes':found['bytes'] if found else None,'actual_sha256':found['sha256'] if found else None,'status':'VERIFIED' if found and found['sha256']==m['sha256'] and found['bytes']==m['bytes'] else 'BLOCKED','evidence':'RECOVERED_ARCHIVE_MEMBERS.json'})
# Historical final handover and all original loose/committed member obligations.
src='handoff/m02_completion_28_execution/L00/L00_FINAL_INDEPENDENT_RESTORE_RECEIPT.json';hist=json.loads((R/src).read_text())
for m in [hist['archive']]+hist['archive']['members']+[dict(path=k,**v) for k,v in hist['assets'].items()]:
 path=m.get('path',m.get('name'));p=R/path
 if not p.exists():p=A/path
 add(path,m['sha256'],src,m.get('bytes'),p.read_bytes() if p.is_file() else None)
# Exact F02 external input, baseline and SQLite source/library as explicit unresolved inputs.
src='handoff/planning/t01_recovered_successor_20261111/UBUNTU_F02_RESTORATION_RECEIPT.json';f=json.loads((R/src).read_text())
add('Downloads/NVDA_R2_G0_L00_F02_INDEPENDENT_REVIEW_HANDOFF_20261031(1)(1).zip',f['input_zip_sha256'],src)
src='handoff/m02_completion_28_execution/L00/R2_SQLITE_3541_RUNTIME_VERIFIED.json';runtime=json.loads((R/src).read_text())
for path,key,b in [(runtime['source_archive_basename'],'source_archive_sha256','source_archive_bytes'),(runtime['compiled_library_path'],'compiled_library_sha256','compiled_library_size_bytes')]:add(path,runtime[key],src,runtime[b])
# Current release and wheel payload identities, ZIP CRC and populated RECORD digests.
for p in sorted(A.iterdir()):
 if p.is_file():add(str(p),None,'GitHub release nvda-l00-transfer-successor-40960483921',data=p.read_bytes())
wheels=[]
for p in sorted((R/'vendor/wheels').glob('*.whl')):
 data=p.read_bytes();add(str(p.relative_to(R)),None,'accepted main vendor/wheels; exact Git bytes',data=data)
 with zipfile.ZipFile(p) as z:
  bad=z.testzip();record=next(n for n in z.namelist() if n.endswith('.dist-info/RECORD'));count=0;errs=[]
  for n,h,size in csv.reader(io.StringIO(z.read(record).decode())):
   if h:
    alg,val=h.split('=',1);actual=base64.urlsafe_b64encode(hashlib.new(alg,z.read(n)).digest()).decode().rstrip('=');count+=1
    if actual!=val:errs.append(n)
  wheels.append({'path':str(p.relative_to(R)),'sha256':sha(data),'bytes':len(data),'crc_error':bad,'record_entries_verified':count,'record_errors':errs})
(O/'NON_GIT_ASSET_RESULTS.json').write_text(json.dumps({'scope':'All original baseline members, final historical L00 handover/assets, F02 and SQLite prerequisites, current release payloads and vendored wheels. External historical binary gaps remain explicit; current release substitutes are not asserted identical.','rows':rows,'counts':dict(collections.Counter(x['status'] for x in rows))},indent=2)+'\n')
(O/'WHEEL_VERIFICATION.json').write_text(json.dumps(wheels,indent=2)+'\n');print(len(rows),collections.Counter(x['status'] for x in rows))
