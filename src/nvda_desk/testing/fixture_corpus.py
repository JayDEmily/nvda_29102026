from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any

LEGACY_OPTION_FIXTURE_PATH = Path("fixtures/legacy/options.csv")
LEGACY_VWAP_CASES_PATH = Path("fixtures/legacy/vwap_cases.jsonl")


@dataclass(frozen=True, slots=True)
class LegacyOptionFixtureRow:
    trade_date: date
    expiry: date
    strike: Decimal
    option_type: str
    bid: Decimal | None = None
    ask: Decimal | None = None
    volume: int | None = None


@dataclass(frozen=True, slots=True)
class LegacyVwapCase:
    case_id: str
    trade_date: date
    vwap: Decimal
    volume: int | None = None


def load_legacy_option_fixture_rows(
    path: Path | str = LEGACY_OPTION_FIXTURE_PATH,
) -> list[LegacyOptionFixtureRow]:
    rows: list[LegacyOptionFixtureRow] = []
    with Path(path).open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            rows.append(
                LegacyOptionFixtureRow(
                    trade_date=parse_date_required(raw.get("trade_date"), field_name="trade_date"),
                    expiry=parse_date_required(raw.get("expiry"), field_name="expiry"),
                    strike=parse_decimal_required(raw.get("strike"), field_name="strike"),
                    option_type=str(raw.get("option_type", "")).strip(),
                    bid=parse_decimal_optional(raw.get("bid"), field_name="bid"),
                    ask=parse_decimal_optional(raw.get("ask"), field_name="ask"),
                    volume=parse_int_optional(raw.get("volume"), field_name="volume"),
                )
            )
    return rows


def load_legacy_vwap_cases(path: Path | str = LEGACY_VWAP_CASES_PATH) -> list[LegacyVwapCase]:
    cases: list[LegacyVwapCase] = []
    for line_number, raw_line in enumerate(
        Path(path).read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not raw_line.strip():
            continue
        payload = json.loads(raw_line)
        cases.append(
            LegacyVwapCase(
                case_id=_required_text(payload.get("case_id"), f"case_id line {line_number}"),
                trade_date=parse_date_required(payload.get("trade_date"), field_name="trade_date"),
                vwap=parse_decimal_required(payload.get("vwap"), field_name="vwap"),
                volume=parse_int_optional(payload.get("volume"), field_name="volume"),
            )
        )
    return cases


def parse_date_required(value: Any, *, field_name: str = "date") -> date:
    token = _required_text(value, field_name)
    try:
        return date.fromisoformat(token)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be ISO date") from exc


def parse_date_optional(value: Any, *, field_name: str = "date") -> date | None:
    if value is None or str(value).strip() == "":
        return None
    return parse_date_required(value, field_name=field_name)


def parse_decimal_required(value: Any, *, field_name: str = "decimal") -> Decimal:
    token = _required_text(value, field_name)
    try:
        return Decimal(token)
    except Exception as exc:
        raise ValueError(f"{field_name} must be decimal") from exc


def parse_decimal_optional(value: Any, *, field_name: str = "decimal") -> Decimal | None:
    if value is None or str(value).strip() == "":
        return None
    return parse_decimal_required(value, field_name=field_name)


def parse_int_optional(value: Any, *, field_name: str = "int") -> int | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return int(str(value).strip())
    except ValueError as exc:
        raise ValueError(f"{field_name} must be integer") from exc


def _required_text(value: Any, field_name: str) -> str:
    token = "" if value is None else str(value).strip()
    if not token:
        raise ValueError(f"{field_name} must be non-empty")
    return token
