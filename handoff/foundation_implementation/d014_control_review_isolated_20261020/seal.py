from pathlib import Path
import hashlib
import json
import subprocess
BASE=Path(__file__).resolve().parent
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
for name in ('invocation_after.json','direct-after.json'):
 record=json.loads((BASE/name).read_text())
 assert record['exit']==0 and record['script_sha256_before']==record['script_sha256_after']
for record in json.loads((BASE/'checks-results.json').read_text()).values():
 assert record['exit']==0
assert '130 passed in 199.94s' in (BASE/'full-control.log').read_text()
assert 'ALL 23 PRISTINE INDEPENDENT ACTUAL-STATE CASES PASS' in (BASE/'direct-independent.log').read_text()
assert (BASE/'audit.log').read_bytes()==(BASE/'audit-final.log').read_bytes()
manifest={path.name:{'bytes':path.stat().st_size,'sha256':sha(path)} for path in sorted(BASE.iterdir()) if path.is_file() and path.name!='EVIDENCE_SHA256.json'}
(BASE/'EVIDENCE_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'files':len(manifest),'review_sha256':sha(BASE/'REVIEW.md'),'manifest_sha256':sha(BASE/'EVIDENCE_SHA256.json')},indent=2))
