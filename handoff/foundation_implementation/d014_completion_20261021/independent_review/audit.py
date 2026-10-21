from pathlib import Path
import subprocess,hashlib,json
repo=Path('/workspace/scratch/56b9974b28a0/d014-review-clone'); out=Path('/workspace/scratch/56b9974b28a0/d014-review-output')
def git(*args):return subprocess.check_output(['git',*args],cwd=repo)
assert git('rev-parse','HEAD').decode().strip()=='b0a61a7f960b1cff4f95605347db2773d1078c65'
assert git('status','--porcelain')==b''
assert git('diff','0d3600c','HEAD','--','src')==b''
assert git('diff','19c14ee','HEAD','--','tests','config/product_proof','implementation/authority','handoff/foundation_implementation/authority')==b''
physical={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (repo/'tests/product/market_measurement_d014').rglob('*.py')}
g=json.loads((repo/'config/product_proof/market_measurement_d014/generations/0002.json').read_text())
for row in g['family_files']+g['support_files']:assert physical[row['path']]==row['sha256']
logs={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in out.iterdir() if p.is_file() and p.suffix in ('.stdout','.stderr')}
(out/'audit.json').write_text(json.dumps(dict(candidate=git('rev-parse','HEAD').decode().strip(),tree=git('rev-parse','HEAD^{tree}').decode().strip(),clean=True,production_unchanged_since='0d3600c',proof_authority_unchanged_since='19c14ee',physical=physical,logs=logs),indent=2))
print('audit PASS')
