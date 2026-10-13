"""Independent OOXML source-versus-V2 worksheet readback; no workbook edits.
Usage: python handoff/workbook_v2/pass01_verify.py
Fails closed on original cell, formula, merge, hyperlink or worksheet identity changes.
"""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import hashlib, json, re, csv, collections

ROOT=Path(__file__).resolve().parents[2]
DIR=Path(__file__).resolve().parent
NAME='NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx'
V1=ROOT/'handoff/m01_completion/authority'/NAME
V2=DIR/'NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS01.xlsx'
S='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
P='http://schemas.openxmlformats.org/package/2006/relationships'
T=lambda tag:'{%s}%s'%(S,tag)


def workbook_extract(path):
 with ZipFile(path) as zip:
  rels=ET.fromstring(zip.read('xl/_rels/workbook.xml.rels'))
  links={x.attrib['Id']:x.attrib['Target'] for x in rels}
  names=ET.fromstring(zip.read('xl/workbook.xml'))
  ss=[]
  if 'xl/sharedStrings.xml' in zip.namelist():
   for si in ET.fromstring(zip.read('xl/sharedStrings.xml')):
    ss.append(''.join(t.text or '' for t in si.iter(T('t'))))
  ret={}
  for item in names.iter(T('sheet')):
   name=item.attrib['name']; target=links[item.attrib['{%s}id'%R]].lstrip('/')
   target=target if target.startswith('xl/') else 'xl/'+target
   rt=ET.fromstring(zip.read(target))
   cells={}; row_attrs={}; col_attrs=[]
   for row in rt.iter(T('row')):
    rowno=int(row.attrib['r']); row_attrs[rowno]={key:val for key,val in row.attrib.items() if key!='r'}
    for c in row.findall(T('c')):
     t=c.attrib.get('t','n'); v=c.find(T('v')); f=c.find(T('f')); inline=c.find(T('is'))
     val=ss[int(v.text)] if t=='s' and v is not None else ''.join(x.text or '' for x in inline.iter(T('t'))) if t=='inlineStr' and inline is not None else v.text if v is not None else None
     formula=f.text if f is not None else None
     if val is not None or formula is not None:
      cells[c.attrib['r']]={'value':val,'formula':formula, 'kind':'string' if t in ('s','inlineStr','str') else t}
   merges=sorted(x.attrib.get('ref') for x in rt.iter(T('mergeCell')))
   hyperlinks=sorted((x.attrib.get('ref'),x.attrib.get('location'),x.attrib.get('display'),x.attrib.get('{%s}id'%R)) for x in rt.iter(T('hyperlink')))
   for col in rt.iter(T('col')):col_attrs.append({k:v for k,v in col.attrib.items()})
   ret[name]={'cells':cells,'row_count':len(row_attrs),'row_attrs':row_attrs,'merges':merges,'hyperlinks':hyperlinks,'columns':col_attrs,'xml':target}
  return ret

source=workbook_extract(V1); output=workbook_extract(V2)
expected=list(source)
assert len(expected)==7,expected
assert list(output)==expected+['00_Guardrails & Method'], (list(output),expected)
problems=[];readback={};diff_attrs={}
for name in expected:
 a,b=source[name],output[name]
 added=set(b['cells'])-set(a['cells']); missing=set(a['cells'])-set(b['cells'])
 changed=[key for key in a['cells'] if key in b['cells'] and a['cells'][key]!=b['cells'][key]]
 discrepancies=[]
 if added:discrepancies.append(('added',sorted(added)[:20],len(added)))
 if missing:discrepancies.append(('missing',sorted(missing)[:20],len(missing)))
 if changed:discrepancies.append(('changed',[(x,a['cells'][x],b['cells'][x]) for x in changed[:4]],len(changed)))
 for p in ['merges','hyperlinks']:
  if a[p]!=b[p]:discrepancies.append((p,a[p][:10],b[p][:10]))
 if discrepancies:problems.append((name,discrepancies))
 readback[name]={'v1_nonempty_cells':len(a['cells']),'v2_nonempty_cells':len(b['cells']),'cell_difference_count':len(added)+len(missing)+len(changed),'merges_equal':a['merges']==b['merges'],'hyperlinks_equal':a['hyperlinks']==b['hyperlinks']}
 diff_attrs[name]={'original_row_attributes_equal':a['row_attrs']==b['row_attrs'],'original_column_attributes_equal':a['columns']==b['columns'],'v1_merges':len(a['merges']),'v2_merges':len(b['merges']),'v1_hyperlinks':len(a['hyperlinks']),'v2_hyperlinks':len(b['hyperlinks'])}

