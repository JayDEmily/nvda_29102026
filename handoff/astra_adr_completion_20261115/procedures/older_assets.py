import json,tarfile,hashlib,collections
from pathlib import Path
O=Path('handoff/astra_adr_completion_20261115');A=Path('/workspace/recovery-assets/older');x=json.loads((O/'NON_GIT_ASSET_RESULTS.json').read_text());members=[]
for ar in A.glob('*.tar.gz'):
 with tarfile.open(ar) as t:
  for m in t.getmembers():
   if m.isfile():
    data=t.extractfile(m).read();h=hashlib.sha256(data).hexdigest();members.append({'archive':ar.name,'path':m.name,'bytes':len(data),'sha256':h})
    for row in x['rows']:
     if row['status']=='BLOCKED' and row['expected_sha256']==h:
      row.update(status='VERIFIED',actual_sha256=h,available_bytes=len(data),recovered_location=str(ar)+'!'+m.name,missing_prerequisite=None)
x['counts']=dict(collections.Counter(r['status'] for r in x['rows']));(O/'NON_GIT_ASSET_RESULTS.json').write_text(json.dumps(x,indent=2)+'\n');(O/'OLDER_RELEASE_MEMBERS.json').write_text(json.dumps(members,indent=2)+'\n');print(x['counts']);print([r['expected_location'] for r in x['rows'] if r['status']=='BLOCKED'])
