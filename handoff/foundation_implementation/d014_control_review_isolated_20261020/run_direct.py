from pathlib import Path
import hashlib
import json
import os
import subprocess
BASE=Path(__file__).resolve().parent
script=BASE/'direct_independent.py'
metadata={'argv':['/tmp/nvda-g61-runtime-GBILkakx/dev/bin/python',str(script)],'cwd':str(BASE),'script_sha256_before':hashlib.sha256(script.read_bytes()).hexdigest()}
(BASE/'direct-before.json').write_text(json.dumps(metadata,indent=2)+'\n')
env=dict(os.environ,TMPDIR=str(BASE/'tmp'),PYTHONDONTWRITEBYTECODE='1')
with (BASE/'direct-independent.log').open('xb') as output:
 result=subprocess.run(metadata['argv'],cwd=BASE,env=env,stdout=output,stderr=subprocess.STDOUT)
metadata.update(exit=result.returncode,script_sha256_after=hashlib.sha256(script.read_bytes()).hexdigest(),log_sha256=hashlib.sha256((BASE/'direct-independent.log').read_bytes()).hexdigest())
(BASE/'direct-after.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps(metadata,indent=2))
