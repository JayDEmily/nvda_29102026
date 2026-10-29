from pathlib import Path
import subprocess
import json
import concurrent.futures

base = Path(__file__).resolve().parent
root = base / 'proposed'
py = '/workspace/scratch/d549b6d808a9/g52-dev/bin/python'
commands = {
 'targeted': [py, '-m', 'pytest', 'tests/architecture/test_proof_control.py', '-k', 'd014'],
 'full-control': [py, '-m', 'pytest', 'tests/architecture/test_proof_control.py'],
 'mypy': [py, '-m', 'mypy', 'src', 'tools/product_proof_claims.py', 'tools/product_proof_outcomes.py', 'tools/validate_product_proof.py', 'tools/run_product_proof_gate.py'],
 'ruff': [py, '-m', 'ruff', 'check', 'tools/product_proof_claims.py', 'tests/architecture/test_proof_control.py'],
 'binding': [py, 'tools/validate_implementation_authority.py', '--binding', 'implementation/authority/G6_1_D014_IMPLEMENTATION_AUTHORITY_BINDING.yaml', '--brief', 'handoff/foundation_implementation/authority/G6_1_D014_IMPLEMENTATION_BRIEF_PROPOSED.md'],
}
def run(item):
 name, argv = item
 with (base / (name + '.log')).open('wb') as out:
  result = subprocess.run(argv, cwd=root, stdout=out, stderr=subprocess.STDOUT)
 return name, {'argv': argv, 'cwd': str(root), 'exit': result.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
 results = dict(executor.map(run, commands.items()))
(base / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
