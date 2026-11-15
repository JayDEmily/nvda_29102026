from pathlib import Path
import json,hashlib,collections
O=Path('handoff/astra_adr_completion_20261115');f=O/'NON_GIT_ASSET_RESULTS.json';x=json.loads(f.read_text());src='handoff/downstream_reconciliation/L14/SOURCE_AND_ASSET_INVENTORY.json';j=json.loads(Path(src).read_text())
for r in j['external_required_assets']:
 h=r['sha256'];p=next((p for p in Path('/workspace/recovery-assets').iterdir() if p.is_file() and h and hashlib.sha256(p.read_bytes()).hexdigest()==h),None)
 x['rows'].append({'inventory':src,'expected_location':r['name'],'expected_sha256':h,'expected_bytes':r.get('size_bytes'),'available_bytes':p.stat().st_size if p else None,'actual_sha256':h if p else None,'recovered_location':str(p) if p else None,'status':'VERIFIED' if p else 'UNKNOWN','missing_prerequisite':None if p else 'Historical CPython 3.12.14 / SQLite toolchain exact binary identity not established by available manifest; qualification is profile-specific','requirement':r['requirement']})
x['unrelated_external_archives']=j['unrelated_external_archives'];x['counts']=dict(collections.Counter(r['status'] for r in x['rows']));f.write_text(json.dumps(x,indent=2)+'\n');print(x['counts'])
