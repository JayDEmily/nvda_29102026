from pathlib import Path
import ast, hashlib, subprocess, tempfile, os
ROOT=Path(__file__).resolve().parents[6]
BASE='cf44a74385536672237de4747d084faaa7971b47'
PATH=Path('tests/tier_a/persistence/test_m13_state_kernel_contract.py')
def sha(b): return hashlib.sha256(b).hexdigest()
def funcs(b):
    tree=ast.parse(b)
    return {n.name:sha(ast.dump(n,annotate_fields=True,include_attributes=False).encode()) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name.startswith('test_m13_')}
def collect(p):
    r=subprocess.run([os.sys.executable,'-m','pytest','-c','/dev/null',str(p),'--collect-only','-q'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if r.returncode: raise AssertionError(r.stdout)
    return tuple(line.split('::',1)[1] for line in r.stdout.splitlines() if '::test_m13_' in line)
base=subprocess.check_output(['git','show',f'{BASE}:{PATH.as_posix()}'],cwd=ROOT)
cur=(ROOT/PATH).read_bytes()
bf,cf=funcs(base),funcs(cur)
with tempfile.TemporaryDirectory() as td:
    p=Path(td)/PATH.name; p.write_bytes(base); bc=collect(p)
cc=collect(ROOT/PATH)
changed=[n for n,d in bf.items() if cf.get(n)!=d]
missing=[n for n in bf if n not in cf]
new=sorted(set(cf)-set(bf))
missing_cases=sorted(set(bc)-set(cc))
duplicates=sorted(x for x in bc if cc.count(x)!=1)
new_cases=tuple(x for x in cc if x not in set(bc))
print(f'baseline_commit={BASE}')
print(f'baseline_file_sha256={sha(base)}')
print(f'current_file_sha256={sha(cur)}')
print(f'baseline_test_functions={len(bf)}')
print(f'current_test_functions={len(cf)}')
print(f'changed_frozen_functions={changed}')
print(f'missing_frozen_functions={missing}')
print(f'new_functions={new}')
print(f'baseline_cases={len(bc)}')
print(f'current_cases={len(cc)}')
print(f'missing_frozen_cases={len(missing_cases)}')
print(f'duplicate_frozen_cases={len(duplicates)}')
print(f'new_cases={len(new_cases)}')
assert len(bf)==24 and len(cf)==26 and len(bc)==131 and len(cc)==152
assert not changed and not missing and not missing_cases and not duplicates
print('frozen_v6_preservation=PASS')