ids={}
with (DIR/'PASS01_SOURCE_ROW_DIGESTS.csv').open('w',newline='',encoding='utf-8') as f:
 writer=csv.writer(f)
 writer.writerow(['source_sheet','source_row','signal_id','family','populated_source_cells','source_row_sha256'])
 for name,prefix,total in [('Raw Signals','R',323),('Derived Signals','D',209)]:
  data=source[name]['cells']; recorded=[]
  for row in range(5,5+total):
   ident=data[f'A{row}']['value']; family=data[f'B{row}']['value']
   rowcells={k:data[k] for k in sorted(data) if re.search(str(row)+r'$',k)}
   msg=json.dumps(rowcells,sort_keys=True,ensure_ascii=False,separators=(',',':'))
   writer.writerow([name,row,ident,family,len(rowcells),hashlib.sha256(msg.encode()).hexdigest()])
   recorded.append(ident)
  assert recorded==[f'{prefix}{j:03}' for j in range(1,total+1)],(name,'ID sequence/uniqueness violation')
  ids[name]=recorded

counts={}; families={};states={}
for name in ['Raw Signals','Derived Signals']:
 data=source[name]['cells']; inds=range(5,328) if name=='Raw Signals' else range(5,214)
 counts[name]=sum(1 for row in inds)
 families[name]=dict(collections.Counter(data[f'B{row}']['value'] for row in inds))
 col='W' if name=='Raw Signals' else 'N'
 states[name]=dict(collections.Counter(data[f'{col}{row}']['value'] for row in inds))

new=output['00_Guardrails & Method']
rule_ids=[cell['value'] for k,cell in new['cells'].items() if re.fullmatch('A\\d+',k) and re.fullmatch('[GRDV]-\\d{3}',str(cell['value']))]
assert len(rule_ids)==35 and len(set(rule_ids))==35,(len(rule_ids),len(set(rule_ids)))
for name in ['01_Raw Signals','02_Derived Signal Index']:
 assert name not in output

result={
 'authority':'V1 workbook is reference evidence only; M01 accepted brief/current normative CSV govern implementation',
 'source_file':str(V1.relative_to(ROOT)),
 'source_sha256':hashlib.sha256(V1.read_bytes()).hexdigest(),
 'source_expected_sha256':'519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae',
 'output_file':str(V2.relative_to(ROOT)),
 'output_sha256':hashlib.sha256(V2.read_bytes()).hexdigest(),
 'original_sheets':expected,
 'v2_sheets':list(output),
 'original_sheet_readback':readback,
 'original_structure_diagnostics':diff_attrs,
 'source_populated_cell_count':{x:len(source[x]['cells']) for x in ('Raw Signals','Derived Signals')},
 'source_data_row_count':counts,
 'source_family_counts':{x:len(families[x]) for x in families},
 'source_families':families,
 'source_status_counts':states,
 'original_rows_hashed_to_csv':sum(counts.values()),
 'v2_guardrail_count':len(rule_ids),
 'new_sheet_only':'00_Guardrails & Method',
 'unapproved_01_02_created':False,
 'original_worksheet_semantic_readback':'PASS' if not problems else 'FAIL',
 'problems':problems,
}
(DIR/'PASS01_SOURCE_CENSUS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ['source_sha256','output_sha256','v2_sheets','original_sheet_readback','original_structure_diagnostics','source_populated_cell_count','source_data_row_count','source_family_counts','v2_guardrail_count','original_worksheet_semantic_readback','problems']},indent=2,ensure_ascii=False))
if problems:raise SystemExit('FAIL-CLOSED: original workbook source sheets changed in V2 export')
