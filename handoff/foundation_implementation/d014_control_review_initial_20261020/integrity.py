from pathlib import Path
import subprocess, ast, hashlib, json, sqlite3, sys
base=Path(__file__).resolve().parent
actual=Path('/workspace/scratch/d549b6d808a9/g52-recovery/repository')
candidate=base/'proposed'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
paths=subprocess.check_output(['git','ls-files','-z'],cwd=actual).decode().split('\0')
scoped=[p for p in paths if p and p.startswith(('src/','config/','schemas/','implementation/authority/','tests/','tools/'))]
different=[p for p in scoped if (actual/p).read_bytes()!=(candidate/p).read_bytes()]
assert different==['tools/product_proof_claims.py'],different
print('scoped tracked byte comparison',len(scoped),'only difference',different)
left=ast.parse((actual/different[0]).read_text()); right=ast.parse((candidate/different[0]).read_text())
for name in ['_authority','_partition','_generation','_admission_history','governed_snapshot']:
 one=next(n for n in left.body if isinstance(n,ast.FunctionDef) and n.name==name)
 two=next(n for n in right.body if isinstance(n,ast.FunctionDef) and n.name==name)
 assert ast.dump(one)==ast.dump(two),name
 print(name,'AST unchanged')
for p in [different[0],'tests/architecture/test_proof_control.py','handoff/foundation_implementation/authority/G6_1_D014_CONTROL_CANDIDATE_20261020.patch','handoff/foundation_implementation/authority/G6_1_D014_IMPLEMENTATION_BRIEF_PROPOSED.md','handoff/foundation_implementation/authority/G6_1_D014_PROOF_CONTRACT_PROPOSED.json','implementation/authority/G6_1_D014_IMPLEMENTATION_AUTHORITY_BINDING.yaml']:
 print(p,'active',sha(actual/p),'proposed',sha(candidate/p))
print('environment',sys.version,'SQLite',sqlite3.sqlite_version)
print('shared-status',subprocess.check_output(['git','status','--porcelain=v1'],cwd=actual).decode())
print('candidate-status',subprocess.check_output(['git','status','--porcelain=v1'],cwd=candidate).decode())
