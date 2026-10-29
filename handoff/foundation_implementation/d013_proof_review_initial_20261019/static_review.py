"""Read/compile/AST inspection only; no application or test module imports."""
import ast
import hashlib
import re
from pathlib import Path

ROOT = Path('/workspace/scratch/d549b6d808a9/g52-recovery/repository')
FILES = ('test_ratio.py', '_support.py', 'typing/valid_seam.py', 'typing/invalid_seam.py')
base = ROOT / 'tests/product/market_measurement_d013'
for name in FILES:
    data = (base / name).read_bytes()
    compile(data, str(base / name), 'exec')
    print(name, hashlib.sha256(data).hexdigest(), 'COMPILE_PASS')
tree = ast.parse((base / FILES[0]).read_text())
tests = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')]
assert len(tests) == 6
print('SIX_FUNCTIONS', [(n.name, n.lineno) for n in tests])
refusals = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'REFUSALS' for t in n.targets))
storage = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
               and any(isinstance(t, ast.Name) and t.id == 'STORAGE_CASES' for t in n.targets))
assert len(refusals) == 66 and len(storage) == 20
print('PROJECTED_CASES', '2 + 66*2 + 12 + 12 + 20 + 1 = 179; no collection performed')
sites = [(i, re.search(r'MISUSE\[([^]]+)\]', line)[1])
         for i, line in enumerate((base / FILES[3]).read_text().splitlines(), 1) if 'MISUSE[' in line]
assert sites == [(16,'assignment'), (17,'assignment'), (18,'assignment'),
                 (19,'attr-defined'), (20,'arg-type'), (21,'arg-type'), (22,'assignment')]
print('SOURCE_REVIEWED_NEGATIVE_SITES', sites, 'COUNT', len(sites))
for file in ('_catalogue.py', '_sqlite.py'):
    source_tree = ast.parse((ROOT / 'src/nvda_desk/market_measurement_truth' / file).read_text())
    variable = 'payload' if file == '_catalogue.py' else 'expected_payload'
    values = [n.value for n in ast.walk(source_tree) if isinstance(n, ast.Assign)
              and any(isinstance(t, ast.Name) and t.id == variable for t in n.targets)
              and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name)
              and n.value.func.id == 'dict']
    keys = next([k.arg for k in n.keywords] for n in values
                if any(k.arg == 'owner_object_id' for k in n.keywords))
    assert 'result' not in keys and 'calculated_at_utc' not in keys
    print('OLD_LOGICAL_KEYS', file, keys)
print('NO_DOMAIN_EXECUTION_NO_IMPORTS_NO_MYPY_NO_COLLECTION')
