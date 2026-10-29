"""G01 deliberately discriminating public-path evidence (not admitted production repair).

Expected values are derived from accepted source identities, not existing test fixtures.
D025: R039 High, R040 Low, R037 Last => (90-80)/(120-80)=0.25.
D099: R015 native C/P, R111 IV, R112 delta => 100*(.40-.30)=10 vol points.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
import pytest
import importlib.util

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

# Existing public setup is reused only for D025 transport; expected arithmetic
# and original raw-ID meanings are supplied independently here.
_SPEC = importlib.util.spec_from_file_location(
    'g01_rc02', Path(__file__).resolve().parents[4] / 'tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py'
)
assert _SPEC and _SPEC.loader
_F = importlib.util.module_from_spec(_SPEC)
import sys
sys.modules[_SPEC.name] = _F
_SPEC.loader.exec_module(_F)


def test_g01_d025_high_low_nonsymmetric_public_result():
    case = _F.Case('D025', (
        ('R039', Decimal(120)), ('R040', Decimal(80)), ('R037', Decimal(90))
    ), Decimal('0.25'))
    owner, request = _F.public_scalar(case)
    result = owner.materialise(request)
    assert result is not None
    assert result.result == case.expected, (
        'D025 must treat R039 as High and R040 as Low, not inverted labels'
    )


@pytest.mark.parametrize("did,expected", [("D099", Decimal(10)), ("D100", Decimal(30))])
def test_g01_skew_native_right_c_p_not_numeric_strike_public_result(did: str, expected: Decimal):
    now = datetime(2026, 10, 10, 9, tzinfo=UTC)
    expiry = '2026-12-18'
    m00 = raw.create_owner()
    bindings = []
    key_paths = tuple((key, ('identity', key)) for key in
                      ('contract_id', 'underlying_instrument', 'expiry', 'strike', 'option_right'))
    points = (
        ('C25', 'call', Decimal(155), Decimal('0.25'), Decimal('0.30')),
        ('P25', 'put', Decimal(145), Decimal('-0.25'), Decimal('0.40')),
        ('C10', 'call', Decimal(165), Decimal('0.10'), Decimal('0.20')),
        ('P10', 'put', Decimal(135), Decimal('-0.10'), Decimal('0.50')),
    )
    seq = 0
    for contract, right, strike, delta, iv in points:
        identity = raw.RawSelectionIdentityV1((
            ('contract_id', contract), ('underlying_instrument', 'NVDA'),
            ('expiry', expiry), ('strike', strike), ('option_right', right),
        ))
        native_right = 'C' if right == 'call' else 'P'
        for rid, value in (('R111', iv), ('R112', delta), ('R015', native_right)):
            seq += 1
            m00.commands.admit_raw_observation_occurrence(raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id('raw_signal.raw_observation_occurrence'),
                contract_id=raw.contract_id('nvda.raw_signal.RawObservationOccurrence.v1'),
                observation_occurrence_id=raw.observation_occurrence_id(f'g01-{contract}-{rid}'),
                delivery_artifact_ref=raw.delivery_artifact_ref(f'g01-{contract}-{rid}'),
                source_provider=raw.provider_id('controlled-g01-source-contract'),
                native_record={'metric': {rid: value}, 'identity': dict(identity.values)},
                received_ts_utc=now-timedelta(seconds=10),
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope('g01:skew'),
                source_temporal_kind='true_instant',
                source_timestamp_raw=(now-timedelta(seconds=10)).isoformat(),
                source_timezone_native='UTC',
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant='native-option-right', subject_instrument='NVDA',
                native_units='canonical', revision_vintage_native='v1',
            ))
            bindings.append(api.RawInputBindingV1(
                rid, api.VersionRefV1('g01-skew-'+rid, 1),
                api.VersionRefV1('g01-canonical', 1), 'NVDA', identity,
            ))
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(raw.RawSignalProjectionMappingV1(
            'g01-skew-'+rid, 1, raw.RawSignalCatalogueId(rid),
            'controlled-g01-source-contract', 'native-option-right',
            ('metric',rid), 'canonical', key_paths,
        ) for rid in ('R111','R112','R015')),
        parameter_sets=(api.CalculationParameterSetV1(
            'g01-skew-basic',1,'P_BASIC',(('subject_instrument','NVDA'),),
        ),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            'g01-skew-expiry',1,('underlying_instrument','expiry'),
            timedelta(minutes=3),timedelta(minutes=3),('true_instant',),(),
        ),),
        unit_conventions=(api.UnitConventionVersionV1(
            'g01-canonical',1,'canonical','canonical',Decimal(1),Decimal(0),
        ),),
        contexts=(), utc_now=lambda:now,
    )
    request = api.CalculationRequestV1(
        did,'NVDA',now,now,'g01-skew','g01-skew-basic',1,
        'g01-skew-expiry',1,(),raw_input_bindings=tuple(bindings),
    )
    actual = owner.materialise(request)
    assert actual is not None, f'{did} refused source-native C/P raw R015'
    assert actual.result == expected
