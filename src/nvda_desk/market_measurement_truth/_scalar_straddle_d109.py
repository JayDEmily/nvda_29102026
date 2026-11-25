"""Fixed controlled D109 scalar pair; exact actual parent provenance, not a strike grid."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as raw

from . import _native_codec as native
from . import _option_scalars as mid
from . import _scalar_straddle_codec as codec
from . import _scalar_straddle_d091 as delta
from . import _scalar_straddle_source as scalar
from . import api as f
from ._record_store import RecordState

NAMESPACE = "neutral_market_measurement_truth/d109/scalar/v1"
DEFINITION = f.CalculationDefinitionV1(
    "D109", "T01-D109-SCALAR-PAIR-DEF-V1", "K02_ALGEBRA",
    "call midpoint + put midpoint", (), ("D087", "D091"), "P_BASIC",
    "USD_per_share", "exact_ratio",
    (
        f.AuthorityArtifactRefV1(scalar.POLICY_PATH, scalar.POLICY_SHA),
        f.AuthorityArtifactRefV1(scalar.BRIEF_PATH, scalar.BRIEF),
    ),
)
_Quotes = tuple[
    raw.RawObservationOccurrenceV1, raw.RawObservationOccurrenceV1,
    raw.RawObservationOccurrenceV1, raw.RawObservationOccurrenceV1,
]
_Mids = tuple[f.WindowMeasurementOccurrenceV1, f.WindowMeasurementOccurrenceV1]
_Deltas = tuple[f.ScalarD091OccurrenceV1, f.ScalarD091OccurrenceV1]
_Projections = tuple[
    raw.ProjectedRawValueV1, raw.ProjectedRawValueV1,
    raw.ProjectedRawValueV1, raw.ProjectedRawValueV1,
]


def _parent_ids(request: f.D109ScalarRequestV1) -> tuple[str, str, str, str]:
    return request.call_mid, request.put_mid, request.call_delta, request.put_delta


def _request_check(request: f.D109ScalarRequestV1) -> None:
    if type(request) is not f.D109ScalarRequestV1:
        raise TypeError("exact D109 scalar request required")
    if (
        request.derived_signal_id != "D109"
        or request.subject_instrument != scalar.SUBJECT
        or request.as_of_utc != scalar.T
        or request.knowledge_cutoff_utc != scalar.CUTOFF
        or request.calculation_definition_version != DEFINITION.calculation_definition_version
    ):
        raise ValueError("unadmitted D109 scalar request identity")
    ids = _parent_ids(request)
    if any(type(oid) is not str or not oid for oid in ids) or len(set(ids)) != 4:
        raise ValueError("four distinct actual parent identities required")
    # Resolve to the exact valid ordered six-member core; the digest is not
    # itself authority. The original/projection bindings below prove each role.
    scalar.core_literal(request.core_manifest_sha256, scalar.C1, "R034")


def _bind_quote(
    core: str, subject: str, role_index: int, parent: f.WindowMeasurementOccurrenceV1,
    original: raw.RawObservationOccurrenceV1, projection: raw.ProjectedRawValueV1,
) -> None:
    rid = ("R034", "R035")[role_index]
    # This predicate is identical for both contracts, both quote roles and
    # both live and durable validation. The original is separately validated:
    # a D087 projection does not carry original delivery artifact/native units.
    exact_value = scalar.validate_core_role(core, subject, rid, original, projection)
    expected = mid.line(projection, parent.request.calculation, role_index)
    actual = parent.raw_input_lineage[role_index]
    if (
        native.canonical(parent.unit_conventions[0].scale)
        != native.canonical(scalar.PRICE_UNIT.scale)
        or native.canonical(parent.unit_conventions[0].offset)
        != native.canonical(scalar.PRICE_UNIT.offset)
        or parent.unit_conventions != (scalar.PRICE_UNIT,)
        or native.canonical(actual.canonical_value) != native.canonical(exact_value)
        or native.canonical(actual) != native.canonical(expected)
    ):
        raise ValueError("D109 exact parent quote-original lineage mismatch")


def _join(
    request: f.D109ScalarRequestV1, mids: _Mids, deltas: _Deltas,
    originals: _Quotes, live_projections: _Projections | None = None,
) -> f.ExactRatioV1:
    _request_check(request)
    if (
        type(mids) is not tuple or len(mids) != 2
        or any(type(parent) is not f.WindowMeasurementOccurrenceV1 for parent in mids)
        or type(deltas) is not tuple or len(deltas) != 2
        or any(type(parent) is not f.ScalarD091OccurrenceV1 for parent in deltas)
        or type(originals) is not tuple or len(originals) != 4
    ):
        raise TypeError("exact D109 typed parent pairs and four quote originals required")
    if tuple(parent.derived_occurrence_id for parent in (*mids, *deltas)) != _parent_ids(request):
        raise ValueError("D109 actual parent lookup identity mismatch")

    # First verify each existing parent's own semantic profile/identity.
    # D087's existing validator checks its stored equation and typed lineage;
    # this is integrity comparison, never selection of a replacement midpoint.
    for slot, (subject, midpoint, signed_delta, atm) in enumerate(zip(
        (scalar.C1, scalar.C2), mids, deltas, (Decimal("0.50"), Decimal("-0.50")),
        strict=True,
    )):
        mid.validate(midpoint)
        delta._validate(signed_delta)
        if (
            midpoint.request.calculation.subject_instrument != subject
            or signed_delta.request.subject_instrument != subject
            or midpoint.effective_as_of_utc != scalar.T
            or midpoint.knowledge_cutoff_utc != scalar.CUTOFF
            or signed_delta.effective_as_of_utc != scalar.T
            or signed_delta.knowledge_cutoff_utc != scalar.CUTOFF
        ):
            raise ValueError("D109 exact named parent slot/frame mismatch")
        if signed_delta.core_manifest_sha256 != request.core_manifest_sha256:
            raise ValueError("D109 exact parent core alignment mismatch")
        if (
            signed_delta.signed_delta != atm
            or signed_delta.result != f.D091CategoryV1("ABS_50_75")
        ):
            raise ValueError("D109 exact signed ATM parent required")
        # delta._validate also binds the full actual original/projection to
        # its unique R112 literal. Together with the four quote bindings
        # below all six ordered immutable original facts equal the pinned
        # manifest members whose core hash scalar.core_literal recomputes.
        for role_index in range(2):
            index = slot * 2 + role_index
            projection = (
                midpoint.raw_input_lineage[role_index].projection
                if live_projections is None else live_projections[index]
            )
            _bind_quote(
                request.core_manifest_sha256, subject, role_index,
                midpoint, originals[index], projection,
            )

    # The exact validated old D087 values are the numerical parents. Do not
    # reselect quotes, multiply by contract size or consult R118.
    first, second = mids[0].result, mids[1].result
    if type(first) is not f.ExactRatioV1 or type(second) is not f.ExactRatioV1:
        raise TypeError("D109 exact ratio midpoint parents required")
    total = Fraction(first.numerator, first.denominator) + Fraction(
        second.numerator, second.denominator,
    )
    return f.ExactRatioV1(total.numerator, total.denominator)


def _validate(value: f.D109ScalarOccurrenceV1) -> None:
    if type(value) is not f.D109ScalarOccurrenceV1:
        raise TypeError("exact D109 scalar occurrence required")
    f._Validated.__post_init__(value)
    expected = _join(
        value.request, (value.call_mid, value.put_mid),
        (value.call_delta, value.put_delta), value.original_quotes,
    )
    if (
        value.owner_object_id != "M02"
        or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != scalar.BRIEF
        or value.derived_signal_id != "D109"
        or value.definition != DEFINITION
        or value.source_policy_sha256 != scalar.POLICY_SHA
        or value.core_manifest_sha256 != value.request.core_manifest_sha256
        or value.effective_as_of_utc != scalar.T
        or value.knowledge_cutoff_utc != scalar.CUTOFF
        or value.calculated_at_utc < value.knowledge_cutoff_utc
        or value.units != "USD_per_share" or value.result_shape != "exact_ratio"
        or value.result != expected
        or value.derived_occurrence_id != codec.identity_d109(value)
    ):
        raise ValueError("D109 scalar record/lineage/identity mismatch")


def _store(storage: f.SQLiteStorageV1 | f.SQLiteReadStorageV1) -> RecordState:
    return RecordState(storage, codec.decode_d109, _validate, encode=codec.encode_d109)


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self._state = state

    def get_derived_occurrence(self, derived_occurrence_id: str) -> f.D109ScalarOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty D109 scalar occurrence identity required")
        return next(
            (value for value in self._state.all()
             if value.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[f.D109ScalarOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (
            derived_signal_id != "D109" or subject_instrument != scalar.SUBJECT
            or type(limit) is not int or not 1 <= limit <= 64
        ):
            raise ValueError("bounded D109 scalar read-only history required")
        rows = (
            value for value in self._state.all()
            if value.request.subject_instrument == subject_instrument
            and value.effective_as_of_utc <= effective_at_or_before_utc
            and value.knowledge_cutoff_utc <= knowledge_at_or_before_utc
        )
        return tuple(sorted(rows, key=lambda value: (
            value.effective_as_of_utc, value.knowledge_cutoff_utc, value.derived_occurrence_id,
        )))[:limit]


class _Owner:
    def __init__(
        self, source: f.ScalarStraddleSourceV1, midpoint_reader: f.MeasurementWindowReadsV1,
        delta_reader: f.ScalarD091ReadsV1, state: RecordState, utc_now: Callable[[], datetime],
    ) -> None:
        self._source = source
        self._midpoint_reader = midpoint_reader
        self._delta_reader = delta_reader
        self._state, self._utc_now = state, utc_now
        self.reads = _Reads(state)

    def materialise(self, request: f.D109ScalarRequestV1) -> f.D109ScalarOccurrenceV1 | None:
        if type(request) is not f.D109ScalarRequestV1:
            raise TypeError("exact D109 scalar request required")
        now = self._utc_now()
        f._utc(now)
        try:
            _request_check(request)
            if (
                request.core_manifest_sha256 != self._source.core_manifest_sha256
                or now < request.knowledge_cutoff_utc
            ):
                raise ValueError("D109 scalar source core or calculation clock mismatch")
        except (TypeError, ValueError, ArithmeticError):
            return None

        # Public read-only parent lookups, exact named identities, no fallback.
        # Technical/storage failures are not swallowed as business refusal.
        call_mid = self._midpoint_reader.get_derived_occurrence(request.call_mid)
        put_mid = self._midpoint_reader.get_derived_occurrence(request.put_mid)
        call_delta = self._delta_reader.get_derived_occurrence(request.call_delta)
        put_delta = self._delta_reader.get_derived_occurrence(request.put_delta)
        if (
            type(call_mid) is not f.WindowMeasurementOccurrenceV1
            or type(put_mid) is not f.WindowMeasurementOccurrenceV1
            or type(call_delta) is not f.ScalarD091OccurrenceV1
            or type(put_delta) is not f.ScalarD091OccurrenceV1
        ):
            return None
        try:
            quotes = tuple(
                scalar.source_role(self._source, subject, rid)
                for subject, rid in scalar.ROLES[:4]
            )
            originals = cast(_Quotes, tuple(original for original, _ in quotes))
            projections = cast(_Projections, tuple(projection for _, projection in quotes))
            result = _join(
                request, (call_mid, put_mid), (call_delta, put_delta), originals, projections,
            )
            for subject, parent in zip(
                (scalar.C1, scalar.C2), (call_delta, put_delta), strict=True,
            ):
                actual, projection = scalar.source_role(self._source, subject, "R112")
                if (
                    native.canonical(actual) != native.canonical(parent.original_observation)
                    or native.canonical(projection) != native.canonical(parent.selected_projection)
                ):
                    raise ValueError("D109 actual source/delta parent mismatch")
            value = f.D109ScalarOccurrenceV1(
                "M02", NAMESPACE, scalar.BRIEF, "D109", "pending", request, DEFINITION,
                scalar.POLICY_SHA, request.core_manifest_sha256,
                call_mid, put_mid, call_delta, put_delta, originals, result,
                "USD_per_share", "exact_ratio", request.as_of_utc,
                request.knowledge_cutoff_utc, now,
            )
            value = replace(value, derived_occurrence_id=codec.identity_d109(value))
        except (TypeError, ValueError, ArithmeticError):
            return None
        # Actual append/readback integrity and transaction errors propagate.
        return cast(f.D109ScalarOccurrenceV1, self._state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, source: f.ScalarStraddleSourceV1,
    midpoint_read_storage: f.SQLiteReadStorageV1, delta_read_storage: f.SQLiteReadStorageV1,
    storage: f.SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> f.D109ScalarOwnerV1:
    scalar.check_admission(admission)
    if (
        type(source) is not f.ScalarStraddleSourceV1
        or type(midpoint_read_storage) is not f.SQLiteReadStorageV1
        or type(delta_read_storage) is not f.SQLiteReadStorageV1
        or type(storage) is not f.SQLiteStorageV1 or not callable(utc_now)
    ):
        raise ValueError("unadmitted D109 scalar source/storage/clock")
    scalar.core_literal(source.core_manifest_sha256, scalar.C1, "R034")
    midpoint_reader = f.create_window_reader(
        admission=f.OwnerAdmissionV1("M02", mid.BRIEF_D087), storage=midpoint_read_storage,
    )
    delta_reader = f.create_scalar_d091_reader(admission=admission, storage=delta_read_storage)
    return _Owner(source, midpoint_reader, delta_reader, _store(storage), utc_now)


def build_reader(
    admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1,
) -> f.D109ScalarReadsV1:
    scalar.check_admission(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D109 scalar read-only storage")
    return _Reads(_store(storage))
