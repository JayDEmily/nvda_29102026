"""Independent literal public setup; no Worker helper or private calculation import."""
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
import sys
import tempfile

root = Path(sys.argv[1])
sys.path[:0] = [str(root / 'src'), str(root / 'tools')]
from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

assert Path(f.__file__).is_relative_to(root)
t = datetime(2026, 10, 16, 1, tzinfo=UTC)
cutoff = t + timedelta(seconds=10)
clock = [cutoff + timedelta(seconds=1)]
brief = '84baa16665db5f8543eba3b1770dafcfb36cc5e8064b2f1837beb924713acb0d'
predecessor = 'a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393'
provider = 'foundation-pilot-fixture'
scope = provider + '/cash_quote_v1'
refs = (
    f.AuthorityArtifactRefV1('handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md', '603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c'),
    f.AuthorityArtifactRefV1('handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv', '67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549'),
)
policy = f.InputSelectionPolicyVersionV1('mmt-pilot-selection', 1, ('subject_instrument',), timedelta(seconds=60), timedelta(seconds=10), ('true_instant',), (), provider, 'cash_quote_v1', scope, 100, 1000)
unit = f.UnitConventionVersionV1('mmt-pilot-price', 1, 'price', 'price', Decimal('1'), Decimal('0'))
def mapping(rid, identity, path):
    return r.RawSignalProjectionMappingV1(identity, 1, r.RawSignalCatalogueId(rid), provider, 'cash_quote_v1', path, 'price', ())
old = (mapping('R034', 'mmt-pilot-bid', ('quote', 'bid')), mapping('R035', 'mmt-pilot-ask', ('quote', 'ask')))
new = (mapping('R120', 'mmt-trade-price', ('trade', 'price')), mapping('R126', 'mmt-trade-bid', ('quote', 'bid')), mapping('R127', 'mmt-trade-ask', ('quote', 'ask')))
raw = r.create_owner()
mid = f.create_owner(
    admission=f.OwnerAdmissionV1('M02', predecessor), raw_projection_reader=raw.reads,
    definitions=(f.CalculationDefinitionV1('D011', 'D011-MIDPOINT-1', 'K02_ALGEBRA', '(R034 + R035) / 2', ('R034', 'R035'), (), 'P_BASIC', 'price', 'scalar_decimal', refs),),
    parameter_sets=(f.CalculationParameterSetV1('mmt-pilot-basic', 1, 'P_BASIC', 'NVDA', ('NVDA',)),),
    input_selection_policies=(policy,), unit_conventions=(unit,), raw_projection_mappings=old,
    storage=f.MemoryStorageV1(), utc_now=lambda: clock[0],
)
database = str(Path(tempfile.mkdtemp(prefix='d015-independent-public-')) / 'sign.sqlite')
owner = f.create_trade_direction_owner(admission=f.OwnerAdmissionV1('M02', brief), raw_projection_reader=raw.reads, predecessor_reader=mid.reads, storage=f.SQLiteStorageV1(database, True), utc_now=lambda: clock[0])
def calculation(did, version, parameter, mappings, at):
    return f.CalculationRequestV1(did, 'NVDA', at, cutoff, version, f.VersionRefV1(parameter, 1), f.VersionRefV1('mmt-pilot-selection', 1), (), tuple(f.RawInputBindingV1(m.raw_signal_catalogue_id.value, f.VersionRefV1(m.mapping_id, 1), f.VersionRefV1('mmt-pilot-price', 1), 'NVDA') for m in mappings))
request = f.TradeDirectionRequestV1(calculation('D015', 'D015-TRADE-DIRECTION-1', 'mmt-trade-rule', new, cutoff), 'not-yet-materialised')
def history():
    return owner.reads.list_derived_history(derived_signal_id='D015', subject_instrument='NVDA', effective_at_or_before_utc=cutoff, knowledge_at_or_before_utc=cutoff, limit=10)
