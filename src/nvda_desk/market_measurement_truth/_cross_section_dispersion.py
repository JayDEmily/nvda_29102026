"""Complete controlled underlying basket, exact sample return dispersion."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import _underlying_returns as underlying
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._log_return import _logarithm
from ._numeric_bounds import sqrt_ratio_50
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "463d126955fa20959ca81b1bb8792fd63750176b78ced7b7dc432d3326923af4"
MEMBERS = ("NVDA", "QQQ", "SMH")
DEFINITION = f.CalculationDefinitionV1(
    "D083", "D083-CROSS-SECTION-DISPERSION-1", "K04_STANDARDISE_RANK",
    "sample_sd(log(current/prior) for all three members)", ("R037", "R042"), (),
    "P_CROSS_SECTION", "return_dispersion", "scalar_decimal",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d083-controlled", 1, "P_CROSS_SECTION", "TECH_SEMI_DISPERSION", MEMBERS
)
POLICY = replace(
    underlying.configuration("D073")[2], context_id="mmt-d083-selection",
    basket_membership=MEMBERS,
)


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D083", "TECH_SEMI_DISPERSION", underlying.T,
        underlying.T + timedelta(seconds=1), DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (underlying.CONTEXT.ref,),
        tuple(
            f.RawInputBindingV1(
                mapping.raw_signal_catalogue_id.value,
                f.VersionRefV1(mapping.mapping_id, 1),
                f.VersionRefV1(underlying.UNIT.context_id, 1), member,
            ) for member in MEMBERS for mapping in underlying.MAPS
        ),
    )
    if (
        canonical(request.calculation) != canonical(expected)
        or request.context != underlying.CONTEXT
        or request.predecessor_occurrence_ids
        or now < expected.knowledge_cutoff_utc
    ):
        raise ValueError("incompatible exact cross-section request")


def line(item: r.ProjectedRawValueV1, request: f.CalculationRequestV1,
         member: str, role: int) -> f.RawInputLineageV1:
    mapping = underlying.MAPS[role]
    scoped = replace(request, subject_instrument=member)
    event = eligible(replace(item, selection_identity=None), mapping, POLICY, scoped)
    expected = r.RawSelectionIdentityV1((
        ("instrument.id", member),
        ("session.id", "controlled-20oct12-13Z" if role == 0 else "controlled-19oct12-13Z"),
        ("adjustment.basis", "controlled_unadjusted/1"),
        ("price.kind", "current_last" if role == 0 else "official_close"),
    ))
    anchor = underlying.T if role == 0 else underlying.REFERENCE
    if (
        event != anchor or item.received_ts_utc != anchor
        or item.selection_identity != expected
        or type(item.native_value) is not Decimal
        or cast(Decimal, item.native_value) <= 0
    ):
        raise ValueError("positive exact member price role required")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1(underlying.UNIT.context_id, 1), item,
        cast(Decimal, item.native_value), anchor,
    )


def produce(request: f.WindowCalculationRequestV1,
            lines: tuple[f.RawInputLineageV1, ...], now: datetime
            ) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    if len(lines) != 6:
        raise ValueError("all six exact member price roles required")
    returns = []
    for member_index, member in enumerate(MEMBERS):
        for role in (0, 1):
            actual = lines[member_index * 2 + role]
            if canonical(actual) != canonical(line(actual.projection, request.calculation,
                                                   member, role)):
                raise ValueError("wrong exact member/source lineage")
        returns.append(Fraction(_logarithm(
            lines[member_index * 2].canonical_value,
            lines[member_index * 2 + 1].canonical_value,
        )))
    mean = sum(returns, Fraction(0)) / 3
    variance = sum(((value - mean) ** 2 for value in returns), Fraction(0)) / 2
    result = sqrt_ratio_50(variance)
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D083", "pending", request, DEFINITION,
        PARAMETER, POLICY, (underlying.UNIT,), underlying.MAPS, lines, (), 85200,
        result, "return_dispersion", "scalar_decimal", underlying.T,
        request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact cross-section occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce(value.request, value.raw_input_lineage,
                                             value.calculated_at_utc)):
        raise ValueError("cross-section result/source/identity mismatch")


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact cross-section request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            lines = []
            for member in MEMBERS:
                scoped = replace(request.calculation, subject_instrument=member)
                for role, mapping in enumerate(underlying.MAPS):
                    anchor = underlying.T if role == 0 else underlying.REFERENCE
                    candidates = tuple(
                        item for item in history(self.raw, scoped, mapping, POLICY)
                        if item.source_timestamp_raw == anchor.isoformat().replace("+00:00", "Z")
                    )
                    if not candidates:
                        raise ValueError("missing exact member source role")
                    def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, int]:
                        return item.received_ts_utc, item.ingestion_sequence
                    selected = max(candidates, key=rank)
                    if sum(rank(item) == rank(selected) for item in candidates) != 1:
                        raise ValueError("ambiguous exact member rank")
                    lines.append(line(selected, request.calculation, member, role))
            value = produce(request, tuple(lines), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D083 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage/clock required")
    return _Owner(RecordState(storage, _decode, validate), raw, now)
