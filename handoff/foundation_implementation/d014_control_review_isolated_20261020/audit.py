from pathlib import Path
import ast
import hashlib
import importlib.metadata
import json
import sqlite3
import subprocess
import sys
BASE=Path(__file__).resolve().parent
ACTUAL=Path('/workspace/scratch/d549b6d808a9/resume-20261020-ejayrse7/repository')
ROOT=BASE/'candidate'
def git(root,*args): return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
assert git(ACTUAL,'rev-parse','HEAD')==git(ROOT,'rev-parse','HEAD')=='f01ad17c48f0eb21148cb7b2aa4e2b2f428c0f2b'
assert git(ACTUAL,'status','--porcelain=v1')==''
assert not (ROOT/'.git/objects/info/alternates').exists()
assert not any(p.is_symlink() for p in ROOT.rglob('*'))
tracked=git(ACTUAL,'ls-files').splitlines()
scope=[name for name in tracked if name.startswith(('src/','tools/','tests/','config/','schemas/','implementation/authority/','handoff/foundation_implementation/authority/'))]
diff=[name for name in scope if (ACTUAL/name).read_bytes()!=(ROOT/name).read_bytes()]
assert diff==['tools/product_proof_claims.py'],diff
for name in tracked:
 assert (ACTUAL/name).stat().st_ino != (ROOT/name).stat().st_ino
left=ast.parse((ACTUAL/diff[0]).read_text()); right=ast.parse((ROOT/diff[0]).read_text())
for name in ('_authority','_partition','_generation','_admission_history','governed_snapshot'):
 one=next(n for n in left.body if isinstance(n,ast.FunctionDef) and n.name==name)
 two=next(n for n in right.body if isinstance(n,ast.FunctionDef) and n.name==name)
 assert ast.dump(one)==ast.dump(two),name
print(json.dumps({'head':git(ROOT,'rev-parse','HEAD'),'tree':git(ROOT,'rev-parse','HEAD^{tree}'),
 'scoped_count':len(scope),'only_difference':diff,'no_shared_tracked_inodes':True,
 'candidate_symlinks':False,'git_alternates':False,'actual_clean':True,
 'lineage_scoped_diff':git(ACTUAL,'diff','--exit-code','c990f8b','f01ad17','--','src','tools','config','schemas','tests','implementation/authority','handoff/foundation_implementation/authority'),
 'preserved_ASTs':['_authority','_partition','_generation','_admission_history','governed_snapshot'],
 'python':sys.version,'sqlite':sqlite3.sqlite_version,'versions':{name:importlib.metadata.version(name) for name in ['pytest','mypy','ruff','PyYAML']},
 'hashes':{name:{'active':sha(ACTUAL/name),'candidate':sha(ROOT/name)} for name in [diff[0],'tests/architecture/test_proof_control.py','handoff/foundation_implementation/authority/G6_1_D014_CONTROL_CANDIDATE_20261020.patch','handoff/foundation_implementation/authority/G6_1_D014_IMPLEMENTATION_BRIEF_PROPOSED.md','handoff/foundation_implementation/authority/G6_1_D014_PROOF_CONTRACT_PROPOSED.json','implementation/authority/G6_1_D014_IMPLEMENTATION_AUTHORITY_BINDING.yaml']}},indent=2))
