import base64,pickle,sys
from datetime import UTC,datetime
from nvda_desk.market_measurement_truth import api as f
reads=f.create_raw_ratio_reader(admission=f.OwnerAdmissionV1('M02',sys.argv[2]),storage=f.SQLiteReadStorageV1(sys.argv[1]))
facts=tuple(reads.get_derived_occurrence(identity) for identity in sys.argv[3:])
assert all(type(x) is f.RawRatioOccurrenceV1 and type(x.result) is f.ExactRatioV1 and all(type(z) is f.RawInputLineageV1 for z in x.raw_input_lineage) for x in facts)
assert not hasattr(reads,'materialise')
bundle=dict(facts=facts,definitions=tuple(reads.get_calculation_definition(derived_signal_id='D014',calculation_definition_version='D014-SIZE-IMBALANCE-'+str(v)) for v in (1,2)),parameters=tuple(reads.get_parameter_set(f.VersionRefV1('mmt-size-basic',v)) for v in (1,2)),policies=tuple(reads.get_input_selection_policy(f.VersionRefV1('mmt-size-selection',v)) for v in (1,2)),units=tuple(reads.get_unit_convention(f.VersionRefV1('mmt-size-shares',v)) for v in (1,2)),mappings=tuple(reads.get_projection_mapping(f.VersionRefV1('mmt-size-'+side,v)) for v in (1,2) for side in ('bid','ask')),history=reads.list_derived_history(derived_signal_id='D014',subject_instrument='NVDA',effective_at_or_before_utc=datetime(2026,10,18,tzinfo=UTC),knowledge_at_or_before_utc=datetime(2026,10,18,tzinfo=UTC),limit=1000))
print(base64.b64encode(pickle.dumps(bundle)).decode())
