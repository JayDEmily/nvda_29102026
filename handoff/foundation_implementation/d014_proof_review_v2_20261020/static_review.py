"""Independent source-only review: never imports/executes authored modules."""
import ast
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys

ROOT = Path('/workspace/scratch/d549b6d808a9/resume-20261020-ejayrse7/repository')
BASE = ROOT / 'tests/product/market_measurement_d014'
expected_hashes = {
    'test_raw_ratio.py': '588abd5c69bda15ea1305a12a3bbc35e7fe3f0ed3f57515e7cdd7926524d8db2',
    '_support.py': '49c6149d1ff64e002154b275bc9c54793cf60623bb0c9878c0fd5539fbc058e6',
    'typing/valid_seam.py': '3d1e2ac2449fc13be7db8f0e26c2b505dee5e6810d591dd190d4044bf859dacc',
    'typing/invalid_seam.py': '84b2806f0c8be162321c35f792f987550a3cf2ff428d37edd007042fcc699fc9',
}
def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode().strip()
assert git('rev-parse', 'HEAD') == 'ec0f36303a35567c92b56b9b017cf4ec684eca65'
assert git('rev-parse', 'HEAD^{tree}') == '9fad3e68bba93ab09ea26403ab638ae50d5d8f07'
assert git('status', '--porcelain') == ''
for name, digest in expected_hashes.items():
    data = (BASE / name).read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest
    compile(data, str(BASE / name), 'exec')  # Compilation only; deliberately no exec.
    print('COMPILE_ONLY', name, digest)
for name, digest in {
    'G6_1_D014_IMPLEMENTATION_BRIEF_PROPOSED.md': 'c23ea315c94b478c568f105e94891a03af62393792a1478c33027a0371738bb8',
    'G6_1_D014_PROOF_CONTRACT_PROPOSED.json': '54850f780c4442924e2d28ed319ae5f0fb109e291b367391ac0a4c86190294fc',
}.items():
    assert hashlib.sha256((ROOT / 'handoff/foundation_implementation/authority' / name).read_bytes()).hexdigest() == digest
contract = json.loads((ROOT / 'handoff/foundation_implementation/authority/G6_1_D014_PROOF_CONTRACT_PROPOSED.json').read_text())
tree = ast.parse((BASE / 'test_raw_ratio.py').read_text())
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
assert [n.name for n in functions if n.name.startswith('test_')] == contract['families'][0]['required_test_names']
literals = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ('REFUSALS', 'POSITIVES', 'DUPLICATE_CASES', 'STORAGE_CASES')}
assert tuple(map(len, (literals['REFUSALS'], literals['POSITIVES'], literals['DUPLICATE_CASES'], literals['STORAGE_CASES']))) == (50,7,16,28)
assert set(literals['DUPLICATE_CASES'].values()) == {(d,r,p) for d in ('provider','representation','stale','receipt') for r in (False,True) for p in (False,True)}
tests = {n.name:n for n in functions if n.name.startswith('test_')}
arith = tests['test_d014_exact_ratio_arithmetic_domain']
assert len(arith.decorator_list[0].args[1].elts) == 14
identity = tests['test_d014_identity_versions_and_later_retry']
assert len(ast.literal_eval(identity.decorator_list[0].args[1])) == 11
count = 2 + 2*(50+7+16) + 14 + 11 + 28 + 1
assert count == 202
print('SIX_MANDATORY_NAMES_MATCH; SOURCE_PROJECTED_CASES', count, '(not collection)')
misuses = [(i,re.search(r'MISUSE\[([^]]+)\]',line)[1]) for i,line in enumerate((BASE/'typing/invalid_seam.py').read_text().splitlines(),1) if 'MISUSE[' in line]
assert misuses == [(18,'assignment'),(19,'assignment'),(20,'assignment'),(21,'assignment'),(22,'assignment'),(23,'attr-defined'),(24,'arg-type'),(25,'arg-type'),(26,'assignment'),(27,'assignment')]
print('NEGATIVE_SOURCE_EXPECTATIONS', misuses, '(not mypy execution)')
support = ast.parse((BASE/'_support.py').read_text())
assert not any(isinstance(n,ast.Attribute) and n.attr == 'materialise' for n in ast.walk(support))
assert json.loads((ROOT/'config/product_proof/market_measurement_d014/admission.json').read_text())['current_generation'] is None
assert not (ROOT/'config/product_proof/market_measurement_d014/generations').exists()
assert not (ROOT/'src/nvda_desk/market_measurement_truth/_raw_rational.py').exists()
assert not (ROOT/'src/nvda_desk/market_measurement_truth/_raw_rational_sqlite.py').exists()
print('NULL_ADMISSION; NO_GENERATION_OR_NEW_RUNTIME')
print('INTERPRETER', sys.version, 'SQLITE', sqlite3.sqlite_version)
