"""Owner-local exact controlled arithmetic and canonical identity representation."""

from __future__ import annotations

import hashlib
import json
import types
from dataclasses import fields, is_dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any, Literal, TypeAliasType, cast, get_args, get_origin, get_type_hints

from nvda_desk.raw_signal_occurrence_truth import api as raw_api

_FACTORIES = {
    "RawSignalCatalogueId": raw_api.RawSignalCatalogueId,
    "observation_occurrence_id": raw_api.observation_occurrence_id,
    "ingestion_sequence_scope": raw_api.ingestion_sequence_scope,
}
_IDENTITIES = {
    type(factory("R034" if name == "RawSignalCatalogueId" else "identity")): name
    for name, factory in _FACTORIES.items()
}


def timestamp(value: datetime) -> str:
    if value.tzinfo is not None and value.utcoffset() != timedelta(0):
        return value.isoformat(timespec="microseconds")
    return (
        f"{value.year:04d}-{value.month:02d}-{value.day:02d}T"
        f"{value.hour:02d}:{value.minute:02d}:{value.second:02d}.{value.microsecond:06d}Z"
    )


def tagged(value: Any) -> Any:
    if type(value) in _IDENTITIES:
        return {"kind": _IDENTITIES[type(value)], "value": value.value}
    if type(value) is Decimal:
        sign, digits, exponent = value.as_tuple()
        return {
            "kind": "decimal",
            "sign": sign,
            "digits": "".join(str(item) for item in digits),
            "exponent": exponent,
        }
    if type(value) is datetime:
        return timestamp(value)
    if type(value) is date:
        return {"kind": "date", "value": value.isoformat()}
    if type(value) is timedelta:
        return (value.days * 86400 + value.seconds) * 1000000 + value.microseconds
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: tagged(getattr(value, field.name)) for field in fields(value)}
    if type(value) is tuple:
        return [tagged(item) for item in value]
    if type(value) is dict:
        return {key: tagged(item) for key, item in value.items()}
    if value is None or type(value) in (bool, int, str):
        return value
    raise TypeError("unsupported controlled measurement representation")


