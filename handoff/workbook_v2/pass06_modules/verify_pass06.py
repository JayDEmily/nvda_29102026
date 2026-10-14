#!/usr/bin/env python3
"""Pass 06 Workbook V2 static source preservation and module allocation proof.

Uses only Python's standard library; does not modify the workbook.
"""
from __future__ import annotations
import csv,hashlib,json,re
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[3]
V2=ROOT/'handoff/workbook_v2'
AUD=V2/'reviews/excluded_95_provenance_20261014'
HERE=Path(__file__).resolve().parent
BASE=V2/'NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS04.xlsx'
NEW=V2/'NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS06.xlsx'
X='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def rows_csv(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def sheet_snap(z,idx):
    root=ET.fromstring(z.read(f'xl/worksheets/sheet{idx}.xml'))
    cells={}
    for c in root.findall(f'.//{X}sheetData/{X}row/{X}c'):
        v=c.find(f'{X}v'); f=c.find(f'{X}f'); inline=c.find(f'{X}is')
        cells[c.attrib['r']]=(c.get('t'),c.get('s'),v.text if v is not None else None,
            f.text if f is not None else None, tuple(t.text or '' for t in inline.iter() if t.tag.endswith('}t')) if inline is not None else None)
    merges=tuple(sorted(e.get('ref') for e in root.findall(f'.//{X}mergeCells/{X}mergeCell')))
    links=tuple(sorted((e.get('ref'),e.get('location'),e.get('display')) for e in root.findall(f'.//{X}hyperlinks/{X}hyperlink')))
    cols=tuple(sorted(tuple(sorted(c.attrib.items())) for c in root.findall(f'.//{X}cols/{X}col')))
    rowdefs=tuple((r.get('r'),r.get('ht'),r.get('customHeight')) for r in root.findall(f'.//{X}sheetData/{X}row'))
    return cells,merges,links,cols,rowdefs

def sheet_values(z,i):
    root=ET.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'))
    ss=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        sr=ET.fromstring(z.read('xl/sharedStrings.xml'))
        ss=[''.join(t.text or '' for t in si.iter(f'{X}t')) for si in sr.findall(f'{X}si')]
    values={}
    for c in root.findall(f'.//{X}sheetData/{X}row/{X}c'):
        v=c.find(f'{X}v'); inline=c.find(f'{X}is')
        if v is not None:
            values[c.get('r')]=ss[int(v.text)] if c.get('t')=='s' else v.text
        elif inline is not None:
            values[c.get('r')]=''.join(t.text or '' for t in inline.iter(f'{X}t'))
    return values

