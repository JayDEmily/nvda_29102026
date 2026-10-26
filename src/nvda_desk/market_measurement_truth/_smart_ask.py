"""D135 ask projection of the accepted four-field SMART positional source."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import datetime
from decimal import Decimal
from typing import cast

from . import _smart_depth
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical, decode
from ._record_store import RecordState

BRIEF = "bbd3cbf1e050bfbf9d80bd11eb828df025a0b8cadda93d178d0b028f307dd514"
DEFINITION = f.CalculationDefinitionV1(
    "D135", "D135-SMART-TOP-TWO-ASK-1", "K02_ALGEBRA",
    "sum(top two standing SMART ask sizes after positional replay)",
    tuple(raw for raw, _, _ in _smart_depth.ROLES), (), "P_BASIC", "shares",
    "scalar_decimal", tuple(f.AuthorityArtifactRefV1(*item) for item in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d135-top-two", 1, "P_BASIC", _smart_depth.SUBJECT, (_smart_depth.SUBJECT,),
)


def request() -> f.SmartDepthRequestV1:
    return f.SmartDepthRequestV1(
        f.CalculationRequestV1(
            "D135", _smart_depth.SUBJECT, _smart_depth.T, _smart_depth.CUTOFF,
            DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1), _smart_depth.SELECTION.ref,
            (_smart_depth.SELECTION.ref,), tuple(f.RawInputBindingV1(
                raw, f.VersionRefV1(mapping.mapping_id, 1),
                f.VersionRefV1(unit.context_id, 1), _smart_depth.SUBJECT,
            ) for (raw, _, _), mapping, unit in zip(
                _smart_depth.ROLES, _smart_depth.MAPS, _smart_depth.UNITS, strict=True)),
        ), _smart_depth.SELECTION, 2,
    )


def _request(value: f.SmartDepthRequestV1, now: datetime) -> None:
    f._utc(now)
    if (type(value) is not f.SmartDepthRequestV1
        or canonical(value) != canonical(request())
        or now < _smart_depth.CUTOFF):
        raise ValueError("unadmitted D135 book selection")


def _produce(req: f.SmartDepthRequestV1, lines: tuple[f.BookRawLineageV1, ...],
             now: datetime) -> f.SmartDepthOccurrenceV1:
    _request(req, now)
    standing = _smart_depth._replay(lines)
    ask = tuple(row for row in standing if row.side == 1 and row.position < req.depth_levels)
    if len(ask) != 2:
        raise ValueError("incomplete selected ask levels")
    depth = sum((row.size for row in ask), Decimal(0))
    value = f.SmartDepthOccurrenceV1(
        "M02", _smart_depth.NAMESPACE, BRIEF, "D135", "pending", req,
        DEFINITION, PARAMETER, _smart_depth.UNITS, _smart_depth.MAPS, lines,
        standing, depth, "shares", "scalar_decimal", _smart_depth.T,
        _smart_depth.CUTOFF, now,
    )
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in ("derived_occurrence_id", "calculated_at_utc")}
    return replace(value, derived_occurrence_id="mmtsmart1:" +
                   hashlib.sha256(canonical(payload)).hexdigest())


def _validate(value: f.SmartDepthOccurrenceV1) -> None:
    if type(value) is not f.SmartDepthOccurrenceV1:
        raise TypeError("exact D135 occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(_produce(value.request, value.raw_input_lineage,
                                              value.calculated_at_utc)):
        raise ValueError("D135 source/state/result/identity mismatch")


def _decode(payload: bytes) -> f.SmartDepthOccurrenceV1:
    return cast(f.SmartDepthOccurrenceV1, decode(payload, f.SmartDepthOccurrenceV1))


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _smart_depth._Reads(state)

    def materialise(self, req: f.SmartDepthRequestV1) -> f.SmartDepthOccurrenceV1 | None:
        now = self.now()
        f._utc(now)
        try:
            _request(req, now)
            lines: list[f.BookRawLineageV1] = []
            for role, mapping in enumerate(_smart_depth.MAPS):
                cursor: str | None = None
                while True:
                    page = self.raw.list_projected_raw_history(
                        mapping.raw_signal_catalogue_id, mappings=(mapping,),
                        subject_instrument=_smart_depth.SUBJECT,
                        received_at_or_before_utc=_smart_depth.CUTOFF,
                        event_at_or_before_utc=_smart_depth.T, limit=100, cursor=cursor,
                    )
                    lines.extend(_smart_depth._line(item, role) for item in page.items)
                    if len(lines) > _smart_depth.SELECTION.maximum_events * len(
                        _smart_depth.MAPS
                    ):
                        raise ValueError("unbounded SMART history")
                    if page.next_cursor is None:
                        break
                    if page.next_cursor == cursor:
                        raise ValueError("nonprogressing SMART cursor")
                    cursor = page.next_cursor
            lines.sort(key=lambda line: (line.projection.received_ts_utc,
                                         line.projection.ingestion_sequence,
                                         next(i for i, spec in enumerate(_smart_depth.ROLES)
                                              if spec[0] == line.raw_signal_id)))
            value = _produce(req, tuple(lines), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.SmartDepthOccurrenceV1, self.state.append(value))


def build_owner(admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
                storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
                now: Callable[[], datetime]) -> f.MeasurementSmartDepthOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("unadmitted D135 owner")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact SMART storage and clock required")
    return _Owner(RecordState(storage, _decode, _validate), raw, now)


def build_reader(admission: f.OwnerAdmissionV1,
                 storage: f.SQLiteReadStorageV1) -> f.MeasurementSmartDepthReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D135 reader")
    return _smart_depth._Reads(RecordState(storage, _decode, _validate))
