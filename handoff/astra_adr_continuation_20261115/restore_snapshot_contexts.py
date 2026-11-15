from pathlib import Path
import subprocess,json,hashlib,gzip
R=Path('/workspace/nvda');O=R/'handoff/astra_adr_continuation_20261115';A=Path('/workspace/recovery-assets');logs=[];contexts=[]
def run(args,cwd):
 p=subprocess.run(args,cwd=cwd,text=True,capture_output=True);logs.append({'command':args,'cwd':str(cwd),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0,(args,p.stderr);return p.stdout.strip()
def load(p):return json.loads(p.read_text())
def add(source,path,refs):contexts.append({'source':source,'context':path,'refs':refs,'id':hashlib.sha256((source+path).encode()).hexdigest()[:12]})
p=R/'handoff/planning/t01_recovered_successor_20261111/ORIGINAL_66_REFS.json';add(str(p.relative_to(R)),'$',{r['ref']:r['tip'] for r in load(p)})
p=R/'handoff/m02_completion_28_execution/L00/L00_MANIFEST.json';add(str(p.relative_to(R)),'$.refs',load(p)['refs'])
p=R/'handoff/m02_completion_28_execution/L00/CURRENT_REFS.txt';add(str(p.relative_to(R)),'$',{r.split()[1]:r.split()[0] for r in p.read_text().splitlines()})
p=R/'handoff/planning/t01_recovered_successor_20261111/GITHUB_REMOTE_RECEIVER_RECEIPT.json';add(str(p.relative_to(R)),'$.fetched_remote_branches',{'refs/heads/'+k:v for k,v in load(p)['fetched_remote_branches'].items()})
for name in ['CURRENT_REF_MANIFEST.json','ADDITIVE_HEADER_COMPLETION.json']:
 def walk(x,path='$'):
  if isinstance(x,dict):
   refs={k:v for k,v in x.items() if k.startswith('refs/') and isinstance(v,str) and len(v)==40}
   if refs:add(name,path,refs)
   for k,v in x.items():
    if k not in refs:walk(v,path+'.'+k)
  elif isinstance(x,list):
   for i,v in enumerate(x):walk(v,f'{path}[{i}]')
 walk(load(A/name))
assert sum(len(c['refs']) for c in contexts)==2281
store=Path('/workspace/astra-context-source.git');fresh=Path('/workspace/astra-context-fresh.git');bundle=A/'ASTRA_REQUIRED_CONTEXTS_FULL_HISTORY.bundle'
run(['git','init','--bare',str(store)],R);(store/'objects/info/alternates').write_text('/workspace/astra-receiver.git/objects\n')
for c in contexts:
 for ref,tip in c['refs'].items():run(['git','update-ref','refs/checkpoint-contexts/'+c['id']+'/'+ref[5:],tip],store)
run(['git','fsck','--full','--no-reflogs'],store);run(['git','bundle','create',str(bundle),'--all'],store);run(['git','init','--bare',str(fresh)],R);run(['git','bundle','verify',str(bundle)],fresh);run(['git','fetch',str(bundle),'refs/*:refs/*'],fresh);run(['git','fsck','--full','--no-reflogs'],fresh)
assert run(['git','for-each-ref','--format=%(objectname) %(refname)'],store)==run(['git','for-each-ref','--format=%(objectname) %(refname)'],fresh)
results=[]
for c in contexts:
 view=Path('/workspace/astra-snapshot-'+c['id']+'.git');run(['git','init','--bare',str(view)],R);(view/'objects/info/alternates').write_text(str(fresh/'objects')+'\n')
 for ref,tip in c['refs'].items():
  alias='refs/preservation/local-bootstrap-work' if ref=='refs/heads/work' else ref;restored=run(['git','rev-parse','refs/checkpoint-contexts/'+c['id']+'/'+ref[5:]],fresh);assert restored==tip;run(['git','update-ref',alias,restored],view)
 for ref,tip in c['refs'].items():
  alias='refs/preservation/local-bootstrap-work' if ref=='refs/heads/work' else ref;actual=run(['git','rev-parse',alias],view);assert actual==tip;results.append({'inventory':c['source'],'snapshot_context':c['context'],'context_id':c['id'],'literal_ref':ref,'expected_tip':tip,'receiver_name':alias,'transport_name':'refs/checkpoint-contexts/'+c['id']+'/'+ref[5:],'final_readback':actual,'status':'VERIFIED'})
 run(['git','fsck','--full','--no-reflogs'],view)
summary={'status':'VERIFIED_SNAPSHOT_SCOPED_TRANSPORT_AND_FINAL_READBACK','rows':len(results),'contexts':len(contexts),'unique_ref_tip_pairs':len({(r['literal_ref'],r['expected_tip']) for r in results}),'bundle_path':str(bundle),'bundle_sha256':hashlib.sha256(bundle.read_bytes()).hexdigest(),'bundle_bytes':bundle.stat().st_size,'fresh_object_store':str(fresh),'fresh_store_alternates':False,'context_views_shared_object_store':str(fresh/'objects'),'contract':'Literal names checked after complete snapshot installation in each view. All snapshots transported together under explicit context namespaces. The single documented work/work/* alias is preserved.','contexts':[{'source':c['source'],'context':c['context'],'id':c['id'],'ref_count':len(c['refs'])} for c in contexts]}
(O/'SNAPSHOT_CONTEXT_RESTORE.json').write_text(json.dumps(summary,indent=2)+'\n');(O/'REQUIRED_REF_RESULTS_CURRENT.json').write_text(json.dumps(results,indent=2)+'\n');(O/'SNAPSHOT_CONTEXT_COMMANDS.json.gz').write_bytes(gzip.compress(json.dumps(logs,indent=2).encode(),mtime=0));print({k:summary[k] for k in ['status','rows','contexts','unique_ref_tip_pairs','bundle_sha256']})
