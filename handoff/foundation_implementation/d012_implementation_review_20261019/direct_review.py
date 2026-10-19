"""Independent authority-literal public sequence; no Worker fixture imports."""
import base64
import hashlib
import os
import pickle
import sqlite3
import subprocess
import sys
from dataclasses import fields, is_dataclass, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal, localcontext
from pathlib import Path

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence

BASE = Path(__file__).parent
BRIEF = 'a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393'
OLD = '3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233'
T = datetime(2026, 10, 16, 1, tzinfo=UTC)
AUTH = (
    f.AuthorityArtifactRefV1('handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md', '603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c'),
    f.AuthorityArtifactRefV1('handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv', '67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549'),
)

def exact(a, b):
    assert type(a) is type(b), (type(a), type(b))
    if type(a) is Decimal:
        assert a.as_tuple() == b.as_tuple(), (a.as_tuple(), b.as_tuple())
    elif is_dataclass(a):
        for x in fields(a):
            exact(getattr(a, x.name), getattr(b, x.name))
    elif type(a) in (tuple, list):
        assert len(a) == len(b)
        for x, y in zip(a, b, strict=True): exact(x, y)
    elif type(a) is dict:
        assert a.keys() == b.keys()
        for x in a: exact(a[x], b[x])
    else:
        assert a == b, (a, b)

def configs(reader, path, clock, *, create=True, digest=BRIEF, ids=('D011', 'D012')):
    return dict(
        admission=f.OwnerAdmissionV1('M02', digest), raw_projection_reader=reader,
        definitions=tuple(f.CalculationDefinitionV1(d, d + ('-SPREAD-' if d == 'D012' else '-MIDPOINT-') + str(v), 'K02_ALGEBRA', 'R035 - R034' if d == 'D012' else '(R034 + R035) / 2', ('R034', 'R035'), (), 'P_BASIC', 'price', 'scalar_decimal', AUTH) for d in ids for v in (1, 2)),
        parameter_sets=tuple(f.CalculationParameterSetV1('mmt-pilot-basic', v, 'P_BASIC', 'NVDA', ('NVDA',)) for v in (1, 2)),
        input_selection_policies=tuple(f.InputSelectionPolicyVersionV1('mmt-pilot-selection', v, ('subject_instrument',), timedelta(seconds=60), timedelta(seconds=10), ('true_instant',), (), 'foundation-pilot-fixture', 'cash_quote_v1', 'foundation-pilot-fixture/cash_quote_v1', 100, 1000) for v in (1, 2)),
        unit_conventions=tuple(f.UnitConventionVersionV1('mmt-pilot-price', v, 'price', 'price', Decimal('1'), Decimal('0')) for v in (1, 2)),
        raw_projection_mappings=tuple(r.RawSignalProjectionMappingV1('mmt-pilot-' + side, v, r.RawSignalCatalogueId(rid), 'foundation-pilot-fixture', 'cash_quote_v1', ('quote', side), 'price', ()) for v in (1, 2) for side, rid in (('bid', 'R034'), ('ask', 'R035'))),
        storage=f.SQLiteStorageV1(str(path), create), utc_now=clock,
    )

def req():
    return f.CalculationRequestV1('D012', 'NVDA', T, T, 'D012-SPREAD-1', f.VersionRefV1('mmt-pilot-basic', 1), f.VersionRefV1('mmt-pilot-selection', 1), (), tuple(f.RawInputBindingV1(rid, f.VersionRefV1('mmt-pilot-' + side, 1), f.VersionRefV1('mmt-pilot-price', 1), 'NVDA') for side, rid in (('bid', 'R034'), ('ask', 'R035'))))

def obs(side, value, *, identity=None, seconds=None, sequence=None):
    bid = side == 'bid'
    seconds = (2 if bid else 1) if seconds is None else seconds
    return r.RawObservationOccurrenceV1(
        concept_id=r.concept_id('raw_signal.raw_observation_occurrence'),
        contract_id=r.contract_id('nvda.raw_signal.RawObservationOccurrence.v1'),
        observation_occurrence_id=r.observation_occurrence_id(identity or 'mmt-pilot-' + side + '-001'),
        delivery_artifact_ref=r.delivery_artifact_ref('mmt-pilot-delivery-001'),
        source_provider=r.provider_id('foundation-pilot-fixture'), native_record={'quote': {side: Decimal(value)}},
        received_ts_utc=T - timedelta(seconds=1 if bid else 0),
        ingestion_sequence=(1 if bid else 2) if sequence is None else sequence,
        ingestion_sequence_scope=r.ingestion_sequence_scope('foundation-pilot-fixture/cash_quote_v1'),
        source_temporal_kind='true_instant', raw_signal_catalogue_ids=(r.RawSignalCatalogueId('R034' if bid else 'R035'),),
        source_variant='cash_quote_v1', subject_instrument='NVDA', native_units='price',
        source_timestamp_raw=(T - timedelta(seconds=seconds)).isoformat().replace('+00:00', 'Z'), source_timezone_native='UTC',
    )

