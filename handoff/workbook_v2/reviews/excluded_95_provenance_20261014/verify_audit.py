#!/usr/bin/env python3
"""Independent readback and source reconciliation for Pass05 audit, without re-running builder."""
import csv,hashlib,json,re,zipfile,xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3]
SRC=R/'handoff/m01_completion/authority'
files={
'rows':H/'NVDA_EXCLUDED_95_PROVENANCE_RESPONSIBILITY_AUDIT.csv',
'edges':H/'NVDA_EXCLUDED_95_STEP_SOURCE_EDGES.csv',
'groups':H/'NVDA_EXCLUDED_95_PROPOSED_GROUPS.csv',
'sources':H/'NVDA_EXCLUDED_95_RESEARCH_SOURCES.csv',
'xlsx':H/'NVDA_EXCLUDED_95_PROVENANCE_REVIEW_20261014.xlsx',
}
def rows(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def assert_eq(a,b,label):assert a==b,f'{label}: {a!r} != {b!r}'
source_csv=rows(SRC/'NVDA_DERIVED_SIGNAL_CATALOGUE.csv')
assert_eq(len(source_csv),209,'norm D count'); idx={r['derived_id']:r for r in source_csv}
pass04=rows(R/'handoff/workbook_v2/reviews/m01_1_boundary_20261014/M01_1_FULL_209_ROW_ELIGIBILITY_REVIEW.csv')
oldno={r['D_ID'] for r in pass04 if r['M01_1_Proposed_Eligibility']=='NO'}
assert_eq(len(oldno),95,'95 count')
d=rows(files['rows']);e=rows(files['edges']);g=rows(files['groups']);s=rows(files['sources'])
assert_eq(len(d),95,'audit row count'); assert_eq({r['D_ID'] for r in d},oldno,'same 95')
assert_eq(len(g),30,'proposed group count');assert_eq(len(e),810,'research edge count');assert_eq(len(s),54,'paper count')
assert_eq(len({r['D_ID']+':'+r['Required_Framework_Step'] for r in e}),810,'one step source per D link')
bygroup={r['Group_ID']:r for r in g};assert_eq({r['Proposed_Responsibility_Group_ID'] for r in d},set(bygroup),'groups complete')
assert_eq(sum(int(r['Count']) for r in g),95,'group counts')
for r in g:
 members=set(r['D_IDs'].split(';'));assert_eq(members,{x['D_ID'] for x in d if x['Proposed_Responsibility_Group_ID']==r['Group_ID']},r['Group_ID'])
for r in d:
 x=idx[r['D_ID']]
 for k,a in [('Raw_Dependencies','raw_dependencies'),('Derived_Dependencies','derived_dependencies'),('Normative_Calculation_Concept','calculation_concept'),('Normative_Kernel','kernel_id'),('Normative_Parameter_Profiles','parameter_profiles'),('Normative_Typed_Contexts','typed_contexts')]:assert_eq(r[k],x[a],r['D_ID']+'/'+k)
 assert r['Direct_Individual_Equation_Paper_Citation_Status']=='NOT_ESTABLISHED'
 assert r['Formal_Module_Owner']=='UNALLOCATED'
 assert r['Playbook_Consumers']=='UNKNOWN_NOT_AUTHORISED'
 assert set(r['Framework_Evidence_Source_IDs'].split(';')) <= {x['Source_ID'] for x in e if x['D_ID']==r['D_ID']}
 source_steps={int(x) for x in r['Expanded_Steps'].split(';')};edge_steps={int(x['Required_Framework_Step']) for x in e if x['D_ID']==r['D_ID']};assert_eq(source_steps,edge_steps,r['D_ID']+' steps')
for link in e:
 assert link['Academic_Claim_Scope']=='STEP_PROPOSITION_ONLY';assert link['D_Equation_Paper_Derivation_Proven']=='NO';assert link['Source_URL'].startswith('https://')
 assert link['Source_ID'] in {x['Source_ID'] for x in s}
# Group graph must be acyclic (more restrictive than D graph for module-layer viability).
ids={r['D_ID']:r['Proposed_Responsibility_Group_ID'] for r in d};adj=defaultdict(set)
for r in d:
 for pred in filter(None,r['Derived_Dependencies'].split(';')):
  if pred in ids and ids[pred]!=ids[r['D_ID']]:adj[ids[r['D_ID']]].add(ids[pred])
visited={}
def walk(node):
 assert visited.get(node)!=1, ('group cycle',node)
 if visited.get(node)==2:return
 visited[node]=1
 for v in adj[node]:walk(v)
 visited[node]=2
for node in bygroup:walk(node)
# Read back generated XLSX using package XML independent of builder, avoiding assumptions about sheet names.
with zipfile.ZipFile(files['xlsx']) as z:
 assert z.testzip() is None
 n='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
 wb=ET.fromstring(z.read('xl/workbook.xml')); names=[x.get('name') for x in wb.find(n+'sheets')]
 assert_eq(names,['Audit Summary','95 D Review','30 Groups','Step Source Links','Academic Sources'],'workbook sheets')
 rels=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'));lookup={x.get('Id'):x.get('Target') for x in rels};rel='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
 for sheet,expected in [('95 D Review',96),('30 Groups',31),('Step Source Links',811),('Academic Sources',55)]:
  a=next(x for x in wb.find(n+'sheets') if x.get('name')==sheet);p=lookup[a.get(rel)].lstrip('/');p=p if p.startswith('xl/') else 'xl/'+p
  x=ET.fromstring(z.read(p)); sheetrows=x.findall('.//'+n+'sheetData/'+n+'row');assert_eq(len(sheetrows),expected,sheet)
summary=json.loads((H/'AUDIT_SUMMARY.json').read_text());assert summary['total_D_to_framework_step_links']==len(e)
assert summary['group_singletons']==sum(int(r['Count'])==1 for r in g)
assert_eq(sha(SRC/'NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx'),'519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae','original sha')
assert_eq(sha(SRC/'NVDA_DERIVED_SIGNAL_CATALOGUE.csv'),'26c5486d1a4c7ff68025c7ce2d7e6847a7798759b847a716c942fd05345f3803','norm sha')
output={'verification':'PASS_AUDIT_ACCOUNTING_ONLY','D_NO_reconciled':95,'group_count':len(g),'singletons':summary['group_singletons'],'edges':len(e),'distinct_registered_papers':len(s),'cross_group_edges':sum(map(len,adj.values())),'cross_group_cycles':0,'original_workbook_sha256':summary['source_original_sha256'],'normative_catalogue_sha256':summary['source_normative_sha256'],'pass04_classification_sha256':summary['source_pass04_sha256'],'artefacts_sha256':{name:sha(path) for name,path in files.items()},'scope_limit':'This verifies integrity and accounting; it does not prove independent paper methodology, per-D implementation, playbook ownership or architectural admission.'}
(H/'PASS05_VERIFICATION.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
print(json.dumps(output,indent=2))
