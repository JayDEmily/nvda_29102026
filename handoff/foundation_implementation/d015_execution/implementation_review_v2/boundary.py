from datetime import UTC, datetime
from pathlib import Path
import sys
import tempfile

root = Path(sys.argv[1])
sys.path[:0] = [str(root / 'src'), str(root / 'tools')]
from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as raw

class CompleteFacet:
    def get_derived_occurrence(self, *args, **kwargs): return None
    def get_calculation_definition(self, *args, **kwargs): return None
    def get_parameter_set(self, *args, **kwargs): return None
    def get_input_selection_policy(self, *args, **kwargs): return None
    def get_unit_convention(self, *args, **kwargs): return None
    def get_projection_mapping(self, *args, **kwargs): return None

temp = Path(tempfile.mkdtemp(prefix='d015-factory-closure-'))
for name, reader, predecessor in (
    ('bad_raw_only', object(), CompleteFacet()),
    ('bad_predecessor_only', raw.create_owner().reads, object()),
):
    path = temp / (name + '.sqlite')
    assert not path.exists()
    try:
        f.create_trade_direction_owner(admission=f.OwnerAdmissionV1('M02', '84baa16665db5f8543eba3b1770dafcfb36cc5e8064b2f1837beb924713acb0d'), raw_projection_reader=reader, predecessor_reader=predecessor, storage=f.SQLiteStorageV1(str(path), True), utc_now=lambda: datetime(2026, 10, 16, tzinfo=UTC))
    except TypeError as exc:
        assert not path.exists(), 'Invalid facet created SQLite file before rejection'
        print(name, 'TypeError', str(exc), 'SQLite remains absent')
    else:
        raise AssertionError(name + ' accepted invalid public facet')
print('PASS F001 independent facet closure')
