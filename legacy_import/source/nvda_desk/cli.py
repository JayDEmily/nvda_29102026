from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import typer
from sqlalchemy.orm import Session

from nvda_desk.config import get_settings
from nvda_desk.db import create_engine_from_url, create_schema, seed_dev_data
from nvda_desk.db.session import create_session_factory
from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.schemas.overnight import OvernightCarryReplayFromMarketInput
from nvda_desk.services.carry_market import OvernightCarryMarketService
from nvda_desk.services.carry_replay import OvernightCarryReplayService
from nvda_desk.services.events import EventsService
from nvda_desk.services.execution_records import ExecutionRecordsService
from nvda_desk.services.legacy_extraction import LegacyExtractionService
from nvda_desk.services.market_state import MarketStateService
from nvda_desk.services.review_packets import ReviewPacketService

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command("init-db")
def init_db() -> None:
    settings = get_settings()
    _ensure_parent_dir(settings.database_url)
    create_schema(settings.database_url)
    typer.echo(f"initialized_database={settings.database_url}")


@app.command("seed-dev")
def seed_dev() -> None:
    settings = get_settings()
    _ensure_parent_dir(settings.database_url)
    create_schema(settings.database_url)
    engine = create_engine_from_url(settings.database_url)
    with Session(engine) as session:
        summary = seed_dev_data(session)
    typer.echo(
        "DevSeedSummary("
        f"instrument_count={summary.instrument_count}, "
        f"bar_count={summary.bar_count}, "
        f"option_snapshot_count={summary.option_snapshot_count}"
        ")"
    )


@app.command("legacy-source-inventory")
def legacy_source_inventory() -> None:
    service = LegacyExtractionService(Path(__file__).resolve().parents[2])
    typer.echo(json.dumps(service.inventory_summary(), indent=2, sort_keys=True))


@app.command("legacy-fixture-summary")
def legacy_fixture_summary() -> None:
    service = LegacyExtractionService(Path(__file__).resolve().parents[2])
    typer.echo(json.dumps(service.fixture_summary(), indent=2, sort_keys=True))


@app.command("carry-replay")
def carry_replay(
    evaluation_ts: str = typer.Option("2026-03-18T17:29:00Z"),
    symbol: str = typer.Option("NVDA"),
) -> None:
    settings = get_settings()
    session_factory = create_session_factory(settings.database_url)
    classifier = SessionClockClassifier(settings)
    replay_service = OvernightCarryReplayService(
        session_factory,
        OvernightCarryMarketService(
            session_factory,
            classifier,
            MarketStateService(classifier, session_factory=session_factory),
        ),
    )
    result = replay_service.replay_from_market(
        OvernightCarryReplayFromMarketInput(
            symbol=symbol,
            evaluation_ts=datetime.fromisoformat(evaluation_ts.replace("Z", "+00:00")),
            asia_precursor_composite=0.25,
            risk_budget_remaining_pct=35.0,
            gross_exposure_pct=10.0,
            open_orders_count=0,
        )
    )
    typer.echo(result.model_dump_json(indent=2))


@app.command("review-daily-packet")
def review_daily_packet(
    report_date: str = typer.Option("2026-03-18"),
    symbol: str = typer.Option("NVDA"),
) -> None:
    settings = get_settings()
    session_factory = create_session_factory(settings.database_url)
    service = ReviewPacketService(
        session_factory,
        ExecutionRecordsService(session_factory),
        EventsService(session_factory),
    )
    packet = service.daily_packet(
        report_date=datetime.fromisoformat(report_date).date(), symbol=symbol
    )
    typer.echo(packet.model_dump_json(indent=2))


def _ensure_parent_dir(database_url: str) -> None:
    prefix = "sqlite+pysqlite:///"
    if database_url.startswith(prefix):
        db_path = Path(database_url.removeprefix(prefix))
        db_path.parent.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    app()
