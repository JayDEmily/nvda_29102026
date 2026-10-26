"""D123 exact-contract controlled official OI period and revision selection."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._evaluation import canonical
from ._option_skew import source_event
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "5451c5c6c99559cc859b5aecac4cffa1ea6aa18676d53dbb3e77bb67222ad4dc"
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF = T + timedelta(seconds=1)
SUBJECT = "controlled-nvda-2026-12-18-C150"
PROVIDER, VARIANT = "foundation-controlled-official-oi", "period_v1"
PERIOD_KEYS = (
    "official_reporting_period_id", "official_reporting_period_order",
    "official_revision_id", "official_revision_precedence",
)
META = tuple((key, ("identity", key)) for key in (
    "contract_id", "underlying_instrument", "expiry", "strike", "option_right",
    *PERIOD_KEYS,
))
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-d123-r047-official-oi", 1, r.RawSignalCatalogueId("R047"),
    PROVIDER, VARIANT, ("quantity",), "contracts", META,
)
UNIT = f.UnitConventionVersionV1("mmt-d123-contracts", 1, "contracts", "contracts",
                                 Decimal(1), Decimal(0))
AUTHORITY = (
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
        "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
    ),
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
        "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
    ),
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/D123_CALCULATION_DEFINITION_AUTHORISED_CLARIFICATION_20261011.md",
        "3dcbb5090f0e32e909e16b361b7b93b2a28cae6e5cc687475e8f78c1e83304ad",
    ),
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-official-oi-selection", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC), datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
DEFINITION = f.CalculationDefinitionV1(
    "D123", "D123-20261011-01", "K02_ALGEBRA",
    "highest official current period revision minus highest prior distinct period revision",
    ("R047", "R048"), (), "P_BASIC", "contracts", "exact_ratio", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d123-controlled", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d123-selection", 1,
    ("subject_instrument", "contract_id", "underlying_instrument", "expiry", "strike",
     "option_right"), timedelta(seconds=60), timedelta(0), ("true_instant",),
    (SUBJECT,), PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
BASE = (
    ("contract_id", "C150"), ("underlying_instrument", "NVDA"),
    ("expiry", "2026-12-18"), ("strike", "150"), ("option_right", "call"),
)


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    expected = f.CalculationRequestV1(
        "D123", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,), (f.RawInputBindingV1(
            "R047", f.VersionRefV1(MAPPING.mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), SUBJECT,
        ),),
    )
    f._utc(now)
    if (type(request) is not f.WindowCalculationRequestV1 or now < CUTOFF
        or canonical(c) != canonical(expected) or request.context != CONTEXT
        or request.predecessor_occurrence_ids):
        raise ValueError("unadmitted exact D123 request")


def _fields(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1
            ) -> tuple[str, int, str, int]:
    identity = item.selection_identity
    if identity is None or tuple(identity.values[:5]) != BASE:
        raise ValueError("wrong exact CALL contract")
    try:
        period, ordinal, revision, precedence = (identity.value_for(key)
                                                  for key in PERIOD_KEYS)
    except (KeyError, ValueError) as exc:
        raise ValueError("missing official period/revision") from exc
    if (type(period) is not str or not period
        or type(ordinal) is not int or ordinal < 0
        or type(revision) is not str or not revision
        or type(precedence) is not int or precedence < 1
        or identity != r.RawSelectionIdentityV1((*BASE,
            (PERIOD_KEYS[0], period), (PERIOD_KEYS[1], ordinal),
            (PERIOD_KEYS[2], revision), (PERIOD_KEYS[3], precedence)))):
        raise ValueError("unadmitted controlled official period/revision")
    if (type(item.native_value) is not Decimal or item.native_value < 0
        or item.received_ts_utc > c.knowledge_cutoff_utc
        or eligible(replace(item, selection_identity=None), MAPPING, POLICY, c) is None):
        raise ValueError("ineligible exact contract OI")
    return period, ordinal, revision, precedence


def line(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1) -> f.RawInputLineageV1:
    _fields(item, c)
    return f.RawInputLineageV1(
        "R047", item.observation_occurrence_id.value,
        f.VersionRefV1(MAPPING.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, cast(Decimal, item.native_value), source_event(item),
    )


def select(items: tuple[r.ProjectedRawValueV1, ...], c: f.CalculationRequestV1
           ) -> tuple[f.RawInputLineageV1, f.RawInputLineageV1]:
    seen: dict[str, r.ProjectedRawValueV1] = {}
    for item in items:
        period, ordinal, revision, precedence = _fields(item, c)
        if period in seen and _fields(seen[period], c)[1] != ordinal:
            raise ValueError("one official period has contradictory ordinal")
        for other in items:
            if other is item:
                continue
            other_period, other_ordinal, other_revision, other_precedence = _fields(other, c)
            if ((other_period != period and other_ordinal == ordinal)
                or (other_period == period and other_revision == revision
                    and other_precedence != precedence)):
                raise ValueError("contradictory official period/revision")
        if period not in seen or _fields(seen[period], c)[3] < precedence:
            seen[period] = item
        elif _fields(seen[period], c)[3] == precedence:
            raise ValueError("ambiguous revision precedence")
    if len(seen) < 2:
        raise ValueError("two distinct official periods required")
    ranked = sorted(seen.values(), key=lambda item: _fields(item, c)[1], reverse=True)
    return line(ranked[1], c), line(ranked[0], c)


def produce(request: f.WindowCalculationRequestV1,
            lines: tuple[f.RawInputLineageV1, ...], now: datetime
            ) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    if len(lines) != 2 or any(type(v) is not f.RawInputLineageV1 for v in lines):
        raise ValueError("two selected official periods required")
    for entry in lines:
        if canonical(entry) != canonical(line(entry.projection, request.calculation)):
            raise ValueError("selected exact source lineage mismatch")
    old, new = (_fields(value.projection, request.calculation) for value in lines)
    if old[0] == new[0] or old[1] >= new[1]:
        raise ValueError("distinct ordered periods required")
    difference = Fraction(lines[1].canonical_value) - Fraction(lines[0].canonical_value)
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D123", "pending", request, DEFINITION,
        PARAMETER, POLICY, (UNIT,), (MAPPING,), lines, (), 0,
        f.ExactRatioV1(difference.numerator, difference.denominator), "contracts",
        "exact_ratio", T, CUTOFF, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact D123 occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce(value.request, value.raw_input_lineage,
                                             value.calculated_at_utc)):
        raise ValueError("D123 persisted source/result mismatch")


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact D123 request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            items = history(self.raw, request.calculation, MAPPING, POLICY)
            candidates = tuple(item for item in items if item.selection_identity is not None
                               and tuple(item.selection_identity.values[:5]) == BASE)
            lines = select(candidates, request.calculation)
            value = produce(request, lines, now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner(admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
                predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
                storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
                now: Callable[[], datetime]) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("unadmitted D123 owner")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage/clock required")
    return _Owner(RecordState(storage, _decode, validate), raw, now)
