from pathlib import Path
import csv, json, collections, re, hashlib
from zipfile import ZipFile
from xml.etree import ElementTree as ET
root=Path(__file__).resolve().parents[3]
base=root/'handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS06.xlsx'
new=root/'handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS08.xlsx'
X='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
def names(z):return [s.attrib['name'] for s in ET.fromstring(z.read('xl/workbook.xml')).find(X+'sheets')]
def cells(z,i):
 ss=[]
 if 'xl/sharedStrings.xml' in z.namelist():
  r=ET.fromstring(z.read('xl/sharedStrings.xml'))
  ss=[''.join(t.text or '' for t in si.iter(X+'t')) for si in r.findall(X+'si')]
 r=ET.fromstring(z.read(f'xl/worksheets/sheet{i}.xml')); data={}
 for c in r.findall(f'.//{X}sheetData/{X}row/{X}c'):
  v=c.find(X+'v'); inline=c.find(X+'is'); f=c.find(X+'f')
  value=ss[int(v.text)] if v is not None and c.get('t')=='s' else v.text if v is not None else ''.join(t.text or '' for t in inline.iter(X+'t')) if inline is not None else None
  data[c.get('r')]=(value,f.text if f is not None else None)
 return data
with ZipFile(base) as a, ZipFile(new) as b:
 sa,sb=names(a),names(b)
 assert sa==sb,len(sb)
 diffs=[]
 entries={}
 for i,name in enumerate(sb,1):
  x,y=cells(a,i),cells(b,i)
  entries[name]=y
  for addr in set(x)|set(y):
   if x.get(addr)!=y.get(addr):diffs.append((name,addr,x.get(addr),y.get(addr)))
 allowed={(name,'H4') for name in [f'M{i:02d}' for i in range(2,32)]}
 allowed|={('00_Guardrails & Method',r) for r in ['C63','E63','C64','E64','C65','E65']}
 allowed|={('M02-M31 Module Register','A2'),('M02-M31 Module Register','H4'),('M02-M31 Signal Allocation','A2'),('M02-M31 Signal Allocation','K4')}
 assert len(allowed)==40
 assert {(a,c) for a,c,_,_ in diffs}==allowed,(len(diffs),set((a,c) for a,c,_,_ in diffs)^allowed)
 # Original seven source worksheets and M01-1 unchanged cell values/formulas
 assert not any(name in sa[:7]+['M01-1 Derived Raw'] for name,addr,old,now in diffs)
 source_ids=[entries['Derived Signals'].get(f'A{r}',(None,None))[0] for r in range(5,214)]
 foundation=[entries['M01-1 Derived Raw'].get(f'A{r}',(None,None))[0] for r in range(6,120)]
 modules=[]
 for n in range(2,32):
  m=f'M{n:02d}'
  for r in range(5,50):
   val=entries[m].get(f'A{r}',(None,None))[0]
   if re.fullmatch(r'D\d{3}',val or ''):modules.append((val,m))
 assert len(source_ids)==209 and len(set(source_ids))==209
 assert len(foundation)==114 and len(set(foundation))==114
 assert len(modules)==95 and len({d for d,m in modules})==95
 assert set(foundation).isdisjoint({d for d,m in modules})
 assert set(foundation)|{d for d,m in modules}==set(source_ids)
 assert all('NOT a runtime dependency' in entries[f'M{n:02d}']['H4'][0] for n in range(2,32))
 assert 'NOT runtime dependency' in entries['M02-M31 Signal Allocation']['K4'][0]
 assert 'no peer runtime dependencies' in entries['M02-M31 Module Register']['A2'][0]
 assert 'no peer' in entries['00_Guardrails & Method']['C63'][0].lower() or 'no peer' in entries['00_Guardrails & Method']['C64'][0].lower()
 old_source_sha=hashlib.sha256((root/'implementation/authority/source_signal_catalogue/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx').read_bytes()).hexdigest()
 out={'status':'PASS_STATIC_WORKBOOK_DESIGN_CLARIFICATION','input':str(base.relative_to(root)),'output':str(new.relative_to(root)),'changed_cells':len(diffs),'allowed_exact_cell_differences':len(allowed),'sheet_count':len(sa),'original_seven_cells_preserved':True,'M01_1_unchanged':True,'v1_source_sha256':old_source_sha,'D_total':len(source_ids),'M01_1_signals':len(foundation),'M02_M31_signals':len(modules),'module_count':30,'runtime_module_independence_proven':False}
 print(json.dumps(out,indent=2))
 (root/'handoff/workbook_v2/pass08_independence_clarification/PASS08_WORKBOOK_READBACK.json').write_text(json.dumps(out,indent=2)+'\n')
