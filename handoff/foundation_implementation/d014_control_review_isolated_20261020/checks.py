from pathlib import Path
import hashlib
import json
import os
import subprocess

BASE = Path(__file__).resolve().parent
PY = '/tmp/nvda-g61-runtime-GBILkakx/dev/bin/python'
commands = {
 'full-control': ['module','pytest','tests/architecture/test_proof_control.py','--basetemp',str(BASE/'pytest-temp')],
 'mypy': ['module','mypy','src','tools/product_proof_claims.py','tools/product_proof_outcomes.py','tools/validate_product_proof.py','tools/run_product_proof_gate.py'],
 'ruff': ['module','ruff','check','tools/product_proof_claims.py','tests/architecture/test_proof_control.py'],
 'binding': ['path','tools/validate_implementation_authority.py','--binding','implementation/authority/G6_1_D014_IMPLEMENTATION_AUTHORITY_BINDING.yaml','--brief','handoff/foundation_implementation/authority/G6_1_D014_IMPLEMENTATION_BRIEF_PROPOSED.md'],
}
env = dict(os.environ, TMPDIR=str(BASE/'tmp'), PYTHONPATH=os.pathsep.join([str(BASE/'candidate/tools'),str(BASE/'candidate/src')]), PYTHONDONTWRITEBYTECODE='1')
(BASE/'tmp').mkdir(exist_ok=True)
results = {}
for name, arguments in commands.items():
    argv = [PY,str(BASE/'invoke.py'),*arguments]
    metadata = {'argv':argv,'cwd':str(BASE/'candidate'),'invoke_sha256':hashlib.sha256((BASE/'invoke.py').read_bytes()).hexdigest()}
    (BASE/(name+'-before.json')).write_text(json.dumps(metadata,indent=2)+'\n')
    with (BASE/(name+'.log')).open('xb') as output:
        result = subprocess.run(argv,cwd=BASE/'candidate',env=env,stdout=output,stderr=subprocess.STDOUT)
    metadata.update(exit=result.returncode,log_sha256=hashlib.sha256((BASE/(name+'.log')).read_bytes()).hexdigest())
    results[name] = metadata
    (BASE/'checks-results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(name,json.dumps(metadata),flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
