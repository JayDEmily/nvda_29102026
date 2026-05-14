from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date as dt_date
from decimal import Decimal
from pathlib import Path


@dataclass(frozen=True)
class LegacyOptionFixtureRow:
    source_document: str
    source_pages: str
    date: dt_date
    expiry: dt_date | None
    option_type: str
    strike: Decimal
    bid: Decimal | None
    ask: Decimal | None
    last: Decimal | None
    volume: int | None
    open_interest: int | None
    iv: Decimal | None
    delta: Decimal | None
    gamma: Decimal | None
    delta_change: Decimal | None
    provenance: str
    confidence: str


@dataclass(frozen=True)
class LegacyVWAPCase:
    fixture_id: str
    symbol: str
    case_date: dt_date
    source_document: str
    source_pages: list[int]
    provenance: list[str]
    confidence: str
    canonical_truth: bool
    admitted_use: str
    summary: str
    close_distance_to_vwap_pct: float
    vix_level: float
    vvix_level: float
    asia_precursor_composite: float
    expected_guardrail_bias: str


REPO_ROOT = Path(__file__).resolve().parents[2]
OPTION_FIXTURE_PATH = (
    REPO_ROOT / "fixtures" / "legacy" / "options_snapshots" / "options_data_csv_output_admitted.csv"
)
VWAP_CASE_FIXTURE_PATH = REPO_ROOT / "fixtures" / "legacy" / "vwap_cases" / "admitted_cases.jsonl"


def load_legacy_option_fixture_rows(
    path: Path | None = None,
) -> list[LegacyOptionFixtureRow]:
    fixture_path = path or OPTION_FIXTURE_PATH
    with fixture_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [
            LegacyOptionFixtureRow(
                source_document=(row.get("source_document") or "unknown").strip() or "unknown",
                source_pages=(row.get("source_pages") or "").strip(),
                date=_parse_date_required(row.get("date")),
                expiry=_parse_date_optional(row.get("expiry")),
                option_type=(row.get("option_type") or "").strip(),
                strike=_parse_decimal_required(row.get("strike")),
                bid=_parse_decimal_optional(row.get("bid")),
                ask=_parse_decimal_optional(row.get("ask")),
                last=_parse_decimal_optional(row.get("last")),
                volume=_parse_int_optional(row.get("volume")),
                open_interest=_parse_int_optional(row.get("open_interest")),
                iv=_parse_decimal_optional(row.get("iv")),
                delta=_parse_decimal_optional(row.get("delta")),
                gamma=_parse_decimal_optional(row.get("gamma")),
                delta_change=_parse_decimal_optional(row.get("delta_change")),
                provenance=(row.get("provenance") or "unknown").strip() or "unknown",
                confidence=(row.get("confidence") or "unknown").strip() or "unknown",
            )
            for row in reader
        ]


def load_legacy_vwap_cases(path: Path | None = None) -> list[LegacyVWAPCase]:
    fixture_path = path or VWAP_CASE_FIXTURE_PATH
    cases: list[LegacyVWAPCase] = []
    with fixture_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            raw = json.loads(line)
            cases.append(
                LegacyVWAPCase(
                    fixture_id=str(raw["fixture_id"]),
                    symbol=str(raw["symbol"]),
                    case_date=dt_date.fromisoformat(str(raw["case_date"])),
                    source_document=str(raw["source_document"]),
                    source_pages=[int(item) for item in raw["source_pages"]],
                    provenance=[str(item) for item in raw["provenance"]],
                    confidence=str(raw["confidence"]),
                    canonical_truth=bool(raw["canonical_truth"]),
                    admitted_use=str(raw["admitted_use"]),
                    summary=str(raw["summary"]),
                    close_distance_to_vwap_pct=float(raw["close_distance_to_vwap_pct"]),
                    vix_level=float(raw["vix_level"]),
                    vvix_level=float(raw["vvix_level"]),
                    asia_precursor_composite=float(raw["asia_precursor_composite"]),
                    expected_guardrail_bias=str(raw["expected_guardrail_bias"]),
                )
            )
    return cases


def _parse_date_required(value: str | None) -> dt_date:
    cleaned = (value or "").strip()
    if not cleaned:
        raise ValueError("missing required date")
    return dt_date.fromisoformat(cleaned)


def _parse_date_optional(value: str | None) -> dt_date | None:
    cleaned = (value or "").strip()
    return dt_date.fromisoformat(cleaned) if cleaned else None


def _parse_decimal_required(value: str | None) -> Decimal:
    cleaned = (value or "").strip()
    if not cleaned:
        raise ValueError("missing required decimal")
    return Decimal(cleaned)


def _parse_decimal_optional(value: str | None) -> Decimal | None:
    cleaned = (value or "").strip()
    return Decimal(cleaned) if cleaned else None


def _parse_int_optional(value: str | None) -> int | None:
    cleaned = (value or "").strip()
    return int(cleaned) if cleaned else None
