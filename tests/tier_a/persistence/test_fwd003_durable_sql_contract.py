from __future__ import annotations

from nvda_desk.persistence.durable_sql import (
    DurableSqliteStore,
    drift_for,
    high_pad_for,
    low_pad_for,
    volume_for,
)


def test_durable_sql_store_creates_schema_and_seeds_bounded_dev_rows(tmp_path) -> None:
    db_path = tmp_path / "nvda10.sqlite3"
    store = DurableSqliteStore(db_path)

    store.initialise_schema()
    store.seed_dev_data(symbol="NVDA", session_ids=("2026-05-15",))

    bars = store.list_intraday_bars()
    option_snapshots = store.list_option_snapshots()
    sessions = store.list_session_calendars()

    assert bars[0]["symbol"] == "NVDA"
    assert bars[0]["close_price"] > bars[0]["open_price"]
    assert option_snapshots[0]["underlying_symbol"] == "NVDA"
    assert sessions == [
        {"session_id": "2026-05-15", "trade_date": "2026-05-15", "session_state": "regular"}
    ]


def test_durable_seed_helpers_are_deterministic() -> None:
    assert drift_for(0) == 0.25
    assert high_pad_for(1) == 0.75
    assert low_pad_for(1) == 0.45
    assert volume_for(2) == 1200
