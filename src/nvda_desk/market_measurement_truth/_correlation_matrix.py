"""Exact complete-anchor return correlation on a controlled three-member basket."""

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
from ._log_return import _logarithm
from ._numeric_bounds import sqrt_ratio_50
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "f2b03173b89ac336728346dbacb625ba4e7bb23e3ca23a690a4ece412f84143e"
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
ANCHORS = tuple(T - timedelta(minutes=k) for k in (3, 2, 1, 0))
MEMBERS = ("NVDA", "SPY", "QQQ")
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-correlation-window", 1), ANCHORS[0],
    T + timedelta(minutes=1), ANCHORS[0],
)
PROVIDER, VARIANT = "foundation-controlled-correlation", "minute_close_v1"
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-r151-correlation", 1, r.RawSignalCatalogueId("R151"), PROVIDER, VARIANT,
    ("bar", "close"), "price",
    (
        ("instrument.id", ("instrument", "id")),
        ("bar.end_utc", ("bar", "end_utc")),
        ("bar.kind", ("bar", "kind")),
        ("adjustment.basis", ("adjustment", "basis")),
    ),
)
UNIT = f.UnitConventionVersionV1(
    "mmt-correlation-price", 1, "price", "price", Decimal("1"), Decimal("0")
)
DEFINITION = f.CalculationDefinitionV1(
    "D082", "D082-ALIGNED-RETURN-CORRELATION-1", "K06_REGRESSION_DEPENDENCE",
    "Pearson correlation of three aligned log-return vectors", ("R151",), (),
    "P_REGRESSION", "correlation", "correlation_matrix",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d082-controlled", 1, "P_REGRESSION", "US_CORRELATION_BASKET", MEMBERS
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d082-selection", 1, ("subject_instrument", "instrument.id", "bar.end_utc"),
    timedelta(seconds=180), timedelta(0), ("true_instant",), MEMBERS,
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)


def _utc(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D082", "US_CORRELATION_BASKET", T, T + timedelta(seconds=1),
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1),
        f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,),
        tuple(
            f.RawInputBindingV1(
                "R151", f.VersionRefV1(MAPPING.mapping_id, 1),
                f.VersionRefV1(UNIT.context_id, 1), member,
            ) for member in MEMBERS
        ),
    )
    if (
        canonical(request.calculation) != canonical(expected)
        or request.context != CONTEXT
        or request.predecessor_occurrence_ids
        or now < expected.knowledge_cutoff_utc
    ):
        raise ValueError("incompatible exact correlation request")


def line(
    item: r.ProjectedRawValueV1, request: f.CalculationRequestV1,
    member: str, anchor: datetime,
) -> f.RawInputLineageV1:
    scoped = replace(request, subject_instrument=member, as_of_utc=anchor)
    event = eligible(replace(item, selection_identity=None), MAPPING, POLICY, scoped)
    expected_identity = r.RawSelectionIdentityV1((
        ("instrument.id", member), ("bar.end_utc", _utc(anchor)),
        ("bar.kind", "controlled_minute_close"),
        ("adjustment.basis", "controlled_unadjusted/1"),
    ))
    if (
        event != anchor
        or item.selection_identity != expected_identity
        or type(item.native_value) is not Decimal
        or cast(Decimal, item.native_value) <= 0
        or item.received_ts_utc != anchor
    ):
        raise ValueError("positive exact-anchor minute close required")
    return f.RawInputLineageV1(
        "R151", item.observation_occurrence_id.value,
        f.VersionRefV1(MAPPING.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, cast(Decimal, item.native_value), anchor,
    )


def _matrix(lines: tuple[f.RawInputLineageV1, ...]) -> f.CorrelationMatrixV1:
    vectors: list[tuple[Fraction, ...]] = []
    for offset in (0, 4, 8):
        closes = [lines[offset + i].canonical_value for i in range(4)]
        vectors.append(tuple(Fraction(_logarithm(closes[i], closes[i - 1]))
                             for i in range(1, 4)))
    centred = [
        tuple(v - sum(vector, Fraction(0)) / 3 for v in vector) for vector in vectors
    ]
    sums = [sum((v * v for v in vector), Fraction(0)) for vector in centred]
    if any(value <= 0 for value in sums):
        raise ValueError("nonconstant aligned return vectors required")
    rows: list[list[Decimal]] = [[Decimal(0)] * 3 for _ in range(3)]
    for i in range(3):
        rows[i][i] = Decimal(1)
        for j in range(i):
            cross = sum((a * b for a, b in zip(centred[i], centred[j], strict=True)),
                        Fraction(0))
            value = sqrt_ratio_50(cross * cross / (sums[i] * sums[j]))
            signed = -value if cross < 0 else value
            rows[i][j] = rows[j][i] = signed
    return f.CorrelationMatrixV1(MEMBERS, tuple(tuple(row) for row in rows))


def produce(
    request: f.WindowCalculationRequestV1, lines: tuple[f.RawInputLineageV1, ...],
    now: datetime,
) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    if len(lines) != 12:
        raise ValueError("complete aligned three-member four-anchor closes required")
    for member_index, member in enumerate(MEMBERS):
        for i, anchor in enumerate(ANCHORS):
            actual = lines[member_index * 4 + i]
            if canonical(actual) != canonical(line(actual.projection, request.calculation,
                                                   member, anchor)):
                raise ValueError("wrong selected exact-anchor lineage")
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D082", "pending", request, DEFINITION,
        PARAMETER, POLICY, (UNIT,), (MAPPING,), lines, (), 180, _matrix(lines),
        "correlation", "correlation_matrix", T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact window occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce(value.request, value.raw_input_lineage,
                                             value.calculated_at_utc)):
        raise ValueError("correlation matrix/source/identity mismatch")


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(
        self, request: f.WindowCalculationRequestV1,
    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact correlation request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            lines = []
            for member in MEMBERS:
                scoped = replace(request.calculation, subject_instrument=member)
                candidates = history(self.raw, scoped, MAPPING, POLICY)
                for anchor in ANCHORS:
                    matching = tuple(
                        item for item in candidates if item.source_timestamp_raw == _utc(anchor)
                    )
                    if not matching:
                        raise ValueError("missing exact-anchor close")
                    def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, int]:
                        return item.received_ts_utc, item.ingestion_sequence
                    selected = max(matching, key=rank)
                    if sum(rank(item) == rank(selected) for item in matching) != 1:
                        raise ValueError("ambiguous exact-anchor source rank")
                    # The selected fact must validate; an older value cannot replace it.
                    lines.append(line(selected, request.calculation, member, anchor))
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
        raise ValueError("exact D082 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage and clock required")
    return _Owner(RecordState(storage, _decode, validate), raw, now)
