from __future__ import annotations

from decimal import Decimal

import pytest

from nvda_desk.analysis.replay.sidecar import (
    EvaluationRunService,
    PromotionDecisionService,
    ResearchNoteService,
)
from nvda_desk.testing.cognition_fixtures import (
    CognitionRuntimeFixture,
    stressed_runtime_fixture,
    supportive_runtime_fixture,
)
from nvda_desk.testing.fixture_corpus import (
    LegacyOptionFixtureRow,
    LegacyVwapCase,
    load_legacy_option_fixture_rows,
    load_legacy_vwap_cases,
    parse_date_optional,
    parse_date_required,
    parse_decimal_optional,
    parse_decimal_required,
    parse_int_optional,
)


def test_fixture_parsers_are_strict_and_optional_where_named() -> None:
    assert parse_date_required("2026-05-15").isoformat() == "2026-05-15"
    assert parse_date_optional("") is None
    assert parse_decimal_required("1.25") == Decimal("1.25")
    assert parse_decimal_optional(None) is None
    assert parse_int_optional("7") == 7

    with pytest.raises(ValueError, match="trade_date"):
        parse_date_required("", field_name="trade_date")
    with pytest.raises(ValueError, match="price"):
        parse_decimal_required("", field_name="price")


def test_legacy_fixture_loaders_parse_csv_and_jsonl(tmp_path) -> None:
    option_csv = tmp_path / "options.csv"
    option_csv.write_text(
        "trade_date,expiry,strike,option_type,bid,ask,volume\n"
        "2026-05-15,2026-06-19,120.5,call,1.10,1.20,100\n",
        encoding="utf-8",
    )
    vwap_jsonl = tmp_path / "vwap.jsonl"
    vwap_jsonl.write_text(
        '{"case_id":"v1","trade_date":"2026-05-15","vwap":"125.50","volume":1000}\n',
        encoding="utf-8",
    )

    option_rows = load_legacy_option_fixture_rows(option_csv)
    vwap_cases = load_legacy_vwap_cases(vwap_jsonl)

    assert option_rows == [
        LegacyOptionFixtureRow(
            trade_date=parse_date_required("2026-05-15"),
            expiry=parse_date_required("2026-06-19"),
            strike=Decimal("120.5"),
            option_type="call",
            bid=Decimal("1.10"),
            ask=Decimal("1.20"),
            volume=100,
        )
    ]
    assert vwap_cases == [
        LegacyVwapCase(
            case_id="v1",
            trade_date=parse_date_required("2026-05-15"),
            vwap=Decimal("125.50"),
            volume=1000,
        )
    ]


def test_cognition_fixtures_are_named_test_only_specimens() -> None:
    supportive = supportive_runtime_fixture()
    stressed = stressed_runtime_fixture()

    assert isinstance(supportive, CognitionRuntimeFixture)
    assert supportive.fixture_id == "supportive_runtime"
    assert supportive.market_regime_context == "supportive"
    assert stressed.fixture_id == "stressed_runtime"
    assert stressed.risk_posture == "stressed"


def test_research_promotion_and_evaluation_sidecars_are_append_only_and_copy_safe() -> None:
    research = ResearchNoteService()
    research.create_research_note("note-1", title="Observed", body="Bounded note")
    research.list_research_notes()[0]["title"] = "mutated"
    assert research.list_research_notes()[0]["title"] == "Observed"

    promotions = PromotionDecisionService()
    promotions.create_promotion_decision(
        "decision-1", candidate_id="candidate-a", decision="promote", rationale="stable"
    )
    assert promotions.list_promotion_decisions()[0]["decision"] == "promote"

    runs = EvaluationRunService()
    runs.record_evaluation_run("eval-1", kind="walk_forward", payload={"score": 1})
    runs.record_experiment_run("exp-1", kind="fragility", payload={"scenario": "baseline"})
    assert runs.list_evaluation_runs()[0]["run_id"] == "eval-1"
    assert runs.list_experiment_runs()[0]["run_id"] == "exp-1"
