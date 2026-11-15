from pathlib import Path
import subprocess,json,hashlib,collections
R=Path('/workspace/nvda'); O=R/'handoff/astra_adr_completion_20261115'; A=Path('/workspace/recovery-assets'); O.mkdir(exist_ok=True)
log=[]
def run(args,cwd=R):
 p=subprocess.run(args,cwd=cwd,text=True,capture_output=True);log.append({'command':args,'cwd':str(cwd),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p

def dump(name,obj):(O/name).write_text(json.dumps(obj,indent=2)+'\n')
def load(p):return json.loads((R/p).read_text())
remote={ref:sha for sha,ref in (l.split() for l in run(['git','ls-remote','origin']).stdout.splitlines())}
dump('REMOTE_REFS.json',remote)
original=load('handoff/planning/t01_recovered_successor_20261111/ORIGINAL_66_REFS.json')
rows=[]
def add(ref,tip,source):rows.append({'ref':ref,'expected_tip':tip,'inventory':source})
for x in original:add(x['ref'],x['tip'],'ORIGINAL_66_REFS.json')
for src in ['handoff/m02_completion_28_execution/L00/L00_MANIFEST.json']:
 for ref,tip in load(src)['refs'].items():add(ref,tip,src)
for line in (R/'handoff/m02_completion_28_execution/L00/CURRENT_REFS.txt').read_text().splitlines():
 tip,ref=line.split();add(ref,tip,'CURRENT_REFS.txt')
receipt=load('handoff/planning/t01_recovered_successor_20261111/GITHUB_REMOTE_RECEIVER_RECEIPT.json')
for ref,tip in receipt['fetched_remote_branches'].items():add('refs/heads/'+ref,tip,'GITHUB_REMOTE_RECEIVER_RECEIPT.json')
# Downloaded successor manifest is additional, not a replacement for committed historical inventories.
for name in ['CURRENT_REF_MANIFEST.json','ADDITIVE_HEADER_COMPLETION.json']:
 if (A/name).exists():
  obj=json.loads((A/name).read_text())
  def walk(x):
   if isinstance(x,dict):
    for k,v in x.items():
     if k.startswith('refs/') and isinstance(v,str) and len(v)==40:add(k,v,name)
     else:walk(v)
   elif isinstance(x,list):
    for y in x:walk(y)
  walk(obj)
receiver=Path('/workspace/astra-receiver.git');run(['git','init','--bare',str(receiver)])
# fetch all advertised refs under an isolated namespace, never historical names onto current main.
run(['git','fetch','--no-tags',str(R),'+refs/remotes/origin/*:refs/received/heads/*','+refs/tags/*:refs/received/tags/*'],receiver)
for x in rows:
 tip=x['expected_tip']; p=run(['git','cat-file','-t',tip],receiver);x['object_type']=p.stdout.strip() if p.returncode==0 else None;x['object_status']='VERIFIED' if p.returncode==0 else 'BLOCKED'
 ref=x['ref'];pub=ref if not ref.startswith('refs/remotes/origin/') else 'refs/heads/'+ref[len('refs/remotes/origin/'):]
 x['published_ref']=pub;x['published_tip']=remote.get(pub);x['literal_remote_status']='VERIFIED' if remote.get(ref)==tip else 'UNKNOWN';x['mapped_remote_status']='VERIFIED' if remote.get(pub)==tip else 'UNKNOWN'
 x['restoration_status']='BLOCKED' if p.returncode else 'VERIFIED';x['restoration_name']= 'refs/preservation/local-bootstrap-work' if ref=='refs/heads/work' else ref
# historical collisions and changing refs across checkpoints require isolated namespaces per inventory.
for source in sorted({x['inventory'] for x in rows}):
 d=Path('/workspace/restore-'+source.split('/')[-1].replace('.','-')+'.git');run(['git','init','--bare',str(d)])
 run(['git','fetch','--no-tags',str(receiver),'+refs/received/*:refs/received/*'],d)
 for x in [x for x in rows if x['inventory']==source and x['object_status']=='VERIFIED']:
  p=run(['git','update-ref',x['restoration_name'],x['expected_tip']],d)
  if p.returncode:x['restoration_status']='BLOCKED';x['restoration_error']=p.stderr
  else:x['readback']=run(['git','rev-parse',x['restoration_name']],d).stdout.strip()
 fsck=run(['git','fsck','--full','--no-reflogs'],d)
 run(['git','bundle','create',str(d)+'.bundle','--all'],d)
 run(['git','bundle','verify',str(d)+'.bundle'],d)
 fresh=Path(str(d)+'.fresh');run(['git','init','--bare',str(fresh)])
 run(['git','fetch',str(d)+'.bundle','+refs/*:refs/*'],fresh)
 run(['git','fsck','--full','--no-reflogs'],fresh)
 xrefs=run(['git','for-each-ref','--format=%(objectname) %(refname)'],d).stdout
 yrefs=run(['git','for-each-ref','--format=%(objectname) %(refname)'],fresh).stdout
 dump(source.split('/')[-1]+'.restore.json',{'ref_equality':xrefs==yrefs,'fsck_exit':fsck.returncode,'bundle_sha256':hashlib.sha256(Path(str(d)+'.bundle').read_bytes()).hexdigest(),'scope':'New full Git transport; not original historical bundle, independent Tester signoff or non-Git recovery'})
dump('REQUIRED_REF_RESULTS.json',rows)
run(['git','fsck','--full','--no-reflogs'])
for sha in ['97f944d51ab9e403250fe76910e2754b50425c73','ef0f6876f2b5673a91946eeaaaac964b40e1efe7']:
 run(['git','merge-base','--is-ancestor',sha,'02a19ae02678824908568d8db08f0e1d015cb861'])
f02='16b7cc67f5d24336d3768e2da006819474a8c792'; tree=run(['git','rev-parse',f02+'^{tree}']).stdout.strip(); listing=run(['git','ls-tree','-r',f02]).stdout
# Historical inventory used ls-tree raw listing.
dump('F02_CURRENT_READBACK.json',{'commit':f02,'tree':tree,'tracked_count':len(listing.splitlines()),'ls_tree_sha256':hashlib.sha256(listing.encode()).hexdigest(),'historical_receiver_unchanged':True,'independent_chat_tester':'NOT_EXECUTED'})
summary={'inventory_rows':len(rows),'unique_ref_tip_pairs':len({(x['ref'],x['expected_tip']) for x in rows}),'original_66':dict(collections.Counter(x['restoration_status'] for x in rows if x['inventory']=='ORIGINAL_66_REFS.json')),'all_objects':dict(collections.Counter(x['object_status'] for x in rows)),'literal_remote':dict(collections.Counter(x['literal_remote_status'] for x in rows)),'restoration':dict(collections.Counter(x['restoration_status'] for x in rows))}
dump('RECOVERY_SUMMARY.json',summary);dump('RECOVERY_COMMANDS.json',log);print(summary)