assert owner.materialise(request) is None and history() == ()
print('EMPTY_RAW_AND_PREDECESSOR -> None, empty public history')
def admit(m, identity, price, event, receipt, sequence):
    parent, field = m.native_field_path
    raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
        concept_id=r.concept_id('raw_signal.raw_observation_occurrence'), contract_id=r.contract_id('nvda.raw_signal.RawObservationOccurrence.v1'), observation_occurrence_id=r.observation_occurrence_id(identity), delivery_artifact_ref=r.delivery_artifact_ref('independent-controlled-delivery'), source_provider=r.provider_id(provider), native_record={parent: {field: Decimal(price)}}, received_ts_utc=receipt, ingestion_sequence=sequence, ingestion_sequence_scope=r.ingestion_sequence_scope(scope), source_temporal_kind='true_instant', raw_signal_catalogue_ids=(m.raw_signal_catalogue_id,), source_variant='cash_quote_v1', subject_instrument='NVDA', native_units='price', source_timestamp_raw=event.isoformat().replace('+00:00', 'Z'), source_timezone_native='UTC'))
admit(old[0], 'old-bid', '99', t-timedelta(seconds=2), t-timedelta(seconds=1), 1)
admit(old[1], 'old-ask', '101', t-timedelta(seconds=1), t, 2)
admit(new[0], 'current', '100', t, t, 3)
admit(new[1], 'new-bid', '99', t-timedelta(seconds=2), t-timedelta(seconds=1), 4)
admit(new[2], 'new-ask', '101', t-timedelta(seconds=1), t, 5)
assert owner.materialise(request) is None and history() == ()
print('RAW_PRESENT_BUT_NO_ACTUAL_D011 -> None, empty public history')
actual = mid.materialise(calculation('D011', 'D011-MIDPOINT-1', 'mmt-pilot-basic', old, t))
assert actual is not None and actual.result == Decimal('100')
request = replace(request, midpoint_occurrence_id=actual.derived_occurrence_id)
unknown = owner.materialise(request)
assert unknown is not None and type(unknown.result) is int and unknown.result == 0
assert len(unknown.raw_input_lineage) == 3
print('ACTUAL_TRADE_TIME_D011_AND_NO_DIFFERENT_PRIOR -> exact int0')
admit(new[0], 'old-different', '98', t-timedelta(seconds=120), t-timedelta(seconds=120), 6)
admit(new[0], 'immediately-equal', '100', t-timedelta(seconds=1), t-timedelta(seconds=1), 7)
signed = owner.materialise(request)
assert signed is not None and type(signed.result) is int and signed.result == 1
assert signed.derived_occurrence_id != unknown.derived_occurrence_id
assert signed.predecessor.occurrence == actual
assert tuple(x.observation_occurrence_id for x in signed.raw_input_lineage) == ('current', 'new-bid', 'new-ask', 'old-different')
assert signed.raw_input_lineage[3].event_time_utc == t-timedelta(seconds=120)
assert owner.reads.get_derived_occurrence(unknown.derived_occurrence_id) == unknown
print('ADMITTED_120_SECOND_DIFFERENT_PRIOR_BEHIND_EQUAL -> exact int+1, new immutable fact; zero fact retained')
admit(new[1], 'post-bid', '199', t+timedelta(seconds=5), t+timedelta(seconds=5), 8)
admit(new[2], 'post-ask', '201', t+timedelta(seconds=5), t+timedelta(seconds=5), 9)
clock[0] += timedelta(seconds=3)
assert owner.materialise(request) == signed
fresh = f.create_trade_direction_reader(admission=f.OwnerAdmissionV1('M02', brief), storage=f.SQLiteReadStorageV1(database))
assert fresh.get_derived_occurrence(signed.derived_occurrence_id) == signed
assert fresh.get_derived_occurrence(unknown.derived_occurrence_id) == unknown
assert len(history()) == 2
print('LATER_QUOTES_PLUS_LATER_CLOCK -> first complete signed fact/time retained; source-free SQLite reader recovers both facts')
print('PASS independent public sequence', database)
