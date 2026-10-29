"""Independent raw identity/representation pair and exact rehashed corruption probes."""
from direct_review import *
import json

root=BASE/'stores'
raw=r.create_owner(durability_port=create_sqlite_persistence(str(root/'raw.sqlite'),create=False))
previous=f.create_owner(admission=f.OwnerAdmissionV1('M02',OLD),raw_projection_reader=raw.reads,definitions=(),parameter_sets=(),input_selection_policies=(),unit_conventions=(),raw_projection_mappings=(),storage=f.SQLiteStorageV1(str(root/'old.sqlite'),False),utc_now=lambda:T+timedelta(seconds=100))
ratio=f.create_ratio_owner(admission=f.OwnerAdmissionV1('M02',NEW),predecessor_reader=previous.reads,definitions=(),parameter_sets=(),storage=f.SQLiteStorageV1(str(root/'ratio.sqlite'),False),utc_now=lambda:T+timedelta(seconds=100))
old_mid=previous.materialise(old_request('D011'))
old_spread=previous.materialise(old_request('D012'))
source=raw.reads.get_raw_observation_occurrence(r.observation_occurrence_id('independent-bid'))
for label,literal,sequence in (('new-identity','100',3),('new-representation','100.00',4)):
    raw.commands.admit_raw_observation_occurrence(replace(source,observation_occurrence_id=r.observation_occurrence_id(label),native_record={'quote':{'bid':Decimal(literal)}},received_ts_utc=T,source_timestamp_raw='2026-10-16T01:00:00Z',ingestion_sequence=sequence))
    mid=previous.materialise(old_request('D011'))
    spread=previous.materialise(old_request('D012'))
    assert mid is not None and spread is not None
    before=history(ratio.reads)
    assert ratio.materialise(ratio_request(mid,old_spread)) is None
    assert history(ratio.reads)==before
    result=ratio.materialise(ratio_request(mid,spread))
    assert result is not None and result.result==f.ExactRatioV1(200,101)
    assert result.predecessor_evidence[0].occurrence.raw_input_lineage[0].canonical_value.as_tuple()==Decimal(literal).as_tuple()
    assert previous.reads.get_derived_occurrence(old_mid.derived_occurrence_id)==old_mid
    assert ratio.reads.get_derived_occurrence(result.derived_occurrence_id)==result
    print('PASS lawful one-sided '+label+' refusal + compatible full new pair + retained old reads')

# Original version3 admission still yields Decimal D011 and rejects D012/D013.
original='3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233'
legacy=f.create_owner(admission=f.OwnerAdmissionV1('M02',original),raw_projection_reader=raw.reads,definitions=(DEFS[0],),parameter_sets=(PARAMS[0],),input_selection_policies=(POLICIES[0],),unit_conventions=(UNITS[0],),raw_projection_mappings=MAPS[:2],storage=f.SQLiteStorageV1(str(root/'original.sqlite'),True),utc_now=lambda:T+timedelta(seconds=100))
legacy_fact=legacy.materialise(old_request('D011'))
assert type(legacy_fact.result) is Decimal
legacy_read=f.create_reader(admission=f.OwnerAdmissionV1('M02',original),storage=f.SQLiteReadStorageV1(str(root/'original.sqlite')))
assert legacy_read.get_derived_occurrence(legacy_fact.derived_occurrence_id)==legacy_fact
assert legacy.materialise(old_request('D012')) is None
assert legacy.materialise(replace(old_request('D011'),derived_signal_id='D013')) is None
print('PASS original version3 D011 Decimal fresh readonly; old factory D012/D013 refusal')

# Backup after operations terminate; only the disposable clone is corrupted.
corrupt=BASE/'corrupt.sqlite'
with sqlite3.connect(root/'ratio.sqlite') as source_db,sqlite3.connect(corrupt) as destination:
    source_db.backup(destination)
with sqlite3.connect(corrupt) as connection:
    triggers=connection.execute("SELECT name,sql FROM sqlite_schema WHERE type='trigger'").fetchall()
    for name,_ in triggers: connection.execute('DROP TRIGGER "'+name+'"')
    old_id,payload,logical=connection.execute('SELECT derived_occurrence_id,payload,logical_identity_payload FROM mmt_ratio_occurrence_v1 LIMIT 1').fetchone()
    document,identity=json.loads(payload),json.loads(logical)
    for item in (document,identity): item['predecessor_evidence'][0]['occurrence']['result']={'kind':'decimal','sign':0,'digits':'999','exponent':0}
    document['result']={'kind':'exact_ratio','numerator':'200','denominator':'999'}
    wire=lambda item:json.dumps(item,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False).encode()
    logical=wire(identity); digest=hashlib.sha256(logical).hexdigest()
    document['derived_occurrence_id']='mmtr1:'+digest
    payload=wire(document)
    connection.execute('UPDATE mmt_ratio_occurrence_v1 SET derived_occurrence_id=?,payload=?,content_sha256=?,logical_identity_payload=?,logical_identity_sha256=? WHERE derived_occurrence_id=?',(document['derived_occurrence_id'],payload,hashlib.sha256(payload).hexdigest(),logical,digest,old_id))
    for _,sql in triggers: connection.execute(sql)
try:
    f.create_ratio_reader(admission=f.OwnerAdmissionV1('M02',NEW),storage=f.SQLiteReadStorageV1(str(corrupt)))
except f.PersistenceFailureV1 as exc:
    assert exc.outcome_uncertain is False
    print('PASS independent fully rehashed outer200/999 + forged old999 rejected by readonly recovery')
else:
    raise AssertionError('forged nested predecessor equation accepted')
