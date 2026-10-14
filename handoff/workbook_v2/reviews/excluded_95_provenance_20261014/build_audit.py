#!/usr/bin/env python3
"""Deterministic read-only provenance crosswalk for Pass04 95 excluded D rows.

Reads exact original reference workbook via stdlib XML (no mutating source), effective
M01 normative CSV and Pass04 eligibility CSV; writes review CSV/JSON/XLSX only.
"""
from __future__ import annotations
import csv,hashlib,json,re,sys,zipfile
import xml.etree.ElementTree as ET
from collections import Counter,defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(HERE))
from group_plan import GROUPS
from artifact_tool import Workbook,SpreadsheetFile

AUTH=ROOT/'handoff/m01_completion/authority'
ORIGINAL=AUTH/'NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx'
NORM=AUTH/'NVDA_DERIVED_SIGNAL_CATALOGUE.csv'
PASS04=ROOT/'handoff/workbook_v2/reviews/m01_1_boundary_20261014/M01_1_FULL_209_ROW_ELIGIBILITY_REVIEW.csv'
EXPECTED={'original':'519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae',
          'norm':'26c5486d1a4c7ff68025c7ce2d7e6847a7798759b847a716c942fd05345f3803'}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read_csv(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def parse_workbook(path):
 n='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
 q='{'+n+'}'; relid='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
 out={}
 with zipfile.ZipFile(path) as z:
  sstr=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   root=ET.fromstring(z.read('xl/sharedStrings.xml'))
   sstr=[''.join(t.text or '' for t in e.iter(q+'t')) for e in root]
  wb=ET.fromstring(z.read('xl/workbook.xml'))
  relationships=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
  rel={e.get('Id'):e.get('Target') for e in relationships}
  for s in wb.find(q+'sheets'):
   name=s.get('name'); dest=rel[s.get(relid)].lstrip('/')
   if not dest.startswith('xl/'):dest='xl/'+dest
   tree=ET.fromstring(z.read(dest)); rows={}
   for row in tree.findall('.//'+q+'sheetData/'+q+'row'):
    i=int(row.get('r'));cmap={}
    for cell in row.findall(q+'c'):
     c=cell.get('r'); val=cell.find(q+'v'); inline=cell.find(q+'is'); f=cell.find(q+'f')
     if f is not None: v='='+str(f.text or '')
     elif val is not None: v=sstr[int(val.text)] if cell.get('t')=='s' else val.text
     elif inline is not None:v=''.join(t.text or '' for t in inline.iter(q+'t'))
     else:continue
     cmap[re.sub(r'\d+','',c)]=v
    if cmap:rows[i]=cmap
   out[name]=rows
 return out

def steps_expand(v):
 steps=[]
 for tok in re.split(r'[,;]',v.strip()):
  tok=tok.strip()
  if not tok:continue
  m=re.fullmatch(r'(\d+)(?:\s*[-–]\s*(\d+))?',tok)
  assert m, ('invalid step token',v,tok)
  a=int(m[1]);b=int(m[2] or a)
  assert a<=b<=94
  steps.extend(range(a,b+1))
 assert len(steps)==len(set(steps)),('duplicate step',v)
 return steps

def tokens(v,regex):return set(re.findall(regex,v or ''))

def write_csv(name,rows,fields):
 with (HERE/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def main():
 assert sha(ORIGINAL)==EXPECTED['original'], 'V1 workbook SHA mismatch'
 assert sha(NORM)==EXPECTED['norm'], 'Normative catalogue SHA mismatch'
 workbook=parse_workbook(ORIGINAL)
 raw_derived={v.get('A'):dict(v,row=row) for row,v in workbook['Derived Signals'].items() if re.fullmatch(r'D\d{3}',v.get('A',''))}
 source={v.get('A'):dict(v,row=row) for row,v in workbook['Source Register'].items() if re.fullmatch(r'S\d{2}',v.get('A',''))}
 research={int(v['A']):dict(v,row=row) for row,v in workbook['Evidence Audit'].items() if str(v.get('A','')).isdigit()}
 addendum={int(v['A']):dict(v,row=row) for row,v in workbook['Addendum Evidence Audit'].items() if str(v.get('A','')).isdigit()}
 norm={r['derived_id']:r for r in read_csv(NORM)}
 pass04=read_csv(PASS04);passed={r['D_ID']:r for r in pass04};no=[r for r in pass04 if r['M01_1_Proposed_Eligibility']=='NO']; yes=[r for r in pass04 if r['M01_1_Proposed_Eligibility']=='YES']
 assert len(norm)==len(raw_derived)==len(passed)==209 and len(no)==95 and len(yes)==114
 assert len(research)==80 and len(addendum)==14 and len(source)==62
 ids_expected={f'D{i:03d}' for i in range(1,210)}
 assert set(norm)==set(raw_derived)==set(passed)==ids_expected
 group_by_d={};groups=[]
 for group_id,name,ids,reason,exclusion,users in GROUPS:
  items=ids.split()
  assert all(k not in group_by_d for k in items)
  group_by_d.update({k:group_id for k in items})
  groups.append(dict(Group_ID=group_id,Proposed_Responsibility_Group=name,D_IDs=';'.join(items),Count=len(items),Basis=reason,Exclusions_And_Boundary=exclusion,Potential_Consumers_Status='REQUIRES DOWNSTREAM OWNER EVIDENCE',Consumer_Notes=users,Module_ID_Allocated='NO',Approval_Status='REVIEW_ONLY'))
 assert set(group_by_d)=={r['D_ID'] for r in no}
 source_by_doi={v['F'].strip().lower():sid for sid,v in source.items()}
 assert len(source_by_doi)==62
 ref={};links=[]
 for step,row in research.items():
  doi=row['I'].strip().lower(); assert doi in source_by_doi,(step,doi)
  ref[step]=dict(src=source_by_doi[doi],paper=row['E'],doi=row['I'],url=row['J'],strength=row['D'],proposition=row['C'],title=row['B'],location=row['K'],limits=row['N'],row=row['row'])
 rev=defaultdict(set)
 for id,row in norm.items():
  for pid in tokens(row['derived_dependencies'],r'D\d{3}'):
   assert pid in norm;rev[pid].add(id)
 result=[]; sourceuse=set();edge_count=0
 for entry in no:
  d=entry['D_ID'];row=raw_derived[d];authoritative=norm[d]; st=steps_expand(row.get('L',''))
  citation_ids=sorted({ref[s]['src'] for s in st if s<=80})
  for k in st:
   if k<=80:
    r=ref[k]
    links.append(dict(D_ID=d,Source_D_Excel_Locator=f'Derived Signals!A{row["row"]}:O{row["row"]}',Required_Framework_Step=k,Step_Title=r['title'],Step_Proposition=r['proposition'],Evidence_Strength=r['strength'],Source_ID=r['src'],Paper_Title=r['paper'],DOI=r['doi'],Source_URL=r['url'],Evidence_Audit_Locator=f'Evidence Audit!A{r["row"]}:N{r["row"]}',Academic_Claim_Scope='STEP_PROPOSITION_ONLY',D_Equation_Paper_Derivation_Proven='NO',Source_Limitations=r['limits']))
    sourceuse.add(r['src']);edge_count+=1
   else:
    s=addendum[k];links.append(dict(D_ID=d,Source_D_Excel_Locator=f'Derived Signals!A{row["row"]}:O{row["row"]}',Required_Framework_Step=k,Step_Title=s['D'],Step_Proposition=s['E'],Evidence_Strength=s['G'],Source_ID='ADDENDUM',Paper_Title=s['H'],DOI=s.get('M',''),Source_URL=s.get('N',''),Evidence_Audit_Locator=f'Addendum Evidence Audit!A{s["row"]}:S{s["row"]}',Academic_Claim_Scope='STEP_PROPOSITION_ONLY',D_Equation_Paper_Derivation_Proven='NO',Source_Limitations=s.get('Q','')))
  rd=sorted(rev[d]); downstream_no=[x for x in rd if x in group_by_d];downstream_yes=[x for x in rd if x not in group_by_d]
  groupid=group_by_d[d]
  group=next(g for g in groups if g['Group_ID']==groupid)
  result.append(dict(
   D_ID=d,D_Name=row.get('C',''),Original_Family=row.get('B',''),Proposed_Family_Review=entry.get('Proposed_Family_Review_Only',''),Proposed_Calculation_Class_Review=entry.get('Proposed_Calculation_Class_Review_Only',''),
   Proposed_Responsibility_Group_ID=groupid,Proposed_Responsibility_Group=group['Proposed_Responsibility_Group'],Why_Calculation_Exists_V1=row.get('M',''),Original_Calculation_Concept=row.get('G',''),Normative_Calculation_Concept=authoritative['calculation_concept'],Normative_Kernel=authoritative['kernel_id'],Normative_Parameter_Profiles=authoritative['parameter_profiles'],Normative_Typed_Contexts=authoritative['typed_contexts'],
   M01_1_Exclusion_Code=entry['Exclusion_Code'],M01_1_Exclusion_Explanation=entry['Individual_Assessment'],Group_Assignment_Basis=group['Basis'],
   Raw_Dependencies=authoritative['raw_dependencies'],Derived_Dependencies=authoritative['derived_dependencies'],Direct_D_Downstream_Consumers=';'.join(rd),Direct_No_Downstream_Consumers=';'.join(downstream_no),Direct_Yes_Downstream_Consumers=';'.join(downstream_yes),Direct_Downstream_Consumer_Count=len(rd),
   Workbook_Required_Steps=row.get('L',''),Expanded_Steps=';'.join(map(str,st)),Framework_Evidence_Source_IDs=';'.join(citation_ids),Distinct_Registered_Sources=len(citation_ids),Source_Audit_Link_Type='D->REQUIRED_STEP->REGISTERED_PAPER',Direct_Individual_Equation_Paper_Citation_Status='NOT_ESTABLISHED',
   Source_V1_Locator=f'Derived Signals!A{row["row"]}:O{row["row"]}',Normative_CSV_Locator=entry['Effective_CSV_Locator'],Source_Purpose_Status='WORKBOOK_DECLARED',Formal_Module_Owner='UNALLOCATED',Playbook_Consumers='UNKNOWN_NOT_AUTHORISED',Group_Status='PROPOSED_REVIEW_ONLY',Code_Test_Isolation_Status='NOT_AUDITED_IN_THIS_PASS'))
 fields=list(result[0]);write_csv('NVDA_EXCLUDED_95_PROVENANCE_RESPONSIBILITY_AUDIT.csv',result,fields)
 efields=list(links[0]);write_csv('NVDA_EXCLUDED_95_STEP_SOURCE_EDGES.csv',links,efields)
 gfields=list(groups[0]);write_csv('NVDA_EXCLUDED_95_PROPOSED_GROUPS.csv',groups,gfields)
 counters=Counter(ref[int(e['Required_Framework_Step'])]['strength'] for e in links if int(e['Required_Framework_Step'])<=80)
 source_counts=Counter(e['Source_ID'] for e in links)
 source_rows=[]
 for sid in sorted(sourceuse):
  s=source[sid]
  source_rows.append(dict(Source_ID=sid,Paper_Title=s['B'],Authors=s['C'],Year=s['D'],DOI=s['F'],Source_URL=s['G'],Register_Original_Steps=s['J'],Edges_From_95=source_counts[sid],Source_Register_Locator=f'Source Register!A{s["row"]}:J{s["row"]}',Source_Audit_Claim='FRAMEWORK_SUPPORT_NOT_D_EQUATION_PROOF'))
 sfields=list(source_rows[0]);write_csv('NVDA_EXCLUDED_95_RESEARCH_SOURCES.csv',source_rows,sfields)
 reverse_mult=[r for r in result if r['Direct_Downstream_Consumer_Count']>=2]
 external=[r for r in result if r['Direct_Downstream_Consumer_Count']>=1]
 grp_counts=Counter(row['Proposed_Responsibility_Group_ID'] for row in result)
 missing=[r for r in result if not r['Workbook_Required_Steps']]
 summary=dict(
  source_original_sha256=sha(ORIGINAL),source_normative_sha256=sha(NORM),source_pass04_sha256=sha(PASS04),
  D_universe=209,existing_excluded=95,existing_eligible=114,group_count=len(groups),
  group_singletons=sum(v==1 for v in grp_counts.values()),all_source_D_rows_accounted=len(result),
  total_D_to_framework_step_links=edge_count,unique_framework_steps=len({int(e['Required_Framework_Step']) for e in links}),
  unique_referenced_registered_papers=len(sourceuse),source_register_total=len(source),
  source_evidence_strength_edges=dict(counters),source_step_links_to_addendum=sum(int(e['Required_Framework_Step'])>80 for e in links),
  source_provenance_missing_steps=len(missing),
  signal_with_two_or_more_downstream_D_consumers=len(reverse_mult),signal_with_at_least_one_D_downstream_consumer=len(external),
  individual_D_to_specific_paper_methodological_derivation_verified_count=0,
  grouping_status='REVIEW_ONLY_NOT_MODULE_ALLOCATION',
  academic_proof_note='All linked papers relate to original framework propositions through required steps; do not claim a paper individually derives D calculation, validates its coefficients, establishes alpha, or mandates a module.',
  grouping_method='Each D assigned to one responsibility grouping by effective calculation semantics, context and direct graph; not assigned by source-paper identity or old family.',
 )
 (HERE/'AUDIT_SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
 # Build separate review workbook, not the V2 main research workbook.
 w=Workbook.create()
 def tab(name,header,data,widths=None):
  sheet=w.worksheets.add(name)
  matrix=[header]+[[str(x.get(k,'')) if x.get(k,'') is not None else '' for k in header] for x in data]
  step=100
  for off in range(0,len(matrix),step):
   segment=matrix[off:off+step]
   sheet.get_range_by_indexes(off,0,len(segment),len(header)).values=segment
  top=sheet.get_range_by_indexes(0,0,1,len(header));top.format={'fill':'#18324F','font':{'bold':True,'color':'#FFFFFF'},'row_height':35,'wrap_text':True}
  sheet.freeze_panes.freeze_rows(1)
  if data:
   sheet.tables.add(sheet.get_range_by_indexes(0,0,len(data)+1,len(header)),True,'Table'+re.sub('[^A-Za-z0-9]','',name))
  for j in range(len(header)):
   a=sheet.get_range_by_indexes(0,j,len(matrix),1)
   a.format.column_width=widths[j] if widths and j<len(widths) else (25 if j<4 else 32)
  return sheet
 highlights=[{'Measure':'Excluded D-signals individually mapped','Value':95}, {'Measure':'Proposed responsibility groups (NOT modules)','Value':len(groups)}, {'Measure':'Single-D responsibility groups (NOT modules)','Value':summary['group_singletons']}, {'Measure':'D-to-research-step-to-source edges','Value':len(links)},{'Measure':'Distinct framework steps cited','Value':summary['unique_framework_steps']},{'Measure':'Registered papers linked via steps','Value':len(sourceuse)},{'Measure':'Per-D paper derivations proved','Value':0},{'Measure':'Formal software modules allocated','Value':0},{'Measure':'V2 workbook modified','Value':'NO'}, {'Measure':'Actual playbook assignments established','Value':'NO'}]
 tab('Audit Summary',list(highlights[0]),highlights,[50,40])
 tab('95 D Review',fields,result)
 tab('30 Groups',gfields,groups)
 tab('Step Source Links',efields,links)
 tab('Academic Sources',sfields,source_rows)
 output=HERE/'NVDA_EXCLUDED_95_PROVENANCE_REVIEW_20261014.xlsx'
 SpreadsheetFile.export_xlsx(w).save(str(output))
 print(json.dumps(summary,indent=2));print('XLSX:',output)

if __name__=='__main__':main()
