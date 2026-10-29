import csv, json, hashlib, re
from pathlib import Path
from collections import Counter
root=Path(__file__).resolve().parents[4]
a=root/'handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv'
f=root/'handoff/m01_completion/foundation'
def rows(p):
 with p.open(newline='',encoding='utf-8-sig') as r:return list(csv.DictReader(r))
def toks(s):return [x.strip() for x in s.split(';') if x.strip()]
def s1(r):return r['kernel_id'].split('_')[0] in {*(f'K{i:02}' for i in range(1,9)),'K16','K17'}
source=rows(a); so={r['derived_id']:r for r in source}; stage=[r for r in source if s1(r)]
E=set(); edges=[]
for r in stage:
 deps=[('R',x,i) for i,x in enumerate(toks(r['raw_dependencies']),1)]+[('D',x,i) for i,x in enumerate(toks(r['derived_dependencies']),1)]
 for t,d,n in deps:
  tup=(r['derived_id'],t,d,n)
  assert tup not in E,('duplicate_authority_edge',tup)
  E.add(tup); edges.append(tup)
 if not deps:E.add((r['derived_id'],'NONE','N/A',0))
assert len(stage)==174 and len(E)==489
mapped=rows(f/'F1_CLASSIFIED_EDGE_MAP.csv'); out=rows(f/'F1_AUTHORITY_RELATIONSHIP_CENSUS.csv'); rmap=rows(f/'F1_AUTHORITY_ROW_CENSUS.csv')
def key(r):return (r['derived_id'],r['source_type'],r['source_id'],int(r['dependency_ordinal']))
assert len(mapped)==len(out)==len(E)
assert set(map(key,mapped))==set(map(key,out))==E
assert len({r['derived_id'] for r in rmap})==174
assert all(all(r[x]==so[r['derived_id']][x] for x in ('workbook_row','kernel_id','parameter_profiles','typed_contexts','raw_dependencies','derived_dependencies','brief_rule_ref','binding_note','parameter_window')) for r in rmap)
assert all(all(m[x]==so[m['derived_id']][x] for x in ('workbook_row','kernel_id','parameter_profiles','typed_contexts','raw_dependencies','derived_dependencies','brief_rule_ref','parameter_window')) for m in mapped)
classes={r['relationship_class'] for r in mapped}
assert classes=={f'RC{i:02}' for i in range(1,22)}
clstext=(f/'F1_RELATIONSHIP_CLASSES.md').read_text()
prooftxt=(f/'F1_PROOF_MATRIX.md').read_text()
assert all(f'### {c} ' in clstext and f'| {c} (' in prooftxt for c in classes)
assert not any(v in ('UNMAPPED','UNCLASSIFIED','UNASSESSED','') for r in mapped for v in (r['implementation_mechanism'],r['relationship_class'],r['proof_status']))
# compute stage2 closure without worker algorithms
adj={r['derived_id']:toks(r['derived_dependencies']) for r in source}
other={r['derived_id'] for r in source if not s1(r)}
need=set(other)
for _ in range(209):
 nxt=need|{d for d,ds in adj.items() if set(ds)&need}
 if nxt==need:break
 need=nxt
else:raise AssertionError('closure_not_converged')
direct={r['derived_id'] for r in stage if set(adj[r['derived_id']])&other}
trans={r['derived_id'] for r in stage if r['derived_id'] in need}-direct
closed={r['derived_id'] for r in stage if r['derived_id'] not in need}
assert (len(direct),len(trans),len(closed))==(25,5,144)
assert all(r['stage2_boundary']== ('CROSS_STAGE_DIRECT' if r['derived_id'] in direct else 'CROSS_STAGE_TRANSITIVE' if r['derived_id'] in trans else 'STAGE1_CLOSED') for r in rmap)
raw=sum(e[1]=='R' for e in E); derived=sum(e[1]=='D' for e in E)
assert (raw,derived)==(291,197)
assert all(re.search(r'§\d',r['brief_rule_ref']) for r in stage)
for d,t,target,c in [('D015','R','R120','RC07'),('D016','D','D015','RC08'),('D120','D','D015','RC08'),('D109','D','D087','RC10'),('D170','D','D087','RC10'),('D121','D','D120','RC11'),('D122','D','D085','RC11'),('D065','D','D064','RC01')]:
 assert any(r['derived_id']==d and r['source_type']==t and r['source_id']==target and r['relationship_class']==c for r in mapped)
print(json.dumps({'independent_review':'F1_STATIC_AUDIT','row_count':len(stage),'raw_edges':raw,'derived_edges':derived,'zero_edge':sum(e[1]=='NONE' for e in E),'stage1_closed':len(closed),'direct_stage2':len(direct),'transitive_stage2_only':len(trans),'classes':len(classes),'mapped_records':len(mapped),'catalogue_digest':hashlib.sha256(a.read_bytes()).hexdigest(),'classification_unmapped':0,'edge_set_difference':0,'row_field_drift':0,'sampled_relationships':['D015/R120','D016/D015','D120/D015','D109/D087','D170/D087','D121/D120','D122/D085','D065/D064'],'summary':'PASS_static_exhaustiveness_not_semantic_acceptance'},indent=2))