def main():
    gr=rows_csv(AUD/'NVDA_EXCLUDED_95_PROPOSED_GROUPS.csv')
    rr=rows_csv(AUD/'NVDA_EXCLUDED_95_PROVENANCE_RESPONSIBILITY_AUDIT.csv')
    assert len(gr)==30 and len(rr)==95
    gid={g['Group_ID']:f'M{i+2:02d}' for i,g in enumerate(gr)}
    mapping={r['D_ID']:gid[r['Proposed_Responsibility_Group_ID']] for r in rr}
    assert len(mapping)==95 and len(set(mapping))==95 and sorted(gid.values())==[f'M{i:02d}' for i in range(2,32)]
    assert all(set(g['D_IDs'].split(';'))=={r['D_ID'] for r in rr if gid[r['Proposed_Responsibility_Group_ID']]==gid[g['Group_ID']]} for g in gr)
    edges=[(r['D_ID'],mapping[r['D_ID']],d,mapping[d]) for r in rr for d in r['Derived_Dependencies'].split(';') if d in mapping and mapping[d]!=mapping[r['D_ID']]]
    assert len(edges)==107 and len({(a,b) for _,a,__,b in edges})==67
    with ZipFile(BASE) as a, ZipFile(NEW) as b:
        sheetlist=ET.fromstring(b.read('xl/workbook.xml')).find(f'{X}sheets')
        names=[s.attrib['name'] for s in sheetlist]
        expected=['Evidence Audit','Source Register','Method & Legend','Summary','Raw Signals','Derived Signals','Addendum Evidence Audit','00_Guardrails & Method','M01-1 Derived Raw','M02-M31 Module Register','M02-M31 Signal Allocation']+[f'M{i:02d}' for i in range(2,32)]
        assert names==expected, (names,expected)
        for i in list(range(1,8))+[9]:
            assert sheet_snap(a,i)==sheet_snap(b,i),f'Pre-existing worksheet {i} mutated'
        old_guide,new_guide=sheet_values(a,8),sheet_values(b,8)
        assert all(new_guide.get(k)==v for k,v in old_guide.items()),'Changed existing guardrail'
        assert [new_guide.get(f'A{i}') for i in range(60,66)]==[f'M-{i:03d}' for i in range(1,7)]
        reg=sheet_values(b,10)
        for n,g in enumerate(gr,start=5):
            assert reg.get(f'A{n}')==gid[g['Group_ID']]
            assert reg.get(f'B{n}')==g['Group_ID']
            assert reg.get(f'E{n}')==g['D_IDs']
            assert int(reg.get(f'D{n}'))==int(g['Count'])
        alloc=sheet_values(b,11)
        alloc_rows={}
        for n in range(5,100):
            d=alloc.get(f'A{n}')
            assert re.fullmatch(r'D\d{3}',d or ''),(n,d)
            assert d not in alloc_rows
            alloc_rows[d]=alloc.get(f'C{n}')
        assert alloc_rows==mapping, '95-row allocation mismatch'
        for i,g in enumerate(gr,start=12):
            sh=sheet_values(b,i)
            observed=[sh.get(f'A{j}') for j in range(5,5+int(g['Count']))]
            assert set(observed)==set(g['D_IDs'].split(';')),(gid[g['Group_ID']],observed)
            assert sh.get('A1','').startswith(gid[g['Group_ID']]+' —')
        # The original M01-1 result remains 114 unique D entries.
        m01=sheet_values(b,9)
        prior_m01=sheet_values(a,9)
        assert m01==prior_m01
        m01_ids=[m01.get(f'A{i}') for i in range(6,120)]
        assert len(set(m01_ids))==114 and not set(m01_ids)&set(mapping)
    register=HERE/'PASS06_30_MODULE_REGISTER.csv'
    with register.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['Module_ID_Working','Pass05_Group_ID','Responsibility','D_IDs','D_Count','Status'])
        for g in gr:w.writerow([gid[g['Group_ID']],g['Group_ID'],g['Proposed_Responsibility_Group'],g['D_IDs'],g['Count'],'WORKBOOK_DESIGN_ONLY'])
    cross=HERE/'PASS06_107_CROSS_MODULE_D_REFERENCES.csv'
    with cross.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['Consumer_D','Consumer_Working_Module','Input_D','Input_Working_Module','Resolution'])
        for e in edges:w.writerow(list(e)+['FUTURE_LOCAL_DUPLICATION_AND_DEPENDENCY_MIGRATION_NOT_IMPLEMENTED'])
    allocation=HERE/'PASS06_95_D_MODULE_ALLOCATIONS.csv'
    with allocation.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['D_ID','Working_Module','Pass05_Group','Source_V1_Locator','Normative_CSV_Locator'])
        for r in sorted(rr,key=lambda x:int(x['D_ID'][1:])):
            w.writerow([r['D_ID'],mapping[r['D_ID']],r['Proposed_Responsibility_Group_ID'],r['Source_V1_Locator'],r['Normative_CSV_Locator']])
    result={'status':'PASS_STATIC_WORKBOOK_CLASSIFICATION_ONLY','base_git_commit':'8dd4a6b86b0158f7c0dba18acea44292e5638eaa','input_workbook_sha256':sha(BASE),'output_workbook_sha256':sha(NEW),'modules':len(gr),'downstream_D_count':len(rr),'unchanged_original_source_sheets':7,'unchanged_prior_M01_1_sheet':True,'unchanged_prior_00_rule_cell_values':True,'preexisting_00_rules_preserved':True,'new_00_rules':6,'registered_proposed_module_sheets':30,'cross_module_direct_D_references':len(edges),'cross_module_distinct_directed_pairs':len({(a,b) for _,a,__,b in edges}),'production_code_modified':False,'production_allocation_status':'NOT_ADMITTED'}
    (HERE/'PASS06_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
