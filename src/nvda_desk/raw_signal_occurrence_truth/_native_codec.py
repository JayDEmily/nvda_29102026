"""Lossless NVDA-NATIVE-V1 codec preserving the retained backend's wire bytes."""

from collections.abc import Mapping
from datetime import UTC, datetime
from decimal import Decimal
from struct import pack, unpack
from typing import cast

from .api import NativeValueV1

_NATIVE_CODEC_PREFIX = b"NVDA-NATIVE-V1\x00"


def _integer_text(value: int) -> str:
    # Decimal(int) is exact, context-independent and has exponent zero. This
    # preserves decimal wire bytes without changing the interpreter-wide limit.
    return str(Decimal(value))


def _integer_from_text(text: str) -> int:
    digits = text[1:] if text.startswith("-") else text
    if not digits or any(digit not in "0123456789" for digit in digits):
        raise ValueError("invalid integer representation")
    result = int(Decimal(text))
    if _integer_text(result) != text:
        raise ValueError("noncanonical integer representation")
    return result


def _encode_length(value: int) -> bytes:
    if value < 0:
        raise ValueError("native codec length cannot be negative")
    return value.to_bytes(8, "big", signed=False)


def _encode_native_value(value: NativeValueV1) -> bytes:
    if value is None:
        return b"n"
    if type(value) is bool:
        return b"b\x01" if value else b"b\x00"
    if type(value) is int:
        payload = _integer_text(value).encode("ascii")
        return b"i" + _encode_length(len(payload)) + payload
    if type(value) is float:
        return b"f" + pack("!d", value)
    if type(value) is Decimal:
        value_tuple = value.as_tuple()
        digits = bytes(value_tuple.digits)
        exponent = str(value_tuple.exponent).encode("ascii")
        return (
            b"d"
            + bytes((value_tuple.sign,))
            + _encode_length(len(digits))
            + digits
            + _encode_length(len(exponent))
            + exponent
        )
    if type(value) is datetime:
        if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
            raise ValueError("native datetime carrier must be UTC-aware")
        payload = value.isoformat().encode("ascii")
        return b"z" + _encode_length(len(payload)) + payload
    if type(value) is str:
        payload = value.encode("utf-8")
        return b"s" + _encode_length(len(payload)) + payload
    if type(value) is bytes:
        return b"y" + _encode_length(len(value)) + value
    if type(value) is list:
        parts = [b"l", _encode_length(len(value))]
        parts.extend(_encode_native_value(item) for item in value)
        return b"".join(parts)
    if type(value) is tuple:
        parts = [b"t", _encode_length(len(value))]
        parts.extend(_encode_native_value(item) for item in value)
        return b"".join(parts)
    if isinstance(value, Mapping):
        items = sorted(value.items(), key=lambda item: item[0].encode("utf-8"))
        parts = [b"m", _encode_length(len(items))]
        for key, item in items:
            key_payload = key.encode("utf-8")
            parts.extend(
                (
                    _encode_length(len(key_payload)),
                    key_payload,
                    _encode_native_value(item),
                )
            )
        return b"".join(parts)
    raise TypeError("native codec received a value outside NativeValueV1")


class _NativeCodecReader:
    __slots__ = ("_payload", "_position")

    def __init__(self, payload: bytes) -> None:
        self._payload = payload
        self._position = 0

    @property
    def at_end(self) -> bool:
        return self._position == len(self._payload)

    def take(self, size: int) -> bytes:
        end = self._position + size
        if size < 0 or end > len(self._payload):
            raise ValueError("native codec payload is truncated")
        result = self._payload[self._position : end]
        self._position = end
        return result

    def length(self) -> int:
        return int.from_bytes(self.take(8), "big", signed=False)

    def value(self) -> NativeValueV1:
        tag = self.take(1)
        if tag == b"n":
            return None
        if tag == b"b":
            raw = self.take(1)
            if raw not in (b"\x00", b"\x01"):
                raise ValueError("native bool codec payload is invalid")
            return raw == b"\x01"
        if tag == b"i":
            return _integer_from_text(self.take(self.length()).decode("ascii"))
        if tag == b"f":
            return unpack("!d", self.take(8))[0]
        if tag == b"d":
            sign_raw = self.take(1)[0]
            if sign_raw not in (0, 1):
                raise ValueError("native Decimal sign is invalid")
            digits = tuple(self.take(self.length()))
            if any(digit > 9 for digit in digits):
                raise ValueError("native Decimal digit is invalid")
            exponent_text = self.take(self.length()).decode("ascii")
            sign_prefix = "-" if sign_raw else ""
            diagnostic = "".join(str(digit) for digit in digits)
            if exponent_text == "F":
                if digits != (0,):
                    raise ValueError("native Infinity Decimal payload is invalid")
                return Decimal(f"{sign_prefix}Infinity")
            if exponent_text == "n":
                return Decimal(f"{sign_prefix}NaN{diagnostic}")
            if exponent_text == "N":
                return Decimal(f"{sign_prefix}sNaN{diagnostic}")
            exponent = int(exponent_text)
            return Decimal((sign_raw, digits, exponent))
        if tag == b"z":
            text = self.take(self.length()).decode("ascii")
            value = datetime.fromisoformat(text)
            if (
                value.tzinfo is None
                or value.utcoffset() != UTC.utcoffset(value)
                or value.isoformat() != text
            ):
                raise ValueError("native datetime codec payload is not canonical UTC")
            return value
        if tag == b"s":
            return self.take(self.length()).decode("utf-8")
        if tag == b"y":
            return self.take(self.length())
        if tag == b"l":
            return [self.value() for _ in range(self.length())]
        if tag == b"t":
            return tuple(self.value() for _ in range(self.length()))
        if tag == b"m":
            result: dict[str, NativeValueV1] = {}
            for _ in range(self.length()):
                key = self.take(self.length()).decode("utf-8")
                if key in result:
                    raise ValueError("native mapping codec contains a duplicate key")
                result[key] = self.value()
            return result
        raise ValueError("native codec contains an unknown type tag")


def _encode_native_record(value: Mapping[str, NativeValueV1]) -> bytes:
    return _NATIVE_CODEC_PREFIX + _encode_native_value(cast(NativeValueV1, value))


def _decode_native_record(value: object) -> Mapping[str, NativeValueV1]:
    if isinstance(value, memoryview):
        payload = value.tobytes()
    elif type(value) is bytes:
        payload = value
    else:
        raise TypeError("native_record did not round-trip as PostgreSQL bytea")
    if not payload.startswith(_NATIVE_CODEC_PREFIX):
        raise ValueError("native_record codec version is not supported")
    reader = _NativeCodecReader(payload[len(_NATIVE_CODEC_PREFIX) :])
    decoded = reader.value()
    if not reader.at_end:
        raise ValueError("native_record codec contains trailing bytes")
    if not isinstance(decoded, Mapping):
        raise ValueError("native_record codec root must be a mapping")
    return cast(Mapping[str, NativeValueV1], decoded)
