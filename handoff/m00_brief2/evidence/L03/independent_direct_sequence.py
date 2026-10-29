"""Independent authority-derived L03 sequence; no Worker fixtures/helpers."""
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

from nvda_desk.raw_signal_occurrence_truth import api as r
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence

RECEIPT = datetime(2026, 10, 20, 12, 39, 59, 100000, tzinfo=UTC)
MAPPING = r.RawSignalProjectionMappingV1(
    'independent-l03-size', 1, r.RawSignalCatalogueId('R190'),
    'independent-synthetic-provider', 'independent-smart-v1', ('size',), 'shares'
)

def read_sequence(path):
    raw = r.create_owner(durability_port=create_sqlite_persistence(str(path), create=False))
    query = dict(mappings=(MAPPING,), subject_instrument='independent-STK',
                 received_at_or_before_utc=RECEIPT, event_at_or_before_utc=None, limit=1)
    rows, cursor = [], None
    while True:
        page = raw.reads.list_projected_raw_history(
            r.RawSignalCatalogueId('R190'), cursor=cursor, **query
        )
        assert len(page.items) <= 1
        rows.extend(page.items)
        cursor = page.next_cursor
        if cursor is None:
            break
    assert [x.observation_occurrence_id.value for x in rows] == ['independent-a', 'independent-z']
    for item in rows:
        assert type(item.native_value) is Decimal and str(item.native_value) == '5.00'
        assert item.received_ts_utc == RECEIPT and item.ingestion_sequence == 1
        assert item.ingestion_sequence_scope.value == 'independent-l03-scope'
        assert item.source_temporal_kind == 'receipt_only' and item.source_timestamp_raw is None
    event = raw.reads.list_projected_raw_history(
        r.RawSignalCatalogueId('R190'), cursor=None,
        **{**query, 'event_at_or_before_utc': RECEIPT + timedelta(seconds=10)}
    )
    assert event.items == () and event.next_cursor is None
    future = raw.reads.get_raw_observation_occurrence(r.observation_occurrence_id('independent-future'))
    assert future is not None and future.received_ts_utc == RECEIPT + timedelta(seconds=2)
    assert type(future.native_record['size']) is Decimal and str(future.native_record['size']) == '7.00'
    assert future.ingestion_sequence == 2 and future.source_timestamp_raw is None
    return {'ordered_ids':[x.observation_occurrence_id.value for x in rows],
            'event_cutoff_rows':len(event.items), 'future_known_id_retained':True,
            'causal_order':'UNKNOWN_TIED_RECEIPT_SCOPE_SEQUENCE'}

if len(sys.argv) == 3 and sys.argv[1] == 'read':
    print(json.dumps(read_sequence(Path(sys.argv[2])), sort_keys=True))
else:
    with TemporaryDirectory(prefix='l03-independent-') as directory:
        path = Path(directory) / 'actual.db'
        raw = r.create_owner(durability_port=create_sqlite_persistence(str(path), create=True))
        original = r.RawObservationOccurrenceV1(
            concept_id=r.concept_id('raw_signal.raw_observation_occurrence'),
            contract_id=r.contract_id('nvda.raw_signal.RawObservationOccurrence.v1'),
            observation_occurrence_id=r.observation_occurrence_id('independent-z'),
            delivery_artifact_ref=r.delivery_artifact_ref('independent-delivery'),
            source_provider=r.provider_id('independent-synthetic-provider'),
            native_record={'position':0,'operation':0,'side':1,'size':Decimal('5.00')},
            received_ts_utc=RECEIPT, ingestion_sequence=1,
            ingestion_sequence_scope=r.ingestion_sequence_scope('independent-l03-scope'),
            source_temporal_kind='receipt_only',
            raw_signal_catalogue_ids=(r.RawSignalCatalogueId('R190'),),
            source_variant='independent-smart-v1', subject_instrument='independent-STK'
        )
        raw.commands.admit_raw_observation_occurrence(original)
        raw.commands.admit_raw_observation_occurrence(replace(
            original,observation_occurrence_id=r.observation_occurrence_id('independent-a')))
        raw.commands.admit_raw_observation_occurrence(replace(
            original,observation_occurrence_id=r.observation_occurrence_id('independent-future'),
            received_ts_utc=RECEIPT+timedelta(seconds=2),ingestion_sequence=2,
            native_record={'position':0,'operation':1,'side':1,'size':Decimal('7.00')}))
        del raw
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        result = read_sequence(path)
        completed = subprocess.run([sys.executable,__file__,'read',str(path)],
            capture_output=True,text=True,env=dict(os.environ),check=True)
        assert json.loads(completed.stdout) == result
        assert hashlib.sha256(path.read_bytes()).hexdigest() == before
        print('DIRECT_SEQUENCE_PASS',json.dumps(result,sort_keys=True))
