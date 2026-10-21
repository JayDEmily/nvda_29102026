import subprocess,os,sys,json,hashlib,pickle,base64
from pathlib import Path
repo=Path('/workspace/scratch/56b9974b28a0/d014-review-clone'); out=Path('/workspace/scratch/56b9974b28a0/d014-review-output')
py=sys.executable
env=dict(os.environ,PYTHONPATH=os.pathsep.join([str(repo/'src'),str(repo/'tests/product/market_measurement_d014')]))
def run(name,args):
 p=subprocess.run(args,cwd=repo,env=env,capture_output=True)
 (out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr)
 print(name,p.returncode,flush=True)
 assert p.returncode==0,p.stderr.decode(errors='replace')
 return p.stdout
run('candidate',['git','rev-parse','HEAD','HEAD^{tree}'])
run('python',[py,'-c','import sys,sqlite3; print(sys.version); print(sqlite3.sqlite_version)'])
writer=run('direct_writer',[py,str(out/'direct_writer.py'),str(out/'public-data')])
bundle=pickle.loads(base64.b64decode(writer)); path=out/'public-data/ratio.sqlite'; before=path.read_bytes()
reader=run('direct_reader',[py,str(out/'direct_reader.py'),str(path),'c23ea315c94b478c568f105e94891a03af62393792a1478c33027a0371738bb8',*[f.derived_occurrence_id for f in bundle['facts']]])
assert pickle.loads(base64.b64decode(reader))==bundle
assert path.read_bytes()==before
(out/'direct_result.json').write_text(json.dumps(dict(facts=len(bundle['facts']),equal_complete_typed_bundle=True,readonly_bytes_unchanged=True,writer_exit_before_reader=True,sha256=hashlib.sha256(before).hexdigest()),indent=2))
run('native_d014',[py,'tools/run_product_proof_gate.py','--aggregate','neutral_market_measurement_truth_d014'])
run('clean_after',['git','status','--porcelain'])
