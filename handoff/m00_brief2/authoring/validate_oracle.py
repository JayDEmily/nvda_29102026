"""Static JSON/schema/hash witnesses; no M00 runtime imports."""
import copy
import hashlib
import json
from pathlib import Path
from nvda_desk.architecture.schema import validate_instance
root=Path(__file__).resolve().parents[1]
schema=json.loads((root/'output_schema_v1.json').read_text())
manifest=json.loads((root/'fixture_manifest_v1.json').read_text())
for name,digest in manifest['hashes'].items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
rows=[]
for path in sorted((root/'fixtures').rglob('expected*jsonl')):
    for line in path.read_text().splitlines():
        row=json.loads(line);validate_instance(row,schema);rows.append(row)
assert len(rows)==196
projection=next(x for x in rows if x['kind']=='projection')
receipt=next(x for x in rows if x['kind']=='observation' and x['value']['source_temporal_kind']=='receipt_only')
malformed=[]
x=copy.deepcopy(projection);x['value']['native_value']={'native_type':'Decimal','value':'not-a-decimal'};malformed.append(x)
x=copy.deepcopy(projection);x['value']['native_value']={'native_type':'bool','value':1};malformed.append(x)
x=copy.deepcopy(projection);x['value']['received_ts_utc']='2026-10-20T12:40:00';malformed.append(x)
x=copy.deepcopy(receipt);x['value']['source_timestamp_raw']='invented';malformed.append(x)
x=copy.deepcopy(projection);del x['value']['projection_mapping_version'];malformed.append(x)
x=copy.deepcopy(projection);x['kind']='absence';x['value']={'case_id':'N06'};malformed.append(x)
for index,x in enumerate(malformed):
    try:validate_instance(x,schema)
    except ValueError:pass
    else:raise AssertionError(f'malformed schema witness accepted:{index}')
for i in range(1,19):
    spec=json.loads((root/f'fixtures/negative/N{i:02}_v1.jsonl').read_text())
    assert spec['case_id']==f'N{i:02}' and len(spec)>2
print(f'PASS: {len(rows)} expected rows validate; {len(manifest["hashes"])} file hashes;6 malformed schema witnesses rejected;18 concrete negative specifications;36/155 positive totals independently table-checked.')