def history(reads, d='D012'):
    return reads.list_derived_history(derived_signal_id=d, subject_instrument='NVDA', effective_at_or_before_utc=T, knowledge_at_or_before_utc=T + timedelta(days=2), limit=1000)

def bundle(reads, identities):
    return {x: reads.get_derived_occurrence(x) for x in identities} | {
        'definitions': tuple(reads.get_calculation_definition(derived_signal_id=d, calculation_definition_version=d + ('-SPREAD-' if d == 'D012' else '-MIDPOINT-') + str(v)) for d in ('D011', 'D012') for v in (1, 2)),
        'parameters': tuple(reads.get_parameter_set(f.VersionRefV1('mmt-pilot-basic', v)) for v in (1, 2)),
        'policies': tuple(reads.get_input_selection_policy(f.VersionRefV1('mmt-pilot-selection', v)) for v in (1, 2)),
        'units': tuple(reads.get_unit_convention(f.VersionRefV1('mmt-pilot-price', v)) for v in (1, 2)),
        'mappings': tuple(reads.get_projection_mapping(f.VersionRefV1('mmt-pilot-' + s, v)) for v in (1, 2) for s in ('bid', 'ask')),
        'history': history(reads),
    }

def reader_process():
    # Receives path and identities only; no calculator, raw reader, configuration,
    # expected answer, or Worker helper is passed to this fresh read-only process.
    rd = f.create_reader(admission=f.OwnerAdmissionV1('M02', BRIEF), storage=f.SQLiteReadStorageV1(sys.argv[2]))
    assert not hasattr(rd, 'materialise')
    print(base64.b64encode(pickle.dumps(bundle(rd, sys.argv[3:]))).decode())

def writer_process():
    raw = r.create_owner(durability_port=create_sqlite_persistence(str(BASE / 'raw.sqlite')))
    owner = f.create_owner(**configs(raw.reads, BASE / 'writer-exited.sqlite', lambda: T + timedelta(seconds=1)))
    value = owner.materialise(req())
    assert value.result.as_tuple() == Decimal('2.00').as_tuple()
    print(base64.b64encode(pickle.dumps(value)).decode())

