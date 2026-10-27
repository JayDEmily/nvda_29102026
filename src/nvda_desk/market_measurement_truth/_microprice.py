"""D137 exact coherent top-book microprice over four public M00 projections."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "58ecb7858c5ecf1dd5d7c840f8f03a76ae259bcd9fdf93c6a58d3fb4f907c302"
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
SUBJECT, PROVIDER, VARIANT = "NVDA", "foundation-controlled-top-book", "coherent_quote_v1"
ROLES = (
    ("R033", "bid_size", "shares"), ("R034", "bid_price", "USD_per_share"),
    ("R035", "ask_price", "USD_per_share"), ("R036", "ask_size", "shares"),
)
IDENTITY = (("quote.id", ("quote", "id")), ("subject.id", ("subject", "id")))
MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-d137-" + raw.lower(), 1, r.RawSignalCatalogueId(raw), PROVIDER,
    VARIANT, ("quote", field), unit, IDENTITY,
) for raw, field, unit in ROLES)
UNITS = tuple(f.UnitConventionVersionV1(
    "mmt-d137-" + raw.lower() + "-unit", 1, unit, unit, Decimal(1), Decimal(0),
) for raw, _, unit in ROLES)
DEFINITION = f.CalculationDefinitionV1(
    "D137", "D137-COHERENT-TOP-BOOK-MICROPRICE-1", "K02_ALGEBRA",
    "(ask_price*bid_size+bid_price*ask_size)/(bid_size+ask_size)",
    tuple(raw for raw, _, _ in ROLES), (), "P_BASIC", "USD_per_share", "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d137-nvda-top-book", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d137-coherent-quote", 1, ("subject_instrument", "quote.id", "subject.id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), (SUBJECT,),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-top-book-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)


def _request(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D137", SUBJECT, T, T + timedelta(seconds=1),
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,), tuple(f.RawInputBindingV1(
            raw, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), SUBJECT,
        ) for (raw, _, _), mapping, unit in zip(ROLES, MAPS, UNITS, strict=True)),
    )
    if (canonical(request.calculation) != canonical(expected)
            or request.context != CONTEXT or request.predecessor_occurrence_ids
            or now < expected.knowledge_cutoff_utc):
        raise ValueError("incompatible coherent quote request")


def _line(item: r.ProjectedRawValueV1, request: f.CalculationRequestV1,
          role: int) -> f.RawInputLineageV1:
    mapping, unit = MAPS[role], UNITS[role]
    event = eligible(replace(item, selection_identity=None), mapping, POLICY, request)
    if (event != T or item.received_ts_utc != T
            or item.selection_identity != r.RawSelectionIdentityV1((
                ("quote.id", "controlled-quote/1"), ("subject.id", SUBJECT),
            )) or type(item.native_value) is not Decimal):
        raise ValueError("matched coherent quote role required")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(unit.context_id, 1),
        item, item.native_value, T,
    )


def _produce(request: f.WindowCalculationRequestV1,
             lines: tuple[f.RawInputLineageV1, ...], now: datetime
             ) -> f.WindowMeasurementOccurrenceV1:
    _request(request, now)
    if len(lines) != 4:
        raise ValueError("four quote roles required")
    for role, actual in enumerate(lines):
        if canonical(actual) != canonical(_line(actual.projection, request.calculation, role)):
            raise ValueError("quote source lineage mismatch")
    if len({line.observation_occurrence_id for line in lines}) != 1:
        raise ValueError("quote roles must share one public occurrence")
    first = lines[0].projection
    if any((line.projection.received_ts_utc,
            line.projection.ingestion_sequence_scope,
            line.projection.ingestion_sequence) !=
           (first.received_ts_utc, first.ingestion_sequence_scope, first.ingestion_sequence)
           for line in lines[1:]):
        raise ValueError("quote receipt and ingestion must cohere")
    bs, bp, ap, az = (line.canonical_value for line in lines)
    if bs < 0 or az < 0 or bs + az == 0 or bp <= 0 or ap <= 0 or bp > ap:
        raise ValueError("positive uncrossed quote and nonzero size required")
    result = (Fraction(ap) * Fraction(bs) + Fraction(bp) * Fraction(az)) / (
        Fraction(bs) + Fraction(az))
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D137", "pending", request, DEFINITION,
        PARAMETER, POLICY, UNITS, MAPS, lines, (), 0,
        f.ExactRatioV1(result.numerator, result.denominator),
        "USD_per_share", "exact_ratio", T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def _validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact microprice occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(_produce(
        value.request, value.raw_input_lineage, value.calculated_at_utc)):
        raise ValueError("microprice/source/identity mismatch")


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact microprice request required")
        now = self.now()
        f._utc(now)
        try:
            _request(request, now)
            lines = []
            for role, mapping in enumerate(MAPS):
                candidates = tuple(history(self.raw, request.calculation, mapping, POLICY))
                if len(candidates) != 1:
                    raise ValueError("one coherent projection per quote role required")
                lines.append(_line(candidates[0], request.calculation, role))
            value = _produce(request, tuple(lines), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def _admission(admission: f.OwnerAdmissionV1) -> None:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D137 admission required")


def build_owner(admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
                storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
                now: Callable[[], datetime]) -> f.MeasurementWindowOwnerV1:
    _admission(admission)
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage and clock required")
    return _Owner(RecordState(storage, _decode, _validate), raw, now)


def build_reader(admission: f.OwnerAdmissionV1,
                 storage: f.SQLiteReadStorageV1) -> f.MeasurementWindowReadsV1:
    _admission(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise TypeError("read-only storage required")
    return _Reads(RecordState(storage, _decode, _validate))
