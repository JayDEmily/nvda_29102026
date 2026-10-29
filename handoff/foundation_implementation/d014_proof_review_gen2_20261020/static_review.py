"""Independent generation2 AST/compile audit; never imports authored code."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path('/workspace/scratch/d549b6d808a9/resume-20261020-ejayrse7/repository')
BASE=ROOT/'tests/product/market_measurement_d014'
def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT).decode().strip()
assert git('rev-parse','HEAD')=='96086e437cd8081e8617aef9324a4b0ee27784d7'
assert git('rev-parse','HEAD^{tree}')=='834e0090acf3c4ce2d3ae4450a737d1a413dbbd3'
assert not git('status','--porcelain')
hashes={
 'test_raw_ratio.py':'7e26d16d59ac42ac456e631e2acb8a5bee204e937550d5667f6bc580ba99f836',
 '_support.py':'49c6149d1ff64e002154b275bc9c54793cf60623bb0c9878c0fd5539fbc058e6',
 'typing/valid_seam.py':'3d1e2ac2449fc13be7db8f0e26c2b505dee5e6810d591dd190d4044bf859dacc',
 'typing/invalid_seam.py':'84b2806f0c8be162321c35f792f987550a3cf2ff428d37edd007042fcc699fc9'}
for name,digest in hashes.items():
    data=(BASE/name).read_bytes()
    assert hashlib.sha256(data).hexdigest()==digest
    compile(data,str(BASE/name),'exec')
    print('COMPILE_ONLY',name,digest)
authority=ROOT/'handoff/foundation_implementation/authority'
for name,digest in [('G6_1_D014_IMPLEMENTATION_BRIEF_PROPOSED.md','c23ea315c94b478c568f105e94891a03af62393792a1478c33027a0371738bb8'),('G6_1_D014_PROOF_CONTRACT_PROPOSED.json','54850f780c4442924e2d28ed319ae5f0fb109e291b367391ac0a4c86190294fc')]:
    assert hashlib.sha256((authority/name).read_bytes()).hexdigest()==digest
contract=json.loads((authority/'G6_1_D014_PROOF_CONTRACT_PROPOSED.json').read_text())
current=ast.parse((BASE/'test_raw_ratio.py').read_text())
old=ast.parse(git('show','ec0f363:tests/product/market_measurement_d014/test_raw_ratio.py'))
dump=lambda n:ast.dump(n,include_attributes=False)
top=lambda t:{n.name:n for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
assert [n.name for n in current.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]==contract['families'][0]['required_test_names']
special='test_d014_selection_and_refusal'
assert all(dump(top(old)[name])==dump(node) for name,node in top(current).items() if name!=special)
old_test,new_test=top(old)[special],top(current)[special]
assert [dump(n) for n in old_test.decorator_list]==[dump(n) for n in new_test.decorator_list]
old_reader=next(n for n in old_test.body if isinstance(n,ast.ClassDef))
new_reader=next(n for n in new_test.body if isinstance(n,ast.ClassDef))
assert [dump(n) for n in old_test.body[old_test.body.index(old_reader)+1:]]==[dump(n) for n in new_test.body[new_test.body.index(new_reader)+1:]]
method=new_reader.body[0]
assert isinstance(method.body[1],ast.If)
assert 'synthetic_cursor_modes' in ast.unparse(method.body[1].test)
assert isinstance(method.body[2],ast.Assign)
assert 'raw.reads.list_projected_raw_history' in ast.unparse(method.body[2])
assert any(isinstance(n,ast.Return) for n in method.body[1].body)
assert not any(isinstance(n,ast.Subscript) and ast.unparse(n)=='page.items[0]' for n in ast.walk(method.body[1]))
assert not any(isinstance(n,ast.Try) for n in ast.walk(new_test))
literal={n.targets[0].id:ast.literal_eval(n.value) for n in current.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('REFUSALS','POSITIVES','DUPLICATE_CASES','STORAGE_CASES')}
assert [len(literal[n]) for n in ('REFUSALS','POSITIVES','DUPLICATE_CASES','STORAGE_CASES')]==[50,7,16,28]
assert set(literal['DUPLICATE_CASES'].values())=={(d,r,p) for d in ('provider','representation','stale','receipt') for r in (False,True) for p in (False,True)}
assert 2+2*(50+7+16)+14+11+28+1==202
misuses=[(i,re.search(r'MISUSE\[([^]]+)\]',line)[1]) for i,line in enumerate((BASE/'typing/invalid_seam.py').read_text().splitlines(),1) if 'MISUSE[' in line]
assert misuses==[(18,'assignment'),(19,'assignment'),(20,'assignment'),(21,'assignment'),(22,'assignment'),(23,'attr-defined'),(24,'arg-type'),(25,'arg-type'),(26,'assignment'),(27,'assignment')]
assert not git('diff','0d3600c','HEAD','--','src')
assert not git('diff','6543a576','HEAD','--','config/product_proof/market_measurement_d014')
gen=ROOT/'config/product_proof/market_measurement_d014/generations/0001.json'
assert hashlib.sha256(gen.read_bytes()).hexdigest()=='f531b7216a3ce1e468015b40d6d3ca01742b56eb09587e49a972d41f33a47b23'
assert json.loads((gen.parent.parent/'admission.json').read_text())['current_generation']['sha256']=='f531b7216a3ce1e468015b40d6d3ca01742b56eb09587e49a972d41f33a47b23'
logs=ROOT/'handoff/foundation_implementation/d014_engineering_first_failure_20261020'
for stem in ('mypy','p01_p04','readiness'):
    meta=json.loads((logs/(stem+'.json')).read_text())
    data=(logs/(stem+'.log')).read_bytes()
    assert hashlib.sha256(data).hexdigest()==meta['log_sha256']
data=(logs/'p01_p04.log').read_text()
assert data.count('E       IndexError: tuple index out of range')==4
assert data.count('page = ProjectedRawHistoryPageV1(items=(), next_cursor=None)')==4
assert '4 failed, 169 passed in 33.11s' in data
print('SIX_NAMES;202_SOURCE_PROJECTED_CASES;10_EXACT_SITES;UNCHANGED_OTHER_FUNCTION_ASTS')
print('REFUSAL_ASSERTIONS_AFTER_READER_BYTE_SEMANTICS_UNCHANGED;EARLY_SYNTHETIC_RETURN')
print('PRODUCTION_EXACT_0d3600c;GEN1_AND_POINTER_UNCHANGED;FIRST_FAILURE_LOG_HASHES_MATCH')
