from pathlib import Path
import hashlib
import subprocess
import json

base=Path(__file__).resolve().parent
script=base/'exact_sequence.py'
argv=['/tmp/nvda-g61-runtime-GBILkakx/dev/bin/python',str(script)]
metadata={'argv':argv,'cwd':str(base),'merged_stdout_stderr':str(base/'exact_sequence.log'),
          'script_sha256_before':hashlib.sha256(script.read_bytes()).hexdigest(),
          'expected_source_head':'f01ad17c48f0eb21148cb7b2aa4e2b2f428c0f2b',
          'expected_proposed_module_sha256':'b2670e26f51d4b6f4fc8c656c859b9e5d63ca9aadd84ff2f818ff06cd9bb118a',
          'exit':None,'status':'NOT_YET_EXECUTED'}
(base/'invocation_before.json').write_text(json.dumps(metadata,indent=2)+'\n')
with (base/'exact_sequence.log').open('xb') as output:
    completed=subprocess.run(argv,cwd=base,stdout=output,stderr=subprocess.STDOUT)
metadata.update(exit=completed.returncode,status='EXECUTED',
                script_sha256_after=hashlib.sha256(script.read_bytes()).hexdigest(),
                log_sha256=hashlib.sha256((base/'exact_sequence.log').read_bytes()).hexdigest())
(base/'invocation_after.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps(metadata,indent=2))