def main():
    print('ENV', sys.version.split()[0], sqlite3.sqlite_version)
    raw = r.create_owner(durability_port=create_sqlite_persistence(str(BASE / 'raw.sqlite'), create=True))
    raw.commands.admit_raw_observation_occurrence(obs('bid', '100.00'))
    raw.commands.admit_raw_observation_occurrence(obs('ask', '102.0'))
    clock = [T + timedelta(seconds=1)]
    cfg = configs(raw.reads, BASE / 'measurement.sqlite', lambda: clock[0])
    owner = f.create_owner(**cfg)
    initial = req()
    assert history(owner.reads) == ()
    with localcontext() as ctx:
        ctx.prec = 1; ctx.Emax = 1; ctx.Emin = -1
        for signal in ctx.traps: ctx.traps[signal] = True
        first = owner.materialise(initial)
    assert type(first.result) is Decimal and first.result.as_tuple() == Decimal('2.00').as_tuple()
    assert first.calculated_at_utc == T + timedelta(seconds=1)
    assert tuple(x.raw_signal_id for x in first.raw_input_lineage) == ('R034', 'R035')
    assert first.raw_input_lineage[0].canonical_value.as_tuple() == Decimal('100.00').as_tuple()
    assert first.raw_input_lineage[1].canonical_value.as_tuple() == Decimal('102.0').as_tuple()
    assert first.predecessor_occurrence_ids == ()
    assert first.universe is first.window is first.supersedes_derived_occurrence_id is None
    clock[0] += timedelta(days=1)
    exact(owner.materialise(initial), first)
    print('PASS direct materialise then later-clock retry; exact 2.00 and original time/ID')
    before = history(owner.reads)
    for rejected in (
        replace(initial, subject_instrument='OTHER'),
        replace(initial, parameter_set_ref=f.VersionRefV1('mmt-pilot-basic', 3)),
        replace(initial, context_refs=(f.VersionRefV1('strategy', 1),)),
        replace(initial, derived_signal_id='D013'),
        replace(initial, knowledge_cutoff_utc=clock[0] + timedelta(seconds=1)),
    ):
        assert owner.materialise(rejected) is None
        exact(history(owner.reads), before)
    print('PASS five direct refusal -> unchanged nonempty bounded history sequences')
    variants = (
        replace(initial, calculation_definition_version='D012-SPREAD-2'),
        replace(initial, parameter_set_ref=f.VersionRefV1('mmt-pilot-basic', 2)),
        replace(initial, input_selection_policy_ref=f.VersionRefV1('mmt-pilot-selection', 2)),
        replace(initial, raw_input_bindings=(replace(initial.raw_input_bindings[0], projection_mapping_ref=f.VersionRefV1('mmt-pilot-bid', 2)), initial.raw_input_bindings[1])),
        replace(initial, raw_input_bindings=(initial.raw_input_bindings[0], replace(initial.raw_input_bindings[1], projection_mapping_ref=f.VersionRefV1('mmt-pilot-ask', 2)))),
        replace(initial, raw_input_bindings=(replace(initial.raw_input_bindings[0], unit_convention_ref=f.VersionRefV1('mmt-pilot-price', 2)), initial.raw_input_bindings[1])),
        replace(initial, knowledge_cutoff_utc=T + timedelta(seconds=1)),
    )
    facts = [first]
    for variant in variants:
        value = owner.materialise(variant)
        assert value.result.as_tuple() == Decimal('2.00').as_tuple()
        assert value.derived_occurrence_id not in {x.derived_occurrence_id for x in facts}
        exact(owner.reads.get_derived_occurrence(first.derived_occurrence_id), first)
        exact(owner.reads.get_derived_occurrence(value.derived_occurrence_id), value)
        facts.append(value)
    print('PASS isolated definition/parameter/selection/bid-mapping/ask-mapping/one-unit/cutoff changes, old/new exact reads')
    legacy_cfg = configs(raw.reads, BASE / 'old.sqlite', lambda: clock[0], digest=OLD, ids=('D011',))
    legacy = f.create_owner(**legacy_cfg)
    assert legacy.materialise(initial) is None and history(legacy.reads) == ()
    try: f.create_owner(**(legacy_cfg | {'definitions': (cfg['definitions'][2],), 'storage': f.MemoryStorageV1()}))
    except ValueError: pass
    else: raise AssertionError('old authority registered D012')
    old_fact = legacy.materialise(replace(initial, derived_signal_id='D011', calculation_definition_version='D011-MIDPOINT-1'))
    assert old_fact.result == Decimal('101') and old_fact.implementation_brief_sha256 == OLD
    exact(f.create_reader(admission=legacy_cfg['admission'], storage=f.SQLiteReadStorageV1(str(BASE / 'old.sqlite'))).get_derived_occurrence(old_fact.derived_occurrence_id), old_fact)
    print('PASS original authority refuses registration/materialisation D012; original D011 exact read')
    expected = bundle(owner.reads, [x.derived_occurrence_id for x in facts])
    child = subprocess.run([sys.executable, __file__, 'reader', str(BASE / 'measurement.sqlite'), *[x.derived_occurrence_id for x in facts]], check=True, capture_output=True, text=True, timeout=30)
    exact(pickle.loads(base64.b64decode(child.stdout)), expected)
    print('PASS fresh read-only process full typed occurrence/definition/all versioned configuration/history recovery')
    writer = subprocess.run([sys.executable, __file__, 'writer'], check=True, capture_output=True, text=True, timeout=30)
    exited = pickle.loads(base64.b64decode(writer.stdout))
    reader = subprocess.run([sys.executable, __file__, 'reader', str(BASE / 'writer-exited.sqlite'), exited.derived_occurrence_id], check=True, capture_output=True, text=True, timeout=30)
    recovered = pickle.loads(base64.b64decode(reader.stdout))
    exact(recovered[exited.derived_occurrence_id], exited)
    assert recovered['history'] == (exited,)
    print('PASS separate writer process exited, then fresh read-only process exact recovery')
    raw.commands.admit_raw_observation_occurrence(obs('bid', '104.00', identity='changed-bid', seconds=1, sequence=3))
    changed = owner.materialise(initial)
    assert changed.result.as_tuple() == Decimal('-2.00').as_tuple()
    assert changed.derived_occurrence_id not in {x.derived_occurrence_id for x in facts}
    exact(owner.reads.get_derived_occurrence(first.derived_occurrence_id), first)
    print('PASS material raw change -> signed crossed -2.00; prior fact remains exact')
    print('ALL DIRECT SEQUENCES PASS')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'reader': reader_process()
    elif len(sys.argv) > 1 and sys.argv[1] == 'writer': writer_process()
    else: main()
