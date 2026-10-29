"""Independent source/documentary checks; never imports or executes authored proof."""
import ast
import hashlib
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path('/workspace/scratch/d549b6d808a9/resume-20261020-ejayrse7/repository')
PROOF = ROOT / 'tests/product/market_measurement_d014'
EXPECTED_HEAD = 'e13ccd9d6570753027ea39832aa5f269d2aacb76'
assert sys.version_info[:3] == (3, 12, 14)
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == EXPECTED_HEAD
assert subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True) == ''
paths = ['test_raw_ratio.py', '_support.py', 'typing/valid_seam.py', 'typing/invalid_seam.py']
digests = {}
trees = {}
for relative in paths:
    content = (PROOF / relative).read_bytes()
    trees[relative] = ast.parse(content, filename=relative)
    compile(content, relative, 'exec')  # Compile only, never eval/exec/import.
    digests[relative] = hashlib.sha256(content).hexdigest()
contract_path = ROOT / 'handoff/foundation_implementation/authority/G6_1_D014_PROOF_CONTRACT_PROPOSED.json'
contract = json.loads(contract_path.read_text())
required = contract['families'][0]['required_test_names']
functions = [node.name for node in trees['test_raw_ratio.py'].body if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')]
assert functions == required
constants = {node.targets[0].id: ast.literal_eval(node.value) for node in trees['test_raw_ratio.py'].body if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ('REFUSALS', 'POSITIVES', 'STORAGE_CASES')}
assert tuple(map(len, constants.values())) == (50, 6, 23)
negative = [(number, re.search(r'MISUSE\[([^]]+)\]', line)[1]) for number, line in enumerate((PROOF / paths[3]).read_text().splitlines(), 1) if 'MISUSE[' in line]
assert len(negative) == 10
assert all(not (isinstance(node, ast.Name) and node.id in ('Any', 'cast')) for tree in trees.values() for node in ast.walk(tree))
support_calls = {node.func.attr for node in ast.walk(trees['_support.py']) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
assert 'materialise' not in support_calls
source = (PROOF / paths[0]).read_text()
assert 'foreign_key_list' not in source
assert 'row[5]' not in source  # PRAGMA table_info PK ordinal not inspected.
assert 'CHECK(kind' not in source
assert 'first, replace(first, source_provider="OTHER")' in source

# Independent SQLite documentary counterexample: the profile's actual
# name/type/not-null/STRICT/FK-check projections cannot observe missing CHECK,
# PK or FK declarations. This is not an owner/store/domain execution.
columns = [('owner_namespace', 'TEXT'), ('kind', 'TEXT'), ('context_id', 'TEXT'), ('version', 'TEXT'), ('payload', 'BLOB'), ('content_sha256', 'TEXT')]
base = ','.join(name + ' ' + kind + ' NOT NULL' for name, kind in columns)
def observe(constraints):
    db = sqlite3.connect(':memory:')
    db.execute('CREATE TABLE cfg (' + base + constraints + ') STRICT')
    info = db.execute('PRAGMA table_info(cfg)').fetchall()
    projection = ([row[1] for row in info], [row[2] for row in info], [row[3] for row in info], db.execute('SELECT strict FROM pragma_table_list WHERE name=\'cfg\'').fetchone()[0], db.execute('PRAGMA foreign_key_check').fetchall())
    declaration = db.execute("SELECT sql FROM sqlite_schema WHERE name='cfg'").fetchone()[0]
    db.close()
    return projection, declaration
good = observe(",PRIMARY KEY(owner_namespace,kind,context_id,version),CHECK(kind IN ('parameter','selection','unit','raw_mapping'))")
bad = observe('')
assert good[0] == bad[0] and good[1] != bad[1]

print(json.dumps(dict(
    head=EXPECTED_HEAD,
    interpreter=sys.version,
    compile_only='4 PASS; zero authored-module imports/execution',
    proof_sha256=digests,
    six_functions=functions,
    source_counts={key: len(value) for key, value in constants.items()},
    projected_case_count=2 + (50 + 6) * 2 + 14 + 11 + 23 + 1,
    negative_sites=negative,
    support_materialise_calls=0,
    exact_schema_probe=dict(equal_authored_profile_observations=True, different_declared_constraints=True, observation=good[0]),
    duplicate_witness='Only original first then provider-changed same-ID in one page; identical control same page; no cross-page/reverse/Decimal-representation duplicate dimension',
    limits='No pytest, collection, mypy, product aggregate, application imports or repository changes'), indent=2))
