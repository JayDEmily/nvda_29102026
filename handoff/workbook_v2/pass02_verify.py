"""Independent structural/readback check for additive V2 00 classification contract only."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import csv, hashlib, json, re

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
V1=ROOT/'handoff/m01_completion/authority/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx'
V2_01=HERE/'NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS01.xlsx'
V2_02=HERE/'NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS02.xlsx'
AUDIT=HERE/'reviews/derived_family_audit_20261014/NVDA_DERIVED_FAMILY_FULL_209_ROW_AUDIT_20261014.csv'
PREVIEW=HERE/'reviews/derived_family_audit_20261014/NVDA_FUTURE_02_TWO_FIELDS_209_ROW_PREVIEW_20261014.csv'
S='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
R='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'

def read(path):
 with ZipFile(path) as z:
  rel=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
  paths={e.get('Id'):e.get('Target') for e in rel}
  wb=ET.fromstring(z.read('xl/workbook.xml'))
  strings=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   strings=[''.join(t.text or '' for t in si.iter(S+'t')) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
  out={}
  for sh in wb.iter(S+'sheet'):
   target=paths[sh.get(R)].lstrip('/')
   if not target.startswith('xl/'):target='xl/'+target
   e=ET.fromstring(z.read(target))
   cells={}
   rows=[];cols=[]
   for row in e.iter(S+'row'):
    rows.append(dict(row.attrib))
    for c in row.findall(S+'c'):
     v=c.find(S+'v');f=c.find(S+'f');i=c.find(S+'is')
     val=(strings[int(v.text)] if c.get('t')=='s' and v is not None else
          ''.join(x.text or '' for x in i.iter(S+'t')) if i is not None else v.text if v is not None else None)
     if val is not None or f is not None: cells[c.get('r')]=(val,f.text if f is not None else None)
   for col in e.iter(S+'col'):cols.append(dict(col.attrib))
   merges=sorted(x.get('ref') for x in e.iter(S+'mergeCell'))
   hyperlinks=sorted((x.get('ref'),x.get('location'),x.get('display'),x.get(R)) for x in e.iter(S+'hyperlink'))
   out[sh.get('name')]={'cells':cells,'row_attrs':rows,'col_attrs':cols,'merges':merges,'hyperlinks':hyperlinks}
  return out

assert hashlib.sha256(V1.read_bytes()).hexdigest()=='519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae'
a,b,c=read(V1),read(V2_01),read(V2_02)
assert len(a)==7
assert list(b)==list(a)+['00_Guardrails & Method']
assert list(c)==list(b)
for name in a:
 assert a[name]==b[name]==c[name], ('source worksheet mutation',name)
assert '01_Raw Signals' not in c and '02_Derived Signal Index' not in c
p=b['00_Guardrails & Method']['cells'];q=c['00_Guardrails & Method']['cells']
for k,v in p.items():
 if k not in ('A1','A2'): assert q.get(k)==v,('altered previous 00 cell',k)
newkeys=set(q)-set(p)
assert all(re.fullmatch(r'[A-E](50|5[1-6])', k) for k in newkeys),('unexpected appended 00 cell',newkeys)
old_ids={k:v[0] for k,v in p.items() if re.fullmatch(r'A\d+',k) and re.fullmatch(r'[GRDV]-\d{3}',str(v[0]))}
new_ids={k:v[0] for k,v in q.items() if re.fullmatch(r'A\d+',k) and re.fullmatch(r'[GRDVC]-\d{3}',str(v[0]))}
assert len(old_ids)==35 and len(new_ids)==41,(len(old_ids),len(new_ids))
assert set(old_ids.items()).issubset(new_ids.items())
assert {q[f'A{r}'][0] for r in range(51,57)}=={f'C-{i:03}' for i in range(1,7)}
assert 'Family' in q['C51'][0] and 'Calculation class' in q['C51'][0]
assert 'UNASSESSED' in q['C54'][0]
with AUDIT.open(encoding='utf-8-sig',newline='') as f: origin=list(csv.DictReader(f))
with PREVIEW.open(encoding='utf-8-sig',newline='') as f: future=list(csv.DictReader(f))
assert len(origin)==len(future)==209
for idx,(a_row,f_row) in enumerate(zip(origin,future),1):
 assert a_row['D_ID']==f_row['D_ID']==f'D{idx:03}'
 assert a_row['Original_Family']==f_row['Family']==f_row['Original_Family_V1']
 assert a_row['Proposed_Family']==f_row['Proposed_Family_Review_Only']
 assert int(a_row['Original_Excel_Row'])==int(f_row['V1_Excel_Row'])==idx+4
 assert f_row['Calculation_class']=='' and f_row['Calculation_class_Status']=='UNASSESSED'
 assert f_row['Family_Status']=='ORIGINAL_V1_NOT_RECLASSIFIED'
assert len({r['D_ID'] for r in future})==209

result={'source_workbook_sha256':hashlib.sha256(V1.read_bytes()).hexdigest(),
        'incoming_pass01_sha256':hashlib.sha256(V2_01.read_bytes()).hexdigest(),
        'pass02_sha256':hashlib.sha256(V2_02.read_bytes()).hexdigest(),
        'original_worksheets_readback':'PASS_7_OF_7_CONTENT_AND_STRUCTURE',
        'previous_pass01_guardrails_preserved':35,
        'new_classification_rules':6,
        'total_guardrails':41,
        'original_audit_rows_retained':209,
        'preview_rows':209,
        'family_column_V1_values_retained':209,
        'calculation_class_assignments_unassessed':209,
        'family_proposal_status':'REVIEW_NOT_ADOPTED',
        'future_01_02_sheets_absent':True,
        'report_present_in_committed_input_tree':(HERE/'reviews/derived_family_audit_20261014/NVDA_DERIVED_FAMILY_RECOMMENDATION_20261014.md').is_file()}
assert result['report_present_in_committed_input_tree']
(HERE/'PASS02_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
