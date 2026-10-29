import subprocess,sys,json,hashlib,os
from pathlib import Path
out=Path('/workspace/scratch/56b9974b28a0/d014-review-output'); repo=Path('/workspace/scratch/56b9974b28a0/d014-review-clone')
commands={
'full_mypy':[sys.executable,'-m','mypy','src','tools/product_proof_claims.py','tools/product_proof_outcomes.py','tools/run_product_proof_gate.py','tests/architecture/test_proof_control.py'],
'scoped_ruff':[sys.executable,'-m','ruff','check','src/nvda_desk/market_measurement_truth/api.py','src/nvda_desk/market_measurement_truth/_raw_rational.py','src/nvda_desk/market_measurement_truth/_raw_rational_sqlite.py','src/nvda_desk/market_measurement_truth/_rational.py','tests/product/market_measurement_d014','tools/product_proof_claims.py','tests/architecture/test_proof_control.py'],
'promotion':[sys.executable,'tools/run_promotion_gate.py','--set','architecture_kernel']}
for name,cmd in commands.items():
 p=subprocess.run(cmd,cwd=repo,capture_output=True,env=dict(os.environ,PYTHONPATH=str(repo/'src')))
 (out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr)
 (out/(name+'.json')).write_text(json.dumps(dict(command=cmd,returncode=p.returncode,stdout_sha256=hashlib.sha256(p.stdout).hexdigest()),indent=2))
 print(name,p.returncode,flush=True)
 if p.returncode:break
