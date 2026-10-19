from pathlib import Path
import subprocess,sys,shutil,json,hashlib
base=Path(__file__).resolve().parent
root=base/'sequence-diagnostic'
subprocess.run(['git','clone','--shared','-q','/workspace/scratch/d549b6d808a9/g52-recovery/repository',str(root)],check=True)
shutil.copyfile(base/'proposed/tools/product_proof_claims.py',root/'tools/product_proof_claims.py')
sys.path[:0]=[str(root/'tools'),str(root/'src')]
import product_proof_claims as api
assert Path(api.__file__).resolve()==root/'tools/product_proof_claims.py'
claims=['raw_signal_occurrence_truth_sqlite','neutral_market_measurement_truth_pilot','neutral_market_measurement_truth_d012','neutral_market_measurement_truth_d013','neutral_market_measurement_truth_d014']
descriptor=root/'config/product_proof/market_measurement_d014/claim.json'
physical=root/'tests/product/market_measurement_d014'
for claim in claims[:-1]: assert api.load_product_proof_claim(root,claim).state=='READY_FOR_PROOF'
print('baseline all4 ready; loader',api.__file__,hashlib.sha256(Path(api.__file__).read_bytes()).hexdigest(),flush=True)
for name in ['_support.py','nested/helper.py','test_orphan.py','dangling.py']:
 witness=physical/name; witness.parent.mkdir(parents=True,exist_ok=True)
 if name=='dangling.py': witness.symlink_to('missing.py')
 else: witness.write_text('# sequential independent control witness\n')
 for claim in claims:
  print('PRE',name,claim,'descriptor',descriptor.exists(),'witness',witness.is_file(),witness.is_symlink(),'allpaths',[str(p.relative_to(physical)) for p in physical.rglob('*')],flush=True)
  assert not descriptor.exists()
  assert witness.is_file() or witness.is_symlink()
  try: api.load_product_proof_claim(root,claim)
  except (ValueError,OSError) as exc: print('REJECT',type(exc).__name__,str(exc),flush=True)
  else: raise AssertionError(('unexpected acceptance',name,claim))
  assert not descriptor.exists() and (witness.is_file() or witness.is_symlink())
 witness.unlink()
 assert not witness.exists() and not witness.is_symlink()
 print('REMOVED',name,flush=True)
 for claim in claims[:-1]: assert api.load_product_proof_claim(root,claim).state=='READY_FOR_PROOF'
print('SEQUENTIAL_DIAGNOSTIC_ALL_PASS',flush=True)