def canonical(value: Any) -> bytes:
    return json.dumps(
        tagged(value), sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def untagged(value: Any, hint: Any) -> Any:
    """Decode only the exact declared public record/factory at this position."""
    if isinstance(hint, TypeAliasType):
        return untagged(value, hint.__value__)
    args = get_args(hint)
    if get_origin(hint) is Literal:
        if type(value) is not str or value not in args:
            raise ValueError("invalid literal content")
        return value
    if get_origin(hint) is types.UnionType:
        if value is None and type(None) in args:
            return None
        for option in args:
            if option is type(None):
                continue
            try:
                return untagged(value, option)
            except (TypeError, ValueError, KeyError):
                pass
        raise ValueError("invalid union content")
    if get_origin(hint) is tuple:
        if type(value) is not list:
            raise ValueError("tuple content must be an array")
        if len(args) == 2 and args[1] is Ellipsis:
            return tuple(untagged(item, args[0]) for item in value)
        if len(value) != len(args):
            raise ValueError("tuple arity mismatch")
        return tuple(untagged(item, cls) for item, cls in zip(value, args, strict=True))
    if hint in _IDENTITIES:
        name = _IDENTITIES[hint]
        if type(value) is not dict or set(value) != {"kind", "value"} or value["kind"] != name:
            raise ValueError("opaque public identity layer mismatch")
        return _FACTORIES[name](value["value"])
    if hint is Decimal:
        if type(value) is not dict or set(value) != {"kind", "sign", "digits", "exponent"}:
            raise ValueError("invalid Decimal tag")
        if (
            value["kind"] != "decimal"
            or type(value["sign"]) is not int
            or value["sign"] not in (0, 1)
            or type(value["digits"]) is not str
            or not value["digits"]
            or any(c not in "0123456789" for c in value["digits"])
            or type(value["exponent"]) is not int
        ):
            raise ValueError("invalid exact Decimal content")
        return Decimal((value["sign"], tuple(map(int, value["digits"])), value["exponent"]))
    if hint is datetime:
        if type(value) is not str:
            raise TypeError("instant must be a string")
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    if hint is date:
        if type(value) is not dict or set(value) != {"kind", "value"} or value["kind"] != "date":
            raise ValueError("invalid exact date tag")
        if type(value["value"]) is not str:
            raise TypeError("date value must be a string")
        parsed = date.fromisoformat(value["value"])
        if parsed.isoformat() != value["value"]:
            raise ValueError("noncanonical date value")
        return parsed
    if hint is timedelta:
        if type(value) is not int:
            raise TypeError("duration must be exact microseconds")
        return timedelta(microseconds=value)
    if isinstance(hint, type) and is_dataclass(hint):
        hints = get_type_hints(hint)
        if type(value) is not dict or set(value) != set(hints):
            raise ValueError("incomplete or extra record fields")
        from . import api as f

        if hint in (
            f.OptionRightLineageV1, f.TemporalRawLineageV1,
            f.TemporalAgeRawLineageV1, f.TemporalLocalRawLineageV1,
            f.TemporalCalendarRawLineageV1,
            f.VintageRawLineageV1,
            f.MarketModeRawLineageV1,
            f.BookRawLineageV1,
            f.BookRateRawLineageV1,
        ):
            projection = value["projection"]
            projection_hints = get_type_hints(raw_api.ProjectedRawValueV1)
            rate_types = {
                "R001": str, "R185": int, "R187": int, "R188": int, "R190": dict,
            }
            rid = projection["raw_signal_catalogue_id"]["value"]
            expected_native = (
                (int if rid in ("R185", "R187", "R188") else dict)
                if hint is f.BookRawLineageV1 else
                rate_types.get(rid) if hint is f.BookRateRawLineageV1 else
                int if hint is f.MarketModeRawLineageV1 else str
            )
            if (type(projection) is not dict or set(projection) != set(projection_hints)
                or type(projection["native_value"]) is not expected_native):
                raise ValueError("invalid exact categorical/temporal projection")
            if hint is f.BookRawLineageV1 and projection["raw_signal_catalogue_id"] not in (
                {"kind": "RawSignalCatalogueId", "value": raw}
                for raw in ("R185", "R187", "R188", "R189", "R190")
            ):
                raise ValueError("unadmitted book source role")
            if (hint is f.BookRateRawLineageV1
                and (rid not in rate_types
                     or type(projection["native_value"]) is not rate_types[rid])):
                raise ValueError("unadmitted typed receipt-book projection")
            if hint is f.MarketModeRawLineageV1 and (projection["native_value"] != 1
                or projection["raw_signal_catalogue_id"]
                != {"kind": "RawSignalCatalogueId", "value": "R005"}):
                raise ValueError("unadmitted delivered mode projection")
            if hint is f.OptionRightLineageV1 and projection["native_value"] not in ("C", "P"):
                raise ValueError("invalid exact R015 categorical projection")
            if hint is f.TemporalRawLineageV1 and projection["raw_signal_catalogue_id"] not in (
                {"kind": "RawSignalCatalogueId", "value": "R002"},
                {"kind": "RawSignalCatalogueId", "value": "R003"},
            ):
                raise ValueError("unadmitted exact temporal source role")
            if hint is f.TemporalAgeRawLineageV1 and projection["raw_signal_catalogue_id"] not in (
                {"kind": "RawSignalCatalogueId", "value": "R001"},
                {"kind": "RawSignalCatalogueId", "value": "R002"},
            ):
                raise ValueError("unadmitted exact temporal age source role")
            if hint is f.TemporalLocalRawLineageV1 and projection["raw_signal_catalogue_id"] != (
                {"kind": "RawSignalCatalogueId", "value": "R004"}
            ):
                raise ValueError("unadmitted exact IANA source role")
            if hint is f.TemporalCalendarRawLineageV1 and projection[
                "raw_signal_catalogue_id"
            ] not in (
                {"kind": "RawSignalCatalogueId", "value": "R023"},
                {"kind": "RawSignalCatalogueId", "value": "R024"},
            ):
                raise ValueError("unadmitted exact calendar source role")
            if hint is f.VintageRawLineageV1 and projection[
                "raw_signal_catalogue_id"
            ] not in (
                {"kind": "RawSignalCatalogueId", "value": "R280"},
                {"kind": "RawSignalCatalogueId", "value": "R281"},
                {"kind": "RawSignalCatalogueId", "value": "R282"},
            ):
                raise ValueError("unadmitted exact vintage source role")
            decoded_projection = raw_api.ProjectedRawValueV1(**{
                key: (untagged(projection[key],
                               datetime if projection["raw_signal_catalogue_id"]["value"] == "R001"
                               else int if projection["raw_signal_catalogue_id"]["value"]
                               in ("R185", "R187", "R188") else Decimal)
                      if hint in (f.BookRawLineageV1, f.BookRateRawLineageV1)
                      else projection[key])
                if key == "native_value" else untagged(projection[key], cls)
                for key, cls in projection_hints.items()
            })
            return cast(Any, hint)(**{
                key: decoded_projection if key == "projection" else untagged(value[key], cls)
                for key, cls in hints.items()
            })
        return hint(
            **{
                key: untagged(
                    value[key],
                    Decimal
                    if hint is raw_api.ProjectedRawValueV1 and key == "native_value"
                    else cls,
                )
                for key, cls in hints.items()
            }
        )
    if hint is Any:
        # Projected native value is broader in M00; this pilot stores only Decimal.
        return untagged(value, Decimal)
    if type(value) is not hint:
        raise TypeError("stored scalar type mismatch")
    return value


def decode(payload: bytes, cls: Any) -> Any:
    value = untagged(json.loads(payload), cls)
    if canonical(value) != payload:
        raise ValueError("noncanonical or lossy persisted representation")
    return value


def spread(bid: Decimal, ask: Decimal) -> Decimal | None:
    """Signed ask minus bid at the aligned exponent, without ambient rounding."""
    try:
        if not bid.is_finite() or not ask.is_finite():
            return None
        parts = []
        for value in (bid, ask):
            sign, digits, exponent = value.as_tuple()
            coefficient = 0
            for digit in digits:
                coefficient = coefficient * 10 + digit
            parts.append((-coefficient if sign else coefficient, int(exponent)))
        (bid_coefficient, bid_exponent), (ask_coefficient, ask_exponent) = parts
        aligned_exponent = min(bid_exponent, ask_exponent)
        number = ask_coefficient * 10 ** (
            ask_exponent - aligned_exponent
        ) - bid_coefficient * 10 ** (bid_exponent - aligned_exponent)
        sign, number = int(number < 0), abs(number)
        result = []
        while number:
            number, digit = divmod(number, 10)
            result.append(digit)
        return Decimal((sign, tuple(reversed(result)) if result else (0,), aligned_exponent))
    except (ArithmeticError, ValueError, MemoryError):
        return None


def midpoint(bid: Decimal, ask: Decimal) -> Decimal | None:
    """Exact coefficient alignment/division; no ambient Decimal arithmetic."""
    try:
        if not bid.is_finite() or not ask.is_finite():
            return None

        def coefficient(value: Decimal) -> tuple[int, int]:
            sign, digits, exponent = value.as_tuple()
            n = 0
            for digit in digits:
                n = n * 10 + digit
            return (-n if sign else n), int(exponent)

        a, ae = coefficient(bid)
        b, be = coefficient(ask)
        exponent = min(ae, be)
        numerator = a * 10 ** (ae - exponent) + b * 10 ** (be - exponent)
        if numerator % 2:
            number, exponent = numerator * 5, exponent - 1
        else:
            number = numerator // 2
        sign, number = int(number < 0), abs(number)
        digits = []
        while number:
            number, digit = divmod(number, 10)
            digits.append(digit)
        return Decimal((sign, tuple(reversed(digits)) if digits else (0,), exponent))
    except (ArithmeticError, ValueError, MemoryError):
        return None
