"""Readback verification of Pass 04 and full proposed D-signal eligibility register."""
from pathlib import Path
import hashlib,csv,json,re
from zipfile import ZipFile
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
OLDER=ROOT/'handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS02.xlsx'
CURRENT=ROOT/'handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS04.xlsx'
CSV=HERE/'M01_1_FULL_209_ROW_ELIGIBILITY_REVIEW.csv'
CAT=ROOT/'handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv'
SUM=HERE/'M01_1_AUDIT_SUMMARY.json'
S='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
R='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'

def read(path):
    with ZipFile(path) as z:
        wb=ET.fromstring(z.read('xl/workbook.xml'))
        rel=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        refs={node.get('Id'):node.get('Target') for node in rel}
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            strings=[''.join(t.text or '' for t in si.iter(S+'t')) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        out={}
        for sh in wb.iter(S+'sheet'):
            target=refs[sh.get(R)].lstrip('/')
            if not target.startswith('xl/'):target='xl/'+target
            node=ET.fromstring(z.read(target))
            cells={}; rows=[];cols=[]
            for row in node.iter(S+'row'):
                rows.append(dict(row.attrib))
                for c in row.findall(S+'c'):
                    v=c.find(S+'v');f=c.find(S+'f');inline=c.find(S+'is')
                    val=(strings[int(v.text)] if c.get('t')=='s' and v is not None else
                         ''.join(t.text or '' for t in inline.iter(S+'t')) if inline is not None else
                         v.text if v is not None else None)
                    if val is not None or f is not None:cells[c.get('r')]=(val,f.text if f is not None else None)
            for c in node.iter(S+'col'):cols.append(dict(c.attrib))
            merges=sorted(m.get('ref') for m in node.iter(S+'mergeCell'))
            links=sorted((m.get('ref'),m.get('location'),m.get('display'),m.get(R)) for m in node.iter(S+'hyperlink'))
            out[sh.get('name')]={'cells':cells,'rows':rows,'cols':cols,'merges':merges,'links':links}
        return out

old=read(OLDER);new=read(CURRENT)
assert len(old)==8,list(old)
assert list(new)==list(old)+['M01-1 Derived Raw'],(list(new),list(old))
for name in old:
    assert old[name]==new[name],('previous sheet changed',name)
assert '01_Raw Signals' not in new and '02_Derived Signal Index' not in new
with CSV.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
with CAT.open(newline='',encoding='utf-8-sig') as f: orig=list(csv.DictReader(f))
assert len(rows)==len(orig)==209
by={r['D_ID']:r for r in rows}
assert [r['D_ID'] for r in rows]==[r['derived_id'] for r in orig]==[f'D{i:03}' for i in range(1,210)]
assert {r['M01_1_Proposed_Eligibility'] for r in rows}=={'YES','NO'}
assert len({r['D_ID'] for r in rows})==209
q=[r for r in rows if r['M01_1_Proposed_Eligibility']=='YES']; n=[r for r in rows if r['M01_1_Proposed_Eligibility']=='NO']
assert len(q)==114 and len(n)==95
for index,(r,c) in enumerate(zip(rows,orig),start=1):
    assert r['Raw_Dependencies_Effective']==c['raw_dependencies'],r['D_ID']
    assert r['Derived_Dependencies_Effective']==c['derived_dependencies'],r['D_ID']
    assert r['Concept_Effective']==c['calculation_concept'],r['D_ID']
    assert r['Kernel_Effective']==c['kernel_id'],r['D_ID']
    assert int(r['Source_Row_V1'])==index+4
    assert r['Effective_CSV_Locator']==f'NVDA_DERIVED_SIGNAL_CATALOGUE.csv:{index+1}'
    assert r['Implementation_And_Independent_Tests']=='NOT_INDIVIDUALLY_VERIFIED_IN_THIS_PASS'
    if r['M01_1_Proposed_Eligibility']=='NO':
        assert r['Exclusion_Code'] and r['Individual_Assessment']
    else:
        assert not r['Exclusion_Code']
        for d in filter(None,c['derived_dependencies'].split(';')):
            assert by[d]['M01_1_Proposed_Eligibility']=='YES',(r['D_ID'],d)
        for raw in filter(None,c['raw_dependencies'].split(';')):
            assert not (205<=int(raw[1:])<=235),(r['D_ID'],raw)

cells=new['M01-1 Derived Raw']['cells']
assert 'REVIEW CANDIDATES ONLY' in cells['A1'][0]
assert '114 of 209' in cells['A2'][0]
assert cells['A5'][0]=='D-ID'
ids=[cells[f'A{j}'][0] for j in range(6,120)]
assert ids==[r['D_ID'] for r in q], ('new sheet is not exactly proposed qualifying rows',ids)
assert len(set(ids))==114
for i,r in enumerate(q,6):
    assert cells[f'B{i}'][0]==r['Signal_Name']
    assert cells[f'C{i}'][0]==r['Original_Family_V1']
    assert cells[f'F{i}'][0]==r['Raw_Dependencies_Effective'] if r['Raw_Dependencies_Effective'] else f'F{i}' not in cells
    assert cells[f'G{i}'][0]==r['Derived_Dependencies_Effective'] if r['Derived_Dependencies_Effective'] else f'G{i}' not in cells
    assert cells[f'H{i}'][0]==r['Kernel_Effective']
    assert cells[f'K{i}'][0]==r['Concept_Effective']
    assert cells[f'Q{i}'][0]==r['V1_Locator']
assert not any(re.fullmatch(r'A1(2[0-9]|[3-9]\d)|A[2-9]\d\d',key) for key in cells)
summary=json.loads(SUM.read_text())
assert summary['proposed_yes']==len(q) and summary['proposed_no']==len(n)
assert summary['pass04_sha256']==hashlib.sha256(CURRENT.read_bytes()).hexdigest()
assert summary['row_audit_csv_sha256']==hashlib.sha256(CSV.read_bytes()).hexdigest()
assert summary['original_v1_sha256']=='519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae'
res={'original_eight_sheets_unchanged':True,'full_row_classification':209,'candidate_only_tab':len(ids),'unadmitted':len(n),
     'qualifying_to_nonqualifying_D_edges':0,'qualifying_to_account_position_order_R_edges':0,
     'proposed_module_id_only':True,'source_and_sheet_readback':'PASS',
     'output_sha256':hashlib.sha256(CURRENT.read_bytes()).hexdigest(),
     'audit_csv_sha256':hashlib.sha256(CSV.read_bytes()).hexdigest()}
(HERE/'PASS04_VERIFICATION.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
